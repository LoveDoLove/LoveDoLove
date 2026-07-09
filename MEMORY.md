# AI 长期记忆

## 用户信息

- **Name**: LoveDoLove (Chong Jun Xiang)
- **Role**: Full-Stack Developer | Cloud Infrastructure & DevOps Engineer
- **Location**: Malaysia
- **Email**: v0130p5100cuboss@gmail.com
- **LinkedIn**: https://www.linkedin.com/in/chong-jun-xiang
- **YouTube**: https://www.youtube.com/@lovedolove
- **Portfolio**: https://portfolio.lovedolove.one
- **GitHub Sponsors**: https://github.com/sponsors/LoveDoLove
- **Buy Me a Coffee**: https://buymeacoffee.com/lovedolove

## 项目目标

- 维护 GitHub Profile README 作为个人展示墙（自动更新 Featured Projects + 3D 贡献图）
- 维护 portfolio-website 作为 Cloudflare Workers 静态站点，与 README 信息同步
- 自动化 CI/CD：3D 贡献图生成、项目同步（每日 UTC 00:00）、Fork 同步、Action 清理
- 所有 AI Agent 技能包必须从 GitHub 开源仓库克隆，不自创

## 持久约定

- **README.md**: Featured Projects 由外部脚本整体替换（不含 FEATURED_PROJECTS 标记）
- **index.html**: 保留 `<!-- FEATURED_PROJECTS_START -->` 与 `<!-- FEATURED_PROJECTS_END -->` 标记区
- **profile-3d-contrib/**: 永不手动修改（自动生成）
- **AI 记忆**: 每次对话先读 AGENTS.md 和 memory/tasks.md
- **日志记录**: 在 memory/ 下记录每日工作日志
- **技能包**: 全局安装于 `C:\Users\LoveDoLove\.agents\skills\`，所有项目共享，不自创

## 已安装技能包（全局）

| 技能包 | 来源 | 说明 |
|---|---|---|
| `karpathy-guidelines` | farmage/opencode-skills (MIT) | 减少 LLM 编码常见错误的行为准则 |
| `code-reviewer` | farmage/opencode-skills (MIT) | 代码审查（bug/安全/性能/可维护性） |
| `test-master` | farmage/opencode-skills (MIT) | 测试生成（单元/集成/E2E/性能/安全） |
| `code-documenter` | farmage/opencode-skills (MIT) | 技术文档（OpenAPI/JSDoc/用户指南） |
| `devops-engineer` | farmage/opencode-skills (MIT) | DevOps（Docker/CI-CD/K8s/Terraform） |
| `debugging-wizard` | farmage/opencode-skills (MIT) | 调试（栈追踪/日志分析/根因定位） |
| `fullstack-guardian` | farmage/opencode-skills (MIT) | 全栈安全开发（从前端到数据库的安全层） |
| `secure-code-guardian` | farmage/opencode-skills (MIT) | 安全加固（OWASP Top 10/JWT/Zod） |
| `spec-miner` | farmage/opencode-skills (MIT) | 逆向工程（从遗留代码提取规格） |

## Widget API 替换记录

| 用途 | 旧地址 | 新地址 | 状态 |
|---|---|---|---|
| GitHub Trophy | `github-profile-trophy.vercel.app` | `personal-trophy.vercel.app` | ✅ 200 |
| GitHub Stats | `github-readme-stats.vercel.app/api` | `github-stats-extended.vercel.app/api` | ✅ 200 |
| Top Langs | `github-readme-stats.vercel.app/top-langs` | `github-stats-extended.vercel.app/top-langs` | ✅ 200 |
| WakaTime | `github-readme-stats.vercel.app/wakatime` | `github-stats-extended.vercel.app/wakatime` | ✅ 200 |

## 已知注意事项

- workflows 中的 Python 脚本从外部仓库（`LoveDoLove/Github-Profile-Manager`、`Github-Forks-Sync-Manager`、`Github-Action-Cleaner`）运行时下载，不在本仓库维护
- README 不含 FEATURED_PROJECTS 标记，整个 Featured Projects section 由外部脚本整体替换
- index.html 已修复多余的 `</div>`（原 line 622 已移除）
- `portfolio.lovedolove.qzz.io` 返回 403，需在 Cloudflare Dashboard 调整安全等级