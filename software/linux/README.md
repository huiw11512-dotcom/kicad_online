# Linux软件与启动

目标：ARM64 Linux独立启动。

启动链需要覆盖：
BootROM → Rockchip DDR/Loader初始化 → U-Boot → Linux Kernel → Device Tree → Root Filesystem。

首轮优先使用能够合法取得、可复现构建的Rockchip BSP。官方Brief Datasheet列出Linux 5.10支持；具体SDK版本、补丁、U-Boot、Kernel和rootfs必须以实际取得的SDK Release Note为准。

待办：
- 确认Rockchip SDK申请与下载权限。
- 归档rkbin/DDR初始化文件的版本和来源。
- 确认U-Boot defconfig、Kernel defconfig和设备树基线。
- 建立eMMC分区、Recovery和升级方案。
- 编写本板Device Tree并记录每个外设的资源分配。
- 保留UART调试和USB下载/恢复路径。

不在未取得SDK和硬件资料前宣称Linux启动已验证。