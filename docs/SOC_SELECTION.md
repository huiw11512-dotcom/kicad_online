# SoC选型记录

## 候选比较

| SoC | CPU | 评价 |
|---|---|---|
| RK3566 | 4 × A55，最高1.8GHz | 低成本，但接口资源和频率低于RK3568 |
| **RK3568** | **4 × A55，最高2.0GHz** | HDMI2.0a、USB3、双GMAC、PCIe、LPDDR4X；资料和参考设计较完整 |
| RK3588S | 4 × A76 + 4 × A55 | 性能更强，但电源、DDR、散热和PCB复杂度明显增加 |

## A1选择：RK3568

- 订货器件：RK3568，FCBGA636L，19×19mm。LCSC目录候选编号C2938930；本次查询显示有现货记录，库存/价格随时变化，下单前复核。
- CPU：4 × Cortex-A55。
- GPU：Mali-G52。
- NPU：最高1 TOPS。
- DDR：32-bit，支持DDR3/DDR4/LPDDR3/LPDDR4/LPDDR4X；LPDDR4X最高3200Mbps。
- 存储：eMMC 5.1、SD 3.0。
- 显示：HDMI 2.0a。
- USB：1 × USB3 Host、1 × USB3 DRD、2 × USB2 Host。
- 网络：2 × GMAC 10/100/1000M。

## 资源复用约束

USB3 Host、USB3 DRD、PCIe2.1、SATA和SGMII/QSGMII共享Multi-PHY资源，不能将规格表中的接口数量全部同时使用。A1优先保留USB3 Host + USB3 DRD（固定Host）+ 两路USB2 Host；不启用外部PCIe/SATA扩展。

## 性能说明

RK3568的A55架构与Pi 4B的A72不同，CPU原始性能不能直接宣称持平。选择RK3568是为了获得功能完整、资料可用、复杂度可控的Linux SBC首版。
