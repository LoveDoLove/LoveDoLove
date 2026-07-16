AI 長期記憶與專案約定 (AI Long-Term Memory & Project Conventions)

本文件是本倉庫 AI 代理人的「長期記憶與專案約定中心」。每一次與 AI 開始新對話時，AI 必須首先讀取本檔案與 AGENTS.md，以恢復對當前專案、技術棧、用戶偏好與持久約定的全面認知。

1. 專案基礎設定 (Project Context)

本節記錄當前專案的根本設定，請根據實際情況進行動態更新：

應用名稱 (App Name): LoveDoLove (Chong Jun Xiang) — GitHub Profile Monorepo

專案類型 (Project Type): GitHub 個人首頁 Monorepo + 靜態個人作品集網站

資料庫 (App Database): 無 (純靜態站點，無後端資料庫)

前端技術棧 (Frontend): Astro SSG v7 (元件化 Astro 元件，無 JS Runtime)

後端技術棧 (Backend): 無 (靜態網站，透過 Cloudflare Workers 託管)

主權部署環境 (Deployment): Cloudflare Workers (Wrangler v4.107.1 + pnpm 11.9.0)

CI/CD: GitHub Actions (5 個自動化流程)

網站網址 (Site URL): https://portfolio.lovedolove.qzz.io

2. 使用者偏好與互動慣例 (User Preferences)

溝通語言：預設使用 繁體中文 (Traditional Chinese) 進行所有對話、架構解釋與日誌記錄（除程式碼註解、變數命名與技術文檔採用英文）。

程式碼風格：

追求極簡與健壯性，嚴禁過度設計。

優先使用型別安全的 TypeScript 與現代 ES 語法。

必須符合內置技能包 karpathy-guidelines 的編碼行為準則。

人機協作 (HITL) 偏好：

在涉及「破壞性寫入資料庫」、「線上環境部署」、「敏感金鑰修改」等操作前，AI 必須暫停並明確徵求使用者批准。

3. 倉庫結構與核心專案知識 (Repository Structure & Knowledge Base)

3.1 目錄結構

LoveDoLove/
├── README.md                        # GitHub 個人首頁 README
├── README-Sponsor.md                # GitHub Sponsors 精簡版
├── portfolio-website/               # Astro SSG + Cloudflare Workers 靜態個人網站
│   ├── astro.config.mjs             # Astro 配置 (site: portfolio.lovedolove.qzz.io)
│   ├── wrangler.jsonc               # Workers 部署配置 (assets: ./dist)
│   ├── package.json                 # Astro v7 + wrangler v4.107.1
│   ├── src/
│   │   ├── pages/index.astro        # 主頁面 (組合 9 個元件)
│   │   └── components/
│   │       ├── Header.astro         # 頭像 (GitHub avatar URL) + 簡介
│   │       ├── About.astro          # 自我介紹 + 8 項成就
│   │       ├── Stats.astro          # Trophy/Stats/TopLangs/WakaTime/Views
│   │       ├── Skills.astro         # skillicons.dev 橫幅
│   │       ├── Certifications.astro # 5 個 AWS/Cisco 徽章
│   │       ├── FeaturedProjects.astro # 10 個精選專案
│   │       ├── ThreeDeeSection.astro  # 3D 貢獻圖
│   │       ├── Connect.astro        # 8 個社交連結
│   │       └── Footer.astro
│   └── public/
├── profile-3d-contrib/              # 3D 貢獻圖輸出目錄（永不手動修改，自動生成）
├── .github/
│   ├── scripts/
│   │   └── sync_top_starred_projects.py  # 精選專案同步腳本（內嵌，避免遠端 429）
│   ├── workflows/                   # 5 個 CI/CD 自動流程
│   └── FUNDING.yml                  # 僅啟用 GitHub Sponsors
├── AGENTS.md                        # AI 身份定義與行為規範
├── MEMORY.md                        # 本文件：長期記憶
├── memory/                          # 每日日誌 + 任務追蹤
│   ├── tasks.md
│   └── YYYY-MM-DD.md
└── MIGRATION.md                     # 遷移指南

3.2 核心專案說明

(1) GitHub Profile (README.md)
- 作用：GitHub 個人首頁展示牆
- 內容：簡介、GitHub 統計 Widgets（Trophy/Stats/TopLangs/WakaTime/Views/3D貢獻圖）、Featured Projects（10 個專案）、Skills（5 大類技能）、Certifications（5 個 AWS/Cisco 徽章）、Achievements（8 項成就）、Connect（8 個連結）
- Widget API 位址：
  - Trophy: personal-trophy.vercel.app
  - Stats/TopLangs/WakaTime: github-stats-extended.vercel.app
- 自動化 Featured Projects：透過 sync-top-starred-projects.yml 每日執行
- 3D 貢獻圖：透過 generate-3d-contribution-graph.yml 每日生成 10 個 SVG
- README 不含 FEATURED_PROJECTS 標記，整個 Featured Projects 段落由外部腳本整體替換

(2) portfolio-website (Cloudflare Workers)
- 框架：Astro SSG v7
- 包管理：pnpm 11.9.0，wrangler v4.107.1
- 部署指令：pnpm run deploy（執行 astro build && wrangler deploy）
- 資料來源：嵌入外部 API 圖片（GitHub Stats、Trophy、WakaTime 等）
- 已知問題：portfolio.lovedolove.qzz.io 返回 403 (Cf-Mitigated: challenge)，需在 Cloudflare Dashboard 調整安全等級為 Low 或關閉 Bot Fight Mode
- 頭像使用 GitHub avatar URL（avatars.githubusercontent.com/u/67772009）

(3) CI/CD Workflows (5 個)
| 流程 | 觸發 | 功能 |
|---|---|---|
| generate-3d-contribution-graph.yml | 每日 UTC 00:00 + 手動 | 生成 10 種 3D 貢獻圖 SVGs |
| sync-top-starred-projects.yml | 每日 UTC 00:00 + 手動 | 按 Star 數同步 README Featured Projects |
| github-forks-sync.yml | 僅手動 | 同步所有 Fork 倉庫與上游 |
| cleanup-failed-runs.yml | 僅手動 | 清理失敗的 Action 記錄 |
| cleanup-all-runs.yml | 僅手動 | 清理全部 Action 記錄 |

3.3 AI Agent 技能包
- 位置：C:\Users\LoveDoLove\.agents\skills\
- 來源：從 GitHub 開源社群（如 github.com/fields/...、farmage/opencode-skills 等）或 Skills.sh 獲取
- 政策：嚴禁 AI 自行憑空編寫技能包。必須優先搜尋開源 Skills 並統一安裝至全局 %USERPROFILE%\.agents\skills\

4. 記憶同步與更新協議 (Memory Sync Protocol)

為了確保 AI 的記憶在跨對話中永不丟失且持續演進，AI 助手必須遵循以下同步機制：

4.1 每日日誌機制 (Daily Logs YYYY-MM-DD.md)

每次對話結束前，AI 必須將當前的關鍵決策、面臨的問題與下一步計劃，摘要寫入 memory/YYYY-MM-DD.md（以當前日期命名）。

日誌格式標準：

# 每日工作日誌: YYYY-MM-DD
* **今日進度**: [簡述完成了哪些功能/修復了哪些 Bug]
* **關鍵決策**: [例如切換了某個 API、更新了某個 Schema]
* **遭遇阻礙**: [遇到的技術難題與解決路徑]
* **明日計劃**: [待續的具體工作事項]


4.2 任務追蹤機制 (tasks.md)

所有的跨對話待辦事項必須維護在 memory/tasks.md 中。

任務分為三個看板狀態：[ ] Backlog（待辦）、[>] In Progress（進行中）、[x] Completed（已完成）。

當 AI 助手完成一項任務時，必須同步更新 memory/tasks.md，並在日誌中註記。

5. 工具狀態與技能索引 (Tool State & Skill Index)

本倉庫的工具安裝狀態自動維護在 memory/tools-state.json，AI 每次對話會自動讀取並更新。

已註冊工具列表（共 7 項）：
- karpathy-guidelines (skill) — 編碼行為準則
- skillx (skill) — 技能市場搜尋與調用，每項任務都應載入
- ui-ux-pro-max (skill) — UI/UX 設計智慧：84 種風格、192 種色板、74 種字體
- context7 (mcp) — 即時程式庫文件查詢
- codebase-memory-mcp (mcp) — 程式碼知識圖譜
- opencode-wakatime (plugin) — WakaTime 使用追蹤
- superpowers (framework) — 代理人技能框架與開發方法論

如需重新檢測或安裝，請執行 repo 根目錄的 init.ps1：
.\init.ps1         # 逐項詢問安裝
.\init.ps1 --yes   # 全自動安裝
.\init.ps1 --no-install  # 只偵測狀態

6. 持久技術約定 (Persistent Rules)

安全優先原則：所有新開發的端點（Endpoints）或微服務，必須在核心邏輯外圍包裹安全認證層，貫徹 AGENTS.md 中的「受控副官防禦」。

零退化 CI/CD 承諾：凡是有新的重大業務邏輯變更，必須同步在 tests/ 下建立對應的斷言測試，以利後續自動化品質飛輪（AgentOps）的集成。

技能包（Agent Skills）優先：解決特定領域問題時（例如：SEO 審計、性能優化、程式碼重構），先檢索本地 .agents/skills/，優先調用已有技能。

profile-3d-contrib/ 不變原則：永不手動修改 profile-3d-contrib/ 目錄內容（完全由 generate-3d-contribution-graph.yml 自動生成）。

README.md 與 portfolio-website 同步原則：README.md 與 portfolio-website/src/pages/index.astro 的資訊必須保持同步。

sync_top_starred_projects.py 已移至 Github-Forks-Sync-Manager：Workflow 改為 `uses:` 呼叫 reusable workflow，不再本地保留腳本。

7. Fork Sync 架構決策 (Architecture Decision: Fork Sync)

架構類型：公共工具提供者 + 消費者模式

公共工具 repo：LoveDoLove/Github-Forks-Sync-Manager 持有 reusable workflow ＋ Python 腳本。
消費者 repo（如 LoveDoLove）：透過 `uses:` 呼叫 reusable workflow，只需設定 `FORK_SYNC_ACCOUNTS`（vars）和 `GH_PAT`（secrets）。

觸發方式：
- 每日 UTC 00:00 定時排程（cron）
- 手動觸發可指定單一帳號覆蓋

行為要點：
- 支援多帳號（逗號或換行分隔）
- 單帳號失敗不影響其他帳號
- 並發上限 5（Semaphore）
- merge-upstream 409 conflict 標記為 [CONF] 需手動處理

8. Sync Top Starred 架構決策 (Architecture Decision: Sync Top Starred)

公共工具 repo：LoveDoLove/Github-Forks-Sync-Manager 持有 reusable workflow + 腳本。
消費者 repo（如 LoveDoLove）：透過 `uses:` 呼叫 reusable workflow，不需設定任何 inputs/secrets。
腳本透過 `GITHUB_REPOSITORY` 自動偵測帳號，`EXCLUDE_REPOS` 取自 caller 的 `vars`。
Workflow 會修改 README.md 並 push 回 caller repo。
