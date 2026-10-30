"""Acquire exact universal gluing data from the numerical chart proposals."""
from pathlib import Path
from fractions import Fraction as R
import sys,json,time
import numpy as np,scipy.linalg as la,cvxpy as cp
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root/'outputs/quadratic_boundary'));import check_shape as m
start=time.perf_counter();out=root/'outputs/resonant_gluing';out.mkdir(exist_ok=True)
gd=json.loads((root/'outputs/graded_stabilization/certificate.json').read_text());proposal=json.loads((root/'work/triad_gluing_proposal.json').read_text())
F,_,T=m.acquired();powers=gd['cubic_powers'];basis=[]
for col in gd['cubic_kernel_basis']:
    v=list(map(R,col));norm=sum(map(abs,v));basis.append([z/norm for z in v])
rays=[[R(1),R(0),R(0),R(0)],[R(0),R(0),R(0),R(1)],[R(1)]*4]+[[R(1),t,t,t*t] for t in (R(-1),R(1,2),R(2))]
HF=[[m.core.diff(m.core.diff(F,i),j) for j in range(4)] for i in range(4)];HH=[[[m.core.evaluate(p,r) for p in row] for row in HF] for r in rays]
modes=[{'frequency':[1,0],'sine':['1','0']},{'frequency':[0,1],'sine':['0','1']},{'frequency':[1,1],'sine':['1','1']}];G=m.gradient(modes)
target=[m.average({tuple(pw):R(1)},G) for pw in powers]
features=[]
for r in rays:
    for j in range(4):features.append([m.core.evaluate(m.core.diff({tuple(pw):R(1)},j),r) for pw in powers])
L=[[m.dot(v,feature) for feature in features] for v in basis];rhs=[m.dot(v,target) for v in basis]
_,_,piv=la.qr(np.array(L,float),pivoting=True,mode='economic');piv=list(map(int,piv[:12]));free=[j for j in range(24) if j not in piv]
assert m.core.rank([[row[j] for j in piv] for row in L])==12
Fmat=[[R(0) for _ in range(3)] for _ in range(3)]
for i in range(3):Fmat[i][i]=R(3,8)*m.core.evaluate(F,rays[i])
for i,j in ((0,1),(0,2),(1,2)):Fmat[i][j]=Fmat[j][i]=sum(rays[j][a]*HH[i][a][b]*rays[j][b] for a in range(4) for b in range(4))/16
charts=[]
for prop in proposal['charts']:
    minimum=prop['minimum'];x0=np.array(prop['X']).ravel();xx=[R(0)]*24
    for j in free:xx[j]=R(round(float(x0[j])*10**12),10**12)
    remaining=[co-sum(row[j]*xx[j] for j in free) for row,co in zip(L,rhs)]
    sol=m.linear_solve([[row[j] for j in piv] for row in L],remaining)
    for j,v in zip(piv,sol):xx[j]=v
    assert all(m.dot(row,xx)==co for row,co in zip(L,rhs));X=[xx[4*i:4*i+4] for i in range(6)]
    energies=[sum(X[i][a]*HH[i][a][b]*X[i][b] for a in range(4) for b in range(4)) for i in range(6)]
    newenergy=9*energies[3]+R(9,16)*energies[4]+9*energies[5]
    D=[row[:] for row in Fmat]
    for i in range(3):
        j,k=[a for a in range(3) if a!=i];co=energies[i]+(newenergy if i==minimum else 0);D[j][k]-=co;D[k][j]-=co
    chart=[[R(int(i==j)) for j in range(3) if j!=minimum]+[R(1)] for i in range(3)]
    Dchart=[[sum(chart[i][a]*D[i][j]*chart[j][b] for i in range(3) for j in range(3)) for b in range(3)] for a in range(3)]
    gap=R(1,8);targetD=[[v-(gap if i==j else 0) for j,v in enumerate(row)] for i,row in enumerate(Dchart)]
    P=cp.Variable((3,3),symmetric=True);mu=cp.Variable();DN=np.array(targetD,float)
    problem=cp.Problem(cp.Maximize(mu),[P-mu*np.eye(3)>>0,DN-P>=mu*np.ones((3,3))])
    problem.solve(solver='CLARABEL',tol_gap_abs=1e-11,tol_feas=1e-11,tol_gap_rel=1e-11,max_iter=200)
    assert P.value is not None and mu.value>1e-6
    PP=[[R(round(float(P.value[i,j])*10**10),10**10) for j in range(3)] for i in range(3)]
    NN=[[targetD[i][j]-PP[i][j] for j in range(3)] for i in range(3)];m.core.pd(PP);assert all(v>=0 for row in NN for v in row)
    charts.append({'minimum':minimum,'X':[[str(v) for v in row] for row in X],
      'energy':[str(v) for v in energies],'positive_matrix':[[str(v) for v in row] for row in PP],
      'nonnegative_matrix':[[str(v) for v in row] for row in NN],
      'coefficient_projection_max_error':float(max(abs(float(v)-z) for v,z in zip(xx,x0)))})
    print('exact chart',minimum,'interior margin',mu.value,'projection',charts[-1]['coefficient_projection_max_error'],flush=True)
# A strict rank-one cross estimate on the three spatial wave rays, allowing
# arbitrary relative output rotations in different resonance-separated blocks.
spatial=[[R(1),R(0)],[R(0),R(1)],[R(1),R(1)]];eta=R(3,50)
cross=[]
for n in spatial:
    A0=[n[0],n[1],R(0),R(0)];H=[[m.core.evaluate(p,A0) for p in row] for row in HF]
    for k in spatial:
        vecs=[[k[0],k[1],R(0),R(0)],[R(0),R(0),k[0],k[1]]];den=sum(z*z for z in n)*sum(z*z for z in k)
        mat=[[sum(vecs[i][a]*H[a][b]*vecs[j][b] for a in range(4) for b in range(4))/den for j in range(2)] for i in range(2)]
        m.core.pd([[v-(eta if i==j else 0) for j,v in enumerate(row)] for i,row in enumerate(mat)]);cross.append([[str(v) for v in row] for row in mat])
cert={'rays':[[str(v) for v in r] for r in rays],'cubic_powers':powers,'cubic_moment_unit':list(map(str,target)),
  'charts':charts,'quartic_moment_matrix':[[str(v) for v in row] for row in Fmat],
  'chart_gap':'1/8','L4_comparison_bound':'25','uniform_L4_gap':'1/200',
  'cross_rank_one_lower_bound':str(eta),'cross_matrices':cross,'seconds':time.perf_counter()-start,
  'scope':'Universal gluing on arbitrary-amplitude, arbitrary-phase canonical triads and resonance-separated unions, for EVERY ROC polynomial over the acquired leading ray. Not global QC.'}
cert['resonance_detection_fields']=json.loads((root/'work/triad_gluing_resonance_rank.json').read_text())['fields']
(out/'certificate.json').write_text(json.dumps(cert,indent=2)+'\n');print('written',out/'certificate.json',flush=True)
