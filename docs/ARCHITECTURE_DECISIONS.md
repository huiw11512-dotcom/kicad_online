# 架构决策记录

## ADR-001：SoC采用RK3568
首选RK3568 FCBGA636L。相较RK3566接口资源更充足；相较RK3588S复杂度和成本更可控。CPU原始性能不等同Pi 4B的Cortex-A72，定位为Pi 4B整机功能级别。

## ADR-002：4GB LPDDR4X
采用32-bit总线，优先评估单颗32Gb x32；若无合适且获Rockchip支持的料号，则改为原厂模板支持的双颗x16方案。颗粒与模板未匹配前不得冻结DQ/CA/CK连接。

## ADR-003：RK809-5 PMIC
按RK3568 Hardware Design Guide中的RK3568 + RK809-5电源树实现。VDD_CPU采用独立高电流Buck，参考TCS4525方案。RK809-5上电时序不可随意改变。

## ADR-004：eMMC + MicroSD
32GB eMMC为默认系统盘，MicroSD用于扩展和恢复；首版不布置NVMe/M.2和SATA。

## ADR-005：两路USB3不加Hub
利用一个USB3 Host和一个USB3 DRD控制器实现两路USB3；DRD固定Host模式。另使用两个USB2 Host。最终按Multi-PHY资源和PinMux核对。

## ADR-006：RTL8211F-CG千兆PHY
RK3568 GMAC RGMII连接RTL8211F-CG，再接带隔离变压器的RJ45。PHY复位、MDIO上拉、RSET和变压器中心抽头按其参考设计。

## ADR-007：AP6275系列无线模块候选
Wi-Fi走SDIO，Bluetooth走UART。完整模块料号、天线数量、供电和固件版本待供应商资料核验。

## ADR-008：六层板
Rockchip RK3568硬件设计指南推荐六层PCB。A1采用六层1.6mm FR-4起步，按板厂阻抗计算调整线宽线距。
