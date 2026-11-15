# A1 DDR内存方案

状态：容量和接口宽度确定；颗粒料号未冻结。

## 目标
- LPDDR4X
- 4GB（32Gb）
- 32-bit总线
- 速率以Rockchip支持的颗粒、PCB模板和DDR BIN为准，不盲目追求最高频率。

## 组织候选
优先评估单颗32Gb x32 LPDDR4X；若没有可采购且获Rockchip支持的匹配料号，则采用原厂模板支持的两颗16Gb x16方案。

## Rockchip公开模板
RK3568 LPDDR4X模板配置表列出：
- RK3568_Template_LP4XD200P132SD4_43x28_1600MHz
- RK3568_Template_LP4XD200P232DD61346_43R0x28R0_1056MHz
- RK3568_Template_LP4XD320P164SD6H1_46X28_1600MHz
- RK3568_Template_LP4XeM254P132SS61346_48R6x33R0_2666Mbps

必须根据实际颗粒封装、位宽、Rank/Die组织和WDQS要求选模板，不能仅凭名称相似套用。

## 颗粒冻结条件
1. 获取Rockchip当前DDR Approved Vendor List。
2. 确认完整料号、容量、位宽、封装和温度等级。
3. 确认对应PCB模板和DDR初始化BIN。
4. 获取颗粒数据手册和ODT/阻抗/上电要求。
5. SoC球位、DQ Byte Lane、DQS、CA、CK、CS、RESET、ZQ逐项映射。
6. DDR区域遵循匹配模板，不复制其他厂商整块主板。

## 验证
匹配DDR BIN启动训练，保存串口日志，识别完整4GB，执行内存压力测试；需要WDQS的颗粒按对应工具执行眼图/频率扫描。
