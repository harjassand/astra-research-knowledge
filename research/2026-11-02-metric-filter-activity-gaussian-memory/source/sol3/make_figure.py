#!/usr/bin/env python3
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
P=Path(__file__).resolve().parent
x=json.loads((P/'results/activity_source_checks.json').read_text());r=x['rapid_scaling'];q=x['refinement_at_rapid_scale_1e6']
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False})
f,axs=plt.subplots(1,3,figsize=(13.6,3.8),layout='constrained')
rho=[v['rapid_scale'] for v in r]
a=axs[0];a.semilogx(rho,[v['actual_outer_envelope_mass'] for v in r],'o-',color='#167a75',label='Computed envelope mass')
a.axhline(20,ls='--',color='#167a75',alpha=.5,label='Proved bound 5KM = 20')
a.semilogx(rho,[v['complete_source_normalizer'] for v in r],'s-',color='#2467a8',label='Complete source normalizer')
a.set(xlabel='Relaxation multiplier',ylabel='Dimensionless source parameter',title='Coupling grows as square root of rate',ylim=(0,24));a.legend(fontsize=8,loc='lower right')
a=axs[1];a.loglog(rho,[v['old_stage2_max_duration'] for v in r],'o-',color='#9b4167',label='Old sufficient Dyson window')
a.loglog(rho,[v['new_max_duration'] for v in r],'s-',color='#167a75',label='New sufficient activity window')
a.set(xlabel='Relaxation multiplier',ylabel='Sufficient maximum duration',title='Large constants remain visible');a.legend(fontsize=8,loc='upper right')
a=axs[2];n=[v['resolution'] for v in q]
a.loglog(n,[v['source_Gram_error'] for v in q],'o-',color='#2467a8',label='Complete source Gram error')
a.loglog(n,[v['weighted_cross_source_Duhamel_error'] for v in q],'s-',color='#167a75',label='Physical jump convolution error')
a.set(xlabel='CPU quadrature resolution',ylabel='Finite operator error',title='Refinement at multiplier 1,000,000');a.legend(fontsize=8,loc='upper right')
a.set_xticks(n,labels=[str(v) for v in n]);a.minorticks_off()
f.suptitle('Bounded metric filtering and the weighted physical loss clock',fontsize=14)
f.savefig(P/'results/activity_construction.png',dpi=180);f.savefig(P/'results/activity_construction.pdf')
print('Saved source-parameter figure; no gate/runtime comparison is implied.')
