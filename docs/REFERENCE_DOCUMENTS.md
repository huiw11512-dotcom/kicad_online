# 参考资料登记

以下资料用于设计输入。引用原厂参考设计不代表复制第三方PCB。正式设计时需记录实际使用的文档版本、页码、器件版本和变更。

| 编号 | 资料 | 来源/版本 | 用途 | 状态 |
|---|---|---|---|---|
| REF-001 | RK3588 Brief Datasheet | Rockchip官网，V1.0，2025-08-28 | SoC功能、接口、封装信息 | 已登记 |
| REF-002 | RK3588 Hardware Design Guide | V1.0，公开镜像副本 | 电源、DDR、时钟、PCB设计约束 | 待下载并逐页审查 |
| REF-003 | RK3588 PinOut | V1.0，2021-12-28，公开资料索引 | 生成完整SoC符号和球位表 | 待取得原始表格并审查 |
| REF-004 | RK3588 Package Pin Length | V1.0，2021-12-28，公开资料索引 | BGA逃线及长度分析 | 待取得 |
| REF-005 | RK3588 Methods for Processing Unused Pins | V1.0，2021-12-28 | NC/未用球处理 | 待取得 |
| REF-006 | RK3588 Power Consumption Test Report | V1.0，2021-12-30 | 功耗估算输入 | 待取得 |
| REF-007 | RK3588 EVB User Guide | V1.0，2022-01-25 | EVB系统、电源、DDR/eMMC和调试参考 | 已登记，需与新版本核对 |
| REF-008 | RK806 Datasheet | V1.0，2021-10-20 | PMIC引脚和配置 | 待取得 |
| REF-009 | RK860 Datasheet | V1.2，2021-10-11 | 辅助电源方案评估 | 待取得 |
| REF-010 | eMMC Support List | V1.63，2022-01-12 | eMMC兼容性参考 | 待取得并核对更新版本 |
| REF-011 | Rockchip Linux SDK Release Notes | 版本需确认 | BSP、Kernel、U-Boot、rootfs | 待向原厂/代理确认 |

## 可访问链接

1. Rockchip RK3588 Brief Datasheet（官方）：https://www.rock-chips.com/uploads/pdf/2022.8.26/191/Rockchip%20RK3588%20Brief%20Datasheet%20V1.0_20250828.pdf
2. Rockchip RK3588官方产品/下载入口：https://www.rock-chips.com/a/en/download/index.html
3. Rockchip RK3588 EVB发布介绍（官方）：https://www.rock-chips.com/a/cn/news/rockchip/2022/0310/1545.html
4. RK3588 Hardware Design Guide V1.0公开镜像：https://github.com/DeciHD/rockchip_docs
5. RK3588 EVB User Guide公开副本：https://dl.xkwy2018.com/downloads/RK3588/01_Official%20Release/01_Common%20Document/Rockchip_RK3588_EVB_User_Guide_V10_EN_0126.pdf
6. Rockchip SDK配置说明（板卡厂商文档）：https://wiki.t-firefly.com/zh_CN/ROC-RK3588-PC/linux_sdk.html
7. U-Boot Rockchip板级支持文档：https://docs.u-boot.org/en/stable/board/rockchip/rockchip.html

## 资料使用规则

- 优先使用Rockchip当前正式发布的原始文件。
- 公开镜像只用于资料检索，不能默认其版本为最新。
- 关键电源、DDR、Boot和NC规则必须回到对应版本原厂指南逐条核对。
- 没有取得完整Pinout、封装尺寸和原厂硬件指南前，不生成最终SoC符号、不开始DDR走线。