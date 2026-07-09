# AI Agent 身份定义与行为规范

## 身份

你是 **LoveDoLove** 的 AI 编程助手（opencode）。LoveDoLove（Chong Jun Xiang）是一位全栈开发者、云基础设施与 DevOps 工程师。

## 仓库结构

```
LoveDoLove/                          # GitHub Profile Monorepo
├── README.md                        # GitHub 个人主页 README（Skills精简化、Contribution折叠）
├── README-Sponsor.md                # GitHub Sponsors 简化版（38行）
├── portfolio-website/               # Astro SSG + Cloudflare Workers 静态个人网站
│   ├── astro.config.mjs             # Astro 配置
│   ├── wrangler.jsonc               # Workers 部署配置（assets: ./dist）
│   ├── package.json                 # Astro v7 + wrangler v4.107.1
│   ├── src/
│   │   ├── pages/index.astro        # 主页面（组合9个组件）
│   │   └── components/
│   │       ├── Header.astro         # 头像（GitHub avatar URL）+ 简介
│   │       ├── About.astro          # 自我介绍 + 8项成就
│   │       ├── Stats.astro          # Trophy/Stats/TopLangs/WakaTime/Views
│   │       ├── Skills.astro         # skillicons.dev 横幅
│   │       ├── Certifications.astro # 5个AWS/Cisco徽章
│   │       ├── FeaturedProjects.astro # 10个Featured Projects
│   │       ├── ThreeDeeSection.astro  # 3D贡献图
│   │       ├── Connect.astro        # 8个社交链接
│   │       └── Footer.astro
│   └── public/                      # 静态资源（profile.png已删除，改用GitHub avatar）
├── .github/
│   ├── scripts/
│   │   └── sync_top_starred_projects.py  # 本地脚本（避免远程429）
│   ├── workflows/                   # 5个 CI/CD 自动流程
│   └── FUNDING.yml                  # 仅启用 GitHub Sponsors
├── AGENTS.md                        # ← 本文件：AI 身份定义
├── MEMORY.md                        # 长期记忆
├── memory/                          # 每日日志 + 任务追踪
│   ├── tasks.md
│   └── YYYY-MM-DD.md
└── README.md                        # GitHub 个人主页（核心输出）
```

## 核心项目

### 1. GitHub Profile (README.md)
- **作用**：GitHub 个人主页展示墙
- **内容**：简介、GitHub 统计 Widgets（Trophy/Stats/TopLangs/WakaTime/Views/3D贡献图）、Featured Projects（10个项目）、Skills（5大类技能）、Certifications（5个AWS/Cisco徽章）、Achievements（8项成就）、Connect（8个链接）
- **Widget API 地址**（已全部替换为可用的替代品）：
  - Trophy: `personal-trophy.vercel.app`
  - Stats/TopLangs/WakaTime: `github-stats-extended.vercel.app`
- **自动化 Featured Projects**：通过 `sync-top-starred-projects.yml` 每日运行，从 `LoveDoLove/Github-Profile-Manager` 下载 Python 脚本重写 README
- **3D 贡献图**：通过 `generate-3d-contribution-graph.yml` 每日生成 10 个 SVG

### 2. portfolio-website (Cloudflare Workers)
- **类型**：纯静态单页 HTML + CSS，无 JS/框架
- **包管理**：pnpm 11.9.0，wrangler v4.107.1
- **部署**：`pnpm run deploy`
- **URL**：`https://portfolio.lovedolove.qzz.io`（需 Cloudflare Dashboard 调整安全等级以解除 403）
- **数据来源**：嵌入外部 API 图片（GitHub Stats、Trophy、WakaTime 等）

### 3. CI/CD Workflows (5 个)

| 流程 | 触发 | 功能 |
|---|---|---|
| `generate-3d-contribution-graph.yml` | 每日 UTC 00:00 + 手动 | 生成 10 种 3D 贡献图 SVGs |
| `sync-top-starred-projects.yml` | 每日 UTC 00:00 + 手动 | 按 Star 数同步 README Featured Projects |
| `github-forks-sync.yml` | 仅手动 | 同步所有 Fork 仓库与上游 |
| `cleanup-failed-runs.yml` | 仅手动 | 清理失败的 Action 记录 |
| `cleanup-all-runs.yml` | 仅手动 | 清理全部 Action 记录 |

### 4. AI Agent 技能包（全局）
- **位置**：`C:\Users\LoveDoLove\.agents\skills\`
- **来源**：全部从 `farmage/opencode-skills`（MIT，53 stars）克隆，不自创
- **已安装**：9 个技能包（详见 MEMORY.md）

## 行为规范

1. **README.md 与 index.html** 保持信息同步
2. **FEATURED_PROJECTS 标记区**：仅 `index.html` 保留 `<!-- FEATURED_PROJECTS_START/END -->`；README 由外部脚本整体替换
3. **profile-3d-contrib/**：永不手动修改（自动生成）
4. **AI 记忆机制**：每次对话先读 AGENTS.md 恢复身份，读 tasks.md 恢复工作状态
5. **任务记录**：在 `memory/YYYY-MM-DD.md` 记录每日工作，在 `memory/tasks.md` 追踪待办
6. **技能包**：只从 GitHub 开源仓库安装到全局 `C:\Users\LoveDoLove\.agents\skills\`，不自创
7. **sync_top_starred_projects.py**：已内嵌到 `.github/scripts/`，workflow 不再远程下载（修复 429）

## 技术栈要点

- **托管**：Cloudflare Workers (Wrangler v4.107.1)
- **包管理**：pnpm 11.9.0
- **前端**：Astro SSG（组件化，无 JS 运行时）
- **CI/CD**：GitHub Actions
- **Widget API**：`github-stats-extended.vercel.app`（Stats/TopLangs/WakaTime）、`personal-trophy.vercel.app`（Trophy）