#!/usr/bin/env python3
"""Generate diagrams used by 作业3.md and 作业4.md."""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
from matplotlib import font_manager

FONT = "/System/Library/Fonts/Hiragino Sans GB.ttc"
font_manager.fontManager.addfont(FONT)
plt.rcParams["font.family"] = "Hiragino Sans GB"
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["text.parse_math"] = False  # 代码里的 $t0 不应被当成数学公式

OUT = Path(__file__).resolve().parent.parent / "imgs"
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


def arrow(ax, x1, y1, x2, y2, color=NAVY, style="-|>"):
    ax.add_patch(
        FancyArrowPatch(
            (x1, y1),
            (x2, y2),
            arrowstyle=style,
            mutation_scale=13,
            linewidth=1.5,
            color=color,
        )
    )


def save(fig, name):
    path = OUT / name
    fig.savefig(path, dpi=160, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    print(path)


def classification():
    """四种常见的计算机系统结构分类法。"""
    fig, ax = plt.subplots(figsize=(11.4, 6.6), facecolor=BG)
    ax.set_xlim(0, 11.4)
    ax.set_ylim(0, 6.6)
    ax.axis("off")
    ax.set_title("计算机系统结构的四种分类法", fontsize=16, color=NAVY, pad=8)

    rounded(ax, 0.4, 5.45, 10.6, 0.75, "分类的共同出发点：机器能同时处理多少信息，以及这些信息由几股“流”驱动", NAVY, fs=12)

    cards = [
        (0.4, 2.95, TEAL, "冯氏分类法", "按最大并行度 Pm\n坐标 (字宽 n, 位片宽 m)\nWSBS / WPBS\nWSBP / WPBP"),
        (3.1, 2.95, BLUE, "Flynn 分类法", "按指令流与数据流的多倍性\nSISD / SIMD / MISD / MIMD\n最常用，本次作业重点"),
        (5.8, 2.95, PURPLE, "Handler 分类法", "按硬件并行与流水程度\nt(系统) = (k×k', d×d', w×w')\nPCU / ALU / ELC 三级"),
        (8.5, 2.95, ORANGE, "库克分类法", "按指令流与执行流的多倍性\nSISE / SIME / MISE / MIME\n关注控制而非数据"),
    ]
    for x, y, color, title, body in cards:
        rounded(ax, x, y + 1.35, 2.5, 0.65, title, color, fs=12)
        rounded(ax, x, y - 0.35, 2.5, 1.6, body, "#ffffff", ec=color, fs=9.5, tc=INK, lw=1.2)

    rounded(
        ax,
        0.4,
        0.45,
        10.6,
        1.5,
        "Flynn 分类法被广泛采用的原因：只用“指令流条数 × 数据流条数”两个维度，\n"
        "就能把单处理机、向量机 / GPU、流水容错阵列和多核多处理机区分开；\n"
        "代价是粒度粗——同为 MIMD 的多核 CPU 与机群，内部结构可以完全不同。",
        "#ffffff",
        ec=NAVY,
        fs=10.5,
        tc=INK,
        lw=1.2,
    )
    save(fig, "3_classification.png")


def flynn():
    """Flynn 四类结构框图。"""
    fig, ax = plt.subplots(figsize=(11.4, 7.6), facecolor=BG)
    ax.set_xlim(0, 11.4)
    ax.set_ylim(0, 7.6)
    ax.axis("off")
    ax.set_title("Flynn 分类法：指令流 × 数据流", fontsize=16, color=NAVY, pad=10)

    quads = [
        (0.45, 4.05, NAVY, "SISD  单指令流单数据流",
         "一个控制器 CU 发出一条指令流 IS，\n一个处理单元 PU 处理一条数据流 DS。\n典型：传统单处理机、早期 x86",
         ["CU", "PU", "MM"]),
        (5.95, 4.05, TEAL, "SIMD  单指令流多数据流",
         "一条指令流同时驱动多个 PU，\n每个 PU 处理各自的数据流。\n典型：阵列机、向量机、GPU、AVX",
         ["CU", "PU×n", "MM×n"]),
        (0.45, 0.45, PURPLE, "MISD  多指令流单数据流",
         "多条指令流作用在同一数据流上，\n数据被逐级加工。学术上有争议，\n常举例：脉动阵列、多模冗余容错",
         ["CU×n", "PU×n", "MM"]),
        (5.95, 0.45, ORANGE, "MIMD  多指令流多数据流",
         "多个控制器各自取指，\n多个 PU 处理各自的数据流。\n典型：多核 CPU、多处理机、机群",
         ["CU×n", "PU×n", "MM×n"]),
    ]
    for x, y, color, title, body, chain in quads:
        rounded(ax, x, y, 5.0, 3.1, "", "#ffffff", ec=color, lw=1.6)
        rounded(ax, x + 0.15, y + 2.35, 4.7, 0.6, title, color, fs=11.5)
        ax.text(x + 2.55, y + 1.85, body, ha="center", va="center", fontsize=9.5, color=INK)
        for i, label in enumerate(chain):
            bx = x + 0.55 + i * 1.55
            rounded(ax, bx, y + 0.35, 1.15, 0.55, label, color, fs=10)
            if i < len(chain) - 1:
                arrow(ax, bx + 1.15, y + 0.63, bx + 1.55, y + 0.63, color=color)
        ax.text(x + 1.35, y + 1.08, "IS", fontsize=8.5, color=MUTED, ha="center")
        ax.text(x + 2.9, y + 1.08, "DS", fontsize=8.5, color=MUTED, ha="center")

    save(fig, "3_flynn.png")


def amdahl():
    """Amdahl 定律：30% 的部分加速 20 倍。"""
    fig, (ax1, ax2) = plt.subplots(
        1, 2, figsize=(12.0, 4.8), facecolor=BG, gridspec_kw={"width_ratios": [1.15, 1]}
    )
    for ax in (ax1, ax2):
        ax.set_facecolor(BG)

    # 左：执行时间分解
    ax1.set_xlim(0, 1.08)
    ax1.set_ylim(0, 2.3)
    ax1.axis("off")
    ax1.set_title("执行时间分解（改进前后）", fontsize=13, color=NAVY)

    ax1.add_patch(Rectangle((0, 1.45), 0.70, 0.45, facecolor="#cfd8e3", edgecolor=NAVY))
    ax1.add_patch(Rectangle((0.70, 1.45), 0.30, 0.45, facecolor=ORANGE, edgecolor=NAVY))
    ax1.text(0.35, 1.675, "不可改进  70%", ha="center", va="center", fontsize=10, color=INK)
    ax1.text(0.85, 1.675, "可改进 30%", ha="center", va="center", fontsize=9.5, color="white")
    ax1.text(-0.02, 2.02, "改进前  T0 = 1", fontsize=11, color=NAVY)

    ax1.add_patch(Rectangle((0, 0.65), 0.70, 0.45, facecolor="#cfd8e3", edgecolor=NAVY))
    ax1.add_patch(Rectangle((0.70, 0.65), 0.015, 0.45, facecolor=TEAL, edgecolor=NAVY))
    ax1.text(0.35, 0.875, "不可改进  70%", ha="center", va="center", fontsize=10, color=INK)
    ax1.annotate(
        "0.30 / 20 = 0.015",
        xy=(0.7075, 0.65),
        xytext=(0.80, 0.30),
        fontsize=9.5,
        color=TEAL,
        arrowprops=dict(arrowstyle="-|>", color=TEAL, lw=1.3),
    )
    ax1.text(-0.02, 1.22, "改进后  Tn = 0.715", fontsize=11, color=NAVY)
    ax1.text(0.0, 0.05, "加速比 Sn = 1 / 0.715 ≈ 1.399，性能提高约 39.9%", fontsize=11, color=INK)

    # 右：Fe-Sn 曲线
    fe = [i / 200 for i in range(201)]
    se = 20
    sn = [1 / ((1 - f) + f / se) for f in fe]
    ax2.plot(fe, sn, color=NAVY, lw=2)
    ax2.axvline(0.3, color=ORANGE, ls="--", lw=1.2)
    ax2.axhline(1 / 0.715, color=ORANGE, ls="--", lw=1.2)
    ax2.plot([0.3], [1 / 0.715], "o", color=ORANGE, ms=7)
    ax2.annotate(
        "(0.30, 1.399)",
        xy=(0.3, 1 / 0.715),
        xytext=(0.36, 3.2),
        fontsize=10,
        color=ORANGE,
        arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=1.2),
    )
    ax2.set_xlabel("可改进比例 Fe", fontsize=11, color=INK)
    ax2.set_ylabel("系统加速比 Sn", fontsize=11, color=INK)
    ax2.set_title("Se = 20 时 Fe–Sn 关系", fontsize=13, color=NAVY)
    ax2.grid(alpha=0.3)
    ax2.set_ylim(1, 21)

    fig.tight_layout()
    save(fig, "3_amdahl.png")


def isa_class():
    """指令集结构的四种分类，以 C = A + B 为例。"""
    fig, ax = plt.subplots(figsize=(11.6, 6.4), facecolor=BG)
    ax.set_xlim(0, 11.6)
    ax.set_ylim(0, 6.4)
    ax.axis("off")
    ax.set_title("指令集结构分类：CPU 内部操作数存放在哪里（以 C = A + B 为例）", fontsize=14.5, color=NAVY, pad=8)

    cols = [
        (0.35, NAVY, "堆栈型", "Push  A\nPush  B\nAdd\nPop   C", "操作数隐含在栈顶\n指令短，但栈顶是瓶颈"),
        (3.20, BLUE, "累加器型", "Load  A\nAdd   B\nStore C", "一个操作数隐含为累加器\n访存频繁"),
        (6.05, TEAL, "寄存器-存储器\n（RM）", "Load  R1, A\nAdd   R1, B\nStore C,  R1", "指令可直接访存\n代码密度高，CPI 不均匀"),
        (8.90, ORANGE, "寄存器-寄存器\n（RR，load-store）", "Load  R1, A\nLoad  R2, B\nAdd   R3, R1, R2\nStore C,  R3", "只有 load/store 访存\nCPI 规整，利于流水，MIPS 属此类"),
    ]
    for x, color, title, code, note in cols:
        rounded(ax, x, 5.00, 2.55, 0.95, title, color, fs=11.5)
        rounded(ax, x, 2.45, 2.55, 2.35, code, "#ffffff", ec=color, fs=10.5, tc=INK, lw=1.3)
        rounded(ax, x, 1.05, 2.55, 1.15, note, "#ffffff", ec=color, fs=8.8, tc=MUTED, lw=1.0)

    ax.text(
        5.8,
        0.45,
        "通用寄存器型胜出的根本原因：寄存器访问快、可由编译器自由分配，能有效减少访存次数。",
        ha="center",
        fontsize=10.5,
        color=INK,
    )
    save(fig, "4_isa_class.png")


def mips_format():
    """MIPS 三种指令格式的位域。"""
    fig, ax = plt.subplots(figsize=(11.6, 6.2), facecolor=BG)
    ax.set_xlim(0, 11.6)
    ax.set_ylim(0, 6.2)
    ax.axis("off")
    ax.set_title("MIPS 指令格式：32 位定长、字段位置固定", fontsize=15, color=NAVY, pad=8)

    left, width = 0.9, 10.1

    def draw_row(y, fields, color, name, example):
        ax.text(0.15, y + 0.32, name, fontsize=12, color=color, va="center", weight="bold")
        x = left
        for label, bits in fields:
            w = width * bits / 32
            ax.add_patch(Rectangle((x, y), w, 0.66, facecolor=color, edgecolor="white", lw=1.4))
            ax.text(x + w / 2, y + 0.40, label, ha="center", va="center", fontsize=9.5, color="white")
            ax.text(x + w / 2, y + 0.14, f"{bits} 位", ha="center", va="center", fontsize=8, color="#e8e8e8")
            x += w
        ax.text(left, y - 0.28, example, fontsize=10, color=INK, parse_math=False)

    draw_row(
        4.60,
        [("op", 6), ("rs", 5), ("rt", 5), ("rd", 5), ("shamt", 5), ("funct", 6)],
        NAVY,
        "R 型",
        "add $t0, $s1, $s2     # 寄存器运算，op=0，功能由 funct 决定",
    )
    draw_row(
        3.00,
        [("op", 6), ("rs", 5), ("rt", 5), ("immediate / offset", 16)],
        TEAL,
        "I 型",
        "lw $t0, 32($s3)       # 访存、立即数运算、条件分支",
    )
    draw_row(
        1.40,
        [("op", 6), ("address（字地址）", 26)],
        ORANGE,
        "J 型",
        "j 1024                # 无条件跳转，目标地址 = PC[31:28] || address || 00",
    )

    ax.text(left, 5.70, "位序：31 ────────────────────────────────────────────── 0", fontsize=10, color=MUTED)
    ax.text(
        left,
        0.55,
        "三种格式的 op 都在同一位置、rs 和 rt 也对齐：取指后不必先译码就能开始读寄存器堆，这正是流水线能规整划分的前提。",
        fontsize=10,
        color=INK,
    )
    save(fig, "4_mips_format.png")


def quant_principles():
    """第一章剩余内容：定量分析技术知识地图。"""
    fig, ax = plt.subplots(figsize=(11.4, 6.6), facecolor=BG)
    ax.set_xlim(0, 11.4)
    ax.set_ylim(0, 6.6)
    ax.axis("off")
    ax.set_title("第一章剩余内容：定量分析技术与系统结构的发展", fontsize=15, color=NAVY, pad=8)

    rounded(ax, 0.4, 5.35, 10.6, 0.8, "设计目标：在成本、功耗、面积的约束下，用定量数据而不是直觉做取舍", NAVY, fs=12)

    items = [
        (0.4, TEAL, "以经常性事件为重点", "把资源优先给高频事件\n（Make the common case fast）"),
        (3.05, BLUE, "Amdahl 定律", "Sn = 1 / [(1-Fe) + Fe/Se]\n上限 1/(1-Fe)"),
        (5.70, PURPLE, "CPU 性能公式", "CPU 时间 = IC × CPI × T\n三个因子互相牵制"),
        (8.35, ORANGE, "程序局部性原理", "时间局部性 + 空间局部性\n存储层次成立的前提"),
    ]
    for x, color, title, body in items:
        rounded(ax, x, 4.00, 2.65, 0.7, title, color, fs=11)
        rounded(ax, x, 2.75, 2.65, 1.15, body, "#ffffff", ec=color, fs=9.5, tc=INK, lw=1.2)

    rounded(ax, 0.4, 1.45, 5.15, 1.1, "性能评测\nMIPS / MFLOPS 受指令集与程序影响大；\n用 SPEC 等测试程序套件 + 几何平均更可靠", "#ffffff", ec=NAVY, fs=10, tc=INK, lw=1.3)
    rounded(ax, 5.85, 1.45, 5.15, 1.1, "系统结构的发展\n冯·诺依曼结构 → 系列机与软件兼容 →\n软硬件功能分配 → 并行性从位级走向多核", "#ffffff", ec=NAVY, fs=10, tc=INK, lw=1.3)

    ax.text(
        5.7,
        0.85,
        "并行性的发展路径：位级并行 → 指令级并行 → 线程级并行 → 任务级 / 作业级并行；"
        "实现手段分为时间重叠、资源重复、资源共享三类。",
        ha="center",
        fontsize=10,
        color=INK,
        wrap=True,
    )
    save(fig, "4_parallel_quant.png")


if __name__ == "__main__":
    classification()
    flynn()
    amdahl()
    isa_class()
    mips_format()
    quant_principles()
