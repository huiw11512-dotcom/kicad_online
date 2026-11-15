# 架构决策记录

## ADR-001：采用RK3588作为A1主控

状态：选定为设计基线；在原理图冻结前完成供应、资料和软件支持复核。

理由：
- ARM64 Linux定位明确，不需要x86兼容。
- 原厂规格列出4核Cortex-A76 + 4核Cortex-A55、Mali-G610 MC4和6 TOPS NPU。
- 支持64-bit LPDDR4/LPDDR4X/LPDDR5、eMMC 5.1、PCIe 3.0 x4、双USB 3.1和双RGMII。
- FCBGA1088L封装，23 × 23 mm，0.65 mm pitch；属于高难度BGA与高速PCB项目，需要专业封装和板厂能力。

## ADR-002：首版采用LPDDR4X，目标8GB

状态：架构选定，颗粒未选定。

参考Rockchip EVB的8GB实现：两颗4GB LPDDR4X。该参考只用于核对容量组织和拓扑，最终颗粒必须满足原厂支持清单、速度等级、封装、温度等级和供货要求。禁止仅按容量选料。

## ADR-003：eMMC启动 + PCIe NVMe扩展

状态：选定为系统架构，具体器件待定。

- eMMC 5.1目标32GB，作为稳定启动介质。
- M.2 M-Key使用PCIe 3.0 x4连接NVMe。
- MicroSD可作为恢复或维护介质，是否保留由空间与Boot配置决定。

## ADR-004：电源管理以原厂EVB方案为起点

状态：待详细比较后冻结。

原厂EVB资料描述了双RK806-2和单RK806-1两种方案；官方EVB配置采用双RK806-2。A1先按双RK806-2方案做电源轨、时序和面积评估，再与单RK806-1方案比较成本和可实现性。不得在未核实原厂参考电路前自行拼接PMIC组合。

## ADR-005：12V DC输入

状态：选为输入电压基线，额定电流待预算。

原厂EVB使用12V/3A适配器和前级Buck。A1的NVMe、USB外设和散热负载不同，不能直接照抄3A额定值。输入电流、连接器、保险丝、TVS和前级Buck必须由最坏工况功耗预算确定。

## ADR-006：10层PCB作为首轮布线评估起点

状态：未冻结。

先用SoC BGA escape、LPDDR4X、PCIe和USB的布线可行性评估8/10层方案。最终层数、HDI结构、微孔和阻抗必须同时满足板厂能力、成本与信号完整性，不以层数作为性能保证。

## ADR-007：软件先采用可获得的Rockchip BSP

状态：选定策略，SDK版本待确认。

第一阶段以能够获得的Rockchip BSP、DDR初始化二进制、U-Boot、Kernel、设备树和Debian/Buildroot为基础完成启动。之后评估主线U-Boot/Linux的驱动与启动链差异。必须确认SDK获取权限和可重建性。