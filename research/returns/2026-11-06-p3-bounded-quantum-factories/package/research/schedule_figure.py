"""Exact schematic of the fixed interval schedule; not experimental data."""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Patch

out=Path(__file__).resolve().parent/'figures'
out.mkdir(exist_ok=True)
n,b=8,3
partition={(0,1),(2,3,4),(5,),(6,7)}
fig,ax=plt.subplots(figsize=(9,4.0))
row=0
for k in range(1,b+1):
    for residue in range(k):
        covered=set()
        for start in range(residue,n-k+1,k):
            interval=tuple(range(start,start+k))
            active=interval in partition
            covered.update(interval)
            ax.add_patch(Rectangle((start-.44,row-.32),k-.12,.64,
                facecolor='#247A82' if active else '#A9B6BE',
                edgecolor='#172D3D',lw=.7))
            if active:
                ax.text(start+(k-1)/2,row,'replace',ha='center',va='center',
                    fontsize=8,color='white',fontweight='bold')
        for i in set(range(n))-covered:
            ax.add_patch(Rectangle((i-.39,row-.28),.78,.56,
                facecolor='#EDF4F5',edgecolor='#A9B6BE',lw=.6))
        ax.text(-.75,row,f'length {k}, color {residue}',ha='right',va='center',fontsize=9)
        row+=1
for edge in (1.5,4.5,5.5):
    ax.axvline(edge,color='#247A82',ls=':',lw=.9,zorder=0)
ax.set_xlim(-.55,7.55)
ax.set_ylim(5.6,-.8)
ax.set_xticks(range(n),[str(i+1) for i in range(n)])
ax.xaxis.tick_top()
ax.set_xlabel('Physical site',labelpad=10)
ax.xaxis.set_label_position('top')
ax.set_yticks([])
for sp in ax.spines.values():sp.set_visible(False)
ax.legend(handles=[Patch(facecolor='#247A82',label='Replacement'),
    Patch(facecolor='#A9B6BE',label='Product noise'),
    Patch(facecolor='#EDF4F5',edgecolor='#A9B6BE',label='Padding')],
    loc='lower center',bbox_to_anchor=(.5,-.16),ncol=3,frameon=False,fontsize=9)
fig.subplots_adjust(left=.25,right=.98,top=.82,bottom=.15)
fig.savefig(out/'fixed_schedule.png',dpi=200,bbox_inches='tight',facecolor='white')
fig.savefig(out/'fixed_schedule.svg',bbox_inches='tight',facecolor='white')

