# 参考资料登记

以下资料用于设计输入。原厂文件的公开镜像仅用于检索和工程研究；正式冻结前必须向Rockchip/授权代理确认适用版本。引用原厂参考设计不代表复制第三方PCB。

| 编号 | 资料 | 版本/日期 | 用途 | 状态 |
|---|---|---|---|---|
| REF-001 | RK3588 Brief Datasheet | Rockchip官网，V1.0，2025-08-28 | SoC功能、接口、封装信息 | 已登记 |
| REF-002 | RK3588 Hardware Design Guide | CN/EN V1.3，2023-02-13 | 原理图、电源、DDR、时钟、PCB、热设计与ESD/EMI | 待取得原始文件并逐页审查 |
| REF-003 | RK3588 PinOut | V1.1，2022-09-22 | 建立完整SoC符号、球位与IO复用表 | 待取得并解析 |
| REF-004 | RK3588 Package Pin Length | V1.0，2021-12-28 | BGA逃线与封装引脚长度分析 | 待取得并解析 |
| REF-005 | RK3588 Methods for Processing Unused Pins | V1.1，2022-09-15 | NC/未用球处理 | 待取得并审查 |
| REF-006 | RK3588 Power Consumption Test Report | V1.1，2022-08-29 | 功耗估算和电源容量设计输入 | 待取得并分析 |
| REF-007 | Rockchip Solutions DDR SDRAM Support List | Ver3.00，2025-08-08（公开镜像） | LPDDR4X颗粒兼容性筛选、状态与应用备注 | 已检索，需向FAE确认原始版本 |
| REF-008 | eMMC Support List | Ver1.72，2023-01-29 | eMMC兼容性筛选 | 待取得并核对更新版本 |
| REF-009 | RK806 Datasheet | V1.2，2022-10-08 | PMIC引脚、寄存器和电气参数 | 待取得 |
| REF-010 | RK860 Datasheet | V1.5，2022-11-01 | 辅助电源方案评估 | 待取得 |
| REF-011 | RK3588 EVB User Guide | V1.1，2022-11-29 | EVB系统、电源、DDR/eMMC、Boot和调试参考 | 待取得并审查 |
| REF-012 | RK3588 Schematic and PCB Review Checklist | V1.0 | 原理图与PCB审查清单 | 待取得 |
| REF-013 | RK3588 Production Process Requirements | V1.0，2023-02-15 | BGA装配、生产与工艺要求 | 待取得 |
| REF-014 | RK3588 HW Test Report Summary | V1.3，2023-02-15 | 原厂硬件测试项目参考 | 待取得 |
| REF-015 | Rockchip Linux SDK Release Notes | 版本需确认 | BSP、Kernel、U-Boot、rootfs和下载工具 | 待向原厂/代理确认 |

## 已核实的公开入口

1. Rockchip RK3588 Brief Datasheet（官方）：https://www.rock-chips.com/uploads/pdf/2022.8.26/191/Rockchip%20RK3588%20Brief%20Datasheet%20V1.0_20250828.pdf
2. Rockchip官方产品/下载入口：https://www.rock-chips.com/a/en/download/index.html
3. Rockchip RK3588 EVB发布介绍（官方）：https://www.rock-chips.com/a/cn/news/rockchip/2022/0310/1545.html
4. Rockchip硬件资料公开镜像仓库（含RK3588 V1.3指南、PinOut V1.1、DDR支持清单、PMIC资料和EVB指南）：https://github.com/mfkiwl/RK3588-custom
5. RK3588 Hardware Design Guide V1.0公开镜像：https://github.com/DeciHD/rockchip_docs
6. RK3588 EVB User Guide V1.0公开副本：https://dl.xkwy2018.com/downloads/RK3588/01_Official%20Release/01_Common%20Document/Rockchip_RK3588_EVB_User_Guide_V10_EN_0126.pdf
7. Rockchip SDK配置说明（板卡厂商文档）：https://wiki.t-firefly.com/zh_CN/ROC-RK3588-PC/linux_sdk.html
8. U-Boot Rockchip板级支持文档：https://docs.u-boot.org/en/stable/board/rockchip/rockchip.html

## 资料使用规则

- 当前公开检索到的较新通用设计资料为RK3588 Hardware Design Guide V1.3（2023-02-13）和PinOut V1.1（2022-09-22）；仍须向Rockchip FAE确认是否存在更新版本或勘误。
- 关键电源、DDR、Boot和NC规则必须回到对应版本原厂指南逐条核对。
- 公开镜像中的资料保留原作者和版权信息，不把第三方PCB、原理图或布局作为本项目设计成果。
- 没有取得完整PinOut、封装尺寸、DDR支持清单和原厂硬件指南前，不生成最终SoC符号、不开始DDR走线。
