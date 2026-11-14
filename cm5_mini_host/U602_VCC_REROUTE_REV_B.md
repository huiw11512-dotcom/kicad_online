# U602 VCC copper reroute

U602 pad 5 was moved from +5V to +3V3_PI. The original local +5V via at (128.600,61.425) mm and its two short F.Cu stubs were removed. A 0.45/0.30 mm through-via at (128.450,60.850) mm connects the U602 pad to In2.Cu. Three 0.15 mm In2.Cu segments route around the local SCL/SDA/GND via cluster to the existing +3V3_PI through-via at (126.950,63.300) mm. The independent +5V via at (128.600,62.000) mm is explicitly preserved on +5V. All copper zones are refilled before save; native DRC verifies clearances and connectivity.
