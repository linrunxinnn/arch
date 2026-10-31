#!/usr/bin/env python3
"""生成作业4修订及作业5—8的电子排版答题摘要，明确区分手写照片。"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
ROOT = Path(__file__).resolve().parent.parent
FONT = '/System/Library/Fonts/Hiragino Sans GB.ttc'
BG, NAVY, INK, TEAL = '#f7f4ef', '#1f3a5f', '#1b1b1b', '#2a9d8f'
DATA = {
4: [
('1.7  CPI、MIPS、执行时间', ['总指令数 = 129500；总周期 = 230000。', 'CPI = 230000/129500 = 1.77606。', 'MIPS = 400/CPI = 225.217。', 'T = 230000/(400×10^6) = 575 微秒。']),
('1.8  三种平均（A / B / C）', ['算术平均：25.325 / 2.80625 / 3.25 MIPS。', '几何平均：1.18921 / 0.59460 / 2.65915 MIPS。', '调和平均：0.24984 / 0.20942 / 2.10526 MIPS。', '每程序指令数相同，整组速率用调和平均。']),
('1.9  Amdahl 定律', ['S = 1 / (0.60 + 0.40/20) = 1.61290。', '性能提高 61.29%，执行时间减少 38%。']),
('1.10  三部件改进', ['0.1 = 0.425 - 0.9F3 → F3 = 36.111%。', 'T新 = 0.2 + 0.3/30 + 0.3/20 + 0.2/10 = 0.245。', '不可改进部分占新总时间：0.2/0.245 = 81.633%。']),
('1.11  浮点方案比较', ['CPI原 = 0.26×5 + 0.04×20 + 0.70×1.25 = 2.975。', '仅改 FPSQR：CPI = 2.295，S = 1.29630。', '全部 FP 改进：CPI = 1.775，S = 1.67606。', '方案二更优。FPSQR 已包含在 30% FP 中。'])],
5: [
('Intel Cache 历史（需区分范围）', ['80486：x86 片内统一 L1 8 KB。', 'Pentium Pro：L1 指令/数据各 8 KB；封装内 L2 256/512 KB。', 'Mendocino：同硅片 L2 128 KB；不能与封装内混淆。', 'Itanium（2001）：L1 16+16 KB，L2 96 KB，L3 2/4 MB。', 'Xeon MP（2002）：L1D 8 KB，L2 256 KB，L3 512 KB/1 MB。', 'Pentium 4 EE（2003）：桌面产品，L2 512 KB，L3 2 MB。']),
('2026 桌面样本：Core Ultra 7 270K Plus', ['8P+16E；L2 总计 40 MB，L3 36 MB。', 'Lion Cove 数据层次：48 KB L0D → 192 KB L1D → L2。', 'E 核 L1：每核 64 KB 指令 + 32 KB 数据。', '移动端 Series 3 的 388H：官方 Smart Cache 18 MB。', '查询日期 2026-10-31；具体来源与口径见 Markdown 正文。']),
('7.2  两种存储层次', ['Cache—主存：缓解速度差距，以硬件管理缓存行为主。', '主存—辅存：扩展地址空间，以操作系统管理页面为主。', '二者都利用局部性，但替换单位、代价与管理方式不同。']),
('7.4  主存块 5 的映像', ['全相联：Cache 任一块，索引字段 0 位，标记 5。', '两路组相联：5 mod 2 = 1，组索引 1，标记 2。', '直接映像：5 mod 4 = 1，块索引 01，标记 1。'])],
6: [
('7.6  相联度与整机性能', ['不命中率下降并不保证 CPU 更快。', '还需比较命中时间、时钟周期、不命中开销。']),
('7.10  直接映像 / 两路组相联', ['AMAT：2+0.014×80 = 3.12 ns；2.2+0.010×80 = 3.00 ns。', '每指令时间：2×2+1.2×0.014×80 = 5.344 ns。', '每指令时间：2×2.2+1.2×0.010×80 = 5.360 ns。', '直接映像约快 0.30%；AMAT 更好不代表 CPU 更快。']),
('7.12  写回 Cache 与 TLB', ['每指令访问 Cache 1.2 次。', '读块 = 40+32/4 = 48 拍；脏块比例 50%。', '平均不命中开销 = 48+0.5×48 = 72 拍。', '理想 TLB：CPI = 1.5+1.2m×72。', '三种 Cache：4.0056 / 3.4008 / 3.2280。', '按题面两类地址来源，TLB 附加 CPI = (1+1.2m)×0.002×20。', '实际 TLB：4.046992 / 3.441856 / 3.268960。', '若课堂按每 CPU 访存查 TLB：另见正文的计数模型说明。']),
('7.15  存储体数', ['最大带宽 = 4m B / 2 微秒 = 2m MB/s。', '实际带宽 = 0.6×2m = 1.2m MB/s。', '1.2m ≥ 4 → m ≥ 10/3 → 至少 4 体。'])],
7: [
('3.2  流水技术特点', ['分段处理、任务重叠；提高吞吐率，不保证缩短单任务延迟。', '各段均衡，连续输入，处理相关和冲突。']),
('3.5  三指令时序', ['末尾写、下周期读约定：MOVE 第 4 拍写 R1；', 'MUL 第 5—8 拍执行；ADD 第 7—9 拍执行。', 'RAW 与 R0 的 WAW 均需满足，共 9 拍。', '若同周期先写后读，则共 8 拍；完整时空图见正文。']),
('3.7  第三段循环一次', ['单任务：S1→S2→S3→S3→S4，耗时 5Δt。', '瓶颈 S3；最大吞吐率 1/(2Δt)。', '10 任务：T = 5Δt+9×2Δt = 23Δt。', 'TP = 10/(23Δt)，E = 50/(4×23) = 54.348%。', '展开 S3 为两段：T = 14Δt，TP = 5/(7Δt)。']),
('3.9  非线性调度', ['禁止间隔 F = {1,3,4,8}。', 'A = 10001101，B = 10101111，C = 10001111。', 'A --2→ B；B --5→ A；A --6→ C。', '完整状态转移表见正文，已穷举三个可达状态。', '最优周期 (2,5)*，平均间隔 3.5Δt。', '最大 TP = 2/(7Δt)。', '六任务起始拍：0,2,7,9,14,16；完成总时间 25Δt。', '实际 TP = 6/(25Δt)。'])],
8: [
('3.11  循环次数及约定', ['(R3-R2初值)/4 = 396/4 = 99 次循环。', 'IF / ID / EX / MEM / WB；ID 末判分支。', '寄存器前半周期写、后半周期读；正常旁路含 store 数据。', '下列主答案计至最后实际操作；括号为统一画满五段。']),
('无旁路 + 冻结分支', ['LW→加法、加法→SW、指针→DSUB、DSUB→分支各停 2 拍。', '迭代启动间隔 6+8+1 = 15 拍。', '最后分支解析：99×15 = 1485 拍（末 WB 1488）。']),
('正常旁路 + 预测不成功', ['load–use 停 1 拍，DSUB→ID 判分支停 1 拍。', '成功分支冲刷 1 拍，迭代启动间隔 9 拍。', '最后分支解析：98×9+9 = 891 拍（末 WB 894）。']),
('正常旁路 + 单周期延迟槽', ['重排为：LW；指针加 4；DSUB；R1 加 1；BNEZ；SW。', '延迟槽 SW 使用 -4(R2)，最后分支失败也必须执行。', '迭代间隔 6 拍，末 SW 访存结束 98×6+9 = 597 拍。', '若统一画满末 SW 的 WB，则为 598 拍。']),
('3.12  控制相关', ['顺序取指/预测不成功：额外 CPI = 0.2×0.6×2+0.05×1。', 'CPI = 1.29；无控制相关相对加速比 1.29。', '若遇分支一律冻结，CPI = 1+0.2×2+0.05 = 1.45。', '两种取指策略不同，不可混用。'])]}
def generate(n, sections):
    width, margin = 1320, 65
    body = ImageFont.truetype(FONT, 27)
    heading = ImageFont.truetype(FONT, 32)
    title = ImageFont.truetype(FONT, 43)
    tmp = ImageDraw.Draw(Image.new('RGB',(1,1)))
    def wrap(s):
        out=[]; cur=''
        for ch in s:
            if tmp.textlength(cur+ch,font=body)>width-2*margin-40:
                out.append(cur);cur=ch
            else:cur+=ch
        if cur:out.append(cur)
        return out
    prepared=[(h,[line for text in lines for line in wrap(text)]) for h,lines in sections]
    height=235+sum(80+len(lines)*43+25 for _,lines in prepared)+105
    im=Image.new('RGB',(width,height),BG);d=ImageDraw.Draw(im)
    d.rectangle((0,0,width,165),fill=NAVY)
    d.text((margin,28),f'计算机系统结构 · 作业 {n}',font=title,fill='white')
    d.text((margin,102),'林润鑫  |  3124004588  |  软件工程4班',font=body,fill='white')
    d.text((margin,185),'电子排版答题摘要（非手写照片） · 教材第2版',font=body,fill=NAVY)
    y=240
    for h,lines in prepared:
        d.rounded_rectangle((margin-15,y-10,width-margin+15,y+55),radius=12,fill=TEAL)
        d.text((margin,y),h,font=heading,fill='white');y+=80
        for line in lines:d.text((margin+5,y),line,font=body,fill=INK);y+=43
        y+=25
    d.text((margin,y+15),'完整题目条件、推导、时空表和资料链接见对应作业 Markdown。',font=body,fill=NAVY)
    path=ROOT/'imgs'/f'{n}_answers.png';im.save(path,optimize=True)
    assert path.stat().st_size < 1_000_000, path
    print(path.name,im.size,path.stat().st_size)
if __name__=='__main__':
    for n,sections in DATA.items():generate(n,sections)
