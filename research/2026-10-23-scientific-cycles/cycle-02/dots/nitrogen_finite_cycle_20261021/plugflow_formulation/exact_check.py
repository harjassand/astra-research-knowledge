#!/usr/bin/env python3
"""Exact rational finite-volume isothermal header conservation diagnostic.
No chemical trajectory, momentum solution, or performance prediction.
"""
from fractions import Fraction as Q
import json, time, resource, hashlib
from pathlib import Path
start=time.perf_counter()
V=list(map(Q,['1/50','3/100','1/20'])); VH=sum(V)
W=list(map(Q,[2,1,3])); RT=Q(10)
u=list(map(Q,[-7,11,3])); h=[a+RT for a in u]
X=[[Q(1,2),Q(1,3),Q(1,6)],[Q(1,4),Q(1,4),Q(1,2)],[Q(1,5),Q(3,5),Q(1,5)]]
XL=[Q(1,3)]*3; XR=[Q(1,10),Q(1,5),Q(7,10)]
def dot(a,b): return sum(x*y for x,y in zip(a,b))
def enc(x):
 if isinstance(x,Q): return {'exact':str(x),'float':float(x)}
 if isinstance(x,list): return [enc(y) for y in x]
 if isinstance(x,dict): return {k:enc(v) for k,v in x.items()}
 return x

def case(name,FL,FR,r):
 FL,FR=Q(FL),Q(FR); r=list(map(Q,r))
 omega=[[-a,2*a,Q(0)] for a in r]
 D=(FL-FR+dot(V,r))/VH
 F=[FL]
 for v,s in zip(V,r): F.append(F[-1]+v*(s-D))
 assert F[-1]==FR
 donors=[XL if F[0]>=0 else X[0]]
 donors += [X[k-1] if F[k]>=0 else X[k] for k in range(1,3)]
 donors += [X[-1] if F[-1]>=0 else XR]
 flux=[[f*x for x in d] for f,d in zip(F,donors)]
 dc=[[(flux[j][i]-flux[j+1][i])/V[j]+omega[j][i] for i in range(3)] for j in range(3)]
 assert all(sum(a)==D for a in dc)
 assert all(dot(W,a)==0 for a in omega)
 store=[sum(V[j]*dc[j][i] for j in range(3)) for i in range(3)]
 src=[sum(V[j]*omega[j][i] for j in range(3)) for i in range(3)]
 assert store==[flux[0][i]-flux[-1][i]+src[i] for i in range(3)]
 mass_boundary=dot(W,flux[0])-dot(W,flux[-1])
 assert dot(W,store)==mass_boundary
 H=[dot(h,a) for a in flux]
 Udot=[V[j]*dot(u,dc[j]) for j in range(3)]
 heat=[Udot[j]-H[j]+H[j+1] for j in range(3)]
 assert sum(Udot)==H[0]-H[-1]+sum(heat)
 positive=sum(max(a,Q(0)) for a in heat); removed=sum(max(-a,Q(0)) for a in heat)
 assert sum(heat)==positive-removed
 # Deliberately wrong pressure term, fixed-MW conversion, and constant-face flows.
 extra_pdot_residual=VH*RT*D
 fixed_W=Q(2); fixed_MW_error=fixed_W*(FL-FR)-mass_boundary
 wrong_D=[(FL-FR)/VH+s for s in r] # constant divergence shortcut
 return dict(name=name,V=V,F=F,source_molar=r,D=D,Pdot=RT*D,donors=donors,
             dc=dc,species_storage=store,mass_boundary=mass_boundary,Udot=Udot,
             heat=heat,heat_positive=positive,heat_removed=removed,
             wrong_extra_VPdot_energy_residual=extra_pdot_residual,
             wrong_fixed_molecular_weight_mass_error=fixed_MW_error,
             wrong_uniform_divergence_breaks_pressure=any(a!=D for a in wrong_D),
             exact_conservation_pass=True)
cases=[case('forward','3','2',['2','1','3']),
       case('reverse','-2','-3',['1','4','2']),
       case('internal_flow_reversal','1/100','1/100',['3','-4','1'])]
assert cases[1]['donors'][-1]==XR
assert any(a<0 for a in cases[2]['F']) and any(a>0 for a in cases[2]['F'])
assert all(c['wrong_extra_VPdot_energy_residual']!=0 for c in cases)
assert all(c['wrong_fixed_molecular_weight_mass_error']!=0 for c in cases)
assert all(c['wrong_uniform_divergence_breaks_pressure'] for c in cases)
assert any(c['heat_positive']>0 and c['heat_removed']>0 for c in cases)
# Exact equal-composition redistribution: preserve total species, mass and U.
c0=[Q(3),Q(2),Q(1)]
N0=[VH*a for a in c0]; Nsplit=[sum(v*a for v in V) for a in c0]
assert N0==Nsplit and dot(W,N0)==dot(W,Nsplit) and dot(u,N0)==dot(u,Nsplit)
out={'scope':'Exact algebra diagnostic, not trajectory or realizability proof',
     'cases':cases,'redistribution_pass':True,'molar_internal_energies':u,
     'molar_enthalpies':h,'molecular_weights':W,'runtime_seconds':time.perf_counter()-start,
     'ru_maxrss_KiB_linux':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
     'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
Path(__file__).with_name('exact_receipt.json').write_text(json.dumps(enc(out),indent=2)+'\n')
print(json.dumps({'passed':True,'cases':len(cases),'runtime_seconds':out['runtime_seconds'],'ru_maxrss_KiB_linux':out['ru_maxrss_KiB_linux']}))
