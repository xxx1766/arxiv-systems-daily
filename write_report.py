#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate today_report.md for arXiv Systems Daily Digest.
Date: 2026-11-15
"""

import os
import json

REPORT_PATH = "/Users/xqr/.gemini/antigravity/scratch/arxiv-systems-daily/today_report.md"

header = """## arXiv 系统方向日报 · 2026-11-15

### 今日概览

今日系统方向（cs.DC / cs.OS / cs.PF 及相关交叉领域）共抓取 68 篇候选论文。经过资深系统调研体系的严格筛选与多维度评分，本次**入选深读：12 篇**（其中 5 篇评分为 5 分的核心突破论文，5 篇评分为 4.5 分的高价值系统论文，2 篇评分为 4 分的特色系统论文），其余 56 篇理论或边缘交叉论文归入文末列表。

今日文献呈现出极具震撼力的「**无服务器大模型冷启动范式下沉、芯片片内细粒度空间切分与流水线、智能体全生命周期推理-沙箱环境协同编排、异构与消费级芯片 MoE 极限并发优化**」技术演进特征：
从 KAIST 与 SK 海力士基于 CXL 共享内存池与容器模板池化将 Serverless LLM 冷启动提速 5.2 倍，到英伟达官方在 Blackwell B200 上利用 CUDA Green Contexts 验证单 GPU 片内微批流水线打破内存带宽墙；从 AMD 官方研究院重塑 Instinct MI300X/MI355X 硬件分区正交切片消除 NUMA 性能崩塌，到蚂蚁集团 Ling 团队提出首个针对 Agent 训练与评测的「推理-沙箱环境协同调度器」缩短批处理 Makespan 高达 65%；从阿里巴巴针对消费级 Blackwell（SM120）在 PCIe 互连下以 Warp 级 FP8xFP4 算子完全掩盖 MoE 通信，到加州大学圣克鲁兹分校在 SGLang 仅加 80 行代码实现长文档多提问的单请求多流 KV Cache 单次读取复用；再到康奈尔大学首创 Tile 级跨 Stream 依赖流转打破 Megakernel 手工编写壁垒、清华大学与生数科技解耦运行时布局与 Muon 矩阵优化器更新、杜克大学在 cs.OS 顶刊发表端侧 MoE 相位感知统一分层内存管理系统 Tideway。系统栈各层正在从粗粒度的跨节点网络调度，全面纵深推进至微架构空间分区、纳秒级内存流水以及智能体异构环境闭环中。

今日必读：
1. **Cairn**: KAIST 与 SK 海力士通过 CXL 共享内存池与容器/进程模板池化解耦模型无关启动，大模型冷启动加速 4.1~5.2 倍。
2. **SubGPU Pipelining**: NVIDIA 提出 GPU 片内细粒度空间并行架构，基于 CUDA Green Contexts 实现算子图切段与微批流水，B200 解码吞吐提升达 2.2 倍。
3. **Starscream**: AMD 官方研究院重塑 Instinct MI300X/MI355X 硬件分区并行架构，引入片内正交切分消解 NUMA 瓶颈，Attention 算子提速最高 4 倍。
4. **Inference-Environment Coordination**: 蚂蚁集团 Ling 团队推出面向 Agent 的推理与沙箱环境协同调度器，CAAS 推进长链动作，批处理 Makespan 缩短最高 65%。
5. **GC-MoE on SM120**: 阿里巴巴针对消费级 Blackwell（RTX 50 系列）重构专家并行算子，在 PCIe 上无缝重叠 Token 分发与 Warp 级 FP8xFP4 MMA，解码提速 1.52 倍。
6. **Parallel Prompting**: UC Santa Cruz 针对长文档多问题场景提出单请求多流并行解码，每步仅读一次共享 KV Cache，在 SGLang 仅加 80 行代码提速最高 6.0 倍。
7. **MegaOps**: 康奈尔大学首创 Tile 级跨 CUDA Stream 依赖流转机制，在保持 PyTorch 原生模块化的同时达成手写 Megakernel 极限吞吐。
8. **SS-HSDP**: 清华大学与生数科技提出运行时与更新参数解耦的分片数据并行框架，原生高效支持 Muon 优化器与 MXFP8 训练，128 卡集群 MFU 提升 21.7%。
9. **Tideway**: 杜克大学在 cs.OS 顶刊发表端侧 MoE 分层内存管理系统，统一编排显存-内存-SSD 并实现 Prefill/Decode 相位自适应，端到端延迟降低 1.97 倍。
10. **Host-Tier KV on Static-Graph NPU**: 高丽大学针对静态图 NPU 智能体多模型级联工作流，实证量化 Host-Tier KV 恢复与重计算得失，过载下 SLO 达标率飙升至 99.8% 以上。
11. **Metal Sandbox**: 上海交大与阶跃星辰推出面向 Apple Silicon 的 GPU 编程智能体受限沙箱与跨 Mac 节点命令调度系统，降低工具等待 18.8%，代码已开源。
12. **PACER**: 威斯康星大学麦迪逊分校与 AMD 揭示短 Kernel 引发的片内 GPU 功率浪涌机理，通过主动式软硬件固件协同平滑突刺，性能净提升 3%~12%。

---

### 逐篇解读
"""

paper_1 = """#### 1. Fast Serverless LLM Cold Starts by Sharing and Prewarming Startup Work
- 中文译名：Cairn：通过共享与预热启动阶段工作实现无服务器大模型极速冷启动
- 链接：https://arxiv.org/abs/2611.16180
- 作者：Hongjin Kim, Igjae Kim, Kwanghoon Choi, Minho Ha, Jaehyuk Huh
- 单位：韩国科学技术院 (KAIST) & SK 海力士 (SK hynix) 【知名实验室/工业界】
- 分类：cs.DC
- 方向标签：A. 容器与运行时 (Serverless/FaaS 运行时、冷启动消除、预热容器池) & C. AI Infra (LLM Serving 启动优化、CXL 共享内存)
- 相关度：5/5

1. 核心贡献：
直击 Serverless 大模型服务化中按需动态拉起 Worker 实例时面临的长达约 1 分钟（60 秒）漫长冷启动痛点。研究团队经过严谨的底层剖析发现，在传统冷启动全流程中，从存储介质加载模型权重实际上仅占总体耗时的 5%~11%，绝大部分时间（接近 90%）被深度学习框架编译、GPU 显存 Profile 探测及运行时环境初始化所占据，而这些工作在集群各个物理节点间不仅高度重复，且相当一部分与具体的模型权重完全解耦。为此，KAIST 与半导体巨头 SK 海力士团队联合打造了 Cairn，通过将首次启动生成的权重和引擎产物发布至集群共享的 CXL 内存池供后续节点就地（In-Place）读取，并结合基于暖容器（Warm Containers）与模板进程（Template Process）的模型无关运行时预热机制，彻底粉碎了云原生无服务器推理的冷启动壁垒。

2. 原理解析：
这就像在 Kubernetes 容器集群中优化重型 GPU Pod 的冷启动生命周期：
- **CXL 内存池跨节点只读共享（类似只读分布式共享内存卷）**：集群中首个加载该模型的 Worker 节点充当「拓荒者」，在完成显存探测与计算引擎构建后，直接将模型权重和运行时不可变产物存放到整个集群可直接物理寻址的 CXL 共享内存池中。后续任何调度到其它服务器节点的容器 Pod 无需再从远程对象存储拉取数十 GB 权重镜像，也无需重新进行环境校验，直接通过 CXL 总线进行就地内存映射读取；
- **容器与模板进程两级池化（类似 CRI 预热沙箱与轻量 Fork 机制）**：系统在后台常驻一组已经预先拉起、完成基础 CUDA 上下文初始化及 Python 解释器库依赖加载的通用「暖容器（Warm Containers）」。当一个未加载过该模型的容器需要服务时，直接从模板进程迅速分叉，瞬间跳过最耗时的模型无关初始化；
- **即用即补的弹性占位控制器**：一旦某个暖容器被分派了具体的模型与流量，后台控制器立刻异步拉起全新的通用模板进程补充进池子，始终维持集群处于极低资源开销的无感知待命水位。

3. 关键结论：
在 ServerlessLLM 与 vLLM v0.20 框架之上，针对 1B 至 14B 参数的 6 种主流大模型在两台共享仿真 CXL 内存池的服务器上展开严苛实测：对于自身本地磁盘没有模型 Checkpoint 缓存的节点，Cairn 将端到端冷启动速度大幅提升了 4.1 至 5.2 倍；在真实的动态在线请求流评测中，首字时延（TTFT）中位数大幅削减了 64%。

4. 背景地位：
来自顶尖系统名校 KAIST 与存储半导体巨头 SK 海力士的最新强强联合成果，代表了以硬件级 CXL 内存互连池化技术解决云原生无服务器 LLM 冷启动前沿探索的最高水准，将无服务器基础设施从传统的粗粒度容器镜像分发推进到硬件级内存池共享阶段。

5. 落地相关性：
对于在 Kubernetes 上维护 Serverless 推理网关（如 Knative、Ray on K8s）或按需弹性缩容至零（Scale-to-Zero）的云原生工程团队具有极强的借鉴意义。即便数据中心暂未全面铺设 CXL 硬件，其将通用运行时初始化从冷启动关键路径剥离、利用进程级模板 Pod 与跨节点共享只读内存挂载的架构设计，完全可以直接复用在现有 GPU 集群编排调度器中。

---
"""

paper_2 = """#### 2. SubGPU Pipelining: Intra-GPU Fine-Grained Spatial Parallelism for LLM Inference
- 中文译名：SubGPU 流水线：面向大模型推理的 GPU 片内细粒度空间并行架构
- 链接：https://arxiv.org/abs/2611.14904
- 作者：Muralidhar Andoorveedu, Marius Juston, Tingkai Liu, Sanjay Patel
- 单位：英伟达 (NVIDIA) 【工业界】
- 分类：cs.DC
- 方向标签：C. AI Infra (LLM 推理服务、GPU 空间切分、CUDA Green Contexts) & D. 性能与可靠性 (DRAM 吞吐上限突破、微批处理延迟)
- 相关度：5/5

1. 核心贡献：
英伟达核心系统架构团队提出面向大模型解码阶段的单卡片内细粒度空间并行执行架构 SubGPU Pipelining。大语言模型 Decoding 阶段主要由短小且高度受限于内存带宽（Memory-Bound）的算子主导，对芯片级执行资源（SM）与全局显存带宽的利用呈现严重的突发与不均。该论文提出将单卡内的算子计算图切割为有序连续段，将其绑定到由互不重叠的流式多处理器（SM）池支撑的空间流水段上，通过在单芯片内部流水线式灌入微批次（Microbatch），首次打破了传统单 GPU 在时间维度全局串行执行的局限。

2. 原理解析：
这就像在单个物理 GPU 芯片内部搭建了一个微型的「Kubernetes Pod 资源拓扑管理器」与「微批空间流水线」：
- **SM 硬件空间硬切分（类似 CPU cgroup 与 K8s 节点拓扑隔离）**：利用 NVIDIA 现代硬件特性（如 Blackwell / Hopper 架构上的 CUDA Green Contexts），把一块物理 GPU 上的海量 SM 划分为若干完全独立的计算分区（SubGPU Stages），每个分区拥有专属且物理隔离的 SM 资源池，互不抢占；
- **计算图空间切段与微批流水**：不再让整个模型算子在整张卡上随时间从头串行跑到尾，而是把 36 层 Decoder 切分成连续的若干段，分别固化在不同的 SM 分区上。请求被拆解为微批次（Microbatches），像现代工厂流水线装配车间一样依次在不同 SM 分区之间流转传递；
- **多维耦合协同寻优**：通过构建共享资源解析模拟器，联合优化算子图切分点、段到 SM 的映射绑定、各流水段的 SM 配额以及微批次尺寸，彻底平滑了突发的显存访问峰值，消除了计算单元因等待内存搬运而产生的气泡。

3. 关键结论：
在 32 卡 Blackwell B200 部署环境与 GPT-OSS 120B 生产级模型评测中：通过解析模拟器在吞吐量帕累托前沿上探索，在相同每 GPU 吞吐下，SubGPU 流水线将每用户吞吐提升高达 2.2 倍；在相同每用户吞吐下，将每 GPU 吞吐提升 1.9 倍。在单块 B200 硬件上利用 CUDA Green Contexts 和 TensorRT-LLM 算子进行物理硅片实测，在全局 Batch 2048 场景下，平均 DRAM 读写吞吐率从峰值的 71.8% 跃升至 83.6%，36 层解码迭代时延直接下降 10.33%。

4. 背景地位：
来自英伟达硬件与底层软件系统核心团队的重量级成果，首次在下一代旗舰硬件 Blackwell B200 上利用 CUDA Green Contexts 验证了片内空间流水线的物理可行性，标志着大模型推理调度正从传统的跨卡流水线向单芯片微架构空间流水线全面演进。

5. 落地相关性：
对于从事 vLLM、TensorRT-LLM 深度定制或 GPU 虚拟化/多租户空间切分系统的系统工程师而言是必读之作。它证实了在单张巨型 GPU（如 B200/H100）上，简单的全局时间独占并非最优解，利用类似 cgroup 的硬件级 SM 切分结合算子空间流水，可以显著压榨出受限于内存带宽的隐藏吞吐。

---
"""

paper_3 = """#### 3. Starscream: Reimagining LLM Sharding on AMD Instinct GPUs with GPU Partitioning
- 中文译名：Starscream：基于硬件分区重塑 AMD Instinct GPU 上的大模型切分架构
- 链接：https://arxiv.org/abs/2611.15951
- 作者：Sumanth Gudaparthi, Smeet Chheda, Ganesh Dasika
- 单位：AMD 官方研究院 (AMD Research and Advanced Development) 【工业界】
- 分类：cs.DC, cs.AR, cs.LG
- 方向标签：C. AI Infra (大模型并行切分、AMD Instinct MI300X/MI355X、GPU 空间切分) & B. 编排与调度 (芯片粒度 NUMA 感知资源调度)
- 相关度：5/5

1. 核心贡献：
AMD 官方研究院针对其旗舰加速器（AMD Instinct MI300X / MI355X）独特的 Chiplet（小芯片）多 Die 架构与硬件分区能力，提出全新大模型切分框架 Starscream。研究团队指出，现代超大 GPU 具有极其显著的非均匀内存访问（NUMA）特性，若直接将传统面向均质 GPU 设计的单维度张量并行（TP）简单平铺到片内硬件分区上，将导致显存冗余增加、算术强度崩溃及平面集合通信开销激增三大致命瓶颈。Starscream 引入与传统卡间切分正交的片内切分维度，重塑了小芯片时代的大模型并行体系。

2. 原理解析：
这就像在具有多个 NUMA 节点的超大多路服务器上进行多级 Pod 编排与内存拓扑对齐：
- **Chiplet NUMA 域感知**：MI300X 由多个计算小芯片（XCD）和高带宽显存堆栈组成，硬件分区允许将单张物理 GPU 划分为具备独立 NUMA 域的多个逻辑设备；
- **正交片内切片架构**：不同于无脑把张量切得更细从而导致每个算子的矩阵太小、算术强度暴跌的传统做法，Starscream 确立了三大核心原则：算子形态保持（Preservation of Kernel Shape，维持高效 GEMM 尺寸）、消除显存冗余复制、极小化跨 Die 集合通信；
- **分层集合通信重构**：将平面的全卡 All-Reduce 拆解为片内高速互连与卡间互连两级，将通信延迟掩盖在片内高带宽域中。

3. 关键结论：
在 AMD Instinct MI300X 与下一代 MI355X 芯片上展开深度评测：与忽视小芯片拓扑的基线相比，Starscream 使得 Attention 算子获得最高达 4 倍的加速，融合 GEMM 获得 1.43 倍加速；全面消除了分区带来的吞吐衰减，展现出极强的跨架构泛化能力。

4. 背景地位：
来自 AMD 官方底层架构团队的一手系统成果，直击大模型算力硬件从小芯片制造走向系统软件栈协同的必经之路，是目前 AMD 生态下针对 MI300X/MI355X 体系最深度的系统切分研究。

5. 落地相关性：
对于正在考虑或已经部署 AMD ROCm 生态（MI300X 等）作为替代算力集群的云原生与 AI Infra 团队至关重要。在 K8s 上挂载并调度具备硬件分区的 AMD GPU 时，不能机械套用 NVIDIA 的 TP 参数配置，必须采纳 Starscream 的 NUMA 感知正交切分逻辑以释放全部硬件潜力。

---
"""

paper_4 = """#### 4. Reducing Batch Makespan for LLM Agent Workloads through Inference-Environment Coordination
- 中文译名：通过推理与环境协同调度缩短大模型智能体工作负载的批处理总耗时
- 链接：https://arxiv.org/abs/2611.16661
- 作者：Wei Feng, Meiling Chen, Boxiao Chen, Lu Liu, Bin Zi, 等（共 9 位作者）
- 单位：蚂蚁集团 (Ant Group, Ling Team) 【工业界】
- 分类：cs.DC, cs.AI
- 方向标签：C. AI Infra (LLM Agent 批量服务调度) & A. 容器与运行时 / B. 编排与调度 (推理-沙箱环境协同调度、批处理 Makespan 优化)
- 相关度：5/5

1. 核心贡献：
蚂蚁集团 Ling 团队针对智能体（Agent）工作流在训练评估、合成数据生成和强化学习 Rollout 阶段的批处理长尾瓶颈，提出业界首个「推理与环境协同调度」优化体系。智能体任务在生命周期中不断在「大模型推理」与「外部环境交互（执行 Docker 容器、Bash 脚本、API 工具等）」之间交替切换。传统方案将两者隔离调度，导致环境容量饱和时 GPU 显存空转或长尾任务阻塞全局批处理总耗时（Batch Makespan）。团队设计了轨迹感知路由、混合模型显存精细化切分以及推进长链的动作调度器（CAAS），使批处理 Makespan 大幅缩短最高达 65%。

2. 原理解析：
这就像在 Kubernetes 集群中同时编排「GPU 推理 Pod」与「执行沙箱 Job」的混合流水线：
- **推理与沙箱两级解耦准入控制**：在沙箱环境（容器池）并发容量受限时，传统 FIFO 调度会让执行链停滞卡住 GPU 上下文。系统将样本的准入控制与沙箱环境执行彻底解耦；
- **长链推进优先调度（CAAS，Chain-Advancing Action Scheduling）**：借鉴作业调度的最短剩余处理时间（SRPT）思想，依据实际观测到的任务执行进度，动态优先调度那些交互链条最长的智能体动作，集中火力消除最后的长尾木桶效应；
- **混合 LLM 资源动态配额**：针对同时具备自注意力机制与循环状态（Recurrent State）的混合架构模型，建立数学资源模型在 KV Cache 与循环状态之间动态平衡显存配额，并给出理论最佳并发度以避免显存颠簸与重计算；
- **轨迹感知路由（Trajectory-Aware Routing）**：基于智能体历史执行轨迹将请求导向已缓存相关上下文的推理节点，极大提升 Prefix Cache 命中率。

3. 关键结论：
在 BFCL（函数调用）、SWE-bench 多语言版（编程代码生成）、WideSearch（复杂检索）以及 MCP-Atlas（多工具智能体）四大真实严苛基准上，配合自研 Ling-3.0-Flash 与 Ling-3.1-Flash 进行全量真实评测：在任务评估得分毫无损失的前提下，批处理 Makespan 显著降低 10.4% 至 65.0%；该方案已被全面应用于蚂蚁灵波（Ling）大模型全生命周期生产训练与评估中。

4. 背景地位：
来自国内头部金融科技大厂蚂蚁集团核心基模团队的重量级系统工业实践，首次把智能体基础设施优化的焦点从单次推理的时延扩展到了「模型+沙箱容器协同」的宏观批处理吞吐维度。

5. 落地相关性：
对于在 Kubernetes 集群中部署 SWE-bench 评测平台、Coding Agent 沙箱服务或 RL 后训练流水线的 Infra 工程师来说，这是一份极具实操价值的工程范式：不要把 Agent 当作普通的 HTTP Web 请求来服务，必须将模型网关与沙箱调度器（如 K8s Operator）实现端到端的控制面闭环。

---
"""

paper_5 = """#### 5. GC-MoE on SM120: Overlapping Expert-Parallel Token Dispatch with Warp-Level FP8xFP4 Block-Scaled MMA on Consumer Blackwell
- 中文译名：面向消费级 Blackwell SM120 的 GC-MoE：专家并行 Token 分发与 Warp 级 FP8xFP4 块缩放 MMA 的完全重叠
- 链接：https://arxiv.org/abs/2611.16219
- 作者：Yong Li, Haoyu Wang, Kan Liu, Tao Lan
- 单位：阿里巴巴 (Alibaba Inc.) 【工业界】
- 分类：cs.DC, cs.LG
- 方向标签：C. AI Infra (MoE 专家并行 / All-to-All 掩盖 / Warp 级 FP8xFP4 混合精度计算 / 消费级 Blackwell SM120 优化) & D. 性能与可靠性 (PCIe 拓扑低延迟解码)
- 相关度：5/5

1. 核心贡献：
阿里巴巴底层系统团队针对消费级 Blackwell 架构（SM120，如 RTX 50 系列）缺乏数据中心高昂 NVLink 互连、张量内存及集群组播等硬件特性的现实物理约束，彻底重构了其著名的 GC-MoE 专家并行算子。在仅能依赖常规 PCIe 互连与 Warp 级块缩放张量核心（mma.sync）的苛刻条件下，实现了专家并行 Token 分发通信与 FP8 激活乘 FP4 权重矩阵乘法（MMA）的完全无缝重叠与零开销掩盖。

2. 原理解析：
这就像在没有高带宽专用背板的低成本服务器集群中，通过软件流水线彻底掩盖慢速网络传输：
- **Swap-AB Warp 级低精度 MMA 布局**：SM120 架构下仅支持基础的 Warp 级块缩放指令。团队创新性采用 Swap-AB 操作数置换，把 FP4 权重加载在寄存器 A 操作数、FP8 激活值放置在 B，并利用立即数寻址快速完成缩放因子字节索引；
- **分批批量拉取引擎与 64 位去重缓存**：设计了专家粒度的流式分发机制，通过常驻的批量拉取引擎配合 64 位去重 Cache，避免跨 PCIe 传输重复的专家权重与 Token；
- **位置主序暂存区与常驻中继拷贝器（Relay Copiers）**：在解码产生全精度 BF16 返回值时，利用预先开辟的 Position-Major Arena，由常驻中继线程无阻塞地异步排空通信数据，并将共享专家无缝折叠入计算角色，实现极致紧凑的算子流水。

3. 关键结论：
在 8 张由 PCIe 互连的 RTX PRO 5000（SM120）消费级 Blackwell 显卡构建的服务器集群上实测：在跨越 18 个主流解码配置点测试中全部取得绝对胜出（18/18 全胜），比 FlashInfer CuTe DSL W4A8 MegaMoE 提速 1.522 倍，比 Cake MegaMoE 提速 1.387 倍；94 项数值一致性测试与 752 项跨卡一致性检查全数通过，跨算子输出余弦相似度高达 0.9999997 以上。

4. 背景地位：
来自阿里巴巴顶级系统与算子团队的突破性底层工作，填补了下一代消费级/工作站级别 Blackwell 芯片在超低精度 MoE 专家并行算子上的生态空白，证明了低成本商用 GPU 集群在精细算子调度下同样能爆发出匹敌专用数据中心的吞吐性能。

5. 落地相关性：
对于希望利用高性价比消费级显卡（如 RTX 5090 / RTX PRO 5000）搭建本地私有化或边缘 MoE 推理节点的团队具有直接指导意义。不仅证明了 FP8xFP4 量化部署的可行性，其在 PCIe 瓶颈下掩盖集合通信的系统流水技巧亦可广泛迁移至各类算子开发中。

---
"""

paper_6 = """#### 6. Read Once, Answer Many: Parallel Prompting for Shared-Context LLM Inference
- 中文译名：单次读取、多次应答：面向共享上下文大模型推理的并行提示架构
- 链接：https://arxiv.org/abs/2611.15130
- 作者：Zekun Zhao, Jeffrey Flanigan
- 单位：加州大学圣克鲁兹分校 (University of California, Santa Cruz) 【知名实验室】
- 分类：cs.CL, cs.AI, cs.DC
- 方向标签：C. AI Infra (LLM 推理服务、Prefix Cache / KV Cache 带宽复用、SGLang 运行时) & D. 性能与可靠性 (内存带宽瓶颈消除)
- 相关度：4.5/5

1. 核心贡献：
加州大学圣克鲁兹分校团队直击长文本多问答场景下的显存带宽墙。在法律合同审核、长文档多维度抽取或 LLM-as-a-Judge 评测等场景中，用户常针对同一篇长文档发起数十至数百个独立提问。现有服务引擎（如 vLLM、SGLang）的前缀缓存（Prefix Caching）虽然去除了重复的 Prefill 计算，但在后续的每一步解码（Decode）中，仍然必须为每个并发请求单独从显存中全量读取一次长文档的 KV Cache，导致显存带宽被彻底耗尽。论文提出了 Parallel Prompting（并行提示架构），将 P 个问题打包为单次请求中的 P 条独立流同时解码，在每一步解码中对共享文档的 KV Cache 仅执行一次读取，彻底消除了显存带宽冗余。

2. 原理解析：
这就像在网络广播中用一条多路复用信道代替数百条单播连接：
- **单请求多流解码（Multi-Stream Multiplexing）**：调度器将面向同一文档的 P 个并发请求在引擎内部聚合成单条特殊复合请求，让它们共享同一份前缀上下文物理缓存；
- **注意力核内流掩码（Stream-ID Attention Mask）**：无需在显存中生成庞大稀疏的稠密 Mask 张量，而是在 FlashInfer/FlashAttention 核函数内部通过极为轻量的逻辑判断（每个 Token 的 Stream-ID 与 Query 的 Stream-ID 匹配关系），确保各问题的回答仅能看到共享文档和自身的问题上下文，流与流之间互不干扰；
- **固定形状与 CUDA Graph 捕获**：每一步解码由于 P 个流同步推进，其张量形状在迭代间完全保持静态，能够 100% 被 CUDA Graph 无缝捕获，抹平内核发射延迟。

3. 关键结论：
团队在 SGLang 最新主分支上仅修改 3 个文件、添加约 80 行代码即完成了优雅落地。在 CodeLlama-7B、8K~16K 文档长度以及 64~256 并发提问规模下：在 NVIDIA A100 上相比原版 SGLang（FlashInfer 后端）吞吐提升 3.7 倍，在 RTX A6000 上提速达到 5.9 至 6.0 倍；在跨越 2 种硬件、2 个 SGLang 版本与不同数据载荷的全部 144 组测试中保持 100% 连胜。

4. 背景地位：
来自 UC Santa Cruz 自然语言与系统实验室的极简且极度实用的工程突破，精准抓住了前缀缓存落地后解码端被大家忽视的「KV 缓存显存读取带宽冗余」痛点，代码已在 GitHub 开源。

5. 落地相关性：
对于在云原生集群中部署企业级 RAG、金融/法律文档智能问答或大规模 LLM 数据标注平台的工程师来说，收益巨大且门槛极低。80 行的轻量侵入性意味着可以极快地 Cherry-pick 进企业内部维护的 SGLang 或 vLLM 分支中，立竿见影将服务器显卡吞吐提升数倍。

---
"""

paper_7 = """#### 7. MegaOps: A Kernel Overlapping Framework with PyTorch-like Modularity and Megakernel Performance
- 中文译名：MegaOps：兼具 PyTorch 模块化与 Megakernel 极致性能的算子重叠执行框架
- 链接：https://arxiv.org/abs/2611.16248
- 作者：Jinkun Lin, Byungsoo Oh, Rachee Singh
- 单位：康奈尔大学 (Cornell University) 【知名实验室】
- 分类：cs.DC
- 方向标签：C. AI Infra (算子与编译系统、CUDA Stream 重叠、Megakernel 运行时调度) & D. 性能与可靠性 (消除 Kernel Launch 屏障开销)
- 相关度：4.5/5

1. 核心贡献：
康奈尔大学系统网络团队直面现代深度学习框架中「模块化与极限执行效率不可兼得」的核心矛盾。主流框架采用「单算子单内核（Kernel-per-Operator）」模式，算子解耦便于维护，但内核间粗粒度依赖屏障导致 SM 频繁空转、计算通信串行化且无法跨内核预取权重；而近期兴起的「巨型内核（Megakernel，如 ThunderKittens）」虽然把全层融合成单内核消除了屏障，却彻底丧失了模块化与通用性。团队研发了 MegaOps 框架，首次证明无需算子硬编码融合，仅通过在独立 CUDA Stream 上基于细粒度数据块（Tile）驱动算子重叠，就能以 PyTorch 原生模块化实现媲美 Megakernel 的极限性能。

2. 原理解析：
这就像在微服务编排中用细粒度流式消息总线取代粗粒度的阻塞式 RPC 栅栏：
- **数据分块（Tile）级跨流依赖**：MegaOps 将前后有依赖关系的算子分别发射到不同的 CUDA Stream 上。两内核之间不再等待前一个完整执行完毕，而是通过轻量级的硬件原子标志位在中间张量的分块（Tile）级别进行同步——生产者只要算完一个 Tile，消费者立即开跑；
- **零修改复用既有算子**：只要两个内核遵循相同的数据分块布局（如 $128 \times 128$），就可以自由插拔组合，完全复用现有经过工业级调优的 Triton、cuBLAS、cuDNN 算子，无需重写任何底层 CUDA 汇编；
- **权重异步流水预取**：后一个算子可以在前一个算子正在计算上一层 Tile 时，并行从 HBM 中预取自己的模型权重，消除了冷等待。

3. 关键结论：
在单卡 H100、A100、L40 以及 4 卡 A100、8 卡 H100 服务器上，对 Llama3 和 Qwen3 密集大模型进行全方位基准测试：MegaOps 完美打平了经过极其复杂手工调优的 ThunderKittens 巨型内核吞吐；相比最强基线，解码吞吐达到 1.09~1.10 倍，Prefill 吞吐达到 0.98~1.10 倍，且完全保留了标准 PyTorch 代码的模块化风格。

4. 背景地位：
来自系统名校康奈尔大学的优雅创新，突破了过去一年系统界认为必须走向手工编写 Megakernel 才能榨干 GPU 性能的思维定势，为大模型编译与运行时系统架构指明了一条务实高效的新道路。

5. 落地相关性：
对于从事 AI 编译器（如 TorchDynamo、Triton、TVM）或定制推理引擎底座的开发者具有极大启发。不需要耗费数月重写无法维护的万行单体 GPU Kernel，通过在其运行时调度器中引入 Tile 级 Stream 事件流转，就能在不破坏算法工程师模型结构代码的前提下压榨出极致吞吐。

---
"""

paper_8 = """#### 8. SS-HSDP: Efficient and Flexible Sharded Data Parallelism via Runtime-Update Decoupling
- 中文译名：SS-HSDP：基于运行时与更新解耦的高效灵活分层分片数据并行框架
- 链接：https://arxiv.org/abs/2611.16467
- 作者：Chendong Xiang, Pengle Zhang, Jinliang Li, Zichen Liang, Jintao Zhang, 等（共 8 位作者）
- 单位：清华大学 (Tsinghua University) & 生数科技 (Shengshu Technology) 【知名实验室/工业界】
- 分类：cs.DC
- 方向标签：C. AI Infra (分布式训练系统、分片数据并行 HSDP/FSDP、Muon 优化器支持、MXFP8 训练) & B. 编排与调度 (超大规模集群训练拓扑)
- 相关度：4.5/5

1. 核心贡献：
清华大学朱军、陈键飞团队联合国内知名多模态生成模型独角兽生数科技（Vidu 视频大模型研发方），针对超大规模集群分布式训练中的混合分片数据并行（HSDP）提出突破性框架 SS-HSDP。现有分片数据并行（如 PyTorch FSDP2、Megatron-FSDP）将前反向计算的运行时参数布局与优化器更新的数据结构强绑定，限制了低精度计算核的排布自由，并导致新型矩阵优化器（如近期备受瞩目的 Muon）无法高效原生支持。SS-HSDP 首创「运行时参数与更新参数解耦」机制，在不引入冗余数据搬运的前提下，实现了异构数据排布与完全零拷贝执行。

2. 原理解析：
这就像在云原生状态机中将只读副本的快速计算投影与持久化存储的有状态更新彻底解耦：
- **运行时与更新双状态解耦**：计算前向与反向传播时，显存中维持最有利于硬件 Tensor Core 计算吞吐的紧凑 Packed 布局（如 MXFP8 微缩放格式）；而优化器更新时，则按优化器算法所需的数据单元（如 Muon 所需的矩阵单元或 AdamW 所需的分片向量）进行视图映射；
- **共享数据视图与多级层次化分片**：通过高级内存视图复用底层物理显存页面，无需在计算和更新阶段之间发生二次显存内存拷贝；结合机内 NVLink 与机间网络的层次化 HSDP 拓扑，实现跨网络域的按需通信；
- **原生支持新型矩阵优化器**：天然兼容 Muon 这类对权重矩阵具有严格二维几何约束的优化器，无需像过去一样降级为低效的全局显存重组。

3. 关键结论：
在跨越语言大模型与视频生成大模型（Shengshu 真实生产负载）的严苛分布式训练测试中（最高测试至 128 卡 GPU 集群，结合 MXFP8 训练）：SS-HSDP 的模型算力利用率（MFU）全线超越 PyTorch FSDP2、字节跳动 veScale-FSDP 以及 Megatron-FSDP；在 128 卡规模下，MFU 相比最强基线提升高达 21.7%，且显存峰值完全持平或更低。

4. 背景地位：
由清华大学计算机系顶尖学者与国产视频大模型第一梯队企业生数科技联合攻关的工业实战成果，代表了当前面向跨节点大集群混合并行训练系统在数据排布与优化器解耦层面的最前沿探索。

5. 落地相关性：
对于在 Kubernetes 集群上维护万卡级别视频/多模态/LLM 训练任务（利用 MPIJob 或 PyTorchJob）的平台工程师至关重要。尤其是训练团队引入 Muon 矩阵优化器或低精度 FP8 训练时，采用 SS-HSDP 的解耦架构能直接在现有物理网络拓扑上榨取超过 20% 的有效算力，大幅削减大模型训练周期与电费成本。

---
"""

paper_9 = """#### 9. Tideway: Phase-Aware Tiered Memory Management for MoE Inference on Consumer Devices
- 中文译名：Tideway：面向消费级设备 MoE 推理的相位感知分层内存管理系统
- 链接：https://arxiv.org/abs/2611.14848
- 作者：Yifei Wang, Tsun-yu Yang, Yechen Xu, Hancheng Ye, Qinsi Wang, 等（共 10 位作者）
- 单位：杜克大学 (Duke University) 【知名实验室】
- 分类：cs.OS
- 方向标签：cs.OS / C. AI Infra (操作系统分层内存换页、MoE 专家调度、CUDA Graph 动态重写) & D. 性能与可靠性 (显存-内存-SSD 换页抖动抑制)
- 相关度：4.5/5

1. 核心贡献：
杜克大学电子与计算机工程系权威学者陈怡然（Yiran Chen）、李海（Hai Li）与卓丹样（Danyang Zhuo）团队在顶级操作系统分类（cs.OS）发表系统大作 Tideway。针对消费级 PC 部署大规模混合专家（MoE）模型时显存与内存双重受限、巨量专家权重被迫溢出（Spill）至 SSD 的现实困境，指出传统系统将各存储层视作独立缓存导致的严重换页颠簸（Thrashing）。Tideway 提出将主机内存与显存统一编排为单虚拟内存池，并开创了「相位感知（Phase-Aware）分层存储管理」，在流式 Prefill 与稀疏 Decode 两阶段自适应重组内存布局，结合针对专家换页的 CUDA Graph 深度优化，彻底释放端侧大模型潜力。

2. 原理解析：
这就像在 Linux 操作系统内核中重构了一套专门针对 MoE 激活特性的智能虚拟内存交换子系统（Swap Subsystem）：
- **统一分层内存池与全双工去重**：显存与主机 RAM 不再是各自为政的二级 Cache，而是统一由系统集中调度。系统在 VRAM 与 RAM 之间实现专家级去重，并压榨 PCIe 双向带宽——在驱逐 GPU 专家的同时，选择性将其送回 Host RAM，避免后续再度触发昂贵的 SSD 磁盘 I/O；
- **计算相位感知内存布局自适应**：精准利用大模型不同推理阶段的算法特征：Prefill 阶段长提示词会激活动态层中的几乎所有专家，系统采用连续流式布局以追求最大预取带宽；进入 Decode 阶段每个 Token 仅稀疏激活几个专家，系统即刻在相位交界处切换为按需离散专家热点缓存布局，杜绝跨层颠簸；
- **专家换页下的 CUDA Graph 动态重写**：传统 CUDA Graph 假定显存物理指针恒定不变，一旦发生专家换入换出 Graph 就会崩溃。Tideway 设计了轻量级的指针间接层，使 GPU 在频繁专家换页时依然能全程保持 CUDA Graph 录制与高速重放。

3. 关键结论：
在消费级硬件与顶尖前沿 MoE 模型上的实测表明：Tideway 相比业界最快基线系统实现了平均 1.97 倍的端到端时延降低、2.40 倍的首字时延（TTFT）加速以及 1.61 倍的单 Token 生成时延（TPOT）优化；系统源代码已完全开源。

4. 背景地位：
来自体系结构与系统顶尖名校杜克大学的重磅突破，陈怡然与李海教授团队将传统经典 OS 内存分层管理与换页置换算法理论，与大模型最新 MoE 架构深度结合，是端侧和边缘 AI 系统领域的标杆之作。

5. 落地相关性：
对于边缘计算、本地端侧智能体以及边缘 Kubernetes 节点（如 K3s）上低成本部署 MoE 模型的工程团队意义重大。通过系统层自适应布局与 CUDA Graph 维持机制，使得原本只能跑在云端数据中心的多百亿参数 MoE 模型得以稳定、高效地运行在几十 GB 内存的普通工作站上。

---
"""

paper_10 = """#### 10. Recompute or Restore? Host-Tier KV for Multi-Model Agent Workflows on a Static-Graph NPU Serving Stack
- 中文译名：重计算还是恢复？静态计算图 NPU 服务栈上面向多模型智能体工作流的 Host 层 KV 缓存
- 链接：https://arxiv.org/abs/2611.15126
- 作者：Sungwon Woo, Seyeon Kim
- 单位：高丽大学 (Korea University) & Rebellions NPU 【知名实验室】
- 分类：cs.DC, cs.LG, cs.PF
- 方向标签：C. AI Infra (智能体多模型级联、KV Cache 分层卸载 vs 重计算、静态图 NPU 运行时优化) & B. 编排与调度 (SLO 达标率与事件驱动调度)
- 相关度：4.5/5

1. 核心贡献：
高丽大学团队针对以神经网络处理器（NPU，如商业级 Rebellions ATOM+）为代表的静态计算图加速芯片，在支撑多模型智能体（Agent）工作流时遭遇的 KV Cache 内存瓶颈展开系统性实证与建模。智能体通常采用大小模型级联（如 Qwen3-8B 规划器 + Qwen3-0.6B 执行器），共享超长上下文前缀。而在 Ahead-of-Time（AOT）静态图编译约束下，芯片板载 KV 预算固定，溢出的前缀通常必须重新计算。团队系统性对比了「从 Host 内存同步恢复（Restore）」与「重新计算（Recompute）」的得失，构建了事件调度预测模型，实现在严苛负载下业务 SLO 达标率从 9.4% 跃升至 99.8% 的巨大突破。

2. 原理解析：
这就像在基于微服务架构的 Kubernetes 集群中评估远程 Redis 缓存读取与本地无状态计算的开销平衡点：
- **静态计算图下的内存死穴**：专用 NPU（如 Rebellions、Google TPU、AWS Inferentia）必须在编译期静态分配计算图形状与 KV 缓冲区，无法像 GPU 那样灵活动态扩展显存池。当智能体并发冲高时，默认配置会发生灾难性服务崩溃，89.5% 的规划器 Token 都在反复做重复的 Prefill 重计算；
- **同步 Host-DRAM 分层搬运**：利用运行时公共接口开辟 Host-DRAM 分层存储，将驱逐的 KV Cache 暂存至主机内存。但由于跨 PCIe 数据传输与模型前向推理共用同一引擎线程，盲目恢复反而可能阻塞计算引擎；
- **调度器感知事件模型（Scheduler-Aware Event Model）**：团队建立离线事件仿真模型，结合任务拓扑（链式 Chain 还是分叉 Fork）、前缀长度、并发队列深度及 PCIe 传输时延，在执行前精准裁决当前请求应当走「Host 恢复」还是「本地重算」。

3. 关键结论：
在基于两张卡部署 8B 规划器、单卡部署 0.6B 执行器的商用 NPU 软硬件栈（vllm-rbln 0.10.2）上实测：Host-Tier KV 分层机制在两种高压超载场景下，将智能体工作流的端到端服务等级目标（SLO）达标率分别从 22.8% 提升至 100%、从 9.4% 提升至 99.8%；在常规负载下带来 11.8%（链式）至 18.2%（分叉）的纯吞吐容量增益；离线预测模型在 24 种负载场景下的 P50 与 P99 时延预测误差严控在 15% 容差以内。

4. 背景地位：
聚焦于新兴专用 ASIC/NPU 生态在大模型智能体长文本前缀复用上的真实瓶颈，首次以严谨量化实验给出了静态图 NPU 在 Host KV 卸载与重计算之间的临界判定边界。

5. 落地相关性：
对于正在尝试非 NVIDIA 芯片方案（如各厂商 NPU、TPU、ASIC）以降低推理算力成本的云原生平台架构师极具参考价值。清晰地指出了专用硬件由于静态图限制所面临的特殊陷阱，并给出了利用 Host 内存与调度模型护航多模型 Agent 生产稳定性的落地方案。

---
"""

paper_11 = """#### 11. Metal Sandbox: Isolated Execution and Command Scheduling for GPU Coding Agents on Apple Silicon
- 中文译名：Metal Sandbox：Apple Silicon 上面向 GPU 编程智能体的隔离执行与命令调度架构
- 链接：https://arxiv.org/abs/2611.17294
- 作者：Haozhe Wang, Lina Chen, Fanqi Wan, Qi Han, Yinmin Zhang, 等（共 8 位作者）
- 单位：上海交通大学 (SJTU)、北京中关村学院 & 阶跃星辰 (StepFun) 【知名实验室/工业界】
- 分类：cs.LG, cs.AI, cs.DC
- 方向标签：A. 容器与运行时 (沙箱/隔离运行环境、文件系统受限访问) & B. 编排与调度 (集群命令级细粒度调度、任务跨节点迁移)
- 相关度：4/5

1. 核心贡献：
上海交大严骏驰教授团队与国内知名大模型企业阶跃星辰（StepFun）联合推出专为 Apple Silicon GPU 编程智能体设计的隔离沙箱与跨节点命令调度基础设施 Metal Sandbox。在自主编写与评测 GPU 底层 Metal 算子时，智能体频繁在「大模型推理」、「本地代码编译测试」与「GPU 执行」之间轮转，导致本地 Mac 芯片的 GPU 资源在整个交互周期中出现大段严重空置。Metal Sandbox 通过实例级文件访问隔离、原生 macOS 命令执行受限沙箱以及跨互联 Mac 集群的命令级细粒度调度，实现了任务跨物理节点的无感迁移与并发利用。

2. 原理解析：
这就像在 Mac 设备集群上构建了一个具备受限文件沙箱（类似轻量级 chroot/Container）与微任务调度器（类似 Nomad/K8s Task Runner）的 Agent 基础设施：
- **实例级工作区受限隔离**：为每个并发智能体分配受限的文件访问路径与私有开发环境，既保证能调用 macOS 原生 Metal 编译工具链，又防止 Agent 危险越权修改宿主机环境；
- **命令级细粒度调度与插槽共享**：分析 Agent 发出的 Shell 命令，将并行只读命令无阻塞并发执行，串行 GPU 编译/执行命令在单节点内共享一个执行插槽；
- **跨机器任务流转迁移**：当本地节点 GPU 正在排队而集群中其它 Mac 处于空闲时，调度器将合规的等待命令直接跨网络热迁移到可用 Mac 上执行，并将 stdout/stderr 结果透明回传给原智能体工作流；
- **开箱即用的 Harbor 验证集成**：与 Harbor 智能体自动化评估套件深度集成，实现任务执行、自动验证与 Rollout 采集一体化。

3. 关键结论：
在 4 台 Mac mini M4 节点构建的小型物理集群上实测：在密集命令请求下，命令吞吐量提升 1.68 至 2.05 倍；在单节点运行 4 个并发 Session 对比单 Session，持续吞吐量预计提升 2.14 倍；在动态调度下回放真实 Agent 运行轨迹，智能体工具平均等待时间降低 18.8%，整批任务运行耗时缩短 22.3%；项目与 Harbor 集成代码均已在 GitHub 开源。

4. 背景地位：
大模型智能体自主开发并优化 GPU 算子（如 Metal/CUDA）是当下自治系统最火热的方向。该研究针对 Mac 统一内存架构下端侧研发集群的痛点，给出了业界首个专为 Coding Agent 定制的物理沙箱与分布式调度解决方案。

5. 落地相关性：
对于在企业内搭建「AI 程序员（Coding Agent）」基础设施、利用 Apple Silicon 集群进行边缘模型开发与测试的研发团队而言，提供了开箱即用的隔离运行与算力压榨模板，大幅提升硬件投资回报率。

---
"""

paper_12 = """#### 12. PACER: GPU Excursion Management for ML Workloads
- 中文译名：PACER：面向机器学习工作负载的 GPU 功率浪涌瞬态治理架构
- 链接：https://arxiv.org/abs/2611.17206
- 作者：Rutwik Jain, Nathaniel Morris, Yiwei Jiang, Shidhartha Das, Gary Kao, 等（共 9 位作者）
- 单位：威斯康星大学麦迪逊分校 (UW-Madison) & AMD 【知名实验室/工业界】
- 分类：cs.DC
- 方向标签：B. 编排与调度 / D. 性能与可靠性 (GPU 集群功率浪涌管控、供电基础设施稳定、硬件级降频抑制)
- 相关度：4/5

1. 核心贡献：
威斯康星大学麦迪逊分校系统研究组联合 AMD 官方硬件团队，首次系统性揭示并治理了现代机器学习（特别是大语言模型）负载中极其频繁严重的「单 GPU 片内功率浪涌（Power Excursions / 电气设计峰值功率 EDP_p）」。传统系统认知通常关注多 GPU 间的宏观功率差异，而该研究发现大模型推理中大量运行耗时极短（微秒级）的算子与剧烈算力波动，导致瞬时功率在极短窗口内反复突破 GPU 额定功率阈值。频繁的硬件级被动降频（Throttling）导致性能严重抖动，甚至危及供电网络稳定。团队设计了软硬件协同的 PACER 机制，实现对功率浪涌的主动平滑管控。

2. 原理解析：
这就像在数据中心配电与 K8s 集群算力调度中引入了一个防雷击和突刺的「电网避雷针与动态稳压器」：
- **微秒级片内瞬态失配机理**：大模型解码中的轻量 Kernel 启动极快且计算强度瞬间跃升，而 GPU 现有的动态电源管理（DVFS）机制反应粒度较粗（通常为毫秒级），这种时间尺度上的不对称导致芯片在短时间内产生剧烈的高幅功率超调（Overshoot）；
- **恶性降频雪崩**：一旦瞬时峰值触碰芯片物理保护红线，底层硬件固件会触发保守的紧急降频，导致后续算子执行变慢、时延拉长，破坏系统整体 SLO；
- **主动式软硬件固件协同（PACER）**：通过在硬件与固件层面构建超低开销的预测与瞬态控制回路，在微内核发射前预先识别潜在的功率激增模式，通过平滑电压/频率过渡曲线主动抹平功率突刺，在保护硬件电路的同时避免进入深谷降频状态。

3. 关键结论：
在涵盖各类主流机器学习工作负载的广泛评测中：PACER 相比目前工业界最先进的 GPU 电源管理机制，带来了 3% 至 12% 的应用级端到端性能净提升，且表现已经逼近理论最优的预知未来神谕（Oracle）方案（差距仅在 3% 以内）。

4. 背景地位：
来自顶尖体系结构强校 UW-Madison（Shivaram Venkataraman 与 Matthew Sinclair 等系统大牛）与 AMD 联合攻关的前沿成果，首次量化并攻克了大模型负载下被长期忽视的微秒级芯片瞬态电力稳定性难题。

5. 落地相关性：
对于超大规模 AI 数据中心运营方、高密度液冷 GPU 机房运维团队以及集群级能耗与稳定性调优工程师具有极高警示与指导价值。阐明了仅靠传统的机柜级供电封顶（Power Capping）不足以应对大模型瞬态突刺，必须在加速器调度与底层固件交互层面进行跨层协同治理。

---
"""

with open(REPORT_PATH, "w", encoding="utf-8") as f:
    f.write(header)
    f.write(paper_1)
    f.write(paper_2)
    f.write(paper_3)
    f.write(paper_4)
    f.write(paper_5)
    f.write(paper_6)
    f.write(paper_7)
    f.write(paper_8)
    f.write(paper_9)
    f.write(paper_10)
    f.write(paper_11)
    f.write(paper_12)

print("Wrote top 12 papers to report.")
