# A1电源架构规划

状态：系统级草案，未进入器件定型。电源轨电压、电流、容差和时序必须从对应版本原厂硬件设计指南、PMIC数据手册和实际负载预算提取。

## 1. 输入架构

初始方案：
12V DC输入 → 反接/过压/浪涌保护 → 前级Buck → VCC5V0_SYS → PMIC及外围电源。

Rockchip RK3588 EVB User Guide描述了12V输入、前级Buck产生VCC5V0_SYS，再供给PMIC的方案。EVB默认适配器为12V/3A；A1不能直接照抄其电流额定值，需按NVMe、USB外设、风扇和SoC最坏负载重新预算。

## 2. PMIC方案比较

| 方案 | 依据 | 初步评价 |
|---|---|---|
| 双RK806-2 | Rockchip官方EVB发布资料及EVB系统框图 | 有成熟EVB实现，作为A1首轮参考 |
| 单RK806-1 | RK3588 EVB User Guide列出的可选方案 | 可能降低面积/成本，但需核对完整电源轨和电流能力 |

当前不冻结PMIC数量。必须对比：
- SoC每条Buck/LDO电源轨的负载与峰值电流
- DDR PHY与DRAM颗粒电源
- 各电源轨上电顺序、PG和Reset依赖
- PMIC I2C地址、控制配置、OTP/寄存器初始化
- 热耗散、效率、输入电流和器件可采购性

## 3. 外围独立电源

需要单独评估：
- USB VBUS 5V：每端口限流、短路保护和过流告警。
- M.2 3.3V：NVMe启动峰值、持续功耗、热和浪涌。
- Ethernet PHY：模拟/数字电源域、磁性器件隔离。
- Wi-Fi模块：峰值发射电流和电源噪声。
- Fan：12V/5V选择、PWM控制和测速。
- RTC：纽扣电池或低功耗后备电源。

## 4. 必须形成的计算表

每个电源轨至少记录：
- Rail Name / Nominal Voltage / Tolerance
- SoC ball或负载器件
- Typical Current / Peak Current
- PMIC输出通道和外围器件
- Power-up order / Power-good dependency
- Decoupling capacitance及封装分布
- 估算损耗、温升和效率

## 5. 禁止事项

- 未核实原厂时序前，不给PMIC随意配置上电顺序。
- 不根据参考板的12V/3A输入直接定型A1电源接口。
- 不将不同PMIC方案的外围电路混用。
- 不以“电压正确”替代瞬态、纹波、时序和热验证。