"""Render the observed inverse constants and analytic bounds from saved data."""
import json,pathlib,os,tempfile
os.environ.setdefault('MPLCONFIGDIR',str(pathlib.Path(tempfile.gettempdir())/'astra-p1-mpl-cache'))
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=pathlib.Path(__file__).resolve().parent
rows=json.loads((ROOT/'DIAGNOSTICS.json').read_text())['lift_cases']
n=np.array([r['n'] for r in rows])
lo=np.array([r['operator_lower_bound'] for r in rows])
hi=np.array([r['operator_upper_bound'] for r in rows])
kf=np.array([r['F_inverse_constant'] for r in rows])
fig,ax=plt.subplots(figsize=(7.7,4.5),layout='constrained')
ax.fill_between(n,lo,hi,color='#2176ae',alpha=.16,label='Operator amplification: analytic bounds')
ax.plot(n,lo,color='#2176ae',marker='o',linewidth=1.5,markersize=4)
ax.plot(n,hi,color='#2176ae',marker='o',linewidth=1.5,markersize=4)
ax.plot(n,kf,color='#b33a3a',marker='s',linewidth=2,markersize=5,label='Frobenius inverse constant')
ax.set(xscale='log',yscale='log',xlabel='Matrix dimension n',ylabel='Worst-case amplification / bound',
       title='The target norm changes the stability conclusion')
ax.set_xticks(n,labels=[str(x) for x in n]);ax.set_yticks([1,2,5,10,20,50,100],labels=['1','2','5','10','20','50','100'])
ax.set_ylim(1,110);ax.grid(True,which='major',alpha=.2);ax.legend(loc='upper left',frameon=False)
ax.spines[['top','right']].set_visible(False)
fig.text(.5,-.015,'Recorded K4 lifts, one edge removed; q = 3. Floating-point evaluations of proved formulas.',ha='center',fontsize=9)
(ROOT/'figures').mkdir(exist_ok=True)
fig.savefig(ROOT/'figures'/'norm_separation.pdf',bbox_inches='tight')
fig.savefig(ROOT/'figures'/'norm_separation.png',dpi=170,bbox_inches='tight')
print(json.dumps({'matplotlib':matplotlib.__version__,'figure':'figures/norm_separation.pdf'}))
