# Local check receipts

16 October 2026. Executed on this macOS host with `python3`; no GPU or external compute. Durations are measured for these actual executions and vary by machine/load.

## `/opt/homebrew/opt/python@3.14/bin/python3.14 check_execution_surface.py --L 4 --max-height 5 --random-traces 200 --random-length 100`

- Exit: 0
- Wall: 69.632 s
- Child user CPU: 67.982 s
- Child system CPU: 0.557 s
- Output:
```text
PASS L=4, exhaustive states=76, checked samples=20076
```

## `/opt/homebrew/opt/python@3.14/bin/python3.14 check_modulo_surface.py`

- Exit: 0
- Wall: 1.580 s
- Child user CPU: 1.547 s
- Child system CPU: 0.015 s
- Output:
```text
one-fault modulo PASS clean states 76 fault trials 8512
two-fault unique-repair trap (0, 1) repairable []
four-fault counterfeit gate PASS (0, 1, 4, 5)
```

## `/opt/homebrew/opt/python@3.14/bin/python3.14 check_color_program.py`

- Exit: 0
- Wall: 0.042 s
- Child user CPU: 0.035 s
- Child system CPU: 0.005 s
- Output:
```text
PASS 108 one-color-fault patterns; fourfold program majority
```

## `/opt/homebrew/opt/python@3.14/bin/python3.14 check_moat_repair.py`

- Exit: 0
- Wall: 1.001 s
- Child user CPU: 0.981 s
- Child system CPU: 0.013 s
- Output:
```text
PASS two-site trials 1000 recovered 1000 single-gate debts 2
```

## `/opt/homebrew/opt/python@3.14/bin/python3.14 check_interleavings.py`

- Exit: 0
- Wall: 9.464 s
- Child user CPU: 9.337 s
- Child system CPU: 0.069 s
- Output:
```text
PASS {'exact': 1976, 'bulk_exact': 24} accepted near-boundary G events 364
```
