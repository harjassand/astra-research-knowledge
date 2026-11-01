#!/usr/bin/env python3
import json
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

P=Path(__file__).resolve().parent
checks=json.loads((P/'results/analytic_checks.json').read_text())
dyn=json.loads((P/'results/noncommuting_channel.json').read_text())

def spec(w,aa):
    x=np.abs(w)
    q=np.ones_like(x)
    for a in aa:q*=((a-x)/(a+x))**2
    out=2*x*np.where(w>0,1,q)/((1-q)*(1+x*x)**2)
    zero=(x==0)
    out[zero]=1/(2*sum(1/a for a in aa))
    return out

plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
fig,axs=plt.subplots(2,2,figsize=(11,7.2),constrained_layout=True)
w=np.linspace(-4,4,2401)+1e-12
target=np.where(w>0,2*w/(1+w*w)**2,np.nan)
for aa,label in [([1.],'2 modes'),([2.**j for j in range(-3,4)],'8 modes')]:
    axs[0,0].semilogy(w,np.maximum(spec(w,aa),1e-12),label=label)
axs[0,0].semilogy(w,target,'k--',lw=1.5,label='zero-temperature target')
axs[0,0].set(xlabel=r'frequency $\omega$',ylabel=r'$S(\omega)$',ylim=(1e-9,2),title='Positive spectra with exact thermal nodes')
axs[0,0].axvline(0,color='.7',lw=.8);axs[0,0].legend(frameon=False,fontsize=9)

t=np.linspace(0,8,161)
im=-t*np.exp(-t)/4
axs[0,1].plot(t,im,'k-',label='target free-bath commutator / 2i')
axs[0,1].plot(t[::10],im[::10],'o',mfc='none',label='explicit 2-mode bath')
axs[0,1].set(xlabel='time',ylabel=r'Im $C(t)$',title='Free dissipative response is exact')
axs[0,1].legend(frameon=False,fontsize=9)

rows=checks['positive_approximation_checks']
axs[1,0].semilogy([r['modes'] for r in rows],[r['proved_variance_bound'] for r in rows],'o',label='proved bound')
axs[1,0].semilogy([r['modes'] for r in rows],[r['excess_variance'] for r in rows],'x',ms=7,label='numerical positive integral')
axs[1,0].set(xlabel='oscillator modes (different node grids)',ylabel='excess classical-noise variance',title='Conservative bound; no optimality claim')
axs[1,0].legend(frameon=False,fontsize=9)

rows=dyn['cutoff_checks']
axs[1,1].semilogy([r['cutoff'] for r in rows],[r['proved_channel_cutoff_bound'] for r in rows],'o-',label='proved cutoff bound')
axs[1,1].semilogy([r['cutoff'] for r in rows],[r['diamond_upper_to_refined_K6'] for r in rows],'x-',label='channel difference to refined K=6')
axs[1,1].set(xlabel='total Fock cutoff K',ylabel='qubit channel error upper bound',title='Noncommuting finite 2-mode test, T=2')
axs[1,1].legend(frameon=False,fontsize=8)
fig.suptitle('Response-exact rational bath: earned construction and finite checks',fontsize=14)
fig.savefig(P/'results/construction_checks.png',dpi=180)
fig.savefig(P/'results/construction_checks.pdf')
