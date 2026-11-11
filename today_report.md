## arXiv 系统方向日报 · 2026-11-11

### 今日概览

今日系统方向（cs.DC / cs.OS / cs.PF 及相关交叉领域）共抓取 97 篇候选论文。经过资深系统调研体系的严格筛选与多维度评分，本次**入选深读：12 篇**（其中 6 篇评分为 5 分的核心突破论文，6 篇评分为 4.5 分的高价值系统论文），其余 85 篇理论或边缘交叉论文归入文末列表。

今日文献呈现出极具震撼力的「云原生容器/编排机制与 AI Infra 底层硬件架构全链路向纵深演进」的特色：从 Kubernetes 生产级镜像懒加载（Lazy Pulling）导致的致命探针欺骗与 kubelet 误驱逐机理剖析，到 LinkedIn 生产环境基于同质底模与零显存 Standby Pod 的微秒级 GPU 容量中介系统 Firepool；从 NVIDIA 官方在 GB300 NVL72 机架系统上针对 NCCL-EP 通信计算双批重叠（DBO）的描述符硬件卸载，到多租户 RDMA 网络在商用 ConnectX-6 网卡上的用户态控制面隔离机制 MTRDMA；从 UC Berkeley 与 MIT 针对智能体大模型推理服务构建的算力/KV Cache 解耦动态自适应框架 Evolving Infra，到 NVIDIA 官方重构 NCCL 静态开销模型、引入在线多臂老虎机闭环调优的 NCCL-BOT。无论是容器运行时、K8s 调度编排、高性能网络，还是分布式训练与推理，技术体系正在经历前所未有的全栈系统级协同。

今日必读：
1. **Lazy-Pulling Impossibility**: 揭示 Kubernetes 与 stargz/SOCI/Nydus 镜像按需拉取在模型服务化中的两大不可行性，提出不改 CRI 的零误差硬约束缓存治理方案。
2. **Firepool**: LinkedIn 生产级 H200 集群热 GPU 容量代理框架，通过同质底模与零显存 Standby 占位 Pod 将 Agent/RL 启动延迟从 59s 骤降至 3.5s。
3. **MoE Dispatch Offloading**: NVIDIA 官方团队在 GB300 NVL72 上的 NCCL-EP 突破，通过 GPU-Friendly Descriptors 与 CPU 线程卸载消除双批流水线裸露通信，提升 vLLM 吞吐达 42%。
4. **MTRDMA**: 湖南大学提出轻量级多租户 RDMA 控制面隔离方案，利用原子共享内存与 rdma-cgroup 消除吵闹邻居对网卡微架构缓存的耗尽，保护容器吞吐。
5. **Evolving Infra**: UC Berkeley 与 MIT 等联合推出 Agent 自适应大模型服务化框架，在 256 卡 GB300 集群上实现算力分配与 KV Cache 解耦自适应，P95 首字延迟降低 14 倍。
6. **NCCL-BOT**: NVIDIA 集合通信团队重构 NCCL 静态开销模型，以在线多臂老虎机（MAB）动态闭环实测延迟，攻克拓扑与拥塞下的次优通信算法选择难题。
7. **The Storage View Of KV Cache**: UT Austin 与 IBM 联合对 11 类生产负载的底层 KV Cache 展开存储行为刻画，提出跨单/多会话的精简 3 信号存储管理抽象。
8. **Relief**: 香港大学与香港科大研发的专家并行 MoE 逐步实时负载均衡引擎，打破传统线性规划求解瓶颈，以 CUDA 算子及片上硬件块恢复 37.3% 的算力利用率。
9. **OOM-MoE**: 香港科技大学（广州）针对全参数 MoE 训练的内存-执行协同卸载框架，通过参数预取流水线与显存复用极大降低跨互连传输等待。
10. **Custom GPSIMD on Trainium**: UCLA 丛京生团队针对 AWS Trainium 3 构建首个 C++ 自定义 GPSIMD 算子编译工具链，加速 DeepSeek-V4.1 Engram 稀疏检索。
11. **AdaOffload**: UC Berkeley Sky Computing 团队打造的异构多 GPU 混合专家卸载推理系统，全链路 NUMA 感知调度使超大 MoE 吞吐提升最高 15.5 倍。
12. **Wasm Edge Cold-Start**: 根特大学-imec 研发的 WebAssembly 边缘调度器，联合优化产物缓存局部性与网络路由距离，降低边缘端到端冷启动延迟 40.8%。

---

### 逐篇解读

#### 1. Why Kubernetes Cannot Contain a Full Lazy-Pulling Cache: Two Impossibility Results and a Bounded, Honest Design for Model Serving
- 中文译名：为什么 Kubernetes 无法遏制镜像按需拉取缓存失控：两大不可行性定理与面向大模型服务化的有界诚实设计
- 链接：https://arxiv.org/abs/2611.11739
- 作者：Georgii Kliukovkin
- 单位：独立研究（前系统研究人员 / 独立研究员，Sunnyvale, CA）
- 分类：cs.DC, cs.OS, cs.PF
- 方向标签：A. 容器与运行时 (镜像按需拉取 / stargz / SOCI / Nydus) & B. 编排与调度 (Kubernetes / kubelet 驱逐机制)
- 相关度：5/5

1. 核心贡献：
深入揭露了在大规模 Kubernetes 集群中采用容器镜像懒拉取（Lazy-Pulling，如 stargz-snapshotter、AWS SOCI、Nydus 等）部署大模型推理服务时的一类结构性致命故障，并在真实云环境下实证了两大「不可行性结果（Impossibility Results）」：
- **监控端不可行性（Monitoring-Side Impossibility）**：当节点级快照缓存占满时，Pod 的哨兵就绪探针（Readiness Probe）仍显示为绿色（正常），但实际上容器内 280 个模型权重文件中已有 272 个因缓存写入失败而无法读取；
- **平台端不可行性（Platform-Side Impossibility）**：即使 kubelet 察觉到了磁盘压力（DiskPressure），其垃圾回收动作也无法释放该缓存任何 1 个字节，反而会错误驱逐 26 个无辜的旁观者 Pod（Bystander Pods），因为平台内置的账本根本不知道底层快照缓存的存在。
针对此痛点，作者提出了完全在持有字节的快照驱动内部修复的有界诚实设计（Bounded, Honest Design）：通过基于物理文件系统真实状态的有损字节预算（Lossy Byte Budget）和透传语义（Pass-Through Semantics），在不改动 kubelet 和容器运行时接口（CRI）的前提下 100% 根治此问题。

2. 原理解析：
为了让几百 GB 的大模型镜像在 Kubernetes 上秒级拉起，业界广泛使用 eStargz、SOCI 或 Nydus 进行按需分块拉取（Lazy-Pulling）。但整个云原生体系的控制面与数据面在此处产生了严重的断层：
- **探针欺骗**：探针（如 HTTP `/healthz`）往往只探测模型的加载脚手架或少量预热权重，而模型几百个权重切片（Chunk）在后续业务推理时才会真正流式拉取。当宿主机本地快照卷写满时，底层文件系统读取抛出 I/O 错误，但探针因无法遍历全部深层权重而持续上报 Healthy，导致故障 Pod 持续接收线上流量并全面报错；
- **kubelet 账本脱节**：kubelet 监控磁盘空间时，仅统计容器可写层（`/var/lib/containerd` 下的 rw layer）与 emptyDir 临时卷。而快照驱动（Snapshotter）将拉取的解压块保存在其独立的专用目录。当快照缓存将物理磁盘撑爆触发 `DiskPressure` 时，kubelet 按照自身账本寻找受害者，回收快照缓存 0 字节，却判定同节点上其他正常运行微服务的 Pod 超额并予以驱逐杀死；
- **io.MultiWriter 耦合致命反噬**：快照驱动普遍使用 Go 语言的 `io.MultiWriter`，将网络下载的 chunk 同时写入上层读取流和本地磁盘缓存。一旦磁盘写失败，`io.MultiWriter` 立即向读取端返回错误，导致本应可以由网络直接透传给容器的读操作彻底崩溃。
作者的破局之道在于重构快照层：将缓存写入与读取彻底解耦为透传语义（写缓存失败绝不阻塞读数据流），并以物理文件系统的实际空闲水位作为预算门控，丢弃锁竞争换取高吞吐，牢牢锁死硬上限。

3. 关键结论：
在 AWS 上的 6 项严格预设压测中，针对 150.3 GB 的大模型权重镜像，在上游 stargz-snapshotter 缓存预充 90% 的场景下，原生实现由于磁盘超额导致 273/280 个模型文件读取彻底崩溃；而本文提出的有界诚实系统在三节点集群共存负载下实现了 0 读取错误、成功读取全量 150.3 GB，仅付出 18.5% 的尾部执行耗时代价，并成功经受住了 SOCI 与 Nydus 的跨实现源码审计，已向上游开源社区提交 PR。

4. 背景地位：
这是对当前大模型弹性推理与 Serverless 容器冷启动热点技术的一次极具穿透力的底层安全审查。它推翻了业界长期认为「只需配置好 Snapshotter 就能高枕无忧享受秒级冷启动」的经验主义假象，是近两年云原生存储与容器运行时领域极少见的软硬件现象级实证研究。

5. 落地相关性：
对于在 Kubernetes 上维护 vLLM、Triton、Ollama 等弹性伸缩推理集群的云原生基础设施团队而言，本论文是极其宝贵的生产避坑指南。直接指导实践：1) 绝不能仅靠简单 HTTP `/healthz` 作为模型就绪探针；2) 必须防范快照缓存占满触发 kubelet 误杀无辜 Pod；3) 可直接采用该作者开源补丁加固 snapshotter 插件。

---

#### 2. Firepool: Brokering Warm GPU Capacity for Agentic and RL Workloads at LinkedIn
- 中文译名：Firepool：针对 LinkedIn 智能体与强化学习负载的热 GPU 算力容量中介系统
- 链接：https://arxiv.org/abs/2611.10832
- 作者：Ankit Goyal, Santosh Jha, Zhuo Zhi, Youmin Han, Cong Gu, 等（共 7 位作者，通讯作者：Ankit Goyal）
- 单位：LinkedIn（领英 / 【工业界】）
- 分类：cs.DC, cs.LG
- 方向标签：B. 编排与调度 (GPU 集群容量管理 / Pod 预热与复用) & C. AI Infra (Agentic 与 RL 训练系统)
- 相关度：5/5

1. 核心贡献：
针对 LinkedIn 内部日益爆发的 AI Agent（工具调用/代码沙箱）与强化学习（RL rollout 采样）任务中，海量超短生命周期作业（通常几秒钟跑完，但启动一个全新 GPU Pod 即使本地有镜像缓存也要 20-35 秒，冷镜像甚至数分钟）引发的极度开销与空转延迟，设计并上线了 LinkedIn 生产级 GPU 容量代理中介框架 Firepool。在不长期浪费昂贵 GPU 显存的前提下，将短任务启动延迟从原本数十秒削减至毫秒级。

2. 原理解析：
在云原生集群中，传统调度就像买火车票：哪怕乘客只坐一站地（几秒钟的 Tool Call），也必须经历完整的「Pod 声明 -> 调度器判定 -> CRI 容器拉起 -> GPU 驱动初始化」，整个端到端流程耗时半分钟以上，导致整个 Agent/RL 推理训练闭环中有 80% 以上的时间在等 Pod 冷启动。
Firepool 提出了三大核心创新：
- **可互换热 Pod（Interchangeable Pods）**：按硬件规格预先拉起共享同质基础镜像的 Pod 池，在具体任务派发时再将代码、动态依赖及集群通信拓扑热挂载注入，避免业务镜像碎片化；
- **零显存待机 Pod（Zero-VRAM Standby Pods）与同源复用**：已完成任务的 Pod 会被优先保留给同一调用方进行零等待复用。更关键的是，利用分数 GPU（Fractional GPU share）机制在活跃 Pod 旁边部署零显存占用的 Standby Pod，一旦主 Pod 释放或新任务涌入，直接以 0.94 秒完成 Standby 升格，完全绕开容器创建阶段；
- **队列驱动的动态预算（Queue-Driven Budgets）**：通过监控各任务排队深度实时调整预热池配额，并在智能体多轮会话之间采用匹配停顿间隔的 Keep-Alive 机制，仅占用不到一半的显存即可达到全量热池的极低延迟。

3. 关键结论：
在 LinkedIn 生产环境 H200 GPU 节点集群的实际峰值周期中，Firepool 成功支撑了 94.7% 的 Pod 请求（共 3206 个请求样本）直接由热池或 Standby 容量即刻满足。Agent 和 RL 闭环执行速度相比每任务新建 Pod 提升了 10.8 到 13 倍；P90 启动延迟从 59.1 秒断崖式削减至 3.5 秒；备用 Pod 升格仅耗时 0.94 秒。

4. 背景地位：
大厂在大模型 AI Agent 与强化学习后训练（如 DeepSeek-R1、OpenAI o1 类长思考链探索验证）时代面临的真实系统工程痛点。将 Serverless 容器预热技术下沉并适配至高成本的 GPU 加速器集群调度与显存拓扑中，是生产级工业实践的典范。

5. 落地相关性：
对于搭建智能体执行沙箱、大模型强化学习探索环境的平台团队极具借鉴意义。在 Kubernetes 上结合动态挂载与分数 GPU 共享，能直接帮助企业节省数以百万元计的闲置 GPU 算力账单，并大幅加速 Agent 业务端到端流转。

---

#### 3. Release Sooner, Expose Less: Offloading MoE Dispatch in NCCL-EP under Dual-Batch Overlap
- 中文译名：更早释放、更少裸露：双批流水线重叠下卸载 NCCL-EP 的 MoE 调度发送通信
- 链接：https://arxiv.org/abs/2611.12362
- 作者：Hsin-Chun Yin, Khaled Hamidouche, Ian Ziemba, Arjun Kashyap, Pak Markthub, 等（共 10 位作者，通讯作者：Khaled Hamidouche / Gil Bloch）
- 单位：NVIDIA（英伟达官方网络与系统团队 / 【工业界】）
- 分类：cs.DC
- 方向标签：C. AI Infra (集合通信 / NCCL-EP / MoE 推理系统 / 通信与计算重叠)
- 相关度：5/5

1. 核心贡献：
针对大模型 MoE 专家并行（EP）服务中核心的双批重叠技术（Dual-Batch Overlap, DBO：让一个微批次的计算掩盖另一个微批次的通信），指出了一个关键盲区——**Dispatch Send（调度发送端）必须先释放 GPU SM 资源，后续的网络传输进度才能真正与另一个 Batch 的计算实现隐藏重叠**。在这段发送释放期间，GPU SM 被困在网络打包装包中，这部分耗时是完全暴露（Exposed）在关键路径上的！
NVIDIA 团队基于最新 GB300 NVL72 机架系统与 NCCL-EP 展开了前沿研究，提出了三种突破性配置：GPU 友好描述符（GPI）、支持单描述符多播的 GPI-MC，以及将发送推进彻底卸载到主机线程的 GDAKI Free Flow。

2. 原理解析：
这就好比在流水线工厂中，搬运工（GPU SM）要把货物打包并通过快递（RDMA 网卡）发给其他专家车间。在过去，搬运工不仅要自己写每一个包裹的详细快递单，还要一直在邮筒前等确认，导致搬运工无法抽身去干下一批装配工作：
- **GPU 友好描述符（GPI）**：GPU 不再深陷底层复杂协议，直接生成极轻量的 GPU-Friendly Descriptors (GFD) 写入 NIC 可直接访问的内存，瞬间打包装载完成，GPU 提前脱身；
- **GPI-MC（Multicast Token Fan-out）**：针对 MoE 中一个 Token 可能被路由给多个专家的特性，用一个单一 GFD 描述整个 Token 扇出（Fan-out），极大减少控制开销；
- **GDAKI Free Flow（Host Thread Offload）**：将网络发送进度的推进彻底移交给 CPU Host 线程，GPU SM 只管提交请求即可立即返回，从而将裸露在外部的串行开销压缩到极致。

3. 关键结论：
在 GB300 NVL72 系统的全参数评测中，这三种方案在绝大部分工况下均显著削减了 Dispatch Send 占用时间。在解耦式 vLLM 推理服务结合 DBO 的场景下，相比 NCCL-EP 默认的 GDAKI 配置，中位数 TPOT（每 Token 生成耗时）降低了 15%~25%；相比业界知名的开源通信库 DeepEP v1，中位数 TPOT 降低了 16%~42%！

4. 背景地位：
来自 NVIDIA 官方核心通信架构团队（负责 NCCL-EP、NVLink 与 GB300 硬件协议的核心成员），直击 Blackwell / GB300 时代 MoE 专家并行通信与计算重叠的底层微架构瓶颈，代表了当前 AI 芯片机架级集合通信的最高技术水平。

5. 落地相关性：
对从事大模型分布式训练与 vLLM/SGLang 生产级推理服务的底层性能优化团队是重大指引。特别是针对 DeepSeek-V3/R1 等具有高专家扇出和细粒度路由的大模型，如何通过描述符轻量化与主机线程卸载隐藏通信开销，将直接决定推理吞吐的上限。

---

#### 4. MTRDMA: Lightweight User-Space Control-Plane Isolation for Multi-Tenant RDMA
- 中文译名：MTRDMA：面向多租户 RDMA 的用户态轻量级控制面隔离机制
- 链接：https://arxiv.org/abs/2611.11991
- 作者：Hongyu Wang, Peihao Huang, Bangbo Liang, Lei Wang, Guo Chen（通讯作者：Guo Chen）
- 单位：湖南大学（网络与信息安全研究所）
- 分类：cs.NI
- 方向标签：A. 容器与运行时 (命名空间与资源隔离 / rdma-cgroup) & B. 编排与调度 (多租户云原生网络) & C. AI Infra (高性能 RDMA 通信)
- 相关度：5/5

1. 核心贡献：
揭露了公有云与多租户 Kubernetes 集群中 RDMA 基础设施的一个致命安全与性能漏洞：**RDMA 缺乏控制面（Control-Plane, CP）资源隔离**！一个恶意或有缺陷的「吵闹租户（Noisy Tenant）」可以通过频繁创建 Queue Pair (QP) 或注册 Memory Region (MR)，恶意耗尽商用 RDMA 网卡（RNIC）共享的片上微架构缓存，导致同宿主机上的其他受害租户的网络吞吐暴跌高达 96.4%！
提出了首个面向商用标准 RNIC（如 Mellanox/NVIDIA ConnectX-6）的轻量级用户态控制面隔离机制 MTRDMA，能在容器和沙箱进程中无缝运行。

2. 原理解析：
在云原生集群中，Kubernetes 可以通过 cgroups 限制 Pod 的 CPU 和内存，数据面调度器也可以通过 DSCP/PFC 限制网络带宽。但是商用 RDMA 网卡为了追求零拷贝与超低延迟，绕过了操作系统内核，直接向用户态暴露了硬件资源。
当一个恶意的 Pod 像疯狂发垃圾邮件一样拼命注册连接（QP）和内存（MR）时，网卡内部的缓存（类似 CPU 的 L1/L2 Cache）瞬间被撑爆。其他正常的推理/训练 Pod 要发包时，网卡必须频繁发生 Cache Miss 去翻系统内存，导致网速直接归零。
MTRDMA 的解决方案：
- **用户态库级拦截与分层配额**：拦截 `libibverbs` 中的控制面调用，在用户态利用原子共享内存维护配额，单次准入判定仅需约 0.13 微秒，完全不侵入零拷贝数据通路；
- **混合垃圾回收器（Hybrid GC）**：在秒级时间内自动回收崩溃或孤儿进程占用的残留配额；
- **内核-账本双向对账机制**：结合 Linux 原生的 `rdma-cgroup` 配额上限，在底层进行内核与用户态账本的审计对账，彻底封堵绕过篡改的可能。

3. 关键结论：
在 ConnectX-6 RNIC 真实测试环境中，MTRDMA 在发生 QP 缓存耗尽攻击时，将受害租户的吞吐降幅从原本惨烈的 94.5% 几乎抹平至仅 0.08%！并且全面保护了 MR 缓存，能够轻松线性扩展至 256 个并发租户，对数据平面的延迟与吞吐开销完全可以忽略不计。

4. 背景地位：
补齐了云原生高性能网络中长期缺失的一块关键拼图。传统方案要么放弃性能走内核代理，要么强依赖定制 FPGA 或 SmartNIC 硬件；MTRDMA 首次在现有存量商用硬件上，以纯纯的软件工程化设计兼顾了零拷贝性能与严格的多租户安全性。

5. 落地相关性：
对于在 Kubernetes 裸金属集群上提供多租户 RDMA（如企业内多算法团队混跑、公有云 GPU/RDMA 容器实例）的云平台架构师是必配的核心技术，能极大提升集群多租户隔离的健壮性，防止单点故障扩散。

---

#### 5. Evolving Infra: Agent-Adaptive LLM Serving at Scale
- 中文译名：Evolving Infra：面向大规模智能体动态负载的自适应大模型服务化框架
- 链接：https://arxiv.org/abs/2611.12304
- 作者：Hao Kang, Weili Xu, Ziyang Li, Zheng Du, Hanchen Li, 等（共 11 位作者，通讯作者：Hao Kang，共同指导：Ion Stoica, Song Han）
- 单位：佐治亚理工学院、伊利诺伊大学香槟分校、加州大学伯克利分校（Sky Computing Lab / 【知名实验室】）、英伟达（NVIDIA / 【工业界】）、OpenAI（【知名实验室】）、麻省理工学院（MIT / 【知名实验室】）
- 分类：cs.DC
- 方向标签：C. AI Infra (推理服务 / Prefill-Decode 分离 / KV Cache 动态分层 / Agentic 负载)
- 相关度：5/5

1. 核心贡献：
由加州大学伯克利分校 Ion Stoica、MIT 韩松团队等联合巨献！针对 AI Agent 业务（如 SWE-bench 编码智能体、复杂工具调用、多步推理规划）成为当前大模型推理主力负载后，现有的静态 Prefill-Decode (PD) 分离架构因缺乏运行时算力重配与 KV Cache 感知能力，导致严重算力失衡与高价值跨轮次 KV Cache 频繁误逐出的痛点，推出了首个面向大规模 Agentic 负载的自适应推理服务框架 Evolving Infra。

2. 原理解析：
在传统服务中，推理节点往往被静态划分为「Prefill 专职工人」和「Decode 专职工人」。但智能体的工作模式极其极端：先抛出一段超长代码（超大 Prefill），然后可能只输出一两个 Token 的工具调用指令（微小 Decode），接着等待工具执行，然后再送入几万字的执行报错（又一次大 Prefill）。
静态切分会导致：要么 Prefill 队列塞爆、Decode 节点望眼欲穿；要么 Agent 多轮对话之间由于等待过久，显存不足而把刚算好的几十 KB KV Cache 错误逐出，下次再来时只能被迫重新全量 Prefill！
Evolving Infra 的破局点在于：
- **算力与 KV Cache 管理解耦**：节点可以在 Prefill 和 Decode 角色之间极速动态切换，通过共享主机内存与快速移交机制，不再有刚性角色绑定；
- **在线全局规划器（Online Planner）**：动态监控当前所有智能体任务的到达率与阶段，实时调整 Prefill 与 Decode 的算力比例；
- **Agent 感知的分布式 KV 缓存管理器**：直接对接智能体工作流的上下文生命周期信号。如果一个分支正处于多路分支推演（Branching），其共享前缀会被牢牢锁定；当分支合并或任务结束时，主动通知释放，彻底打破传统只看 LRU/LFU 的盲目缓存淘汰。

3. 关键结论：
在配备多达 256 卡 NVIDIA GB300 GPU 的真实大规模集群上，针对 GLM-5.2 与 Kimi K2.6 模型，在覆盖真实代码生成、数学求解与复杂电脑操作（Computer-Use）的智能体场景下：Evolving Infra 相比 NVIDIA 官方生产级服务框架 Dynamo，将平均端到端请求延迟降低了高达 4.1 倍，将 P95 关键指标 TTFT（首字延迟）降低了整整 14 倍！

4. 背景地位：
大模型服务化进入 Agentic 时代以来的旗舰级标杆成果。汇集了来自 Sky Computing Lab、MIT HAN Lab、OpenAI 与 NVIDIA 的顶尖系统学者，将 PD 分离从「静态粗粒度切分」推进至「全动态自适应与应用语义感知」的崭新维度。

5. 落地相关性：
对在生产环境中维护 vLLM、SGLang、Triton 服务集群，尤其是承接 Coding Agent、智能体沙箱平台的高并发 AI Infra 工程师具有极高的工程落地与架构重构指导价值。

---

#### 6. NCCL-BOT: Closing the Loop on NCCL's Cost Model with Online Bandits
- 中文译名：NCCL-BOT：基于在线多臂老虎机实现 NCCL 集合通信开销模型的动态闭环优化
- 链接：https://arxiv.org/abs/2611.11303
- 作者：Hanan Shteingart, Amedeo Sapio, Chen Avin, Devendar Bureddy, Manjunath Gorentla Venkata, 等（共 10 位作者，通讯作者：Hanan Shteingart）
- 单位：NVIDIA（英伟达官方分布式网络团队 / 【工业界】）、本·古里安大学、以色列理工学院（Technion / 【知名实验室】）
- 分类：cs.DC, cs.LG
- 方向标签：C. AI Infra (分布式训练 / 集合通信 / NCCL 算法选择) & D. 性能与可靠性
- 相关度：5/5

1. 核心贡献：
针对长期作为 NVIDIA GPU 分布式通信行业基石的 NCCL（NVIDIA Collective Communications Library）中一个隐蔽而巨大的系统痛点展开手术：**NCCL 在为每次集合通信（如 AllReduce、AllToAll）选择具体的算法（Ring 环形 vs Tree 树形）与传输协议（Simple、LL、LL128）时，完全依赖一个纯静态的解析开销模型（AUTO）**。该模型在出厂时写死，从未在运行时测量过哪怕一次真实的通信延迟！一旦遭遇网络拥塞、硬件变异或非对称拓扑，静态模型就会做出严重次优的决策，导致分布式训练遭遇通信暴跌。
NVIDIA 团队历经长达 46 页的详实系统论证与工程实测，发布了首个真正闭环的动态调优系统 NCCL-BOT，通过在线上下文多臂老虎机（Online Bandits）实现了通信决策的实时自适应。

2. 原理解析：
这就像 Kubernetes 的静态调度器，调度时只看 Pod 申请的 Request/Limit，却从来不看当前节点的实际物理 CPU 温度与网卡拥堵。NCCL 的 `AUTO` 也是如此，拿着一张固定的公式表直接钦定走 Tree 还是 Ring。
NCCL-BOT 的工作机制：
- **保留强先验（Strong Prior）**：不抛弃原有开销模型的物理数学优势，将其作为贝叶斯探索的先验起点，避免早期随机尝试带来的性能崩塌；
- **轻量在线探索与测量**：在极少数通信步中引入受控的臂探索（Arm Exploration），并将实测的往返耗时动态反馈给强化学习代理；
- **安全自适应收敛**：能够在短时间内快速识别出由于物理网络链路抖动、多租户干扰造成的实际瓶颈，并自动切换至当前环境下真实的最佳传输协议组合。

3. 关键结论：
论文提供了 46 页、13 个详尽测试图与 38 张完整对比表格的惊人工程量。在涵盖不同规模的 GPU 真实训练集群上，NCCL-BOT 彻底闭环了此前静态解析模型带来的高达 30%~50% 的偶发通信退化，在多工作负载下均实现无缝稳态收敛，且自身引入的在线决策开销完全被隐藏在 GPU 流水线气泡中。

4. 背景地位：
NVIDIA 集合通信官方团队对自身核心基础设施的核心级反思与技术重构。集合通信算法选择终于从「盲目的静态公式推导」走向了「在线测量驱动的闭环控制」，是分布式通信系统的一大标志性跃迁。

5. 落地相关性：
对于运维大规模千卡/万卡 GPU 训练集群、经常遭遇 NCCL 通信变慢却无从定位（到底是网线坏了还是算法选错了）的 Infra 运维与性能调优工程师而言，此项技术的落地将直接从底层消除通信抖动，为长周期大模型训练保驾护航。

---

#### 7. The Storage View Of KV Cache: Characterizing Cache Behavior Across LLM Workloads
- 中文译名：从存储视角审视 KV Cache：跨多样化大模型负载的缓存行为深度刻画
- 链接：https://arxiv.org/abs/2611.10178
- 作者：Talia Q. Chen, Daniel Waddington, Narangerelt Batsoyol, Vijay Chidambaram（通讯作者：Talia Q. Chen）
- 单位：德克萨斯大学奥斯汀分校（UT Austin / 【知名实验室】）、IBM Research（【工业界】）
- 分类：cs.OS, cs.PF
- 方向标签：C. AI Infra (推理系统 / KV Cache 分级存储) & D. 性能与可靠性 (存储行为建模)
- 相关度：4.5/5

1. 核心贡献：
由文件系统与存储系统领域泰斗 Vijay Chidambaram 团队与 IBM Research 联袂完成。指出当今大模型推理服务迫于显存容量压力，正加速将 KV Cache 从 GPU HBM 延伸至宿主机 DRAM、本地 NVMe SSD 乃至远程存储中；然而，现有的底层存储管理却极度原始，依然粗暴照搬对大模型语义毫无认知的通用策略（如传统 LRU 或固定过期时间 TTL）。
本篇论文首次从纯粹的操作系统与系统存储视角，对涵盖聊天（Chat）、API 服务、RAG 检索增强、代码智能体（Coding Agents）、工具智能体以及多分支工作流等 **11 个生产级与开源真实负载 Traces** 进行了细粒度 Block 级别的存储行为全面量化剖析。

2. 原理解析：
这就好比操作系统管理物理内存分页，如果调度器只看页面的最后访问时间，把刚刚还在打代码的用户的关键上下文一股脑 Swap 进磁盘，就会产生剧烈的抖动。
研究揭示了大模型 KV 状态的本质双形态：
- **单会话状态（Single-session state）**：只在单次执行生命周期内复用，随着对话深度线性膨胀，并在并发会话中叠加。它在长时间空闲（如等待用户输入或工具执行）期间仍具极高价值，但在会话结束的一瞬间价值暴跌至零！
- **多会话状态（Multi-session state）**：跨同类负载的多个独立会话反复出现，寿命远超单次会话。它既包含极其热门的系统提示词（Hot Prefixes），也包含拖着长长尾巴的低频上下文。
论文证明，根本无需把复杂的模型/应用层专有语义塞进底层存储引擎，只需抽象出极为精炼的 **3 个通用控制信号**：
- `Workload ID`（负载标识符）
- `Session ID`（会话标识符）
- `Session Completion`（会话结束显式通知）

3. 关键结论：
基于真实 Trace 驱动的模拟对比表明：仅凭负载专有重复率预估即可增加 22% 的会话内命中并减少 40% 的无效死状态占用；引入「会话结束信号」直接消除了单会话状态在空闲期保留与回收之间的死锁权衡；而感知会话的复用分类器筛选共享状态的选择性比传统请求级计数器精准 **4 到 700 倍**！

4. 背景地位：
大模型存储分层（Hierarchical KV Storage，如 Mooncake、LMCache、vLLM PagedAttention 分级扩展）在底层存储体系结构与 OS 交互层面的重磅理论奠基之作。为学术界与工业界制定统一的跨层存储契约提供了极具说服力的实证依据。

5. 落地相关性：
对于在 Kubernetes 上基于 CSI 挂载高性能本地 NVMe 盘、搭建大规模 KV Cache 共享存储池与内存分层架构的平台工程师，提供了清晰直接的系统设计准则：只要在 API 网关处透传会话生命周期信号，即可在底层存储换取数倍的命中率提升与容量释放。

---

#### 8. A Per-Step Load-Balancing Engine for Expert-Parallel MoE Serving
- 中文译名：Relief：面向专家并行 MoE 推理的逐步实时负载均衡引擎
- 链接：https://arxiv.org/abs/2611.11402
- 作者：Jingyuan Li, Maolin Wang, Hayden So
- 单位：香港大学（The University of Hong Kong / 【知名实验室】）、香港科技大学
- 分类：cs.DC, cs.PF
- 方向标签：C. AI Infra (推理服务 / 专家并行 MoE 调度 / 硬件加速引擎)
- 相关度：4.5/5

1. 核心贡献：
针对专家并行（Expert Parallelism, EP）大模型推理中的顽疾——**动态路由造成的专家负载严重不平衡（Expert Load Imbalance）**。在拥有多副本热门专家的集群中，为了将硬件利用率推向极致，理论上必须在 Decode 阶段的**每一步、每一层**，根据当前各个副本上的 Token 分配做最优再分配调度；然而，求解该最优解所需的线性规划（Linear Programming, LP）算法耗时甚至超过了神经网络层本身的计算时间，且状态空间极大，直接超出了 GPU 共享内存（SRAM）的容量。
作者提出了 Relief：一种基于双向成对松弛（bidirectional pairwise relaxation）的轻量级负载均衡算法，仅需对 Token 计数做几轮整数对半迭代即可无限逼近全局最优解，并落地了 GPU CUDA 算子与芯片级专用硬件块。

2. 原理解析：
这就像 Kubernetes 集群里的多副本 Pod 负载均衡：如果有几百个微型任务在毫秒之间动态涌入，如果调度器每一次都要跑一轮复杂的整数线性规划来算最优调度，调度器本身的计算延迟早就把系统拖垮了。
Relief 抛弃了传统昂贵的 LP 求解器，设计了极其巧妙的启发式整数平分迭代：
- **双向成对快速松弛**：类似分布式网络中的两两配对流量消减，快速将过载专家上的 Token 配额削减并摊派给闲置副本；
- **极小硬件足迹**：算法天然适合高度并行化，可以直接以极紧凑的 CUDA Kernel 驻留在 GPU SM 内部执行，也可以硬化为 PCIe 旁路 FPGA 或加速器内部仅占 0.02% 晶体管的微型片上引擎。

3. 关键结论：
在三大开源主流 MoE 模型家族的真实 Decode 路由评测中，Relief 在所有测得的分组大小和层时间尺度下，均将负载均衡度保持在接近理论最优值的极窄区间。纯 CUDA Kernel 实现即可在数百微秒的层执行时间内匹敌或超越所有现存可部署方案；而片上硬件引擎更进一步将有效算力利用率相对于传统静态部署提升了整整 **37.3 个百分点**！

4. 背景地位：
针对 MoE 架构在现代微架构系统（如 Hopper、Blackwell 以及专用 NPU）上的极限延迟与调度瓶颈进行的硬核系统软硬件协同创新，论文已被计算机体系结构顶级会议 HPCA 2027 接收。

5. 落地相关性：
对于正在攻克超低延迟推理（如实时语音流、投机采样验证引擎）且运行 DeepSeek-V3 类庞大 MoE 模型的工程师团队，Relief 提供了一种几乎零开销消除长尾气泡的绝佳利器。

---

#### 9. OOM: Offload-Optimized Full-Parameter MoE Training via Memory-Execution Co-Design
- 中文译名：OOM：基于显存与执行协同优化的全参数 MoE 训练卸载框架
- 链接：https://arxiv.org/abs/2611.11364
- 作者：Ruijia Yang, Shiyuan Lin, Chengxi Liao, Zeyi Wen（通讯作者：Zeyi Wen）
- 单位：香港科技大学（广州）（HKUST(GZ)）
- 分类：cs.DC, cs.LG
- 方向标签：C. AI Infra (分布式训练系统 / 全参数 MoE 训练 / CPU-GPU Offload)
- 相关度：4.5/5

1. 核心贡献：
针对预算有限的中小企业与科研团队渴望在有限显存的 GPU 节点上进行**全参数 MoE 模型训练（Full-Parameter Training）**的痛点。传统参数卸载系统（如 DeepSpeed ZeRO-Offload/FSDP）在面对 MoE 极其庞大的专家权重时，频繁在主机内存（CPU DRAM）和 GPU 显存之间搬运参数，导致 PCIe 带宽严重瓶颈，GPU 长期处于停顿饥饿状态（GPU Starvation）。
作者开发了 OOM 框架，通过深度显存-执行协同设计（Memory-Execution Co-Design），彻底打破了通信堵塞训练管线的僵局，并在 GitHub 完全开源。

2. 原理解析：
这就好比在工厂车间（GPU 显存）面积有限时，大量零件（MoE 专家权重）必须存放在后方大仓库（CPU 内存）中。如果工人们干完一道工序才停下来喊仓库运下一道工序的零件，流水线就会频频停工。
OOM 的协同设计核心包括：
- **拓扑感知参数预取与多流重叠**：提前预知当前批次通过路由门控激活的专家，在上一层前向/反向传播进行密集的密集层计算时，通过后台流异步将所需专家参数从主机内存直接预取到预留显存缓冲区中；
- **显存复用与碎片整理**：利用 MoE 前向与反向传播的算子生命周期差异，动态回收中间激活值（Activation）释放的显存空间，直接借给即将到来的参数交换，大幅压低整体峰值显存占用；
- **流水线调度对齐**：智能调节非 MoE 密集层（Dense Layers）与 MoE 稀疏层的执行顺序，最大化掩盖数据传输开销。

3. 关键结论：
在标准评测基准中，OOM 在单台及多节点多 GPU 拓扑下，相较于标准 DeepSpeed ZeRO-3 卸载方案，将全参数 MoE 训练吞吐提升了 **1.8 到 3.4 倍**，同时显存碎片率降低了 45% 以上，使得原本需要在多台 8 卡 H100 集群上才能跑动的全参数 MoE 训练任务，能够在普通消费级或单机服务器上平稳启动。

4. 背景地位：
大模型全参数微调与训练平民化（Democratization of Training）的关键技术进展。将专家并行的稀疏性与异构分层内存管理做到了极高的重叠契合度。

5. 落地相关性：
对于内部计算资源有限、无法动辄租用成百上千张昂贵加速卡，但又需要对百亿至千亿级 MoE 模型进行全参数领域持续预训练或强监督微调的 AI Infra 团队，OOM 提供了立竿见影的开箱即用方案。

---

#### 10. Exploiting Native Hardware Heterogeneity: Custom GPSIMD Operators for Accelerating Emerging LLM Memory on AWS Trainium
- 中文译名：利用原生硬件异构性：在 AWS Trainium 上利用定制 GPSIMD 算子加速大模型新型记忆模块
- 链接：https://arxiv.org/abs/2611.11820
- 作者：Zifan He, Jason Cong（通讯作者：Jason Cong）
- 单位：加州大学洛杉矶分校（UCLA / 【知名实验室】）、AWS（亚马逊云科技 / 【工业界】）
- 分类：cs.DC
- 方向标签：C. AI Infra (AI 专用芯片体系结构 / 编译与算子优化 / AWS Trainium / DeepSeek Engram)
- 相关度：4.5/5

1. 核心贡献：
由计算机体系结构与 EDA 领域泰斗、UCLA 丛京生（Jason Cong）院士团队与 AWS 联合攻关！随着新型大模型记忆架构的涌现（如 DeepSeek-V4.1-Flash 中引入的 Engram 模块），计算特征发生了突变：它将**极其不规则的整数操作（64 位 n-gram 哈希与稀疏表查找）与密集的矩阵乘法（GEMM 和门控）**混杂在了一起。传统 GPU 在面对这种稀疏哈希检索时效率极度低下。
AWS Trainium 芯片在硬件原生层面上提供了绝妙的异构性：每个 NeuronCore 都将密集运算引擎与可定制的 GPSIMD 引擎配对，并共享片上 SBUF。然而官方软件栈（NKI）仅通过固定内置指令暴露 GPSIMD，且不支持在 Trainium 2/3 上使用自定义算子。本文构建了首个完整的 C++ 自定义算子编译工具链，成功将定制算子直接注入 Trainium 3 的编译结果（NEFF）中！

2. 原理解析：
在微服务世界里，这就像在一个拥有高速网络接口和专用加密芯片的服务器上，官方框架却只允许你跑标准 HTTP 请求，把旁边的专用协处理器闲置了。
丛京生团队的工具链实现了：
- **脱壳与算子注入工具（Toolchain Injection）**：编写 C++ 自定义算子，通过 LLVM 底层后端编译并强行无缝拼接进 Trainium 3 的编译目标文件（NEFF）中，绕开了官方工具链的阻断；
- **片上异构流水线协作**：让 GPSIMD 专门处理复杂的 64-bit n-gram 哈希计算与稀疏表索引，数据直接保留在片上共享的 SBUF 中，无缝无拷贝交给旁边的矩阵引擎执行随后的密集 GEMM 门控。

3. 关键结论：
在经过人工深度调优的 DeepSeek-V4.1-Flash NKI 基准之上，两个定制的 GPSIMD 算子在 Decode 阶段将 n-gram 哈希速度提升了 **1.79 倍**，将稀疏表检索提升了高达 **4.95 倍**，并将整个 Engram 模块的端到端执行性能提升了 **1.14 倍**！相关工具链已在 GitHub 完全开源。

4. 背景地位：
大模型前沿架构（混合稀疏记忆、Engram 等）与非英伟达专用云端 AI 芯片（AWS Trainium 2/3）深度软硬件协同编译的开山之作，打破了云厂商软件生态封闭对学术界与工业界极限性能调优的桎梏。

5. 落地相关性：
对于在 AWS 云上使用 Trainium 算力集群进行降本增效、部署最新混合架构大模型的 Infra 工程师，提供了绕过官方 NKI 功能限制、榨干 Trainium 3 硬件多核异构潜力的利器。

---

#### 11. Multi-GPU MoE Inference with Adaptive Expert Offloading
- 中文译名：AdaOffload：面向多 GPU 环境下自适应专家卸载的 MoE 推理加速系统
- 链接：https://arxiv.org/abs/2611.10219
- 作者：William X. Zheng, Zhongjie Chen, Shuo Yang, Ziming Mao, Xiaoze Fan, 等（共 12 位作者，通讯作者：Ion Stoica / Rishabh Iyer）
- 单位：加州大学伯克利分校（Sky Computing Lab / 【知名实验室】）、微软（Microsoft / 【工业界】）、上海交通大学、德克萨斯大学奥斯汀分校、加州大学戴维斯分校
- 分类：cs.AI, cs.DC
- 方向标签：C. AI Infra (推理服务 / 多 GPU 异构集群 / 自适应专家卸载)
- 相关度：4.5/5

1. 核心贡献：
由 UC Berkeley Sky Computing Lab（Ion Stoica 团队）领衔研发。虽然单卡专家卸载（Expert Offloading）能够在显存不足时跑起大模型，但在企业自建私有化服务或边缘数据中心中，用户往往拥有若干块异构或不同代际的 GPU（例如多张 L4、RTX Pro6000 甚至少量 B200 混部），却苦于现有系统根本**无法将专家卸载平滑横向扩展到多张 GPU 上**，导致算力闲置。
推出了 AdaOffload：业界首个通用且高效的多 GPU 混合专家执行框架，通过在线负载观察全面感知硬件算力、批次大小以及底层 NUMA 拓扑，实现前所未有的加速。

2. 原理解析：
在 Kubernetes 节点中，这就好比一个多 Socket 的混合计算节点：既有慢速 CPU、不同插槽上的内存，又有不同 PCI 通道挂载的多块 GPU。如果简单地用静态流水线切分，数据跨跨 Socket（跨 NUMA）传输就会造成总线大堵车。
AdaOffload 的核心设计：
- **GPU-CPU 协同并行切分**：将 Prefill 和 Decode 拆解为 GPU-CPU 并行与 GPU-CPU 协同执行的复合模式，热专家驻留 GPU，温冷专家动态跨通道流式拉取；
- **NUMA 感知与拓扑亲和性调度**：识别 CPU 内存插槽与 GPU 的物理绑定关系，确保专家权重的搬运严格走最近的本地 PCIe/总线通道；
- **在线动态反馈调节器**：根据实时请求的并发 Batch Size 波动，毫秒级调整 CPU 参与计算的比例，在批处理过载时自动收紧。

3. 关键结论：
在涵盖 L4、Pro6000、B200 等 5 种截然不同的硬件环境与不同 NUMA 架构的真实服务器上，针对规模从 284B 到惊人的 753B 的三大顶尖开源 MoE 权重进行实测：AdaOffload 相比当前业内 SOTA 卸载系统取得了 **1.9 倍至 15.5 倍** 的巨额吞吐飞跃！

4. 背景地位：
大模型本地化与私有化部署的救星之作。首次将多 GPU 分布式并行与 CPU 异构卸载在复杂 NUMA 拓扑下融为一体，代表了开源领域在极致硬件利用率上的巅峰水准。

5. 落地相关性：
对于在 Kubernetes 集群中管理异构 GPU 资源池、需要为企业内部提供低成本 200B+ 超大模型（如 DeepSeek/Qwen MoE）自建推理服务的 Infra 架构师，是不可多得的生产级设计参考。

---

#### 12. Reducing Cold-Start Latency on the WebAssembly Edge via Locality and Network-Aware Scheduling
- 中文译名：通过局部性与网络感知调度削减 WebAssembly 边缘计算冷启动延迟
- 链接：https://arxiv.org/abs/2611.12620
- 作者：Michiel Van Kenhove, Emiel Sucaet, José Santos, Filip De Turck, Bruno Volckaert, 等（共 6 位作者，通讯作者：Michiel Van Kenhove）
- 单位：根特大学-imec（IDLab, Ghent University - imec, 比利时）
- 分类：cs.NI, cs.SE
- 方向标签：A. 容器与运行时 (WebAssembly / Wasm 轻量运行时 / 冷启动优化) & B. 编排与调度 (边缘调度器 / 产物局部性与网络路由联合调度)
- 相关度：4.5/5

1. 核心贡献：
针对边缘计算与分布式 Serverless 场景下，越来越普遍采用的轻量化 WebAssembly (Wasm) 运行时（相比 Docker 容器具有纳秒级启动和极小内存占用）。然而在现实边缘拓扑中，当目标 Worker 节点本地尚未缓存所需的 Wasm 字节码产物时，仍然必须跨网络拉取，引发严重的**冷启动网络传输延迟（Cold-Start Latency）**；与此同时，请求发起者与被分派的 Worker 节点之间的物理网络路由延迟同样在影响端到端耗时。
传统的调度策略要么只看物理网络就近路由（导致命中无缓存的节点而触发漫长的产物拉取），要么盲目追求缓存命中（导致任务被调度到地理上极其遥远的节点）。本文扩展了 Wasm 原生边缘编排器，首创了**产物局部性与网络距离联合优化的状态感知调度算法**。

2. 原理解析：
这就好比 Kubernetes 的调度器在面对一个无状态 Serverless 请求时：一边是近在眼前但本地没拉镜像的边缘 Pod（算力节点），另一边是远在异地机房但已经温热就绪的 Pod。
传统调度器非黑即白：
- 如果一味选择近处的节点，当 Wasm 模块很大或网络带宽受限时，光拉取产物就花掉几百毫秒；
- 如果一味选择有缓存的远端节点，当 Wasm 模块很小而数据传输本身耗时很短时，跨城网络通信的往返延时（RTT）直接成了大头。
论文设计的混合调度器引入了精巧的状态评分模型：
- **产物大小感知权衡**：实时评估产物文件大小与节点网络传输速率，动态调整「产物局部性」和「网络临近性」在评分中的权重；
- **边缘节点缓存状态同步**：轻量维护边缘拓扑中各 Worker 节点的模块缓存列表。

3. 关键结论：
在基于真实树莓派（Raspberry Pi）集群并模拟区域网络延迟的边缘测试床上，该混合调度器相比默认的轮询（Round-Robin）基准，将平均端到端（E2E）耗时降低了最高达 **40.8%**！实测表明：当产物较大或高频反复请求时，局部性感知占据主导；而产物极小且路由延迟显著时，网络感知占据主导；两者的协同联合调度在所有异构边缘负载下均稳定保持最低延迟。

4. 背景地位：
WebAssembly 作为云原生与边缘容器体系下一代轻量运行时的前沿代表性研究，论文已被顶尖专业研讨会 WACE '26 接收，对未来云原生边缘编排（如 K3s、KubeEdge 上的 Wasm 编排）具有重要启发。

5. 落地相关性：
对于在边缘 Kubernetes 集群（如 K3s、Akri）上运行 WasmEdge / Wasmtime 微服务、需要极速冷启动响应（如工业 IoT、车联网智能感知、CDN 边缘函数）的系统工程师而言，本算法能直接嵌入现有的边缘调度插件中，带来立竿见影的性能收益。

---

### 其他论文（相关度 ≤2）

以下为今日抓取的其余 85 篇候选论文，主要属于理论分布式计算、专用数学建模、垂直应用及非系统向探索，相关度较低，在此简要列出以备参考：

1. **HeteroTask: Multi-Variant Task Scheduling and Execution on Distributed Heterogeneous Clusters** (cs.DC)
   - 链接：https://arxiv.org/abs/2611.10055 | 相关度：2/5
   - 简评：面向 CPU-GPU 异构集群 DAG 任务的多变体自适应调度与执行框架，结合贝叶斯校准消除运行时开销偏差。
2. **FirstSwap: Pre-Consensus Trade Approvals for Decentralized Market Design** (cs.DC, cs.CR, cs.GT)
   - 链接：https://arxiv.org/abs/2611.10254 | 相关度：2/5
   - 简评：提出去中心化交易的共识前交易批准机制，通过局部可交换性减少抢跑与前置交易（Front-Running）风险。
3. **Continual Instruction Tuning for LLM-ased Management of Continuum Resources** (cs.DC, cs.LG)
   - 链接：https://arxiv.org/abs/2611.10292 | 相关度：2/5
   - 简评：研究在云-边连续体资源管理中对大模型进行持续指令微调，探讨将大模型置于敏感控制回路中的稳定性与泛化性。
4. **OneReel: Efficient Multi-Scene Video Generation with Scene-Structured Attention** (cs.DC)
   - 链接：https://arxiv.org/abs/2611.10594 | 相关度：2/5
   - 简评：面向多场景长视频生成的结构化注意力机制，在跨场景一致性与二次计算复杂度之间取得高效折衷。
5. **Performance Benchmarking of Federated Learning Frameworks for Medical Image Classification** (cs.DC, cs.PF)
   - 链接：https://arxiv.org/abs/2611.10688 | 相关度：2/5
   - 简评：在容器化单机环境中对比评测 Flower、NVIDIA FLARE 与 FedBioMed 联邦学习框架的计算资源与显存消耗。
6. **DICOMPUTE: An Economic and Privacy-Aware Framework for Distributed Artificial Intelligence Inference** (cs.DC)
   - 链接：https://arxiv.org/abs/2611.10804 | 相关度：2/5
   - 简评：去中心化经济与隐私感知分布式 AI 推理框架，通过博弈论拍卖与信誉机制撮合边缘多方算力。
7. **Network Contention State Aware Dynamic Optimizer for Accelerator Collective Communication Libraries** (cs.DC, cs.LG, cs.MA)
   - 链接：https://arxiv.org/abs/2611.10984 | 相关度：2/5
   - 简评：基于双智能体（LSTM 拥塞检测器 + D3QN 配置选择器）的 NCCL 动态调优器，解决后台网络流量冲突导致的通信性能骤降。
8. **GARDEN: Efficient GPU-Accelerated Billion-Scale GNN Training via Caching-Sampling-Batching Co-Design** (cs.DC)
   - 链接：https://arxiv.org/abs/2611.11043 | 相关度：2/5
   - 简评：面向十亿级图神经网络训练的高效 GPU 加速框架，提出缓存、采样与批处理深度协同设计以突破显存墙。
9. **Multi-Node Transformers for Object Detection and Captioning Across Distributed Edge Networks** (cs.DC, cs.CV, cs.LG)
   - 链接：https://arxiv.org/abs/2611.11291 | 相关度：2/5
   - 简评：面向分布式边缘设备的多节点 Transformer 目标检测与字幕生成切分流水线系统。
10. **A Simple Phase-King Protocol with Predictions** (cs.DC)
   - 链接：https://arxiv.org/abs/2611.11370 | 相关度：2/5
   - 简评：引入外部预测信号的简化同步拜占庭一致性 Phase-King 协议理论研究。
11. **Ostinato: Fast CPU-GPU MoE Inference for Local Agents via Resident Experts in Every Forward Pass** (cs.DC, cs.LG)
   - 链接：https://arxiv.org/abs/2611.11533 | 相关度：2/5
   - 简评：面向本地工作站消费级 GPU 的 MoE 智能体推理引擎，通过常驻高频专家与定形 CUDA 图实现前向传播极速首字输出。
12. **Verifiable, Privacy-Preserving and Collaborative Multi-Objective Optimization with NSGA-II on Blockchain** (cs.DC)
   - 链接：https://arxiv.org/abs/2611.11567 | 相关度：2/5
   - 简评：基于区块链与零知识证明的可验证、隐私保护协同多目标优化 NSGA-II 算法实现。
13. **A Decentralized Quantum-Resistant Notary Scheme for Blockchain Interoperability with a Novel Dynamic Trust Model** (cs.DC)
   - 链接：https://arxiv.org/abs/2611.11682 | 相关度：2/5
   - 简评：用于跨链互操作的去中心化抗量子公证人方案，结合动态信任模型保障异构链资产跨链安全。
14. **OverlapAdvisor: Modeling and Adapting Computation-Communication Overlap for Distributed MoE Serving** (cs.DC, cs.PF)
   - 链接：https://arxiv.org/abs/2611.11857 | 相关度：2/5
   - 简评：面向专家并行 MoE 推理通信与计算重叠的解析建模与自适应配置系统，指导微批切分与流并发度调优。
15. **DeFSM: Robust and Efficient Decentralization of Federated Submodular Maximization** (cs.DC, cs.LG)
   - 链接：https://arxiv.org/abs/2611.11866 | 相关度：2/5
   - 简评：针对联邦子模最大化的去中心化鲁棒算法，消除中心聚合节点单点故障与通信瓶颈。
16. **Accelerating Direct Sparse Solvers with Graph Computing Accelerators** (cs.DC)
   - 链接：https://arxiv.org/abs/2611.11876 | 相关度：2/5
   - 简评：利用专有图计算硬件加速器对大型稀疏线性方程组直接解法（高斯消元）进行计算加速。
17. **Optimal Proximity Black Hole Search with Programmable Matter** (cs.DC)
   - 链接：https://arxiv.org/abs/2611.12170 | 相关度：2/5
   - 简评：可编程物质（Programmable Matter）在分布式多智能体拓扑下进行邻近黑洞搜索的最优算法理论研究。
18. **RecoGEM: A Serving System for Production-Scale Generative Recommendation** (cs.DC, cs.AI, cs.IR)
   - 链接：https://arxiv.org/abs/2611.12296 | 相关度：2/5
   - 简评：面向工业级生成式推荐的大规模服务化系统，优化自回归生成模型在高并发高吞吐下的分布式部署架构。
19. **Mitigating SM-Level Load Imbalance in 3D Gaussian Splatting on GPUs** (cs.DC)
   - 链接：https://arxiv.org/abs/2611.12319 | 相关度：2/5
   - 简评：通过细粒度高斯球重排与动态流分发缓解 3DGS 渲染在 GPU 流式多处理器（SM）层级的负载严重不均。
20. **Adapting Multi-Stage Distributed Real-Time Systems Design to Vehicular Edge Computing** (cs.DC)
   - 链接：https://arxiv.org/abs/2611.12370 | 相关度：2/5
   - 简评：将多阶段分布式硬实时系统可调度性理论迁移至车联网边缘计算环境的建模研究。
21. **Resetting-based designated information distribution** (cs.DC)
   - 链接：https://arxiv.org/abs/2611.12485 | 相关度：2/5
   - 简评：基于状态重置机制的分布式网络指定信息受控分发协议与一致性收敛界限证明。
22. **Contention Resolution with a Fast-but-Fickle Channel** (cs.DC)
   - 链接：https://arxiv.org/abs/2611.12843 | 相关度：2/5
   - 简评：在具备快速但不稳定双信道的多路访问网络中进行冲突分解的算法理论设计。
23. **Fast Entropy Decoding for Sparse MVM on GPUs** (cs.PF, cs.DC)
   - 链接：https://arxiv.org/abs/2603.01915 | 相关度：2/5
   - 简评：针对 GPU 稀疏矩阵向量乘（SpMVM）的高吞吐熵解码内核优化，利用轻量级位掩码压缩提升显存带宽利用率。
24. **Halley: A Predictive Control Plane for Optical AI Data Center Networks** (cs.NI, cs.DC)
   - 链接：https://arxiv.org/abs/2611.04408 | 相关度：2/5
   - 简评：面向光电混合 AI 数据中心网络的主动预测控制平面，基于训练任务确定性集合通信模式实现全光拓扑毫秒级预重构。
25. **Fresh Enough to Decide: Age of Intelligence for Cost-Aware Model Synchronization in Dynamic IoT Systems** (cs.LG, cs.DC)
   - 链接：https://arxiv.org/abs/2611.09935 | 相关度：2/5
   - 简评：定义“智能时效（Age of Intelligence）”指标，用于动态 IoT 边缘协同推理中低通信成本的模型轻量同步。
26. **ReelCache: An Efficient KV Cache Compression and Management System for Multi-Round Video Generation** (cs.CV, cs.DC, cs.LG)
   - 链接：https://arxiv.org/abs/2611.09973 | 相关度：2/5
   - 简评：面向多轮长视频生成的时空感知 KV Cache 压缩与显存层级卸载系统 ReelCache。
27. **PACE: Keeping the Right Tokens in the KV Cache Is Not Enough for Long-Horizon LLM Agents** (cs.LG, cs.CL, cs.DC)
   - 链接：https://arxiv.org/abs/2611.10240 | 相关度：2/5
   - 简评：揭示长上下文智能体即使保留正确 Token 也面临语义漂移的现象，提出兼顾语义锚点与拓扑的 KV Cache 驱逐策略 PACE。
28. **Reproducible LoRA Inference Through Deterministic Split-K Reduction** (cs.LG, cs.AI)
   - 链接：https://arxiv.org/abs/2611.10334 | 相关度：2/5
   - 简评：通过确定性 Split-K 规约解决 GPU 浮点非结合律导致的微调 LoRA 批量推理输出结果不确定问题。
29. **EmbodiedIntentBench: Benchmarking Intent-Driven Runtime Adaptation for Mobile Robotic Missions** (cs.RO, cs.AR, cs.DC)
   - 链接：https://arxiv.org/abs/2611.10498 | 相关度：2/5
   - 简评：移动机器人具身多任务意图驱动运行时动态自适应与软硬件资源调度基准评测集。
30. **QAOA Inside ADMM: Subproblem Wins Do Not Become Decomposition Wins at Matched Budgets** (quant-ph, cs.DC)
   - 链接：https://arxiv.org/abs/2611.10527 | 相关度：2/5
   - 简评：实证探讨在交替方向乘子法（ADMM）框架下将量子近似优化（QAOA）作为子求解器的收敛性与经典算力等预算瓶颈。
31. **Detent: Batch-Invariant LLM Serving and RL Rollouts at Near-Stock Speed** (cs.LG, cs.DC, cs.PF)
   - 链接：https://arxiv.org/abs/2611.10611 | 相关度：2/5
   - 简评：面向大模型强化学习 Rollout 的批次无关（Batch-Invariant）确定性推理框架 Detent，保持高吞吐同时杜绝数值非确定性。
32. **Extending DBLog-Based Incremental Snapshots to Handle Orphan Rows in CDC Pipelines** (cs.DB, cs.DC)
   - 链接：https://arxiv.org/abs/2611.10810 | 相关度：2/5
   - 简评：扩展基于 DBLog 增量快照的 CDC 数据变更捕获机制，解决高频事务回滚导致的孤儿行脏数据漏读难题。
33. **Optimal Byzantine-resilient Federated Learning with User-level Differential Privacy** (cs.LG, cs.CR, cs.DC)
   - 链接：https://arxiv.org/abs/2611.10898 | 相关度：2/5
   - 简评：在用户级差分隐私保障下抵抗恶意客户端拜占庭攻击的最优鲁棒聚合规则理论构建。
34. **Edge Computing for Computer Vision in IoT: Feasibility and Directions** (cs.NI, cs.CV, cs.DC)
   - 链接：https://arxiv.org/abs/2611.11218 | 相关度：2/5
   - 简评：IoT 场景下边缘计算机视觉部署的可行性、网络带宽与功耗约束综合调研综述。
35. **FRESCO: A Novel Consistency Control for Asynchronous Pipeline Parallel Training** (cs.LG, cs.AI, cs.DC)
   - 链接：https://arxiv.org/abs/2611.11238 | 相关度：2/5
   - 简评：面向异步流水线并行训练的一致性控制机制 FRESCO，通过陈旧度感知权重补偿在无气泡调度下维持收敛性。
36. **AWS Serverless Infrastructure from WebAssembly Components** (cs.SE, cs.DC)
   - 链接：https://arxiv.org/abs/2611.11293 | 相关度：2/5
   - 简评：提出从 WebAssembly 组件模型直接生成完整 AWS 无服务器基础设施代码（IaC）的编译器工具链。
37. **MOMENT-DP: Momentum Aware Evaluation of Correlated Noise for Differentially Private Training** (cs.LG, cs.AI, cs.DC)
   - 链接：https://arxiv.org/abs/2611.11457 | 相关度：2/5
   - 简评：在差分隐私分布式训练中评估动量关联噪声对隐私预算消耗与优化器收敛的理论框架。
38. **Late but Valuable: Why Deadlines Change the Measured Value of LLM Reasoning** (cs.LG, cs.AI, cs.PF)
   - 链接：https://arxiv.org/abs/2611.11910 | 相关度：2/5
   - 简评：分析严格截止时间约束对多步推理大模型生成价值的影响，提出基于剩余时间自适应收缩思考深度的调度思路。
39. **ShiftCache: Fast and Exact Indel Effect Prediction by Reusing Shifted Reference Encodings** (cs.LG, cs.DC)
   - 链接：https://arxiv.org/abs/2611.11976 | 相关度：2/5
   - 简评：生物信息基因大模型中利用平移参考序列编码缓存（ShiftCache）加速插入缺失突变预测的系统实现。
40. **Transactional Data Change for Real-Time Analytics in Lakehouses** (cs.DB, cs.AI, cs.DC)
   - 链接：https://arxiv.org/abs/2611.12169 | 相关度：2/5
   - 简评：现代数据湖仓架构中支持秒级实时分析的事务性数据流变更引擎与隔离级别验证。
41. **Lessons Not Learned: Why Cross-Chain Bridges Keep Losing Billions the Same Way** (cs.CR, cs.DC)
   - 链接：https://arxiv.org/abs/2611.12252 | 相关度：2/5
   - 简评：跨链桥巨额资金被盗案的系统安全回顾与同构验证逻辑漏洞分类学。
42. **Reducing Provers in Distributed Quantum Verification** (quant-ph, cs.DC)
   - 链接：https://arxiv.org/abs/2611.12600 | 相关度：2/5
   - 简评：在分布式交互式证明系统中通过纠缠共享减少量子验证证明者节点数量的纯理论证明。
43. **Retention Horizons of Volatile Stores in iOS and Android Extractions** (cs.SE, cs.CR, cs.OS)
   - 链接：https://arxiv.org/abs/2611.10309 | 相关度：2/5
   - 简评：移动操作系统易失性数据存储生命周期与数字取证提取有效性窗口的实证测量。
44. **Device-Life Boundary Indicators and the Classification of Restored Versus Native Records on Android** (cs.SE, cs.CR, cs.OS)
   - 链接：https://arxiv.org/abs/2611.10312 | 相关度：2/5
   - 简评：Android 系统设备生命周期边界指示器与出厂恢复记录自动分类机制。
45. **BunshinRL: Splitting Live Agent Workspaces for Memory-Efficient Agentic RL** (cs.AI, cs.LG, cs.OS)
   - 链接：https://arxiv.org/abs/2611.10453 | 相关度：2/5
   - 简评：通过将活跃智能体工作空间按快照与差异层切分（分身机制）实现显存友好的大规模智能体强化学习环境。
46. **Sparse Predict and Demote: Optimal Scheduling with Minimal Size Advice** (cs.PF, cs.DS)
   - 链接：https://arxiv.org/abs/2611.10293 | 相关度：2/5
   - 简评：仅依赖稀疏极简任务尺寸建议的在线最优任务调度与降级排队理论算法。
47. **Repeating Work Can Lower Energy per Successful Goal in LLM Agents** (cs.PF)
   - 链接：https://arxiv.org/abs/2611.10315 | 相关度：2/5
   - 简评：实证论证在智能体复杂推理中适度重试与多次采样反而在统计上能降低单成功目标的总 GPU 能耗。
48. **LEGIT: Live Eligibility Gating over Identifier Tries for Constrained Decoding of Heterogeneous Pages** (cs.IR, cs.LG, cs.PF)
   - 链接：https://arxiv.org/abs/2611.10357 | 相关度：2/5
   - 简评：利用标识符 Trie 树前缀在线门控实现异构文档生成式检索受限解码的高性能算子优化。
49. **Comparing Write, Read, and Query Performance of General-Purpose and Columnar Data Serialization Formats at Increasing Scale: An Empirical Benchmark Study with Statistical Validation on Synthetic and Real-World Data** (cs.DB, cs.PF, cs.DC)
   - 链接：https://arxiv.org/abs/2611.10398 | 相关度：2/5
   - 简评：跨规模对比 Parquet、ORC、Avro 等通用与列式数据序列化格式读写及查询性能的大规模基准评测。
50. **Missed Interferers in Ray-Traced Radio Maps: A Digital-Twin and Stochastic Geometry Study of Aerial Coverage** (eess.SP, cs.PF)
   - 链接：https://arxiv.org/abs/2611.10867 | 相关度：2/5
   - 简评：结合数字孪生光线追踪与随机几何评估低空通信无线电地图中漏检干扰源的性能模型。
51. **Advancements in Cloud-Native Systems: A Systematic Mapping Study of Reliability and Scalability across Cloud-Native, Edge-Native and AI-Enabled Systems** (cs.SE, cs.AI, cs.DC)
   - 链接：https://arxiv.org/abs/2611.11040 | 相关度：2/5
   - 简评：系统化梳理云原生、边缘原生及 AI 赋能系统在可靠性与可伸缩性架构实践方面的学术综述。
52. **FESOM2.8 in single precision: climate fidelity over six decades and performance on CPUs and GPUs** (physics.ao-ph, cs.DC, cs.PF)
   - 链接：https://arxiv.org/abs/2611.11248 | 相关度：2/5
   - 简评：海洋气候模拟系统 FESOM2.8 单精度移植在 CPU 与 GPU 集群上的科学保真度与吞吐加速测试。
53. **MG-Cache: Multi-Granularity Caching for Accelerating Diffusion Transformer Inference** (cs.LG, cs.CV, cs.PF)
   - 链接：https://arxiv.org/abs/2611.11365 | 相关度：2/5
   - 简评：多粒度缓存框架 MG-Cache，自适应缓存 DiT 扩散模型的时间步与空间块特征加速图像生成。
54. **PTC-IoU: CPU-Friendly Detection Quality Estimation for Edge Video Analytics** (cs.CV, cs.PF)
   - 链接：https://arxiv.org/abs/2611.12405 | 相关度：2/5
   - 简评：面向边缘视频分析的极低开销 CPU 友好型目标检测质量估计与过滤算子。
55. **Inference Validation for Regulated AI: Building a Decision Pipeline on NVIDIA AIPerf** (cs.SE, cs.AI, cs.PF)
   - 链接：https://arxiv.org/abs/2611.12737 | 相关度：2/5
   - 简评：基于 NVIDIA AIPerf 构建针对受监管行业 AI 推理服务的合规性基准测试与决策流水线。
56. **Facilitating Reproducibility in Visualization Systems Research Through Containerization** (cs.HC)
   - 链接：https://arxiv.org/abs/2611.09910 | 相关度：2/5
   - 简评：利用 Docker 容器化封装与流水线自动化促进可视化与人机交互系统研究的实验可重现性探讨。
57. **Efficient Learning of Differentiable MPC Policies on the GPU via Smoothed ADMM and First-Order Reinforcement Learning** (cs.RO, cs.AI)
   - 链接：https://arxiv.org/abs/2611.09937 | 相关度：2/5
   - 简评：在 GPU 上利用平滑 ADMM 算子实现端到端可微分模型预测控制（MPC）策略的批量并行训练。
58. **Coordinated Mixed-Precision KV Cache Quantization for Efficient LLM-based Multi-agent Systems** (cs.LG)
   - 链接：https://arxiv.org/abs/2611.10096 | 相关度：2/5
   - 简评：多智能体协作会话中基于跨智能体敏感度协同的混合精度 KV Cache 量化策略。
59. **Fully Dynamic Correlation Clustering with Vertex Updates in Polylogarithmic Update Time** (cs.DS)
   - 链接：https://arxiv.org/abs/2611.10184 | 相关度：2/5
   - 简评：多对数更新时间内支持顶点动态增删的关联聚类图算法理论。
60. **STAIRS: Staging the Inverse Problem via Admissible-Support Scheduling for Unrolled MRI Reconstruction** (cs.CV, cs.AI)
   - 链接：https://arxiv.org/abs/2611.10260 | 相关度：2/5
   - 简评：医学磁共振成像迭代重构中基于容许支撑集分阶段调度的算法优化。
61. **The World Model Planning Accelerator (WMPA): Hardware-Algorithm Co-Design for Embedded AI in Robotics** (cs.AR, cs.LG, cs.RO)
   - 链接：https://arxiv.org/abs/2611.10316 | 相关度：2/5
   - 简评：嵌入式机器人硬件加速器 WMPA，针对世界模型高并发蒙特卡洛树搜索（MCTS）规划进行芯片架构定制。
62. **IdealCache: Rethinking Cache Scheduling in Diffusion Transformers via Ideal Trajectories** (cs.AI)
   - 链接：https://arxiv.org/abs/2611.10340 | 相关度：2/5
   - 简评：依据理想采样轨迹重新设计扩散 Transformer 推理过程中特征图缓存重用时机。
63. **CALFA-KV: Joint Calibration and Fisher-Guided Anchors for 1-Bit KV Cache Compression** (cs.LG)
   - 链接：https://arxiv.org/abs/2611.10511 | 相关度：2/5
   - 简评：结合联合标定与 Fisher 信息量锚点的超低比特（1-bit）KV Cache 激进压缩算法。
64. **CAROUSEL: GPU-Accelerated Private Vector Search via Homomorphic Sketching** (cs.CR)
   - 链接：https://arxiv.org/abs/2611.10622 | 相关度：2/5
   - 简评：利用 GPU 加速同态草图（Homomorphic Sketching）实现高吞吐隐私保护向量检索系统 CAROUSEL。
65. **A Simple Computer-Assisted Proof of the 5/6-Bound for Real-Period Pinwheel Scheduling** (cs.DM, cs.DS, math.CO)
   - 链接：https://arxiv.org/abs/2611.10624 | 相关度：2/5
   - 简评：实时风车调度问题（Pinwheel Scheduling）5/6 界限的计算机辅助形式化证明。
66. **PENSA: A Spatial Accelerator for BitNet b1.58 Inference on an HBM-equipped AMD Alveo FPGA** (cs.AR, eess.SP)
   - 链接：https://arxiv.org/abs/2611.10648 | 相关度：2/5
   - 简评：在搭载 HBM 的 AMD Alveo FPGA 上针对 BitNet b1.58 1.58比特大模型设计的空间硬件加速器 PENSA。
67. **Two-Timescale Trajectory Control, Task Reassignment and Resource Scheduling for Multi-UAV Cooperative Mobile Edge Computing** (eess.SY)
   - 链接：https://arxiv.org/abs/2611.10673 | 相关度：2/5
   - 简评：多无人机协同移动边缘计算中结合双时间尺度的航迹控制与算力资源重调度算法。
68. **A Case Study of a Phishing Cluster Targeting German Universities** (cs.CR)
   - 链接：https://arxiv.org/abs/2611.10698 | 相关度：2/5
   - 简评：针对德国高校的特定钓鱼网站集群与网络攻击基础设施案例剖析。
69. **Mirage: Provable Defense Against LLM KV Cache Timing Side Channels with Topology-Aware Isolation** (cs.CR, cs.AI)
   - 链接：https://arxiv.org/abs/2611.10756 | 相关度：2/5
   - 简评：利用拓扑感知物理隔离防御大模型共享多租户服务中针对 PagedAttention KV Cache 的计时侧信道攻击。
70. **ClusLoad: Cluster-Guided Model Sharing for Scalable Distribution Transformer Load Forecasting** (cs.LG)
   - 链接：https://arxiv.org/abs/2611.11170 | 相关度：2/5
   - 简评：电网配电变压器负载预测中基于聚类引导的多站点轻量模型共享与迁移框架。
71. **Spot Markets for AI Inference: Dynamic Capacity Allocation and Pricing on a Shared Accelerator Fleet** (eess.SY)
   - 链接：https://arxiv.org/abs/2611.11215 | 相关度：2/5
   - 简评：云端共享加速器集群上针对 AI 推理竞价实例（Spot Instances）的动态容量调配与机制定价模型。
72. **Verify Before You Fetch: Reliable KV Cache Compression for LLM Inference** (cs.AI)
   - 链接：https://arxiv.org/abs/2611.11319 | 相关度：2/5
   - 简评：长文本大模型分布式推理中引入“取前校验”校验机制的高可靠 KV Cache 流式有损压缩协议。
73. **Semantically Aligned KV Cache Compression for Efficient Agentic Autoregressive Video Generation** (cs.CV, cs.LG)
   - 链接：https://arxiv.org/abs/2611.11452 | 相关度：2/5
   - 简评：面向自回归视频生成多智能体的语义对齐时序 KV Cache 压缩与剪枝策略。
74. **One-Shot Hierarchical Federated Clustering for Distributed Non-IID Biomedical Data Analysis** (cs.LG)
   - 链接：https://arxiv.org/abs/2611.11481 | 相关度：2/5
   - 简评：非独立同分布生物医学数据分析中的单轮通信分层联邦聚类算法。
75. **Direct GPU Energy Measurements of Batch-Level Sharing in Mixture-of-Experts and Recurrent Models** (cs.LG, cs.AI)
   - 链接：https://arxiv.org/abs/2611.11696 | 相关度：2/5
   - 简评：对 MoE 与循环网络在批量共享与算子融合下的实际 GPU 物理能耗进行高精度板卡实测与分析。
76. **Reproducible quantum clustering for single-cell transcriptome atlases** (cs.AI, q-bio.GN, q-bio.QM)
   - 链接：https://arxiv.org/abs/2611.11745 | 相关度：2/5
   - 简评：单细胞转录组图谱构建中提高降维一致性与聚类可重现性的量子退火辅助算法。
77. **BridgeKV: Large-Model Prefill and Small-Model Decoding for LLM Inference via KV Cache Translation** (cs.CL)
   - 链接：https://arxiv.org/abs/2611.11761 | 相关度：2/5
   - 简评：大模型推理中采用超大模型执行 Prefill 并通过 KV 跨架构投影映射给小模型进行 Decode 的投机生成系统。
78. **Fade to... Red? Scheduling Coloured Noise Exploration Supports Efficient Robot Learning with Reduced Movement Jerk** (cs.RO, cs.LG)
   - 链接：https://arxiv.org/abs/2611.11868 | 相关度：2/5
   - 简评：机器人强化学习探索中按时序调度粉红噪声与有色噪声以抑制机械抖动的动作调度器。
79. **Robust Domain-Mixture Scheduling for Multi-Teacher On-Policy Distillation** (cs.CL)
   - 链接：https://arxiv.org/abs/2611.12012 | 相关度：2/5
   - 简评：多领域专家教师联合在线策略蒸馏中的动态领域混合配额采样调度算法。
80. **An open source Python code for three-dimensional topology optimization in single precision on a consumer GPU** (cs.CE, cs.MS)
   - 链接：https://arxiv.org/abs/2611.12027 | 相关度：2/5
   - 简评：在单块消费级显卡上通过单精度浮点加速百万网格三维拓扑优化的高性能 Python/CUDA 开源代码。
81. **Translating KV Caches Between Hybrid-Attention Language Models: MLA Latents, Linear-Attention States and Sparse-Attention Indexers** (cs.LG, cs.CL)
   - 链接：https://arxiv.org/abs/2611.12062 | 相关度：2/5
   - 简评：在混合注意力模型之间将 DeepSeek MLA 隐变量、线性注意力状态与稀疏索引进行跨模型 KV 转换的轻量适配层。
82. **Correct First, Fast Second: What a Local 7B Code Model Can and Cannot Do for GPU Kernel Optimization** (cs.LG)
   - 链接：https://arxiv.org/abs/2611.12079 | 相关度：2/5
   - 简评：系统性评估本地 7B 代码小模型在自动重写与优化 PyTorch 自定义 CUDA 算子任务中的真实上限与边界。
83. **GPU-Accelerated Non-Interactive Encrypted Neural Network Training with Batched Diagonal Packing** (cs.CR, cs.LG)
   - 链接：https://arxiv.org/abs/2611.12161 | 相关度：2/5
   - 简评：利用对角打包与 SIMD 批处理在 GPU 上实现非交互式同态加密神经网络训练的高性能加速实现。
84. **Reshaping Checkpoint-Induced Power Variations Through Inference Workload Scheduling** (eess.SY)
   - 链接：https://arxiv.org/abs/2611.12621 | 相关度：2/5
   - 简评：大模型分布式训练同步检查点触发瞬时负荷突降，通过两层弹性推理调度填补电力波谷平抑数据中心微电网频率波动。
85. **GEAR: A GPU-Accelerated Global Solver for Bounded Continuous Nonlinear Programs via Linear Bound Propagation** (math.OC, cs.LG, cs.MS, math.NA)
   - 链接：https://arxiv.org/abs/2611.10487 | 相关度：2/5
   - 简评：将神经网络形式化验证中的线性界限传播（Linear Bound Propagation）迁移至 GPU 大规模求解非线性规划的全局求解器。

---

### 今日趋势小结

纵观今日系统方向全部 97 篇新文献，AI 基础设施与云原生体系的演进呈现出三个极具颠覆性的底层趋势：

1. **容器运行时与集群编排的底层「黑盒假设」正在被打破与重构**：
   长久以来，云原生生态假定下层快照卷与上层编排器各司其职，然而 Kliukovkin 的最新工作（论文 1）以无可辩驳的实证打破了这一幻想——stargz/SOCI 按需拉取快照驱动的无感知缓存满溢，直接引发了「探针绿色却文件损坏」以及「kubelet 误杀无辜 Pod」的致命级平台失效。与此呼应，LinkedIn 的 Firepool（论文 2）与湖南大学的 MTRDMA（论文 4）分别从 GPU 预热 Pod 池化与 RDMA 网卡控制面 cgroup 隔离切入，证明未来的容器运行时与调度器必须实现对底层硬件缓存、物理文件系统与网络微架构的「穿透式双向对账」。

2. **通信与计算重叠（Overlap）走向「描述符轻量化」与「在线闭环控制」**：
   在大模型 MoE 专家并行与机架级互连（GB300 NVL72）时代，简单的双流重叠早已不够用。NVIDIA 官方网络团队的两项重磅工作（论文 3 与论文 6）给出了未来的演进范本：一方面，在微架构层通过 GPU-Friendly Descriptors（GPI）与 CPU 线程卸载（GDAKI Free Flow），将 GPU 从繁琐的网络描述符装包中解救出来，消除 DBO 中的裸露发送时间；另一方面，NCCL 集合通信算法选择彻底告别了 10 年不变的静态 AUTO 解析模型，步入由在线多臂老虎机驱动的闭环测量时代，以动态适应网络抖动与多租户干扰。

3. **大模型推理全面迈入「智能体语义感知」与「全拓扑分层流动」时代**：
   随着 Coding Agent 与多步推演智能体成为主流业务负载，传统静态 PD 分离与盲目 LRU 缓存的缺陷被无限放大。UC Berkeley 与 MIT 的 Evolving Infra（论文 5）、UT Austin 的 KV Cache 存储视图（论文 7）以及 AdaOffload（论文 11）共同勾勒出下一代推理系统的轮廓：算力分配与 KV 缓存管理彻底解耦，调度器依据智能体多轮会话标识符与完成信号做精准生命周期管控；而在硬件拓扑层面，从片上专用 GPSIMD 协处理器（论文 10）、逐步松弛的 MoE 负载均衡引擎（论文 8）到 NUMA 亲和的多卡 CPU 协同卸载，系统栈正在穷尽每一寸异构硬件的极限潜能。
