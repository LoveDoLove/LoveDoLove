# LoveDoLove

**Software Engineer | AI Coding Agents · Developer Tooling · Cloud Infrastructure**

I build engineering intelligence for coding agents, developer tooling that reduces friction, and cloud infrastructure that scales. My work centers on making AI-assisted development trustworthy, automating away toil, and running reliable systems on Cloudflare and modern cloud platforms.

[GitHub](https://github.com/LoveDoLove) • [Portfolio](https://portfolio.lovedolove.qzz.io) • [Email](mailto:v0130p5100cuboss@gmail.com) • [LinkedIn](https://www.linkedin.com/in/chong-jun-xiang)

---

## What I Build

| Direction | Focus |
|-----------|-------|
| **AI Coding Agents** | Persistent engineering memory, structural code intelligence, evidence-backed automation — making agents trustworthy over long horizons |
| **Developer Tooling** | MCP bridges, CLI plugins, build automation, cross-platform utilities — reducing the gap between intent and running code |
| **Cloud Infrastructure** | Cloudflare Workers, edge caching, load balancing, DNS automation, Workers-native deployments — serverless-first, globally distributed |
| **Systems & Automation** | CI/CD pipelines, infrastructure-as-code, Windows/Linux/FreeBSD build systems — reliable, repeatable, auditable |

---

## 🏗️ Flagship Projects

### [Veyra](https://github.com/LoveDoLove/Veyra) — *Primary flagship*

**Engineering intelligence for coding agents.** A DeepSeek Harness plugin implementing a Dual-Brain architecture: (1) **Veyra Memory** — persistent, evidence-backed engineering lessons with validation states (`unverified → reviewed → verified`) and authority levels (`candidate → derived → canonical`); (2) **Code Intelligence** — AST-level structural facts (symbols, call graphs, class hierarchies) derived live from the repository via `codebase-memory-mcp`. Hybrid search combines FTS5 BM25, semantic overlap, intent affinity, and relationship-graph cohesion. Code Intelligence flags potentially stale memories when evidence anchors point to modified code. Zero runtime npm dependencies (~130 kB packed).

**Tech:** TypeScript, Node.js, SQLite/FTS5, MCP, Cordis plugin architecture

---

### [dsh-codebase-memory-mcp](https://github.com/LoveDoLove/dsh-codebase-memory-mcp) — *Core infrastructure*

**Codebase Memory MCP bridge for DeepSeek Harness.** Registers six knowledge-graph code tools (`cbm_projects`, `cbm_search`, `cbm_snippet`, `cbm_arch`, `cbm_trace`, `cbm_search_code`) natively on the DSH tool surface. Auto-starts the `codebase-memory-mcp` daemon with its Web UI over stdio JSON-RPC 2.0, injects system-prompt guidance for when to prefer graph tools over grep, bundles a native agent skill (`codebase-memory`), and provides a `/cbm` slash command. Graceful degradation: only `tools` is a hard dependency; `systemPrompt`, `skills`, `commands` attach via deferred injection.

**Tech:** TypeScript, MCP, Cordis, stdio JSON-RPC, cross-platform executable detection

---

### [cloudflare-load-balancer](https://github.com/LoveDoLove/cloudflare-load-balancer)

**Production-ready HTTP load balancer as a Cloudflare Worker.** Weighted traffic distribution across multiple origins, failover to backup servers, maintenance-mode routing, and health-check integration — all at the edge with zero cold-start overhead.

**Tech:** JavaScript, Cloudflare Workers, Wrangler

---

### [personal-hq](https://github.com/LoveDoLove/personal-hq) *(private / in progress)*

**Personal identity site + dynamic registry on Cloudflare Workers.** Next.js 16 (App Router, Turbopack) + React 19 + TypeScript + Tailwind v4, deployed via `@opennextjs/cloudflare`. Supabase (PostgreSQL + Auth) for metadata registry. Phase-gated development with hermetic DB tests (PGlite), Playwright E2E, and Vitest. Canonical site URL defined once, shared across metadata, canonical links, and Wrangler vars.

**Tech:** Next.js, TypeScript, Tailwind v4, Supabase, Cloudflare Workers, OpenNext

---

### [cloudflare-smart-cache](https://github.com/LoveDoLove/cloudflare-smart-cache)

**All-in-one Cloudflare cache solution for WordPress.** Edge HTML caching with automatic purging, AJAX admin controls, API token support, and comprehensive logging. Modular PHP/TypeScript architecture for maintainable cache invalidation strategies.

**Tech:** PHP, TypeScript, JavaScript, Cloudflare API

---

### [cf-best-domain](https://github.com/LoveDoLove/cf-best-domain)

**Automated Cloudflare DNS A-record management and IP optimization.** Collects and tests Cloudflare IP ranges, selects lowest-latency IPs, and updates DNS records programmatically. Designed for scheduled runs via GitHub Actions or Workers Cron Triggers.

**Tech:** Python, Cloudflare API, GitHub Actions

---

### [alist-freebsd](https://github.com/LoveDoLove/alist-freebsd)

**Build wrapper and CI automation for compiling Alist on FreeBSD.** Custom `build.sh` and GitHub Actions workflows producing runnable FreeBSD binaries from upstream source. Demonstrates cross-platform build engineering and CI/CD for non-Linux targets.

**Tech:** Shell, GitHub Actions, FreeBSD toolchain

---

## Experience & Education

- **B.I.T. (Hons.) Software Systems Development** — TARUMT
- **AWS Academy Graduate** — Cloud Architect, Cloud Web Application Builder, Cloud Foundations (2024–2025)
- **AWS Educate** — Cloud Computing 101
- **Cisco Networking Academy** — Completed coursework (no official CCNA certification)
- **Sangfor Technologies** — Cloud & Network Engineer Intern: triaged L1/L2 global incidents for HCI/Cloud Platform/VDI (95%+ SLA), led storage split-brain recovery, Linux kernel diagnostics, automated Git-to-AWS CodeCommit migrations

---

## Automated Sections

The following section is updated daily by GitHub Actions (top 10 starred public repos, excluding forks):

## 🚀 Featured Projects

*Auto-generated — do not edit manually*

---

## Connect

<p align="center">
  <a href="https://github.com/LoveDoLove"><img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white" /></a>
  <a href="https://portfolio.lovedolove.qzz.io"><img src="https://img.shields.io/badge/Portfolio-007ACC?style=for-the-badge&logo=cloudflare&logoColor=white" /></a>
  <a href="mailto:v0130p5100cuboss@gmail.com"><img src="https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white" /></a>
  <a href="https://www.linkedin.com/in/chong-jun-xiang"><img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" /></a>
</p>

---

<details>
<summary><b>📊 Contribution Activity</b></summary>
<br>
<p align="center">
  <a href="https://github.com/LoveDoLove?tab=overview&from=2024-01-01&to=2024-12-31">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/LoveDoLove/LoveDoLove/main/profile-snake/github-snake-dark.svg" />
      <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/LoveDoLove/LoveDoLove/main/profile-snake/github-snake.svg" />
      <img alt="Contribution Snake" src="https://raw.githubusercontent.com/LoveDoLove/LoveDoLove/main/profile-snake/github-snake.svg" width="100%"/>
    </picture>
  </a>
  <br>
  <a href="https://github.com/LoveDoLove?tab=overview&from=2024-01-01&to=2024-12-31">
    <img src="https://raw.githubusercontent.com/LoveDoLove/LoveDoLove/main/profile-3d-contrib/profile-night-rainbow.svg" alt="3D GitHub Profile" width="100%"/>
  </a>
</p>
</details>

---

<p align="center">
  <a href="https://github.com/ryo-ma/github-profile-trophy">
    <img src="https://personal-trophy.vercel.app/api?username=LoveDoLove&theme=dark" alt="GitHub Trophy"/>
  </a>
  <br>
  <a href="https://github.com/anuraghazra/github-readme-stats">
    <img src="https://github-stats-extended.vercel.app/api?username=LoveDoLove&show_icons=true&theme=gruvbox" alt="GitHub Stats"/>
  </a>
  <a href="https://github.com/anuraghazra/github-readme-stats">
    <img src="https://github-stats-extended.vercel.app/api/top-langs/?username=LoveDoLove&layout=compact&theme=gruvbox" alt="Top Langs"/>
  </a>
  <br>
  <a href="https://github.com/anuraghazra/github-readme-stats">
    <img src="https://github-stats-extended.vercel.app/api/wakatime?username=LoveDoLove&theme=gruvbox" alt="Wakatime Stats"/>
  </a>
  <br>
  <a href="https://komarev.com/ghpvc/?username=LoveDoLove">
    <img src="https://komarev.com/ghpvc/?username=LoveDoLove&color=blue" alt="Profile Views"/>
  </a>
</p>

---

> **Engineering intelligence for coding agents. Developer tooling that reduces friction. Cloud infrastructure that scales.**