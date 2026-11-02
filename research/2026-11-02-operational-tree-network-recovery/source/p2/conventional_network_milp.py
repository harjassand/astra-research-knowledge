"""Conventional SAME-PROBLEM mixed integer linear formulation for general
connected grounded nonlinear resistor networks with unknown monotone edge laws.

Finite set interpolation is encoded by pairwise disjunctions; finite *valid*
big-M constants follow from a grounded Laplacian energy/voltage bound.
SciPy/HiGHS is a numerical conventional comparator, not an exact arithmetic
certificate; failed/incomplete runs are never evidence of hardness.
"""
import numpy as np
from scipy import sparse
from scipy.optimize import milp, LinearConstraint, Bounds
from itertools import combinations


def formulation(nodes,edges,ground,terminals,p_hist,observations,p_task,alpha,beta,objective_port):
    """edges [(u,v)] oriented u->v, current variable positive v->u.
    nodes arbitrary node labels, terminals list excludes ground. p_hist injections
    and p_task indexed by terminals; observations {(h,terminal): (value, tol)}.
    """
    others=[n for n in nodes if n!=ground];nd=len(others);E=len(edges)
    H=len(p_hist)+1; nold=len(p_hist)
    assert objective_port in terminals
    D=np.zeros((E,nd),float)
    for e,(u,v) in enumerate(edges):
        if u!=ground:D[e,others.index(u)]-=1
        if v!=ground:D[e,others.index(v)]+=1
    L=D.T@D
    eig=np.linalg.eigvalsh(L)
    assert eig[0]>0
    aa=np.broadcast_to(alpha,(E,)).astype(float)
    bb=np.broadcast_to(beta,(E,)).astype(float)
    assert np.all(aa>0)&np.all(bb>=aa)
    p_all=np.r_[np.array(p_hist).reshape(-1,len(terminals)),np.array(p_task).reshape(1,-1)]
    pmat=np.zeros((H,nd),float)
    for i,t in enumerate(terminals):pmat[:,others.index(t)]=p_all[:,i]
    V=max(.01,float(np.max(np.linalg.norm(pmat,axis=1)))/(np.min(aa)*eig[0]))*1.02
    # Variable ordering: v[h,n], j[h,e], binary z[e,h,k], each pair includes anchor 0.
    nv=H*nd;nj=H*E
    pids=[(a,b) for a in range(H+1) for b in range(a+1,H+1)]
    nbin=E*len(pids)
    full=nv+nj+nbin
    ci=np.zeros(full);ci[(H-1)*nd+others.index(objective_port)]=1.
    lb=np.r_[np.full(nv,-V),np.repeat(-2*bb*V,H).reshape(H,E).ravel(),np.zeros(nbin)]
    ub=np.r_[np.full(nv,V),np.repeat(2*bb*V,H).reshape(H,E).ravel(),np.ones(nbin)]
    # Explanation: repeat(E-vector,H) is not row-major tiling; fix below.
    lb[nv:nv+nj]=np.tile(-2*bb*V,H)
    ub[nv:nv+nj]=np.tile(2*bb*V,H)
    integ=np.r_[np.zeros(nv+nj),np.ones(nbin)]
    rows=[]; lower=[]; upper=[]
    def add(d,lo=-np.inf,hi=np.inf):rows.append(d);lower.append(lo);upper.append(hi)
    def vid(h,n):return h*nd+n
    def jid(h,e):return nv+h*E+e
    def zid(e,k):return nv+nj+e*len(pids)+k
    def svec(h,e):
        if h<0:return {}
        return {vid(h,n):D[e,n] for n in range(nd) if D[e,n]!=0}
    def jvec(h,e):return {} if h<0 else {jid(h,e):1.}
    def combine(*parts):
        out={}
        for coef,vec in parts:
            for k,v in vec.items():out[k]=out.get(k,0.)+coef*v
        return {k:v for k,v in out.items() if abs(v)>1e-12}
    for h in range(H):
        for n in range(nd):
            row={jid(h,e):D[e,n] for e in range(E) if D[e,n]}
            add(row,lo=pmat[h,n],hi=pmat[h,n])
    for (h,t),(val,tol) in observations.items():
        add({vid(h,others.index(t)):1.},lo=val-tol,hi=val+tol)
    for e in range(E):
        for k,(a,b) in enumerate(pids):
            h0=a-1;h1=b-1 # index0=zero anchor; 1..H = actual observed/task
            ds=combine((1.,svec(h1,e)),(-1.,svec(h0,e)))
            dj=combine((1.,jvec(h1,e)),(-1.,jvec(h0,e)))
            z=zid(e,k)
            Ms=4*V+1e-10
            Mg=8*bb[e]*V+1e-10
            # z=1 ds>=0, slope in [a,b]; z=0 ds<=0, slope reversed.
            # -ds <= Ms(1-z) => -ds+Ms z <= Ms.
            add(combine((-1.,ds),(Ms,{z:1.})),hi=Ms)
            # ds <= Ms z -> ds -Ms z<=0
            add(combine((1.,ds),(-Ms,{z:1.})),hi=0.)
            # alpha*ds-dj <= Mg(1-z)
            add(combine((aa[e],ds),(-1.,dj),(Mg,{z:1.})),hi=Mg)
            # dj-beta*ds <= Mg(1-z)
            add(combine((1.,dj),(-bb[e],ds),(Mg,{z:1.})),hi=Mg)
            # beta*ds-dj <= Mg*z
            add(combine((bb[e],ds),(-1.,dj),(-Mg,{z:1.})),hi=0.)
            # dj-alpha*ds <= Mg*z
            add(combine((1.,dj),(-aa[e],ds),(-Mg,{z:1.})),hi=0.)
    rr=[];cc=[];vv=[]
    for i,row in enumerate(rows):
        for j,val in row.items():rr.append(i);cc.append(j);vv.append(val)
    A=sparse.coo_matrix((vv,(rr,cc)),shape=(len(rows),full)).tocsr()
    return {'objective':ci,'integrality':integ,'bounds':Bounds(lb,ub),
            'constraints':LinearConstraint(A,np.array(lower),np.array(upper)),
            'meta':{'nodes':nd,'edges':E,'snapshots':H,'binaries':nbin,'rows':len(rows),'voltage_bound':V,
                    'non_ground':others,'D':D}}


def solve(form,seconds=30):
    c=form['objective']; sols=[]
    for direction in (+1,-1):
        r=milp(direction*c,integrality=form['integrality'],bounds=form['bounds'],
               constraints=form['constraints'],options={'time_limit':seconds,'mip_rel_gap':1e-10})
        vals= None if r.x is None else float(c@r.x)
        sols.append((direction,vals,r))
    return sols

if __name__=='__main__':
    edges=[(0,1),(1,2),(1,3)]
    ns=[0,1,2,3]
    p_old=np.array([[.2,.2]])
    p_future=np.array([.2,.4])
    f=formulation(ns,edges,0,[2,3],p_old,{(0,2):(.3,0.),(0,3):(.3,0.)},p_future,1.,5.,2)
    print('STAR conventional mixed integer model', {k:v for k,v in f['meta'].items() if k not in ('D','non_ground')})
    for direction,val,r in solve(f):
        print('sense',direction,'output',val,'status',r.status,'gap',getattr(r,'mip_gap',None),'nodes',getattr(r,'mip_node_count',None))
    # Cyclic diamond, additional bypass edge, true source linear for simple data.
    edges2=[(0,1),(1,2),(1,3),(2,4),(3,4),(1,4)]
    # known linear identity phi(j)=.5 j => p = D^T j, v=.5 inv(D^T D) p.
    nds=[0,1,2,3,4]
    D=np.zeros((6,4))
    for e,(u,v) in enumerate(edges2):
        if u:D[e,u-1]-=1
        if v:D[e,v-1]+=1
    terminals=[2,3,4]
    p_obs=np.array([[.3,.2,.1],[.2,.1,.3]])
    oldv=[]
    for p in p_obs:
        p0=np.zeros(4);p0[[1,2,3]]=p
        oldv.append(.5*np.linalg.solve(D.T@D,p0))
    ob={(h,t):(oldv[h][t-1],1e-5) for h in range(2) for t in terminals}
    f2=formulation(nds,edges2,0,terminals,p_obs,ob,np.array([.15,.17,.24]),1.,5.,2)
    print('CYCLE conventional MILP', {k:v for k,v in f2['meta'].items() if k not in ('D','non_ground')})
    for direction,val,r in solve(f2,seconds=12):
        print('sense',direction,'output',val,'status',r.status,'gap',getattr(r,'mip_gap',None),'nodes',getattr(r,'mip_node_count',None))
