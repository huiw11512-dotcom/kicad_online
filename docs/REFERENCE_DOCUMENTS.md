# 参考资料登记

本项目使用官方CM5模块和官方接口资料。第三方载板只可用于观察常见实现方式，不复制其原理图、PCB或布局布线。

| 编号 | 资料 | 来源 | 用途 |
|---|---|---|---|
| REF-001 | Compute Module 5 Datasheet | Raspberry Pi官方，Release 2，2025-09-02 | 200-pin Pinout、电源、USB、PCIe、HDMI、Ethernet、机械尺寸 |
| REF-002 | Compute Module 5 Product Brief | Raspberry Pi官方 | 模块规格和订货配置 |
| REF-003 | Compute Module 5 IO Board Datasheet | Raspberry Pi官方 | 官方载板接口参考 |
| REF-004 | CM5 Design Files | Raspberry Pi官方 | 官方模块机械模型、接口核对 |
| REF-005 | CM5 Forward Guidance | Raspberry Pi官方 | 连接器替代型号和设计变更 |
| REF-006 | Raspberry Pi OS Documentation | Raspberry Pi官方 | 系统烧录、启动和更新 |

## 官方链接

1. CM5 Datasheet：https://pip.raspberrypi.com/categories/944-raspberry-pi-compute-module-5/documents/RP-008180-DS/cm5-datasheet.pdf
2. CM5 Product Brief：https://pip-assets.raspberrypi.com/categories/944-raspberry-pi-compute-module-5/documents/RP-008181-DS-12-cm5-product-brief.pdf
3. CM5IO Datasheet：https://pip-assets.raspberrypi.com/categories/1097-raspberry-pi-compute-module-5-io-board/documents/RP-008182-DS-3-cm5io-datasheet.pdf
4. CM5官方设计与资料入口：https://www.raspberrypi.com/documentation/computers/compute-module.html
5. CM5 Forward Guidance：https://pip-assets.raspberrypi.com/categories/945-forward-guidance/documents/RP-005110-WP/CM5-Forward-Guidance.pdf

## 重要核对项

- CM5模块使用两个100-pin高密度连接器，Pin 1–100与101–200分别属于两个连接器。
- CM5数据手册列出Amphenol 10164227-1001A1RLF（1.5mm堆叠高度）和10164227-1004A1RLF（4.0mm堆叠高度）两种配套连接器。
- 5V电源应维持在4.75V以上；USB-C CC1/CC2按CM5手册连接以支持5V/5A协商。
- PCIe为Gen2 x1；Gen3虽有部分情况下可能工作，但官方不支持，不作为设计目标。
- USB3差分阻抗90Ω；PCIe差分阻抗90Ω；HDMI与Ethernet差分阻抗100Ω。线宽线距按实际板厂叠层计算。
- CM5无线天线需保留净空；金属外壳可能降低板载天线性能，应按外壳结构决定是否使用外置天线。
