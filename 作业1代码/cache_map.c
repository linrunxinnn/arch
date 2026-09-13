/*
 * 直接映射 Cache 组号计算（作业 1 自拟示例）
 * 假设：Cache 容量 32KB，块大小 64B，直接映射
 */
#include <stdio.h>
#include <stdint.h>

int main(void) {
    const unsigned cache_bytes = 32 * 1024;
    const unsigned block_bytes = 64;
    const unsigned num_sets = cache_bytes / block_bytes; /* 512 组 */
    const unsigned offset_bits = 6;                      /* 2^6 = 64 */
    const unsigned index_bits = 9;                       /* 2^9 = 512 */

    uint32_t addrs[] = {0x00001234u, 0x00008234u, 0x0010F000u};
    int n = (int)(sizeof(addrs) / sizeof(addrs[0]));

    printf("sets=%u  offset_bits=%u  index_bits=%u\n", num_sets, offset_bits, index_bits);
    for (int i = 0; i < n; i++) {
        uint32_t addr = addrs[i];
        unsigned offset = addr & ((1u << offset_bits) - 1u);
        unsigned index = (addr >> offset_bits) & ((1u << index_bits) - 1u);
        unsigned tag = addr >> (offset_bits + index_bits);
        printf("addr=0x%08X  tag=0x%X  index=%u  offset=%u\n", addr, tag, index, offset);
    }
    return 0;
}
