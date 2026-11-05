from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parent
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,
    'axes.spines.top':False,'axes.spines.right':False,
    'axes.labelcolor':'#152535','text.color':'#152535',
    'axes.titleweight':'bold','savefig.bbox':'tight'})
colors=['#195c85','#16a085','#c98116','#8a4f9e']
s=np.logspace(-5,np.log10(1/64),400); L=np.log(64)
fig,ax=plt.subplots(figsize=(6.8,3.7))
for kap,c in zip([16,256,4096,1e8],colors):
    phi=np.sqrt(kap)*L*np.log1p(L/(s*np.sqrt(kap)))
    ax.loglog(s,phi,color=c,lw=2,label=rf'$\kappa={kap:g}$')
ax.loglog(s,L*L/s,'--',color='#707c89',lw=1.5,label='unbounded rate range')
ax.set(xlabel=r'Maximum transient age $s=\mu T$',ylabel=r'Log-effort scale $\Phi$',
       title='A finite rate range changes the price of early inference')
ax.grid(alpha=.16,which='both'); ax.legend(ncol=2,fontsize=8,loc='upper right')
fig.savefig(ROOT/'resource_crossover.pdf'); fig.savefig(ROOT/'resource_crossover.png',dpi=200)
plt.close(fig)
t=np.logspace(-5,1.1,600)
hplus=.8*(-np.expm1(-t))+.2*(-np.expm1(-16*t))/16
hminus=(-np.expm1(-4*t))/4
fig,ax=plt.subplots(figsize=(6.8,3.5))
ax.semilogx(t,hplus,color=colors[0],lw=2,label=r'$0.8\,\delta_1+0.2\,\delta_{16}$')
ax.semilogx(t,hminus,color=colors[1],lw=2,label=r'$\delta_4$')
ax.axvspan(t[0],1/128,color='#d5dde4',alpha=.7,label=r'observed interval $t\leq1/128$')
ax.axhline(.8125,color=colors[0],ls=':',lw=1)
ax.axhline(.25,color=colors[1],ls=':',lw=1)
ax.text(1.5,.83,'DC gain 0.8125',color=colors[0],fontsize=9)
ax.text(1.5,.27,'DC gain 0.25',color=colors[1],fontsize=9)
ax.set(xlabel='Dimensionless time',ylabel='Normalized unit-step response',
       title='A simple positive-spectrum ambiguity')
ax.legend(fontsize=8,loc='upper left'); ax.grid(alpha=.16)
fig.savefig(ROOT/'simple_witness.pdf'); fig.savefig(ROOT/'simple_witness.png',dpi=200)
plt.close(fig)
print('Scientific figures generated from analytic formulas.')
