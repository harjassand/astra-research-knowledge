#!/usr/bin/env python3
import json,itertools
from pathlib import Path
from fractions import Fraction as F
import numpy as np
from branch_recovery_v1 import P,from_ptm,to_ptm,herm
HERE=Path(__file__).parent;Q=HERE.parent
# Exact inverse-probability-free moment calculation on the sharp fixture.
p=F(1,5);maps=[]
M=[[F(int(a==b))*(1-p) for b in range(4)] for a in range(4)];maps.append(M)
for sign in [1,-1]:
 M=[[F(0) for _ in range(4)] for _ in range(4)];M[0][0]=p/2;M[0][3]=sign*p/2;maps.append(M)
est=[[[F(0) for _ in range(4)] for _ in range(4)] for _ in maps];mass=F(0)
for j,u,k,v,s in itertools.product(range(1,4),[-1,1],range(1,4),[-1,1],range(3)):
 M=maps[s];prob=(M[0][0]+u*M[0][j]+v*M[k][0]+u*v*M[k][j])/36
 assert prob>=0;mass+=prob
 est[s][0][0]+=prob;est[s][0][j]+=3*u*prob;est[s][k][0]+=3*v*prob;est[s][k][j]+=9*u*v*prob
assert mass==1 and est==maps
# Generic random Kraus checks for spin-flip unitalization.
rng=np.random.default_rng(202610282303);worst=0.;low=1.;trres=0.
for _ in range(200):
 Z=rng.normal(size=(8,2))+1j*rng.normal(size=(8,2));V,_=np.linalg.qr(Z);Ks=V.reshape(4,2,2)
 D=np.array([[sum(np.trace(P[a]@K@P[b]@K.conj().T).real/2 for K in Ks) for b in range(4)] for a in range(4)])
 flip=[P[2]@K.conj()@P[2] for K in Ks]
 Df=np.array([[sum(np.trace(P[a]@K@P[b]@K.conj().T).real/2 for K in flip) for b in range(4)] for a in range(4)])
 D0=(D+Df)/2;worst=max(worst,float(np.max(abs(D0[1:,0]))),float(np.max(abs(D0[1:,1:]-D[1:,1:]))));low=min(low,float(np.linalg.eigvalsh(from_ptm(D0))[0]));trres=max(trres,float(np.max(abs(D0[0]-[1,0,0,0]))))
 assert np.max(abs(D0[1:,0]))<1e-12 and np.max(abs(D0[1:,1:]-D[1:,1:]))<1e-12 and np.linalg.eigvalsh(from_ptm(D0))[0]>-1e-12
src=json.loads((Q/'continuous_inverse_control_20261028/endpoint_instrument_v1.json').read_text());L=sum(float(np.linalg.norm(np.array(M)[0,1:])) for M in src['branch_PTMs'].values())
out={'status':'PASS_EXACT_MOMENTS_AND_NUMERICAL_SPIN_FLIP_CHECKS','exact_fixture_moment_entries':48,'exact_total_trial_mass':str(mass),'record_squared_norm':100,'random_channels':200,'unitalization_max_error':worst,'unitalized_Choi_min_eigenvalue':low,'TP_max_error':trres,'actual_record_dependence_L':L,'actual_nonunital_advantage_cap':L/4,'scope':'Moment checks exact rational. Random/source checks floating, not interval certified.'}
(HERE/'mechanism_check_v1.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
