# GitHub Forks Sync 改進設計

## 背景

目前 workflow 手動輸入單一帳號 → 下載外部腳本 → sync 全部 fork。
目標：支援多帳號、定時排程、可設定化管理，同時保持公共工具與消費者分離。

## 角色分離

| 專案 | 角色 |
|------|------|
| LoveDoLove/Github-Forks-Sync-Manager | 公共工具提供者：reusable workflow + Python 腳本 |
| 各消費者 repo（如 LoveDoLove） | 設定自己的 vars/secrets，呼叫 reusable workflow |

## 架構

```
Github-Forks-Sync-Manager                   消費者 (e.g., LoveDoLove)
 ┌─────────────────────┐                   ┌──────────────────────┐
 │ workflows/           │                   │ .github/workflows/   │
 │   forks-sync.yml     │◄── reusable ────│   forks-sync.yml     │
 │   (workflow_call)    │      call        │   (cron + dispatch)  │
 │                      │                   │                      │
 │ scripts/             │                   │ vars:                │
 │   github_forks_sync  │                   │   FORK_SYNC_ACCOUNTS │
 │   .py                │                   │ secrets:             │
 └─────────────────────┘                   │   GH_PAT             │
                                            └──────────────────────┘
```

## 檔案變更

### Github-Forks-Sync-Manager

#### `workflows/github-forks-sync.yml`（改用 workflow_call）

```yaml
name: Fork Sync (Reusable)

on:
  workflow_call:
    inputs:
      accounts:
        description: "Comma-separated GitHub accounts to sync"
        required: true
        type: string
    secrets:
      GH_PAT:
        required: true

jobs:
  sync-forks:
    runs-on: ubuntu-latest
    env:
      GH_TOKEN: ${{ secrets.GH_PAT }}
      FORK_SYNC_ACCOUNTS: ${{ inputs.accounts }}
    steps:
      - uses: actions/setup-python@v5
        with:
          python-version: "3.x"
      - run: pip install aiohttp
      - run: curl -sSL -o github_forks_sync.py
          https://raw.githubusercontent.com/LoveDoLove/Github-Forks-Sync-Manager/main/scripts/github_forks_sync.py
      - run: python -u github_forks_sync.py
```

#### `scripts/github_forks_sync.py`

- 支援多帳號：從 `FORK_SYNC_ACCOUNTS` env 讀取（逗號或換行分隔）
- 向後相容：若無 `FORK_SYNC_ACCOUNTS`，fallback 到 `GH_ACCOUNT`
- 逐帳號處理：fetch 所有 fork → 呼叫 `POST /repos/{owner}/{name}/merge-upstream`
- 單帳號失敗不影響其他帳號
- `asyncio.Semaphore(5)` 控制並發
- 輸出：`[OK]` / `[FAIL]` / `[SKIP]` / `[CONF]`

### LoveDoLove（消費者）

#### `.github/workflows/github-forks-sync.yml`

```yaml
name: Fork Sync

on:
  workflow_dispatch:
    inputs:
      github_account:
        description: "Override: sync only this account"
        required: false
        default: ""
  schedule:
    - cron: '0 0 * * *'

jobs:
  sync-forks:
    uses: LoveDoLove/Github-Forks-Sync-Manager/.github/workflows/github-forks-sync.yml@main
    with:
      accounts: ${{ inputs.github_account || vars.FORK_SYNC_ACCOUNTS }}
    secrets:
      GH_PAT: ${{ secrets.GH_PAT }}
```

#### 消費者需自行設定

- **Variables**: `FORK_SYNC_ACCOUNTS` = `org1,org2,org3`
- **Secrets**: `GH_PAT` = Personal Access Token

## 觸發邏輯

| 觸發方式 | `github_account` | `accounts` 傳入值 |
|----------|-----------------|-------------------|
| schedule | 不存在 | `vars.FORK_SYNC_ACCOUNTS` |
| 手動沒填 | `""` | `vars.FORK_SYNC_ACCOUNTS` |
| 手動有填 | `"某帳號"` | `"某帳號"` |

## 注意事項

- merge-upstream 回傳 409（conflict）時腳本輸出 `[CONF]`，需手動處理
- 確保 GH_PAT 有 `repo` 和 `workflow` scope
