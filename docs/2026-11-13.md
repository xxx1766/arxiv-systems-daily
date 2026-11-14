## arXiv 系统方向日报 · 2026-11-13

### 今日概览

今日系统方向（cs.DC / cs.OS / cs.PF 及相关交叉领域）共抓取 68 篇候选论文。经过资深系统文献调研体系的严格筛选与多维度评分，本次**入选深读：12 篇**（其中 6 篇评分为 5 分的核心突破论文，6 篇评分为 4.5 分的高价值系统论文），其余 56 篇理论、算法或边缘交叉论文归入文末列表。

今日文献呈现出极为鲜明的「**AI Infra 纵深重构：从单卡微架构切片、无 HBM 数据中心到云原生沙箱与长尾编排**」技术演进主线：
在单卡与芯片微架构层面，英伟达官方团队基于最新 Blackwell B200 提出 SubGPU 空间流水线切分，打破算子串行发射对 SM 与显存带宽的浪费；AMD 研究院官方团队针对 MI300X/MI355X 芯粒（Chiplet）物理拓扑重构大模型分片，直击盲目切分造成的算力坍塌；而在数据中心级系统架构上，瑞典乌普萨拉大学提出了面向 8 万卡规模的 OBM 光广播共享内存，颠覆了每张 GPU 独立复制几百 GB 静态权重的传统范式，彻底摆脱推理节点对昂贵 HBM 的容量绑架。
在训练与推理执行引擎层面，清华大学与生数科技提出 SS-HSDP，在 128 卡规模下解耦计算排布与 Muon 等矩阵优化器更新，MFU 提升高达 21.7%；SGLang 社区迎来 Parallel Prompting，对同文档批量问答实现多流并发解码与 KV Cache 单次读取，吞吐暴增 3.7~6 倍；阿里巴巴团队攻克工作站级 Blackwell（SM120）上的 MoE 通信与计算重叠难题。
在容器运行时、智能体沙箱与集群编排层面，韩国科学技术院（KAIST）与 SK 海力士推出 Cairn，揭示 Serverless 大模型冷启动仅 5%~11% 用于权重加载，通过跨节点 CXL 共享池与 Zygote 预热容器将冷启动缩减 5.2 倍；蚂蚁集团 Ling 团队提出 CAAS 关键链路调度器，化解智能体在沙箱环境中交替推理与执行带来的长尾 Makespan 危机；上海交大与阶跃星辰联合打造 Apple Silicon 上的 Metal Sandbox 命令级窃取调度器；高丽大学系统评估了静态图 NPU 在智能体过载时 89.5% 算力沦为冗余 Prefill 的痛点并构建 Host-Tier 恢复机制；纽卡斯尔大学则破解了 Java 21 虚拟线程 $M:N$ 调度导致云原生 eBPF 追踪错乱的隐蔽顽疾。

今日必读：
1. **Cairn**: KAIST 与 SK 海力士揭示 Serverless 大模型冷启动仅 5%~11% 用于权重加载，首创跨节点 CXL 共享内存池与 Zygote 预热容器，冷启动时间缩减高达 5.2 倍。
2. **SubGPU Pipelining**: 英伟达官方团队面向 Blackwell B200 提出 GPU 内细粒度空间流水线并行，以 CUDA Green Contexts 划分 SM 池重叠短算子，访存带宽利用率提升至 83.6%。
3. **Starscream**: AMD 研究院针对 MI300X/MI355X 芯粒架构重构大模型分片，打破传统粗粒度切分造成的算力坍塌，自注意力算子取得最高 4 倍加速。
4. **SS-HSDP**: 清华大学与生数科技提出计算与优化器更新解耦的混合分片数据并行，以共享视图消灭冗余数据搬运，128 卡 MFU 提升高达 21.7%。
5. **OBM (Optical Broadcast Memory)**: 乌普萨拉大学提出面向 8 万卡数据中心的广播式光共享内存架构，颠覆每卡复制大模型权重的传统范式，彻底摆脱推理节点昂贵 HBM 束缚。
6. **Recompute vs Restore**: 高丽大学针对 Rebellions ATOM+ 静态图 NPU 揭示过载下 89.5% 算力沦为冗余 Prefill，构建 Host-Tier KV 桥接器将智能体工作流 SLO 达成率从 9.4% 挽救至 99.8%。
7. **Ling Makespan Coordination**: 蚂蚁集团针对智能体评测与 RL 批处理长尾瓶颈，提出推理-沙箱环境协同与 CAAS 关键链路推进调度，Makespan 显著降低 10.4%~65.0%。
8. **Parallel Prompting**: 加州大学圣克鲁兹分校提出单请求多流并发解码机制，针对同文档批量问答仅需单次读取 KV Cache，在 SGLang 生产引擎上实现最高 6 倍吞吐加速。
9. **GC-MoE on SM120**: 阿里巴巴底层团队攻克消费级/工作站 Blackwell（RTX PRO 5000）上的 MoE 通信与计算重叠难题，融合 FP8xFP4 块缩放 MMA 算子取得 1.52 倍加速。
10. **Metal Sandbox**: 上海交大与阶跃星辰推出面向 Apple Silicon 的 GPU 代码智能体隔离沙箱与跨节点命令调度系统，动态任务迁移缩减 22.3% 批处理时间。
11. **Tideway**: 杜克大学提出面向消费级 MoE 推理的阶段感知分层统一内存管理，动态自适应 Prefill 与 Decode 访存特征，端到端延迟降低 1.97 倍、TTFT 加速 2.4 倍。
12. **Virtual Threads eBPF Tracing**: 纽卡斯尔大学破解 Java 21 虚拟线程 $M:N$ 调度导致 eBPF 上下文错乱的顽疾，在 OpenJDK 内以 33ns 极低开销实现微秒级全生命周期精准追踪。

---

### 逐篇解读

#### 1. Fast Serverless LLM Cold Starts by Sharing and Prewarming Startup Work
- 中文译名：通过共享与预热启动任务加速无服务器大语言模型冷启动
- 链接：https://arxiv.org/abs/2611.16180
- 作者：Hongjin Kim, Igjae Kim, Kwanghoon Choi, Minho Ha, Jaehyuk Huh
- 单位：韩国科学技术院 (KAIST) 【知名实验室】、SK 海力士 (SK hynix) 【工业界】
- 分类：cs.DC
- 方向标签：A. 容器与运行时 (Serverless/FaaS 冷启动、Zygote 容器预热、CXL 共享池) & C. AI Infra (LLM 运行时初始化、模型权重分发、KV 显存预估)
- 相关度：5/5

1. 核心贡献：
深入解剖了 Serverless LLM 服务按需冷启动（Cold Start）耗时近 1 分钟的底层执行分解，首次揭示了一个反常识的系统真相：**整个冷启动过程中仅有 5%~11% 的时间真正花费在从存储向 GPU 搬运模型权重上！** 其余近 90% 的漫长时间被模型编译、GPU 显存 Profiling（为 KV Cache 探测尺寸）、运行时环境搭建、Python 依赖栈导入以及 CUDA 上下文初始化所霸占。为此，KAIST 与 SK 海力士团队设计了无服务器推理系统 **Cairn**，首次将冷启动任务分类为「模型无关的预热任务」与「跨节点可共享的模型专属任务」，依托机架级 CXL 共享内存池与 Zygote 模板进程，使冷启动耗时缩短高达 4.1~5.2 倍。

2. 原理解析：
这就像在 Kubernetes 集群中启动一个配置极重的 AI 业务 Pod：
- **冷启动的真实瓶颈**：以往大家以为冷启动慢是因为容器镜像太大（拉取镜像慢，即类似权重加载），于是疯狂做镜像轻量化。但 Cairn 发现，即使镜像秒级拉齐，容器内部的 `entrypoint` 启动时还在盲目执行大量重复而确定的自检工作：每个节点各自在 Python 里 `import torch`、各自跑一遍 CUDA Graph 内存探测、各自将计算图编译一遍，造成巨大算力与时间浪费；
- **任务三分类与 Zygote 预热**：Cairn 将工作解构为三层：
  1) **Prewarmable（可预热任务）**：与模型完全无关，如 Python 解释器初始化、PyTorch/vLLM 库导入、CUDA Context 建立。系统像 Android 系统的 Zygote 机制一样，在每个节点维护一个通用的「预热容器基座」，当新模型请求到来时，直接通过 `fork` 衍生 Worker 进程，彻底消灭进程启动与基础库加载开销；
  2) **Shareable（跨节点可共享任务）**：与模型强相关但在同构 GPU 集群中输出完全一致，包括权重反序列化结构、编译缓存（Compile Cache）、编译器 Keys 以及 CUDA-Graph 显存估算结果。Cairn 利用底层 CXL 共享内存池（CXL Memory Pool），首个启动该模型的节点将这些产物写入 CXL 池作为不可变词条，后续集群内任意节点需要拉起该模型时，直接通过 DMA 就地读取，无需重新编译与探测；
  3) **Process-bound（进程绑定状态）**：仅剩捕获 CUDA Graph 等极少数必须在本地进程内完成的轻量动作。

3. 关键结论：
在基于 ServerlessLLM 与 vLLM v0.20 搭建的跨节点 CXL 共享内存环境中，针对 1B 至 14B 参数量的 6 个主流模型评测：
- Cairn 将端到端冷启动延迟从基线的 57~85 秒急剧削减至 **11.0~21.0 秒**，实现 **4.1~5.2 倍的断崖式加速**；
- 在完全没有预存 Checkpoint 的全新冷节点上，直接读取 CXL 共享产物即可瞬间上线；
- 在长达 1 小时的 Azure Functions 真实生产负载追踪回放下，首字时延（TTFT）中位数从 32.5 秒降低至 **11.8 秒（降幅达 64%）**；
- 在 16 节点的集群模拟中，当并发压力达到 3.2 req/s 时，因冷启动超时的失败率从 15.6% 直降到 2.1%。

4. 背景地位：
来自顶尖体系结构实验室 KAIST 与全球存储半导体巨头 SK 海力士的联合成果。这是首个将 CXL 硬件池化内存与容器运行时 Zygote 范式深度整合、直击 Serverless 大模型冷启动内部 Profiling 与编译瓶颈的系统工作，指明了云原生 FaaS 与 AI Infra 结合的硬件落地路径。

5. 落地相关性：
对于在 Kubernetes 上维护 Knative、KEDA、Ray 或基于 GPU 的 FaaS 平台的系统工程师具有巨大的实践指导价值。以往工程师面对几十秒的冷启动束手无策，Cairn 证明了通过进程预热池（Prewarmed Pod Pool）预先导入 Python/CUDA 运行库，并将模型编译产物与显存大小预估结果抽取为集群级共享卷（Shared Volume / NFS / CXL），即可在极小代价下消除 80% 以上的冷启动等待。

---

#### 2. SubGPU Pipelining: Intra-GPU Fine-Grained Spatial Parallelism for LLM Inference
- 中文译名：SubGPU 流水线：面向大语言模型推理的 GPU 内细粒度空间并行机制
- 链接：https://arxiv.org/abs/2611.14904
- 作者：Muralidhar Andoorveedu, Marius Juston, Tingkai Liu, Sanjay Patel
- 单位：英伟达 (NVIDIA) 【工业界】
- 分类：cs.DC
- 方向标签：C. AI Infra (LLM 解码推理、单卡空间流水线并行、CUDA Green Contexts、Blackwell B200 硬件饱和度、微批次调度)
- 相关度：5/5

1. 核心贡献：
英伟达架构与系统核心团队针对大语言模型在下一代旗舰硬件（如 NVIDIA Blackwell B200）上解码时的严重资源浪费问题，提出了全新的芯片内执行范式——**SubGPU Pipelining（SubGPU 流水线）**。针对 Decoding 阶段算子执行时间短（仅数十微秒）、受访存带宽制约严重且呈现突发性（Bursty）波动的特征，该工作彻底打破了单张 GPU 内各算子按时间顺序串行执行（Temporal Execution）的传统模式，将 Transformer 层的算子图切分成有序连续片段，分配给基于 **CUDA Green Contexts** 划分的互斥流式多处理器（SM）池，通过微批次（Microbatch）在 GPU 芯片内部流转实现细粒度空间流水线，在真实 Blackwell B200 硅片上使 DRAM 吞吐从 71.8% 提升至 83.6% 峰值，单层迭代耗时降低 10.33%。

2. 原理解析：
这就像在单个大型物理节点内从传统的「独占批处理调度」进化为「精细化的容器 cgroup / CPU Pinning 流水线」：
- **微架构困境**：像 Blackwell B200 这样拥有海量 SM 和超高 HBM3e 带宽的怪兽级芯片，运行 70B/120B 大模型的单步解码算子时，一个算子几十微秒就跑完了。频繁的 Kernel Launch 发射开销占比极高；更致命的是，访存受限算子（如 Expert 投影）还没跑满全部 SM 就已经打满了内存总线，导致多余的 SM 空转；而紧随其后的计算受限算子又让内存带宽空闲，形成周期性的硬件算力饥饿与带宽空洞；
- **单卡内的空间切片与流水调度**：SubGPU Pipelining 在物理 GPU 内部划分出若干个独立的「SubGPU」或 Stage（阶段），每个 Stage 独占一组独立的 SM 集合（利用 NVIDIA 官方支持的 CUDA Green Contexts 进行硬件级硬件切分）；
- **微批次平滑吞吐**：全局 Batch 被拆解为微批次（Microbatches），微批次流水穿梭于各个 Stage 之间。当 Stage 0 在对微批次 2 运行前置注意力算子时，Stage 1 正在对微批次 1 运行后置 MLP/GEMM 算子。计算密集型算子与访存密集型算子在单卡内部实现时空交叠，消除发射气泡并熨平 HBM 访存峰谷。

3. 关键结论：
- **真实 Blackwell B200 物理验证**：研究团队在一张物理 NVIDIA B200 GPU 上模拟了 32 卡 B200 集群部署下的 GPT-OSS 120B 工作负载，在全局批次 2,048、采用 TensorRT-LLM 算子库的双阶段流水线配置下，实测平均 DRAM 读写吞吐率从基线的 **71.8% 跃升至 83.6% 峰值**，36 层 Decoder 迭代耗时直接缩短 **10.33%**；
- **Pareto 前沿性能建模**：共享资源仿真器探索表明，在相同单卡吞吐下，SubGPU 流水线能提供最高 **2.2 倍的单用户每秒吞吐（Per-user Throughput）**；而在相同单用户延迟达标线下，提供最高 **1.9 倍的单卡吞吐收益**。

4. 背景地位：
来自英伟达系统工程与架构部门的直接贡献。这是业界首个在 Blackwell B200 真实硬件上验证、利用 CUDA Green Contexts 在单卡内部实现微批次流水线并行的标杆级论文。它标志着大模型推理优化已跨越了简单的多卡并行（TP/PP/EP），正式迈入单卡微架构级的空间隔离与流水调度时代。

5. 落地相关性：
对深度从事 GPU 调度切分（MPS、MIG、Green Contexts）与推理引擎底层开发的工程师极具启发。随着 GPU 算力密度不断暴涨（B200/GB200），传统依靠全局顺序发射算子的 TensorRT-LLM 或 vLLM 架构将遭遇严重的微架构边际效用递减。在引擎内部集成基于 SM 划分的空间流水线，是最大化压榨下一代 AI 芯片利用率的必由之路。

---

#### 3. Starscream: Reimagining LLM Sharding on AMD Instinct GPUs with GPU Partitioning
- 中文译名：Starscream：基于 GPU 硬件切分重构 AMD Instinct 芯粒架构下的大模型分片机制
- 链接：https://arxiv.org/abs/2611.15951
- 作者：Sumanth Gudaparthi, Smeet Chheda, Ganesh Dasika
- 单位：超威半导体 (AMD Research and Advanced Development) 【工业界】
- 分类：cs.DC
- 方向标签：C. AI Infra (AMD Instinct MI300X/MI355X 芯粒架构、GPU 物理切分/NUMA 域、LLM 模型分片、对称内存与分层集合通信) & B. 编排与调度 (GPU 算力切片与拓扑感知)
- 相关度：5/5

1. 核心贡献：
AMD 研究院与先进开发部官方团队发布了专门针对其多芯粒（Multi-Chiplet）旗舰 GPU（AMD Instinct MI300X 及下一代 MI355X）的全新大模型分片体系 **Starscream**。现代高端 GPU 为解决单晶圆良率极限，广泛采用芯粒拼装架构（MI300X 集成了 8 个 XCD 计算芯粒和 4 个 IOD 输入输出芯粒），使得 GPU 内部天然具备鲜明的非一致性内存访问（NUMA）特性。AMD 硬件提供了计算切分（DPX/QPX/CPX）与内存切分（NPS1/NPS4）能力。然而，现有主流框架（vLLM、Megatron 等）盲目将传统单维度的分布式切分（TP/PP）套用到切分后的逻辑 GPU 上，导致严重的显存冗余、计算强度坍塌以及跨芯粒通信雪崩。Starscream 首次确立了面向芯粒 GPU 的正交内部分片三大原则，在 MI300X/MI355X 上使 Self-Attention 算子提速高达 4 倍，Fused GEMM 提速 1.43 倍。

2. 原理解析：
这就像在具有多个 CPU Socket 和 NUMA 节点的超大型物理服务器上部署 Kubernetes Pod：
- **盲目切分的陷阱**：在 MI300X 上开启 CPX 模式（将 1 张物理卡切分为 8 个逻辑 GPU），若直接让推理框架把它们当成 8 张卡去跑常规张量并行（TP），会发生灾难性的性能坍塌：
  1) **算力强度崩塌**：大矩阵被生硬地切成细长条（Skinny Matrices），GEMM 运算迅速退化为受内存带宽限制的访存操作；
  2) **显存冗余爆炸**：每一路切片都复制一份不必要的参数或 KV Cache；
  3) **通信严重倾斜**：扁平的全收集（All-Gather/All-Reduce）算子无视了单卡内部芯粒互联与跨物理卡网络之间高达 **10 倍的带宽断崖**；
- **Starscream 的正交解法**：
  1) **保持算子形状（Kernel Shape Preservation）**：通过二维 GEMM 分片维持计算密度，绝不破坏底层矩阵计算的黄金长宽比；
  2) **消除显存冗余（Redundancy Elimination）**：引入沿序列长度（Sequence-Length）切分的自注意力机制，杜绝各切片间 KV Cache 的重复拷贝；
  3) **分层通信与对称内存融合（Hierarchical Collectives & Symmetric Memory）**：将昂贵的全局集合通信拆解为「芯粒内部高带宽聚合」+「跨物理卡轻量传输」，并通过 AMD 对称内存（Symmetric Memory）将通信直写与计算原生融合。

3. 关键结论：
在 AMD Instinct MI300X 及 MI355X 物理硬件上，针对 Llama3-70B、Llama3-405B 以及 GPT-OSS 120B 大模型的严格实测中：
- Starscream 的分片机制相比忽略芯粒拓扑的朴素切分基线，**Self-Attention 算子取得了高达 4× 的端到端加速**；
- Fused GEMM 融合算子获得了 **1.43× 的性能提升**；
- 彻底扭转了此前开启 GPU Partitioning 后大模型吞吐反向暴跌的负优化局面，首次证明了充分利用芯粒硬件切分是释放万亿参数模型吞吐潜能的核心杠杆。

4. 背景地位：
来自 AMD 官方研发机构的核心突破。随着半导体工艺逼近物理极限，无论是 AMD MI300X/MI355X 还是 NVIDIA Blackwell 均全面倒向多 Chiplet 互连封装。这篇论文是系统界首个系统性剖析 Chiplet-NUMA 拓扑对 LLM 并行策略冲击并给出权威工程解决方案的开山之作。

5. 落地相关性：
对于正在国内算力集群或海外公有云中采纳 AMD ROCm 生态、部署 MI300X 集群的云原生架构团队具有决定性指导意义。它不仅给出了在 Kubernetes Device Plugin 与 ROCm 驱动层配置 Compute/Memory Partitioning 的最佳实践，更为在上层编排 Volcano、Ray 及 vLLM-ROCm 分片参数时提供了不可或缺的拓扑对齐指南。

---

#### 4. SS-HSDP: Efficient and Flexible Sharded Data Parallelism via Runtime-Update Decoupling
- 中文译名：SS-HSDP：基于计算-更新解耦的高效灵活混合分片数据并行框架
- 链接：https://arxiv.org/abs/2611.16467
- 作者：Chendong Xiang*, Pengle Zhang*, Jinliang Li, Zichen Liang, Jintao Zhang, Fan Bao‡, Jun Zhu‡, Jianfei Chen‡
- 单位：清华大学 (Tsinghua University) 【知名实验室】、生数科技 (Shengshu Technology) 【工业界】
- 分类：cs.DC
- 方向标签：C. AI Infra (分布式训练、FSDP/ZeRO-3/HSDP、计算更新解耦、MXFP8 混合精度、Muon 矩阵优化器)
- 相关度：5/5

1. 核心贡献：
清华大学朱军、陈键飞团队与生数科技（Vidu 视频大模型背后的核心研发力量）联合提出面向超大规模模型训练的高性能分布式并行框架 **SS-HSDP**。针对现代前沿大模型在低精度训练（如 MXFP8 微缩放格式）与前沿优化器（如近期备受瞩目的矩阵优化器 **Muon**）演进中暴露出的底层结构性冲突，SS-HSDP 首次提出了**「运行时计算参数（Runtime Parameters）与优化器更新参数（Update Parameters）彻底解耦」**的全新架构，通过共享数据视图（Shared Data Views）与分层分片体系，在保持完全零拷贝执行的同时赋予训练框架极致的灵活性，在 128 卡 GPU 集群上相比当前最强基线将模型浮点利用率（MFU）提升了高达 21.7%。

2. 原理解析：
这就像在云原生微服务开发中将「面向高性能查询的数据读视图（Read Replica Cache）」与「面向事务持久化的领域实体模型（Write Model）」进行 CQRS 架构解耦：
- **分布式训练底层的结构性死锁**：在 ZeRO-3 / FSDP2 / HSDP 等分片数据并行体系中，权重（Weights）、梯度（Gradients）与优化器状态（Optimizer States）以紧耦合的同构形式分片在各卡上。然而现实工业界的两大演进趋势打破了这种美好假象：
  1) **计算端要求极致打包（Packed）**：为了喂饱 Tensor Core，前向和反向计算要求把 QKV 投影权重紧密打包成定制排布的融合张量，配合 MXFP8 的 Block Scale 布局；
  2) **优化端要求独立细粒度（Per-Unit）**：新型优化器 Muon 要求按注意力头（Per Attention Head）甚至独立的二维子矩阵进行正交化动量更新；
- 现存框架如 PyTorch FSDP2、字节跳动 veScale-FSDP 或 Megatron-FSDP 被迫二选一，要么牺牲计算性能无法深度融合算子，要么直接阉割对 Muon 等高级优化器的支持；
- **SS-HSDP 的解耦与零拷贝共享视图**：SS-HSDP 将内存结构拆分为「运行时参数」和「更新参数」。计算阶段各层使用极致打包的紧凑 Tensor 运行极速 GEMM；在优化器更新阶段，系统通过底层的 Strided Shared Views 虚拟切片指针，让优化器直接原地对子矩阵进行原地数学运算，全程不引入任何跨内存区域的额外搬运或重排开销。

3. 关键结论：
- 在大规模视频生成大模型（Vidu 系列架构）与语言模型上，基于 MXFP8 混合精度的严苛训练基准测试表明，SS-HSDP 的性能全面超越 PyTorch FSDP2、字节跳动 veScale-FSDP 以及 Megatron-FSDP；
- 在 **128 张 GPU 集群规模**下，SS-HSDP 相比当前业界评测中最快的基线，**Model FLOPs Utilization (MFU) 提升高达 21.7%**，同时峰值显存占用持平或更低；
- 完美支持了包含 Muon、AdamW 在内的多种现代优化器，并已在生数科技生产级多模态大模型研发闭环中全面实战上线。

4. 背景地位：
来自国内顶尖 AI 系统团队清华大学 PACMAN/TSAIL 实验室与全球顶尖多模态生成创企生数科技的工业级重磅成果。论文直接对决 Meta 的 FSDP2 与字节跳动的 veScale，代表了国产大模型训练底层通信编排与显存管理框架的一流水平。

5. 落地相关性：
对于在大型 Kubernetes 集群中负责大模型预训练与持续后训练（Post-training / RL）平台的 Infra 工程师而言，Muon 优化器与 FP8 训练是当前最炙手可热的技术热点。SS-HSDP 提供了完美的解法，直接消除了底层算子开发者与上层算法科学家在张量排布上的长久冲突，可直接指导企业私有训练平台底层 FSDP 引擎的架构重构。

---

#### 5. Broadcast, Don't Replicate: Eliminating Weight HBM in Datacenter LLM Serving
- 中文译名：广播而非复制：彻底消除数据中心大语言模型推理中的权重 HBM 显存
- 链接：https://arxiv.org/abs/2611.17097
- 作者：Hannah Atmer, Yuan Yao, Thiemo Voigt, Stefanos Kaxiras
- 单位：乌普萨拉大学 (Uppsala University) 【知名实验室】
- 分类：cs.DC, cs.AR
- 方向标签：C. AI Infra (数据中心机架级推理架构、光广播共享内存 OBM、脱离本地 HBM 束缚、MoE 广播流调度) & B. 编排与调度 (超大规模集群显存池化)
- 相关度：5/5

1. 核心贡献：
瑞典乌普萨拉大学体系结构实验室提出了一种足以颠覆现代 AI 数据中心基础设施的革命性架构——**光广播共享内存（Optical Broadcast Memory, OBM）**。当前数据中心部署大模型推理服务时，成千上万张昂贵的 GPU 各自在本地高速 HBM/DRAM 中复制存储完全相同、且全生命周期只读的数百 GB 模型静态权重，不仅导致集群硬件采购成本（CapEx）中绝大部分被 HBM 吞噬，更产生了恐怖的静态漏电功耗与重复访存能耗。OBM 彻底抛弃了每张卡独立存储权重的传统范式，由集中式内存服务器通过分层 Tap-and-Amplify 光纤网络持续单向广播权重流，数万张计算节点利用片上共封装光学器件（Receive-only CPO）在飞行的光纤信号中实时「搭便车（Tap）」直接提取权重喂给计算核心，在 **80,000 张加速卡的数据中心规模**下消除了数以 PB 计的昂贵 HBM，吞吐与能效比全面超越传统 HBM 推理集群。

2. 原理解析：
这就像在超大型城市中将千家万户「各买一套昂贵的私家储水箱并在本地反复加热」，改造成「由中央热电厂通过高压环网持续循环供应高温热水，各住户水龙头即开即用、零本地蓄水」：
- **传统 HBM 复制的荒谬困境**：在 8 万张卡的大型推理农场里，如果部署 Llama-405B，每张卡或每个 8 卡 Pod 都在用数万元的 HBM3e 存着一模一样的矩阵参数，静态待机功耗巨大，且全球 HBM 产能短缺卡死了算力扩展的脖子；
- **从光纤闭环延迟线到开环广播树**：此前学术界曾设想用几千公里的光纤闭环延迟线当作内存（Delay-Line Memory），但光纤长度随模型线性膨胀且无法适应动态负载。OBM 将其彻底革新为「开环分层分光放大树（Tap-and-Amplify）」；
- **零缓冲直接入核计算**：集中式广播服务器持续按 Decoding 步序向主干光纤脉冲注入模型权重；分布式推理节点只搭载极简的「纯接收共封装光学引擎（Receive-only CPO）」，没有昂贵的激光发射器和复杂的 RDMA 网卡缓冲，光信号进入芯片后通过分光器无缝转换为电信号直接喂入计算单元；系统辅以动态松弛窗口（Dynamic Slack）平滑不同用户上下文长度差异，并原生支持 MoE 模型的专家广播流。

3. 关键结论：
- 在覆盖 **80,000 张加速器节点的数据中心超大规模**仿真验证中，OBM 在整个数据中心内**彻底消除了全部权重 HBM（总量达数以百计的 PB 显存空间）**；
- 在端到端推理完成吞吐量（Throughput）与每 Token 能量消耗（Energy per Token）两项关键核心指标上，OBM 均达到甚至显著优于全套配备昂贵 HBM 的传统 GPU 集群；
- 节点由于剥离了高发热量的 HBM 堆栈和光发射激光器，单芯片制造成本与热设计功耗（TDP）急剧下降。

4. 背景地位：
来自欧洲计算机体系结构名校乌普萨拉大学 Stefanos Kaxiras 教授（IEEE/ACM Fellow）团队的重磅力作。这是系统架构领域首次在工程可行性与光学网络拓扑层面对大模型服务化提出「无本地权重内存（Weight-HBM-Free）」的系统实现方案，为打破算力中心「Memory Wall」与「Power Wall」提供了颠覆性蓝图。

5. 落地相关性：
对于长期饱受 GPU 采购预算不足、机房供电与配电瓶颈困扰的云原生机房架构师与基础设施规划者而言，这是一剂强心针。它揭示了下一代机架级乃至整机房级 AI 算力设计的未来终局：计算单元将彻底无状态化与轻量化，昂贵的高速存储通过机架级光互联统一流式供给。

---

#### 6. Recompute or Restore? Host-Tier KV for Multi-Model Agent Workflows on a Static-Graph NPU Serving Stack
- 中文译名：重算还是恢复？静态图 NPU 服务栈上面向多模型智能体工作流的宿主机分层 KV 机制
- 链接：https://arxiv.org/abs/2611.15126
- 作者：Sungwon Woo, Seyeon Kim
- 单位：高丽大学 (Korea University) 【知名实验室】、Rebellions 【工业界】
- 分类：cs.DC, cs.LG, cs.PF
- 方向标签：C. AI Infra (静态计算图 NPU 服务栈、Rebellions ATOM+、智能体多模型工作流、Host-Tier KV 缓存分层与换入、Prefill 冗余治理)
- 相关度：5/5

1. 核心贡献：
高丽大学与韩国知名 AI 芯片独角兽企业 Rebellions 针对商业化**静态图 NPU 算力集群（Rebellions ATOM+ 服务器与 vllm-rbln 0.10.2 栈）**，首次系统性研究了多模型协同智能体（Multi-Model Agent Workflows，例如由 Qwen3-8B 充当 Planner 规划器、Qwen3-0.6B 充当 Executor 执行器）在生产级高压过载场景下的崩溃机理。论文揭示了在静态编译的 NPU 架构上，当片上 KV Cache 显存耗尽发生驱逐时，**高达 89.5% 的规划器计算沦为对历史前缀的重复执行（Repeated Prefill）**。团队构建了直通 NPU 底层内存布局的宿主机分层 KV 桥接器（Host-Tier KV Bridge），在真实硬件上将智能体工作流的业务 SLO 达标率从惨不忍睹的 9.4% 直接挽救回 **99.8%**。

2. 原理解析：
这就像在基于 Kubernetes 容器编排的微服务系统中分析「本地内存缓存击穿」与「走网络拉取 PV 存储」的代价权衡：
- **静态图 NPU 的天生枷锁**：与英伟达 GPU 灵活的动态内存管理（如 PagedAttention）截然不同，商业化 NPU（如 Rebellions ATOM、Google TPU 等）为了追求极致算力能效比，必须在编译期将模型计算图和片上 KV Cache 内存池的尺寸彻底锁死，且由芯片私有运行时（Vendor Runtime）独霸内存布局；
- **智能体工作流引发的显存击穿**：智能体任务（规划-执行-归纳）由多个模型串行交替调用，且各阶段严重共享超长 Prompt 上下文。在 NPU 片上定长缓存被撑爆后，已完成请求的前缀被无情逐出片上显存。当下一阶段调用到来时，系统不得不重新跑一遍漫长的 Prefill；
- **重算（Recompute）vs 恢复（Restore）的精细博弈**：把驱逐的 KV Cache 存到 Host 内存（CPU DRAM），看似美好，但在静态图 NPU 栈中，通过 PCIe 拷贝恢复 KV 会独占正在运行 Decode 解码的引擎主线程！如果无脑搬运，PCIe 传输本身的耗时甚至会拖垮整个推理线程。该工作通过建立调度感知的离散事件预测模型，精准把控在何种负载与前缀长度下通过 Host-Tier 恢复 KV 能够彻底碾压重新计算。

3. 关键结论：
- 在由 2 张 ATOM+ 卡部署 Qwen3-8B 规划器、1 张 ATOM+ 卡部署 Qwen3-0.6B 执行器的真实 NPU 生产服务器上实测：
- 在默认的原生服务栈过载崩溃时，规划器执行的全部 Prompt Token 中有 **89.5% 是此前早已计算过的纯粹冗余 Prefill**；
- 引入 Host-Tier KV 桥接器后，在两种严苛的过载压测场景下，智能体工作流的端到端 **SLO 达标率分别从 22.8% 飙升至 100%，以及从 9.4% 跃升至 99.8%**；
- 在 Chain（链式）与 Fork（分叉）智能体工作流中，端点确认支撑的稳定算力承载增益分别达到 11.8% 与 18.2%；离散事件性能预测模型对 P99 尾延迟的预测误差保持在 15% 容差以内。

4. 背景地位：
来自韩国顶尖大学高丽大学与主力 NPU 硬件厂商 Rebellions 的一线实测突破。这是学术界与工业界首次针对商用静态图 NPU 算力栈（而非通用英伟达 GPU）深入解剖多模型 Agent 服务化瓶颈并实现 Host 级 KV 扩展的实证文献。

5. 落地相关性：
对于正在考虑或已经采购国产静态编译 NPU、TPU 或专用加速卡（如华为昇腾、燧原、昆仑芯、Rebellions 等）来替代昂贵英伟达 GPU 的云原生 AI 算力平台架构师具有极高的实操参考价值。它指明了在 NPU 上跑复杂 Agent 工作流绝不能生搬硬套默认配置，必须结合 Host-Tier KV 换入换出并配套调度协同，才能避免芯片算力沦为无休止的重复 Prefill 垃圾时间。

---

#### 7. Reducing Batch Makespan for LLM Agent Workloads through Inference-Environment Coordination
- 中文译名：通过推理与环境协同降低大语言模型智能体工作负载的批处理总耗时
- 链接：https://arxiv.org/abs/2611.16661
- 作者：Wei Feng, Meiling Chen, Boxiao Chen, Lu Liu, Bin Zi, 等（共 9 位作者，通讯作者：Xingyu Lu）
- 单位：蚂蚁集团 Ling 团队 (Ling Team, Ant Group) 【工业界】
- 分类：cs.DC
- 方向标签：B. 编排与调度 (智能体批处理 Makespan 优化、长尾作业收敛、沙箱环境并发解耦) & C. AI Infra (混合架构 KV/循环状态分配、轨迹感知前缀缓存路由、CAAS 调度器)
- 相关度：4.5/5

1. 核心贡献：
蚂蚁集团主力大模型技术团队（Ling Team）针对智能体在强化学习（RL Rollout）、基准评测（SWE-bench 等）以及合成数据生成（Synthetic Data）等离线/批处理场景下的核心效率痛点，提出了首套**推理-沙箱环境端到端协同优化体系**。在智能体批量作业中，所有下游流水线必须等待整批任务全部完成，因此决定研发迭代效率的核心瓶颈是**批处理总耗时（Batch Makespan）**而非单请求首字时延。团队针对混合架构大模型（Hybrid LLMs）的显存分配、多轮轨迹前缀路由以及外部环境受限下的长尾木桶效应展开联合重构，提出 **CAAS 关键链路推进调度算法**，在 Ling-3.x 真实模型与权威基准上实现 Makespan **10.4% 至 65.0% 的断崖式削减**。

2. 原理解析：
这就像在 Kubernetes 集群中使用 Argo Workflows 或 Volcano 编排具有海量复杂分支与外部 Sidecar 调用的批量 DAG 作业：
- **批处理智能体的结构性痛点**：每个 Agent 样本（Sample）代表一条探索轨迹（Trajectory），在执行中不停地在「GPU 上的大模型推理」与「宿主机/容器沙箱内的外部环境工具调用（执行 Bash、爬虫、跑测试用例）」之间反复横跳；
- **三大协同重构机制**：
  1) **显存与并发容量模型**：针对混合架构大模型（融合注意力机制与 RNN/Mamba 循环状态），精准建模 KV Cache 与 Recurrent State 的显存占用比例，推导出防止触发重算的黄金样本并发度上限；
  2) **轨迹感知负载均衡路由（LBCH Routing）**：基于智能体历史执行轨迹进行前缀亲和性路由，既让同一条探索链的上下文极大化复用 GPU 节点内的 Prefix Cache，又防止局部 Worker 节点被打爆热点；
  3) **准入解耦与 CAAS（Chain-Advancing Action Scheduling）调度器**：传统批处理中，沙箱环境（Docker 实例或网络并发槽位）容量有限，所有 Agent 乱序抢占沙箱，导致本就处于关键路径（Critical Path）的长链 Agent 频频阻塞排队，拖垮整个批次的最终完成时间。CAAS 将样本准入与环境执行彻底解耦，动态观测各任务的链条深度与进展，将沙箱执行名额严格优先倾斜给长执行链，全力扫清长尾木桶短板。

3. 关键结论：
- 在蚂蚁集团自主研发的 **Ling-3.0-Flash** 与 **Ling-3.1-Flash** 模型上，针对 Berkeley Function Calling Leaderboard (BFCL)、SWE-bench Multilingual、WideSearch 以及 MCP-Atlas 等高难度多轮智能体基准进行全量实测；
- 端到端批处理总耗时（Batch Makespan）**普遍缩短 10.4% 至 65.0%**，同时任务评测准确率得分与基线完全严格对齐无损；
- 该系统优化方案已在蚂蚁集团 Ling-3.x 大模型系列的全生命周期训练与评测流水线中常态化部署运行，成倍加速了算法团队的模型迭代进程。

4. 背景地位：
来自国内头部金融科技巨头蚂蚁集团核心 AI Infra 团队的工业界重磅落地成果。论文率先跳脱出了传统只关注线上单请求 TPOT/TTFT 的 Serving 局限，开辟了专属于「智能体批处理研发链路（Agentic Batch Pipelines）」的系统调度与资源协同全新范式。

5. 落地相关性：
对于在 Kubernetes 集群中负责大模型 RL 训练（如 PPO、DPO 采样池）、SWE-bench 自动化测试框架搭建或 Agent 数据飞轮建设的工程团队极具实战指导价值。论文清晰阐明了如何通过调度层将 Docker 沙箱资源向关键路径倾斜，可直接转化为 K8s 自定义控制器（Operator）或 Volcano 调度插件的业务逻辑。

---

#### 8. Read Once, Answer Many: Parallel Prompting for Shared-Context LLM Inference
- 中文译名：一次读取，并发作答：面向共享上下文大语言模型推理的并行提示机制
- 链接：https://arxiv.org/abs/2611.15130
- 作者：Zekun Zhao, Jeffrey Flanigan
- 单位：加州大学圣克鲁兹分校 (University of California, Santa Cruz)
- 分类：cs.CL, cs.DC
- 方向标签：C. AI Infra (LLM 推理服务、SGLang 扩展、RadixAttention/Prefix Caching 增强、并行流注意力掩码、CUDA Graph 捕获)
- 相关度：4.5/5

1. 核心贡献：
加州大学圣克鲁兹分校研究团队针对长文档批量问答（Document QA）、自动化数据标注（Data Labeling）以及 LLM-as-a-Judge 评测等共享超长前缀的推理场景，指出了当前生产级前缀缓存（Prefix Caching）架构的核心瓶颈，并提出了 **Parallel Prompting（并行提示解码）** 机制。现存引擎（vLLM 的 PagedAttention、SGLang 的 RadixAttention）虽然消除了共享文档的重复 Prefill，但在后续解码（Decode）阶段，针对同一个文档的 $Q$ 个独立提问仍然被当作 $Q$ 个独立请求处理，导致每个 Decoding 步长中**整个长文档的 KV Cache 都要被重复从 GPU 显存读入缓存 $Q$ 次**，使推理严重受制于显存带宽墙。Parallel Prompting 将针对同文档的 $P$ 个提问聚合成单请求内的 $P$ 路并行独立流，仅需一次读取共享文档 KV Cache，在开源 SGLang 生产引擎上实现高达 **3.7~6.0 倍的吞吐暴增**。

2. 原理解析：
这就像在 Linux 操作系统中多个轻量级线程通过只读映射（`mmap` MAP_SHARED）共享同一个大文件的只读页缓存，而不是让每个独立进程各自往自己的内存空间里深拷贝一份：
- **现存架构的访存雪崩**：当用户对一个 16K tokens 的长文档连续提问 128 个问题时，即便开启了前缀缓存，Decode 阶段每一轮输出 1 个 token，GPU 都要把这 16K 对应的海量 KV 字节在显存总线上反复搬运 128 遍！由于每个问题是独立 Request，访存带宽被彻底吃光；
- **Parallel Prompting 的单请求多流架构**：系统将 $P$ 个提问打包进一个单一的复合请求中，在 Decode 步序中同时为这 $P$ 个提问并行推进解码（生成 $P$ 个流）；
- **Kernel 内 Stream-ID 注意力掩码**：各流之间绝对不能发生串扰（提问 2 的答案绝不能看到提问 1 的上下文）。团队直接在 SGLang 的 Triton Extend-Attention 算子内部植入了轻量级的 Stream-ID Mask：通过两组定长索引张量动态判断注意力可见性，既杜绝了构建巨大稠密掩码张量的显存开销，又让整个多流解码过程保持恒定的 Tensor 形状，从而**完美兼容 CUDA Graph 的固化捕获与极速回放**！
- 最终，单步解码中长文档的 KV 搬运次数从 $P$ 次骤降为 1 次，将 $P$ 个分散的矩阵-向量乘（GEMV）融合成了一个高计算密度的批处理矩阵-矩阵乘（GEMM）。

3. 关键结论：
- 研究团队在开源顶级推理引擎 **SGLang** 内部完成了完整工程落地，仅向 3 个核心文件追加了约 80 行代码并打包了轻量调度引擎；
- 在 NVIDIA A100 与 RTX A6000 硬件上，针对 CodeLlama-7B、8K~16K 长度文档及 64~256 个并发提问进行全面评测；
- 相比开启了完整 Prefix Caching 和 CUDA Graph 的原生 SGLang（FlashInfer 后端），Parallel Prompting 在 A100 上**提速 3.7 倍**，在 RTX A6000 上**提速 5.9~6.0 倍**；相比 Triton 后端提速高达 5.1~7.5 倍；
- 在总计 **144 组严格对齐的测试矩阵中（2 种 GPU × 2 个 SGLang 版本 × 6 种工作负载 × 6 套数据集），Parallel Prompting 在全部 144 次运行中无一例外保持全胜**。

4. 背景地位：
直击 RAG 密集检索、合规审计、文档分析场景下推理开销过高的死穴。这项工作精巧至极，代码量极小却以四两拨千斤的方式重构了 Decoding 阶段的显存读取流水线，已被业界视为 SGLang 与 vLLM 前缀缓存体系最重要的演进方向之一。

5. 落地相关性：
对于在私有云或公有云 K8s 集群中维护企业级知识库问答、长合同审查、Agent 数据分析服务平台的架构师来说，该论文具有近乎立竿见影的生产价值。通过在网关层将针对同文档的并发请求合并，并引入 Stream-ID Mask，可以用近乎为零的工程侵入成本，直接将现有 GPU 节点的长文本问答吞吐能力拉升数倍。

---

#### 9. GC-MoE on SM120: Overlapping Expert-Parallel Token Dispatch with Warp-Level FP8xFP4 Block-Scaled MMA on Consumer Blackwell
- 中文译名：SM120 架构上的 GC-MoE：在消费级 Blackwell 上实现专家并行 Token 分发与 Warp 级 FP8xFP4 块缩放 MMA 算子重叠
- 链接：https://arxiv.org/abs/2611.16219
- 作者：Haoyu Wang, Kan Liu, Tao Lan, Yong Li
- 单位：阿里巴巴 (Alibaba Inc.) 【工业界】
- 分类：cs.DC
- 方向标签：C. AI Infra (消费级/工作站 Blackwell SM120、MoE 专家并行通信计算重叠、CUDA Green Contexts、FP8xFP4 块缩放 MMA 算子)
- 相关度：4.5/5

1. 核心贡献：
阿里巴巴核心算子与系统团队针对 NVIDIA 最新消费级与工作站 Blackwell 芯片（计算能力 12.0 的 **SM120**，如 RTX PRO 5000），成功将面向数据中心顶级 GPU（Hopper SM90 / 数据中心 Blackwell SM100）的专家并行（EP）通信计算重叠算子 **GC-MoE** 移植并重构落地。针对消费级 GPU 缺少数据中心级 Tensor Memory、缺乏跨卡 NVLink 广播支持且仅能通过 PCIe 互联的严苛硬件限制，团队研发了基于寄存器 Swap-AB 翻转的 Warp 级微缩放矩阵乘（QMMA）核心、紧凑 FP4 解包流水线与基于 PCIe 的聚合回传机制，在 8 卡 RTX PRO 5000 节点上取得了相比 FlashInfer MegaMoE **1.522 倍**、相比 Cake MegaMoE **1.387 倍**的显著性能超越。

2. 原理解析：
这就像在没有高昂 InfiniBand/RoCE 专线网络和智能网卡 offload 的边缘廉价服务器节点之间，通过精巧的本地环形队列与内存对齐，强行实现微秒级零拷贝 RPC 流水线：
- **数据中心设计的降维打击痛点**：在数据中心级 SM100（如 B200）上，GC-MoE 利用 NVLink 的高带宽和硬件 TMA 组播，用 CUDA Green Contexts 划出几个 SM 专职做通信，剩下的 SM 专职做计算，二者在持久化 CUDA Graph 中交叠运行。然而，当把这套方案搬到工作站级的 SM120 显卡上时立刻碰壁：
  1) **硬件特性被阉割**：SM120 没有 Tensor Memory，没有两块 CTA 协同的 MMA，微缩放 Tensor Core 只能通过最底层的 Warp 级指令（`mxf8f6f4`）调用；
  2) **网络退化为 PCIe**：跨卡传输只能走慢速的 PCIe 总线，Combine 阶段由各个专家回传的 BF16 结果成为了整个通信链路中最庞大、最致命的阻塞瓶颈；
- **针对 SM120 的系统级重构**：
  1) **Swap-AB 寄存器翻转机制**：将 4 位的 FP4 专家权重绑定在 QMMA 的 A 操作数，而将 FP8 激活值绑定在 B 操作数，使得矩阵在 Token 维度变化时无需重构庞大的权重流水线，零成本支持动态 Batch 形状；
  2) **MMA 立即数直选 Scale**：利用指令内置的立即数直接定位 32 元素块缩放字节，彻底剔除内部循环中昂贵的位移与洗牌指令；
  3) **PCIe 聚合流式回传（Bulk-Store & Relay Copiers）**：在本地显存开辟 Position-Major 缓冲区，专职的中继拷贝线程将分散的专家输出聚合成大块连续内存跨 PCIe 传输，消灭细碎碎片。

3. 关键结论：
- 在配备 **8 张 NVIDIA RTX PRO 5000 GPU（通过 PCIe 互联）**的工作站服务器上进行严格实测；
- 在跨越 18 个严苛的解码负载配置和 2 种前沿 MoE 模型形状下，面对 FlashInfer CuTe DSL W4A8 MegaMoE 算子，GC-MoE 取得 **18 战全胜，平均提速 1.522 倍**；
- 面对高性能 Cake MegaMoE 算子，GC-MoE 同样取得 **18 战全胜，平均提速 1.387 倍**；
- 在融合共享专家（Shared Expert）的变体中，依然领先 Cake 1.388 倍；
- 通过了全部 94 个严苛的数值精度测试，跨算子余弦相似度高达 0.9999997，确保数学计算绝对无损。

4. 背景地位：
来自阿里巴巴顶级工业界系统团队的硬核硬件级调优成果。该工作不仅展现了令人惊叹的底层 CUDA / PTX 汇编与 Warp 级算子掌控力，更为即将全面铺向开发者工作站和轻量级机房的消费级 Blackwell 显卡（SM120 / RTX 50 系列）注入了强心剂。

5. 落地相关性：
对于广大无法承担数百万昂贵 H100/B200 机架、但又极度渴望在本地工作站或中小规模 K8s 集群（基于 PCIe 组网的消费级/工作站 GPU）部署 DeepSeek-V3 等大尺寸 MoE 模型的企业与研发实验室而言，提供了极具价值的开源算子基础设施，极大降低了私有化部署前沿 MoE 模型的硬件门槛。

---

#### 10. Metal Sandbox: Isolated Execution and Command Scheduling for GPU Coding Agents on Apple Silicon
- 中文译名：Metal Sandbox：面向 Apple Silicon 平台 GPU 代码智能体的隔离执行与命令级调度架构
- 链接：https://arxiv.org/abs/2611.17294
- 作者：Haozhe Wang, Lina Chen, Fanqi Wan, Qi Han, Yinmin Zhang, 等（共 8 位作者，通讯作者：Junchi Yan）
- 单位：上海交通大学 (Shanghai Jiao Tong University) 【知名实验室】、阶跃星辰 (StepFun) 【工业界】、北京中关村学院 (Beijing Zhongguancun Academy)
- 分类：cs.LG, cs.DC, cs.OS
- 方向标签：A. 容器与运行时 (沙箱隔离、受限工作区、代码智能体安全执行) & B. 编排与调度 (命令级跨节点窃取调度、GPU 空闲复用) & C. AI Infra (Metal 算子生成与评测生态)
- 相关度：4.5/5

1. 核心贡献：
上海交通大学严骏驰教授团队与国内大模型领军企业阶跃星辰（StepFun）联合推出了首个面向端侧 Apple Silicon 生态、专为自主生成 GPU 算子代码的 AI Agent 打造的安全隔离与分布式协同执行系统——**Metal Sandbox**。论文通过真实系统的长时间追踪，揭示了代码智能体（Coding Agent）在自主编写、调试与评测 GPU 底层算子时的一个惊人现象：在长达 31.6 分钟的典型 Session 中，**物理 GPU 真正处于活动状态的时间仅有 44.0 秒，GPU 利用率仅有 2.32%！** 绝大部分时间被 LLM 思考生成、本地文件修改、静态检查等非 GPU 任务占满，造成极大硬件算力闲置。为此，研究团队设计了具备受限文件访问的实例沙箱与跨节点命令级窃取调度器，并与 Harbor 自动化评测平台全面集成，在 4 节点 Mac mini M4 集群上实现命令吞吐提升高达 1.68~2.05 倍。

2. 原理解析：
这就像在 Kubernetes 集群中将传统的「全生命周期独占静态 Pod（Pod 占着整个 GPU 不放）」重构成「轻量安全沙箱容器 + 细粒度 Serverless 命令调度器」：
- **安全沙箱防线（Security Isolation）**：让 AI Agent 自由在本地编写、编译并运行底层的 C++/Metal 代码极其危险，恶意或失控代码极易覆写宿主机系统。Metal Sandbox 为每个 Agent 实例构建严格受限的私有工作空间（Private Workspace），限制文件越权读写，确保本地原生工具链调用的安全性；
- **串行与并行命令分类解耦**：将 Agent 发出的操作解构成两类：
  1) **并行命令（Parallel Commands）**：如文件查看、语法 Linting、代码编辑等，允许多个 Session 共享同一节点的 CPU/内存并发推进，无需任何排队；
  2) **串行排他命令（Serial Commands）**：真正触发 GPU 编译运行与微秒级精准耗时评测的命令，必须独占进入节点的单槽位执行队列，防止并发算子干扰测速基准；
- **跨物理 Mac 节点的实时任务窃取与迁移**：当某台 Mac 节点上的串行 GPU 队列拥堵，而集群内其他互联的 Mac 节点正处于 Agent 思考的 GPU 闲置期时，等待中的命令可以连带其上下文自动跨网络迁移（Migrate）到空闲 Mac 上执行，并将测量结果无缝透传回原始 Agent 会话，全程对 Agent 内部状态透明。

3. 关键结论：
- 研究团队在由 **4 台 Mac mini M4 节点**组成的互联集群上开展真实压力评测；
- 在高密度的并发算子开发请求下，Metal Sandbox 的命令吞吐量提升了 **1.68× 至 2.05×**；
- 在单节点承载 4 个并发 Session 的持续运行测试中，集群持续吞吐提升达到 **2.14×**；
- 在真实 Trace 的动态回放下，智能体等待外部工具执行的均值等待时间削减了 **18.8%**，整批 Agent 任务的完成耗时（Batch Elapsed Time）缩减了 **22.3%**；
- 核心系统与 Harbor 评测基准套件已在 GitHub 全面开源。

4. 背景地位：
来自国内顶尖高校上海交大与独角兽阶跃星辰的前沿交叉成果。这是业界首个将 AI Agent 安全运行时沙箱（Agent Sandbox Runtime）与微架构级 GPU 算子生成评测场景深度绑定的系统工作，填补了 Apple Silicon 平台在 AI Infra 与 Agentic 编排上的关键拼图。

5. 落地相关性：
对于正在构建自动化代码生成智能体（如 Devin、SWE-agent 类应用）、尤其是涉及底层硬件算子自动化搜索与编译调优的团队而言，具有直接借鉴意义。它指出了传统为 Agent 分配独占 GPU 虚拟机的巨大资源浪费，证明了采用轻量沙箱配合细粒度命令级抢占调度，可以用极低的硬件成本支持数倍规模的并发智能体演练。

---

#### 11. Tideway: Phase-Aware Tiered Memory Management for MoE Inference on Consumer Devices
- 中文译名：Tideway：消费级设备上面向混合专家模型推理的阶段感知分层内存管理系统
- 链接：https://arxiv.org/abs/2611.14848
- 作者：Yifei Wang, Tsun-yu Yang, Yechen Xu, Hancheng Ye, Qinsi Wang, 等（共 10 位作者，通讯作者：Hai Li, Danyang Zhuo, Yiran Chen）
- 单位：杜克大学 (Duke University) 【知名实验室】
- 分类：cs.OS, cs.DC, cs.PF
- 方向标签：C. AI Infra (消费级端侧 MoE 推理、统一分层内存池 VRAM/RAM/SSD、Prefill/Decode 阶段感知换页、CUDA Graph 保留)
- 相关度：4.5/5

1. 核心贡献：
杜克大学陈怡然、李海教授团队联合提出面向消费级个人设备（Consumer PC / Edge Workstations）运行超大参数混合专家模型（MoE）的高效分层内存管理系统 **Tideway**。端侧设备往往受制于有限的 GPU 显存（如 RTX 5090 仅 32GB）与有限的系统内存（16~64GB），无法将数十乃至上百 GB 的前沿 MoE 权重常驻，必须将权重按需换页（Paging）溢出至 SSD。现有框架将显存、主机内存与固态硬盘割裂为孤立的多级 Cache，导致推理过程中遭遇灾难性的跨层颠簸（Thrashing）与 PCIe 总线阻塞。Tideway 首次将 GPU VRAM 与 Host RAM 抽象为统一内存池，结合 Prefill 与 Decode 阶段截然相反的访存行为实行阶段感知重组，并在动态换页下完好保留了 CUDA Graph 的高效回放，平均端到端时延降低 1.97 倍，首字时延（TTFT）加速高达 2.40 倍。

2. 原理解析：
这就像在 Linux 操作系统的虚拟内存子系统中，结合业务阶段自适应调整 `swappiness`、页缓存（Page Cache）换出算法与大页映射（Huge Pages）：
- **MoE 两阶段访存的内在分裂**：
  1) **Prefill 阶段（长输入）**：成千上万个 Prompt Token 同时输入，几乎全网激活了每一层的所有专家！此时专家访问呈现高度确定性的「稠密流式扫描（Streaming Access）」，瓶颈在于吞吐量，系统需要像大管道一样快速流水吞吐；
  2) **Decode 阶段（逐字生成）**：每个 Token 仅激活稀疏的 Top-2 或 Top-4 专家，但哪几个专家被激活在运行时完全不可预测。一旦所需的专家未命中显存，解码循环必须被动硬性停顿，等待从 SSD/RAM 漫长调页，造成严重的每 Token 延迟（TPOT）拖尾；
- **Tideway 的三大系统创新**：
  1) **统一去重内存池（Unified Memory Pool）**：坚决避免同一专家权重同时在 VRAM 和 Host RAM 中保留双份拷贝；同时充分压榨 PCIe 的全双工双向带宽，在将新专家换入 GPU 的同时，将淘汰的 GPU 专家异步写回 Host RAM，杜绝后续重复从极其缓慢的 SSD 重新读取；
  2) **阶段自适应拓扑切换（Phase-Aware Layouts）**：在 Prefill 与 Decode 的交界处，平滑重组内存排布，使 Prefill 获得最大流式吞吐，Decode 获得最高缓存命中率；
  3) **专家调页下的 CUDA Graph 延续**：传统换页机制会打破 CUDA Graph 的固定内存指针假设，导致系统退化为昂贵的主机端逐算子下发。Tideway 巧妙解耦了执行骨架与专家内存槽位，在动态加载外部专家权重的极限工况下依然维持 CUDA Graph 的极速回放。

3. 关键结论：
- 在配备单张 **NVIDIA RTX 5090（32GB VRAM）**、系统内存 16~128 GiB 的典型高配消费级 PC 上实测；
- 评测涵盖 Qwen3.6-35B-A3B、Gemma4-26B-A4B 以及 DeepSeek-V4-Flash 三大代表性前沿开源 MoE 模型，覆盖 270 组固定配置（Prompt 长度达 128K）及 8 套 TraceLab 真实多轮代码 Agent 轨迹；
- 相比业界最快基线系统，Tideway 实现了端到端平均延迟 **1.97× 的提速**；首字时延（TTFT）**提速 2.40×**；单 Token 生成吞吐提升 **1.61×**；
- 源代码已在 GitHub 全面开源。

4. 背景地位：
来自体系结构与智能系统领域享誉全球的杜克大学团队（CEI Lab，陈怡然/李海/卓丹阳教授）。该论文直击大模型落地「平民化与本地隐私化」的最核心痛点，代表了学术界在单卡端侧运行超大 MoE 模型的最高工程水准。

5. 落地相关性：
对于边缘计算、本地代码审查助手以及在本地算力受限工作站上运行大模型的研发团队具有不可替代的工程价值。论文提出的 VRAM-RAM 统一去重池与动态 CUDA Graph 保留策略，可直接反哺给 llama.cpp、Ollama、vLLM 的 CPU/GPU Offloading 模块进行工业级增强。

---

#### 12. Towards Runtime-Aware Observability for Java Virtual Threads
- 中文译名：面向 Java 虚拟线程的运行时感知可观测性机制
- 链接：https://arxiv.org/abs/2611.14999
- 作者：Wenjie Ding
- 单位：英国纽卡斯尔大学计算学院 (School of Computing, Newcastle University)
- 分类：cs.PF, cs.OS
- 方向标签：A. 容器与运行时 (eBPF / USDT 探针、Java 21 虚拟线程 Project Loom、用户态 $M:N$ 运行时观测) & D. 性能与可靠性 (微服务调用链追踪、零开销静默探针)
- 相关度：4.5/5

1. 核心贡献：
针对云原生 Kubernetes 集群中日益普及的 Java 21+ 虚拟线程（Virtual Threads，Project Loom），深入剖析了传统操作系统级可观测性工具（如基于 **eBPF** 的 OpenTelemetry、Grafana Beyla、DeepFlow 等）在遭遇用户态 $M:N$ 线程调度时发生的**严重静默失效（Silent Failure）**问题。由于虚拟线程将数万个用户并发单元复用在极少数 OS Carrier 载体线程上，导致传统的「以 OS 线程 ID 为唯一关联键」的假定彻底崩塌，实测导致 **63% 的链路 Span 丢失父请求，19% 的日志行错误附带了他人的 Trace ID！** 作者通过对 OpenJDK 进行微内核式改造，将一个紧凑的 64 字节堆外 Trace 缓冲区与虚拟线程生命周期强绑定，并通过 4 个 USDT 静态探针向 eBPF 发布上下文，在无监听者时将开销压低至极限的 **33 ns**，完美实现了用户态纤程与内核级事件的亚微秒级精确关联。

2. 原理解析：
这就像在 Kubernetes 节点上，如果某个 Pod 内部跑了一个复杂的多租户代理服务，将几千个不同租户的 HTTP 请求汇聚在同一个对外长连接 Socket 上，宿主机内核的 `conntrack` 或网络抓包工具就会完全无法区分到底哪一段流量属于哪个租户：
- **云原生可观测性的基石塌陷**：eBPF 监控的黄金法则是「一个 OS 线程在一段时间内只忠实处理一个请求」（One-execution-per-thread）。一旦内核截获系统调用，就可以拿 `bpf_get_current_pid_tgid()` 充当 Map 的 Key，把耗时算在当前请求头上。但 Java 虚拟线程为了追求高并发，由 JVM 调度器在用户空间极其频繁地对虚拟线程进行 Mount（挂载）和 Unmount（卸载）。操作系统只看到 Carrier Thread ID 一直没变，但实际处理的业务已经换了八百拨，导致 eBPF 把张三的 I/O 阻塞扣到了李四的头上；
- **为何现有方案不是慢就是错**：已有的 JVMTI 机制开销巨大（引入高达 20% 的运行时代价），且全生命周期无法静默关停；而简单的 eBPF 探针又缺乏对调度瞬态的严谨处理；
- **四探针状态机与堆外 64B 环形槽**：
  1) 在 OpenJDK 内部分配固定的 64-byte 堆外内存槽，作为虚拟线程的随身「数字身份证」；
  2) 设计了严密的 **4-USDT 探针状态机**，不仅捕获 Freeze（冻结）与 Thaw（解冻），更覆盖生命周期销毁，彻底粉碎了业界天真以为「双探针即可搞定」的幻想（论文严密论证了双探针会导致严重且隐蔽的上下文串扰）；
  3) 发现了 OpenTelemetry 规范提案 OTEP 4947 在缓存型 Reader 下的协议漏洞，确立了基于 Valid 标志位的 In-Place 原地改写语义。

3. 关键结论：
- 在合成高压基准测试与真实微服务调用测试中，4 探针架构在内容平面（Content Plane，Trace 上下文完整性）与身份平面（Identity Plane，归属线程唯一性）两项指标上，**全部 768 个复杂测试用例实现 100% 精确归因**；
- 在没有监控消费者挂载的常态静默运行下，每次线程挂载/卸载的附加开销仅为 **~33 纳秒（ns）**，相比 JVMTI 机制每秒数万次切换下高达 20% 的吞吐损耗，本方案对生产业务几乎零感知；
- 彻底解决了生产环境中开启虚拟线程后，微服务全链路监控拓扑图中出现的大量断链、野指针 Span 与串号日志的严重运维灾难。

4. 背景地位：
来自系统评测与可观测性前沿领域的扎实突破。这篇论文深刻揭示了现代高级语言运行时（Java Project Loom、Go Goroutine 等用户态轻量协程）与底层 Linux 内核 eBPF 无侵入监控之间的根本矛盾，为下一代云原生 APM（应用性能监控）标准制定提供了极具说服力的协议修正与工程范本。

5. 落地相关性：
对于在 Kubernetes 生产集群中运维大规模 Java Spring Boot 3.x / Quarkus 微服务网关，同时深度依赖 Cilium、OpenTelemetry eBPF、Pixie 或 Grafana Beyla 进行链路追踪的 SRE 与架构师而言，这是必读的避坑指南。它不仅解释了为何生产开启 Virtual Threads 后链路监控频频诡异报错，更为企业自行修补 OpenJDK 运行时或等待官方吸收 upstream 补丁提供了最精确的架构蓝图。

---

### 其他论文（相关度 ≤2）

本批次其余 56 篇论文主要涉及通用分布式图计算、基础运筹优化、特定行业应用、区块链共识或边缘算法优化，相关度评估为 ≤2 分，按领域归类简列如下：

#### A. 分布式理论、通信与通用性能评测 (cs.DC / cs.PF)
1. **[2611.14741] Reconstructing Fine-grained Memory Reuse Structure in GPU Kernels**: 提出 cuVein 工具，基于拓扑距离与程序计数器依赖图重建 GPU 算子细粒度访存复用结构，重在微架构分析。
2. **[2611.16330] Snoopie: A Multi-GPU Communication Profiler and Visualizer**: 针对多卡通信的分析可视化工具，侧重于 NVLink/网络数据包在时序层面的追踪展示。
3. **[2611.15201] Sparse Matrix Multiplication Exponent 1.5 in the Low-bandwidth Model**: 理论分布式模型下的稀疏矩阵乘法复杂度分析，偏纯理论算法。
4. **[2611.15271] MoE Pretraining: Parallelism Layout Changes the Model, Not Quality**: 探讨 MoE 预训练中不同并行排布对模型内部参数状态变化的实证研究，偏训练动态分析。
5. **[2611.15926] NVIDIA Vera: A Microarchitecture-Level Comparison with Grace, Turin, and Granite Rapids**: 对英伟达下一代 Vera CPU 核心架构与 AMD、Intel 最新旗舰 CPU 的微基准能效评测对比。
6. **[2611.16037] Plurality Consensus for $h$-Majority via First-Repetition Rules**: 分布式系统多值共识协议在重复规则下的理论收敛性证明。
7. **[2611.16302] Smoothed Analysis for Distributed MIS**: 分布式最大独立集（MIS）问题在平滑分析框架下的理论复杂度探讨。
8. **[2611.16290] Parallel Computing Systems for the Optimal Selection of Process Equipment**: 工艺设备选型的并行工程计算系统，偏传统工业制造优化。
9. **[2611.16844] Locality Meets Interference: Structure and Scheduling in Radio Multicasting**: 无线多播网络中的干扰调度与几何局部性算法研究。
10. **[2611.16652] Autonomous Mobile Robots on a Computing Field**: 移动机器人集群在计算场下的分布式几何移动与编队理论模型。
11. **[2611.16155] Accelerating Distributed Variational Quantum Computing over Wireless Networks**: 面向无线量子计算网络中变分量子电路的激励机制设计。
12. **[2611.15032] Instruction-Aware Transfer of GPU Implementation Crossovers**: 在 GB200、H100 和 A100 上分析高阶间断 Galerkin 算子的指令级迁移特性，偏数值计算。
13. **[2611.15615] A Parallel Greedy Algorithm for Maximal b-Matching in Hypergraphs**: 超图中最大 b-匹配问题的并行贪心逼近算法，属经典理论图算法。
14. **[2611.17212] Theoretical and Empirical Analysis of Sparse Convolution**: 稀疏卷积算子的 Roofline 模型理论与边缘硬件实验分析。
15. **[2611.15372] LLMRunner: Closed Workload Model Performance Testing Framework for LLM Servings**: 针对 LLM Serving 的闭环工作负载压测工具，评估 UVM 显存替换 KV Cache 的性能波动。
16. **[2611.16566] Towards Automated Recommendation of Steady-State Detection Algorithms for Benchmarks**: 软件性能基准评测中稳态检测算法的自动推荐框架。
17. **[2611.16889] Control-Flow Profiling for Workload Representativeness**: 控制流剖析在测试用例代表性评估中的有效性研究。
18. **[2611.16376] SPEC CPU2026 Under the Microscope: Programs, Phases, and Samples**: 对下一代 SPEC CPU2026 基准测试集的程序相变与采样行为进行的微架构剖析。
19. **[2611.17206] PACER: GPU Excursion Management for ML Workloads**: 针对机器学习集群中 GPU 电压跌落与功耗突增（Excursion）的硬件级缓解机制。

#### B. 硬件架构、边缘计算与专用内核 (cs.AR / cs.CE)
20. **[2611.14776] SlipStream: Enabling HBF for GPU Systems by Mitigating Latency and SRAM Overheads**: 在 GPU 体系结构中通过缓解延迟和 SRAM 开销支持硬件布隆过滤器（HBF）。
21. **[2611.14545] metalSPARSE: A 2:4 Semi-Structured Sparse GEMV Kernel for Apple Silicon GPUs**: 针对 Apple Silicon GPU 打造的 2:4 半结构化稀疏 GEMV 优化内核。
22. **[2611.15167] AMARA: Compiler-Driven Accelerator Architecture Design for Graphical Probabilistic Sampling**: 编译驱动的图概率采样专用加速器微架构设计。
23. **[2611.15281] Priority-Based Network Access with Strict-Priority Scheduling in PLCA Networks**: 汽车工业以太网 PLCA 多点通信中的严格优先级网络调度机制。

#### C. 区块链、数据库与系统可靠性 (cs.CR / cs.DB / cs.SE)
24. **[2611.14916] CuEVM: Scaling Smart Contract Execution on GPUs**: 在 GPU 上大规模并行执行以太坊 EVM 智能合约交易的加速引擎。
25. **[2611.15847] SoK: Design Choices in Tendermint BFT Consensus**: Tendermint 及 CometBFT 拜占庭容错共识协议设计方案的系统化知识整理（SoK）。
26. **[2611.17184] Omakase: Execution Congestion Control through Conflict-Graph Integration in Blockchain**: 多提议者区块链中基于冲突图集成的并行交易执行拥塞控制框架。
27. **[2611.14962] FIRE: Failure Isolation and Reliability for Production-Connected Experiments at Scale**: 面向大规模生产系统连接实验的故障隔离与可靠性验证架构。
28. **[2611.15441] KernelMutate: Mutation-Guided Validation of Generated GPU Kernels**: 基于变异测试对大模型生成 GPU 算子内核进行正确性验证的工具。
29. **[2611.15506] KernelAudit: Contract-Aware Auditing of Validators for LLM-Generated GPU Kernels**: 针对大模型 GPU 算子验证工具自身的契约感知审计框架。
30. **[2611.16158] PolicySniff: Inferring Agent Policy States through Shared-GPU Execution**: 探讨在多租户 GPU 混部共享时，利用侧信道推测同卡其他 Agent 策略状态的安全性攻击论文。
31. **[2611.16565] Look Here, Then Decide: Small Decision Models Find Memory-Safety Vulnerabilities**: 利用轻量决策模型配合测试框架在开源代码中挖掘内存安全漏洞。

#### D. AI 算法、模型训练与专用应用 (cs.AI / cs.LG / cs.RO / eess / stat)
32. **[2611.15911] Smart Model Routing for Order-of-Magnitude LLM Cost Reduction**: 针对大模型调用的语义路由算法，偏重根据提问难度路由到不同大小的模型以降低 API 账单。
33. **[2611.15842] Fewer Expert Transfers Without Changing Routing: Expert Eviction for MoE Offloading**: 探讨在不修改模型路由权重的前提下，利用最优离线替换策略优化 MoE 专家淘汰算法。
34. **[2611.16248] MegaOps: A Kernel Overlapping Framework with PyTorch-like Modularity and Megakernel Performance**: 康奈尔大学提出的算子重叠框架，通过模块化方式逼近手写 Megakernel 的计算吞吐。
35. **[2611.14969] Scaling VLA Serving Under Robotic Execution Constraints**: 机械臂具身智能场景下视觉-语言-动作（VLA）模型在实时动作循环约束下的服务化系统。
36. **[2611.16301] LoCoJAX: Host-Local Coordination for Small-Model RL on TPUs**: 针对 TPU 上小模型强化学习的高频主机本地协调与通信库。
37. **[2611.14748] UniPipe: Unified Inference Serving and Fine-Tuning for DNN Surrogate Workflows**: 科学计算代理模型中统一推理服务与在线微调的流水线调度系统。
38. **[2611.16543] To Race or Not to Race? Exploiting Performance Variability in Mixed-Integer Programming**: 利用混合整数规划求解器性能波动的自适应算力分配算法。
39. **[2611.14589] CAFIN: CUDA-accelerated Adaptive Fisher Information Matrix Network Optimization**: 基于原生 GPU 内核融合的自适应费舍尔信息矩阵加速网络优化。
40. **[2611.14665] Galop: Billion-Scale Genetic Programming on a Single GPU**: 在单张 GPU 上实现十亿规模遗传算法树进化的计算优化。
41. **[2611.14924] Edge-Native Multimodal RAG: Hardware-Aware Quantization for Consumer GPUs**: 消费级 GPU 上多模态图文检索增强生成的硬件感知量化方案。
42. **[2611.15091] Advancing Weighted Partial MaxSAT Solving via Differentiable GPU Guidance**: 基于可微 GPU 引导的大规模布尔最大可满足性（MaxSAT）问题求解器。
43. **[2611.15111] Speedup-Aware Rounding for Scheduling Malleable Tasks with Precedence Constraints**: 带优先级依赖的可变任务调度中具备加速比感知的舍入逼近算法。
44. **[2611.15153] MatrixSplat: Matrix-Parallel and Feature-Scalable 3D Gaussian Splatting Rendering**: 3D 高斯泼溅渲染的矩阵并行与特征缩放 GPU 渲染优化。
45. **[2611.15246] Dual Representation Enhanced Diffusion Policy for Flexible Job Shop Scheduling**: 柔性作业车间调度中基于双重表征增强的扩散策略生成模型。
46. **[2611.15346] Towards Better Legal Reasoning LLMs: Signal Balancing and Reward Scheduling**: 法律垂直领域大模型强化学习中的奖励函数调度机制。
47. **[2611.15569] TraceKV: Policy-Preserving Low-Rank KV Cache Compression for Reasoning VLMs**: 针对多模态推理大模型的多轮交互 KV Cache 低秩无损压缩算法。
48. **[2611.16422] BlinkMimic: Training a Humanoid Motion Tracker in Minutes on a Single GPU**: 人形机器人全身姿态模仿控制器的单卡极速强化学习训练框架。
49. **[2611.16524] A Joint LLM and Optimization Agent Solution for Drone Scheduling**: 无人机荒野搜救任务中基于大模型与组合优化的任务分配算法。
50. **[2611.16749] ORCA: Orthogonal Residual Consensus Alignment for Multi-View Clustering**: 多视图聚类中正交残差对齐算法，偏计算机视觉模式识别。
51. **[2611.16884] Collision-Resilient All-to-All Broadcast Scheduling in Underwater Networks**: 水下声学传感网络中具备抗碰撞物理层的全对全广播调度。
52. **[2611.17213] Collaborative Task Allocation for Heterogeneous Multi-Robot Systems**: 异构多机器人协同任务分配的迭代聚类启发式方法。
53. **[2611.14529] Clustering Trajectories of Modelled Estimates: Cardiovascular Burden Application**: 心血管疾病负担统计学模型轨迹的聚类不确定性分析框架。
54. **[2611.15270] Communication-Efficient Federated Multi-View Clustering via View-Aware Quantization**: 联邦多视图聚类中自适应视图量化的通信压缩算法。
55. **[2611.16285] Scaling Pêlagos: Multi-GPU Orchestration for Relay Belief-Propagation Decoding**: 量子纠错码（QEC）中基于 AMD MI300X/MI355X 显卡集群的中继置信传播多卡调度仿真系统。
56. **[2611.16484] TAPES: Terminal Adjoint-Propagated Error Scheduling for Financial Diffusion Samplers**: 金融衍生品风险定价中扩散采样器终端伴随误差调度算法。

---

### 今日趋势小结

纵观今日 2026-11-13 的全部 68 篇系统方向前沿文献，我们可以清晰地捕捉到系统界正在经历的**四大底层范式变革**：

1. **AI 基础设施迈入「芯片内微架构级空间并行」与「去 HBM 化机架级光互联」的两极演进**：
   - 过去两年，AI Infra 的重心主要放在集群级粗粒度切分（Tensor/Pipeline/Data Parallelism）。但随着单芯片算力与芯片封装面积逼近物理极限，今日文献展现出清晰的纵深分化：
   - **微观向下扎根（Intra-GPU Spatial Pipelining & Chiplet NUMA）**：英伟达官方团队关于 Blackwell B200 的 SubGPU Pipelining 与 AMD 官方团队关于 MI300X/MI355X 的 Starscream 表明，顶尖厂商正在将传统操作系统的进程/线程空间切片思想（如 CUDA Green Contexts）深植于单 GPU 内部，以空间流水线平滑微秒级算子的访存与算力饥饿；
   - **宏观向上跃迁（Optical Broadcast Memory）**：乌普萨拉大学的 OBM 系统则从数据中心顶层彻底颠覆传统思维——不再让数万台服务器各自采购几百 GB 昂贵 HBM 存储重复的模型权重，而是通过集中式连续单向光广播，让无状态的轻量推理节点搭光纤便车执行计算，展现了后 HBM 时代极具想象力的机架级蓝图。

2. **Serverless 与冷启动的破局焦点从「镜像传输」转向「执行栈预热与机架级池化共享」**：
   - KAIST 与 SK 海力士打造的 Cairn 论文揭示了一个极具震撼力的技术事实：大模型冷启动中仅 5%~11% 的耗时是权重搬运，真正的大头是 Python 库加载、CUDA 初始化与模型编译；
   - 这一发现为云原生平台架构师敲响了警钟：单纯依靠镜像加速、P2P 分发或高速只读网络存储已经触碰到天花板。未来的 Serverless 容器运行时必须与大模型引擎紧密联动，依托 Zygote 模板进程实现基座即时衍生，并借助 CXL 等机架级低延迟内存池实现跨节点编译缓存与显存探测结果的就地共享，才能真正跨越「冷启动秒级化」的鸿沟。

3. **大模型推理从单次交互走向长链 Agent，批处理 Makespan 与前缀缓存成为第一系统指标**：
   - 随着大模型全面进阶为 Coding Agent 与复杂工作流智能体，推理系统的优化维度正在从单请求的首字时延（TTFT）与吞吐量，演变为整个研发流水线的批处理总耗时（Batch Makespan）与长尾治理；
   - 蚂蚁集团 Ling 团队的 CAAS 关键链路推进调度、加州大学圣克鲁兹分校在 SGLang 上的单请求多流 Parallel Prompting，以及高丽大学针对静态图 NPU 的 Host-Tier KV 桥接器，从不同切入点揭示了同一个真理：智能体在多轮迭代中存在海量共享的前缀上下文与漫长的工具调用交互；只有在调度层对齐关键链路、在执行层通过 Stream-ID 掩码实现单次读取共享 KV、在存储层平滑换入换出，才能彻底粉碎由于频繁前缀击穿导致高达 90% 算力沦为重复 Prefill 的灾难。

4. **微内核、轻量沙箱与用户态轻量调度，倒逼底层可观测性与安全编排全栈重构**：
   - 在端侧与沙箱安全领域，上海交大与阶跃星辰的 Metal Sandbox 证明了为自主生成可执行代码的 Agent 构建安全隔离沙箱与分布式任务迁移机制的绝对必要性；
   - 与此同时，纽卡斯尔大学关于 Java 21 虚拟线程在 eBPF 监控下静默失效的深入剖析，更是给所有云原生运维工程师上了生动的一课：当现代语言运行时在用户态大行其道搞 $M:N$ 协程/纤程调度时，内核与底层操作系统必须建立极其精密的微型上下文通信协议（如 4 探针状态机与堆外共享描述符），才能在零运行时惩罚的前提下维系系统的可观测性生命线。
