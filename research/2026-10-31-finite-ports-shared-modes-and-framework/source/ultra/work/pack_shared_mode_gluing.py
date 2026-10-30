"""Reconstruct rational sources and positive remainder identities."""
from pathlib import Path
from fractions import Fraction as R
import importlib.util,json,time
import numpy as np,scipy.linalg as la,cvxpy as cp
root=Path(__file__).resolve().parents[1];out=root/'outputs/shared_mode_gluing'
spec=importlib.util.spec_from_file_location('shared_receiver',out/'receive.py');r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
start=time.perf_counter();data=r.setup();proposal=json.loads((root/'work/shared_mode_radial_proposal.json').read_text());charts=[]
for case in proposal['charts']:
    bi=case['base'];L=r.features(data,bi);norms=[sum(map(abs,v)) for v in data['basis']];LN=[[v/norm for v in row] for row,norm in zip(L,norms)];profiles=[]
    for e,x0 in enumerate(case['X']):
        allowed=list(range(24 if e==bi else 28));A=[[row[j] for j in allowed] for row in LN]
        _,_,piv=la.qr(np.array(A,float),pivoting=True,mode='economic');piv=[allowed[int(j)] for j in piv[:12]];free=[j for j in allowed if j not in piv]
        assert r.b.rank([[row[j] for j in piv] for row in LN])==12
        xx=[R(0)]*28;x0=np.array(x0).ravel()
        for j in free:xx[j]=R(round(float(x0[j])*10**12),10**12)
        rhs=[r.dot(v,[row[e] for row in data['targets']])/norm for v,norm in zip(data['basis'],norms)]
        rr=[co-sum(row[j]*xx[j] for j in free) for row,co in zip(LN,rhs)]
        sol=r.m.linear_solve([[row[j] for j in piv] for row in LN],rr)
        for j,v in zip(piv,sol):xx[j]=v
        assert all(r.dot(row,xx)==co for row,co in zip(LN,rhs));profiles.append([xx[4*i:4*i+4] for i in range(7)])
    exact={'order':case['order'],'base':bi,'minimum':case['minimum'],'tau':str(R(str(case['tau']))),'epsilon':str(R(str(case['epsilon']))),'young_parameters':[str(R(round(row[0]*10**10),10**10)) for row in case['young']]}
    D,energies=r.residual(data,exact,profiles);DC=r.congruence(D,r.chart_matrix(exact['order']));DN=np.array(DC,float)
    P=cp.Variable((4,4),symmetric=True);mu=cp.Variable();problem=cp.Problem(cp.Maximize(mu),[P-mu*np.eye(4)>>0,DN-P>=mu*np.ones((4,4))]);problem.solve(solver='CLARABEL',tol_feas=1e-11,tol_gap_abs=1e-11,tol_gap_rel=1e-11,max_iter=300)
    assert P.value is not None and mu.value>1e-7,(case['order'],problem.status,mu.value)
    PP=[[R(round(float(P.value[i,j])*10**10),10**10) for j in range(4)] for i in range(4)];NN=[[DC[i][j]-PP[i][j] for j in range(4)] for i in range(4)];r.b.pd(PP);assert all(v>=0 for row in NN for v in row)
    exact.update({'sources':[[list(map(str,row)) for row in X] for X in profiles],'positive_matrix':[list(map(str,row)) for row in PP],'nonnegative_matrix':[list(map(str,row)) for row in NN]});charts.append(exact)
    print(tuple(exact['order']),'exact positive margin',mu.value,flush=True)
cert={'uniform_single_block_L4_gap':'1/32','quartic_pair_matrix':[list(map(str,row)) for row in data['FM']],'quartet_coefficients':list(map(str,[data['u'],data['v']])),'cubic_targets':[list(map(str,row)) for row in data['targets']],'radial_upper_matrix':[list(map(str,row)) for row in data['TU']],'charts':charts,'generation':'Numerical proposals followed by rational free-variable rounding, exact cubic projection, and exact positive remainder identities. The receiver uses no numerical solver.','scope':'All four real relative amplitudes and all phases of the stated overlapping network; not full-face QC.'}
(out/'certificate.json').write_text(json.dumps(cert,indent=2)+'\n');print('seconds',time.perf_counter()-start,'bytes',(out/'certificate.json').stat().st_size,flush=True)
