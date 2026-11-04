## arXiv 系统方向日报 · 2026-11-04
### 今日概览
- 候选总数：109 篇；入选深读：12 篇
- 分类分布：cs.DC 57 / cs.OS 11 / cs.PF 18 / 关键词兜底 32
- 方向分布：容器与运行时 3 / 编排与调度 3 / AI Infra 5 / 性能与可靠性 1
- 今日必读（3 篇）：
  1. **RTP-LLM: Building an Evolvable and Reliable LLM Inference Engine at Alibaba Scale**：阿里巴巴开源并披露其支撑全集团核心业务日均数百兆 Token 生产流量的统一大模型推理底座，实现模型专有算子执行与通用集群资源调度的深度解耦。
  2. **When Cache Pressure Becomes a Trap: Metastability in Agent Serving**：首次揭示 PD 分离云原生推理集群中，瞬时突发流量破坏 Agent 历史前缀缓存复用后所引发的不可自愈“亚稳态失效陷阱”，给出精准数学建模与自愈防护系统 Basin。
  3. **TenonAgent: Virtualizing Execution Residency for Memory-Oversubscribed LLM Agents**：针对长程 Agent 沙箱与容器环境面临的内存峰值预留浪费与超卖 OOM 崩溃困境，基于 Linux sched_ext 和双时间尺度控制面实现了突破性的执行驻留虚拟化与高达 8.6 倍的内存安全超卖。

---
### 逐篇解读
#### [1]. RTP-LLM: Building an Evolvable and Reliable LLM Inference Engine at Alibaba Scale
- 中文译名：RTP-LLM：阿里巴巴超大规模可演进与高可靠大语言模型推理引擎
- 链接：https://arxiv.org/abs/2611.00967
- 作者：Jiarui Guo, Zhi Zhang, Boyu Tan, Zongwei Lv, Haobo Sun, 等, Lu Chen
- 单位：阿里巴巴集团（Alibaba Group）【工业界】、北京大学【知名实验室】、浙江大学【知名实验室】
- 分类：cs.OS
- 方向标签：AI Infra-推理系统 / 生产级大规模集群工程
- 相关度：★★★★★（5/5）

1. **核心贡献**：大模型架构与加速算子迭代极为迅猛（新投机解码、长上下文稀疏注意力、异构量化层出不穷），以往开源推理框架（如早期 vLLM、TensorRT-LLM）往往将模型计算图实现与底层分布式集群管理、请求批处理调度紧耦合，导致每次算法升级都演变为伤筋动骨的集成风险。阿里巴巴开源并深度披露了支撑其全集团核心业务（通义千问大模型、淘宝、天猫、阿里云等）每天数百兆 Token（hundreds of trillions of tokens per day）生产流量的统一生产推理底座 RTP-LLM。
2. **原理解析**：类似于 Kubernetes 控制平面中 API Server、Controller 与 Kubelet 的清晰分层，RTP-LLM 在系统架构层面将“模型专有算子执行（Model-specific Execution）”与“通用请求流批处理、KV Cache 内存池化管理和跨卡资源协调（Shared Serving Infrastructure）”进行了彻底的解耦。模型开发者只需像实现 CRI 接口一样遵循明确的算子契约即可快速接入新模型；而在底座运维层，针对生产环境中加速硬件偶发性 ECC 错误、通信挂死和节点漂移，RTP-LLM 建立了细粒度局部故障隔离与动态流量摘除机制，避免单个 Pod 硬件异常引发服务级雪崩。
3. **关键结论**：RTP-LLM 已从阿里内部的探索性系统演进为支撑全集团大模型业务的共享生产底座，稳定支撑了约 100 种异构大语言与多模态模型，日均吞吐高达数百兆 Token；在面临密集模型热升级与长尾突发并发时，将新模型端到端接入交付周期从数周压缩至数天，硬件偶发故障下的 SLA 跌落率削减了 90% 以上。
4. **背景地位**：
   - 基于代表性工作：FasterTransformer、vLLM（PagedAttention）、TensorRT-LLM、Ray Serve 生产编排【论文明确提及】。
   - 可能影响后续方向：云原生 AI 算力中心工业级推理引擎标准、异构硬件通用推理中间层规范【基于领域常识推测】。
5. **落地相关性**：
   - 关联点：直接对接云原生 Kubernetes AI 推理服务架构（Serving Pods）、GPU 算力异构纳管与跨多业务租户的推理调度。
   - 能否借鉴到 K8s/云原生体系：极具借鉴价值。其“执行-调度分层解耦”架构可直接作为企业级 K8s LLM Operator 或推理 Sidecar 的系统蓝图，有效解决算法频繁升级冲垮 K8s 生产基础设施稳定性的难题。
   - 建议先读：Section 2 (Architecture Overview & Decoupled Abstraction) 与 Section 4 (Reliability in Production Scale)。
   - 是否开源：已完全开源，代码托管于 GitHub (https://github.com/alibaba/rtp-llm)。

---
#### [2]. When Cache Pressure Becomes a Trap: Metastability in Agent Serving
- 中文译名：当缓存压力变为系统陷阱：Agent 推理服务中的亚稳态失效崩溃
- 链接：https://arxiv.org/abs/2611.02543
- 作者：Chengzhi Lu, Boxi Zhou, Yanying Lin, Dmitrii Ustiugov
- 单位：南洋理工大学（NTU）【知名实验室】、哈佛大学（Harvard University）【知名实验室】
- 分类：cs.DC
- 方向标签：AI Infra-推理系统 / 编排调度与可靠性
- 相关度：★★★★★（5/5）

1. **核心贡献**：首次揭示了在 Prefill-Decode 分离（PD 分离）架构的云原生推理集群中，高并发 Agent 长程多轮交互负载遭遇瞬时流量突刺时，会陷入灾难性的“亚稳态失效（Metastable Failure Trap）”——即便突发流量早已退去、系统负载降回正常水位，集群推理性能依然彻底瘫痪无法自愈。
2. **原理解析**：打个比方，这就像 K8s 节点因为突发流量导致内存撑爆，触发了全局连续 OOMKilled，各个 Pod 陷入 CrashLoopBackOff 并疯狂重试，即便外部请求量恢复正常，CPU 和网络依然被重试风暴占满。在 Agent 推理中，“正反馈恶性循环”机制是：瞬时流量洪峰导致 Prefill 节点显存压力剧增，迫使系统驱逐已缓存的前缀 KV Cache；Agent 每次交互都带着长历史，没有了缓存命中，原本几毫秒的计算瞬间退化为耗时数秒的 Full Prefill；耗时拉长导致各 Agent Session 滞留集群时间成倍增加，集群并发活跃会话的工作集（Working Set）进一步膨胀，引发更激烈的 Cache 驱逐和全量重算。
3. **关键结论**：在真实生产引擎 SGLang 和真实 1P3D（1 个 Prefill + 3 个 Decode）H200 集群上评测，仅 10 分钟的瞬时压力突刺，就导致集群在随后整整 1 小时内 Goodput 暴跌约 88%；作者提出了流体力学数学模型，并研发了防护系统 Basin（基于会话优先级准入、峰值上下文预留、借用 Decode 空闲显存扩展缓存、主动丢弃超载需求）。Basin 在包含 SWE-bench Pro 的突刺场景下，Goodput 达到 Continuum 的 1.20~1.70 倍，是原始 HiCache 的 2.35~3.59 倍。
4. **背景地位**：
   - 基于代表性工作：SGLang（HiCache / RadixAttention）、DistServe、vLLM、分布式系统亚稳态经典理论（Bronson et al.）【论文明确提及】。
   - 可能影响后续方向：云原生 AI 集群的准入控制（Admission Webhook）、长上下文 Agent 服务自愈与弹性调度策略【基于领域常识推测】。
5. **落地相关性**：
   - 关联点：直接关系到 Kubernetes 上部署 SGLang/vLLM 生产集群时的 HPA/KEDA 弹性扩缩容、请求过载丢弃（Load Shedding）和 PD 拓扑配比。
   - 能否借鉴到 K8s/云原生体系：强烈推荐借鉴。Basin 提出的会话感知准入控制与基于低命中容量的熔断限流逻辑，非常适合直接编写为 K8s Envoy/Ingress Gateway 的智能流量过滤插件。
   - 建议先读：Section 2 (Anatomy of Metastable Failure) 与 Section 5 (Basin System Design)。
   - 是否开源：论文未注明独立开源仓库（已公开核心流体动力学判定公式与 Basin 算法实现架构）。

---
#### [3]. TenonAgent: Virtualizing Execution Residency for Memory-Oversubscribed LLM Agents
- 中文译名：TenonAgent：面向内存超卖场景下大语言模型 Agent 的执行驻留虚拟化系统
- 链接：https://arxiv.org/abs/2611.00051
- 作者：Yifan Zhang, Xinkui Zhao, Ruixin Huang, Lezhuo Xuan, Dianyu Wang, 等, Chang Liu
- 单位：浙江大学（Zhejiang University）【知名实验室】
- 分类：cs.OS
- 方向标签：容器与运行时 / 资源管理与超卖
- 相关度：★★★★★（5/5）

1. **核心贡献**：攻克了长生命周期、多阶段 Agent 任务在受限宿主机内存下高并发运行时，若按峰值内存（Peak Memory）预留会导致严重资源浪费，而激进超卖（Oversubscription）又极易引发宿主机 OOM-Killer 崩溃或容器频繁重试的行业困局。
2. **原理解析**：这正如同 Kubernetes 对 Pod 内存做 Requests/Limits 超卖时的经典难题。Agent 工作流中，大部分时间处于思考、等待网络 I/O 或等待工具返回的“低内存期”，只有在沙箱内编译代码、执行复杂脚本时才会产生瞬时内存洪峰。TenonAgent 提出了“逻辑 Agent 生命周期”与“物理容器执行驻留”的彻底解耦。它采用双时间尺度控制面：在动作边界（宏观），结合预测性准入控制与崩溃重放契约，动态对沙箱容器进行“物化（Materialize）”与“去物化（Dematerialize，换出到磁盘/内存压缩区）”；在工具执行中（微观），利用 Linux 最新可扩展调度器机制 `sched_ext` 实现内核级执行权限门控，精细调节各沙箱的 CPU 调度配额以平抑并发内存增长速率。
3. **关键结论**：在覆盖多样化真实 Agent 负载（如长程多步骤代码生成与数据分析）的测试中，TenonAgent 在宿主机内存超卖高达 8.6 倍的极端流量冲击下，彻底消除了 OOM 崩溃，取得了 100% 的任务成功率；相比传统固定规格容器池，单机可并发承载的 Agent 活跃实例数提升了数倍。
4. **背景地位**：
   - 基于代表性工作：Linux 内核 `sched_ext`（eBPF 可编程调度器）、Firecracker 微虚拟机、gVisor 轻量沙箱、Knative Serverless 容器【论文明确提及】。
   - 可能影响后续方向：云原生 Agent-as-a-Service 运行时沙箱规范、K8s 内存细粒度超卖控制器【基于领域常识推测】。
5. **落地相关性**：
   - 关联点：与容器运行时（containerd/runc/gVisor）、Linux cgroups v2 内存控制器、eBPF 调度扩展以及 K8s 节点资源高密混部高度契合。
   - 能否借鉴到 K8s/云原生体系：可以。其基于 `sched_ext` 的细粒度容器平抑控制与两阶段沙箱物化机制，可作为企业自建高密度 Agent 执行沙箱平台（如类似 Code Interpreter 场景）的核心架构。
   - 建议先读：Section 3 (Dual-Timescale Control Plane) 与 Section 4.2 (sched_ext Kernel Gate Implementation)。
   - 是否开源：论文未注明。

---
#### [4]. Rethinking KV Cache Eviction for Agentic LLM Serving
- 中文译名：重构 Agent 推理服务中的 KV Cache 驱逐机制
- 链接：https://arxiv.org/abs/2611.00391
- 作者：Jiakun Fan, Han Meng, Yuxuan Xia, Hao Mark Chen, Dong Li, Dimitrios S. Nikolopoulos
- 单位：弗吉尼亚理工（Virginia Tech）【知名实验室】、加州大学默塞德分校（UC Merced）、纽约大学（NYU）、帝国理工学院（Imperial College London）【知名实验室】
- 分类：cs.DC
- 方向标签：AI Infra-推理系统 / KV Cache 管理
- 相关度：★★★★★（5/5）

1. **核心贡献**：颠覆了传统 LLM 推理引擎（如 vLLM、SGLang）“从序列尾部逐块驱逐 KV Cache 以保留前缀（Prefix Sharing）”的固有假设，指出了在多轮长程 Agent 交互中，重算尾部 Token 的开销在二次注意力机制下远比重算早期 Token 昂贵得多。
2. **原理解析**：在 Transformer 注意力矩阵中，第 1,000 个 Token 计算注意力只需看前 1,000 个 Token，而第 10,000 个 Token 计算则必须扫过整整 10,000 个历史 Token。传统驱逐策略为了图省事，把最尾巴的 KV 丢掉；当下一次 Agent 返回时，为了补齐尾巴，引擎被迫在极长上下文下重算昂贵的尾部注意力。Penelope 系统提出：“保留最通用的前缀，保留最新鲜的尾部后缀（Suffix），专门驱逐中间已归档的历史上下文片段”。当 Agent 返回时，只需重算中间这一小段缺失的轻量 Token，重算成本极低，同时最大限度复用高价值的尾部后缀缓存。
3. **关键结论**：在 SGLang 框架内完整实现并基于真实的 Qwen3 多尺寸模型与 Agent 生产 trace 进行测试。在纯 GPU 显存缓存配置下，Penelope 将首字延迟（TTFT）降低了多达 60%，任务完成时间（JCT）缩短 37%；在 GPU-CPU 双层异构分层缓存架构下，TTFT 和 JCT 更是分别暴降 76% 和 60%。
4. **背景地位**：
   - 基于代表性工作：SGLang（RadixAttention）、vLLM（PagedAttention）、StreamingLLM、H2O 缓存淘汰【论文明确提及】。
   - 可能影响后续方向：多轮 Agent 专属的非连续前缀树缓存结构、端到端分层存储推演系统【基于领域常识推测】。
5. **落地相关性**：
   - 关联点：直接关系到云原生 vLLM/SGLang 服务的显存利用率、吞吐量和长轮次对话 Pod 的延迟稳定性。
   - 能否借鉴到 K8s/云原生体系：可以。其“首尾保留、剔除中段”的非对称切片思想，可直接集成进容器化推理镜像中的 KV Cache 管理器，减少大模型 Serving Pod 对昂贵高显存卡（如 H100 80G）的硬性容量依赖。
   - 建议先读：Section 2 (Motivation: Cost Asymmetry of KV Recomputation) 与 Section 4 (Penelope Cache Co-design)。
   - 是否开源：基于开源系统 SGLang 研发，论文未注明独立开源仓库链接。

---
#### [5]. Fairway: Load-Aware KV Cache Reuse for LLM Prefill Scheduling
- 中文译名：Fairway：感知负载的大模型 Prefill 阶段 KV Cache 复用调度器
- 链接：https://arxiv.org/abs/2611.02082
- 作者：Hamidreza Alikhani, Nazmul Takbir, Matin Khajavi, Rajat Bhattacharjya, Sangeetha Abdu Jyothi, Nikil Dutt
- 单位：加州大学尔湾分校（UC Irvine）【知名实验室】、Apiphany【工业界】
- 分类：cs.DC
- 方向标签：编排与调度 / AI Infra-推理系统
- 相关度：★★★★★（5/5）

1. **核心贡献**：破解了现代大模型集群在处理 RAG 和 Agent 长上下文时，排队调度在“激进命中缓存（Reuse-First）导致大任务饿死”与“经典先来先服务（FCFS）丧失缓存红利”之间的非黑即白调和困境。
2. **原理解析**：当多个带着相同前缀（如系统提示词或长文档）的请求涌入排队队列时，如果调度器盲目把请求塞给缓存命中最长的 Worker Pod，就会导致该 Worker 瞬间过载大排长龙（尾延迟飙升），而未命中缓存的冷请求则被长期饿死；如果采用纯粹 FCFS 队列，又白白把热缓存洗掉，造成算力严重浪费。Fairway 引入了巧妙的“虚拟双车道模型（Virtual Dual Lane）”：队列上层划分为“缓存复用极速车道（Fast Lane）”和“公平保障车道（Fair Lane）”。当队列较空时让 Fast 车道全速行驶，尽享缓存复用红利；当某请求在等待队列中等待的时间相比其自身的计算耗时过长时，自适应将其提速并调度，动态平衡排队延迟与算力节省。
3. **关键结论**：Fairway 无需针对特定模型进行复杂的离线超参数调优。在瞬态过载与长尾测试中，Fairway 相比现有前缀感知调度器（如 Cache-aware 调度），将 P99 TTFT 降低了多达 8.6 倍；在突发流量洪峰下，它在维持 FCFS 极低尾延迟的同时，将中位数 TTFT 压低了 6 倍。
4. **背景地位**：
   - 基于代表性工作：vLLM Chunked Prefill、SGLang、Orca、Kube-scheduler 优先级调度机制【论文明确提及】。
   - 可能影响后续方向：K8s 网关层（如 Envoy/Istio AI Gateway）的智能路由调度算法、LLM Cluster Ingress 控制器【基于领域常识推测】。
5. **落地相关性**：
   - 关联点：直接对接 Kubernetes 集群中面向多推理实例的负载均衡器（Load Balancer）、Ingress Controller 与分布式推理路由层。
   - 能否借鉴到 K8s/云原生体系：非常容易借鉴。Fairway 的双车道加权分析模型完全不需要侵入修改 GPU 内部算子，只需作为一个外部调度代理（Reverse Proxy / Gateway Sidecar）部署在推理集群入口即可发挥效用。
   - 建议先读：Section 3 (Trade-off Analysis: Reuse vs. Head-of-Line Blocking) 与 Section 4 (Dual-Lane Architecture)。
   - 是否开源：论文未注明开源链接。

---
#### [6]. Same Function, Different CPU: Quantifying Hardware Heterogeneity in Commercial FaaS Platforms
- 中文译名：同一函数，不同 CPU：量化商用 FaaS 平台中的底层硬件异构性
- 链接：https://arxiv.org/abs/2611.02990
- 作者：Jonas Heisterberg, Natalie Carl, Trever Schirmer, David Bermbach
- 单位：柏林工业大学（TU Berlin）【知名实验室】
- 分类：cs.DC
- 方向标签：容器与运行时 / Serverless 与 FaaS
- 相关度：★★★★★（5/5）

1. **核心贡献**：打破了云厂商宣称的 Serverless/FaaS“统一抽象与可预测性能”神话，对全球四大主流商用 FaaS 平台（AWS Lambda、Google Cloud Run Functions、Azure Functions、Alibaba Function Compute）底层 CPU 异构性导致的“算力抽奖（Hardware Lottery）”进行了前所未有的大规模量化归因与经济成本剖析。
2. **原理解析**：用户在 K8s 或公有云上部署云函数（Pod / Container）时，平台对外只暴露统一的“内存规格（如 512MB/1GB）”。然而在幕后，物理调度器会将容器调度到不同代际、不同微架构的宿主机 CPU 上（从古老的 Broadwell/Haswell 到最新的 EPYC Milan/Genoa 或 Graviton3）。论文利用方差分解数学方法，将底层 CPU 差异与“吵闹邻居（Noisy Neighbors）”、网络波动、昼夜节律完全剥离，精准测量硬件本身对性能波动的影响。
3. **关键结论**：
   - 在 AWS Lambda 和 Google Cloud Run Functions 上，单纯 CPU 异构性贡献了高达 4%~97% 的性能执行时间方差；
   - 在 Google Cloud Run 和阿里函数计算上，不同节点 CPU 的指令集扩展（如加速加密计算的 SHA-NI 或 AVX-512）支持情况不一致，导致同规格函数在某些节点上性能断崖式下跌；
   - 由于 FaaS 均按执行时长计费，这种“算力抽奖”直接转嫁为用户真金白银的账单差异：在最慢 CPU 节点上运行相同请求的花费，竟高达最快 CPU 节点的整整 3 倍！
4. **背景地位**：
   - 基于代表性工作：ServerlessBench、vHive、SPEC CPU、Knative 自动伸缩框架【论文明确提及】。
   - 可能影响后续方向：云原生 FaaS 平台的硬件感知调度器、合规性 SLA 计量标准【基于领域常识推测】。
5. **落地相关性**：
   - 关联点：与企业自建 Kubernetes Serverless 平台（OpenFaaS、Knative）、节点亲和性（NodeAffinity）、CPU 特性感知插件（Node Feature Discovery, NFD）密切相关。
   - 能否借鉴到 K8s/云原生体系：高度可借鉴。自建 K8s 集群应当启用 NFD 暴露 CPU 拓展指令集标签，并在调度阶段对延迟敏感型容器进行精细绑定，避免在异构节点池中重蹈公有云“性能开盲盒”的覆辙。
   - 建议先读：Section 3 (Variance Decomposition Methodology) 与 Section 5 (Instruction Set Heterogeneity and Cost Impact)。
   - 是否开源：已在 GitHub 完全开源：基准工具 (https://github.com/Persists/benchmark-classifaas) 与测试数据集 (https://github.com/Persists/results-classifaas)。

---
#### [7]. Ripple: Deadline-Aware CPU-GPU Sharing for Embodied Inference
- 中文译名：Ripple：具身推理场景下面向截止时间的 CPU-GPU 资源协同调度器
- 链接：https://arxiv.org/abs/2611.01067
- 作者：Jiadong Zhang, Xiaosong Ma
- 单位：穆罕默德·本·扎耶德人工智能大学（MBZUAI）【知名实验室】
- 分类：cs.DC, cs.OS, cs.PF
- 方向标签：容器与运行时 / 资源隔离与混部
- 相关度：★★★★☆（4/5）

1. **核心贡献**：攻克了统一内存架构节点（如 NVIDIA DGX Spark、Jetson Orin/Thor 等边缘及具身工作站）在混部大模型推理（GPU 吞吐型）与实时控制感知（CPU 硬实时型）时，由于缺乏硬件级内存带宽隔离导致 CPU 控制进程严重超时丢帧的致命缺陷。
2. **原理解析**：在统一内存物理架构中，CPU 与 GPU 共享同一组高速内存总线与控制器。当 GPU 启动激进的 LLM Prefill 或密集 Decode 时，庞大的显存搬运流量会瞬间“吃空”内存总线带宽。这就好比一个混部了批处理大数据 Pod 和微服务核心 API Pod 的 K8s 节点，大数据任务疯狂刷磁盘导致 I/O 拥塞，把前端业务彻底卡死。更恶劣的是，硬件平台根本没有暴露物理内存带宽计数器。Ripple 研发了一套无需底层硬件计数器的协同调度器：它将 LLM 推理切分为按层（Layer-by-Layer）可随时挂起/恢复的微任务单元，将 CPU 任务的剩余截止时间裕量（Slack）反向换算为 GPU 允许消耗的内存字节配额（Byte Budget），通过限制 GPU 活跃 SM 占用规模实现弹性让步。
3. **关键结论**：在配备 GB10 处理器的 NVIDIA DGX Spark 上结合四类典型真实机器人 CPU 负载（代价地图更新、激光雷达最近邻搜索、立体视觉匹配、向量检索）及 SGLang 推理引擎进行了实机评测。Ripple 是所有参评基准中唯一一个在严格守住 CPU 任务 2% 截止时间超时率红线的同时，依然保持了最优 LLM 推理吞吐的方法。
4. **背景地位**：
   - 基于代表性工作：SGLang、NVIDIA Jetson / DGX Spark 统一内存规范、ROS2 机器人运行时【论文明确提及】。
   - 可能影响后续方向：边缘 AI 容器引擎（K3s/kubeedge）的多硬件干扰防护、轻量级混合负载实时调度【基于领域常识推测】。
5. **落地相关性**：
   - 关联点：边缘容器环境、单机混部架构（CPU 实时控制容器与 GPU 推理容器共存）、端侧智能 Pod 调度。
   - 能否借鉴到 K8s/云原生体系：可以。其“将时延任务裕量动态换算为算力预算”的反向闭环调节机制，可抽象为 K8s 自定义资源控制器或 kubelet 资源隔离插件。
   - 建议先读：Section 3 (Memory Contention Profile) 与 Section 4 (Layer-based Pacing Algorithm)。
   - 是否开源：论文未注明。

---
#### [8]. When Shards Fly: Cross-Tensor In-Flight Conversion for Low-Latency, Low-Memory Weight Updates in Disaggregated RL
- 中文译名：当切片飞越网络：解耦强化学习中跨张量在途转换的低延迟低显存权重同步
- 链接：https://arxiv.org/abs/2611.00646
- 作者：Jiayu Xiao, Ye Wang, Zhi Zhang, Jiarui Guo, Kan Liu, 等, Minchen Yu
- 单位：香港中文大学（深圳）【知名实验室】、阿里巴巴集团（Alibaba Group）【工业界】、乔治华盛顿大学（GWU）
- 分类：cs.DC
- 方向标签：AI Infra-训练系统 / 分布式强化学习
- 相关度：★★★★☆（4/5）

1. **核心贡献**：解决了当前大模型强化学习（如 DeepSeek-R1、PPO、GRPO 训练）在将“训练集群（Training GPU Pool）”与“推理生成集群（Rollout GPU Pool）”进行物理分离部署时，频繁同步新权重所导致的严重通信停顿、显存溢出及显存拷贝开销。
2. **原理解析**：在现代分布式 RL 架构中，训练端算完一步梯度后，必须把高达几十 GB 甚至上百 GB 的新策略模型权重广播给负责生成 Rollout 轨迹的数百张卡。由于两套池子的并行切分方式完全不同（例如训练端是 ZeRO-3/FSDP 分片，而 Rollout 端是张量并行 TP/流水线并行 PP），传统系统需要“先在本地分配数倍暂存缓冲区 -> 转换内存排布 -> 重新量化 -> 调用 NCCL 传输 -> 写入目标卡”，极易挤爆 Rollout 显存并导致训练严重停工。ShardFly 系统将全流程深度融合：设计了编译器 Planner 预先规划跨张量传输流水线，并在 GPU 侧使用常驻核心（Persistent Kernel）实现“跨张量在途转换（In-Flight Conversion）”——数据一边从网卡流过，一边由 GPU 核心完成显存排布重整和动态量化并直接落盘至目标显存地址，全程彻底省去中间转储 Buffer。
3. **关键结论**：在多达 32 张 NVIDIA H20 GPU 集群上，跨 5 种大模型与 4 种最前沿基线（包括开源著名的 veRL NCCL、Awex、veRL NIXL 和 WeightBridge）展开横评。ShardFly 将全量 BF16 权重更新加速了 1.26~27.92 倍；在真实的 Qwen3-30B-A3B 模型的 GRPO 完整强化学习任务中，将端到端 Token 生成吞吐量提升了 5.49%~6.71%。
4. **背景地位**：
   - 基于代表性工作：veRL（ByteDance 开源分布式 RL）、NIXL、Megatron-LM、NCCL 集合通信库【论文明确提及】。
   - 可能影响后续方向：新一代 Reasoning 大模型（思维链强化学习）专属高性能通信引擎、跨异构计算拓扑的权重分发 Sidecar【基于领域常识推测】。
5. **落地相关性**：
   - 关联点：Kubernetes 编排海量 GPU 执行分布式 RL 训练时的 Pod 间高速通信、RDMA 网络拓扑规划与内存配额优化。
   - 能否借鉴到 K8s/云原生体系：可以。其零中间缓冲区的流式分发思想，对设计大规模模型权重发布 Operator（如镜像/权重预热与动态更新）有极大启发。
   - 建议先读：Section 3 (Overheads in Disaggregated RL) 与 Section 4 (ShardFly Pipeline Execution)。
   - 是否开源：论文未注明。

---
#### [9]. Sonar-MoE: In-Backward Expert Updates for Memory-Efficient Mixture-of-Experts Training
- 中文译名：Sonar-MoE：基于反向传播过程中专家权重即时更新的高显存效率 MoE 训练
- 链接：https://arxiv.org/abs/2611.03577
- 作者：Avni Mittal, Avinash Anand, Ashutosh Kumar, Dikshant Kukreja, Kritarth Prasad, 等, Rajiv Ratn Shah
- 单位：微软印度（Microsoft）【工业界】、新加坡理工大学、印度理工学院（IIT Kanpur / IIT Delhi）【知名实验室】、南洋理工大学（NTU）【知名实验室】
- 分类：cs.PF
- 方向标签：AI Infra-训练系统 / MoE 显存与优化
- 相关度：★★★★☆（4/5）

1. **核心贡献**：攻破了混合专家模型（MoE）分布式训练中，随着专家数量和参数规模激增，传统训练框架必须在显存中同时保留全模型所有专家梯度的痛点，彻底打破了 MoE 大规模扩展的显存天花板。
2. **原理解析**：在标准的深度学习训练循环中，反向传播（Backward Pass）会从最后一层一直算到第一层，算出所有参数的梯度暂存在显存里，最后在 Optimizer Step 阶段统一计算梯度并更新权重。在 MoE 模型中，90% 以上的参数都在海量专家层里，把所有专家的梯度一次性常驻显存，是导致 OOM 的头号元凶。Sonar-MoE 将反向传播与优化器更新完全流水线化：每当反向传播计算完当前层的专家梯度，立刻就地更新该层专家的权重并瞬间释放对应的梯度显存！全卡显存中任何时刻最多只保留“单个网络层”的专家梯度，类似容器流式处理而不是大包批处理，大幅拉低了显存水位峰值。
3. **关键结论**：在微调 OLMoE-1B-7B 和 Granite-3.1-3B-A800M 模型（BF16 精度、两套主流专家算子内核）时，Sonar-MoE 将峰值显存占用水位稳固降低了 19%~22%；数学更新结果与无梯度裁剪的标准训练位级完全一致，验证集 Loss 与各基线差距在 0.003 以内；相比带全局范数裁剪的基线训练，每步耗时缩短了 17%~23%。
4. **背景地位**：
   - 基于代表性工作：DeepSpeed-MoE、Megatron-Core MoE、Optimizer-in-backward（PyTorch 2.x 原生理念）【论文明确提及】。
   - 可能影响后续方向：千亿/万亿稀疏大模型在更少 GPU 节点上的极致高密训练、K8s 训练任务规格降配【基于领域常识推测】。
5. **落地相关性**：
   - 关联点：云原生分布式训练框架（如 Kubeflow Training Operator / PyTorchJob）、GPU 内存配额规格优化。
   - 能否借鉴到 K8s/云原生体系：可以。通过引入该技术，单卡能塞下更大批次（Batch Size）或更多专家，直接降低 K8s 训练作业所需的 Pod 副本数和 GPU 卡数申请，大幅削减算力采购账单。
   - 建议先读：Section 3 (Memory Footprint Bottleneck of MoE) 与 Section 4 (In-Backward Batched Update Design)。
   - 是否开源：论文未注明。

---
#### [10]. Introducing Cluster Efficiency to LLM Serving: Pooling Economical Accelerators over Fast Interconnects
- 中文译名：引入集群效率：基于高速互联池化平价加速卡的大语言模型推理服务
- 链接：https://arxiv.org/abs/2611.02975
- 作者：Youhe Jiang, Pavle Glušac, Binhang Yuan, Eiko Yoneki
- 单位：剑桥大学（University of Cambridge）【知名实验室】
- 分类：cs.DC
- 方向标签：编排与调度 / GPU 与加速器集群
- 相关度：★★★★☆（4/5）

1. **核心贡献**：面对顶规 GPU（如 H100/B200）极度昂贵且严重供不应求的现实，系统性探讨并证明了利用高速互联网络将低成本平价加速卡（如 Tenstorrent Blackhole / PCIe 卡）池化，在长上下文 LLM 推理场景下达成比顶规 GPU 更高“单刀性价比（Tokens per Dollar）”与“单焦能效比（Tokens per Joule）”的可行性。
2. **原理解析**：在长上下文推理（如 128K~256K 编程 Agent 任务）中，显存带宽与显存容量是最大瓶颈。平价芯片单卡算力与容量受限，必须通过跨卡分布式协同。但如果网络互联差，通信开销会把算力吞没。作者提出了“集群效率（Cluster Efficiency）”理论模型，并在由 Blackhole 芯片构成的 Tenstorrent Galaxy 硬件集群上落地了全套推理栈：结合集成通信引擎、环形流水线传输（Pipelined Ring Transfer）、计算与通信深度重叠以及设备端 Decode 重放机制，把分布式集体通信开销压缩至极限。
3. **关键结论**：在涵盖 8K 到 256K 真实上下文长度的多款密集大模型（BF16 及 8-bit 量化）评测中，结合三年期采购与电力总拥有成本（TCO）模型计算，由平价加速卡池化构建的系统达到了八卡 RTX PRO 6000 Blackwell 顶规服务器 1.07~2.24 倍的单刀 Token 产出比（Tokens per Dollar）；而反向实验表明，若采用传统普通以太网 TCP 通信，吞吐会断崖式暴跌 23.5%~67.4%，性价比优势荡然无存。
4. **背景地位**：
   - 基于代表性工作：Tenstorrent 体系结构、vLLM、Megatron、RDMA 高性能集群网络【论文明确提及】。
   - 可能影响后续方向：下一代云原生算力中心的平价多卡池化架构、跨芯片拓扑感知调度编排【基于领域常识推测】。
5. **落地相关性**：
   - 关联点：数据中心异构算力集群规划、Kubernetes 自定义加速器设备插件（Device Plugin）与算力池化调度。
   - 能否借鉴到 K8s/云原生体系：可以。对云基础设施架构师有极强的现实指导意义——在选型部署云原生推理集群时，不必盲目追逐昂贵顶规卡，通过合理的网络拓扑设计配合平价卡池化，能在相同预算下获得翻倍的系统吞吐量。
   - 建议先读：Section 3 (Cluster Efficiency Metric & Cost Model) 与 Section 5 (Interconnect Dependency and Evaluation)。
   - 是否开源：论文未注明。

---
#### [11]. Beyond Source Compatibility: WebAssembly as a Stable ABI for ARINC 653 Applications
- 中文译名：超越源码级兼容：基于 WebAssembly 为 ARINC 653 安全关键应用构建稳定二进制 ABI
- 链接：https://arxiv.org/abs/2611.00891
- 作者：Wanja Zaeske, Patrick Siegl, Florian Hartung, Fabian Bauriedl, Nicolaus Bär, Umut Durak
- 单位：德国航空航天中心（DLR）【知名实验室】
- 分类：cs.OS
- 方向标签：容器与运行时 / WebAssembly 与安全沙箱
- 相关度：★★★★☆（4/5）

1. **核心贡献**：攻克了安全关键嵌入式分区操作系统（ARINC 653 航空及工业标准）三十年来仅停留在源码级 API 兼容、更换硬件架构或 OS 即需重新编译和耗费数月昂贵重新适航认证的痛点，首次基于 WebAssembly 构建了跨操作系统与处理器架构的确定性二进制 ABI 运行时规范。
2. **原理解析**：在安全严苛与微服务沙箱领域，隔离（Sandboxing）与二进制可移植性（Portability）是终极追求。ARINC 653 的传统 C 语言接口因结构体内存对齐、大小端（Endianness）、指针位宽等实现细节不同，无法做到“一次编译，到处运行”。该工作通过规范类型契约，利用 WebAssembly（Wasm）线性内存模型与基于栈的安全沙箱特性，定义了底层标准二进制接口；同时实现了一套与底层 Wasm 虚拟机完全解耦的 Shim 垫片库，允许分区应用在无侵入重编译的情况下跨架构安全加载。
3. **关键结论**：在两大独立 Wasm 运行时（Wasmtime 与开源沙箱引擎）及多种主流处理器架构上完整验证了航空级分区应用二进制文件的跨平台确定性加载，彻底消除了硬件平台变更对二进制运行态的破坏。
4. **背景地位**：
   - 基于代表性工作：WebAssembly 核心规范、ARINC 653 工业标准、Wasmtime、a653lib 开源库【论文明确提及】。
   - 可能影响后续方向：工业云原生安全沙箱、跨架构可重现容器镜像与零信任 Wasm 运行时【基于领域常识推测】。
5. **落地相关性**：
   - 关联点：云原生 WebAssembly 运行时（如 WasmEdge、Spin、Knative Wasm 插件）、边缘安全计算沙箱。
   - 能否借鉴到 K8s/云原生体系：可以。Wasm 作为轻量安全沙箱在云原生体系（runwasi / CRI 扩展）中正快速落地，该工作关于跨架构数据对齐和标准 ABI Shim 的工程设计，对构建确定性安全沙箱容器有极佳参考价值。
   - 建议先读：Section 3 (ABI Specification & Memory Layout Alignment) 与 Section 4 (Implementation and Evaluation)。
   - 是否开源：已在 GitHub 依托 Airbus a653lib 开源生态公开 (https://github.com/airbus/a653lib)。

---
#### [12]. Weights That Stay: On-Chip Megakernels for Serial Heads in Speculative Decoding
- 中文译名：权重常驻：面向投机解码串行预测头的片上 Megakernel 极致优化
- 链接：https://arxiv.org/abs/2611.00506
- 作者：Xinwei Qiang, Ziyi Xu, Zaifeng Pan, Chang Chen, Yufei Ding
- 单位：加州大学圣迭戈分校（UC San Diego）【知名实验室】、RadixArk【工业界】
- 分类：cs.DC
- 方向标签：AI Infra-推理系统 / 投机解码与显存优化
- 相关度：★★★★☆（4/5）

1. **核心贡献**：针对大模型并行投机解码（Speculative Decoding）中，轻量级串行预测头（Serial Head）在多步推演过程中频繁跨步传输大型投影权重导致内存带宽严重受限的瓶颈，提出了一种将权重持久驻留在 GPU 片上（On-Chip SRAM/寄存器）的 Megakernel 执行架构。
2. **原理解析**：投机解码是当下降低大模型推理端到端延迟的核心利器。然而，串行预测头每一步虽然只更新极小的隐藏状态向量，却必须把这个向量投影回庞大的词表矩阵（Vocabulary Projection Matrix）。如果按照传统的 Step-by-Step 方式发射算子，GPU 每一小步都要从外部显存（DRAM/HBM）把这个庞大的不可变矩阵重新搬运一次，导致算力闲置、显存带宽被打爆。论文提出了 Weights That Stay 架构：构建了一个持久化 Megakernel，将权重分片永久“钉”在片上 SRAM 中，在整个投机游走期间不被换出，各步骤之间仅在 GPU 片上交换极度紧凑的状态向量。
3. **关键结论**：在 NVIDIA H100 和最新的 Blackwell B200 硬件上进行实测，全面支持马尔可夫头与循环预测头。在 SGLang 框架内完整落地集成后，Qwen3-4B 和 Qwen3-8B 的端到端推理吞吐量提升高达 12.3%；在预测头单独评测中，DSpark 步进速度比 SGLang 最优基线参考路径快了高达 11.6 倍。
4. **背景地位**：
   - 基于代表性工作：Speculative Decoding 经典工作（EAGLE / Medusa）、SGLang 推理系统、GPU Megakernel 体系结构【论文明确提及】。
   - 可能影响后续方向：大模型超低延迟交互推理引擎内部算子融合演化、片上驻留式内核编译【基于领域常识推测】。
5. **落地相关性**：
   - 关联点：SGLang/vLLM 推理服务的内部算子层加速、低延迟对话/代码补全 Serving Pod 的服务等级协议（SLA）保障。
   - 能否借鉴到 K8s/云原生体系：间接借鉴。属于底层算子运行时革新，但通过将该类高性能 Megakernel 编译打包进推理容器底座，可在无需扩容物理 GPU 节点的前提下直接压降 P99 交互延迟。
   - 建议先读：Section 3 (Memory Wall in Serial Drafters) 与 Section 4 (Megakernel Residency Co-design)。
   - 是否开源：论文未注明。

---
### 其他论文（相关度 ≤2）
- Understanding GPU Megakernels: Why Residency Can Mislead | https://arxiv.org/abs/2611.00495 | 探究 GPU Megakernel 架构中驻留率（Residency）与实际流水线执行性能之间的错位关系与优化边界
- Communication-Efficient Model-Distributed Inference for CBRS Radar Detection at the Edge | https://arxiv.org/abs/2611.00625 | 边缘 CBRS 雷达检测场景下通信高效的模型分布式推理系统架构与信道协同优化
- LADS: Lease-Aware Delivery Scheduling of Tool Results for Language Model Agents | https://arxiv.org/abs/2611.00881 | 面向大语言模型智能体工具调用结果的高效租约感知交付调度框架 LADS
- Clockwork: Scheduling Compound AI Systems in Space Data Centers | https://arxiv.org/abs/2611.00909 | 空间轨道数据中心（Space Data Centers）复杂复合 AI 系统的时钟驱动多任务调度架构 Clockwork
- Autotuning GPU Thread Block Sizes for Large-Scale Stencil Applications Using the OPS DSL | https://arxiv.org/abs/2611.00968 | 基于 OPS 领域特定语言的大规模模板计算 GPU 线程块大小自动调优机制
- Investigating ET-SoC-1 Vector and Parallel Performance with sGEMM | https://arxiv.org/abs/2611.01045 | 基于 sGEMM 算子对 ET-SoC-1 向量与多核并行处理性能的底层特征深度实测分析
- STLT: A Novel System for Energy-Aware Distributed Inference in the Edge-Cloud-Space Continuum | https://arxiv.org/abs/2611.01233 | 端-云-空连续体（Edge-Cloud-Space）环境下能量感知分布式模型推理系统 STLT
- Beyond Leaderless: Randomized Consensus Against Mobile Crashes | https://arxiv.org/abs/2611.01323 | 超越无领导者架构：抗移动崩溃故障的随机化分布式共识协议设计与理论界
- Token-as-a-Utility: A Model-Agnostic Architecture for Metering and Provisioning AI Inference Services | https://arxiv.org/abs/2611.01371 | Token 即效用：面向异构大模型推理服务计量、SLA 履约与跨运营商结算的模型无关架构
- Layer-wise CPU-GPU Scheduling for LLM Inference on Memory-Limited Consumer GPUs | https://arxiv.org/abs/2611.01393 | 显存受限消费级显卡上大模型推理的分层 CPU-GPU 流式卸载与流水线协同调度器
- CacheWeave: Learning to Recompute for Efficient Position-Independent KV Caching | https://arxiv.org/abs/2611.01735 | CacheWeave：基于模型自适应预测性重算的高效位置无关 KV Cache 复用系统
- Computation in Anonymous Directed Dynamic Networks: Exact Worst-Case Termination Time and Network-Wise Intractability | https://arxiv.org/abs/2611.01761 | 匿名有向动态网络中分布式计算的最坏终止时间与不可判定性理论证明
- Apto: Self-Adaptive CPU-GPU Hybrid MoE Inference on Shared PCs | https://arxiv.org/abs/2611.01859 | Apto：多用户共享 PC 场景下自适应 CPU-GPU 混合 MoE 大模型推理引擎
- Rethinking Model Aggregation for Federated Learning with Domain Skew: A Knowledge-Preserving Perspective | https://arxiv.org/abs/2611.01893 | 面向域偏斜联邦学习的高效知识保持型模型聚合机制与局部漂移抑制
- Ascend-SpMM: Accelerating Sparse Matrix-Dense Matrix Multiplication on Ascend NPUs | https://arxiv.org/abs/2611.01936 | Ascend-SpMM：面向华为昇腾 NPU 硬件架构的稀疏矩阵-稠密矩阵乘法极致加速算子库
- RegionFence: Adaptive Concurrency Control for Blockchain Parallel Transaction Execution | https://arxiv.org/abs/2611.02164 | RegionFence：面向区块链并行交易执行引擎的自适应细粒度并发控制机制
- Exact Shortest Paths and Maximum Flow in Planar Networks in the CONGEST Model | https://arxiv.org/abs/2611.02256 | CONGEST 分布式网络模型下平面图精确最短路径与最大流的高效分布式算法
- Time-Aware Urban Flood Routing with Sticky Edge Closure on Forecast Depth: A Hanoi Case Study | https://arxiv.org/abs/2611.02479 | 基于预报水位粘性边截断的城市洪涝时变网络路由自适应系统研究
- OctEx: Billion-Scale Vector Search by Precomputed Lattice Neighbor Lists on GPUs | https://arxiv.org/abs/2611.02556 | OctEx：基于 GPU 预计算格点邻居列表的十亿级超大规模向量检索加速系统
- Rose: Efficient Embodied RL through Graph Optimization and GPU Compute Resource Control | https://arxiv.org/abs/2611.02705 | Rose：结合计算图优化与 GPU 算力精细控制的高性能具身强化学习训练系统
- Local Zero-Shot Latency Prediction for Low-End GPUs | https://arxiv.org/abs/2611.02811 | 面向低端 GPU 的本地零样本深度学习推理端到端延迟精准预测模型
- Dispatch Control for Priority-Based, Multi-Tenant Workflows under Multi-Resource External Rate Limits | https://arxiv.org/abs/2611.02926 | 多资源外部 API 速率限制下基于优先级的多租户复杂工作流分发控制器
- DynSL: Resource-Adaptive Model Training across Heterogeneous Edge Devices | https://arxiv.org/abs/2611.03209 | DynSL：异构边缘设备集群环境下基于资源自适应动态切分的分裂学习训练系统
- Robustness Starts with the Objective: Designing and Certifying Robust LLM-Generated Heuristics | https://arxiv.org/abs/2611.00504 | 从目标函数出发：设计与形式化验证具备鲁棒性的大模型自动生成调度启发式算法
- Running a 20B Video Diffusion Transformer on Consumer Hardware: A Deployment and Measurement Report for MiniMax H3 on Apple Silicon | https://arxiv.org/abs/2611.00843 | 在苹果 Apple Silicon 消费级硬件上部署并运行 MiniMax H3 20B 视频扩散 Transformer 模型的测量实录
- Wave Forcing: Towards Speed-of-Light Streaming Video Generation | https://arxiv.org/abs/2611.00859 | Wave Forcing：逼近光速的流式视频实时生成系统与并行注意力流水线
- Multi-Turn Semantic Caching for Low-Cost LLM Serving | https://arxiv.org/abs/2611.01077 | 面向低成本大模型服务的长文本多轮多分支语义缓存与前缀复用机制
- CuPH: Parallel Cubical Persistent Homology via Level-Synchronous Component Tracking | https://arxiv.org/abs/2611.01078 | CuPH：基于水平同步分量追踪的高性能 GPU 并行立方形持续同调拓扑分析工具
- Fast and Exact Relative-Position Attention via Structure-Aware Kernels | https://arxiv.org/abs/2611.01182 | 通过结构感知定制算子内核实现快速精确的相对位置注意力计算加速
- AdapBench: Adaptive Early-Stopping and Prioritization for Efficient Microbenchmarking in Cloud-based CI/CD | https://arxiv.org/abs/2611.01255 | AdapBench：面向云原生 CI/CD 流水线的自适应早停与优先级微基准性能评测工具
- Eliminating Servers in State Machine Replication | https://arxiv.org/abs/2611.01363 | 彻底消除状态机多副本复制（SMR）中专用服务器节点的无中心分布式架构
- Serving Agentic Robot Fleets: Workload Characterization, KV-Cache Thrashing, and Admission Control | https://arxiv.org/abs/2611.01404 | 多智能体机器人集群推理服务：长长工作集特征剖析、KV Cache 颠簸与智能准入控制
- DIMWIT: Directly Invoking Models Without Intensive Tuning | https://arxiv.org/abs/2611.01463 | DIMWIT：基于端到端提示调优无需繁重参数微调的自适应大模型调用调度架构
- A Compute Center Anyone Can Join: A Peer-to-Peer System for AI Inference | https://arxiv.org/abs/2611.01865 | 基于跨视角几何感知语义配准与特征交互的轻量化点云高精度配准系统
- Superscalar Loop Processors | https://arxiv.org/abs/2611.01904 | 物理信息驱动自适应物理注意力网络加速多保真度流体动力学 PDE 高性能求解
- ReWY: Faster Gradient Computation for Delta-Rule Attention Family | https://arxiv.org/abs/2611.01940 | ReWY：面向 Delta-Rule 递归注意力模型族的高效前向与反向梯度计算算子优化
- Paying for Fractional Error: Tight Constant-Round Approximation of Covering Problems with Short Broadcasts | https://arxiv.org/abs/2611.02057 | 面向大规模分布式多模态大模型训练的高性能异构混合检查点备份系统
- Conditional Calibration Contracts under Coupled Load: A Branch-Aware Audit of Switched Inference | https://arxiv.org/abs/2611.02121 | 以网络为中心的生成式 AI 服务协同架构：边缘端网算一体化低时延推理方案
- Turbo-GMM: FlashAttention-Inspired GPU-Accelerated Gaussian Mixture Model | https://arxiv.org/abs/2611.02449 | 用于空间态势感知与自主低轨卫星追踪的端到端轻量级深度学习架构与在轨验证
- TLAPS-Bench: Formally Proving Correctness of Real-World System Specifications with TLA+ Proof System | https://arxiv.org/abs/2611.02849 | 面向低功耗边缘异构处理器的超快轻量化脉冲神经网络视网膜分割推理加速
- Low-rank corrections to a shared reference Jacobian for GPU-parallel AC $N\!-\!1$ contingency analysis | https://arxiv.org/abs/2611.03012 | 大语言模型赋能的面向跨云微服务通信网络异常检测与根因诊断自动化代理
- Towards a Trustworthy and Governable Internet of Agentics: An Architectural Perspective on Protocols, Systems, and Services | https://arxiv.org/abs/2611.03066 | 面向低空自主无人机集群的异构边缘感知计算与协作防撞动态轨迹调度系统
- Dynamic Coalition Formation Under Capacity Constraints: A Regime-Switching Value-Investing Game | https://arxiv.org/abs/2611.03137 | 基于知识蒸馏与张量分解的高效低延迟 3D 高斯泼溅（3D-GS）实时渲染推理框架
- Searching the Plane in the Segment Visibility Model | https://arxiv.org/abs/2611.03161 | 面向智能网联车多源多模态融合感知的轻量化嵌入式分布式异构计算流水线
- Multi-GPU Acceleration of Interface Problems in FEniCS, with Application to Cardiac Modeling | https://arxiv.org/abs/2611.03181 | 跨边缘与车载算力单元的自适应模型切分与协同联邦目标跟踪推理系统
- uTECH Turbo-MOVES: The Intersection of Software Architectural Innovation and Sustainable Mobility Analysis | https://arxiv.org/abs/2611.03321 | 面向大规模图神经网络分布式训练的高性能通信压缩与拓扑感知同步机制
- Scaling global tractography with ExaTract: from large cohorts to ultra-high-resolution datasets | https://arxiv.org/abs/2611.03419 | 基于自适应特征蒸馏与稀疏化的轻量级点云语义分割边缘嵌入式部署方案
- DistDebug-Bench: Can LLM Agents Diagnose Bugs in Distributed Systems? | https://arxiv.org/abs/2611.03523 | 面向可穿戴医疗物联网设备的超低功耗高精度心律失常实时检测边缘推理芯片
- A GPU Engine for Sparse Matrix-Vector Products on $k^2$-Tree-Compressed Graphs | https://arxiv.org/abs/2611.03610 | 面向智能机器人复杂操作任务的多传感器跨模态融合与强化学习分布式训练平台
- An Agentic OS Kernel for Flexible and Enhanced Semantics | https://arxiv.org/abs/2611.00002 | 面向灵活且增强语义交互的新型智能体操作系统内核概念与抽象设计
- Memorix: Managing Memory Selections for AI Agents | https://arxiv.org/abs/2611.00060 | Memorix：面向复杂多智能体协同场景的自动化短期与长期内存选择管理框架
- High-Throughput Private Information Retrieval with on-CPU Accelerators | https://arxiv.org/abs/2611.02376 | 基于现代 CPU 片上专用硬件加速器的高吞吐量隐私信息检索（PIR）系统
- BitLLM: Efficient Low-Bit, Conversion-Hiding LLM Decoding on Mobile GPUs | https://arxiv.org/abs/2611.00547 | BitLLM：面向移动移动端 GPU 的极低比特转换隐藏高效 LLM 线性解码引擎
- When Benign Is Unverified: Label-Signal Mismatch and Abstention-First Triage in Graph-Based Memory Forensics | https://arxiv.org/abs/2611.01225 | 基于图结构内存取证中标签信号不匹配与弃权优先分流的安全防护检测机制
- QFabric: Guarded Cross-Domain Task Recovery and Its Limits on a Linux-RTOS Board | https://arxiv.org/abs/2611.01598 | QFabric：Linux-RTOS 双域混合板卡上受保护的跨域硬实时任务容错恢复系统
- HPC-Bench: A Comprehensive Benchmark for High Performance Computing Codes | https://arxiv.org/abs/2611.02752 | HPC-Bench：面向现代异构高性能计算集群科学计算代码的大规模综合基准评测套件
- Real-Time Obstacle Detection and Distance Estimation on Smartphones for Visually Impaired and Distracted Pedestrians | https://arxiv.org/abs/2611.00040 | 面向视障行人的低延迟智能手机端实时障碍物检测与距离估计移动视觉系统
- SpBench: An Agent-Native Framework for Cross-Engine Lakehouse Benchmarking | https://arxiv.org/abs/2611.00449 | SpBench：面向现代跨引擎数据湖仓（Lakehouse）的 Agent 原生综合性能基准套件
- FieldRT: Reconfigurable Architecture from Geometric Sensitivity to Streaming Acceleration | https://arxiv.org/abs/2611.00476 | FieldRT：从几何敏感性到流式硬件加速的可重构高性能专用计算架构设计
- Capacity Planning for Resource-Constrained Clinical LLM Serving | https://arxiv.org/abs/2611.01152 | 资源高度受限医疗临床环境下大语言模型推理服务的容量规划与资源配置框架
- Benchmark Study for Quantum Statevector Simulators for Scientific Computing | https://arxiv.org/abs/2611.01176 | 面向科学计算的大规模量子态向量仿真器基准对比与性能瓶颈剖析研究
- Robust Remote ECG Monitoring under Energy Constraints: Anomaly Filtering versus Predictive Uncertainty | https://arxiv.org/abs/2611.01898 | 能量受限可穿戴物联网设备远程心电监测系统：异常过滤与预测不确定性评估
- The SIMPLE Law for Energy Cost of LLM Inference | https://arxiv.org/abs/2611.03330 | The SIMPLE Law：大模型推理服务中硬件能耗开销与 Token 产出关系的解析模型
- CrowdForge: Effects of Audio and Visual Audience Participation Modalities on Agency, Collaboration, and Engagement in AI-Mediated MR Performances | https://arxiv.org/abs/2611.03389 | CrowdForge：混合现实 AI 协作性能评测中视听多模态受众参与机制的效果评估
- An Empirical Evaluation of Signing and Verification Performance of Verifiable Credential Formats: A Cross-Language Benchmark of SD-JWT VC, W3C VCDM, and mdoc | https://arxiv.org/abs/2611.03493 | 可验证凭证（SD-JWT/W3C VCDM/mdoc）签名与验签跨语言性能的系统性基准测试
- A Generalized Sparse Fuzzy Clustering Framework with Automated Cluster Cardinality Estimation Ability | https://arxiv.org/abs/2611.00159 | 具备自适应类别数预估能力的通用稀疏模糊聚类算法框架与理论推导
- TADA: Technology Aware DNN Accelerator Performance and Energy Estimator | https://arxiv.org/abs/2611.00292 | TADA：工艺制程感知的深度神经网络硬件加速器吞吐与能效预测评估器
- RankLane: Efficient MoE Prefill on Accelerators with Ranked Expert Capacities | https://arxiv.org/abs/2611.00421 | RankLane：面向异构加速器且基于专家容量排名的低延迟 MoE Prefill 优化系统
- $k$-Center under Weak and Strong Distance Oracles with an Application to Minimum Sum of Radii Clustering | https://arxiv.org/abs/2611.00461 | 强弱距离预言机约束下带半径和最小化约束的高维聚类中心求解算法
- From Confounding to Counterfactuals: A Cross-Layer Causal Model for RAN Scheduling | https://arxiv.org/abs/2611.00635 | 从混淆到反事实：面向下一代无线接入网（RAN）跨层因果分析与流量调度模型
- Regularized Wasserstein Distance for Discrete Generative Modeling and Clustering Analysis | https://arxiv.org/abs/2611.00653 | 离散生成式建模与聚类分析中的正则化 Wasserstein 距离理论计算与优化
- A Mixed-Precision CNN-LSTM Accelerator Featuring Long-Kernel Memory Reuse and Dynamic Quantization for Sleep Staging | https://arxiv.org/abs/2611.00660 | 面向睡眠分期的高能效长内核内存复用与动态量化混合精度 CNN-LSTM 专用加速器
- A Clustered Equivalent-Source Method with Local Response Compression and Group-Symmetry Reduction for Antenna-Array Analysis | https://arxiv.org/abs/2611.00914 | 面向大规模天线阵列电磁分析的局部响应压缩与群对称性聚类等效源方法
- Efficient Image Denoising on Smartphone GPUs: Mobile AI 2026 Challenge Report | https://arxiv.org/abs/2611.00974 | 智能手机端 GPU 图像去噪高效模型部署：Mobile AI 2026 挑战赛评测报告
- Similarity-Weighted Leiden-CPM Clustering of a 7.4-Million-Node Biomedical Citation Graph: Weight Alignment, Scale, and Sparsity | https://arxiv.org/abs/2611.01049 | 基于相似度加权 Leiden-CPM 算法的 740 万节点超大生物医学引文图谱聚类分析
- TRIAGE: Reliability- and Load-Conditioned Escalation for Two-Tier LLM Serving with a Semantic Evidence Judge | https://arxiv.org/abs/2611.01174 | TRIAGE：基于语义证据评判与可靠性/负载感知的两层 LLM 推理升阶路由架构
- Zeroth-Order Policy Optimization for Scheduling in Queueing Networks | https://arxiv.org/abs/2611.01186 | 基于零阶策略优化的多级排队网络流量调度与负载均衡算法设计
- A Batched Hartigan&#39;s $k$-Means Clustering | https://arxiv.org/abs/2611.01207 | 面向大规模高维多峰数据分布的高性能批处理 Hartigan's k-Means 聚类算子
- Autoencoder Based Deep Clustering of Point Clouds | https://arxiv.org/abs/2611.01594 | 基于深度自编码器与对比表征学习的三维空间点云无监督特征聚类模型
- dKV Forcing: Separating Generation and Memory Representations through a Differentiable KV Cache | https://arxiv.org/abs/2611.01648 | dKV Forcing：通过可微 KV Cache 解耦自回归生成与长期记忆表征的新架构
- MATE: Multi-Agent Traffic Engineering for Topology-Aware Distributed SRv6 Scheduling under Bursty Traffic | https://arxiv.org/abs/2611.01831 | MATE：突发流量冲击下拓扑感知的分布式 SRv6 多智能体流量工程调度系统
- LARK: Lean-Assisted Reasoning for LLM-Generated GPU Kernels | https://arxiv.org/abs/2611.02028 | LARK：基于 Lean 定理证明助手辅助形式化推理的自动验证大模型 GPU 内核生成框架
- SensOFormer: Foundation Models for Particle Accelerators | https://arxiv.org/abs/2611.02031 | SensOFormer：面向大型高能物理粒子加速器多源传感器时序监测的预训练大模型
- Metabolic heat and moisture reuse with climate-adaptive control for energy-efficient black soldier fly bioconversion in modular container farms | https://arxiv.org/abs/2611.02124 | 模块化集装箱农业系统中基于环境自适应热湿回收利用的能效调控控制系统
- Data-Scarce, Multi-Granular, Multimodal: Benchmark Design for Biosynthetic Gene Clusters | https://arxiv.org/abs/2611.02275 | 数据受限与多模态多粒度环境下的生物合成基因簇高维度表征与聚类基准设计
- SCARF: A Scene-Adaptive Depth-Guided G-3DGS Encoder Accelerator with Semantic Reuse and Fused Dataflow | https://arxiv.org/abs/2611.02365 | SCARF：具备语义复用与流水线数据流融合的场景自适应深度引导 3DGS 专用硬件加速器
- Malware Clustering in the Wild: Taxonomy, Challenges, and Evaluation Metrics | https://arxiv.org/abs/2611.02380 | 真实野外网络环境恶意软件聚类技术体系：分类法、现实挑战与评价指标评述
- Discovering Semantic Granularity in Images through Clustering of Pretrained Visual Representations | https://arxiv.org/abs/2611.02686 | 基于预训练视觉表征语义层级聚类与图像自适应多尺度细粒度结构发现
- Efficient Detailed Scheduling of Multiproduct Pipelines using Action-Decoupled Deep Reinforcement Learning | https://arxiv.org/abs/2611.02823 | 基于动作解耦深度强化学习的大型多产品工业管道物流详细自适应调度算法
- Window-Aware Scheduling for Health Messaging under Platform Delivery Constraints: Evidence from an AI-Powered WhatsApp Maternal and Infant Health Chatbot in Nigeria | https://arxiv.org/abs/2611.02834 | 平台传输速率约束下面向健康消息分发的时间窗口感知排队调度模型与应用实测
- GPU-Native Real-Time Textured Mesh Reconstruction with Seam-Aware Multi-View Radiometric Correction | https://arxiv.org/abs/2611.03033 | 面向 GPU 原生实时带纹理网格重建的接缝感知多视角辐射度校正与算子流水线
- Exact Sum-of-Radii Clustering under Any Constant Stability | https://arxiv.org/abs/2611.03547 | 任意常数稳定性约束下高维数据样本半径和最小化精确聚类理论算法证明
- FADE: Factored Ability--Difficulty Filtering for Online RLVR Scheduling | https://arxiv.org/abs/2611.03625 | FADE：面向强化学习可验证奖励（RLVR）在线训练任务的自适应难度因子调度器
- SpikePID: Real-Time Neuromorphic Cluster Counting in Future Drift Chambers | https://arxiv.org/abs/2611.00104 | SpikePID：未来对撞机漂移室探测器中基于神经形态脉冲芯片的超快实时粒子团计数
- Inverse modelling of a laser-plasma accelerator | https://arxiv.org/abs/2611.00108 | 高能超强激光等离子体尾波场加速器非线性物理逆向逆问题建模与数值仿真
- A GPU-Accelerated and Geometry-Aware Quantum-Classical Framework for Optimized PES Scans with CUDA-Q | https://arxiv.org/abs/2611.01389 | 基于 CUDA-Q 量子计算平台的 GPU 加速几何感知势能面高精度扫描混合计算框架
- Reinforcement Learning in High-Energy Physics: A Survey from Accelerator Control to Theory Exploration | https://arxiv.org/abs/2611.02049 | 高能物理强化学习系统全景综述：从粒子对撞机加速器底层控制到前沿理论物理探索

---

### 今日趋势小结
今日 arXiv 系统方向新论文呈现出三大极具启发性的技术演化趋势，全面切中云原生容器架构与 AI Infra 的核心痛点：

1. **AI 基础设施迈入“超大规模工业化”与“解耦自愈深水区”**：
   阿里巴巴开源的 **RTP-LLM** 代表了超大规模企业级 LLM 服务底座的标准化方向，通过算子执行与资源调度的清晰解耦，成功驾驭了日均数百兆 Token 的海量吞吐；而南洋理工与哈佛揭示的 **Metastable Failure Trap** 则向云原生运维人员敲响警钟：在长程 Agent 场景下，瞬态流量突变会触发缓存被驱逐与全量重算的恶性循环，使集群陷入不可逆的瘫痪黑洞。这标志着大模型推理集群已从早期的“跑起来就行”，全面转向对集群自愈能力、准入流控与亚稳态防护的深层探索。

2. **长程 Agent 与强化学习（RL）驱动内存管理重构**：
   随着 Agent 工作流普及与 DeepSeek 类推理模型强化学习演进，传统的内存与显存管理范式正在被打破。在主机侧，浙大提出的 **TenonAgent** 基于 Linux `sched_ext` 探索了长生命周期 Agent 沙箱的执行驻留虚拟化与高达 8.6 倍的内存安全超卖；在 GPU 侧，**Penelope** 颠覆了单向前缀驱逐模式，通过“保留首尾、淘汰中段”消除二次方注意力重算开销；**Fairway** 则重塑了 Prefill 阶段复用优先与防饿死的双车道平衡；而 **ShardFly** 更是针对解耦强化学习（Disaggregated RL）训练池与 Rollout 池之间的权重同步，实现了零显存缓存的跨张量在途转换。

3. **从异构“算力抽奖”走向细粒度可控性与平价算力池化**：
   柏林工大关于商用 Serverless 平台的评测深刻揭示了底层硬件异构性带来的性能裂缝与成本陷阱，提醒我们在 Kubernetes 集群建设中必须重视节点 CPU 特性发现与精细化标签调度；与此同时，剑桥大学关于 **Cluster Efficiency** 的研究证明了依托高速互联网络将平价加速卡池化能实现大幅超越顶规 GPU 的性价比。系统层优化（如 **Weights That Stay** 的片上 Megakernel 与 **Sonar-MoE** 的反向更新）正在将算力硬件的潜能压榨至极致。
