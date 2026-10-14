"""Exploratory heat-flow SOS feasibility. No numerical output is a theorem."""
import sympy as sp
import numpy as np
import scipy.linalg as la
import itertools,time,os
BASE=os.path.dirname(__file__)

def build():
    a=sp.symbols('a b c d'); h=sp.symbols('h0:6'); vs=a+h
    pairsA=list(itertools.combinations_with_replacement(range(4),2))
    pairsH=list(itertools.combinations_with_replacement(range(6),2))
    def exp_pair(pair,n):
        e=[0]*n
        for i in pair:e[i]+=1
        return tuple(e)
    monoms=[exp_pair(x,4)+exp_pair(y,6) for x in pairsA for y in pairsH]
    idx={e:i for i,e in enumerate(monoms)}
    def vec(poly):
        v=np.zeros(len(monoms))
        for e,c in sp.Poly(sp.expand(poly),*vs).terms():
            if c:v[idx[e]]=float(c)
        return v
    X=sp.Matrix(a); B1=sp.Matrix([h[0],h[1],h[3],h[4]]);B2=sp.Matrix([h[1],h[2],h[4],h[5]])
    u=a[0]**2+a[2]**2;v=a[1]**2+a[3]**2;w=a[0]*a[1]+a[2]*a[3];q=a[0]*a[3]-a[1]*a[2]
    basis=[u*u,v*v,u*v,w*w,u*w,v*w,q*u,q*v,q*w]
    energies=np.stack([vec((B1.T*sp.hessian(f,a)*B1+B2.T*sp.hessian(f,a)*B2)[0]) for f in basis],axis=1)
    alphas=[];nv=[]
    for exps in itertools.combinations_with_replacement(range(4),3):
        poly=sp.prod(a[i] for i in exps)
        for j in range(4):
            da=sp.Matrix([sp.diff(poly,x) for x in a])
            cor=(da.dot(B1))*B2[j]-(da.dot(B2))*B1[j]
            alphas.append((exps,j));nv.append(vec(cor))
    N=np.stack(nv,axis=1)
    ij=list(itertools.combinations_with_replacement(range(24),2))
    T=np.zeros((210,len(ij)))
    for k,(i,j) in enumerate(ij):
        e=exp_pair([i//6,j//6],4)+exp_pair([i%6,j%6],6)
        T[idx[e],k]=1 if i==j else np.sqrt(2)
    U,s,Vh=la.svd(N,full_matrices=True);rank=np.sum(s>1e-9);P=U[:,rank:].T
    B=P@T
    U2,s2,Vh2=la.svd(B,full_matrices=False);rank2=np.sum(s2>1e-9)
    U2=U2[:,:rank2];s2=s2[:rank2];R=Vh2[:rank2]
    np.savez(BASE+'/heat_matrices.npz',N=N,T=T,E=energies,P=P,U=U2,s=s2,R=R,ij=np.array(ij),alphas=np.array([(tuple(x)+(j,)) for x,j in alphas]))
    print('ranks',rank,rank2,'nullGram',len(ij)-rank2,flush=True)

def solve(p,maxiter=10000,tol=1e-9,margin=0.0,verbose=False):
    z=np.load(BASE+'/heat_matrices.npz');R=z['R'];ij=z['ij'];n=24
    I=np.eye(n);i,j=ij.T;sf=np.where(i==j,1,np.sqrt(2))
    def smat(v):
        G=np.zeros((n,n));G[i,j]=v/sf;G[j,i]=v/sf;return G
    def svec(G):return G[i,j]*sf
    rhs=z['P']@z['E']@np.asarray(p)
    g0=R.T@((z['U'].T@rhs)/z['s'])
    def aff(g):return g+g0-R.T@(R@g)
    def psd(g):
        val,V=la.eigh(smat(g),check_finite=False)
        return svec((V*np.maximum(val,margin))@V.T)
    x=g0.copy();hist=[]
    for k in range(maxiter):
        y=psd(x);w=aff(2*y-x);x+=w-y
        if k%100==0 or k==maxiter-1:
            gg=aff(y);ev=la.eigvalsh(smat(gg),check_finite=False)[0]
            res=np.linalg.norm(gg-y)
            hist.append([k,float(ev),float(res)])
            if verbose and k%1000==0:print(k,ev,res,flush=True)
            if res<tol:break
    G=smat(aff(y));c=la.lstsq(z['N'],z['T']@svec(G)-z['E']@p)[0]
    error=np.max(np.abs(z['T']@svec(G)-z['E']@p-z['N']@c))
    return G,c,hist,error
if __name__=='__main__':
    if not os.path.exists(BASE+'/heat_matrices.npz'):build()
    for name,p in [('norm4',[1,1,2,0,0,0,0,0,0]),('Fstar',[1,1,3.5,.5,0,0,-2.9,-2.9,0])]:
        t=time.time();G,c,hist,err=solve(np.array(p),margin=1e-4,verbose=True)
        print(name,'time',time.time()-t,'last',hist[-1],'error',err,flush=True)
        np.savez(BASE+'/heat_'+name+'.npz',G=G,c=c,hist=hist,error=err,p=p)
