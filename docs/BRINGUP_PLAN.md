# A1首板Bring-up顺序

1. 首板目检、BGA焊接检查和阻值检查。
2. 不插存储器时检查输入和待机电源。
3. 限流上电，检查RK809-5各路输出及VDD_CPU。
4. 检查RESETn、24MHz主时钟和32.768kHz RTC时钟。
5. 连接3.3V TTL UART，记录完整启动日志。
6. 烧录匹配的DDR BIN和U-Boot，先验证DDR训练。
7. 验证4GB LPDDR4X全容量和内存稳定性。
8. 烧录eMMC系统，启动Debian/Buildroot。
9. 逐项验证HDMI、Ethernet、USB、Wi-Fi/BT、MicroSD和GPIO。
10. CPU/DDR/网络/USB联合负载，检查电源压降、温升和长期稳定性。

DDR训练失败时，先核对颗粒型号、模板、DDR BIN、DQ Lane映射和电源质量，不以盲目修改时序掩盖硬件问题。
