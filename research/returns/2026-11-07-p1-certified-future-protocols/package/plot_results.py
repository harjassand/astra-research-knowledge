from pathlib import Path
from fractions import Fraction as Q
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

P=Path(__file__).resolve().parent/'results'
read=lambda n:json.loads((P/n).read_text())
trace=read('TRANSCRIPT.json');r=read('EXECUTION.json');c=read('CRITICAL_NOISE.json')
requests=((0,1),(0,-1),(1,1),(1,-1),(2,1),(2,-1))
project=[];completed=[];ages=[];age=0
for row in trace:
    axis,sign=requests[row['request']]
    project.append(sign*row['read_integers'][axis]/(1<<40))
    age+=1
    if row['served']:completed.append(row['step']);ages.append(age);age=0
fig=plt.figure(figsize=(12,7.4),layout='constrained')
grid=fig.add_gridspec(2,2,height_ratios=[1.45,1])
ax=fig.add_subplot(grid[0,:]);n=72
ax.plot(np.arange(n),project[:n],color='#226077',lw=1.4,label='Readout in the requested direction')
ix=[i for i in completed if i<n]
ax.scatter(ix,[project[i] for i in ix],color='#c35431',s=35,zorder=4,label='Request completed')
ax.axhline(.5,color='#6e6e6e',ls='--',lw=1,label='Reported threshold')
ax.set(xlabel='Controller tick (2 source-time units)',ylabel='Signed port readout',
       title='Executed hostile requests and read errors — first 72 of 432 ticks')
ax.legend(loc='lower right',frameon=False,ncol=3,fontsize=9)
ax.grid(alpha=.18)
ax=fig.add_subplot(grid[1,0])
ax.step(np.arange(1,len(ages)+1),ages,where='mid',color='#226077',lw=1.5)
ax.axhline(4,color='#c35431',ls='--',lw=1)
ax.set(xlabel='Completed request',ylabel='Ticks to completion',ylim=(0,4.6),yticks=range(5),
       title='All 120 executed requests met the deadline')
ax.grid(alpha=.18)
ax=fig.add_subplot(grid[1,1])
lo=float(Q(c['source_optimal_radius_lower']));hi=float(Q(c['source_optimal_radius_upper']))
star=float(Q(c['critical_radius']));yes=float(Q(r['reader_radius']));no=149/1024
ax.axvspan(lo,hi,color='#226077',alpha=.2)
ax.axvline(star,color='#226077',ls='--',lw=1.2)
ax.scatter([yes,no],[0,0],s=85,c=['#237953','#c35431'],zorder=3)
ax.text(yes,.2,'Certified policy',ha='center',fontsize=10,color='#237953')
ax.text(no,-.3,'Counterstrategy',ha='center',fontsize=10,color='#c35431')
ax.text((lo+hi)/2,.55,'True optimum lies in this interval',ha='center',fontsize=10)
ax.set(xlabel='Adversarial read-error radius',yticks=[],ylim=(-.6,.9),
       xlim=(yes-.00065,no+.00065),title='Capability inferred from 36 scalar acquisition readings')
ax.ticklabel_format(axis='x',style='plain',useOffset=False)
ax.grid(axis='x',alpha=.18)
fig.suptitle('A finite acquired model supports an indefinitely repeated protocol',fontsize=15,weight='bold')
fig.savefig(P/'CAUSAL_PROTOCOL_CERTIFICATE.png',dpi=180)
fig.savefig(P/'CAUSAL_PROTOCOL_CERTIFICATE.svg')
print(str(P/'CAUSAL_PROTOCOL_CERTIFICATE.png'))
