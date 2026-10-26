"""Generate standalone scientific figure from the constructed linear models."""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.linalg import eigh
from explore import optimum, ladder_moments

OUT=Path(__file__).resolve().parent


def density(c,r,t):
    n=len(c)
    lap=np.zeros((n,n))
    for i in range(n-1):
        g=1/r[i]
        lap[i,i]+=g; lap[i+1,i+1]+=g
        lap[i,i+1]-=g; lap[i+1,i]-=g
    lap[-1,-1]+=1/r[-1]
    w,v=eigh(lap/np.sqrt(c[:,None]*c[None,:]))
    weights=v[-1,:]*v[0,:]/(r[-1]*np.sqrt(c[-1]*c[0]))
    f=np.sum(weights[:,None]*np.exp(-w[:,None]*t[None,:]),axis=0)
    return f


if __name__=='__main__':
    d=json.loads((OUT/'numerical_results.json').read_text())
    fig,ax=plt.subplots(1,2,figsize=(11,4.1),layout='constrained')
    ns=np.arange(2,101)
    for ratio in [2,10,100,10000]:
        b=1/(1+(ns-1)*np.tanh(np.log(ratio)/(2*(ns-1))))
        line,=ax[0].plot(ns,np.sqrt(b),label=f'Total/source capacity {ratio:g}')
        ax[0].axhline(1/np.sqrt(1+np.log(ratio)/2),color=line.get_color(),lw=.8,ls=':')
    ax[0].set(xlabel='Number of thermal lumps',ylabel='Minimum RMS pulse width / mean',
              title='Exact optimum over reciprocal trees',ylim=(0,1))
    ax[0].legend(fontsize=8)
    t=np.linspace(0,4,2501)
    n,ratio=8,100.
    c,r,b=optimum(n,ratio)
    ax[1].plot(t,density(c,r,t),lw=2,label='Analytic optimal ladder')
    comp=next(x for x in d['ordinary_comparators'] if x['n']==8)
    ax[1].plot(t,density(np.array(comp['capacities']),np.array(comp['resistances']),t),
               ls='--',lw=1.4,label='Ordinary optimized ladder (same resources)')
    cu=np.r_[1.,np.repeat((ratio-1)/(n-1),n-1)]
    ru=np.ones(n)
    ru=ru/ladder_moments(cu,ru)[0]
    ax[1].plot(t,density(cu,ru,t),color='0.5',lw=1.3,label='Uniform remaining capacities and resistors')
    ax[1].set(xlabel='Time / mean delay',ylabel='Normalized release flux',
              title='Local model only: 8 lumps, capacity ratio 100',xlim=(0,4))
    ax[1].legend(fontsize=8)
    for a in ax:
        a.spines[['top','right']].set_visible(False)
        a.grid(alpha=.15)
    fig.savefig(OUT/'thermal_delay_result.png',dpi=180)
    fig.savefig(OUT/'thermal_delay_result.svg')
    print(str(OUT/'thermal_delay_result.png'))
