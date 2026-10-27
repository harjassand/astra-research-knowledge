from pathlib import Path
import json
from fractions import Fraction as F
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from network import run,build,serializable

root=Path(__file__).resolve().parent
N=5;net=build(N);r=run([1,0,1,1,0]);L=2*N+1
fig=plt.figure(figsize=(13,7.2),layout='constrained')
gs=fig.add_gridspec(2,2,height_ratios=[1,1.25],width_ratios=[1.7,1])
ax=fig.add_subplot(gs[0,:])
for j in range(L-1):ax.plot([j+1,j+2],[0,0],c='#355f89',lw=2)
for j in range(L):
    color='#355f89' if j%2==0 else '#c97936'
    ax.plot([j+1,j+1],[0,1],c=color,lw=1.7)
    ax.scatter([j+1],[0],s=220,c='#e6ebf0',edgecolors='#333333',zorder=3)
    ax.scatter([j+1],[1],s=180,c='#fff4d7',edgecolors='#555555',zorder=3)
    ax.text(j+1,0,f'q{j+1}',ha='center',va='center',fontsize=8)
    ax.text(j+1,1,f'z{j+1}',ha='center',va='center',fontsize=8)
for i in range(N):
    xx=2*i+2.5
    for endpoint in [2*i+2,2*i+3]:ax.plot([endpoint,xx],[0,-1],c='#9d5846',lw=1.7)
    ax.scatter([xx],[-1],s=260,marker='s',c='#eff3e3',edgecolors='#333333',zorder=3)
    ax.text(xx,-1,f'm{i+1}',ha='center',va='center',fontsize=8)
ax.text(.15,0,'fixed +',ha='center',va='center',fontsize=9)
ax.plot([.55,1],[0,0],c='#355f89',lw=2)
ax.text(L+.8,0,'fixed −',ha='center',va='center',fontsize=9)
ax.plot([L,L+.4],[0,0],c='#355f89',lw=2)
ax.set(xlim=(-.25,L+1.5),ylim=(-1.45,1.8))
ax.axis('off')
ax.set_title('One scalar H; all couplings reciprocal; stationary output memories below the track',fontsize=12)
ax.text(1,1.55,'Track edges: −10     Auxiliary edges: alternating −4 / +4     Memory edges: +1',fontsize=10)

heat=fig.add_subplot(gs[1,0]);data=np.asarray([z['state'] for z in r['phases']]).T
heat.imshow(data,aspect='auto',interpolation='nearest',cmap=ListedColormap(['#355f89','#e4a657']),vmin=-1,vmax=1)
heat.set_yticks([0,L-1,L,2*L-1,2*L,2*L+N-1],['q1',f'q{L}','z1',f'z{L}','m1',f'm{N}'])
heat.set_xticks(np.arange(len(r['phases'])),[str(z['H']) for z in r['phases']],rotation=90,fontsize=7)
heat.axhline(L-.5,c='white',lw=1);heat.axhline(2*L-.5,c='white',lw=1)
heat.set(xlabel='Successive global field commands',title='Exact endpoint states while writing 10110')
for j in range(N):heat.text(len(r['phases'])-.4,2*L+j,str([1,0,1,1,0][j]),ha='left',va='center',fontsize=9)

cost=fig.add_subplot(gs[1,1]);nn=np.arange(1,65)
cost.plot(nn,478*nn+200,label='Ideal net full-rewrite work',c='#355f89',lw=2)
cost.plot(nn,88*nn**2+856*nn+348,label='Positive source work, no recovery',c='#a14e42',lw=2)
cost.set_yscale('log');cost.set(xlabel='Output bits N',ylabel='Normalized work',title='0…0 → 1…1, including reset')
cost.legend(fontsize=8,frameon=False);cost.grid(alpha=.2)
fig.savefig(root/'broadcast_construction.png',dpi=180)
fig.savefig(root/'broadcast_construction.pdf')

checks=json.loads((root/'CHECKS.json').read_text())
cost_checks=[]
for batch in checks['rewrite_order_checks']:
    n=batch['N']
    for v in batch['cases']:
        p=sum(v['old']);q=sum(v['new'])
        expected=F(452*n+200+26*(p+q))+F(2,10**9)*(14*n+6+p+q)
        actual=F(v['dissipation'])
        assert actual==expected and F(v['energy_change'])==0 and F(v['work'])==actual
        cost_checks.append(True)
for row in checks['resource_scaling']:
    n=row['N']
    for v in row['cases']:
        nominal=(88*n*n+856*n+348) if v['old_bit']==0 else (60*n*n+850*n+348)
        assert abs(F(v['gross_positive_work'])-nominal)<F(1,100000)
receipt=dict(status='INTERNALLY_CONSTRUCTED_ENERGY_MODEL_NOT_ACQUIRED_TECHNOLOGY',
             input_alphabet=[-64,-16,-10,0,8,10,12,15,24],cells='5N+2',edges='6N+1',
             maximum_degree=4,maximum_weighted_degree=25,maximum_onsite_c=40,maximum_drive_gain=2,
             maximum_absolute_boundary_bias=10,min_wrong_cell_event_margin=2,min_endpoint_margin=1,
             pulse_bound='3N+8',full_rewrite_flip_count='10N+4+p_old+p_new',
             ideal_net_work='452N+200+26(p_old+p_new)',
             full_work_balance_checks=len(cost_checks),full_work_balance_all_exact=True,
             no_recovery_work_zeros_to_ones='88N^2+856N+348',
             no_recovery_work_ones_to_zeros='60N^2+850N+348',
             measured_material_performance='NOT_ACQUIRED',novelty='UNKNOWN; strong one-input memory prior art exists',
             practical_advantage='NOT_ESTABLISHED',whole_pattern_thermal_fidelity='NOT_ESTABLISHED',
             parent_finite_compliance_version='19 levels; different finite-time dynamics and work accounting')
(root/'RESULT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
