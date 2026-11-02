# arXiv Systems Daily Digest 🚀

每日自动追踪并深度解读系统方向与 AI Infra 领域的最新 arXiv 论文。

读者定位为从事「容器架构与运行时、Kubernetes 编排、AI 基础设施（分布式训练/推理/GPU集群）」的工程师与研究者。

## 📌 最新日报
- **[2026-11-02 日报](docs/2026-11-02.md)**（入选 7 篇）：
  - **ARK**: 针对大模型 PD 分离架构中跨节点搬运庞大 KV Cache 引发的网络哈希冲突（ECMP 拥塞），提出零修改交换机的发送端协同路由方案，P95 传输完成时间降低 34%。
  - **LLM Fine-Tuning Workloads**: 基于 IBM 30,920 次实际微调任务的大规模实测，揭示了 Serverless 环境下微调任务高达 95% 的潜在配置失败率，为云原生平台设计 Serverless 训练运行时提供了关键指导。
  - **HiState**: 巧妙把 Agent 循环交互中的长尾历史 Checkpoint 卸载到 SSD，实现仅消耗常数级 GPU 显存恢复上下文，p99 首字延迟（TTFT）大幅降低超 5 倍。

## 📅 历史归档
| 日期 | 入选篇数 | 重点内容提要 | 报告链接 |
| :--- | :---: | :--- | :--- |
| **2026-11-02** | 7 篇 | • <b>ARK</b>: 针对大模型 PD 分离架构中跨节点搬运庞大 KV Cache 引发的网络哈希冲突（ECMP 拥塞），提出零修改交换机的发送端协同路由方案，P95 传输完成时间降低 34%。<br>• <b>LLM Fine-Tuning Workloads</b>: 基于 IBM 30,920 次实际微调任务的大规模实测，揭示了 Serverless 环境下微调任务高达 95% 的潜在配置失败率，为云原生平台设计 Serverless 训练运行时提供了关键指导。<br>• <b>HiState</b>: 巧妙把 Agent 循环交互中的长尾历史 Checkpoint 卸载到 SSD，实现仅消耗常数级 GPU 显存恢复上下文，p99 首字延迟（TTFT）大幅降低超 5 倍。 | [查看全文](docs/2026-11-02.md) |

---
*由 Google Antigravity 定时自动化流水线每日早晨自动分析并生成推送。*
