#!/usr/bin/env python3
"""Generate diagrams used by 作业1.md and 作业2.md."""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
from matplotlib import font_manager

FONT = "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc"
font_manager.fontManager.addfont(FONT)
plt.rcParams["font.family"] = "WenQuanYi Micro Hei"
plt.rcParams["axes.unicode_minus"] = False

OUT = Path("/workspace/imgs")
OUT.mkdir(parents=True, exist_ok=True)

NAVY = "#1f3a5f"
TEAL = "#2a9d8f"
ORANGE = "#e76f51"
GOLD = "#e9c46a"
BLUE = "#457b9d"
PURPLE = "#6d597a"
BG = "#f7f4ef"
INK = "#1b1b1b"
MUTED = "#5c5c5c"


def rounded(ax, x, y, w, h, text, fc, ec=NAVY, fs=11, tc="white", lw=1.4):
    box = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.02,rounding_size=0.08",
        linewidth=lw,
        facecolor=fc,
        edgecolor=ec,
    )
    ax.add_patch(box)
    ax.text(
        x + w / 2,
        y + h / 2,
        text,
        ha="center",
        va="center",
        fontsize=fs,
        color=tc,
        wrap=True,
    )


def arrow(ax, x1, y1, x2, y2, color=NAVY):
    ax.add_patch(
        FancyArrowPatch(
            (x1, y1),
            (x2, y2),
            arrowstyle="-|>",
            mutation_scale=14,
            linewidth=1.6,
            color=color,
        )
    )


def save(fig, name):
    path = OUT / name
    fig.savefig(path, dpi=160, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    print(path)


def von_neumann():
    fig, ax = plt.subplots(figsize=(10.5, 6.4), facecolor=BG)
    ax.set_xlim(0, 10.5)
    ax.set_ylim(0, 6.4)
    ax.axis("off")
    ax.set_title("冯·诺依曼体系结构（作业 1）", fontsize=16, color=NAVY, pad=8)

    rounded(ax, 3.6, 5.15, 3.3, 0.85, "控制单元 CU", NAVY, fs=13)
    rounded(ax, 0.4, 3.35, 3.3, 0.95, "运算器 ALU", TEAL, fs=13)
    rounded(ax, 6.8, 3.35, 3.3, 0.95, "存储器 Memory", BLUE, fs=13)
    rounded(ax, 0.4, 1.15, 3.3, 0.95, "输入设备", ORANGE, fs=13)
    rounded(ax, 6.8, 1.15, 3.3, 0.95, "输出设备", GOLD, fs=13, tc=INK)

    # buses
    ax.plot([5.25, 5.25], [5.15, 4.3], color=NAVY, lw=1.8)
    ax.plot([2.05, 8.45], [3.82, 3.82], color=NAVY, lw=1.8)
    ax.plot([2.05, 2.05], [3.35, 2.1], color=NAVY, lw=1.8)
    ax.plot([8.45, 8.45], [3.35, 2.1], color=NAVY, lw=1.8)
    ax.plot([2.05, 8.45], [2.1, 2.1], color=NAVY, lw=1.8)

    ax.text(5.25, 4.55, "控制信号", ha="center", fontsize=9, color=MUTED)
    ax.text(5.25, 3.95, "数据 / 地址总线", ha="center", fontsize=9, color=MUTED)
    ax.text(
        5.25,
        0.35,
        "程序与数据存放在同一存储器中，CPU 按地址顺序取出指令并执行。",
        ha="center",
        fontsize=10,
        color=INK,
    )
    save(fig, "1_von_neumann.png")


def pipeline():
    fig, ax = plt.subplots(figsize=(11.2, 5.6), facecolor=BG)
    ax.set_xlim(0, 11.2)
    ax.set_ylim(0, 5.6)
    ax.axis("off")
    ax.set_title("经典五级流水线", fontsize=16, color=NAVY, pad=8)

    stages = [
        (0.4, "IF\n取指", NAVY),
        (2.6, "ID\n译码", TEAL),
        (4.8, "EX\n执行", ORANGE),
        (7.0, "MEM\n访存", BLUE),
        (9.2, "WB\n写回", PURPLE),
    ]
    for x, text, color in stages:
        rounded(ax, x, 3.2, 1.7, 1.35, text, color, fs=13)
    for i in range(4):
        arrow(ax, 2.1 + 2.2 * i, 3.87, 2.6 + 2.2 * i, 3.87)

    ax.text(5.6, 2.55, "同一时刻，不同指令停留在不同流水段", ha="center", fontsize=11, color=INK)

    # mini timeline
    colors = [NAVY, TEAL, ORANGE, BLUE, PURPLE]
    labels = ["IF", "ID", "EX", "MEM", "WB"]
    for row, inst in enumerate(["I1", "I2", "I3"]):
        ax.text(0.35, 1.85 - row * 0.55, inst, ha="left", va="center", fontsize=10, color=INK)
        for col in range(5):
            cidx = col
            if col + row < 7:
                x = 1.3 + (col + row) * 1.25
                y = 1.6 - row * 0.55
                ax.add_patch(
                    Rectangle((x, y), 1.1, 0.42, facecolor=colors[cidx], edgecolor="white")
                )
                ax.text(
                    x + 0.55,
                    y + 0.21,
                    labels[cidx],
                    ha="center",
                    va="center",
                    fontsize=8,
                    color="white",
                )
    save(fig, "1_pipeline.png")


def memory_hierarchy():
    fig, ax = plt.subplots(figsize=(9.6, 6.4), facecolor=BG)
    ax.set_xlim(0, 9.6)
    ax.set_ylim(0, 6.4)
    ax.axis("off")
    ax.set_title("存储层次：速度、容量与成本", fontsize=16, color=NAVY, pad=8)

    layers = [
        (3.35, 5.15, 2.9, 0.7, "寄存器  Register", NAVY, "最快 / 最小"),
        (2.85, 4.15, 3.9, 0.7, "L1 / L2 / L3 Cache", TEAL, "片上缓存"),
        (2.25, 3.15, 5.1, 0.7, "主存  DRAM", BLUE, "容量增大"),
        (1.55, 2.15, 6.5, 0.7, "固态硬盘 / 磁盘", ORANGE, "最慢 / 最大"),
    ]
    for x, y, w, h, title, color, note in layers:
        rounded(ax, x, y, w, h, title, color, fs=12)
        ax.text(x + w + 0.18, y + h / 2, note, ha="left", va="center", fontsize=10, color=MUTED)

    ax.text(0.5, 1.2, "访问延迟 ↑", fontsize=11, color=INK)
    ax.text(7.2, 1.2, "容量 ↑  单位成本 ↓", fontsize=11, color=INK)
    save(fig, "1_memory_hierarchy.png")


def isa_landscape():
    fig, ax = plt.subplots(figsize=(11.4, 6.6), facecolor=BG)
    ax.set_xlim(0, 11.4)
    ax.set_ylim(0, 6.6)
    ax.axis("off")
    ax.set_title("国产芯片主要指令集 / 架构路线", fontsize=16, color=NAVY, pad=8)

    groups = [
        (0.35, 4.55, 3.3, "自主指令集", NAVY, ["龙芯 LoongArch", "申威 SW64"]),
        (4.05, 4.55, 3.3, "ARM 授权自研", TEAL, ["华为麒麟 / 鲲鹏", "飞腾 Phytium"]),
        (7.75, 4.55, 3.3, "x86 授权兼容", ORANGE, ["海光 C86", "兆芯开先 / 开胜"]),
        (0.35, 1.55, 3.3, "开源 RISC-V", BLUE, ["平头哥玄铁", "香山 / 玄铁 C 系列"]),
        (4.05, 1.55, 3.3, "AI 专用架构", PURPLE, ["寒武纪 MLU", "华为达芬奇 / 昇腾"]),
        (7.75, 1.55, 3.3, "典型场景", GOLD, ["端侧手机 SoC", "服务器 / 超算 / 智算"]),
    ]
    for x, y, w, title, color, items in groups:
        rounded(ax, x, y + 1.15, w, 0.7, title, color, fs=12, tc="white" if color != GOLD else INK)
        for i, item in enumerate(items):
            rounded(
                ax,
                x + 0.12,
                y + 0.55 - i * 0.55,
                w - 0.24,
                0.46,
                item,
                "#ffffff",
                ec=color,
                fs=10,
                tc=INK,
                lw=1.1,
            )
    save(fig, "2_isa_landscape.png")


def kirin_soc():
    fig, ax = plt.subplots(figsize=(11.2, 6.5), facecolor=BG)
    ax.set_xlim(0, 11.2)
    ax.set_ylim(0, 6.5)
    ax.axis("off")
    ax.set_title("麒麟 9050 Pro 片上系统示意（公开信息整理）", fontsize=15, color=NAVY, pad=8)

    rounded(ax, 0.35, 0.4, 10.5, 5.55, "", "#ffffff", ec=NAVY, lw=1.6)
    ax.text(5.6, 5.55, "Kirin 9050 Pro  /  LogicFolding 逻辑折叠", ha="center", fontsize=12, color=NAVY)

    blocks = [
        (0.7, 3.55, 3.1, 1.55, "灵犀 CPU\n1+2+4+2 九核\n超线程：9核16线程", NAVY),
        (4.05, 3.55, 3.1, 1.55, "马良 GPU\n硬件光追\n渲染性能 +142%", TEAL),
        (7.4, 3.55, 3.1, 1.55, "达芬奇 NPU\n约 70 TOPS INT8\n端侧 30B MoE", PURPLE),
        (0.7, 1.55, 3.1, 1.45, "巴龙基带\n5.5G + 卫星通信", BLUE),
        (4.05, 1.55, 3.1, 1.45, "缓存层次\n大核共享 L3\nSoC Cache 12MB", ORANGE),
        (7.4, 1.55, 3.1, 1.45, "封装工艺\n1.5μm 混合键合\n约 5000 万垂直互连", GOLD),
    ]
    for x, y, w, h, text, color in blocks:
        rounded(ax, x, y, w, h, text, color, fs=11, tc="white" if color != GOLD else INK)
    ax.text(
        5.6,
        0.85,
        "资料来自 2026 年公开报道与拆解，细节以华为官方为准。",
        ha="center",
        fontsize=9,
        color=MUTED,
    )
    save(fig, "2_kirin_soc.png")


def loongson():
    fig, ax = plt.subplots(figsize=(11.0, 6.3), facecolor=BG)
    ax.set_xlim(0, 11.0)
    ax.set_ylim(0, 6.3)
    ax.axis("off")
    ax.set_title("龙芯 3A6000 / 3C6000 微架构要点", fontsize=15, color=NAVY, pad=8)

    rounded(ax, 0.4, 4.35, 10.2, 1.3, "指令系统：LoongArch（自主 ISA，含向量 / 虚拟化 / 二进制翻译扩展）", NAVY, fs=13)
    cores = [
        (0.4, 2.55, "LA664 核\n六发射乱序\n4 定点 + 4 向量 + 4 访存"),
        (3.9, 2.55, "缓存\n64KB I/D L1\n256KB 私有 L2\n共享 L3"),
        (7.4, 2.55, "3A6000 桌面\n4 物理核 / 8 逻辑核\n2.0–2.5 GHz"),
    ]
    for x, y, text in cores:
        rounded(ax, x, y, 3.2, 1.5, text, TEAL, fs=11)
    rounded(ax, 0.4, 0.55, 4.95, 1.6, "3C6000 服务器\n单硅片 16 核 32 线程\n龙链可扩展到 64 核 / 128 线程", BLUE, fs=12)
    rounded(ax, 5.55, 0.55, 5.05, 1.6, "安全与 IO\n龙芯 SE（SM2/3/4）\nDDR4-3200 + PCIe / HT", ORANGE, fs=12)
    save(fig, "2_loongson.png")


def cambricon():
    fig, ax = plt.subplots(figsize=(11.0, 6.4), facecolor=BG)
    ax.set_xlim(0, 11.0)
    ax.set_ylim(0, 6.4)
    ax.axis("off")
    ax.set_title("寒武纪 MLU：Cluster / MLU Core 抽象结构", fontsize=15, color=NAVY, pad=8)

    rounded(ax, 0.35, 0.45, 10.3, 5.5, "", "#ffffff", ec=NAVY, lw=1.5)
    ax.text(5.5, 5.55, "一颗 MLU 芯片 = 多个 Cluster", ha="center", fontsize=12, color=NAVY)

    rounded(ax, 0.7, 3.15, 9.6, 2.05, "", "#eef6f4", ec=TEAL, lw=1.3)
    ax.text(5.5, 4.9, "Cluster", ha="center", fontsize=11, color=TEAL)
    for i, title in enumerate(["MLU Core 0", "MLU Core 1", "MLU Core 2", "MLU Core 3"]):
        rounded(ax, 0.95 + i * 2.35, 3.4, 2.15, 1.15, f"{title}\n向量 / 张量计算\nNRAM + WRAM", NAVY, fs=10)
    rounded(ax, 0.7, 1.55, 4.6, 1.3, "Memory Core\nSRAM ↔ DDR / Core 搬运", BLUE, fs=11)
    rounded(ax, 5.55, 1.55, 4.75, 1.3, "Shared SRAM\nCluster 内共享暂存", PURPLE, fs=11)
    ax.text(
        5.5,
        0.85,
        "思元 370：7nm Chiplet + MLUarch03，双芯卡峰值约 256 TOPS（INT8）",
        ha="center",
        fontsize=10,
        color=INK,
    )
    save(fig, "2_cambricon.png")


if __name__ == "__main__":
    von_neumann()
    pipeline()
    memory_hierarchy()
    isa_landscape()
    kirin_soc()
    loongson()
    cambricon()
