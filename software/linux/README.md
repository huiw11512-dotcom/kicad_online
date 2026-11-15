# Linux软件与启动

A1使用CM5模块，不重新开发SoC启动链和DDR初始化。

首轮软件：
- Raspberry Pi OS 64-bit
- Debian ARM64（按官方支持情况）
- eMMC作为系统启动盘
- NVMe作为数据盘/可选系统盘

工作内容：
1. 使用官方工具将系统镜像写入CM5 eMMC。
2. 首次启动验证UART、HDMI和Ethernet。
3. 配置USB、NVMe、Wi-Fi/BT和风扇。
4. 记录Bootloader EEPROM和固件版本。
5. 验证nRPIBOOT下载/恢复接口。
6. 建立系统镜像备份与恢复流程。

不需要Rockchip BSP、RKbin、DDR初始化bin或RK3588设备树。
