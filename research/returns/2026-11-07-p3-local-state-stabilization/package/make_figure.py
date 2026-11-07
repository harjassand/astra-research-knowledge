from pathlib import Path
import json,math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from fractions import Fraction

p=Path(__file__).resolve().parent
b=json.loads((p/'BOTTLENECK_CERTIFICATES.json').read_text())
t=json.loads((p/'ACCURACY_RESOURCE_TABLE.json').read_text())
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.spines.top':False,
                    'axes.spines.right':False,'figure.facecolor':'#fbfcfe','axes.facecolor':'#fbfcfe'})
fig,axes=plt.subplots(1,2,figsize=(12.8,5.1))
ax=axes[0]
ax.plot([x['N'] for x in b],[math.log10(int(x['quantum_auxiliary_allowed_event_lower_integer'])) for x in b],
        marker='o',color='#234e70',linewidth=2.2)
ax.set_title('Exact equilibrium: a certified obstruction',loc='left',fontweight='bold',pad=16)
ax.set_xlabel('Physical spins N')
ax.set_ylabel('log₁₀ minimum local events')
ax.grid(alpha=.18)
ax.text(.03,.96,'Curie–Weiss, β = 2\n≤ 5 physical spins per event\nArbitrary quantum auxiliaries',
        transform=ax.transAxes,va='top',fontsize=10,bbox={'facecolor':'white','edgecolor':'#dddddd','pad':7})
ax=axes[1]
x=[1/float(Fraction(z['requested_duty_error_bound'])) for z in t]
y=[z['total_events_bound'] for z in t]
ax.loglog(x,y,marker='o',linewidth=2.2,color='#b35c23')
ax.set_title('Approximate restoration: a finite construction',loc='left',fontweight='bold',pad=16)
ax.set_xlabel('Inverse allowed clock error 1/δ')
ax.set_ylabel('Certified sufficient local events')
ax.grid(alpha=.18,which='both')
ax.text(.04,.96,'Fixed 4-gate thermal-state circuit\n4 work + 4 clock qubits\nComplete mixing error ≤ 1/16',
        transform=ax.transAxes,va='top',fontsize=10,bbox={'facecolor':'white','edgecolor':'#dddddd','pad':7})
fig.suptitle('Local stabilization has a precision cost',fontsize=19,fontweight='bold',y=1.01)
fig.text(.5,-.01,'Left: lower bound for exact stationary physical Gibbs marginals.  Right: conservative upper bound for a different, approximate process.\nThese are mathematical event counts, not measured device times; gate, reset, model and holding costs remain separate.',
         ha='center',fontsize=9.5,color='#444444')
fig.tight_layout(pad=2)
fig.savefig(p/'PRECISION_AND_LOCAL_RESTORATION.png',dpi=170,bbox_inches='tight')
