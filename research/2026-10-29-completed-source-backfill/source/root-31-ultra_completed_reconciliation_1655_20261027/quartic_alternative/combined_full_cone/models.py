"""Matched numerical acquisition models; exact reconstruction is separate."""
from itertools import combinations_with_replacement as cwr
from pathlib import Path
import time,json
import numpy as np
import scipy.sparse as sp
import cvxpy as cp
from maps import load,common_gaussian,ROOT


def symmetric(v,n):
    rr=[];cc=[];dd=[]
    for k,(i,j) in enumerate(cwr(range(n),2)):
        rr.append(i*n+j);cc.append(k);dd.append(1)
        if i!=j:rr.append(j*n+i);cc.append(k);dd.append(1)
    M=sp.coo_matrix((dd,(rr,cc)),shape=(n*n,len(list(cwr(range(n),2))))).tocsr()
    return cp.reshape(M@v,(n,n),order='C')


class Primal:
    def __init__(self,d,kind):
        self.d=d;self.kind=kind;self.p=cp.Parameter(9);self.rho=cp.Variable();self.eq=[];self.variables={}
        constraints=[]
        if kind in ['PC','combined']:
            v=cp.Variable(1840);Q=symmetric(v[:1830],60);self.variables['pc']=v
            h=cp.Variable(9) if kind=='combined' else cp.Constant(np.zeros(9))
            if kind=='combined':self.variables['h']=h
            self.eq.append(d['A']@v+d['B']@h==d['B']@self.p)
            constraints+=[Q-self.rho*np.eye(60)>>0]
        if kind in ['heat','combined']:
            r=cp.Variable(300);omega=cp.Variable(45);R=symmetric(r,24)
            self.variables.update(heat=r,omega=omega)
            if kind=='heat':
                gamma=cp.Variable(nonneg=True);self.variables['gamma']=gamma
                h=self.p-gamma*np.array([0,0,1,-1,0,0,0,0,0])
            self.eq.append(d['G']@r-d['E']@h-d['ON']@omega==0)
            constraints+=[R-self.rho*np.eye(24)>>0]
        constraints+=self.eq+[self.rho<=1]
        self.problem=cp.Problem(cp.Maximize(self.rho),constraints)
    def solve(self,p,save=None):
        start=time.monotonic();self.p.value=np.asarray(p,float)
        self.problem.solve(solver='CLARABEL',max_iter=160,tol_gap_abs=1e-8,tol_gap_rel=1e-8,tol_feas=1e-8)
        out={'status':'NUMERICAL_ONLY','model':self.kind,'solver_status':self.problem.status,
             'margin':None if self.rho.value is None else float(self.rho.value),
             'max_equality_residual':None if self.rho.value is None else max(float(np.max(np.abs(c.violation()))) for c in self.eq),
             'seconds':time.monotonic()-start,'input':list(map(float,p))}
        if save and self.rho.value is not None:
            np.savez(ROOT/(save+'.npz'),p=np.asarray(p),**{k:v.value for k,v in self.variables.items()},
                     **{f'dual_{i}':c.dual_value for i,c in enumerate(self.eq)},rho=self.rho.value)
            (ROOT/(save+'.json')).write_text(json.dumps(out,indent=2)+'\n')
        return out


class CommonDual:
    def __init__(self,d):
        self.d=d;self.p=cp.Parameter(9);self.lp=cp.Variable(658);self.lh=cp.Variable(210)
        self.g=d['B'].T@self.lp
        Mp=cp.reshape(self.lp[d['pc_indices']],(60,60),order='C')
        Mh=cp.reshape(self.lh[d['heat_indices']],(24,24),order='C')
        constraints=[Mp>>0,Mh>>0,d['A'][:,1830:].T@self.lp==0,d['ON'].T@self.lh==0,
                     self.g==d['E'].T@self.lh,cp.trace(Mp)+cp.trace(Mh)==1]
        self.problem=cp.Problem(cp.Minimize(self.p@self.g),constraints)
    def solve(self,p):
        self.p.value=np.asarray(p,float);start=time.monotonic()
        self.problem.solve(solver='CLARABEL',max_iter=160,tol_gap_abs=1e-9,tol_gap_rel=1e-9,tol_feas=1e-9)
        return {'value':float(self.problem.value),'g':self.g.value.copy(),
                'lp':self.lp.value.copy(),'lh':self.lh.value.copy(),'seconds':time.monotonic()-start}


class Acoustic:
    def __init__(self,d,epsilon=1e-3):
        self.g=cp.Parameter(9);self.v=cp.Variable(15);self.epsilon=epsilon
        self.matrix=sum(self.v[i]*d['Q'][i] for i in range(15))
        self.problem=cp.Problem(cp.Minimize(self.g@self.v[:9]),
                                [self.matrix>>epsilon*np.eye(8),cp.trace(self.matrix)==1])
    def solve(self,g):
        self.g.value=np.asarray(g,float);start=time.monotonic()
        self.problem.solve(solver='CLARABEL',max_iter=120,tol_gap_abs=1e-10,tol_gap_rel=1e-10,tol_feas=1e-10)
        return {'value':float(self.problem.value),'v':self.v.value.copy(),
                'min_eigenvalue':float(np.linalg.eigvalsh(self.matrix.value)[0]),'seconds':time.monotonic()-start}


def controls():
    d=load();common_gaussian(d)
    norm=np.array([1,1,2,0,0,0,0,0,0]);dm=np.array([1,1,2,0,0,0,-2.2,-2.2,0])
    output=[]
    for kind,p,name in [('PC',norm,'control_norm_PC'),('PC',dm,'control_DM_PC'),
                        ('heat',dm,'control_DM_heat'),('combined',dm,'control_DM_combined')]:
        result=Primal(d,kind).solve(p,name);output.append(result);print(json.dumps(result),flush=True)
    (ROOT/'CONTROLS.json').write_text(json.dumps(output,indent=2)+'\n')


if __name__=='__main__':controls()
