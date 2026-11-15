# KiCad工程目录

此目录只存放Linux MiniHost A1自主创建的KiCad工程。

当前尚未生成SoC符号、封装或原理图。必须先取得并审查RK3588完整PinOut、封装球位和原厂Hardware Design Guide。

工程创建顺序：
1. 建立受版本控制的项目级符号库和封装库。
2. 根据原厂PinOut建立RK3588符号，执行球位/Pad自动核对。
3. 完成PMIC、电源、DDR、eMMC和Boot最小系统。
4. 通过原理图审查后再创建PCB。
5. 不引用或复制CM5 MiniHost的原理图、PCB、封装或布局。

KiCad工程文件、库表、规则和版本均需提交到Git。锁文件、临时缓存和本地自动备份不纳入版本控制。