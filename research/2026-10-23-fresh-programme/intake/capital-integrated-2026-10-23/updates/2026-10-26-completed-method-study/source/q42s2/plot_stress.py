from pathlib import Path
import csv
import numpy as np
import mpmath as mp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
mp.mp.dps = 100
with (ROOT/'underflow_stress.csv').open() as f:
    under = list(csv.DictReader(f))
with (ROOT/'ring_isolation_long_period.csv').open() as f:
    ring = list(csv.DictReader(f))
fig, axes = plt.subplots(1, 2, figsize=(10.8, 4.1), constrained_layout=True)
axes[0].plot([float(r['z']) for r in under],
             [float(mp.log10(mp.mpf(r['high_precision_reverse']))) for r in under],
             'o-', label='100-digit reverse coefficient')
axes[0].axhline(np.log10(np.nextafter(0., 1.)), color='tab:red', linestyle='--',
                label='Smallest positive Float64 value')
axes[0].set(xlabel='Contact exposure per phase z', ylabel='log10(reverse / G)',
            title='A computed zero can be a positive coefficient')
axes[0].legend(fontsize=8)
P = [float(r['period']) for r in ring]
axes[1].plot(P, [float(r['isolation']) for r in ring], 'o-', color='tab:blue')
axes[1].axhline(69.78366967578278, color='tab:blue', linestyle=':', linewidth=1)
axes[1].set(xscale='log', xlabel='Ring period, C = G = 1', ylabel='Forward / reverse',
            title='Long cycling raises isolation while reducing flux')
twin = axes[1].twinx()
twin.plot(P, [float(r['forward']) for r in ring], 's--', color='tab:orange')
twin.set(yscale='log', ylabel='Forward transfer / G')
axes[1].yaxis.label.set_color('tab:blue')
twin.yaxis.label.set_color('tab:orange')
for ax in axes:
    ax.grid(alpha=.25)
fig.savefig(ROOT/'stress_and_ring.svg')
fig.savefig(ROOT/'stress_and_ring.png', dpi=170)
