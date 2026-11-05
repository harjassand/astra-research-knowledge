"""Figures are exact-model calculations, not measured data."""
from pathlib import Path
import json
import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output'/'invention'
OUT.mkdir(parents=True,exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,
                     'axes.spines.top':False,'axes.spines.right':False,
                     'figure.facecolor':'white','axes.titleweight':'bold'})

angle=np.linspace(.05,180,600)
theta=np.radians(angle)
ell=np.sqrt(theta*theta+2*np.pi*theta)
fig,ax=plt.subplots(1,2,figsize=(11.5,4.4),layout='constrained')
ax[0].semilogy(angle,100*np.exp(-ell),color='#14566d',lw=2.5,label='Continuous control limit')
for n,col in [(5,'#dc8b26'),(10,'#a33750')]:
    sn=n*np.arccosh(np.cos(np.pi/n)/np.cos((np.pi+theta)/n))
    ax[0].semilogy(angle,100*np.exp(-sn),color=col,lw=1.8,ls='--',label=f'{n} constant stages')
ax[0].set(xlabel='Requested rotation (degrees)',ylabel='Largest retained amplitude (%)',
          title='Rotation consumes signal amplitude',xlim=(0,180))
ax[0].legend(frameon=False,fontsize=9)
ax[0].grid(alpha=.2)

ns=np.arange(5,81)
th=np.pi
sn=ns*np.arccosh(np.cos(np.pi/ns)/np.cos((np.pi+th)/ns))
kappa=np.exp(2*sn/ns)
ax[1].plot(ns,kappa,color='#14566d',lw=2.5)
ax[1].scatter([5],[kappa[0]],color='#a33750',s=45,zorder=3)
ax[1].annotate('5 stages: 25.377\n(proved optimum)',xy=(5,kappa[0]),xytext=(20,23),
                fontsize=10,arrowprops={'arrowstyle':'-','color':'#666666'})
ax[1].set(xlabel='Number of constant stages',ylabel='Smallest possible worst factor condition number',
          title='Exact resource law for a 180° rotation',xlim=(4,80),ylim=(0,29))
ax[1].grid(alpha=.2)
fig.suptitle('Bounded symmetric restoring forces: exact-model resource frontiers',fontsize=14,fontweight='bold')
fig.savefig(OUT/'rotation_resource_frontiers.png',dpi=190)
plt.close(fig)

resource=json.loads((ROOT/'invention_root'/'resource_table.json').read_text())
comp=resource['same_time_comparison']
fig,ax=plt.subplots(1,2,figsize=(11.5,4.4),layout='constrained')
vals=[comp[k] for k in ['cool_first','distributed_cooling','cool_last']]
bars=ax[0].bar(['Cooling first','Cooling throughout','Cooling last'],vals,
              color=['#acb9bf','#6695a7','#14566d'],width=.63)
for bar,v in zip(bars,vals):
    ax[0].text(bar.get_x()+bar.get_width()/2,v+.12,f'{v:.3f}',ha='center',fontsize=11)
ax[0].set(ylabel=r'Added mean-square error / $(D/\Lambda)$',ylim=(0,7.3),
          title='Same map, same minimum duration')
ax[0].text(.02,.96,r'$\theta=90^\circ,\ s=L_\theta+0.5$',transform=ax[0].transAxes,va='top',fontsize=10)
ax[0].tick_params(axis='x',labelsize=9)
ax[0].grid(axis='y',alpha=.2)
table=resource['rotation_table']
degrees=[r['angle_degrees'] for r in table]
lower=[r['input_energy_lower_bound_for_95pct_error_10pct_kBT'] for r in table]
fast=[r['input_energy_required_fastest_95pct_error_10pct_kBT'] for r in table]
ax[1].semilogy(degrees,lower,'o--',color='#a33750',lw=1.7,label='Necessary bound, any duration')
ax[1].semilogy(degrees,fast,'o-',color='#14566d',lw=2,label='Exact requirement, fastest boundary')
ax[1].set(xlabel='Requested rotation (degrees)',ylabel=r'Initial stored signal energy / $(k_B T_{bath})$',
          title='A small net work bill hides input resources',xlim=(0,185))
ax[1].text(.03,.97,'95% probability of error ≤ 10%\nof desired output radius',transform=ax[1].transAxes,
           va='top',fontsize=10)
ax[1].legend(loc='lower right',frameon=False,fontsize=8)
ax[1].grid(alpha=.2)
fig.suptitle('Thermal quality and input energy in the specified model',fontsize=14,fontweight='bold')
fig.savefig(OUT/'thermal_order_and_input_cost.png',dpi=190)
plt.close(fig)
print(json.dumps({'figures':[str(OUT/'rotation_resource_frontiers.png'),
                             str(OUT/'thermal_order_and_input_cost.png')]}))
