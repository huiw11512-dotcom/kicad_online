# M.2 socket symbol variant audit

Before (ERC, hard PCB DRC, footprint parity, unconnected): (0, 4, 5, None)

After: (0, 4, 1, None)

Only the four nonexistent mechanical pad pins M1–M4 were removed from the cached CM5IO:Bus_M.2_Socket_M schematic symbol and its J701 instance. No PCB copper, SSD grounds, shield pins S1/S2, or separate mounting holes M701/M702 were changed.
The decorative REF** logo remains a deliberate PCB-only footprint and may still be flagged by schematic parity.
