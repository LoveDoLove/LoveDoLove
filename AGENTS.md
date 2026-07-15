通用代理人工程架構與行為規範 (Universal Agentic Architecture & Identity Specification)

本文件是本倉庫 AI 代理人（Agent）的「身份定義與行為規範行為準則」，也是每次對話的至高入口。本文件將「神諭級全端代理人工程鐵律」與「本地技能包（Agent Skills）工作流」進行深度綁定，確保 AI 助手在解決任何工程問題時，皆能遵循高解耦、高安全、可觀測的最高標準。

1. 倉庫核心結構 (Repository Structure)

本倉庫採用「自適應認知與技能架構」，結構如下：

全局技能包
%USERPROFILE%
├── .agents/
│   └── skills/               # AI Agent 技能包庫（可發現、可安裝、可複用）

項目目錄
projects/
├── AGENTS.md                 # AI Agent 身份定義與行為規範（每次對話的入口）
├── MEMORY.md                 # AI 长期记忆：用戶偏好、專案背景、持久約定
├── memory/
│   ├── tasks.md              # AI 任務追蹤（待辦 / 進行中 / 完成）
│   └── YYYY-MM-DD.md         # 每日 AI 工作日誌
└── .github/
    └── workflows/            # AI 自動化工作流（每日摘要、Issue 處理、部署）


2. AI Agent 技能工作流 (Skill-Pack Engine)

技能包（Agent Skill）是本倉庫的核心機制——將可複用的 AI 能力封裝為標準單元，存放在 .agents/skills/<skill-name>/。主入口為 SKILL.md，AI 助手在接到任務時必須遵循以下工作流：

2.1 技能調用工作流 (Invocation Workflow)

任務檢索：接到任何代碼、架構或優化任務時，AI 必須優先檢索 本地 .agents/skills/ 目錄，查看是否有符合的技能包。

外部導入 (不自行編寫)：若本地無合適技能包，嚴禁 AI 自行憑空編寫技能包。必須優先搜尋 GitHub 開源社群（如 github.com/fields/... 等開源 Skills）或 Skills.sh 進行 Clone，並統一安裝存放至 .agents/skills/<skill-name>/。

加載與聲明：調用技能包時，AI 必須在對話中明確聲明：「偵測到相關任務，正在加載本地技能包 [skill-name]...」，並嚴格執行該技能包中的 SKILL.md 指引。

2.2 已內置技能包索引

karpathy-guidelines：減少 LLM 編碼常見錯誤的行為準則。在編寫、審查或重構代碼時使用這些準則，可以避免過度複雜化，進行精準修改，揭示潛在假設，並定義可驗證的成功標準。

3. 代理人架構三大不妥協鐵律 (The Three Uncompromisables)

不論任務規模多小，AI 助手在執行任何工具呼叫與後端變更時，必須 100% 遵守以下三大鐵律：

+---------------------------------------------------------------------------------+
|                                 三大不妥協鐵律                                   |
|                                                                                 |
|  1. 受控副官防禦 (Security)   ====>  JWT/ACL 系統級隔離，嚴禁信任 Prompt 意志    |
|  2. 宣告式工具解耦 (Decoupling) ====>  使用標準化介面 (MCP/JSON)，工具與 LLM 完全分離  |
|  3. 軌跡即真理 (Observability) ====>  採用 OpenTelemetry 標準，完整追蹤決策 Spans  |
+---------------------------------------------------------------------------------+


3.1 鐵律一：受控副官防禦 (Confused Deputy Defense)

核心原則：永遠不要相信 Prompt 能守住系統安全。

實踐：AI 助手本質上只是個「信差（Messenger）」。當代表用戶調用後端工具（API、資料庫、檔案系統）時，工具執行層必須依據使用者的安全憑證（JWT / ACL）進行硬性隔離校驗。縱使 AI 遭受 Prompt 注入（Prompt Injection）被洗腦，系統層也必須直接拒絕其越權存取。

3.2 鐵律二：宣告式工具解耦 (Declarative Tool Decoupling)

核心原則：禁止將工具呼叫邏輯與 LLM 驅動程式碼硬編碼（Hardcode）在一起。

實踐：工具必須是以宣告式（如 Model Context Protocol 協定或 JSON Schema）定義。模型僅負責輸出調用決策與參數。這確保了當底層模型（如從 Gemini 換到 Claude）迭代時，一條工具程式碼都不需要修改。

3.3 鐵律三：軌跡即真理 (Trajectory is the Truth)

核心原則：拋棄傳統 console.log，採用標準「軌跡追蹤（Trace）」。

實踐：必須完整記錄每一次推理的上下文。一個標準的 Trace Span 必須依循 OpenTelemetry GenAI Semantic Conventions 標準格式輸出：

{
  "trace_id": "8f3b1a2c5e7d9f0a1b2c3d4e5f6a7b8c",
  "span_id": "4a5b6c7d8e9f0a1b",
  "name": "agent_execution_loop",
  "attributes": {
    "gen_ai.system": "gemini",
    "gen_ai.request.model": "gemini-2.5-pro",
    "gen_ai.usage.input_tokens": 42105,
    "gen_ai.usage.output_tokens": 1024,
    "agent.name": "EnterpriseDevAgent",
    "agent.loop.iterations": 3
  }
}


4. 動態上下文預算與中斷機制 (Context & Preemption)

預算分配公式：


$$\text{Context Budget} = \text{Model Max Tokens} - \text{Target Output Tokens (Reserved)} - \text{Safety Buffer}$$

語境剪枝策略：

工作記憶 (Working Memory)：保留最新 $N$ 輪的原始對話，超出限制則背景調用 LLM 生成「摘要（Summary）」。

聲明式記憶 (Declarative Memory)：使用語義相似度過濾向量資料庫（Vector DB）內容，設定 $0.78$ 以上門檻避免無關雜訊。

超時與循環阻斷 (Preemption)：當 LLM 出現「邏輯死循環」或對同一個 API 連續發出 5 次錯誤請求時，執行階段（Runtime）必須在指定步數（如 Max 10 Steps）內主動阻斷，並執行 Fallback 降級處理與優雅報錯。

5. 生產就緒檢核清單 (Production Checklist)

在將任何代理人系統推向生產環境前，請確認已落實以下檢核點：

[ ] 受控副官防禦：如果用戶輸入注入指令要求越權操作，後端工具層是否能依靠 JWT/ACL 強制拒絕，而非僅僅依賴 Prompt 拒絕？

[ ] 模型無關性 (Model-agnostic)：工具與 LLM 驅動層是否完全解耦？若明天更換底層大模型，是否能做到一條工具程式碼都不改？

[ ] 超時熔斷：系統是否能在指定步數（如 Max 10 Steps）內主動阻斷死循環？

[ ] Context 溢出保護：當多輪對話長度接近臨界值時，系統是否能自動對歷史對話進行 Sliding Window 裁剪或自動摘要？

[ ] 標準化軌跡 (Trace)：當線上用戶報錯時，後端是否能一鍵調出該次決策的 OpenTelemetry 結構化 Trace 進行快速除錯？
