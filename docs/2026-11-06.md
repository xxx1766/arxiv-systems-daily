## arXiv 系统方向日报 · 2026-11-06

### 今日概览

今日系统方向（cs.DC / cs.OS / cs.PF 及相关交叉领域）共抓取 38 篇候选论文。经过资深系统调研体系的严格筛选与多维度评分，本次**入选深读：12 篇**（其中 9 篇评分为 5 分的核心突破论文，3 篇评分为 4 分的高价值实用论文），其余 26 篇理论或边缘交叉论文归入文末列表。

今日文献呈现出极强的「硬件拓扑与分布式系统深度融合」特色：从机架级 GB200 NVL72 与 B300 跨 Die 局部性域的实测剖析，到 AMD CDNA4 架构与昇腾生态上的原生算子/卸载优化；从分布式优化器 Muon 与 FSDP 的矩阵级协同，到 CXL 异构内存分层在 Linux 内核层面的硬件抽象，整体技术栈正在加速向硬件亲和与端到端协同演进。

今日必读：
1. **DMuon**: 针对新型矩阵优化器 Muon 与 FSDP/HSDP 拓扑冲突，首创矩阵粒度所有权与稀疏通信调度，在 256 卡 H100 集群上实现超越 AdamW 的训练吞吐。
2. **FastAFD**: 针对 GB200 NVL72 机架级 NVLink 体系，系统性实测 Attention 与 MoE FFN 解耦收益，提出三因子解析模型指导微批流水线部署。
3. **SiliconForge**: 针对 Prefill/Decode 与 AFD 细粒度解耦展开前瞻性算力与功耗建模，揭示跨代芯片与机架拓扑演进下 AFD 的落地边界。
4. **KOSMOS**: AMD Instinct MI350X/MI355X 上的自调度持久化 Kernel，打破传统静态流水线，实现 Transformer 层 TP+SP 及 MoE 全链路通信计算重叠。
5. **Locality Domains on Blackwell**: CUDA 13.4 双 Die 局部性域深度实测，揭示 B300 跨 Die 内存访问特异性与驱动内核模块 32MB 分配瓶颈及修复方案。
6. **FlashOffloading**: 面向昇腾 910C 的长序列端到端 KV Cache 主机内存全卸载架构，已并入 vLLM-ascend 生产级代码。
7. **OpenRDMA**: 提出 8 字节轻量 Doorbell 与 FPGA 网卡硬件重构 WQE，彻底卸载 GPU SM 控制开销的原生多路径可靠 RDMA 传输架构。
8. **FlexFloor**: 基于弹性专家并行（EEP）解决 MoE 强化学习后训练（RLHF）尾延迟与长尾响应阻塞，实现计算节点即时释放。
9. **Memory Fit**: 面向 CXL 与非易失性异构内存的 Linux 6.6 页面放置硬件抽象，以仅 64 位元数据达到接近理论最优的页面分层放置。
10. **NUMA-Torch**: 编译器层级 NUMA 感知 Tensor Parallelism，将多路服务器 CPU 视作独立分区，消除跨 Socket UPI 互连瓶颈。
11. **StrataFlux**: 低比特大模型量化流式精度补偿系统，利用主机 RAM/SSD 作为分级存储按需补充关键精度，显存减半且无损输出。
12. **ZYFA**: 针对 AMD CDNA4 (MI355X) 架构软硬件特性的 FP8 FlashAttention 与 DeepSeek MLA 算子极限性能与数值精度优化。

---

### 逐篇解读

#### 1. DMuon: Scaling Matrix Optimizers in Data Parallelism with Topology-Aware Matrix Ownership and Communication
- 中文译名：DMuon：基于拓扑感知矩阵所有权与通信调度在数据并行中扩展矩阵优化器
- 链接：https://arxiv.org/abs/2611.07084
- 作者：Starrick Liu, Ruizhi Chengze, Lufang Chen, Michael Zhao, Ran Yu 等（共 13 位作者，通讯作者：Hao Wang）
- 单位：X Square Robot（X2Robot / 【工业界】）
- 分类：cs.DC
- 方向标签：C. AI Infra (训练系统 / 优化器与分布式通信优化)
- 相关度：5/5

1. 核心贡献：
针对近期在大模型训练中表现惊艳的新型矩阵优化器 Muon（通过 Newton-Schulz 迭代进行全矩阵正交化更新）与主流参数切分数据并行运行时（PyTorch FSDP / ZeRO-2/3、HSDP）天然冲突的问题，提出了首个矩阵粒度优化器分布式运行时 DMuon。DMuon 消除了以往要么重复计算迭代、要么产生高额 gather 通信的两难困境，在多达 256 卡 NVIDIA H100 集群上，首次将 Muon 的训练吞吐提升至匹配甚至超越标准 AdamW 的水平（达 FSDP2+AdamW 的 1.05 倍，比传统 Gather-then-Replicate 方案快 2.1 倍）。
2. 原理解析：
在云原生分布式训练中，AdamW 是逐元素（Element-wise）更新的，每个 GPU 节点像 Kubernetes 中按 cgroup 划分配额一样各自计算自己持有的参数分片即可；但 Muon 需要对整个二维权重矩阵做 Newton-Schulz (NS) 矩阵正交化迭代，如果像 FSDP 那样把矩阵横切切碎，局部切片根本无法进行全矩阵迭代。
DMuon 的思路类似云原生集群中的「Leader-Worker 拓扑所有权机制」：
- **矩阵拓扑所有权（Matrix Ownership）**：不再按行切碎矩阵，而是为每一整个权重矩阵指派一个专属 Owner GPU。该 Owner 负责执行该矩阵全部的 NS 迭代计算，并通过计算负载均衡算法将不同层、不同大小的矩阵均匀打散给集群中的各个 GPU。
- **全局单副本与流水线发布**：在 HSDP（跨节点分片、节点内副本）拓扑下，所有副本全局共享单份梯度与优化器状态。Owner 一旦计算完成某矩阵的新权重，立即通过双层网络（机内 NVLink + 机间 RoCE/IB）向其他副本节点广播发布，并与后续的前向反向计算完全 Overlap。
- **稀疏可变长集合通信调度**：由于各个矩阵大小不一、完成时间不同，通信变成了稀疏、不定长的 ReduceScatter 与 AllGather。DMuon 设计了数据就绪即触发的动态通信调度器，彻底避免了粗粒度 Barrier 带来的卡间空闲等待。
3. 关键结论：
在 256 卡 H100 集群上，针对三款密集语言模型（Dense LLM）以及两款视觉-语言-动作具身智能大模型（VLA），DMuon 的训练吞吐在所有模型下均持平或超越 PyTorch FSDP2 + AdamW（中位数达到 1.05 倍），且比基线方案（收集后复制计算）吞吐提升 2.1 倍，消除了矩阵优化器在大规模集群训练中的系统落地瓶颈。
4. 背景地位：
Muon 是近期大模型算法领域最受关注的优化器之一（在微小步数内实现快速收敛），但其系统层面的可扩展性一直是阻碍其在千卡、万卡集群替代 AdamW 的阿喀琉斯之踵。DMuon 是业界首个从系统通信拓扑与并行切分根基上彻底解决 Muon 扩展性难题的开创性工作。
5. 落地相关性：
对于负责搭建 GPU 训练集群、KubeFlow / Ray 编排平台的 AI Infra 工程师具有极高参考价值。传统训练调度只需关注整齐划一的 Tensor Parallelism 或 FSDP Bucket 通信，而 DMuon 证明了在新型算法驱动下，通过精细化重构通信图与动态所有权分配，可以在不对算法做任何近似妥协的前提下榨干硬件双层互连带宽。

---

#### 2. FastAFD: When Does Attention-FFN Disaggregation Pay on Rack-Scale NVLink?
- 中文译名：FastAFD：机架级 NVLink 体系下 Attention-FFN 解耦架构何时更具性价比？
- 链接：https://arxiv.org/abs/2611.07149
- 作者：Yichao Fu, Yuxuan Zhang, Minshen Zhang, Ruitian Wang, Junda Chen, Hao Zhang（共 6 位作者）
- 单位：加州大学圣迭戈分校（UCSD / 【知名实验室】）
- 分类：cs.DC, cs.LG
- 方向标签：C. AI Infra (推理系统 / MoE 解耦与机架级通信)
- 相关度：5/5

1. 核心贡献：
深入解答了当前 AI Infra 界最火热的架构争议：在 GB200 NVL72 这种机架级全互连（Rack-Scale NVLink）巨型系统中，将 MoE 模型的 Attention（KV Cache 密集型）与 FFN（专家计算密集型）物理拆分部署（AFD, Attention-FFN Disaggregation），相比成熟的宽专家并行（Wide EP）究竟是否有实际收益？作者构建了针对 GB200 调优的 FastAFD 推理引擎，并在 Qwen3、Qwen3.5、MiniMax-M2.5 上进行了实测，同时给出了误差小于 3% 的解析预测模型。
2. 原理解析：
在云原生容器微服务架构中，单体架构（Colocated）是将 Attention 和 Expert 容器混部在同一台 GPU 上；而 AFD 则类似微服务解耦，专门划拨一批 GPU 存 KV Cache 跑 Attention，另一批 GPU 专门加载 Expert 跑 FFN。
FastAFD 揭示了 AFD 产生净加速的数学本质——取决于三因子的乘积：
$$\text{Speedup} = \text{Batch Gain} \times \text{Overlap Gain} / \text{Disaggregation Cost}$$
- **Batch Gain（批次增益）**：Attention GPU 上完全不存 Expert 权重，省下的 HBM 全拿来做 KV Cache，单卡能够承载更大的 Batch 尺寸；
- **Overlap Gain（重叠增益）**：FastAFD 在两个 Microbatch 间做流水线掩盖——Microbatch A 在跑 Attention 的同时，Microbatch B 在 Expert GPU 上跑 MoE 计算，双流水线隐藏计算耗时；
- **Disaggregation Cost（解耦代价）**：为了部署 Expert 必须从集群中划扣出去专属的 GPU 数量。
只有当 Batch Gain 与 Overlap Gain 的乘积能覆盖分走 GPU 的代价时，AFD 才有正向收益。
3. 关键结论：
在 GB200 NVL72 实测下，FastAFD 在 Qwen3 上吞吐超越最优配置的 vLLM Wide EP 达 1.17 倍，在 Qwen3.5 上超越 1.16 倍，而在 MiniMax-M2.5 上二者持平。投机解码（Speculative Decoding）对「轻专家（Light-Expert）」模型提升尤为明显，能让 AFD 的领先优势再扩大 8%。作者还预测若未来将 Expert 部署在超高 SRAM 带宽的芯片（如 Groq LPX）上，AFD 理论加速比可跃升至 2.48 倍。代码已在 GitHub 开源。
4. 背景地位：
业界对 AFD 的评价两极分化严重（字节跳动万卡落地支持，但多项模拟器研究又称不划算）。该论文是首个在真实的 GB200 NVL72 机架级全互连硬件上，给出严格全量实验和清晰解析理论的权威标杆之作。
5. 落地相关性：
对 Kubernetes 调度器开发与 LLM 服务化编排工程师至关重要。论文明确指出：AFD 绝非万灵药，盲目把推理 Pod 拆分成 Attention Pod 和 Expert Pod 会导致算力碎片化与资源闲置；只有结合模型专家激活比例、Speculative Decoding 长度以及底层互连带宽（如 NVL72 vs 节点间 RoCE），通过其提供的预测公式评估后再做调度决策，才能避免集群吞吐倒退。

---

#### 3. Should You Split Decode? Disaggregation Across Future Models and Accelerators
- 中文译名：是否应该拆分 Decode？面向未来模型架构与加速器演进的推理解耦分析
- 链接：https://arxiv.org/abs/2611.08299
- 作者：Ramyad Hadidi
- 单位：独立研究（前 d-Matrix & Volantis Semiconductor / 【工业界】）
- 分类：cs.AR, cs.DC
- 方向标签：C. AI Infra & D. 性能建模 (集群推理拓扑 / Prefill-Decode 与 AFD 架构评估)
- 相关度：5/5

1. 核心贡献：
与 FastAFD 形成绝妙的学术对鸣！本文针对 Prefill/Decode 分离（P/D）以及在 Decode 阶段进一步进行 Attention/FFN 分离（P/D + AFD）提出了前瞻性系统建模工具 SiliconForge。通过涵盖 39 种加速器、6 类硬件架构原型（从 GPU、LPDDR 加速器到片上 SRAM 加速器）与不同互连 Fabric，在严格等功耗（SLO per kW）与等延迟约束下，深入论证了 AFD 在生产级落地中的潜在风险与边界条件。
2. 原理解析：
从分布式系统和服务网格视角来看，每增加一级物理拆分（Split），就如同在链路中增加了一道跨网络 RPC 边界：
- **网络开销与拓扑绑定**：AFD 要求每个 Token 在每一层 MoE 中都必须穿透一次解耦边界进行数据往返。以 DeepSeek-V3 为例，单请求生成需跨越解耦网络边界 116 次！
- **资源搁浅（Stranded Capacity）**：解耦后集群被迫划分为独立配额的资源池（Prefill 池、Attention 池、Expert 池）。由于不同用户 Prompt 长度变化多端，多级资源池极其容易导致某些池过载而另一些池算力闲置；
- **SLO per kW 现实**：将数据中心供电限制（kW）和严格的 TPOT（每 Token 生成耗时）考虑在内，单纯的 P/D 往往更紧凑高效；AFD 所谓的高吞吐往往只是因为省下内存能堆更大并发，但在工业生产关注的单位能耗良率（Goodput/kW）下，P/D 占据压倒性优势。
3. 关键结论：
在绝大多数公开发布的硬件配置与实际业务负载下，传统的 P/D 架构在综合能效（Goodput/kW）上均优于 P/D+AFD。AFD 仅在特定狭窄场景占优（例如小尺度 Scale-up 域中支撑极度庞大的超长上下文 KV 负载）。盲目过早锁定硬件解耦池比例会导致平均高达 36% 的有效吞吐损失，而通过动态弹性调整池配额可将损失降至 9%。
4. 背景地位：
这是对当前大模型服务化「过度解耦架构（Over-Disaggregation）」狂热思潮的一记当头棒喝。作者跳出单一硬件跑分的局部视角，以芯片架构师与基础设施总监的高维视角，为未来 2-3 年的集群基建投资提供了不可或缺的冷静分析。
5. 落地相关性：
对在 Kubernetes 上规划 RayCluster / vLLM 实例拓扑、进行容量规划（Capacity Planning）的基础设施架构师极具指导意义。在采购和切分昂贵加速器节点时，不应盲目为了跟随 AFD 新热点而重构调度流水线，而应优先做好弹性 P/D 的动态副本伸缩与算力混部。

---

#### 4. KOSMOS: Self-scheduling Persistent Kernels for Communication-Compute Overlap
- 中文译名：KOSMOS：基于自调度持久化 Kernel 实现通信与计算流水线重叠
- 链接：https://arxiv.org/abs/2611.07477
- 作者：Alexander Magro, Aristotle Martin, Ye Wang, Wen Chen
- 单位：超威半导体（AMD / 【工业界】）
- 分类：cs.DC, cs.AI, cs.LG, cs.PF
- 方向标签：C. AI Infra (训练系统 / 算子与通信计算重叠)
- 相关度：5/5

1. 核心贡献：
AMD 官方团队针对其最新 Instinct MI350X 和 MI355X GPU 架构，发布了自调度持久化算子库 KOSMOS。该库攻克了大模型训练中张量/序列并行（TP+SP）与专家并行（EP）通信堵塞关键路径的行业难题，消除了以往融合算子依赖静态角色切分或预设比例预测的僵化缺陷，在 Megatron-LM 和类 DeepSeek-V3/Qwen3 训练负载中取得显著端到端加速。
2. 原理解析：
大模型分布式训练常通过 AllGather / ReduceScatter 交换张量，通常做法是用单独的 CUDA Stream 甚至 CPU 线程按经验比例去交错 launch 计算与通信算子，这就像固定的 Cron 定时任务，稍微遇到网络抖动或算子耗时波动就会出现大段 GPU 计算单元（CU/SM）空转气泡。
KOSMOS 的解决思路是「Kernel 内部的反应式工作窃取（Work-Stealing）调度器」：
- **持久化工作组（Persistent Workgroups）**：在 GPU 上启动常驻的 Workgroup 线程块，生命周期贯穿整个算子；
- **就绪驱动自适应角色切换**：Workgroup 内部维护基于消费者需求排序的就绪队列。当外部通信数据未到达时，线程组全量投入本地 GEMM 矩阵计算；一旦网络数据块进入就绪队列，线程组自动感知并切入规约/搬运角色；
- **全链路算子大融合**：将 Transformer 层的每个 TP+SP 集合通信与 GEMM 融为一体，且将 MoE 整个专家层（从 Router 路由分发到最终 Fold 规约）压缩至单次方向 launch 完成。
3. 关键结论：
在 AMD Instinct MI350X / MI355X GPU 实测中，KOSMOS 在 Megatron-LM 端到端训练中为 TP+SP 带来了 1.10–1.28 倍（BF16）和 1.10–1.25 倍（MXFP8）的加速；在 DeepSeek-V3 和 Qwen3-235B 的模拟专家训练代理任务中，比业界标杆 DeepEP 加速达到惊人的 1.29–1.83 倍。
4. 背景地位：
标志着持久化 Kernel（Persistent Kernels）技术从以往小规模学术原型正式跨入大模型千亿参数工业级训练主流舞台，同时展示了 AMD ROCm 生态在底层算子通信重叠领域正面硬战 NVIDIA 并取得局部领先的技术实力。
5. 落地相关性：
对于搭建 AMD GPU 训练集群、优化分布式训练底座的工程师是一场及时雨。KOSMOS 无需修改上层复杂的调度配置和参数调优，以即插即用的持久化算子方式直接吞掉通信开销，对推动异构算力（国产加速器/AMD）进入生产训练集群具有极强的标杆示范意义。

---

#### 5. Characterizing CUDA Locality Domains on Blackwell GPUs
- 中文译名：深入剖析 NVIDIA Blackwell GPU 上的 CUDA 局部性域（Locality Domains）特性
- 链接：https://arxiv.org/abs/2611.07535
- 作者：Rocky Wang, Joyce Zhou, Keith Jiang, Jason Zhao
- 单位：Scitix AI (【工业界】)
- 分类：cs.DC
- 方向标签：C. AI Infra & D. 性能与可靠性 (GPU 底层拓扑、跨 Die 通信与驱动优化)
- 相关度：5/5

1. 核心贡献：
首篇全面披露并深入实测 NVIDIA 最新 Blackwell 双 Die 架构（B300 GPU）与 CUDA 13.4 全新核心特性——局部性域（Locality Domain, LD）的底层系统白皮书。报告详尽测定了单节点 8 卡 B300 跨 Die 访问的物理性能代价，并精准定位出当前 NVIDIA 官方 GPU 驱动内核模块中存在的一个严重内存分配瓶颈，向 NVIDIA 官方提交了修复代码，实现了分配开销 7 到 10 倍的巨幅缩减。
2. 原理解析：
NVIDIA Blackwell 架构的核心秘密在于每颗 GPU 封装内包含了两个独立的 Compute Die。这与 CPU 的多 Socket NUMA 架构如出一辙：
- **硬件拓扑非对称性**：访问同 Die 的 HBM 延迟低、带宽满血；而跨 Die 访问 HBM 延迟高达 193.4 ns，带宽骤降至基线的 27%！但神奇的是，一旦数据命中对方 Die 的 L2 缓存，跨 Die 延迟几乎可以忽略不计；
- **CUDA 13.4 LD 机制**：如同 Linux 的 `cgroup cpuset` 与 NUMA 绑定，CUDA 13.4 允许开发者通过虚拟内存管理（VMM）将内存精准绑定到指定 Die，并通过 Green Context 将算力限制在单 Die 的 70 个 SM 上；
- **驱动内核 Bug 诊断**：实测发现当申请内存超过 32MB 时，由于过度的屏障（Barrier）和 TLB 无效化操作，驱动会产生不可容忍的阻塞延迟。作者通过重构 GPU 内核驱动模块成功消除了该阻碍。
3. 关键结论：
利用 Die 感知的局部性域优化，在 NCCL 2.32.3 AllGather 集合通信上提速达 43.5%，nvbandwidth 设备内跨 Die 搬运提速 111.3%，DeepGEMM 专家并行算子提速 37%。针对驱动的补丁修复无需修改任何用户代码，即刻抹除大块内存分配的严重抖动。
4. 背景地位：
Blackwell 是当前全球 AI Infra 的兵家必争之地。本报告揭示了未来 2-3 年面向 Blackwell 编写高性能系统软件的核心法则：不可再将单颗 GPU 视为扁平黑盒，必须将其视作双节点 NUMA 拓扑来编排。
5. 落地相关性：
针对从事底层 GPU 算子编写、NCCL 调优以及 Kubernetes 容器设备插件（Device Plugin）研发的工程师极具冲击力。未来的 K8s GPU 拓扑感知调度不仅要看 Node 与 PCIe/NVLink 拓扑，更要在容器/Pod 内部对 Blackwell 的 Die 级 Locality Domain 进行资源拓扑感知编排。

---

#### 6. FlashOffloading: Low-Latency KV Cache Offloading for Long-Context LLM Serving
- 中文译名：FlashOffloading：面向长上下文大模型推理服务的低延迟 KV Cache 主机卸载架构
- 链接：https://arxiv.org/abs/2611.07542
- 作者：Xuan Wang, Zhuanhao Wu, Tingzhu Fang, Xushi Li, Sicheng Zhang 等（共 20 位作者，通讯作者：Cheng Li）
- 单位：华为技术有限公司【工业界】、华为昇腾计算【工业界】、上海交通大学【知名实验室】
- 分类：cs.AI, cs.DC
- 方向标签：C. AI Infra (推理系统 / KV Cache 卸载与 PD 分离)
- 相关度：5/5

1. 核心贡献：
华为与上海交大联手打造并完全开源的工业级长上下文推理系统 FlashOffloading。该系统针对大模型长上下文推理中 HBM 容量墙导致的低并发瓶颈，颠覆了以往「仅将冷数据部分换出」的折中做法，在 Prefill 与 Decode 全阶段实现端到端向 Host DRAM 全量卸载 KV Cache，并已直接合并入 `vLLM-ascend` 官方生产版本（v0.30.0）。
2. 原理解析：
将 KV Cache 卸载到主机内存并不是新想法，但过去一直受制于 PCIe/Host 搬运延迟，导致整体推理 TPOT 严重超时。FlashOffloading 的突破在于四大协同机制：
- **Prefill 阶段的滚动 HBM 缓存（Rolling HBM Cache）**：Prefill 不需要全程保留全量 KV，只需保留当前窗口的 KV，其余随算随排入主机内存；
- **Decode 阶段的热缓存（Hot Cache）**：结合动态注意力稀疏特性维护微型 HBM 热区，抵消大部分逐步访问；
- **反向稀疏索引（Reverse Sparse Index）**：彻底消除了传统缓存管理在 Cache Miss 时的昂贵查找开销，做到零额外命中判定损耗；
- **计算-加载重叠 Kernel（Compute-Load Overlapped Kernel）**：利用投机解码（Speculative Decoding）或 MTP（多 Token 预测）的算力间隙，将后续 Token 所需的 KV 数据提前通过异步 DMA 流水加载。
3. 关键结论：
在华为昇腾 910C 芯片构建的 Prefill-Decode (PD) 分离集群上，针对 GLM-5.2 模型与 MTP3 投机解码，在严苛的 30ms TPOT（每 Token 吐字延迟）SLO 约束下，FlashOffloading 将 Prefill 吞吐提升高达 1.38 倍，Decode 吞吐提升高达 1.91 倍。
4. 背景地位：
国产 AI 算力底座在长序列长上下文生产场景下的标杆之作。不仅给出了完整的系统设计，更关键的是代码完全开源且融入了主流 vLLM 生态分支，具备立竿见影的工程落地成熟度。
5. 落地相关性：
对于正在使用昇腾 NPU 或考虑在国产算力基础设施上部署十万级长上下文 RAG、Agent 服务的云原生团队是重磅利好。可直接通过升级 vLLM-ascend 容器镜像获得并发翻倍收益，极大地降低了对昂贵板载 HBM 显存容量的硬性依赖。

---

#### 7. OpenRDMA: A GPU-Native Multi-Path Reliable RDMA Transport Architecture
- 中文译名：OpenRDMA：一种 GPU 原生的多路径高可靠 RDMA 传输架构
- 链接：https://arxiv.org/abs/2611.07559
- 作者：Ziheng Ji, Chunyu Liu, Weihao Peng, Mingheng Mi, Pu Wang, Hai Zhang
- 单位：香港大学、西安交通大学、北京邮电大学、琶洲实验室
- 分类：cs.AR, cs.DC
- 方向标签：C. AI Infra & B. 编排调度 (GPU 原生通信、高性能网络与 RDMA)
- 相关度：5/5

1. 核心贡献：
针对大规模 AI 集群中网络通信成为算力死锁瓶颈的现状，提出了面向 GPU 极度友好的开源多路径可靠 RDMA 传输架构 OpenRDMA。该架构彻底解决了传统 GPUDirect RDMA 控制面依赖 CPU 介入、以及 IBGDA（InfiniBand GPUDirect Async）由 GPU 组装工作队列项（WQE）严重占用昂贵 SM 算力与内存带宽的痛点，打造了极致精炼的通信控制协议。
2. 原理解析：
如果把 GPU 发送网络包比作容器调用 CNI 网络插件：
- **8 字节轻量 Doorbell**：传统的网络提交需要 GPU 花费大量通用寄存器和指令去封装复杂的网络描述符；OpenRDMA 设计了极简门铃协议，GPU 只需向专用 FPGA 网卡写入一个 8 字节的 Token，网卡硬件根据预先配置的上下文自动在硬件内重构完整 WQE，GPU 耗时仅需纳秒级；
- **多路径可靠连接（MRC）与乱序吸收**：支持逐包（Per-packet）多路径喷淋路由以最大化网络交换矩阵吞吐，硬件层通过选择性重传、有序 DMA 落地和 GPU 可见标志位轮询，向上层暴露完全线性的可靠数据接口；
- **软硬件协同容错**：FPGA 只负责高频极速的数据通路，复杂的超时判定、连接状态机跟踪与重传控制则交由主机 CPU 慢速软件栈兜底，使低成本 Board-level FPGA 也能完美胜任。
3. 关键结论：
该架构大幅减少了网卡状态维护的硬件资源占用，同时将 GPU 提交网络的控制开销压降到理论物理极限。项目已开源，在 GitHub 获得了广泛关注，提供了下一代原生 GPU 集群网络的全新范式。
4. 背景地位：
在后 InfiniBand 时代与超以太网联盟（Ultra Ethernet Consortium, UEC）加速落地的背景下，OpenRDMA 代表了学术界与开源界对由 NVIDIA 独家主导的私有网络栈（IBGDA/SHARP）的有力突围。
5. 落地相关性：
对从事云原生网络（CNI、RoCEv2 交换网络调优）、RDMA 容器网络设备插件研发的架构师提供了极佳的技术路线指引。轻量 Doorbell 思想极有可能成为未来自研网卡与大规模集群通信基础设施的标准配置。

---

#### 8. Resource-Efficient Reinforcement Learning Post-Training through Elastic Expert Parallelism
- 中文译名：FlexFloor：通过弹性专家并行实现资源高效的大模型强化学习后训练
- 链接：https://arxiv.org/abs/2611.06984
- 作者：Jia Wei, Ziyi Qiu, Yi Xu, Xuehai Qian
- 单位：清华大学计算机系（【知名实验室】）
- 分类：cs.AI, cs.DC
- 方向标签：C. AI Infra & B. 编排与调度 (强化学习后训练 / 集群弹性资源释放)
- 相关度：5/5

1. 核心贡献：
清华大学钱学海团队针对当前大模型强化学习后训练（RLHF / PPO / GRPO）中推理采样（Rollout）阶段巨大的算力浪费，提出了弹性专家并行系统 FlexFloor。通过在同步生成期间动态缩容、提前释放计算节点，在业界主流强化学习框架 `verl` 之上实现了每单位计算时间提升 65.4% 的 Token 生成效率，吞吐跃升 52.74%。
2. 原理解析：
大模型通过 RL 探索解题（如 DeepSeek-R1 式的长思维链推理）时，不同 Prompt 生成回答的长度差异极大（尾延迟极长）。在 MoE 模型部署专家并行（EP）时，生成得快的 Worker 虽然自己早早就写完了答案，但因为其本地卡上存放了其他还在生成的 Worker 所需要的专家模型权重（Expert），导致它必须在原地干等、无法下线退场！基线系统中整整三分之一的 GPU 时间被耗费在这种「无所事事的陪跑」中。
FlexFloor 提出了类似 Kubernetes 优雅下线与动态排水（Drain）的调度算法：
- **配额感知 Prompt 放置**：利用历史响应长度预测，调度器不再单纯追求配对均衡，而是以「促成整组尽早达成完成法定人数（Quorum）」为目标聚类编排输入；
- **渐进式节点释放与专家保活**：在长文本生成的后半程，逐步安全剥离那些已经完成自身任务的 Worker 节点，并动态调整通信域与路由表，确保留守的存活 Worker（Survivors）依然能访问完整专家并拥有充足的 KV Cache；
- **零破坏动态重构**：在不破坏分布式集合通信顺序的前提下完成世界拓扑（Distributed World）的动态切换与重组。
3. 关键结论：
在基于 `verl` 框架的端到端评测中，FlexFloor 比原生 baseline 在每 GPU 占用秒数下产出多 65.40% 的 Token，生成吞吐提升 52.74%，且在采样质量与奖励得分（Reward / pass@1）上完全无损。
4. 背景地位：
大模型研发重心正从 Pre-training 全面转向以强化学习为核心的 Post-training（后训练）。FlexFloor 是业界首个深入 MoE 专家并行底层、解决 RL 生成长尾阻塞的系统级编排调度方案。
5. 落地相关性：
对于管理大模型后训练集群、K8s RayJob / Volcano 调度的工程师具有立竿见影的实用价值。通过弹性资源早期释放，省下的 GPU 节点可以立即被 K8s 回收用于下一批 Prompt 训练或作为推理服务，大幅削减千卡 RL 集群的闲置浪费。

---

#### 9. Memory Fit: Architectural Support for Page Placement by Learning Models of Good Behavior
- 中文译名：Memory Fit：通过学习良性行为模型实现异构内存页面放置的架构支持
- 链接：https://arxiv.org/abs/2611.07506
- 作者：Chun Deng, Hui Sub Shim, Evan Laufer, Anna Eaton, David Tennenhouse 等（共 7 位作者，导师：Philip Levis）
- 单位：斯坦福大学【知名实验室】、谷歌【工业界】
- 分类：cs.OS, cs.AR
- 方向标签：A. 容器与运行时 & D. 性能与可靠性 (操作系统内核 / CXL 异构内存分层页面放置)
- 相关度：5/5

1. 核心贡献：
斯坦福大学与谷歌团队针对云原生服务器中日益普及的多层异构内存（如 本地 DRAM、zswap 压缩内存、CXL 扩展内存条以及非易失相变内存 PCM），提出了软硬件协同的页面放置抽象 Memory Fit。在 Linux 6.6 内核与开源 RISC-V 处理器（BOOMv3）上完成了端到端实现，相较于当前 Linux 内核的主流分层策略 TPP（Tiered Memory Placement），将性能差距挽回率提升了 2.2 至 3.8 倍。
2. 原理解析：
在云原生容器节点中，为了降低成本，集群大量混部了 CXL 慢速内存与标准 DRAM。Linux 内核决定页面该放在快内存还是踢到慢内存，以往只能依靠粗糙的页面 Access Bit 标记，或者耗费高昂 CPU 中断进行软件采样，经常导致高频热数据误杀。
Memory Fit 的思路是将复杂的策略留给内核，而在硬件层实现超轻量抽象：
- **契合度度量（Memory Fit）**：硬件实时评估每个 4KiB 页面与不同介质内存的契合度，解耦「亲和度度量机制」与内核「何时搬移的调度策略」；
- **软轨迹匹配算法（STM）**：硬件学习每种内存的「良性访问模型」，将页面的轻量访问轨迹与其比对，每个 4KiB 页面仅需 64 位的硬件状态开销；
- **极简内核开销**：在主内存每次访问时硬件自动更新，给 Linux 6.6 内核带来的中断处理开销仅有微不足道的 1.2%。
3. 关键结论：
在通用指针追踪测试（GUPS）中，Memory Fit 相比 Linux 原生 TPP 挽回了 2.2–3.8 倍的性能差距；在内存容量对半开（DRAM : PCM = 1:1）的 Redis 生产级负载下，Memory Fit 挽回了高达 80% 的理论最优性能差距，而 Linux TPP 仅能挽回 19%。
4. 背景地位：
操作系统的顶级硬核成果（出自 Philip Levis 顶尖系统实验室）。彻底攻克了自 CXL 概念诞生以来，系统软件在分层内存管理上「精度差」与「软件开销大」不可兼得的世纪难题。
5. 落地相关性：
对于维护 Kubernetes 节点底层 OS、cgroup 内存超卖（Memory Overcommit）、以及利用 CXL 扩展池做成本优化的云计算运维与内核研发团队是必读之作。该技术一旦随硬件固化，将使容器无感平替使用廉价 CXL 内存，大幅削减数据中心内存 TCO。

---

#### 10. NUMA-Torch: Compiler-Driven NUMA-Aware LLM Prefill on Multi-Socket CPUs
- 中文译名：NUMA-Torch：编译器驱动的多路 CPU NUMA 感知大模型 Prefill 吞吐优化
- 链接：https://arxiv.org/abs/2611.07105
- 作者：Thisara Rathnayaka Weerakoon, Ishan Dewpura, Niman Ransindu, Shavin Anjitha, Tharindu R. Patabandi, Sanath Jayasena
- 单位：莫拉图瓦大学（University of Moratuwa）、独立研究者（San Jose, CA）
- 分类：cs.DC, cs.PF, cs.PL
- 方向标签：C. AI Infra & B. 编排与调度 (多 Socket CPU NUMA 感知 / 亲和性调度 / 编译器优化)
- 相关度：4/5

1. 核心贡献：
针对无 GPU 或 GPU 紧缺的私有化服务器场景，深入攻克了多路（Multi-Socket）CPU 运行大模型 Prefill 阶段内存带宽瓶颈问题。提出了首个编译器层级驱动的 NUMA 感知方案 NUMA-Torch，将该能力直接注入 PyTorch 官方编译器 TorchInductor 中，消除跨 Socket 访问开销，在双路与四路服务器上取得了最高 2.63 倍的 Prefill 加速。
2. 原理解析：
大模型 Prefill 阶段权重规模庞大，无法驻留 CPU L3 Cache，性能被本地内存总线带宽钉死在 Roofline 的倾斜壁上。传统的 PyTorch / TorchInductor 编译时是「NUMA 盲（NUMA-Blind）」的，它把所有物理核当作统一的平坦线程池，导致大量核心频繁通过极慢的跨 Socket 互连总线（如 Intel UPI）跨节点读取权重，有效带宽腰斩。
NUMA-Torch 将云原生 NUMA 拓扑调优下沉到了编译器中间件：
- **NUMA 感知张量并行（NUMA-TP）**：在编译器内部直接将每个 CPU Socket 视作一个独立的「GPU 卡（Tensor-Parallel Partition）」，对权重张量在内存分配时就强制做 Socket 本地切分；
- **严格亲和性线程与内存绑定**：结合 CPU Affinity 调度，将工作线程池严格钉死在对应 Socket 的本地物理核心上，内存分配同样使用本地物理 Bank，彻底消除跨 Socket UPI 流量。
3. 关键结论：
在双路 Haswell 服务器上达到 2.63 倍加速，双路 Cascade Lake 上提速 1.87 倍，在四路 Haswell-EX 大型服务器上提速 2.27 倍，模型覆盖了 GPT-2、BERT 以及结合 MQA 与 GeGLU 的最新 Gemma 3 模型。
4. 背景地位：
填补了 PyTorch 官方 TorchInductor 编译器在 CPU 复杂拓扑感知方面的空白，首次在标准编译通道内原生实现了硬件拓扑亲和性注入。
5. 落地相关性：
与 Kubernetes 的 `TopologyManager` 和 `CPUManager` 的 `static` 策略完美契合。在私有化部署、金融安全或端侧边缘节点中，由于合规或成本限制无法配备 GPU，采用 NUMA-Torch 配合容器 NUMA 绑核编排，可以让传统通用 CPU 服务器跑大模型的吞吐翻倍。

---

#### 11. StrataFlux: Memory-Hierarchy-Native Low-Bit LLM Inference
- 中文译名：StrataFlux：原生结合多级内存层级结构的低比特大模型流式推理系统
- 链接：https://arxiv.org/abs/2611.08363
- 作者：Jake Hyun, Ziyu Zhao, Jae-sun Seo, Mohamed S. Abdelfattah
- 单位：康奈尔大学（Cornell University / 【知名实验室】）、卡耐基梅隆大学（CMU / 【知名实验室】）
- 分类：cs.LG, cs.DC
- 方向标签：C. AI Infra (显存与存储分级管理 / 低比特流式精度补偿)
- 相关度：4/5

1. 核心贡献：
康奈尔与 CMU 团队提出了面向多级内存层级（GPU HBM / Host RAM / NVMe SSD）的原生低比特大模型推理框架 StrataFlux。该框架打破了「要么低比特量化损失精度、要么全精度卸载拖慢吞吐」的二元对立，通过选择性精度流式加载（Selective Precision Streaming），在维持极低显存占用的同时挽回了量化掉的精度。
2. 原理解析：
大模型推理需要兼顾显存占用、延迟和准确率。直接压到 2-bit 吞吐极快但模型容易变胡言乱语；而以往通过 offloading 从主机慢速总线加载完整精度又会阻塞计算流水线。
StrataFlux 构建了类似分布式存储中「分级冷热存储与增量同步」的精妙架构：
- **极小驻留基座（Resident Base）**：GPU 显存中常驻 2–3 bit 的量化模型基座与精简 KV Cache，为绝大多数常规 Token 生成提供全速的高带宽访存；
- **选择性精度流式传输**：廉价的大容量介质（主机内存或 SSD）存储高精度的「残差增量补丁（Refinement）」。系统根据 Token 的不确定性与敏感度，仅按需拉取极少量的增量精度位；
- **传输与计算异步流水覆盖**：拉取过程在后台异步执行，且拉取到的精度信息在跨解码步间缓存复用，完全避免了生成阻塞。
3. 关键结论：
在消费级单卡 RTX 5090 上，运行 2-bit Llama-3.1-8B-Instruct 时，StrataFlux 在保持 95.4% 的超高吞吐同时，将困惑度大幅改善；在 Qwen3-8B（2-bit 权重与 2-bit KV）评测中，AIME 竞赛解题准确率从 11.0% 飙升至 47.1%！在 128K 超长上下文下，其 3-bit 权重 + 2-bit KV 的配置仅消耗 vLLM（4-bit AWQ + 8-bit KV）约一半的显存，达到了完全相同的速度与准确率。
4. 背景地位：
大模型部署正在迈入后量化时代。StrataFlux 开创性地将「分级存储（Tiering Storage）」与「残差量化（Residual Quantization）」紧密结合，为受限于显存容量的边缘计算与单卡大并发服务指明了全新方向。
5. 落地相关性：
对于在云上使用廉价 GPU 实例（如消费卡或中小显存卡）提供长上下文推理服务的工程师极具吸引力。原本需要 80G A100/H100 才能撑起的 128K 上下文推理，现在借助 StrataFlux 和 Host 内存扩展即可在便宜得多的硬件上稳健运行。

---

#### 12. ZYFA: Speed and Accuracy of FP8 FlashAttention on AMD CDNA4
- 中文译名：ZYFA：AMD CDNA4 架构上 FP8 FlashAttention 算子的速度与数值精度优化
- 链接：https://arxiv.org/abs/2611.07496
- 作者：Quentin Anthony, Ganesh Bikshandi, Praneeth Medepalli, Stephen Ebert
- 单位：Zyphra (【工业界】)
- 分类：cs.DC, cs.LG
- 方向标签：C. AI Infra (算子与系统层优化 / AMD CDNA4 FP8 FlashAttention 与 MLA)
- 相关度：4/5

1. 核心贡献：
工业界团队 Zyphra 针对 AMD 最新一代 CDNA4 架构（Instinct MI355X）推出了完全开源的 FP8 FlashAttention 预填充核心 ZYFA。针对 MI355X 缺少硬件指令完成追踪、向量单元与矩阵单元算力不匹配等硬件特性展开深度软硬协同设计，大幅超越 AMD 官方核心库 AITER，且完美支持 DeepSeek 格式的多头潜在注意力（MLA）。
2. 原理解析：
虽然 FP8 矩阵指令能提供两倍于 BF16 的峰值算力，但在 FlashAttention 算子内部，两次矩阵乘法中间夹着的 Softmax 却跑在并未被 FP8 加速的通用向量单元上。在 AMD MI355X 硬件上，AMD 官方库 AITER 在 32K 上下文下仅能达到 39% 的 FP8 矩阵峰值利用率。此外，MI355X 不像 NVIDIA Hopper/Blackwell 那样在硬件层面追踪矩阵指令完成，指令乱序和交错完全依赖软件排布。
ZYFA 提出了三大绝技：
- **乘加与整数转换替代指数计算**：直接利用 FP8 的位模式特性（Bit Pattern 本质上近似对数），通过一次乘加和整数转换直接求出 Softmax 概率，避开昂贵复杂的向量 exp 运算；
- **Ping-Pong 线程调度流水线**：精细编排汇编级指令，当一组线程执行矩阵乘法时，另一组线程交错计算 Softmax，将向量耗时完全掩盖；
- **2的幂次缩放与归一化**：在舍入前将概率块做 $2^k$ 缩放，极大抑制了 FP8 量化噪声。
3. 关键结论：
在真实模型激活值实测下，ZYFA 相比 AMD 官方 AITER 库吞吐提升 1.16 至 1.76 倍；在 32K 长度基准测试下达 1.26–1.37 倍；而在 DeepSeek 风格的 MLA 算子上提速高达 1.99 倍！同时数值误差比 AITER 降低 62%–78%，达到与 Triton / Composable Kernel 相当的数值稳定性。代码已开源。
4. 背景地位：
大模型前沿 Infra 正在全面向 FP8 / MXFP8 演进，而针对非英伟达平台（AMD Instinct / 国产算力）的高性能 FP8 注意力算子一直是生态卡脖子痛点。ZYFA 为开源社区提供了教科书级的顶级 GPU 算子优化实践。
5. 落地相关性：
对于部署 AMD 算力集群、运行 DeepSeek-V3 / R1 推理加速的团队而言是极其关键的底层组件。可直接替换底层 FlashAttention 依赖，即刻将超长上下文 Prefill 阶段的吞吐压榨提升数成。

---

### 其他论文（相关度 ≤2）

以下为今日抓取的其余 26 篇候选论文，主要属于纯理论分布式计算、小众领域专用建模、非系统向应用及密码学，相关度较低，在此简要列出以备参考：

1. **Modular Parameterized Model Checking of Threshold-Based Distributed Algorithms** (cs.DC)
   - 链接：https://arxiv.org/abs/2611.07919 | 相关度：2/5
   - 简评：提出针对基于阈值的分布式容错一致性算法的模块化模型检测与形式化验证方法。
2. **ZeroRAG: Adaptive Semantic Peer Routing for Decentralized Retrieval-Augmented Generation** (cs.DC, cs.AI)
   - 链接：https://arxiv.org/abs/2611.07928 | 相关度：2/5
   - 简评：基于非结构化 P2P 覆盖网络与局部广告缓存实现的去中心化文档语义检索与 RAG 路由层。
3. **SEER: A Scalable Event-Driven Runtime for Parallel Execution of Multi-Agent Reinforcement Learning Environments** (cs.DC, cs.MA)
   - 链接：https://arxiv.org/abs/2611.07996 | 相关度：2/5
   - 简评：为多智能体强化学习环境设计的事件驱动并行运行时，采用 CAS 双层事件队列解决 CPU 侧环境交互瓶颈。
4. **Precision - Preserving Subtensor Inference for a 22B Joint Audio - Video Generator under a Fixed GPU Working Set** (cs.DC)
   - 链接：https://arxiv.org/abs/2611.08023 | 相关度：2/5
   - 简评：面向 22B 音视频大模型在严格 3GB 显存预算下的固定内存池子张量流式推理方案。
5. **xDSL-CCPP: An alternative code generator for atmospheric modelling** (cs.DC)
   - 链接：https://arxiv.org/abs/2611.08060 | 相关度：1/5
   - 简评：针对气象与物理科学计算领域的专用 DSL 代码生成工具。
6. **Quantum Advantage in Local Certification of Graph Properties** (cs.DC)
   - 链接：https://arxiv.org/abs/2611.08076 | 相关度：1/5
   - 简评：分布式网络局部认证图属性的纯量子算法理论研究。
7. **Post-Quantum Authentication of IoT Data on Ethereum: Signatures, the Calldata Floor, and Device-Signed Merkle Roots** (cs.DC)
   - 链接：https://arxiv.org/abs/2611.08108 | 相关度：1/5
   - 简评：基于以太坊的后量子物联网数据认证与 Calldata 优化方案。
8. **The Two-Ledger Model: Transaction-Grain Cost Accounting for Multi-Agent AI Systems Across Clouds, Models, and Systems of Record** (cs.DC, cs.AI)
   - 链接：https://arxiv.org/abs/2611.06989 | 相关度：2/5
   - 简评：跨云与多模型 Multi-Agent 系统的交易粒度成本核算双账本模型。
9. **Beyond Proof of Possession: A Relational Theory of Authority** (cs.DC, cs.CR)
   - 链接：https://arxiv.org/abs/2611.07159 | 相关度：1/5
   - 简评：分布式系统权限与凭证关系的形式化安全理论。
10. **Full Provenance on the COSS Causal Axis: An Event-Level Closure of Causal Attribution and Confused-Deputy Exclusion** (cs.DC, cs.CR)
    - 链接：https://arxiv.org/abs/2611.07164 | 相关度：1/5
    - 简评：分布式因果事件闭包溯源与混淆代理排除的理论分析。
11. **GUARDTs: Decentralized Access Control for Replicated Data Types** (cs.DC, cs.PL)
    - 链接：https://arxiv.org/abs/2611.08083 | 相关度：2/5
    - 简评：针对拜占庭容错无冲突复制数据类型（CRDT）的细粒度去中心化访问控制扩展。
12. **GINGER: Spicing Up Graph-Based Vector Search** (cs.DC, cs.IR)
    - 链接：https://arxiv.org/abs/2611.08306 | 相关度：2/5
    - 简评：Google 开源的高性能图基向量检索 C++ 库，提出 NTQ 双层量化与 AdaptiveGap 压缩算法。
13. **Measured Coupling for Parallel Decoding in Diffusion Language Models** (cs.DC, cs.CL, cs.PF)
    - 链接：https://arxiv.org/abs/2611.08307 | 相关度：2/5
    - 简评：利用前向传播内的内生耦合度量指导扩散语言模型并行生成 Token 的算法改进。
14. **Capability Gain from ISA to Shared Execution on AMD MI300A and MI250X** (cs.DC)
    - 链接：https://arxiv.org/abs/2611.07198 | 相关度：2/5
    - 简评：评估 AMD MI300A/MI250X 从指令级峰值到多流并发共享执行层面的性能折损基准测试。
15. **Not All Loops Cost the Same: Phase-Dependent Depth for Serving Looped Transformers** (cs.DC)
    - 链接：https://arxiv.org/abs/2611.07211 | 相关度：2/5
    - 简评：LoopDuet：在 vLLM 中为循环 Transformer（Looped Transformers）实现阶段动态深度的推理调度框架。
16. **LowRAM: Low-Rank Keys and Amortised Values for Composable KV Cache Compression at Test-Time** (cs.LG, cs.CL)
    - 链接：https://arxiv.org/abs/2611.07025 | 相关度：2/5
    - 简评：结合低秩 Key 与 Value 摊销预测的测试期 KV Cache 压缩算法，可与量化和驱逐组合使用。
17. **The Gating Mechanism of KV Cache Eviction** (cs.CL)
    - 链接：https://arxiv.org/abs/2611.07605 | 相关度：2/5
    - 简评：大模型推理中基于注意力门控机制的 KV Cache 驱逐策略与冗余度分析。
18. **TACT-KV: Tri-Axis Cosine Transform for Compressing Volumetric KV Caches in Medical VLMs** (cs.CV, cs.LG)
    - 链接：https://arxiv.org/abs/2611.07593 | 相关度：2/5
    - 简评：面向 3D 医学影像大模型的三轴离散余弦变换 KV Cache 频域压缩方案。
19. **Energy-Aware Open-Vocabulary Detection Scheduling for Low-Power Robotic Autonomy** (cs.RO, cs.AI)
    - 链接：https://arxiv.org/abs/2611.07663 | 相关度：2/5
    - 简评：基于机器人运动状态感知自适应调节开放词汇目标检测频率以节省边缘能耗的调度策略。
20. **$L_1$ versus $L_2$ Clustering: When Does the Choice of Norm Matter?** (cs.DS)
    - 链接：https://arxiv.org/abs/2611.07248 | 相关度：1/5
    - 简评：聚类算法中 L1 范数与 L2 范数近似保证可移植性的理论证明。
21. **Breaking $\\mathsf{TraintoDefend}$ via Adaptive Neuron Clustering in Cryptanalytic Model Extraction** (cs.CR)
    - 链接：https://arxiv.org/abs/2611.07370 | 相关度：1/5
    - 简评：通过自适应神经元聚类逆向窃取深度学习模型参数的安全攻防研究。
22. **Closed-Loop Physics-Based Manipulation Evaluation at a Commodity Price: What 4.4 L4 GPU hours at $3.50 Buys You** (cs.RO)
    - 链接：https://arxiv.org/abs/2611.07441 | 相关度：1/5
    - 简评：探讨利用少量廉价 L4 GPU 云端算力进行机器人物理操作闭环评估的工程实践。
23. **AMORT-V1: Checkpointed Post-Quantum Attestation for Industrial Controllers** (cs.CR)
    - 链接：https://arxiv.org/abs/2611.07476 | 相关度：1/5
    - 简评：工业 PLC 控制器基于检查点的后量子远程可信认证方案。
24. **Graph learning-assisted logic-based Benders decomposition for distributionally robust in-station train rescheduling under disruptions** (cs.AI)
    - 链接：https://arxiv.org/abs/2611.07520 | 相关度：1/5
    - 简评：结合图神经网络与 Benders 分解的铁路车站列车突发延误重调度运筹优化。
25. **Adversarially Robust Streaming Algorithms for $(k, z)$-Clustering** (cs.DS)
    - 链接：https://arxiv.org/abs/2611.07678 | 相关度：1/5
    - 简评：几何动态数据流中针对对抗攻击的鲁棒流式聚类算法理论分析。
26. **Credibility Clustering for Experience Rating: An Automated Approach to Risk Group Allocation in Group Life Insurance** (q-fin.RM, cs.LG)
    - 链接：https://arxiv.org/abs/2611.07110 | 相关度：1/5
    - 简评：结合信度理论与 k-means 聚类的团体人寿保险风险群组自动化分类方案。

---

### 今日趋势小结

纵观今日系统方向的全部新出论文，AI 基础设施与云原生体系的演进呈现出三个极为清晰的底层趋势：

1. **解耦（Disaggregation）进入深水区，架构评测走向理性与全生命周期能效化**：
   从过去的单体服务到 Prefill-Decode (P/D) 分离，业界正在热议 Attention-FFN Disaggregation (AFD)。今天的两篇重磅论文（FastAFD 与 SiliconForge）从正反两个维度给出了最为详尽的答案：在 GB200 NVL72 这类机架级高速总线赋能下，AFD 在特定轻专家模型上确实能带来 15% 以上吞吐提升；但在更广泛的生产约束下，细粒度解耦会引入 100+ 次网络穿透和严重的算力碎片化。大模型服务化切忌「为了解耦而解耦」，容器与集群调度器必须结合模型专家激活率与物理网络域动态决策。

2. **跨 Die / 跨 Socket / 跨介质的「非均匀局部性（NUMA）」成为算子与系统的通用法则**：
   无论是在单卡内的 NVIDIA Blackwell 双 Die 架构（CUDA 13.4 Locality Domains），还是在服务器内的多路 CPU（NUMA-Torch），抑或是主存层面的 CXL / DRAM 异构内存分层（Memory Fit），计算与内存的物理边界正在剧烈割裂。传统「假定内存完全均质统一」的调度假设已彻底失效。未来的 Kubernetes 调度器、操作系统内核以及底层算子，必须实现对 Die、Socket、CXL 拓扑的全栈端到端感知。

3. **通信与计算重叠向「硬件原生轻量化」与「自调度持久化」极速演进**：
   传统利用 CPU 线程或静态 CUDA Stream 交错通信与计算的方式正在被淘汰。OpenRDMA 通过极简 8 字节门铃与硬件重构彻底把 GPU SM 从复杂的网络装包中解放出来；而 KOSMOS 则通过 GPU 内部常驻的持久化 Kernel，依据数据就绪状态自适应窃取计算/通信任务。这标志着高性能通信系统正在实现「将控制面交还硬件、将计算面留给模型」的本质回归。
