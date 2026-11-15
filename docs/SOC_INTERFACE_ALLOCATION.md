# RK3588 SoC资源分配草案

状态：功能级资源规划，尚未映射到球位。所有端口名称和复用关系须以对应版本PinOut、Hardware Design Guide及EVB原理图复核。

## 1. 资源分配建议

| SoC资源 | A1拟分配功能 | 说明/约束 |
|---|---|---|
| LPDDR4X 64-bit | 8GB系统内存 | 参考EVB双颗4GB组织；精确DQ/DQS/CA/CK映射待原厂PinOut |
| eMMC 5.1 | 32GB启动存储 | 优先作为系统启动介质 |
| PCIe 3.0 x4 | M.2 M-Key NVMe | 主高速扩展；核对Lane、REFCLK、PERST#、CLKREQ#及连接器定义 |
| HDMI TX Combo 0 | HDMI输出 | 只先布一组；确认HDMI/eDP复用和PHY资源 |
| USB OTG0 3.1 | USB-C下载/维护口 | USB角色、CC控制、ESD和恢复模式按EVB方案核对 |
| USB OTG1 3.1 | USB 3.x主机扩展 | 端口数量与外部连接器类型待USB资源核对 |
| USB HOST0/1 2.0 | 两路USB 2.0主机 | 连接器、限流开关和ESD待选型 |
| GMAC0 RGMII | 1GbE PHY + RJ45 | 核对IO电压、RGMII时序、PHY参考时钟和驱动支持 |
| SDMMC | MicroSD | 作为恢复/维护介质，Boot策略待确定 |
| SDIO 3.0 | Wi-Fi模块候选 | 可选功能，确认模块、驱动和天线空间 |
| PCIe2.1/SATA3 Combo | Wi-Fi/其他扩展候选 | 与SATA/PCIe复用关系须核实，首版不预先占用 |
| UART | 调试串口 | 保留独立3.3V或1.8V电平适配方案，实际电压按Bank确认 |
| SPI/SFC | 可选SPI NOR | 是否装配取决于Boot/恢复方案 |
| I2C | PMIC及低速外设 | 总线分配、地址冲突和电压域待核对 |
| SARADC/GPIO | Power/Recovery/状态输入 | 按Boot模式要求保留指定ADC输入与按键电路 |

## 2. 高速接口优先级

P0：
1. LPDDR4X 64-bit
2. PCIe 3.0 x4 NVMe
3. HDMI输出
4. 至少一路USB 3.x
5. RGMII千兆以太网

P1：
1. 第二路USB 3.x
2. Wi-Fi/BT
3. MicroSD
4. 第二显示输出或DP Alt Mode

## 3. 资源冲突检查

在原理图冻结前，必须完成以下矩阵：
- PCIe3 x4是否完整保留给NVMe。
- PCIe2.1/SATA3各Combo PHY的可用数量和模式限制。
- USB3与DP Alt Mode的高速Lane共享关系。
- HDMI/eDP Combo PHY选择。
- RGMII与其他IO复用及Bank电压。
- SDMMC、SDIO与Boot ROM启动配置。
- SARADC_IN0/IN1与MASKROM/Loader进入条件。
- UART Debug与Boot ROM/U-Boot调试引脚。

不得根据芯片宣传框图直接推断所有接口可同时工作。