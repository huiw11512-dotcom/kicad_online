# Diagnostic: missing components in native netlist (2026-11-16)

Confirmed KiCad 9.0.9 execution from GitHub Actions run 43843532754: exported netlist has only 97 components and **no U3, U7, U8, U9, U10 or J201**; only root/late-added Ethernet, AP6256, GPIO devices populated. ERC reports 325 violations.

This change targets only two pages as a controlled test: removes obsolete inline (id N) tokens from symbol property nodes for **RK809_PMIC** and **HDMI_TX**. It DOES NOT assert a fix without a subsequent native netlist and ERC report; other sheets intentionally unchanged for comparison. Do not start PCB before original page devices appear in the exported netlist and ERC reviewed.

Check the next CI artifact for U3 and J201 and then investigate other original subpages, especially RK3568/DDR/eMMC.
