# 计算机系统结构作业仓库

本仓库对应课程 **计算机系统结构** 的 Git 作业。项目名称按老师要求使用 `arch`。用户名使用学号注册校内 GitLab，并把 `cshao` 加为 **Maintainer**。


| | |
| -: | :- |
|科目|计算机系统结构|
|班级|软件工程4班|
|学号|3124004588|
|姓名|林润鑫|

- 作业 1：[作业1.md](作业1.md)（2026-09-03）
- 作业 2：[作业2.md](作业2.md)（2026-09-10）


每次作业在根目录保留一个 `作业x.md`。编程相关源码放在 `作业x代码/`，图片放在 `imgs/`，路径一律写相对路径。

## 目录

```
.
│  .gitignore
│  homework_from_cshao.md
│  README.md
│  作业1.md
│  作业2.md
│
├─from_cshao/          # 老师目录，不在此改评语
├─imgs/                # Markdown 引用的图片
├─scripts/             # 生成 imgs 的辅助脚本（非作业要求）
└─作业1代码/
       cache_map.c     # 作业 1 自拟示例程序
```

本地查看：用支持 Markdown 的编辑器打开 `作业1.md`、`作业2.md`。校内提交：在服务器开放时段（周一、周四下午约 17:00 开启，次日 01:00 关闭）推到 `http://10.21.21.251`。先访问该页面确认服务器是否在线。

`from_cshao/` 由老师写入 `check.md`、`Comments.md` 等文件，不要自行修改。`homework_from_cshao.md` 是布置说明原文。

---



## 作业 1 正文

完整排版与图片见 [作业1.md](作业1.md)。下面保留作业内容，方便 GitLab 首页直接阅读。

### 计算机系统结构在研究什么

计算机系统结构关心的是：指令系统、微结构、存储层次和系统互连如何共同决定一台机器的性能、功耗与可编程性。

### 冯·诺依曼结构

![冯·诺依曼体系结构](imgs/1_von_neumann.png)

程序与数据共用存储器。现代 CPU 对外仍是这一编程模型，片内 Cache 则常按哈佛结构把指令和数据分开。

### 指令流水线

![经典五级流水线](imgs/1_pipeline.png)

五级为 IF / ID / EX / MEM / WB。数据相关、控制相关、结构相关会插入气泡。

### 存储层次

![存储层次](imgs/1_memory_hierarchy.png)

### 自拟代码：直接映射 Cache

源文件：[`作业1代码/cache_map.c`](作业1代码/cache_map.c)

假设 32KB Cache、64B 块、直接映射：offset 6 位，index 9 位，其余为 tag。

```c
#include <stdio.h>
#include <stdint.h>

int main(void) {
    const unsigned cache_bytes = 32 * 1024;
    const unsigned block_bytes = 64;
    const unsigned num_sets = cache_bytes / block_bytes;
    const unsigned offset_bits = 6;
    const unsigned index_bits = 9;
    uint32_t addrs[] = {0x00001234u, 0x00008234u, 0x0010F000u};
    int n = (int)(sizeof(addrs) / sizeof(addrs[0]));
    printf("sets=%u  offset_bits=%u  index_bits=%u\n",
           num_sets, offset_bits, index_bits);
    for (int i = 0; i < n; i++) {
        uint32_t addr = addrs[i];
        unsigned offset = addr & ((1u << offset_bits) - 1u);
        unsigned index = (addr >> offset_bits) & ((1u << index_bits) - 1u);
        unsigned tag = addr >> (offset_bits + index_bits);
        printf("addr=0x%08X  tag=0x%X  index=%u  offset=%u\n",
               addr, tag, index, offset);
    }
    return 0;
}
```

编译运行：

```bash
gcc -O0 -Wall -o cache_map 作业1代码/cache_map.c
./cache_map
```

---



## 作业 2 正文

完整论述、对照表和参考链接见 [作业2.md](作业2.md)。GitLab 首页摘要如下。

### 路线总览

![国产芯片主要指令集与架构路线](imgs/2_isa_landscape.png)

### 华为麒麟 9050 Pro

端侧 SoC。灵犀 CPU 为 `1+2+4+2` 九核并支持超线程；马良 GPU 支持硬件光追；达芬奇 NPU 面向端侧 MoE 大模型；封装使用 LogicFolding 混合键合。

![麒麟 9050 Pro 片上系统示意](imgs/2_kirin_soc.png)

### 龙芯 LoongArch

自主指令集。桌面 3A6000 为 4 核 8 线程 LA664；服务器 3C6000 用龙链扩展到 16/32/64 核。

![龙芯 3A6000 / 3C6000 微架构要点](imgs/2_loongson.png)

### 寒武纪 MLU

领域专用智能芯片。4 个 MLU Core 加 Memory Core 与共享 SRAM 构成 Cluster。思元 370 采用 MLUarch03 与 7nm Chiplet，双芯卡峰值约 256 TOPS（INT8）。

![寒武纪 MLU Cluster 抽象结构](imgs/2_cambricon.png)

### 对照（节选）


| 产品                     | 企业   | ISA / 架构                  | 课堂关键词                 |
| ---------------------- | ---- | ------------------------- | --------------------- |
| 麒麟 9050 Pro            | 华为海思 | ARM 自研 + 达芬奇              | 异构 SoC、SMT、3D 键合      |
| 龙芯 3A6000 / 3C6000     | 龙芯中科 | LoongArch                 | 自主 ISA、乱序、龙链          |
| 思元 370                 | 寒武纪  | MLUarch03                 | Cluster、NRAM、MLU-Link |
| 鲲鹏 920 / 昇腾 910B       | 华为   | ARMv8.2 / 达芬奇             | 服务器 CPU、训练 NPU        |
| 飞腾 / 海光 / 兆芯 / 申威 / 玄铁 | 各厂商  | ARM / x86 / SW64 / RISC-V | 授权、兼容、超算、开源           |


数字来自厂商手册和 2026 年 9 月前后公开报道，仅供作业使用。
