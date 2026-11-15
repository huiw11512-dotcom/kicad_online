# 首板Bring-up计划

## 0. 首板调试准备

- 预留可接触的UART TX/RX/GND。
- 预留输入电源电流测量和关键电源轨测试点。
- 预留PMIC I2C、Reset、Power Good和Recovery/MASKROM控制点。
- 预留SoC JTAG或原厂要求的调试接口。
- 预留eMMC/USB下载恢复路径。
- BGA器件装配后安排X-Ray检查。

## 1. 不装SoC阶段

1. 检查PCB短路、开路、阻抗coupon和叠层。
2. 检查输入保护和前级Buck。
3. 逐路验证外围5V、3.3V和其他辅助电源。
4. 验证电源使能、限流和热状态。

## 2. 装SoC与PMIC阶段

1. 限流电源首次上电。
2. 逐项测量PMIC输入和输出。
3. 检查时序、PG、Reset和待机电流。
4. UART观察BootROM/Loader/DDR初始化输出。
5. 若DDR初始化失败，先核查电源、时钟、Reset、颗粒焊接和DDR配置，不盲目改设备树。

## 3. Linux启动阶段

1. 验证DDR容量和压力测试。
2. 验证eMMC读写、分区和系统启动。
3. 验证USB下载、Recovery和常规Host。
4. 验证HDMI热插拔与显示。
5. 验证Ethernet链路、吞吐和持续运行。
6. 验证PCIe枚举、NVMe读写和温升。
7. 验证可选Wi-Fi/BT与MicroSD。

## 4. 稳定性测试

- CPU/GPU/DDR联合压力测试。
- NVMe持续读写与掉电恢复。
- USB多设备并发。
- 网络持续传输。
- 冷启动、热启动、断电重启。
- 高低温和长时间运行。

所有测试必须记录板卡版本、BOM版本、固件版本、环境温度、仪器、测试步骤和原始日志。