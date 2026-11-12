# Script to generate today's arXiv systems report
import os

report_content = """## arXiv 系统方向日报 · 2026-11-12

### 今日概览

今日系统方向（cs.DC / cs.OS / cs.PF 及相关交叉领域）共抓取 34 篇候选论文。经过资深系统调研体系的严格筛选与多维度评分，本次**入选深读：12 篇**（其中 5 篇评分为 5 分的核心突破论文，4 篇评分为 4.5 分的高价值系统论文，3 篇评分为 4 分的特色系统论文），其余 22 篇理论或边缘交叉论文归入文末列表。

今日文献呈现出极具震撼力的「智能体服务化与前缀缓存（Prefix Caching）稳定性治理、NVLink 机架级集合通信极简化、大模型训练/推理系统级协同」演进特征：
从微软 Azure CTO Mark Russinovich 等揭示的智能体动态模型路由下前缀缓存丢失痛点与 SHADOWPREFILL 预热机制，到揭示 vLLM/SGLang 在短时流量抖动下陷入长达数小时「亚稳态性能雪崩」的容量崩溃机理；从 NVIDIA 官方在 Blackwell NVLink 域内剔除元数据握手开销的单边 MoE All-to-All 通信，到 NVIDIA 与德克萨斯 A&M 大学联合提出的解耦权重放置与注意力归属的解码 Token 并行（TKNP）；从亚马逊 AWS 生产级大模型训练验证系统 Plumbline 捕获 7 大静默故障，到针对 DeepSeek-V4.1 庞大 Engram 查表的层级预取截止期分层存储 SlackTier；再到中科院信工所基于 seL4 权能微内核构建的高性能 Buddy 物理内存管理系统 CapBuddy，以及柏林工大将 Scale-to-Zero 延伸至物理节点的单板机能耗比例 Serverless 架构。无论是底层 OS 沙箱、集群编排与准入调度，还是 AI Infra 算子与集合通信，系统栈各层正在紧密联动以应对长上下文大模型与 Agent 时代的全新挑战。

今日必读：
1. **SHADOWPREFILL**: 微软 Azure 团队打造下一模型预热机制，通过挤压 SLO 闲置时间与 Shadow KV 换入换出，攻克智能体动态路由服务化下的 Prefix Cache 丢失难题。
2. **NVLinkOneSided**: NVIDIA 核心团队针对 Blackwell NVLink 域提出单边 MoE All-to-All，彻底去除元数据握手开销，解耦通信与 Grouped GEMM 算子。
3. **Decode Token Parallelism**: NVIDIA 与 TAMU 提出 TKNP 解码注意力并行架构并在 vLLM 上落地，解耦模型权重放置与注意力归属，长上下文高并发吞吐提升达 2.06 倍。
4. **Bursts That Outlast Themselves**: 微软揭示 Prefix-Cached 智能体服务化中因短时突发引发的亚稳态性能雪崩机理，提出基于会话挂起的硬预算容量治理方案。
5. **Placing LLM Lookup Tables**: 微软与独立研究员针对 DeepSeek-V4.1 的 203GB Engram 表研发 SlackTier，以层级截止期实现 NVMe 异步预取，节约 178GB 主机内存并提升吞吐 36%。
6. **Plumbline**: 亚马逊 AWS 官方大模型训练验证系统，揭示 Loss 正常但推理崩溃等 7 种静默故障模式，上线即发现 61 个底层框架隐蔽 Bug。
7. **ForeSpark**: Meta 与首尔大学联合研发并行投机解码联合预算调度器，在 vLLM 上以全局排序动态分配草稿与验证长度，吞吐提升最高 1.77 倍。
8. **ForeSight & UnitSight**: 港科大（广州）与清华大学突破英伟达 Profiler 硬件计数器隐藏限制，实现 2% 极低误差的 vLLM 端到端耗时预测并指导芯片性价比选型。
9. **Looping Deeper Without Growing KV**: UCSD 与清华提出因果编码器-解码器循环深度架构，在 4 卡 GB200 节点上支撑 552B DeepSeek-V4.1-Flash 零轮次 KV 增长，吞吐提升 3.6 倍。
10. **CapBuddy**: 中科院信工所针对 seL4 权能微内核构建高效物理内存 Buddy 管理器，剥离关键路径权能操作，内存分配性能提升 20 至 54.5 倍逼近 Linux。
11. **Energy-Proportional Serverless**: 柏林工业大学在单板机集群上将 Scale-to-Zero 延伸至物理节点电源状态，使突发无服务器负载平均能耗降低 39.6%~46.7%。
12. **Can KV Cache Be Reused Across Updates**: 硅基流动针对 DeepSeek-V4-Flash 跨版本迭代展开首个 KV Cache 复用实证研究，长文本首字时延（TTFT）加速最高达 5.08 倍。

---

### 逐篇解读

#### 1. SHADOWPREFILL: Keeping Your Next Model Warm for Per-Step Model Routing in Agentic LLM Serving
- 中文译名：SHADOWPREFILL：面向智能体大模型逐步路由服务化的下一模型预热机制
- 链接：https://arxiv.org/abs/2611.13176
- 作者：Haoran Qiu, Rohan Mahapatra, Rodrigo Fonseca, Mark Russinovich
- 单位：微软研究院 (Microsoft Azure Research) & 微软 Azure (Microsoft Azure) 【工业界】
- 分类：cs.DC
- 方向标签：C. AI Infra (LLM 推理服务、智能体服务化、Prefix Caching 优化、动态路由调度) & B. 编排与调度 (集群算力潮汐复用 / SLO Slack 收集)
- 相关度：5/5

1. 核心贡献：
首次系统性指出了智能体（AI Agent）多步执行中动态模型路由（Per-Step Model Routing，如 LLMRouter）与前缀缓存（Prefix Caching）之间的严重内在冲突：每次会话从大模型切换到小模型（或反之）时，由于各模型间的 KV Cache 互不兼容，导致既有前缀缓存瞬间清空失效，必须对平均 63K 的上下文重新执行高昂的 Prefill 预填充。为此，微软 Azure CTO Mark Russinovich 团队提出了 SHADOWPREFILL，在当前选定模型进行 Token 推理的同时，利用未选定模型实例在常规流量下留存的 SLO Slack（时延预算空闲时间）与空闲计算容量，在后台并行执行「影子预填充（Shadow Prefill）」，使得下一次模型切换发生时能够命中预热好的前缀缓存。

2. 原理解析：
这就像在 Kubernetes 集群中部署了一组主从微服务或 Pod：业务流量当前正在访问 A 服务的容器（比如 GPT-4o 级别的重型推理实例），但调度路由系统预测下一步可能要调用 B 服务（比如轻量代码验证实例）。如果等路由决策下来才去启动 B 容器拉取镜像，业务端就会遭遇漫长的冷启动阻塞：
- **SLO Slack 潮汐收割**：未选定模型的线上实例并非 100% 满载，每个推理迭代（Iteration）中都有因服务等级目标（SLO）裕量而剩余的微秒级空隙。SHADOWPREFILL 像一个精细的 QoS 旁路调度器，把影子预填充伪装成超低优先级的「Best-Effort」工作载荷，见缝插针地在后台对未选定模型预计算上下文 KV Cache；
- **Shadow KV 内存换出（Spill-to-Host）**：为防止后台影子 KV 挤占前台核心推理请求宝贵的 GPU 显存，系统将生成的影子 KV Cache 主动卸载溢出到宿主机 CPU 内存中；
- **保护性优雅降级**：一旦前台高优先级线上业务流量涌入，系统立即优先驱逐影子 KV Cache；若发生模型切换时影子预热尚未彻底完成，系统平滑回退（Fallback）至冷切换路径，绝不阻塞任何正常请求的端到端时延。

3. 关键结论：
在基于真实生产级代码智能体（平均上下文长达 63K tokens）及 5 套主流智能体基准测试（覆盖 24 组模型配对）评测中，基线系统在模型切换后的前缀命中率从同模型的 80%~89% 骤降至 44%~65%，切换请求耗时增加 1.5~3.2 倍；而 SHADOWPREFILL 成功将模型切换调用的端到端时延削减了 8.5%~21.4%，整体 LLM 调用时延降低 3.7%~17.7%，路由 Token 成本节省 22.5%~46.1%，且常规流量完全维持了严格的 SLO 达标率，单请求附加能耗仅上升 0.4%。

4. 背景地位：
这是大模型推理从单次 Prompt 问答迈向长时间、多步骤自主智能体（Coding Agent、Tool-use Agent）时代的关键基础设施突破。由微软 Azure 架构权威 Mark Russinovich 领衔，将传统操作系统中的预取与多租户优先级调度思想，极其巧妙地融合到大模型前缀缓存管理中。

5. 落地相关性：
对于在公有云或私有 K8s 集群中维护大模型网关、Agent 路由分发器及多模型混部推理池的架构团队而言，具有直接的指导意义。它指明了多模型级联（Model Cascading）走向生产化时必经的前缀缓存预热演进方向，可直接指导在 vLLM/SGLang 上层或 Sidecar 路由代理中实现影子预填充策略。

---

#### 2. One-Sided Expert-Parallel All-to-All for Mixture-of-Experts Inference over NVLink
- 中文译名：NVLink 域内面向混合专家模型推理的单边专家并行 All-to-All 集合通信
- 链接：https://arxiv.org/abs/2611.13188
- 作者：Bo Li, Chulian Zhang, Or Biri, Anthony Chang, Anton Korzh, 等（共 13 位作者，通讯作者：Bo Li, Chulian Zhang）
- 单位：NVIDIA (英伟达系统与网络团队) 【工业界】
- 分类：cs.DC, cs.CL, cs.LG, cs.PF
- 方向标签：C. AI Infra (MoE 专家并行 / All-to-All 集合通信 / NVLink / Blackwell 微架构协同) & D. 性能与可靠性 (小批次延迟与硬件利用率)
- 相关度：5/5

1. 核心贡献：
由 NVIDIA 核心网络与底层加速库团队联合推出面向 Blackwell 架构 NVLink 域内 MoE 推理的全新专家并行通信算子 NVLinkOneSided。研究团队针对推理场景中每卡处理 Token 数量较少、小批次下固定开销而非网络带宽决定总体延迟的本质特征，颠覆了传统 DeepEP 等双边握手集合通信设计，构建了单边（One-Sided）跨 GPU 显存直写范式：源端 GPU 无需事先与目的端交换任何路由元数据，直接将 Token 推送到目标 GPU 的 Rank 优先缓冲区中，并使后续的 Grouped GEMM 算子能够原地就地（In-Place）读取，消除了昂贵的数据重排开销。

2. 原理解析：
传统 MoE 专家并行 All-to-All（Dispatch 和 Combine）就像不同分拣车间之间的跨部门协作：
- **传统双边痛点**：在 DeepEP 或传统 NCCL 实现中，每个 GPU 必须先跟其它 7 张甚至更多卡「打电话对账」（交换 Metadata 告知各自要发多少个 Token），接收方开辟对应专家的临时内存，再分批接收并在显存中做一次重新打包转置（Permute），最后才喂给 Grouped GEMM。在 Decoding 阶段每个 GPU 只有几个到几十个 Token，打招呼与数据搬运的固定开销比真正的矩阵计算还要慢几倍；
- **NVLink 对称内存直写**：在单 NVLink 域（如 8 卡或 GB200 机架）内，GPU 拥有统一的 Symmetric Memory（对称内存）寻址能力。源端 GPU 根据自身 Router 决策，直接通过 NVLink 单边 Store 指令把 Token 砸进对端预先分配好的 Rank-Major 缓冲区，完全省略前置握手；
- **Fence 与 Sentinel 双同步协议**：系统设计了两种极简同步机制——高吞吐场景采用 Fence 屏障，极低延迟解码场景采用基于原子标志位的 Sentinel（哨兵）流转；
- **原地计算解耦**：Grouped GEMM 被深度改造，直接跨步读取 Rank-Major 缓冲区中的离散 Token，免除了中间的 per-expert 内存拷贝，实现了通信数据面与下游计算后端的零拷贝直通。

3. 关键结论：
在英伟达最新 Blackwell GPU 硬件平台上的微基准测试与端到端评测中，NVLinkOneSided 在 Dispatch 和 Combine 阶段比业界公认最强的 DeepEP 提速 1.2~3.0 倍，且在 Batch Size 极小时优势最为巨大。与 DeepGEMM 组合后，整个 MoE 层吞吐相比 DeepEP + DeepGEMM 提升达 2.4 倍；甚至在单卡 Token 数达 128 以内时，超越了手工融合成一体的 DeepGEMM MegaMoE 算子，同时保持了完全模块化、与各种激活值量化格式（FP8/FP4）彻底解耦的优雅接口设计。

4. 背景地位：
来自英伟达官方通信与算子底层团队（包括 FasterTransformer 与 Megatron-LM 核心元老 Julien Demouth、Artem Polyakov 等），代表了当前 Blackwell 机架级硬件拓扑下 MoE 专家并行通信的最前沿水准，彻底重塑了下一代机架级推理集群的通信范式。

5. 落地相关性：
直接影响主流开源推理引擎（vLLM、SGLang、TensorRT-LLM）在 8 卡 H100/H200 以及全新 Blackwell NVL72 平台上的核心架构设计。对于正在部署 DeepSeek-V3、Mixtral 等超大规模 MoE 模型的基础设施工程师而言，NVLinkOneSided 提供了从根本上消灭 Decoding 阶段通信气泡的终极武器。

---

#### 3. Decode Token Parallelism: Memory-Efficient Distributed Attention Parallelism for Scalable LLM Decoding
- 中文译名：解码 Token 并行：面向可扩展大语言模型解码的显存高效型分布式注意力并行架构
- 链接：https://arxiv.org/abs/2611.13293
- 作者：Susav Shrestha, Brad Settlemyer, Narasimha Reddy
- 单位：NVIDIA (Santa Clara) 【工业界】、德克萨斯 A&M 大学 (Texas A&M University)
- 分类：cs.DC, cs.CL, cs.LG
- 方向标签：C. AI Infra (LLM 解码服务、vLLM 系统实现、注意力并行 / TKNP、长上下文与 KV Cache 分布式调度)
- 相关度：5/5

1. 核心贡献：
由 NVIDIA 与德克萨斯 A&M 大学联合提出了一种专为超长上下文、高并发大模型解码服务池设计的全新分布式注意力并行架构——解码 Token 并行（Decode Token Parallelism, TKNP）。针对现存并行策略（张量并行 TP 无法横向扩展注意力头数、数据并行 DP 重复复制权重挤占 KV Cache 显存、解码上下文并行 DCP 带来昂贵的跨节点部分注意力汇聚归约）的固有限制，TKNP 首次将模型权重的放置拓扑与请求注意力的归属权彻底解耦，在不跨节点复制模型权重的前提下，让每个节点仅承载自身请求的本地注意力计算，大幅提升了显存容量利用率与服务吞吐。

2. 原理解析：
这就像在大型 Kubernetes 生产集群中管理无状态计算与有状态缓存的排布哲学：
- **注意力与全连接层的解耦本质**：在 Decoding 阶段，全连接 Dense 层（QKV 投影与 MLP）可以通过 Batch 摊薄权重读取，适合在高速 NVLink 域内做紧密的张量并行；而 Attention 的显存开销完全被各请求持有的 KV Cache 垄断，其算力随请求并发线性增长；
- **流水线层块分布与请求本地化**：TKNP 将整套模型仅保留一份单一拷贝，按均衡的 Layer Block（层块）切分放置在集群各节点上。持有某一特定层块的节点在本地使用节点内 TP 为整批请求统一运行投影和 MLP 计算；
- **跨节点仅传输当前激活值**：当需要执行 Attention 计算时，该节点无需跨节点拉取庞大的 KV Cache，而是由每个节点在本地针对自己负责的并发请求专属 KV Cache 运行完整的 Attention 计算。整个跨节点网络（RoCE/IB）只流动当前步极轻量的单 Token 激活值（Activation），所有 Dense All-Reduce 严格限制在节点内 NVLink 完成，彻底告别了跨节点的注意力部分结果拼接与重排。

3. 关键结论：
该系统已在主流开源推理框架 vLLM 中完成全栈落地开发，并在多达 64 张 NVIDIA H100 GPU 上针对 Llama 3.1 405B 以及 Nemotron-4 340B 两大超大参数模型进行了严格验证。在长上下文高并发工况下，TKNP 相比当前业界标准的解码上下文并行（DCP）将端到端完成吞吐量提升了 1.7 倍，相比相同卡数下的数据并行（DP）吞吐量提升高达 2.06 倍。

4. 背景地位：
直击当前长文本推理服务化中「KV Cache 显存爆炸」与「分布式通信开销剧增」的核心矛盾。该工作打破了 Megatron 与 DeepSpeed 等传统并行策略在大模型解码池中的生搬硬套，为 vLLM 社区及工业界长文本 Serving 开拓了全新流派。

5. 落地相关性：
对于在 Kubernetes 上运维 70B/405B 级别长文本模型推理集群（如 RAG 检索、代码智能体仓库分析）的算力平台架构师而言，TKNP 能够直接在既有 GPU 节点上将并发容量翻倍，显著减少对高昂跨节点高带宽网络的依赖。

---

#### 4. Bursts That Outlast Themselves: Persistent Degradation in Prefix-Cached Agent Serving
- 中文译名：遗患无穷的突发流量：前缀缓存智能体服务化中的亚稳态持续性能衰退
- 链接：https://arxiv.org/abs/2611.13412
- 作者：Wen Huang, Jack Liu
- 单位：微软 (Microsoft) 【工业界】、独立研究员 (Independent Researcher)
- 分类：cs.DC, cs.AI, cs.LG
- 方向标签：C. AI Infra (LLM 推理服务、Prefix Caching 亚稳态失效、vLLM / SGLang 稳定性) & D. 性能与可靠性 (过载雪崩防护与准入控制)
- 相关度：5/5

1. 核心贡献：
首次在生产级 LLM 推理引擎（vLLM、SGLang）中证实并数学建模了一类隐蔽且极具破坏性的「亚稳态失效（Metastable Failure）」现象：当使用前缀缓存（Prefix Caching）服务多轮智能体（Agent）会话时，仅仅数分钟的短暂流量突增（Burst），就会将推理引擎推入持续数十甚至上百分钟的恶性性能衰退泥潭——缓存命中率从 85% 暴跌至 ~10%，服务吞吐减半，请求队列积压无法自愈。作者深入剖析了该恶性循环的正反馈机理，证明了传统基于新请求限流（Throttling Admissions）对灾难恢复基本无效，并提出了一种基于容量硬预算的主动会话挂起（Suspending Admitted Sessions）与准入恢复机制。

2. 原理解析：
这与微服务和 Kubernetes 集群中著名的「级联雪崩（Cascading Failure）」如出一辙，其内核机制堪称经典的控制面反噬：
- **正反馈雪崩闭环**：智能体任务是多轮闭环交互，每轮 Prompt 包含历史所有上下文（10K~40K tokens）。命中前缀缓存时只需微秒级追加 Prefill 1K token；一旦突发流量挤占了 GPU 显存中的 KV Cache 块，导致缓存块被驱逐发生 Miss，计算量瞬间暴增 10~40 倍！计算变慢导致会话在系统内的驻留时间（Holding Time）延长，更多未完成会话继续霸占显存，导致后续所有轮次全部发生 Miss，整个系统永久滞留在「重计算 -> 耗时变长 -> 显存拥塞 -> 持续重计算」的崩溃态；
- **限流失效与挂起破局**：仅仅拦截外部新进来的 Pod/请求根本无法打破死结，因为已经进入系统的存量会话本身就能把算力耗尽（实测新请求限流在 7 次测试中仅侥幸恢复 1 次）。真正有效的解药是类似 Linux OOM-Killer 或 K8s 抢占的激进治理：严格将活跃会话的总 KV 需求硬限制在当前内存池水线内，主动「冻结挂起」超额的已接纳会话，优先让一部分会话高速完成退出并释放显存，随后在数分钟内即可彻底恢复系统的健康缓存态。

3. 关键结论：
在 Qwen3-32B 运行 SWE-bench 真实智能体流量轨迹的压测中，仅 3 分钟的短暂过载让 vLLM 实例在接下来的 70 分钟内持续处于崩溃状态（缓存命中率长期低于 10%，排队积压持续攀升），而完全相同基线负载的对比组平稳运行。在 SGLang 上的实验亦复现了该现象。作者提出的无需调参的无感知容量预算控制器，在所有测试场景下 100% 成功阻止了系统坠入亚稳态，且挂起恢复策略在数分钟内让崩溃实例实现 100% 满血复活。

4. 背景地位：
大模型推理领域首篇将经典分布式系统可靠性理论（亚稳态故障）严谨映射到 LLM 显存状态与前缀缓存机制的里程碑式论文，揭露了当前主流推理引擎在并发控制和容量规划上的严重盲区。

5. 落地相关性：
每一位在生产环境中部署 K8s 大模型网关与推理集群的 SRE 和平台架构师的「必读避坑宝典」。直接指出：当前 K8s 针对大模型服务的 HPA 弹性伸缩和常规 Ingress 限流在智能体场景下完全失效，必须在推理框架层引入会话级 KV 显存预算感知的自适应挂起/恢复策略。

---

#### 5. Placing LLM Lookup Tables by Per-Layer Prefetch Deadlines
- 中文译名：基于层级预取截止期放置大模型查表：DeepSeek-V4.1 Engram 存储分层与调度优化
- 链接：https://arxiv.org/abs/2611.13413
- 作者：Wen Huang, Jack Liu
- 单位：微软 (Microsoft) 【工业界】、独立研究员 (Independent Researcher)
- 分类：cs.DC, cs.AI, cs.LG
- 方向标签：C. AI Infra (DeepSeek-V4.1 Engram 模块、SGLang 框架系统扩展、NVMe/RDMA 预取流水线与 CUDA Graph、显存/主机内存协同)
- 相关度：5/5

1. 核心贡献：
针对 DeepSeek-V4.1 新引入的 Engram n-gram 条件查表机制（双层查表体积高达 203 GB，在 4 卡 H200 节点上占据高达 190 GiB 的主机 DRAM 内存，严重挤占甚至导致单机无法承载 KV Cache）的硬件瓶颈，首次提出了基于「层级预取截止期（Per-Layer Prefetch Deadlines）」的异构存储分层放置系统 SlackTier。在推理框架 SGLang 内部重构了异步预取流水线，将查表操作无缝嵌入解码阶段的 CUDA Graph 中，成功将深层大表直接下沉至廉价 NVMe SSD 或跨节点 RDMA 内存中，以几乎零性能损失换取了上百 GB 主机内存的解放。

2. 原理解析：
这与操作系统虚拟内存分页及 Kubernetes 存储分级调度的原理高度契合：
- **行索引提前知晓与时间窗口不对称性**：Engram 查表的行索引仅由输入的 Prompt 或当前解码的 Token 决定，在每个解码 Step 刚开始时就能完全算出。DeepSeek-V4.1 的两层 Engram 分别位于第 1 层和第 14 层：第 1 层只有 0.3 ms 的准备时间（窗口极紧），而第 14 层由于前面 13 层的串行计算掩护，拥有足足 9.3 ms 的超长前置时间（截止期裕量相差 30 倍！）；
- **存储阶梯精确适配**：9.3 ms 的时间窗口足以从 4 块并行 NVMe 固态硬盘中以异步方式直接拉取非缓存数据（耗时仅 2~4 ms）。因此，SlackTier 决定将第 14 层的巨型查表彻底扔到底层 NVMe 磁盘，完全不占主机内存；对时间敏感的第 1 层，则在 GPU 片上显存分配一个极小的动态热点行缓存；
- **CUDA Graph 零开销重叠与 RDMA 汇聚**：查表下发被无缝包裹在 CUDA Graph 重放中，保证严格的 bit-exact 精度；当利用跨节点 RDMA 访问远端统一查表节点时，单份 203 GB 权重表可同时服务 2 个以上计算实例。

3. 关键结论：
在真实的 SGLang 环境中重放对话与智能体轨迹，当两层查表全部下放至 4 块 NVMe 磁盘时，每个输出 Token 的生成耗时（TPOT）相比原生全部驻留 DRAM 的 SGLang 仅微增 1.4%，而宿主机内存占用从 212 GiB 骤降至 34 GiB（节省 84% 内存！）。在显存受限的长文本智能体任务中，将省出的 178 GiB 内存充当 Host 端 KV Cache 缓存池后，集群中位数服务吞吐提升了 36%，首字生成耗时 P90 延迟从 38 秒断崖式降低至 24 秒。

4. 背景地位：
大模型架构进入「超大参数与稀疏外置显存/查表」融合时代的标志性系统工作。精准抓住了 DeepSeek-V4.1 及类似架构（Engram、PKM 等）的算子时序特征，展现了深度软硬件协同对降低算力持有成本的巨大威力。

5. 落地相关性：
对于广大使用私有算力池部署 DeepSeek 系列前沿开源模型的工程团队，本论文提供了立刻可复现的降本方案。不再需要为每台 4 卡 GPU 机器采购顶配昂贵的 1TB+ 主机内存，利用机器自带的 NVMe SSD 或高速 RDMA 网络即可实现超大规模模型的高并发低延迟部署。

---

#### 6. Plumbline: When the Loss Lies, Validating LLM Training Correctly
- 中文译名：Plumbline：当 Loss 在说谎时，如何正确验证大模型分布式训练
- 链接：https://arxiv.org/abs/2611.13393
- 作者：Ruochen Wen, Hongyang Wang, Siwei Li, Wenbo Chen, Xian Li, 等（共 11 位作者，通讯作者：Ruochen Wen）
- 单位：亚马逊 (Amazon AWS AI 团队) 【工业界】
- 分类：cs.DC, cs.LG
- 方向标签：C. AI Infra (大模型分布式训练系统、正确性验证、静默故障根因诊断、训练容错) & D. 性能与可靠性
- 相关度：4.5/5

1. 核心贡献：
来自亚马逊 AWS 生产级大模型训练基础设施团队的重磅成果。论文揭露了一个令所有大模型训练工程师深恶痛绝的残酷事实：在大规模分布式训练集群中，「Loss 曲线平稳下降并不代表训练正确（When the Loss Lies）」。由于算子精度截断、集合通信隐藏溢出、并行切分掩码错误等底层 Bug，训练过程极易发生无报错、无 Crash 的「静默故障（Silent Failures）」，往往耗资数百万美元训练数周后才在最终下游评测中暴露。AWS 团队研发并上线了训练全生命周期正确性校验系统 Plumbline，归纳了 7 大静默故障范式，并在跨 3 个框架与 5 大模型的真实接入中排查出 61 处底层隐蔽缺陷。

2. 原理解析：
这就像在复杂的云原生微服务调用链路中引入了端到端金丝雀对账与分布式追踪探针：
- **全生命周期逐层探针校验**：Plumbline 从数据加载端（Data Loader 确定性洗牌与分片对齐）、模型层级抽象（单算子、自定义层的前反向数学等价性）、并行切分（TP/PP/DP 张量切分重组守恒校验），一直延伸至全量运行时（Gradient Checkpointing 状态隔离）；
- **Day-0 新模型接入哨兵**：当开源社区发布全新模型架构（如 MoE 新路由、新型 RoPE 变体）时，在业务团队大规模投产前，自动执行全套形式化正确性回归测试，在毫秒级内定位张量维度或广播语义的微小偏差；
- **智能体根因诊断链**：利用轻量化断言与梯度比对，复用前置测试用例，从海量 Worker 节点的分布式日志与通信追踪中自动倒推，精准定位是哪一行 CUDA 算子或通信掩码破坏了数值稳定性。

3. 关键结论：
Plumbline 已在 Amazon AWS 生产集群全面部署。在针对 PyTorch、Megatron 及 AWS 内部自研框架的验证中，系统成功捕获了 61 个严重 Bug，其中高达 32 个为完全不产生报错的隐蔽静默故障！团队据此向上游开源社区提交并修复了 42 个缺陷（8 个为首次由 AWS 团队揭露）。论文系统总结了分布式训练中的 7 种典型失效模式，为整个 AI Infra 工业界提供了标准故障字典。

4. 背景地位：
大模型分布式训练领域由公有云巨头团队（AWS AI）公开的最具工程实操价值的系统可靠性论文之一。改变了以往依靠炼丹工程师「肉眼看 Loss 图」的蛮荒排障时代，将软件工程的形式化验证全面引入千卡/万卡 AI 基础设施。

5. 落地相关性：
极度契合负责维护 Kubernetes（如 Volcano、Kueue、Ray Operator）上大规模分布式训练任务的基础设施与算法平台工程师。论文提出的 7 大模式可直接作为大模型训练平台的健康检查探针与准入测试用例，避免巨额算力浪费。

---

#### 7. ForeSpark: Joint Draft and Verification Budget Scheduling for Parallel Speculative Decoding
- 中文译名：ForeSpark：面向并行投机解码的生成与验证预算联合调度系统
- 链接：https://arxiv.org/abs/2611.13442
- 作者：Jaeyong Song, Daniel Wang, Pratyush Patel, Jonny Kong, Preyas Shah, Shobhit Kanaujia
- 单位：Meta (工作于 Meta 实习期间完成) 【工业界】、首尔国立大学 (Seoul National University)
- 分类：cs.DC, cs.AI, cs.LG
- 方向标签：C. AI Infra (vLLM 推理服务化、并行投机解码、批处理动态预算调度、SLO 保障)
- 相关度：4.5/5

1. 核心贡献：
针对并行投机解码（Parallel Speculative Decoding，即草稿模型一次前向传播同时吐出整块候选 Token）在高负载 Serving 场景下严重的算力浪费问题，提出了首个草稿长度与验证预算联合分配调度系统 ForeSpark。作者发现现有系统仅自适应调节目标模型的验证长度，导致每个请求无条件生成全量候选块，在繁重负载下草稿生成竟侵占了高达 40% 的单步耗时且大部分未经验证即被丢弃。为此，ForeSpark 确立了「保功投机（Work-Conserving Speculation, WCS）」原则，在 vLLM 调度器中以纳秒级全局排序联合决策每个请求的生成与验证预算。

2. 原理解析：
这就像 Kubernetes 调度器在节点计算资源极度吃紧时，精细化动态裁决 Pod 的 CPU Request 与 Limit：
- **传统并行投机盲区**：过去系统好比每个工人无论活多活少，每次都固执地生产 8 个预制件，但质检员（目标大模型）在当前批次只能抽检 2 个，剩余 6 个当场报废，白白占用了生产线工时；
- **上下文感知预估器**：ForeSpark 在请求进入草稿阶段前，基于目标模型上一轮的注意力熵和上下文特征，以极低开销预测当前请求各个候选长度被接受的概率分布；
- **轻量联合调度器（Global Sort）**：由于整个 Batch 内所有请求共享 GPU 显存带宽与算力，ForeSpark 在 vLLM 每步迭代前，将所有并发请求的期望收益与算力开销进行全局快速排序，一步求解出全局收益最大化的各个请求专属的（草稿长度 $K$, 验证长度 $V$）组合；
- **保功预算再分配**：将节省下来的 GPU 算力集中倾斜给命中概率极高的高价值请求，消除无谓浪费。

3. 关键结论：
在基于主流推理框架 vLLM 的工程实现与针对 Qwen3-14B、GLM5.3 等多元模型的全栈压测中，ForeSpark 在维持生成文本分布完全无损的前提下，相比当前最顶尖的自适应系统 DSpark 吞吐提升高达 1.77 倍，相比传统自回归解码提升 2.49 倍；在严格的时延 SLO 约束下，系统能够支撑的请求吞吐速率相比 DSpark 提升了 1.51 倍。

4. 背景地位：
来自 Meta 基础设施团队与学术界的紧密合作成果，首次将投机解码技术从单纯的「模型算法级小修小补」升维至「推理引擎批处理调度与 QoS 资源分配」的系统工程层面。

5. 落地相关性：
vLLM / SGLang 推理集群落地的核心利器。对于正在线上部署 Medusa、EAGLE 等投机采样方案以压降时延的推理平台团队，ForeSpark 提供了一套可即插即用的调度器优化补丁，大幅提升高并发场景下的资源有效利用率（Goodput）。

---

#### 8. Exploiting What NVIDIA Profilers Hide: Fast and Accurate Analytical GPU Performance Modeling
- 中文译名：挖掘英伟达 Profiler 隐藏的微架构信息：快速且精准的 GPU 解析性能建模
- 链接：https://arxiv.org/abs/2611.13762
- 作者：Ziwen Wang, Qi Luo, Kunlin Li, Changxi Liu, Dongsheng Wang, Yun Chen
- 单位：香港科技大学（广州） (HKUST-GZ) 【知名实验室】、清华大学 (Tsinghua University) 【知名实验室】
- 分类：cs.AR, cs.PF
- 方向标签：C. AI Infra (GPU 硬件微架构分析、vLLM 推理端到端耗时预测、芯片选型与性价比优化) & D. 性能建模
- 相关度：4.5/5

1. 核心贡献：
港科大（广州）与清华大学团队联合揭露了英伟达官方性能分析工具（如 NCU / Nsight Compute）的一项关键缺陷：官方 Profiler 会在硬件单元层面进行全局聚合汇总，掩盖了底层各物理单元的离散真实计数，导致传统解析性能模型在预测跨 GPU 硬件配置时的预测误差居高不下。研究团队开发了突破聚合限制的微架构探针 UnitSight 与排队解析性能模型 ForeSight，不仅以极高速度实现了单个 Kernel 的毫秒级推演，更能以 2.0% 的极低误差精确预测 vLLM 上大模型推理的端到端运行耗时，并成功指导了面向 H20 等定制芯片的高性价比硬件配置探索。

2. 原理解析：
这就像在排查复杂集群网络抖动时，传统的监控指标只给出一个粗糙的平均 CPU 利用率，掩盖了特定网卡队列的单核打满与瞬时丢包：
- **固定时延与排队时延的精细剥离**：传统模型粗暴地将 Warp 停顿（Stall）在所有硬件单元上同等缩放。作者敏锐指出，指令发射固有的执行时延在不同微架构下是固定的，真正随硬件规模动态剧烈波动的是硬件执行单元前排队造成的排队停顿（Queueing Stalls）；
- **UnitSight 逆向微架构剖析**：官方 NCU 屏蔽了各物理单元底层细节，UnitSight 通过精心构造的汇编级 SASS 指令探针，绕开聚合层，完整还原出各个硬件计算与访存单元内部的微架构物理状态与真实压力；
- **ForeSight 极速排队求解**：利用排队论解析方程复用真实测量的固定时延，仅重新求解随单元压力变化的排队停顿，速度比 Accel-Sim 等周期级硬件模拟器快 49 倍，完全摆脱了昂贵的逐周期仿真。

3. 关键结论：
在跨越 9 款主流英伟达 GPU 的全面评测中，ForeSight 预测 GPU Kernel 执行时间的平均绝对百分比误差（MAPE）仅为 8.3%（比最佳基线模型的 14.1% 误差大幅降低）；在 vLLM 运行的真实大模型端到端服务评测中，端到端时延预测误差仅为 2.0%！借助 ForeSight 的超高速设计空间探索能力，团队针对 NVIDIA H20 芯片推演出了新的架构衍生配置，实现了高达 1.78 倍的性能/成本比提升。

4. 背景地位：
系统性能评价（cs.PF）与硬件微架构（cs.AR）领域的突破性工作。打通了从底层 GPU 物理晶体管与汇编指令执行，到上层 vLLM 复杂推理引擎宏观性能表现之间的定量因果链条。

5. 落地相关性：
对从事 AI 算力中心容量规划、国产芯片适配选型、以及大模型推理算子深度调优的系统架构师极具实战价值。无需采购成百上千张昂贵芯片做全量压测，借助该解析模型即可精准评估不同显存带宽与算力配比在大模型业务下的实际表现。

---

#### 9. Looping Deeper Without Growing the KV Cache: Recurrent Depth for Causal Encoder-Decoders
- 中文译名：深层循环而不增加 KV Cache：面向因果编码器-解码器的循环深度架构与极限推理优化
- 链接：https://arxiv.org/abs/2611.13378
- 作者：Jiaqi Leng, Minshen Zhang, Zhaofeng Sun, Yu-Yang Qian, Peng Zhao, Hao Zhang
- 单位：加州大学圣迭戈分校 (UC San Diego / UCSD) 【知名实验室】、清华大学、南京大学
- 分类：cs.LG
- 方向标签：C. AI Infra (KV Cache 极致压缩、DeepSeek-V4.1-Flash 552B 推理部署、GB200 节点高并发吞吐优化)
- 相关度：4.5/5

1. 核心贡献：
加州大学圣迭戈分校（UCSD）张豪教授团队与清华、南大联合攻克了循环深度大模型（Looped Language Models）推理服务化中的核心瓶颈：传统循环模型虽然通过权重参数复用加深了表征能力，但每增加一轮循环都要成倍累加全局 KV Cache，导致推理批处理大小受到极度压缩。团队设计了一种全新的非对称循环因果编码器-解码器（Looped CED）架构，通过将循环深度收敛在稀疏编码器内部，并引入随机循环深度不动点训练，实现了「跨轮次零 KV Cache 增长（Zero Round-wise KV Growth）」！在 4 卡 GB200 节点上成功完成 552B 级超大参数 DeepSeek-V4.1-Flash 的 8 轮循环部署，并发能力实现质的飞跃。

2. 原理解析：
这就像在云原生无状态工作流中，不再为每次重试循环克隆全量上下文日志，而是提炼出一份紧凑的不可变共享摘要：
- **循环位置重构**：传统方案盲目在解码器端反复读取投影，导致每轮解码都要复制一份全量上下文 KV。作者通过严格理论与实验证明，循环表征迭代必须且只需放置在非对称堆栈的编码器侧，用于持续精炼全局语义；
- **不动点平衡与无损跨轮共享**：在训练阶段引入随机循环深度（Stochastic Recurrence Depth），强制模型在数学上收敛至不动点均衡态——后一轮循环能够无缝、无损地直接复用前一轮的 KV Cache 物理内存，彻底终结了轮次级的 KV 膨胀；
- **跨层与跨轮双重压缩**：结合非对称稀疏编码器本身的紧凑设计，Looped CED 仅用相当于标准循环 Transformer 1/6 的全局 KV Cache 显存，就捕获了其 86%~93% 的模型性能增益。

3. 关键结论：
针对参数量高达 552B 的 DeepSeek-V4.1-Flash 模型，在单台包含 4 张 NVIDIA GB200 加速卡的机架节点上进行 8 轮循环部署实测：若采用传统的逐层逐轮 KV 缓存，系统显存甚至连 1 个 128K 超长上下文请求都无法容纳；而 Looped CED 使得单 Token 占用的 KV 显存骤降 36.8 倍，单机轻松容纳 38 个 128K 并发请求（与完全不带循环的静态基线持平），在 8K 输入的常规压测中端到端服务吞吐量提升了整整 3.6 倍！

4. 背景地位：
大模型架构革新与底层系统显存工程协同演进的典范成果。成功将循环深度的理论算力放大优势，从实验室推向工业级生产环境（GB200 NVL 集群），打破了「超大模型无法兼顾参数循环与高吞吐 Serving」的固有成见。

5. 落地相关性：
对于正在调研下一代紧凑型推理底座、探索在受限 GPU 显存内塞入超大上下文推理服务的 AI 平台团队而言具有重大参考价值。为推理引擎显存池管理开辟了全新的「不动点原地复用」设计思路。

---

#### 10. CapBuddy: Efficient Physical Memory Management for Capability-based Resource-controlling Microkernel
- 中文译名：CapBuddy：面向基于权能资源控制微内核的高效物理内存管理系统
- 链接：https://arxiv.org/abs/2611.13036
- 作者：Zhuang Lu, Guangtao Zhu, Shijun Zhao, Qianying Zhang, Lixin Chen, 等（共 8 位作者，通讯作者：Zhuang Lu, Shijun Zhao）
- 单位：中国科学院信息工程研究所 (IIE, CAS) 【知名实验室】、中国科学院大学、新南威尔士大学 (UNSW Sydney)、首都师范大学
- 分类：cs.OS
- 方向标签：A. 容器与运行时 (微内核与沙箱隔离、seL4 Library OS、物理内存管理与安全开销消除)
- 相关度：4/5

1. 核心贡献：
中科院信工所（IIE）团队针对基于权能（Capability）的强隔离资源控制微内核（以国际顶尖安全微内核 seL4 为代表），攻克了其长期存在的用户态内存管理性能瓶颈。在现代机密计算沙箱和安全容器场景中，微内核通过将物理内存抽象为安全权能对象下放给用户态管理，但频繁的权能派生、撤销与微内核系统调用导致动态内存分配极其缓慢。作者提出了 CapBuddy，在权能保护的物理内存抽象之上构建了高效的双层 Buddy 系统，将权能重操作彻底剥离出内存请求的关键路径，使安全微内核的内存分配性能提升数十倍，逼近传统宏内核 Linux 水准。

2. 原理解析：
这好比在 Kubernetes 多租户安全隔离体系中，Pod 每次需要一块临时存储卷，都必须向控制面 API Server 申请签名证书并刷写 etcd 审计日志，导致本地 IOPS 极速暴跌：
- **安全权能与性能的矛盾**：seL4 等微内核要求对每块物理页的控制权都具备不可伪造的 Capability。传统的用户态 Buddy 算法每次内存拆分或合并，都必须同步触发昂贵的内核权能重新类型化（Retype）与微内核 IPC，关键路径陷入泥潭；
- **离线解耦与权能缓冲池**：CapBuddy 在用户态建立了一个安全的权能预分配缓冲池。当应用程序发起内存申请时，CapBuddy 直接在用户态完成高效的伙伴算法检索与位图计算，立即向应用返回可用的物理地址；
- **异步惰性同步**：所有与微内核安全机制相关的权能层级派生与合法性校验，全部被延后推移至后台离线处理，完全移出前台调用的临界区（Critical Path）。

3. 关键结论：
团队在 seL4 Library OS 上实现了 CapBuddy 完整原型。实测基准测试表明，CapBuddy 将原生 seL4 用户态 Buddy 系统的内存分配性能提升了 20 到 54.5 倍，其分配时延达到了与宏内核 Linux 同等数量级；在突发并发分配压测下，随着客户端并发数急剧增加，CapBuddy 依然保持了极低的中位数分配时延与卓越的可扩展性。

4. 背景地位：
发表于体系结构与代码优化顶刊 ACM TACO 的扎实操作系统成果。突破了长期阻碍 seL4 等形式化验证微内核在高性能生产场景（如安全容器 Kata/gVisor 替代底座、机密计算 Enclave）大规模落地的核心性能藩篱。

5. 落地相关性：
对于从事云原生安全容器（如基于安全微内核的下一代轻量级运行时沙箱）、边缘设备隔离节点以及机密计算平台研发的系统底层工程师具有直接价值，证明了无需削弱形式化安全边界即可获得工业级运行性能。

---

#### 11. Energy-Proportional Serverless Computing on SBC Clusters
- 中文译名：面向单板机集群的能耗比例型无服务器计算系统
- 链接：https://arxiv.org/abs/2611.14026
- 作者：Yuliya Sasinskaya, Natalie Carl, Niklas Kowallik, David Bermbach
- 单位：柏林工业大学 (TU Berlin - Mobile Cloud Computing Group)
- 分类：cs.DC
- 方向标签：A. 容器与运行时 (Serverless/FaaS 平台架构) & B. 编排与调度 (单板计算机集群物理节点 Scale-to-Zero、能耗比例调度与尾延迟优化)
- 相关度：4/5

1. 核心贡献：
柏林工业大学移动云团队针对边缘单板机（SBC）集群环境下的 Serverless / FaaS 计算，提出了一种将「缩容至零（Scale-to-Zero）」概念从单纯的容器函数实例下沉延伸至物理裸机电源状态的全新系统方案。作者敏锐指出，现有 Serverless 平台仅实现了代码层面的按需启动，但底层服务器在闲置（Idle）状态下依然消耗大部分基底功率，导致系统能耗无法与实际负载成比例。通过改造轻量级无服务器框架 tinyFaaS，系统将物理节点的通电/断电状态深度融入工作节点选择器中，实现了边缘集群的能耗比例计算（Energy-Proportionality）。

2. 原理解析：
这就像把 Kubernetes 的 Cluster Autoscaler 与 Kubelet 的节点生命周期直接做硬核物理协同：
- **无状态特性的硬件穿透**：Serverless 函数本身的无状态（Stateless）特性使得调度器可以在任意物理机之间自由迁移动态调用，无需维护复杂的本地脏数据；
- **电源感知的工作节点调度（Worker Selection）**：调度器持续监控集群的请求排队水位与到达率。当系统处于低谷时，调度器主动将流量向少数活跃节点紧凑编排，并将闲置的单板机物理节点彻底断电关机；当突发流量来临时，通过网络唤醒或智能 PDU 梯次唤醒物理节点；
- **尾延迟代价量化管理**：系统清晰剖析了从物理断电中唤醒的代价——由于完全冷启动需要约 1 分钟的物理主板引导时间，系统利用预测性微批次与常驻热备节点，将这种冷启动冲击严格隔离在最深层的尾部延迟中，确保常规流量无感。

3. 关键结论：
在真实物理单板机（SBC）集群上重放真实世界生产轨迹的压测表明，该方案在具有突发特征的流量轨迹下将集群平均功耗削减了 39.6%，在稀疏流量轨迹下功耗削减了 46.7%；在突发负载下，中位数时延几乎没有任何可察觉的变化，仅在全部节点休眠时到达的首次调用承担了约 1 分钟的节点引导尾延迟；在持续高负载下，平台自适应退化为全开的高性能集群。

4. 背景地位：
聚焦于边缘计算、绿色计算与可持续云基础设施（Green Computing）的前沿系统探索。首次在开源 FaaS 框架中完整打通了从上层微服务无状态调用到底层单板机电源管理的端到端控制回路。

5. 落地相关性：
对于边缘智能网关、车载计算集群、私有微型数据中心等能耗极度敏感场景的边缘 K8s（K3s/MicroK8s）运维团队具有极强借鉴意义。展示了在无需改造应用代码的前提下，如何通过调度器与硬件电源管理联动换取近 40% 的电费削减。

---

#### 12. Can KV Cache Be Reused Across Model Updates? A DeepSeek-V4-Flash Case Study
- 中文译名：大模型更新后 KV Cache 还能复用吗？以 DeepSeek-V4-Flash 为例的跨版本实证研究
- 链接：https://arxiv.org/abs/2611.14051
- 作者：Zhikun Tao, Junping Zhao, Fangyong Jin
- 单位：硅基流动 (SiliconFlow / SiFlow) 【工业界】
- 分类：cs.DC, cs.AI
- 方向标签：C. AI Infra (KV Cache 跨版本复用、DeepSeek-V4-Flash 推理优化、首字延迟 TTFT 加速)
- 相关度：4/5

1. 核心贡献：
由硅基流动（SiliconFlow）技术团队领衔完成。在大模型快速迭代的时代，底模版本微调升级（如从 DeepSeek-V4-Flash 更新到 0731/1017 补丁版本）极其频繁，而既有全局 KV Cache 往往被全量作废重算。本论文在业界首次针对真实生产级大模型跨版本更新，展开了「已生成的 KV Cache 能否直接被新版本模型继承复用」的系统实证调研。团队创新性提出了「功能性缓存分歧度（Functional Cache Divergence, FCD）」量化指标，证明在长文本 QA 任务中直接复用旧缓存可实现高达 2.10~5.08 倍的首字生成（TTFT）性能飞跃，并系统揭示了跨版本复用的能力边界。

2. 原理解析：
这就像在容器镜像构建中，利用上一版本的基础镜像层缓存来跳过某些冗长的编译步骤：
- **核心科学发问**：当模型的权重参数发生了微调漂移，上一代模型吐出的历史 KV Cache 物理矩阵中，究竟保留了多少有用的任务语义？新模型能否「读懂」旧模型写下的记忆？
- **任务实用性与原生保真度的分离**：实证发现，直接复用旧 KV Cache 虽然会导致新模型的内层激活状态偏离其原生轨迹，但在许多下游任务中，其最终的分类与检索判定结果依然高度正确（Answer-Margin 分析表明正确决策能够承受相当幅度的内部状态扰动）；
- **自然文本延续 vs 精确单 Token 检索的边界**：在自然语言连续生成场景下，跨版本 KV 复用展现出极高的语义兼容度；但在大海捞针（Needle-In-A-Haystack）等极端依赖精确键值匹配的长文本任务中，随着 Prefix 长度超过 16K/32K，直接复用的精度会逐步出现衰退。

3. 关键结论：
团队针对 DeepSeek-V4-Flash 至 Flash-0731、DeepSeek-V4.1-Flash 至 Flash-1017、GLM 系列以及 Qwen 系列等 4 组经典模型版本迭代展开了详尽评测。在 3 个长前缀问答基准测试上，直接复用既有缓存将中位数首字生成延迟（TTFT）大幅缩短了 2.10 到 5.08 倍；在 32K 长度的大海捞针测试中，DeepSeek-V4.1-Flash 的跨版本复用准确率依然高达 97.92%，与原生推理高度重合。

4. 背景地位：
大模型推理领域极少见的工业界逆向实证探索。推翻了长期以来「模型权重一改、KV Cache 必须全部废弃重算」的教条思维，首次确立了将「任务效用（Task Utility）」与「原生推理保真度（Native Fidelity）」解耦的全新评估标准。

5. 落地相关性：
对于运营大规模云端知识库、持续交互式智能体以及企业级 RAG 系统的团队而言具有颠覆性的成本价值。在模型版本微调或 A/B 测试滚动发布时，利用该策略能够直接复用数以 TB 计的历史 KV 缓存，极大缓解上线瞬间推理集群的算力雪崩与冷启动时延。

---

### 其他论文（相关度 ≤2）

以下为今日抓取的其余 22 篇候选论文，主要属于理论分布式算法、专用控制优化、端侧应用及硬件架构仿真，相关度较低，在此简要列出以备参考：

1. **Two-Tier Task Offloading for Satellite-Assisted Marine Networks: A Hybrid Stackelberg-Bargaining Game Approach** (cs.DC)
   - 链接：https://arxiv.org/abs/2611.13019 | 相关度：2/5
   - 简评：基于博弈论的空天地海多接入边缘计算任务卸载与定价算法，偏向海洋物联网与卫星通信。
2. **PegasusAI Studio: Legible Cyberinfrastructure and Accountable AI Agents for Scientific Workflows** (cs.DC, cs.AI, cs.SE)
   - 链接：https://arxiv.org/abs/2611.13309 | 相关度：2.5/5
   - 简评：结合 Pegasus 与 HTCondor 工作流网关的科学智能体可信环境构建，偏向网格计算与科研基础设施。
3. **FP64 Performance and the Limits of Ozaki Emulation on HPC Systems** (cs.DC, math.NA)
   - 链接：https://arxiv.org/abs/2611.13332 | 相关度：2.5/5
   - 简评：劳伦斯利弗莫尔国家实验室等评测 Ozaki 方法在 Tensor Core 上模拟双精度 FP64 的适用边界，偏向 HPC 科学计算。
4. **Multi-Objective Scheduling of LLM-Based Multi-Agent Workflows in Cloud Computing** (cs.DC)
   - 链接：https://arxiv.org/abs/2611.13740 | 相关度：2.5/5
   - 简评：基于遗传算法与启发式规则的多智能体工作流在公有云中的多目标拓扑调度。
5. **Scaling Shapley Energy Attribution to Large LLM Batches** (cs.DC, cs.AR, cs.PF)
   - 链接：https://arxiv.org/abs/2611.13802 | 相关度：2.5/5
   - 简评：基于微基准校准与闭式解将大模型连续批处理中的能耗按 Shapley 值精确分摊至单请求，偏向能耗审计与多租户计费。
6. **Performance Portability Explained: Insights from accelerating ICON microphysics** (cs.DC, cs.PF, cs.PL)
   - 链接：https://arxiv.org/abs/2611.14204 | 相关度：2/5
   - 简评：苏黎世联邦理工学院 Torsten Hoefler 等针对气候微物理内核跨 7 种可移植性框架的 HPC 性能移植性评测。
7. **RBLA+: Efficient Rank-Specific LoRA Adapter Extraction for Federated Fine-Tuning with Heterogeneous Clients** (cs.AI, cs.DC)
   - 链接：https://arxiv.org/abs/2611.12961 | 相关度：2/5
   - 简评：面向异构客户端联邦微调的紧凑 QR/SVD 秩特异性 LoRA 适配器提取方案。
8. **Darmok: Championship Cryptic Crossword Solving via Constraint Tightening and Resilient Orchestration** (cs.AI, cs.CL, cs.DC)
   - 链接：https://arxiv.org/abs/2611.13557 | 相关度：1.5/5
   - 简评：利用多模型交叉校验与字典回溯求解英国填字游戏的自动化解题编排系统。
9. **Deterministic, Reproducible Inference in Exact Integer Arithmetic, and Verifiable Distributed Inference as Its Consequence** (cs.LG, cs.DC, cs.SE)
   - 链接：https://arxiv.org/abs/2611.13730 | 相关度：2.5/5
   - 简评：基于全整数确定性算术的跨硬件分布式推理运行时 tritify，验证在 3 台网络机器上比特一致切分运行 106B 大模型。
10. **On Federated Averaging with Partial Participation under a General Variance Condition** (math.OC, cs.DC, cs.LG)
    - 链接：https://arxiv.org/abs/2611.14239 | 相关度：1/5
    - 简评：非凸优化下带部分参与的 FedAvg 算法有限时间平稳性界收敛性理论分析。
11. **EngineAgent: Agentizing On-Device LLM Inference Engines with Inference Stack Hierarchy Awareness and Hardware Abilities** (cs.OS, cs.AI, cs.CL, cs.SE)
    - 链接：https://arxiv.org/abs/2611.14356 | 相关度：2.5/5
    - 简评：上海交大与阿里联合研发的自动化端侧大模型推理引擎代码生成与多后端适配智能体。
12. **WINIC: An Automatic Cycle-Accurate Multi-Platform Microbenchmarking Tool for Instruction Performance Metrics** (cs.PF)
    - 链接：https://arxiv.org/abs/2611.13978 | 相关度：2/5
    - 简评：无需 root 权限的跨平台汇编指令级微基准自动化测试工具，支持 x86、AArch64 与 RISC-V。
13. **SPMW: A Grid-Based Programming Model for Scalable Accelerator Design** (cs.PL, cs.AR)
    - 链接：https://arxiv.org/abs/2611.12944 | 相关度：2/5
    - 简评：康奈尔大学团队提出的面向规则网格硬件加速器设计的单程序多连接工作单元编程模型与 MLIR 编译器。
14. **FAME-QP: A GPU-Accelerated Quadratic-Programming Solver for Real-Time Model Predictive Control** (cs.RO, cs.GR, eess.SY)
    - 链接：https://arxiv.org/abs/2611.13766 | 相关度：1.5/5
    - 简评：基于 CUDA Graph 与算子缓存的高性能 GPU 二次规划求解器，用于机器人模型预测控制。
15. **Uncovering the Memory Hierarchy of Modern NVIDIA GPUs for Accurate Simulation** (cs.AR)
    - 链接：https://arxiv.org/abs/2611.13860 | 相关度：2.5/5
    - 简评：港科大（广州）与清华大学通过微汇编逆向工程揭秘现代 NVIDIA GPU 未公开的缓存组相联度与哈希路由机制。
16. **Online Adaptive Clustering in Robust Distributed Model Predictive Control** (eess.SY)
    - 链接：https://arxiv.org/abs/2611.13923 | 相关度：1/5
    - 简评：鲁棒分布式模型预测控制中的在线动态拓扑自适应聚类框架。
17. **HERO-D3QN: Inter-Cluster Routing with Energy-Aware Soft Constraints in Wireless Sensor Networks** (cs.NI)
    - 链接：https://arxiv.org/abs/2611.13943 | 相关度：1/5
    - 简评：基于深度强化学习的无线传感器网络能量均衡集群间路由优化。
18. **What to Predict for Efficient Scheduling on Parallel Machines** (cs.DS)
    - 链接：https://arxiv.org/abs/2611.13980 | 相关度：1.5/5
    - 简评：并行机器完工时间最小化调度中的学习增强算法容错界理论研究。
19. **Accelerating matrix-free fast diagonalization and preconditioned linear solvers for higher-order finite element discretized elliptic problems on distributed GPUs** (math.NA, physics.comp-ph)
    - 链接：https://arxiv.org/abs/2611.14041 | 相关度：1.5/5
    - 简评：面向高阶有限元离散椭圆方程在分布式 GPU 上的无矩阵快速对角化预条件求解器。
20. **SinkState: On-the-Fly SVD of Recurrent States for Efficient Hybrid LLM Serving** (cs.LG)
    - 链接：https://arxiv.org/abs/2611.14246 | 相关度：2.5/5
    - 简评：罗格斯大学针对 Mamba-2 与 Gated DeltaNet 等混合大模型，利用局部 SVD 在线压缩循环隐藏状态以加速解码。
21. **Lilo: A Multi-Agent Conversational Sandbox for Children's Digital Communication** (cs.HC, cs.AI)
    - 链接：https://arxiv.org/abs/2611.14260 | 相关度：1/5
    - 简评：面向儿童同伴社交沟通的多智能体冲突演练沙箱系统。
22. **Two Communities, One Problem: Branch-and-Bound vs. A* for Resource-Constrained Project Scheduling** (math.OC, cs.AI)
    - 链接：https://arxiv.org/abs/2611.14426 | 相关度：1/5
    - 简评：运筹学分支定界法与人工智能 A* 搜索算法在资源受限项目调度中的底层机制对比。

---

### 今日趋势小结

通读今日全部 34 篇系统方向最新文献，容器编排、操作系统底座与 AI 基础设施正呈现出三股极具启示性的演进浪潮：

1. **智能体（Agent）服务化对前缀缓存（Prefix Caching）体系带来颠覆性冲击**：
   过去的 LLM Serving 优化主要围绕单次短请求或静态长文档展开。而今日微软 Azure 团队的两项重磅研究（论文 1 与论文 4）给整个云原生社区敲响了警钟：多模型逐步路由直接导致不同模型间的 Prefix Cache 归零重算，催生了像 SHADOWPREFILL 这样利用底层 SLO 闲置时间做影子预取的创新机制；更严峻的是，论文 4 首次用严格数学模型证实，前缀缓存系统在面临短时流量突发时会陷入持续数十甚至上百分钟的「亚稳态性能雪崩」。这证明 Kubernetes 上传统的外部 Pod 扩缩容和请求限流已完全失灵，未来的大模型推理必须具备深度感知会话级 KV 显存预算的主动挂起/恢复控制面。

2. **硬件拓扑（NVLink / PCIe / NVMe）驱动推理算子与并行策略发生结构性解耦**：
   在机架级互连和超大参数模型时代，软件栈正在全方位贴合物理硬件的时序与拓扑特征：NVIDIA 官方（论文 2）利用 Blackwell 对称内存构建单边直写 MoE All-to-All，彻底去除了通信前的元数据握手开销；NVIDIA 与 TAMU（论文 3）提出的 TKNP 架构打破了十年来模型权重与注意力计算绑定的思维定势，跨节点仅流通单 Token 激活值；而微软与独立研究员（论文 5）针对 DeepSeek-V4.1 Engram 查表提出的 SlackTier，更是巧妙利用第 1 层与第 14 层相差 30 倍的时间窗口将巨型表卸载至 NVMe 固态硬盘，节约了上百 GB 主机内存。

3. **大模型全生命周期的系统可靠性与工程落地正在告别「黑盒粗放」**：
   无论是亚马逊 AWS 团队（论文 6）深入生产集群一线总结出的 7 大静默故障范式与 Plumbline 自动化验证系统，还是港科大与清华团队（论文 8）击穿 NVIDIA 官方 Profiler 聚合壁垒实现的 2% 极低误差推理时延解析模型，抑或是硅基流动（论文 12）针对 DeepSeek-V4-Flash 首次验证跨版本 KV Cache 的可用性边界，都标志着大模型基础设施正在从前期的「盲目堆卡粗放式炼丹」快速迈入「精细微架构刻画、全链路形式化验证与极致降本增效」的成熟工业化新阶段。
"""

out_file = '/Users/xqr/.gemini/antigravity/scratch/arxiv-systems-daily/today_report.md'
with open(out_file, 'w', encoding='utf-8') as f:
    f.write(report_content)

print(f'Successfully generated {out_file}, size: {len(report_content)} characters.')
