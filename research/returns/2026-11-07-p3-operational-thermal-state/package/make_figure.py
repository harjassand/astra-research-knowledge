"""Scientific figure from the delivered data; no experimental observations."""
import json,math
from pathlib import Path
from fractions import Fraction as Q
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parent
plt.rcParams.update({'font.size':11,'axes.spines.top':False,'axes.spines.right':False,
                     'figure.facecolor':'white','axes.titleweight':'bold'})
fig,axes=plt.subplots(1,3,figsize=(15,4.4),layout='constrained')
colors={'canonical':'#304a9b','window':'#007c72'}
for label in colors:
    raw=json.loads((ROOT/f'{label.upper()}_N64_BLOCKS.json').read_text()); N=64
    dist=np.zeros(N+1)
    for b in raw['blocks']:
        A=(np.array(b['A_re'],float)+1j*np.array(b['A_im'],float))/(2.**b['bits'])
        diag=np.sum(abs(A)**2,axis=1); diag/=diag.sum()
        q=float(Q(b['probability_count'],1<<b['probability_bits']))
        for k,p in zip(b['keep'],diag): dist[(N-b['L'])//2+k]+=q*p
    x=(N-2*np.arange(N+1))/N
    axes[0].plot(x,dist,'o-',ms=3,lw=1.7,color=colors[label],label='Canonical' if label=='canonical' else 'Constrained optimum')
axes[0].axvspan(-.25,.25,color='#007c72',alpha=.08)
axes[0].set(title='A  Prepared magnetization law',xlabel=r'$M_z=N^{-1}\sum_i Z_i$',ylabel='Probability per outcome',xlim=(-1.02,1.02))
axes[0].legend(frameon=False,fontsize=9,loc='upper left')
axes[0].text(.55,.91,'64 spins, quartic model\n'+r'$\beta=2$, window $[-1/4,1/4]$',transform=axes[0].transAxes,fontsize=8)

data=json.loads((ROOT/'STRUCTURAL_RESULTS.json').read_text())
cw=data['Curie_Weiss_binary64_diagnostics']; n=np.array([r['N'] for r in cw])
axes[1].plot(n,[math.log10(r['central_window_probability']) for r in cw],'o-',color='#304a9b',label='Exact binomial sum (binary64)')
upper=(n-1)*math.log10(2)-2*(1-1/16)*n*n/(n-1)/math.log(10)
axes[1].plot(n,upper,'--',color='#c47a10',label='Analytic upper bound')
axes[1].set(title='B  Mean zero can hide rare outcomes',xlabel='Number of spins',ylabel=r'$\log_{10}\Pr(|M_z|\leq1/4)$')
axes[1].text(.05,.55,'Ferromagnetic Curie–Weiss model\n'+r'$\beta=2$; zero field',transform=axes[1].transAxes,fontsize=9)
axes[1].legend(frameon=False,fontsize=8,loc='lower left')

rows=data['tagged_sector_obstruction']; pos=np.arange(len(rows)); width=.34
axes[2].bar(pos-width/2,[float(Q(r['canonical_J0_probability_certified_lower'])) for r in rows],width,color='#304a9b',label='Target singlet-sector weight ≥')
axes[2].bar(pos+width/2,[float(Q(r['tagged_product_bath_reachable_upper'])) for r in rows],width,color='#bc5a40',label='Loaded-sample reachable weight ≤')
axes[2].set(xticks=pos,xticklabels=['8 / 20','16 / 32','64 / 64'],ylim=(0,1.13),
            title='C  A control interface can be insufficient',xlabel=r'Number of spins / $\beta$',ylabel='Sector probability')
axes[2].legend(frameon=False,fontsize=8,loc='upper center')
for i,r in enumerate(rows):
    bound=Q(r['trace_error_certified_lower']); down=(bound.numerator*1000//bound.denominator)/1000
    axes[2].text(i,.50,'T ≥\n'+f'{down:.3f}',ha='center',fontsize=10)
fig.suptitle('Finite-system state preparation: outcome control, thermal rarity and access',fontsize=15,fontweight='bold')
fig.savefig(ROOT/'OPERATIONAL_THERMODYNAMICS.png',dpi=190)
print('Saved OPERATIONAL_THERMODYNAMICS.png')
