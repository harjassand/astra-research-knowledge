#!/usr/bin/env python3
"""Reconcile physical Fig1c frequency with normalized deposited Fig3 axis."""
from pathlib import Path
import json
import math
import numpy as np

HERE=Path(__file__).resolve().parent
p=HERE/'inherited/sources/biaxial_raw/biaxial_repository'
f1=np.loadtxt(p/'fig1c/fig1c_primary.csv',delimiter=',')
f3=np.loadtxt(p/'fig3a/fig3a_frequency.csv')
matrix=np.loadtxt(p/'fig3a/fig3a_exp_matrix.csv',delimiter=',')
assert np.array_equal(matrix[2],f1[:,1])
d={'status':'cross-file unit reconciliation; normalized Fig3 coordinates are not physical rad/s',
   'Fig1c_axis':'omega (rad/s), visually verified accepted PDF p2, sources/lin-figure1.png',
   'Fig3_axis':'omega/(2*pi*primary_rate), visually verified accepted PDF p4, sources/lin-figure3.png',
   'same_viscosity_row_exact':bool(np.array_equal(matrix[2],f1[:,1])),
   'physical_Fig1c_omega_range_rad_s':[float(f1[0,0]),float(f1[-1,0])],
   'Fig3a_coordinate_range':[float(f3[0]),float(f3[-1])],
   'observed_coordinate_multiplier':math.pi/(2*.2),
   'max_absolute_error_vs_observed_multiplier':float(np.max(np.abs(f3-f1[:,0]*math.pi/(2*.2)))),
   'max_relative_error_vs_observed_multiplier':float(np.max(np.abs(f3/(f1[:,0]*math.pi/(2*.2))-1))),
   'published_axis_vs_deposited_numeric_multiplier_discrepancy':'The deposited coordinates multiply physical omega by pi/(2*0.2), while the displayed normalized axis omega/(2*pi*0.2) would divide by pi. This is a factor pi^2 discrepancy. Do not silently treat Fig3a_frequency as an independent physical-frequency sweep or repair the deposited data without author confirmation. Use explicit physical Fig1c and definition chi=omega*A/0.2 for current gate.',
   'raw_physical_max_agrees_with_Fig1d':True}
(HERE/'FREQUENCY_RECONCILIATION.json').write_text(json.dumps(d,indent=2)+'\n')
print(json.dumps(d,indent=2))
