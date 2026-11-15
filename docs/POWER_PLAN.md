# A1电源架构 Rev 0.3 — 基于Rockchip RK3568 Hardware Design Guide V1.2

状态：电源树框架已收敛；具体PMIC输出映射、器件值及完整原理图仍未冻结。

## 1. 输入电源

- 暂定USB-C PD输入：9V/3A（27W），作为首版整机输入目标。
- 9V输入经同步Buck生成5V_SYS；5V_SYS为USB VBUS和各后级稳压器的输入母线。
- 9V PD适配器必须真实支持9V/3A PDO；未协商成功时禁止按满功率运行。
- USB-C接口需配置CC/PD控制、输入过压/浪涌保护、反灌保护和输入电流监测。
- 5V_SYS输出能力和外设端口预算必须统一核算，不能把每个USB口的最大电流与SoC峰值功耗简单叠加后忽略输入功率上限。
- 暂不冻结HUSB238的VSET/ISET电阻。必须按所采购版本数据手册的电阻曲线、PDO和板级限流策略计算，不能沿用未经核对的经验阻值。

## 2. RK3568核心电源设计硬约束

根据Rockchip RK3568 Hardware Design Guide V1.2：

| 电源轨 | 电压/动态要求 | 官方电源能力要求 | 设计约束 |
|---|---|---:|---|
| VDD_CPU | DVFS，约0.8–1.2V范围需结合软件配置 | ≥4A | 独立Buck，VDD_CPU_COM接Buck FB远端反馈 |
| VDD_GPU | DVFS | ≥2A | 独立Buck，除非使用Rockchip明确允许的合并方案 |
| VDD_NPU | DVFS | ≥2A | 独立Buck；若首版不使用NPU，需按Rockchip要求处理供电及DTS禁用 |
| VDD_LOGIC | 默认约0.92V，可预留DVFS | ≥2A（指南2.2.2.7） | 独立Buck |
| PMU_VDD_LOGIC_0V9 | 0.9V | 峰值50mA | 可与PMUPLL_AVDD_0V9合并，保留原厂去耦 |
| PMUPLL_AVDD_0V9 | 0.9V | 峰值10mA | 低噪声供电 |
| PMUPLL_AVDD_1V8 | 1.8V | 峰值9mA | 低噪声供电 |
| SYSPLL_AVDD_0V9 | 0.9V | 峰值30mA | 推荐低噪声LDO，PSRR@1kHz >65dB |
| SYSPLL_AVDD_1V8 | 1.8V | 峰值18mA | 推荐低噪声LDO，PSRR@1kHz >65dB |

注意：指南2.2.2.7给出VDD_LOGIC电源能力≥2A；后面的离散电源替代方案章节给出≥1.5A的替代选型描述。A1优先按≥2A的更严格要求设计，待Rockchip对应参考原理图确认。

## 3. VDD_CPU Buck

- 采用独立同步Buck，支持I2C或PWM动态调压，优先沿用Rockchip参考设计。
- 输出能力≥4A。
- 输出精度±1.5%。
- 负载从最大电流10%跃迁至80%，变化斜率1A/µs，纹波要求±3%以内。
- VDD_CPU总电容必须大于135µF。
- VDD_CPU_COM必须连接至Buck反馈端，按原厂参考电路布置Kelvin采样。
- TCS4525系列仅作为候选；必须核对具体后缀、输入范围、输出电压范围、I2C地址、动态响应、补偿及封装散热后才可冻结。
- 不允许仅凭“5A额定电流”判断其满足CPU电源要求。

## 4. GPU、NPU和LOGIC

- VDD_GPU峰值可达1.2A，Buck输出能力≥2A，精度±1.5%，瞬态和纹波按指南执行；总电容>90µF。
- VDD_NPU峰值可达1A，Buck输出能力≥2A，精度±1.5%；是否上电必须与Linux设备树和实际功能一致。
- VDD_LOGIC峰值可达1.2A，Buck输出能力≥2A，精度±1.5%；总电容>90µF。
- 不将RK809-5 BUCK3/BUCK4等1.5A通道直接指定为上述电源，除非官方完整电源树明确允许且负载/动态要求通过验证。

## 5. LPDDR4X电源

LPDDR4X模式下，RK3568有独立的VCC_DDR与VCC0V6_DDR供电网络，不能把SoC DDR PHY供电和DRAM供电按名称混为一谈。

- Micron颗粒的VDD1/VDD2/VDDQ按确切订货型号数据手册核对。
- RK3568 DDRPHY_VDDQ、DDRPHY_VDDQL按Rockchip LPDDR4X专用参考电路供电。
- Rockchip指南指出单颗LPDDR4X方案可评估1A等级DDR DC/DC；实际仍需按颗粒峰值电流、SoC PHY负载及纹波预算复核。
- LPDDR4X的1.8V电源在待机自刷新条件下需保持供电。
- RK3568 VCC_DDR/VCC0V6_DDR去耦电容数量和位置必须遵循原厂图2-51、PCB图3-34至图3-37，不得任意删减。
- DDR颗粒与模板/BIN尚未匹配，因此本节电压轨和器件值未冻结。

## 6. RK809-5角色与限制

Rockchip指南V1.2说明RK809-5：
- 输入范围2.7–5.5V。
- BUCK1/2：各最大2.5A。
- BUCK3/4：各最大1.5A。
- BUCK5：最大2.5A。
- LDO1/2、LDO4–LDO9：各最大400mA。
- LDO3：最大100mA。
- Switch1/2：各最大2.1A。
- 封装QFN68，7×7mm。

关键注意事项：
- RK809-5的上电时序已固化，不可修改，也不可与RK809-1/-2/-3的时序混用。
- VCC_RTC必须先于或同时于其他电源供电；建议与VCC9同源。
- VCC9上电后必须高于3.0V，否则PMIC会自动关机。
- VDC启动门限>0.55V，推荐约1.2V；EXT_EN拉高后，VCC9必须在1.5ms内达到3.0V。
- VCC_RTC需>3.0V。
- PWRON按键启动需拉低超过500ms。
- 32.768kHz晶体负载电容按晶体CL计算，指南推荐22pF，且不低于18pF。
- RESETB需保留100nF电容。
- SDA/SCL/INT/CLK32K/RESETB为开漏输出，需要合适上拉。
- 若不使用Fuel Gauge，BATDIV、SNSP、SNSN按指南接地处理。
- BUCK1/2输入电容>10µF，输出电容>30µF。
- BUCK3输入电容>10µF，输出电容>30µF；输出由外部分压设定，VBUCK3参考电压0.8V，阻值按目标DDR电压计算。
- BUCK4输入电容>10µF，输出电容>30µF。
- BUCK5输入电容>10µF，输出电容>33µF。
- 电感参考0.47µH，饱和电流>3.5A，DCR<50mΩ，优先<20mΩ。

## 7. RK809-5电源分配策略

当前只冻结芯片角色和硬约束，不在没有完整图2-62原厂电源树的情况下臆测BUCK/LDO到SoC电源轨的一一映射。

下一步需要对照RK3568 EVB原理图和RK809-5完整参考电路，形成如下逐项分配表：
- PMIC输出脚与输入供电脚
- 输出电压/默认值/动态范围
- 负载峰值与连续电流
- 目标SoC电源球位/外围负载
- 上电序号
- 电感/反馈/输入输出电容
- I2C地址和软件电源配置

## 8. IO与模拟电源域

- PMUIO0固定1.8V，PMUIO1固定3.3V；PMUIO2及VCCIO1、VCCIO3–VCCIO7需硬件供电与DTS配置一致。
- VCCIO2为Flash IO域，必须与FLASH_VOL_SEL状态匹配；1.8V时FLASH_VOL_SEL拉高，3.3V时拉低。
- USB3 PHY、MULTI_PHY和HDMI PHY模拟电源按Rockchip指南推荐的低噪声LDO、磁珠和去耦网络实现。
- 不使用的PHY电源可以按指南关闭，但对应DTS节点必须禁用，避免内核初始化卡住。

## 9. 原理图冻结条件

1. 获取并逐页核对RK3568 EVB原理图和RK809-5参考设计。
2. 完成全部SoC电源球位—网络名—电源芯片输出映射。
3. 完成各Buck负载/动态响应/电感/补偿/电容计算。
4. 完成LPDDR4X颗粒、DDR模板和BIN配对。
5. 完成IO Bank与DTS电压域一致性表。
6. 检查启动、关机、掉电和复位时序。
7. 完成电源原理图ERC及交叉检查后，才允许冻结SoC核心电源页。

## 参考资料

- Rockchip RK3568 Hardware Design Guide V1.2, Sections 2.2.2–2.2.3, Figures 2-43–2-63.
  https://dl.xkwy2018.com/downloads/RK3568/RK356X/Hardware/Rockchip_RK3568_Hardware_Design_Guide_V1.2_EN.pdf
- RK809 Datasheet Rev 2.5.
  https://www.boardcon.com/download/Rockchip_RK809_Datasheet_V2.5-20250407.pdf
