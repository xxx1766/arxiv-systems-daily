# arXiv Systems Daily Digest 🚀

每日自动追踪并深度解读系统方向与 AI Infra 领域的最新 arXiv 论文。

读者定位为从事「容器架构与运行时、Kubernetes 编排、AI 基础设施（分布式训练/推理/GPU集群）」的工程师与研究者。

## 📌 最新日报
- **[2026-11-11 日报](docs/2026-11-11.md)**（入选 12 篇）：
  - **Lazy-Pulling Impossibility**: 揭示 Kubernetes 与 stargz/SOCI/Nydus 镜像按需拉取在模型服务化中的两大不可行性，提出不改 CRI 的零误差硬约束缓存治理方案。
  - **Firepool**: LinkedIn 生产级 H200 集群热 GPU 容量代理框架，通过同质底模与零显存 Standby 占位 Pod 将 Agent/RL 启动延迟从 59s 骤降至 3.5s。
  - **MoE Dispatch Offloading**: NVIDIA 官方团队在 GB300 NVL72 上的 NCCL-EP 突破，通过 GPU-Friendly Descriptors 与 CPU 线程卸载消除双批流水线裸露通信，提升 vLLM 吞吐达 42%。
  - **MTRDMA**: 湖南大学提出轻量级多租户 RDMA 控制面隔离方案，利用原子共享内存与 rdma-cgroup 消除吵闹邻居对网卡微架构缓存的耗尽，保护容器吞吐。
  - **Evolving Infra**: UC Berkeley 与 MIT 等联合推出 Agent 自适应大模型服务化框架，在 256 卡 GB300 集群上实现算力分配与 KV Cache 解耦自适应，P95 首字延迟降低 14 倍。
  - **NCCL-BOT**: NVIDIA 集合通信团队重构 NCCL 静态开销模型，以在线多臂老虎机（MAB）动态闭环实测延迟，攻克拓扑与拥塞下的次优通信算法选择难题。
  - **The Storage View Of KV Cache**: UT Austin 与 IBM 联合对 11 类生产负载的底层 KV Cache 展开存储行为刻画，提出跨单/多会话的精简 3 信号存储管理抽象。
  - **Relief**: 香港大学与香港科大研发的专家并行 MoE 逐步实时负载均衡引擎，打破传统线性规划求解瓶颈，以 CUDA 算子及片上硬件块恢复 37.3% 的算力利用率。
  - **OOM-MoE**: 香港科技大学（广州）针对全参数 MoE 训练的内存-执行协同卸载框架，通过参数预取流水线与显存复用极大降低跨互连传输等待。
  - **Custom GPSIMD on Trainium**: UCLA 丛京生团队针对 AWS Trainium 3 构建首个 C++ 自定义 GPSIMD 算子编译工具链，加速 DeepSeek-V4.1 Engram 稀疏检索。
  - **AdaOffload**: UC Berkeley Sky Computing 团队打造的异构多 GPU 混合专家卸载推理系统，全链路 NUMA 感知调度使超大 MoE 吞吐提升最高 15.5 倍。
  - **Wasm Edge Cold-Start**: 根特大学-imec 研发的 WebAssembly 边缘调度器，联合优化产物缓存局部性与网络路由距离，降低边缘端到端冷启动延迟 40.8%。

## 📅 历史归档
| 日期 | 入选篇数 | 重点内容提要 | 报告链接 |
| :--- | :---: | :--- | :--- |
| **2026-11-11** | 12 篇 | • <b>Lazy-Pulling Impossibility</b>: 揭示 Kubernetes 与 stargz/SOCI/Nydus 镜像按需拉取在模型服务化中的两大不可行性，提出不改 CRI 的零误差硬约束缓存治理方案。<br>• <b>Firepool</b>: LinkedIn 生产级 H200 集群热 GPU 容量代理框架，通过同质底模与零显存 Standby 占位 Pod 将 Agent/RL 启动延迟从 59s 骤降至 3.5s。<br>• <b>MoE Dispatch Offloading</b>: NVIDIA 官方团队在 GB300 NVL72 上的 NCCL-EP 突破，通过 GPU-Friendly Descriptors 与 CPU 线程卸载消除双批流水线裸露通信，提升 vLLM 吞吐达 42%。<br>• <b>MTRDMA</b>: 湖南大学提出轻量级多租户 RDMA 控制面隔离方案，利用原子共享内存与 rdma-cgroup 消除吵闹邻居对网卡微架构缓存的耗尽，保护容器吞吐。<br>• <b>Evolving Infra</b>: UC Berkeley 与 MIT 等联合推出 Agent 自适应大模型服务化框架，在 256 卡 GB300 集群上实现算力分配与 KV Cache 解耦自适应，P95 首字延迟降低 14 倍。<br>• <b>NCCL-BOT</b>: NVIDIA 集合通信团队重构 NCCL 静态开销模型，以在线多臂老虎机（MAB）动态闭环实测延迟，攻克拓扑与拥塞下的次优通信算法选择难题。<br>• <b>The Storage View Of KV Cache</b>: UT Austin 与 IBM 联合对 11 类生产负载的底层 KV Cache 展开存储行为刻画，提出跨单/多会话的精简 3 信号存储管理抽象。<br>• <b>Relief</b>: 香港大学与香港科大研发的专家并行 MoE 逐步实时负载均衡引擎，打破传统线性规划求解瓶颈，以 CUDA 算子及片上硬件块恢复 37.3% 的算力利用率。<br>• <b>OOM-MoE</b>: 香港科技大学（广州）针对全参数 MoE 训练的内存-执行协同卸载框架，通过参数预取流水线与显存复用极大降低跨互连传输等待。<br>• <b>Custom GPSIMD on Trainium</b>: UCLA 丛京生团队针对 AWS Trainium 3 构建首个 C++ 自定义 GPSIMD 算子编译工具链，加速 DeepSeek-V4.1 Engram 稀疏检索。<br>• <b>AdaOffload</b>: UC Berkeley Sky Computing 团队打造的异构多 GPU 混合专家卸载推理系统，全链路 NUMA 感知调度使超大 MoE 吞吐提升最高 15.5 倍。<br>• <b>Wasm Edge Cold-Start</b>: 根特大学-imec 研发的 WebAssembly 边缘调度器，联合优化产物缓存局部性与网络路由距离，降低边缘端到端冷启动延迟 40.8%。 | [查看全文](docs/2026-11-11.md) |
| **2026-11-09** | 0 篇 | 周末 / 节假日 arXiv 无新增论文 | [查看全文](docs/2026-11-09.md) |
| **2026-11-08** | 0 篇 | 周末 / 节假日 arXiv 无新增论文 | [查看全文](docs/2026-11-08.md) |
| **2026-11-07** | 0 篇 | 周末 / 节假日 arXiv 无新增论文 | [查看全文](docs/2026-11-07.md) |
| **2026-11-06** | 12 篇 | • <b>DMuon</b>: 针对新型矩阵优化器 Muon 与 FSDP/HSDP 拓扑冲突，首创矩阵粒度所有权与稀疏通信调度，在 256 卡 H100 集群上实现超越 AdamW 的训练吞吐。<br>• <b>FastAFD</b>: 针对 GB200 NVL72 机架级 NVLink 体系，系统性实测 Attention 与 MoE FFN 解耦收益，提出三因子解析模型指导微批流水线部署。<br>• <b>SiliconForge</b>: 针对 Prefill/Decode 与 AFD 细粒度解耦展开前瞻性算力与功耗建模，揭示跨代芯片与机架拓扑演进下 AFD 的落地边界。<br>• <b>KOSMOS</b>: AMD Instinct MI350X/MI355X 上的自调度持久化 Kernel，打破传统静态流水线，实现 Transformer 层 TP+SP 及 MoE 全链路通信计算重叠。<br>• <b>Locality Domains on Blackwell</b>: CUDA 13.4 双 Die 局部性域深度实测，揭示 B300 跨 Die 内存访问特异性与驱动内核模块 32MB 分配瓶颈及修复方案。<br>• <b>FlashOffloading</b>: 面向昇腾 910C 的长序列端到端 KV Cache 主机内存全卸载架构，已并入 vLLM-ascend 生产级代码。<br>• <b>OpenRDMA</b>: 提出 8 字节轻量 Doorbell 与 FPGA 网卡硬件重构 WQE，彻底卸载 GPU SM 控制开销的原生多路径可靠 RDMA 传输架构。<br>• <b>FlexFloor</b>: 基于弹性专家并行（EEP）解决 MoE 强化学习后训练（RLHF）尾延迟与长尾响应阻塞，实现计算节点即时释放。<br>• <b>Memory Fit</b>: 面向 CXL 与非易失性异构内存的 Linux 6.6 页面放置硬件抽象，以仅 64 位元数据达到接近理论最优的页面分层放置。<br>• <b>NUMA-Torch</b>: 编译器层级 NUMA 感知 Tensor Parallelism，将多路服务器 CPU 视作独立分区，消除跨 Socket UPI 互连瓶颈。<br>• <b>StrataFlux</b>: 低比特大模型量化流式精度补偿系统，利用主机 RAM/SSD 作为分级存储按需补充关键精度，显存减半且无损输出。<br>• <b>ZYFA</b>: 针对 AMD CDNA4 (MI355X) 架构软硬件特性的 FP8 FlashAttention 与 DeepSeek MLA 算子极限性能与数值精度优化。 | [查看全文](docs/2026-11-06.md) |
| **2026-11-05** | 12 篇 | • <b>GC-MoE</b>: 阿里巴巴开源的 MoE 生产级推理算子，创新性引入硬件级 CUDA Green Contexts 进行 SM 空间硬切分，实现全互联 Token 分发与低精度 Grouped GEMM 的完全掩盖重叠，在 H20/B300 上全线超越 DeepGEMM Mega MoE。<br>• <b>A Year in LLM Serving</b>: 芝加哥大学、哈佛大学与 Chutes 联合开源发布长达一年的真实大模型生产推理数据集（Chutes/OpenRouter），系统性解构前缀缓存（Prefix Caching）在真实长文本/Agent 负载中的命中规律，实证揭示全局缓存感知路由如何削减 41% 尾延迟。<br>• <b>Characterizing Serverless Workloads</b>: 柏林工大与德国 Fraunhofer 研究所横向对比横跨阿里、Azure、华为、IBM 等各大云厂商的 8 个 FaaS 数据集，系统性解密现代 Serverless 容器冷启动、超高并发突刺及严重内存超卖闲置现状，为 K8s 弹性调度器提供扎实量化基准。 | [查看全文](docs/2026-11-05.md) |
| **2026-11-04** | 12 篇 | • <b>RTP-LLM</b>: 阿里巴巴开源并披露其支撑全集团核心业务日均数百兆 Token 生产流量的统一大模型推理底座，实现模型专有算子执行与通用集群资源调度的深度解耦。<br>• <b>When Cache Pressure Becomes a Trap</b>: 首次揭示 PD 分离云原生推理集群中，瞬时突发流量破坏 Agent 历史前缀缓存复用后所引发的不可自愈“亚稳态失效陷阱”，给出精准数学建模与自愈防护系统 Basin。<br>• <b>TenonAgent</b>: 针对长程 Agent 沙箱与容器环境面临的内存峰值预留浪费与超卖 OOM 崩溃困境，基于 Linux sched_ext 和双时间尺度控制面实现了突破性的执行驻留虚拟化与高达 8.6 倍的内存安全超卖。 | [查看全文](docs/2026-11-04.md) |
| **2026-11-03** | 12 篇 | • <b>HiState</b>: 直击 Agent 工作流频繁回溯历史会爆显存的痛点，给出了 SSD + 显存分层管理循环快照的优雅解法。<br>• <b>ARK</b>: 针对 PD 分离架构中跨节点搬运 KV Cache 导致 ECMP 网络哈希冲突的难题，提出了发送端自适应端口协调机制。<br>• <b>Matching Workloads to Blackwell</b>: 揭示了下一代 B300 相比 B200 在部分卷积与 70B LLM 推理上因功耗未能打满而性能倒退的现象，对云原生 GPU 集群选型有极高参考价值。 | [查看全文](docs/2026-11-03.md) |
| **2026-11-02** | 7 篇 | • <b>ARK</b>: 针对大模型 PD 分离架构中跨节点搬运庞大 KV Cache 引发的网络哈希冲突（ECMP 拥塞），提出零修改交换机的发送端协同路由方案，P95 传输完成时间降低 34%。<br>• <b>LLM Fine-Tuning Workloads</b>: 基于 IBM 30,920 次实际微调任务的大规模实测，揭示了 Serverless 环境下微调任务高达 95% 的潜在配置失败率，为云原生平台设计 Serverless 训练运行时提供了关键指导。<br>• <b>HiState</b>: 巧妙把 Agent 循环交互中的长尾历史 Checkpoint 卸载到 SSD，实现仅消耗常数级 GPU 显存恢复上下文，p99 首字延迟（TTFT）大幅降低超 5 倍。 | [查看全文](docs/2026-11-02.md) |
---
*由 Google Antigravity 定时自动化流水线每日早晨自动分析并生成推送。*
