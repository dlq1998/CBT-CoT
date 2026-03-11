# CBT-CoT: 基于认知行为疗法的多智能体思维链问答框架

欢迎来到 **CBT-CoT (Cognitive Behavioral Therapy - Chain of Thought)** 项目仓库。

本项目探讨了如何将心理学中经典的**认知行为疗法（CBT）**与大语言模型（LLMs）的多智能体架构相结合。本仓库开源了研究中使用的核心干预材料，即基于 CBT 理论严密构建的 Agent 提示词（Prompts）与角色流转逻辑。

## 🌟 核心开源内容与声明

为遵循心理学研究的“开放材料（Open Materials）”规范，同时保护工程实现的隐私，本项目重点开源以下核心学术资产：
- **`CBT_Multi_Agent.py`**: 包含了本研究中定义的所有核心智能体（Agent），包括：
  - 提取自动思维 (Automatic Thought Extraction)
  - 评估自动思维 (Automatic Thought Evaluation)
  - 基于 CBT 规则的思维链推理 (CoT Inference)
  - 生成支持性回复 (Supportive Response Generation)
- **结构化干预逻辑**: 完整展示了如何利用大模型复现 CBT 中的“三栏表”到“五栏表”的认知重构过程。

*注：本项目不包含用于批量并发请求或具体 API 路由的工程执行脚本 (`main.py`)。研究人员完全可以基于公开的 Agent 定义，使用主流多智能体框架进行复现。*

## 🛠️ 环境依赖与安装

本框架的运行依赖于 OpenAI 团队开源的轻量级多智能体编排框架 **Swarm**。

- **Python 版本要求**: `Python 3.11.0` (推荐)

请按照以下步骤配置复现环境：

1. **安装 OpenAI 官方库** (建议指定版本以确保兼容性)：
   pip install openai==1.63.2
2. 安装 Swarm 框架：
pip install git+[https://github.com/openai/swarm.git](https://github.com/openai/swarm.git)
关于 Swarm 框架的更多详细信息，请参考其官方链接：https://github.com/openai/swarm
🚀 快速复现指南
如果您希望在本地跑通 CBT-CoT 流程，可以参考以下伪代码逻辑来构建您的执行脚本：

导入本仓库提供的 CBT_Multi_Agent.py 中的 Agent。

初始化 Swarm 客户端。

将用户的初始输入（如心理困扰描述）喂给 Automatic_Thought_Extraction_agent。

依靠 Swarm 内置的 handoff 机制，Agent 会根据提示词中的函数自动流转至下一个环节，直至生成最终的共情与支持性回复。

📝 引用声明
如果您在研究中使用了本仓库的提示词框架或理论设计，请引用我们的相关论文（论文发表后将在此更新具体的引用格式）。
