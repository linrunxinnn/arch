#!/usr/bin/env python3
"""复核本次作业的数值、非线性调度及延迟槽程序语义。仅使用标准库。"""
from collections import deque
from fractions import Fraction
from pathlib import Path
import math
import re

def close(actual, expected):
    assert math.isclose(actual, expected, rel_tol=1e-7), (actual, expected)

# 第一章加权、单位与 Amdahl 计算。
counts, cpis = [45000,75000,8000,1500], [1,2,4,2]
cycles=sum(n*c for n,c in zip(counts,cpis))
assert cycles==230000 and sum(counts)==129500
close(cycles/400e6,575e-6)
close(1/(.6+.4/20),1/.62)
close(2.975/1.775,1.6760563380281692)

# 同时检查缓存 AMAT 和整机执行时间，防止把两者的胜负混同。
assert 2+.014*80 > 2.2+.01*80
assert 2*2+1.2*.014*80 < 2*2.2+1.2*.01*80
for miss, expected in zip([.029,.022,.020],[4.0056,3.4008,3.228]):
    close(1.5+1.2*miss*(48+.5*48),expected)

# 从预约表推导禁止间隔，并穷举全部可达冲突状态。
reservation=[{1,9},{2,3},{4,7,8},{4,5},{6,7}]
forbidden={b-a for row in reservation for a in row for b in row if b>a}
assert forbidden=={1,3,4,8}
c0=sum(1<<(i-1) for i in forbidden)
q=deque([c0]); graph={}
while q:
    state=q.popleft(); graph[state]=[]
    for interval in range(1,10):
        if interval<=8 and state>>(interval-1)&1: continue
        nxt=(state>>interval)|c0
        graph[state].append((interval,nxt))
        if nxt not in graph and nxt not in q:q.append(nxt)
assert set(graph)=={0b10001101,0b10101111,0b10001111}
means=[]
def visit(start,state,seen,weights):
    for weight,nxt in graph[state]:
        if nxt==start:means.append(Fraction(sum(weights)+weight,len(weights)+1))
        elif nxt not in seen:visit(start,nxt,seen|{nxt},weights+[weight])
for state in graph:visit(state,state,{state},[])
assert min(means)==Fraction(7,2)
# 直接叠加六个任务，逐段逐拍检查没有预约冲突。
starts=[0,2,7,9,14,16]
for row in reservation:
    occupied=[start+slot for start in starts for slot in row]
    assert len(occupied)==len(set(occupied))
assert starts[-1]+9==25

# 对原程序和延迟槽重排程序进行简化指令解释执行，与独立预期比较。
original=[('LW',),('INC_R1',),('SW',0),('INC_R2',),('SUB',),('BR',)]
reordered=[('LW',),('INC_R2',),('SUB',),('INC_R1',),('BR',),('SW',-4)]
def execute(program,delay):
    mem={4*i:10*i-400 for i in range(99)}
    regs={'R1':0,'R2':0,'R3':396,'R4':0}
    pc=0;pending=None;branches=0;steps=0
    while 0<=pc<len(program):
        ins=program[pc];op=ins[0];target=pending;pending=None;steps+=1
        if op=='LW':regs['R1']=mem[regs['R2']]
        elif op=='INC_R1':regs['R1']+=1
        elif op=='INC_R2':regs['R2']+=4
        elif op=='SUB':regs['R4']=regs['R3']-regs['R2']
        elif op=='SW':mem[regs['R2']+ins[1]]=regs['R1']
        elif op=='BR':
            branches+=1
            if delay:pending=0 if regs['R4'] else len(program)
            elif regs['R4']:pc=0;continue
        pc=target if target is not None else pc+1
        assert steps<1000
    assert branches==99 and steps==594
    assert regs['R2']==396 and regs['R4']==0
    assert mem=={4*i:10*i-399 for i in range(99)}
    return mem,regs
assert execute(original,False)==execute(reordered,True)

# 交付文件引用、代码围栏与图片尺寸上限。
root=Path(__file__).resolve().parent.parent
for name in ['README.md']+[f'作业{i}.md' for i in range(4,9)]:
    p=root/name;body=p.read_text()
    assert body.count('```')%2==0,name
    for url in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)',body):
        if '://' not in url and not url.startswith('#'):assert (p.parent/url).exists(),(name,url)
for i in range(4,9):assert (root/'imgs'/f'{i}_answers.png').stat().st_size<1_000_000
print('PASS: arithmetic, reachable scheduling states, minimum cycle mean, reservations, MIPS delay-slot semantics, links and image sizes')
