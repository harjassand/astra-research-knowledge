"""Exact gluing of two overlapping cubic resonances and their quartets."""
from pathlib import Path
from fractions import Fraction as R
import sys,json,time
import numpy as np,scipy.linalg as la
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root/'outputs/quadratic_boundary'));import check_shape as m
start=time.perf_counter();raw=json.loads((root/'work/overlap_gluing_proposal.json').read_text());gd=json.loads((root/'outputs/graded_stabilization/certificate.json').read_text())
F,_,T=m.acquired();powers=gd['cubic_powers'];basis=[]
for v in gd['cubic_kernel_basis']:
    v=list(map(R,v));norm=sum(map(abs,v));basis.append([z/norm for z in v])
rays=[list(map(R,r)) for r in raw['rays']];weights=list(map(R,raw['weights']));targets=[list(map(R,v)) for v in raw['cubic_target_vectors']]
features=[]
for r,w in zip(rays,weights):
    for j in range(4):features.append([w*m.core.evaluate(m.core.diff({tuple(pw):R(1)},j),r) for pw in powers])
L=[[m.dot(v,col) for col in features] for v in basis];_,_,piv=la.qr(np.array(L,float),pivoting=True,mode='economic');piv=list(map(int,piv[:12]));free=[j for j in range(40) if j not in piv]
profiles=[]
for which in range(2):
    x0=np.array(raw['X' if which==0 else 'Y']).ravel();xx=[R(0)]*40
    for j in free:xx[j]=R(round(float(x0[j])*10**12),10**12)
    rhs=[m.dot(v,[row[which] for row in targets]) for v in basis];remaining=[co-sum(row[j]*xx[j] for j in free) for row,co in zip(L,rhs)]
    solution=m.linear_solve([[row[j] for j in piv] for row in L],remaining)
    for j,v in zip(piv,solution):xx[j]=v
    assert all(m.dot(row,xx)==co for row,co in zip(L,rhs));profiles.append([xx[4*i:4*i+4] for i in range(10)])
# Merge duplicate and proportional rank-one rays; the background averaging
# decreases their quadratic cost as a matrix, preserving both cubic targets.
groups={}
for i,(r,w) in enumerate(zip(rays,weights)):
    factor=r[0] if r[0] else r[3];key=tuple(v/factor for v in r);ww=w*factor*factor
    if key not in groups:groups[key]=[R(0),[R(0)]*4,[R(0)]*4]
    groups[key][0]+=ww
    for k in range(4):
        for j in range(2):groups[key][j+1][k]+=ww*profiles[j][i][k]
rays=list(map(list,groups));weights=[v[0] for v in groups.values()];XX=[[x/v[0] for x in v[1]] for v in groups.values()];YY=[[x/v[0] for x in v[2]] for v in groups.values()]
HF=[[m.core.diff(m.core.diff(F,i),j) for j in range(4)] for i in range(4)];cost=[[R(0) for _ in range(2)] for _ in range(2)]
for r,w,x,y in zip(rays,weights,XX,YY):
    H=[[m.core.evaluate(p,r) for p in row] for row in HF]
    for i,a in enumerate((x,y)):
        for j,b in enumerate((x,y)):cost[i][j]+=w*sum(a[k]*H[k][l]*b[l] for k in range(4) for l in range(4))/2
f0,fc,fs=map(R,raw['quartic_phase_coefficients']);t1=R(round(raw['t1']*10**10),10**10)+1;t2=R(round(raw['t2']*10**10),10**10)+1
cosine=[[t1-cost[0][0],fc/2-cost[0][1]],[fc/2-cost[1][0],t2-cost[1][1]]];sine=[[t1,fs/2],[fs/2,t2]];m.core.pd(cosine);m.core.pd(sine);gap=f0-t1-t2;assert gap>0
rad={tuple(row[:2]):R(row[2],row[3]) for row in raw['radial_phase_moments']};rad0=rad.get((0,0),0);radplus=2*rad.get((1,1),0);radminus=2*rad.get((1,-1),0);rc=radplus+radminus;rs=radminus-radplus
radmax=rad0+abs(rc)+abs(rs);assert gap>radmax/200
spatial=[[R(1),0],[0,R(1)],[R(1),R(1)],[R(2),R(1)]];eta=R(3,50);cross=[]
for n in spatial:
    H=[[m.core.evaluate(p,[*n,R(0),R(0)]) for p in row] for row in HF]
    for k in spatial:
        vv=[[k[0],k[1],0,0],[0,0,k[0],k[1]]];den=sum(v*v for v in n)*sum(v*v for v in k)
        mat=[[sum(vv[i][a]*H[a][b]*vv[j][b] for a in range(4) for b in range(4))/den for j in range(2)] for i in range(2)];m.core.pd([[v-(eta if i==j else 0) for j,v in enumerate(row)] for i,row in enumerate(mat)]);cross.append([[str(v) for v in row] for row in mat])
cert={'rays':[[str(v) for v in r] for r in rays],'weights':list(map(str,weights)),
  'X':[[str(v) for v in row] for row in XX],'Y':[[str(v) for v in row] for row in YY],
  'cubic_targets':[[str(v) for v in row] for row in targets],
  'quartic_phase_coefficients':list(map(str,[f0,fc,fs])),'cost_matrix':[[str(v) for v in row] for row in cost],
  'phase_budget_diagonal':list(map(str,[t1,t2])),'positive_cosine_matrix':[[str(v) for v in row] for row in cosine],
  'positive_sine_matrix':[[str(v) for v in row] for row in sine],'phase_uniform_budget':str(gap),
  'radial_phase_coefficients':list(map(str,[rad0,rc,rs])),'radial_upper_bound':str(radmax),
  'cross_matrices':cross,'cross_rank_one_lower_bound':'3/50','uniform_quartic_gap':'1/200','seconds':time.perf_counter()-start,
  'scope':'All phases, all means and overall amplitudes of the explicit overlapping four-wave block, universally over every ROC polynomial in the original face. Independent relative wave amplitudes are not classified.'}
(root/'outputs/resonant_gluing/overlap_certificate.json').write_text(json.dumps(cert,indent=2)+'\n')
print(json.dumps({'rank_one_rays':len(rays),'uniform_phase_budget_float':float(gap),'radial_upper_bound':str(radmax),'uniform_gap':'1/200','seconds':cert['seconds']},indent=2))
