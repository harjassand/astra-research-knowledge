from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import json, math
out=Path('outputs');out.mkdir(exist_ok=True)
sstar=math.log((1+math.sqrt(17))/2)
h=np.array([1.,2.]);A=np.array([[2.,-math.sqrt(2)],[-math.sqrt(2),3.]])
def phi(s):
 d=np.exp(-s*h/2)
 return math.log(max(1.,np.linalg.eigvalsh(d[:,None]*A*d[None,:])[-1]))
def objective(c,s):return phi(s)+c*s
def curve(c):
 lo,hi=0.,sstar
 ratio=(math.sqrt(5)-1)/2
 l=hi-ratio*(hi-lo);r=lo+ratio*(hi-lo)
 for _ in range(85):
  if objective(c,l)<objective(c,r):hi,r=r,l;l=hi-ratio*(hi-lo)
  else:lo,l=l,r;r=lo+ratio*(hi-lo)
 return min(objective(c,0),objective(c,sstar),objective(c,(lo+hi)/2))
x=np.linspace(0,2.15,431);ent=np.array([curve(c) for c in x]);sep=np.minimum(x*math.log(2),math.log(4))
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.spines.top':False,'axes.spines.right':False})
fig,ax=plt.subplots(figsize=(8,4.7),layout='constrained')
ax.fill_between(x,sep,ent,color='#DDEAF7',label='Entanglement advantage')
ax.plot(x,ent,color='#163F68',lw=2.8,label='Optimal entangled probes')
ax.plot(x,sep,color='#B35F16',lw=2.5,label='All separable probes')
ax.set(xlim=(0,2.15),ylim=(0,1.5),xlabel='Hard input-energy ceiling per channel use, c',ylabel='Asymptotic miss exponent per use',title='Exact hard-energy tradeoff for the qutrit example')
ax.text(.14,1.22,r'$-\log p_n(nc)=n g(c)+O(\log n)$',fontsize=13,color='#163F68')
ax.text(.14,1.04,r'Initial slopes: $\log[(1+\sqrt{17})/2]$ versus $\log 2$',fontsize=10.5)
ax.axvline(5/3,ls=':',lw=1,color='#8091A4');ax.text(5/3+.025,.53,'Entangled saturation\nat c = 5/3',fontsize=9,color='#506077')
ax.grid(axis='y',alpha=.16);ax.legend(loc='lower right',frameon=False,fontsize=9)
fig.savefig(out/'hard_energy_tradeoff.png',dpi=190)
fig.savefig(out/'hard_energy_tradeoff.pdf')
(out/'hard_energy_tradeoff_data.json').write_text(json.dumps({'status':'Numerical illustration of the internally derived exact variational theorem; not proof certification','sstar':sstar,'eta':math.log(2),'c':x.tolist(),'entangled_rate':ent.tolist(),'separable_rate':sep.tolist()},indent=2)+'\n')
assert np.all(ent+1e-10>=sep)
assert abs(curve(2)-math.log(4))<1e-10
print('Saved plot and data; variational endpoint and comparison checks passed.')
