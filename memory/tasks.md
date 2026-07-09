# AI 任务追踪

## 当前方案：README + Portfolio 全量 UI/UX 重写

**计划（2026-07-09）：**
- README: Skills 精简（保留 skillicons.dev，去掉 5 类 badge 表格）、新增 Stats 仪表板（贡献热图/日历）、URL 统一为 `portfolio.lovedolove.qzz.io`
- portfolio-website/ 用 Astro 覆盖重写（现代动效风格：玻璃态卡片 + 微动效 + 深色渐变背景）
- 一次性同步所有待办：Certifications 新增、Connect 补 8 链接、Featured Projects 同步、URL 统一
- 保持 pnpm + wrangler 部署到 Cloudflare Workers

## 待办

- [x] 更新 memory/tasks.md 和 memory/2026-07-09.md 记录重写方案
- [ ] portfolio-website/ 用 Astro 覆盖初始化
- [ ] 写 Astro 组件 (Header/Stats/Skills/Certifications/Projects/Connect/Footer/3D)
- [ ] 写主页 index.astro 组合所有组件 + 完整 CSS 动效
- [ ] 同步待办：Certifications/Connect 补全/URL 统一/Featured Projects
- [ ] README.md Skills 精简 + URL 统一 + 新增 Stats 仪表板
- [ ] 迁移旧资源 (profile.png) 到 Astro public/ 并构建验证
- [ ] 部署到 Cloudflare Workers
- [ ] commit 所有变更

## 已完成

- [x] 创建 AGENTS.md、MEMORY.md、memory/ 目录结构
- [x] 修复 index.html HTML 结构错误（`</div>` → `</footer>`，移除多余 `</div>`）
- [x] 安装 9 个全局 skill 包（farmage/opencode-skills）
- [x] 替换 Widget API 地址（README + index 同步更新）
- [x] npm → pnpm 迁移（pnpm 11.9.0, wrangler 4.107.1）
- [x] 部署至 portfolio.lovedolove.qzz.io
- [x] 修复 sync-top-starred-projects.yml 429：脚本内嵌到 .github/scripts/