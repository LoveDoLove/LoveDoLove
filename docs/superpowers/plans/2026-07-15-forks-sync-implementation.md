# GitHub Forks Sync Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Refactor the fork sync system so the public tool repo provides a reusable workflow + multi-account script, and consumer repos configure accounts via GitHub Variables.

**Architecture:** Two-layer separation — Github-Forks-Sync-Manager hosts the reusable `workflow_call` workflow and the multi-account Python script; each consumer repo calls it via `uses:` with its own `vars.FORK_SYNC_ACCOUNTS` and `secrets.GH_PAT`.

**Tech Stack:** GitHub Actions (reusable workflows), Python 3 + aiohttp, GitHub REST API (merge-upstream)

## Global Constraints

- The public tool repo (`Github-Forks-Sync-Manager`) must NOT reference any consumer-specific vars/secrets
- The consumer repo (`LoveDoLove`) owns its own `vars.FORK_SYNC_ACCOUNTS` and `secrets.GH_PAT`
- Python script must be backward-compatible: support `FORK_SYNC_ACCOUNTS` (multi) and `GH_ACCOUNT` (single fallback)
- All file paths are relative to their respective repo roots

---

### Task 1: Update script in Github-Forks-Sync-Manager

**Files:**
- Modify: `scripts/github_forks_sync.py` (full rewrite)

**Interfaces:**
- Consumes: `GH_TOKEN` (env), `FORK_SYNC_ACCOUNTS` or `GH_ACCOUNT` (env)
- Produces: stdout sync log per repo per account

- [ ] **Step 1: Write the updated script**

Write the following to `scripts/github_forks_sync.py`:

```python
import os
import sys
import asyncio
import aiohttp

CONCURRENCY_LIMIT = 5


def get_accounts():
    raw = os.environ.get("FORK_SYNC_ACCOUNTS", "").strip()
    if raw:
        accounts = [a.strip() for a in raw.replace(",", "\n").split("\n") if a.strip()]
        if accounts:
            return accounts
    single = os.environ.get("GH_ACCOUNT", "").strip()
    if single:
        return [single]
    print("::error:: No accounts configured. Set FORK_SYNC_ACCOUNTS or GH_ACCOUNT.")
    sys.exit(1)


async def fetch_forks(session, headers, account):
    repos = []
    page = 1
    while True:
        url = f"https://api.github.com/users/{account}/repos?type=forks&per_page=100&page={page}"
        async with session.get(url, headers=headers) as resp:
            if resp.status != 200:
                text = await resp.text()
                print(f"  [WARN] Failed to fetch repos for {account}: {text}")
                break
            data = await resp.json()
            if not data:
                break
            repos.extend(data)
            page += 1
    return repos


async def sync_fork(session, semaphore, headers, owner, name):
    async with semaphore:
        repo_url = f"https://api.github.com/repos/{owner}/{name}"
        async with session.get(repo_url, headers=headers) as resp:
            if resp.status != 200:
                print(f"  [SKIP] {owner}/{name}: cannot get repo info ({resp.status})")
                return
            repo = await resp.json()
        if not repo.get("parent"):
            print(f"  [SKIP] {owner}/{name}: not a fork, skipping")
            return
        branch = repo["default_branch"]
        merge_url = f"https://api.github.com/repos/{owner}/{name}/merge-upstream"
        payload = {"branch": branch}
        async with session.post(merge_url, headers=headers, json=payload) as resp:
            if resp.status == 200:
                result = await resp.json()
                print(f"  [OK]   {owner}/{name} -> {result.get('message', 'synced')}")
            elif resp.status == 204:
                print(f"  [OK]   {owner}/{name} already up-to-date")
            elif resp.status == 409:
                text = await resp.text()
                print(f"  [CONF] {owner}/{name}: merge conflict, needs manual resolution")
            else:
                text = await resp.text()
                print(f"  [FAIL] {owner}/{name}: {resp.status} {text}")


async def process_account(session, headers, account, semaphore):
    print(f"\n>>> Account: {account}")
    try:
        repos = await fetch_forks(session, headers, account)
        print(f"    Found {len(repos)} fork(s)")
        if not repos:
            return
        tasks = [sync_fork(session, semaphore, headers, account, r["name"]) for r in repos]
        await asyncio.gather(*tasks)
    except Exception as e:
        print(f"  [FAIL] Account {account} error: {e}")


async def main():
    accounts = get_accounts()
    print(f"=== Fork Sync Start: {len(accounts)} account(s): {', '.join(accounts)} ===")

    token = os.environ.get("GH_TOKEN")
    if not token:
        print("::error:: GH_TOKEN environment variable is not set")
        sys.exit(1)

    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json",
    }

    semaphore = asyncio.Semaphore(CONCURRENCY_LIMIT)
    async with aiohttp.ClientSession() as session:
        for account in accounts:
            await process_account(session, headers, account, semaphore)

    print("\n=== Fork Sync Complete ===")


if __name__ == "__main__":
    asyncio.run(main())
```

- [ ] **Step 2: Verify script runs without syntax errors**

Run:
```bash
cd D:\Projects\CloudProjects\Github-Forks-Sync-Manager
python -c "import ast; ast.parse(open('scripts/github_forks_sync.py').read()); print('Syntax OK')"
```

Expected: `Syntax OK`

- [ ] **Step 3: Commit**

```bash
cd D:\Projects\CloudProjects\Github-Forks-Sync-Manager
git add scripts/github_forks_sync.py
git commit -m "feat: support multi-account via FORK_SYNC_ACCOUNTS env var"
```

---

### Task 2: Update workflow in Github-Forks-Sync-Manager to reusable

**Files:**
- Modify: `workflows/github-forks-sync.yml` (rewrite to `workflow_call`)

- [ ] **Step 1: Write the reusable workflow**

Write the following to `workflows/github-forks-sync.yml`:

```yaml
name: Fork Sync (Reusable)

on:
  workflow_call:
    inputs:
      accounts:
        description: "Comma-separated GitHub accounts to sync forks for"
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
      - name: Set Up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.x"

      - name: Install Dependencies
        run: pip install aiohttp

      - name: Download Sync Script
        run: curl -sSL -o github_forks_sync.py https://raw.githubusercontent.com/LoveDoLove/Github-Forks-Sync-Manager/refs/heads/main/scripts/github_forks_sync.py

      - name: Sync Forked Repositories
        run: python -u github_forks_sync.py
```

- [ ] **Step 2: Commit**

```bash
cd D:\Projects\CloudProjects\Github-Forks-Sync-Manager
git add workflows/github-forks-sync.yml
git commit -m "feat: convert to reusable workflow_call with accounts input"
```

- [ ] **Step 3: Push to main**

```bash
cd D:\Projects\CloudProjects\Github-Forks-Sync-Manager
git push origin main
```

---

### Task 3: Update consumer workflow in LoveDoLove

**Files:**
- Modify: `.github/workflows/github-forks-sync.yml` (rewrite as wrapper)

- [ ] **Step 1: Write the consumer wrapper workflow**

Write the following to `.github/workflows/github-forks-sync.yml`:

```yaml
name: Fork Sync

on:
  workflow_dispatch:
    inputs:
      github_account:
        description: "Override: sync only this account (leave empty for all configured)"
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

- [ ] **Step 2: Write the design spec doc**

Write to `docs/superpowers/specs/2026-07-15-forks-sync-design.md`:

```markdown
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
```

- [ ] **Step 3: Update memory files**

Append to `memory/tasks.md` with completed tasks and update `MEMORY.md` with the new architecture decision.

- [ ] **Step 4: Commit**

```bash
cd D:\Projects\WebProjects\LoveDoLove
git add .github/workflows/github-forks-sync.yml docs/superpowers/specs/2026-07-15-forks-sync-design.md memory/tasks.md MEMORY.md
git commit -m "feat: switch to reusable fork sync workflow with multi-account support"
```
