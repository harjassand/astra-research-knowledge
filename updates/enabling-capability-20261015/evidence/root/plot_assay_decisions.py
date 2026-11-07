from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
P=Path(__file__).resolve().parents[1]
d=json.loads((P/'workers/chemistry_search/MEASURED_YIELDS.json').read_text())
r=[dict(zip(d['columns'],v)) for v in d['rows']]
x=np.array([v['target_yield_pct'] for v in r]);y=np.array([v['side_yield_pct'] for v in r])
v=(x>=0)&(y>=0)&(x+y<=100)
a=v&(x+y>=50);bad=a&(x<50);good=v&(x>=50)&(y<=x/19)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False})
fig,ax=plt.subplots(figsize=(8.8,6.1),dpi=170)
ax.scatter(x[v],y[v],s=8,c='#adb5bd',alpha=.26,rasterized=True,label='All admissible reported pairs (50,518)')
ax.scatter(x[bad],y[bad],s=15,c='#c75b28',alpha=.7,label='Combined yield ≥50%, desired yield <50% (199)')
ax.scatter(x[good],y[good],s=21,c='#216e9a',alpha=.8,label='Desired ≥50%, reported desired fraction ≥95% (65)')
xx=np.linspace(0,100,400)
ax.plot(xx,50-xx,ls='--',color='#9c6e56',lw=1)
ax.plot(xx,xx/19,ls=':',color='#216e9a',lw=1)
ax.axvline(50,color='#888888',ls=':',lw=1)
ax.set(xlim=(-1,102),ylim=(-1,102),xlabel='Desired regioisomer: reported assay yield (%)',ylabel='Other reported regioisomer: assay yield (%)')
ax.set_title('Combined assay yield can select the wrong chemical outcome',loc='left',fontsize=14,pad=16)
ax.legend(loc='upper right',frameon=False,fontsize=8)
fig.text(.105,.025,'Source: 50,688 Cernak/ORD experimental records. Producer assay labels, not independent truth.\n149 negative-component and 21 over-100% pairs excluded from this plot, retained in the audit.\nTwo-product fraction is not total purity. Thresholds are exploratory; zero labels can be censored.',fontsize=8,color='#444444')
fig.subplots_adjust(bottom=.20,left=.105,right=.97,top=.9)
fig.savefig(P/'root/ASSAY_DECISIONS.png')
fig.savefig(P/'root/ASSAY_DECISIONS.pdf')
print('Saved actual-label decision figure')
