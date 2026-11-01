"""Scientific overview: actual force, full meter calendar, and history tail."""
from pathlib import Path
import json, os
import numpy as np
os.environ.setdefault('MPLCONFIGDIR','producer-workspace/astra_phase8_matplotlib')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

HERE=Path(__file__).resolve().parent
p=json.loads((HERE.parent/'physical_mechanisms/one_bus_parity_results.json').read_text())['optimized_safe']
T=p['T'];k=p['kappa'];A,B,c=p['coefficients']
t=np.linspace(0,T,3001);q=np.pi*t/T;dq=np.pi/T
s=np.sin(q);co=np.cos(q)
X=s*s*np.sin(2*q);Xp=dq*(2*s*co*np.sin(2*q)+2*s*s*np.cos(2*q))
Y=s*s*(np.cos(2*q)+.5);Yp=dq*(2*s*co*(np.cos(2*q)+.5)-2*s*s*np.sin(2*q))
ef=np.exp(k*t/2)
x=A*ef*X;xp=A*ef*(Xp+k*X/2)
y=B*ef*(Y-c*X);yp=B*ef*(Yp-c*Xp+k*(Y-c*X)/2)
fx=xp+k*x/2;fy=-(yp+k*y/2)
total=np.sqrt(4*fx*fx+fy*fy)

plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.spines.top':False,
 'axes.spines.right':False,'axes.titleweight':'bold','axes.labelcolor':'#253247',
 'text.color':'#253247','xtick.color':'#253247','ytick.color':'#253247'})
fig=plt.figure(figsize=(12,8.6),facecolor='white')
gs=fig.add_gridspec(2,2,height_ratios=[1,1.05],hspace=.65,wspace=.32)
a=fig.add_subplot(gs[0,0])
a.plot(t,fx,color='#237a9b',label='Each data force quadrature')
a.plot(t,fy,color='#8d5cad',label='Ancilla force quadrature')
a.plot(t,total,color='#dc8531',lw=2.5,label='Largest total branch force')
a.axhline(3,color='#526070',ls='--',lw=1,label='Declared shared cap')
a.set(xlabel=r'Time $gt$',ylabel=r'Force / $g$',xlim=(0,T),ylim=(-3.2,3.35))
a.set_title('A  Finite parity interaction',loc='left',pad=12)
a.legend(fontsize=8.5,loc='lower right',frameon=False)
a.grid(alpha=.15)

b=fig.add_subplot(gs[0,1])
dur=[4.472,.05,.05,1.84,.05,4.472,.05]
cols=['#237a9b','#8d5cad','#8d5cad','#dc8531','#8d5cad','#237a9b','#8d5cad']
left=0
for d,col in zip(dur,cols):
 b.barh(0,d,left=left,height=.32,color=col,edgecolor='white',linewidth=.4)
 if d>1:
  b.text(left+d/2,0,f'{d:g}',ha='center',va='center',color='white',weight='bold',fontsize=11)
 left+=d
b.set(xlim=(0,11),ylim=(-.5,.75),xlabel=r'Elapsed time $gt$',yticks=[])
b.set_title('B  Complete meter: 10.984 / g',loc='left',pad=12)
b.text(0,.53,'Both driven readouts, all local slots and port ramps',fontsize=9.7)
b.text(0,-.39,'Outer decoding and additional waits remain explicit.',fontsize=9.5)
b.legend(handles=[Patch(color='#237a9b',label='Preparation / terminal readout'),
 Patch(color='#dc8531',label='Parity loop'),Patch(color='#8d5cad',label='Control / decision')],
 loc='upper left',bbox_to_anchor=(-.02,-.29),frameon=False,fontsize=9)
b.spines['left'].set_visible(False)

d=fig.add_subplot(gs[1,:])
L=np.linspace(200,400,801);lq=64-.4*(L+1)
logbound=np.minimum(0,7+(lq/2+np.log1p(np.exp(lq/2)))/np.log(10))
d.plot(L,logbound,lw=2.6,color='#237a9b')
d.axhline(-6,color='#8d5cad',ls='--',lw=1.2,label=r'$10^{-6}$ reference accuracy')
selected=7+((64-.4*321)/2+np.log1p(np.exp((64-.4*321)/2)))/np.log(10)
d.scatter([320],[selected],color='#dc8531',s=55,zorder=3)
d.annotate('L = 320: whole-history bound ≤ 1.04 × 10⁻⁷',xy=(320,selected),xytext=(236,-11.7),
 arrowprops={'arrowstyle':'->','color':'#526070'},fontsize=11)
d.set(xlabel=r'Mathematical input-sector cap $L$',ylabel=r'$log_{10}$ half trace-distance bound',
 xlim=(200,400),ylim=(-15,.5))
d.set_title('C  Rare-history cost from the analytic energy barrier',loc='left',pad=12)
d.text(.99,.94,r'$M_{0.4}(t)\leq e^{64}$; $10^7$ actual interfaces',transform=d.transAxes,
 ha='right',va='top',fontsize=10)
d.legend(loc='lower right',frameon=False,fontsize=10)
d.grid(alpha=.16)
fig.suptitle('Retained apparatus: a finite operation and a complete-history bound',
 fontsize=16,weight='bold',x=.075,ha='left',y=.985)
fig.text(.075,.015,'Effective linear / homogeneous-thermal model. Tail cost is not the total logical error; microscopic and controller terms remain.',fontsize=9,color='#526070')
fig.subplots_adjust(left=.08,right=.97,top=.90,bottom=.09)
for ext in ['png','svg']:
 fig.savefig(HERE/f'retained_operation_and_history.{ext}',dpi=180,bbox_inches='tight')
print('Saved retained_operation_and_history.png and .svg')
