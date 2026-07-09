# AI 任务追踪

## 待办

- [ ] 同步 index.html Featured Projects 与 README 保持一致
- [ ] 统一 Portfolio URL（README: `portfolio.lovedolove.one` vs index.html: `lovedolove.github.io`）
- [ ] 在 index.html 添加 Certifications 证书区
- [ ] 同步 Connect 链接（README 有8个，index.html 只有4个）
- [ ] 在 Cloudflare Dashboard 调整安全等级以解除 `portfolio.lovedolove.qzz.io` 403

## 已完成

- [x] 创建 AGENTS.md、MEMORY.md、memory/ 目录结构
- [x] 修复 index.html HTML 结构错误（`</div>` → `</footer>`，移除多余 `</div>`）
- [x] 安装 9 个全局 skill 包（farmage/opencode-skills）
- [x] 替换 Widget API 地址（README + index.html 同步更新）
- [x] npm → pnpm 迁移（pnpm 11.9.0, wrangler 4.107.1）
- [x] 部署至 portfolio.lovedolove.qzz.io