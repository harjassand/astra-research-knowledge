"""Finite modal split arbitrarily close to the minimum stiffness boundary."""
from fractions import Fraction as Q
from pathlib import Path
from intervals import I,sqrt,bose,full_conductance
from certify_joint_cap import components
from certify_envelope import interpolate

HERE=Path(__file__).resolve().parent
C=Q(1,20);k0=20
r=sqrt(40);d=sqrt(101)
ordinary=[sqrt(22-2*d),r,sqrt(22+2*d)]
lam,mu,eta=interpolate(ordinary)
assert mu.hi<0 and eta.lo>0
v=100;w=I(10)
R=bose(w)+lam/w+2*mu*w-eta/(w**3)
assert R.hi<0
G=Q(v-k0,v*(v-2*k0))
gamma=2*I(v)*sqrt(v)*G*G/(1-4*G)
derivative=gamma*R
cost_slope=Q((v-k0)**2,v)
epsilon=Q(1,10000);H=epsilon*v
k=(1-epsilon)**2/(C-epsilon/v)
assert epsilon**2/H+(1-epsilon)**2/k==C
assert 20<H+k<Q('20.0065')
row=components(epsilon,H,k)
J=full_conductance(row['edges']);Jone=full_conductance(ordinary)
gain=Jone-J
assert gain.lo>0
lines=['PASS: certified one-pendant modal instability at C=1/20.',
       'mu '+mu.decimal(), 'eta '+eta.decimal(), 'R(10) '+R.decimal(),
       'positive new-band width coefficient gamma '+gamma.decimal(),
       'dJ/d_epsilon '+derivative.decimal(),
       'd_kappa/d_epsilon '+str(cost_slope),
       'Actual finite split masses [1,1/10000,9999/10000]',
       'H='+str(H)+'; k='+str(k)+'; exact C=1/20',
       'total stiffness '+I(H+k).decimal(),
       'full all-band conductance '+J.decimal(),
       'J_one-J_split '+gain.decimal(),
       'All modes, including the small high-frequency branch, are counted.']
text='\n'.join(lines)+'\n'
(HERE/'CERTIFIED_BOUNDARY_SPLIT.txt').write_text(text)
print(text)
