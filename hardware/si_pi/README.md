# A1高速接口检查

只重点处理载板上的四类高速接口：

| 接口 | 目标差分阻抗 | 依据 |
|---|---:|---|
| USB 3.0 | 90 Ω | CM5 Datasheet |
| PCIe Gen2 x1 | 90 Ω | CM5 Datasheet |
| HDMI 2.0 | 100 Ω | CM5 Datasheet |
| Gigabit Ethernet | 100 Ω | CM5 Datasheet |

- USB3/PCIe/HDMI/Ethernet差分线下方保持连续参考地。
- 不跨地平面开槽或分割。
- 线宽线距按板厂实际4层/6层叠层计算，不照搬其他板子的尺寸。
- PCIe按Gen2 x1设计，检查CLK_nREQ、nRST和必要控制信号。
- M.2 3.3V电源与高速信号分开布局，避免电源开关噪声耦合。
- 不需要DDR SI/PI仿真，因为DDR已集成在CM5模块内。
