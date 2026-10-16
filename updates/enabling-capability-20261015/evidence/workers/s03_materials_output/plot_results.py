from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

B=Path(__file__).resolve().parent
runs=json.loads((B/'results_v2/ACQUISITION_RUNS.json').read_text())
raw=json.loads((B/'RAW_LOOP_AUDIT.json').read_text())
plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
fig,ax=plt.subplots(1,3,figsize=(15.6,4.6))
styles={'composition':('Composition EI','#3666aa','-'),
        'continuous_spectra':('Composition + continuous XRD EI','#218c65','-'),
        'partition':('Spectrum partition EI','#bd584b','--'),
        'equally_informed_union':('All-kernel EI selector','#8065a0',':'),
        'random':('Random','#888888','--')}
for j,(output,unit) in enumerate([('Coer','mT'),('Kerr','mrad')]):
    ymax=0
    for arm,(label,color,linestyle) in styles.items():
        values=np.array([r['regret'] for r in runs if r['output']==output and r['arm']==arm])
        ax[j].plot(np.arange(1,81),values.mean(0),label=label,color=color,ls=linestyle,lw=1.8)
        ymax=max(ymax,float(values.mean(0)[7:].max()))
    ax[j].set(xlabel='Magnetic observations',ylabel=f'Mean regret in stored output ({unit})',
              title=f'NIST Fe–Co–Ni: {output}',xlim=(8,80),ylim=(0,1.08*ymax))
    ax[j].grid(alpha=.15)
for geometry,label,color in [('out_of_membrane_plane','Out of membrane plane','#3666aa'),
                              ('in_membrane_plane','In membrane plane','#bd584b')]:
    rows=sorted([r for r in raw['loops'] if r['geometry']==geometry],key=lambda r:r['potential_V'])
    voltage=np.array([r['potential_V'] for r in rows]);hc=np.array([r['linear_interpolation_Hc_Oe'] for r in rows])
    low=np.array([r['crossing_bracket_Hc_interval_Oe'][0] for r in rows])
    high=np.array([r['crossing_bracket_Hc_interval_Oe'][1] for r in rows])
    ax[2].errorbar(voltage,hc,yerr=np.r_[(hc-low)[None,:],(high-hc)[None,:]],fmt='o',capsize=3,
                   color=color,label=label)
    if geometry=='out_of_membrane_plane':
        ax[2].scatter(voltage,[r['source_tabulated_Hc_Oe'] for r in rows],marker='x',color='black',label='Source parameter table',s=40)
ax[2].set(xlabel='Deposition potential (V)',ylabel='Coercivity from stored SQUID loop (Oe)',
          title='Fe–Co–Ni–Cu nanowires: actual loops')
ax[2].grid(alpha=.15);ax[2].legend(frameon=False,fontsize=8,loc='lower left')
ax[0].legend(frameon=False,fontsize=7,loc='upper right')
fig.text(.03,.025,'NIST: 12 seeds; all 921 XRD scans supplied upfront to spectrum arms. Their acquisition cost is excluded from this axis.',fontsize=8)
fig.text(.70,.025,'Bars: crossing brackets, not confidence intervals.',fontsize=8)
fig.subplots_adjust(bottom=.17,wspace=.28,top=.9)
fig.savefig(B/'MEASURED_OUTPUT_RESULTS_v2.png',dpi=160,bbox_inches='tight')
