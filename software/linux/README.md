# A1 Linux软件与启动

## 首版系统
优先使用Rockchip RK3568 Linux SDK完成首次Bring-up，硬件稳定后验证Debian/Ubuntu ARM64或Buildroot。

## 启动链
BootROM → DDR初始化BIN/SPL → U-Boot → Linux Kernel → Device Tree → RootFS。

## 首板顺序
1. 使用与LPDDR4X颗粒/模板匹配的DDR BIN。
2. 通过UART保存DDR训练和BootROM日志。
3. 先从MicroSD启动最小系统，验证CPU、RAM和基础外设。
4. 再烧录eMMC并配置默认启动。
5. 逐项启用HDMI、Ethernet、USB3/USB2、Wi-Fi/BT和GPIO。
6. 记录Kernel、U-Boot、DDR BIN和无线固件版本。

DDR BIN必须与颗粒、Rank/Die组织、速度和PCB模板匹配，不能拿其他RK3568板子的BIN直接作为最终配置。
