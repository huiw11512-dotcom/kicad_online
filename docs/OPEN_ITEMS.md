# 未决事项与风险清单

| ID | 项目 | 风险/需要确认的内容 | 关闭条件 |
|---|---|---|---|
| OI-001 | RK3588供货 | 具体订货型号、渠道、批次、价格和生命周期 | 获得可追溯报价和样品 |
| OI-002 | 原厂资料 | 完整Datasheet、PinOut、Package Pin Length、Hardware Guide | 版本确认并归档 |
| OI-003 | SDK | Rockchip BSP获取权限、版本、许可证及DDR初始化文件 | 获取并完成一次可复现构建 |
| OI-004 | LPDDR4X | 8GB颗粒方案、制造商料号、颗粒组织、速度和兼容性 | 与原厂支持清单及EVB拓扑核对 |
| OI-005 | PMIC | 双RK806-2与单RK806-1成本/电源轨/时序比较 | 电源树评审通过 |
| OI-006 | eMMC | 32GB候选料号、HS400、温度和供货 | 兼容性和供货核验 |
| OI-007 | PCIe | PCIe3 x4 lane映射、参考时钟、PERST#、CLKREQ#、M.2定义 | Pinmux与原理图审查 |
| OI-008 | USB | USB3 PHY、USB2端口、Type-C角色与DP复用 | 完成接口资源矩阵 |
| OI-009 | HDMI | HDMI输出通道、DDC、HPD、CEC、ESD和连接器 | 完成原理图评审 |
| OI-010 | Ethernet | GMAC电压域、RGMII时序、PHY和磁性器件 | PHY方案及参考时钟确认 |
| OI-011 | Wi-Fi/BT | 模块接口、驱动、天线净空和认证 | 决定首版是否装配 |
| OI-012 | 电源预算 | SoC峰值、DDR、NVMe、USB负载和风扇 | 最坏工况预算与热设计完成 |
| OI-013 | PCB工艺 | 8/10层、HDI、线宽线距、微孔、阻抗 | 板厂DFM确认 |
| OI-014 | 机械 | 120×90mm外形、接口位置、散热器高度、安装孔 | 3D接口与外壳评审 |
| OI-015 | 生产测试 | BGA焊接、X-Ray、上电限流、UART测试点 | 生产测试计划批准 |

## 阻断项

OI-002、OI-003、OI-004、OI-005、OI-007和OI-012未关闭前，不允许发布原理图冻结版本。