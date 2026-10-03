#
# sum_array.s —— 计算机系统结构 第四次作业
# 用 MIPS 汇编求整型数组之和，并打印结果。
# 运行环境：MARS 4.5 / SPIM（使用 MIPS32 系统调用约定）
#
# 对应 C 代码：
#   int sum = 0;
#   for (int i = 0; i < n; i++) sum += arr[i];
#

        .data
arr:    .word   3, 1, 4, 1, 5, 9, 2, 6      # 待求和的数组，共 8 个字
n:      .word   8                           # 元素个数
msg:    .asciiz "sum = "

        .text
        .globl  main

main:
        la      $t0, arr            # $t0 = 数组基地址 &arr[0]
        lw      $t1, n              # $t1 = n，循环上界
        li      $t2, 0              # $t2 = sum = 0
        li      $t3, 0              # $t3 = i = 0

loop:
        beq     $t3, $t1, done      # if (i == n) goto done
        sll     $t4, $t3, 2         # $t4 = i << 2，字地址偏移 = i * 4
        add     $t5, $t0, $t4       # $t5 = &arr[i]
        lw      $t6, 0($t5)         # $t6 = arr[i]
        add     $t2, $t2, $t6       # sum += arr[i]
        addi    $t3, $t3, 1         # i++
        j       loop                # 回到循环头

done:
        li      $v0, 4              # syscall 4：输出字符串
        la      $a0, msg
        syscall

        li      $v0, 1              # syscall 1：输出整数
        move    $a0, $t2
        syscall

        li      $v0, 10             # syscall 10：正常退出
        syscall
