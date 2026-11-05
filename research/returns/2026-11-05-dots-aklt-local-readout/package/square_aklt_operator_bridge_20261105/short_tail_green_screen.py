"""Positive 60-short-types plus all-length tail comparison. Feasibility first.
Uses exact short local geometry, interval-certified total moment caps, and raw
finite-type kernel (not heat-bath). No numerical q improvement is called a gap.
"""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
import sys,json,numpy as np
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
P=Path(__file__).resolve().parent
sys.path.insert(0,str(P.parent/'square_aklt_boundary_operation_20261105'))
from crossed_loop_influence import variants
cat=json.loads((P.parent/'square_aklt_loop_audit_20261105/loop_catalog_through12.json').read_text())
C=np.load(P.parent/'square_aklt_boundary_operation_20261105/crossed_loop_influence_l12.npz')['C'];N=len(cat)
x=F(1000001,3000000);tilt=3*x
# Rational upper caps rounded outwards from the audited interval certificate.
Gs=F('0.007804025440');Gt=F('0.041045250940');S=F('0.523943909811');T=F('1.690182152836');M4=F('0.046531016280')
svec=[];tvec=[];m4short=F(0);ns=[];nt=[];rs=[];Ls=[]
for typ in cat:
 vs=list(map(tuple,typ['cyclic_vertices']));L=len(vs);mult=len(variants(vs));cnt=Counter(vs);nstraight=nturn=0
 for k,v in enumerate(vs):
  a=vs[k-1];b=vs[(k+1)%L]
  straight=(a[0]+b[0]==2*v[0] and a[1]+b[1]==2*v[1]);nstraight+=straight;nturn+=not straight
 n2s=sum(1 for k,v in enumerate(vs)if cnt[v]==1 and(vs[k-1][0]+vs[(k+1)%L][0]==2*v[0] and vs[k-1][1]+vs[(k+1)%L][1]==2*v[1]))
 n2t=sum(c==1 for c in cnt.values())-n2s;n4=sum(c==2 for c in cnt.values())
 b=F(typ['activity'])*tilt**L*L*mult
 svec.append(b*n2s);tvec.append(b*n2t);m4short+=b*n4
 ns.append(nstraight);nt.append(nturn);rs.append(n4);Ls.append(L)
Ss=sum(svec,F(0));Ts=sum(tvec,F(0));st=S-Ss;tt=T-Ts;mt=M4-m4short
as_t=st/5+tt/2;at_t=st/2+7*tt/20;d=as_t+mt
assert as_t>=at_t
assert as_t-at_t>=F(3*14,4)*x**14
assert all(z>0 for z in(st,tt,mt))
# Finite normalized matrix; target exponential tilt included.
Larr=np.array(Ls,float);Cs=C*Larr[None,:]/Larr[:,None]*np.array([float(tilt**L)for L in Ls])[None,:]
bvec=np.array([float((nss*as_t+ntt*at_t)/L+mt*(1 if rr==0 else F(1,L)))for nss,ntt,rr,L in zip(ns,nt,rs,Ls)])
As=np.array([float(s/5+t/2)for s,t in zip(svec,tvec)])
At=np.array([float(s/2+7*t/20)for s,t in zip(svec,tvec)])
v=np.ones(N+1)
for iteration in range(10000):
 nv=np.r_[Cs@v[:N]+bvec*v[N],max(As@v[:N],At@v[:N])+float(d)*v[N]]
 nv/=nv[-1]
 if max(abs(nv-v))<1e-13:v=nv;break
 v=nv
Tv=np.r_[Cs@v[:N]+bvec*v[N],max(As@v[:N],At@v[:N])+float(d)*v[N]]
q=max(Tv/v)
record=dict(short_types=N,short_max_length=12,tail_min_length=14,S_short=float(Ss),T_short=float(Ts),M4_short=float(m4short),S_tail_upper=float(st),T_tail_upper=float(tt),M4_tail_upper=float(mt),tail_to_tail_upper=float(d),long_to_short_straight_sum=float(sum(As)),long_to_short_turn_sum=float(sum(At)),short_to_tail_min=float(min(bvec)),short_to_tail_max=float(max(bvec)),nonlinear_perron_screen=q,comparison_weights=v.tolist(),active_tail_geometry='straight'if As@v[:N]>=At@v[:N]else'turn',iterations=iteration+1,notes='Floating screen. Finite C originates from exact rational enumeration but needs its source arithmetic recertified; full tail moments use audited upper rational caps. Source-label and boundary-height dependence are not yet included.')
np.savez_compressed(P/'short_tail_green_screen.npz',Cs=Cs,b=bvec,As=As,At=At,d=float(d),v=v,L=Larr)
(P/'short_tail_green_screen.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record,indent=2))
