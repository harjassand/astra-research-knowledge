"""Full opposite-cut search: all base matrices are optimized analytically.

The minimum eigenvector of a matrix difference supplies the base A. Five
remaining real parameters cover pairs of nonsingular directions modulo their
irrelevant scales and simultaneous left rotations. Numerical findings are
not accepted as exact obstructions until replayed separately.
"""
from pathlib import Path
import json,math,time
import numpy as np

HERE=Path(__file__).resolve().parent
E=np.array([[0,0,0,1],[0,0,-1,0],[0,-1,0,0],[1,0,0,0]],float)
D=np.diag([1,-1,1,-1]);I=np.eye(4)

def energy_data(v,beta,r):
    T=v@v;q=(v@E@v)/2;X=v@D@v
    dq=E@v;dx=2*D@v
    f=T*T+4*(r-1)*q*q+4*beta*q*X
    g=4*T*v+8*(r-1)*q*dq+4*beta*(X*dq+q*dx)
    h=4*T*I+8*np.outer(v,v)+8*(r-1)*(np.outer(dq,dq)+q*E)+4*beta*(X*E+2*q*D+np.outer(dq,dx)+np.outer(dx,dq))
    return f,g,h,q

def cut(v,beta,r):
    v=v/np.linalg.norm(v)
    f,g,h,q=energy_data(v,beta,r)
    return (h/2-np.outer(g,g)/(4*f))/q

def rot(t):return np.array([[math.cos(t),-math.sin(t)],[math.sin(t),math.cos(t)]])

def directions(p):
    zp,tp,am,zm,tm=map(float,p)
    zp=float(np.clip(zp,-4,4));zm=float(np.clip(zm,-4,4))
    plus=np.diag([math.exp(zp),math.exp(-zp)])@rot(tp)
    minus=rot(am)@np.diag([math.exp(zm),-math.exp(-zm)])@rot(tm)
    return plus.reshape(4),minus.reshape(4)

def objective(p,beta,r,detail=False):
    plus,minus=directions(p)
    mat=cut(plus,beta,r)-cut(minus,beta,r)
    if detail:
        vv,ww=np.linalg.eigh(mat);return float(vv[0]),ww[:,0],plus,minus
    return float(np.linalg.eigvalsh(mat)[0])

def nm(x0,beta,r,steps=450):
    n=len(x0);ss=np.array([x0]+[np.array(x0)+.07*np.eye(n)[i] for i in range(n)],float)
    ff=np.array([objective(x,beta,r) for x in ss])
    for _ in range(steps):
        ids=np.argsort(ff);ss=ss[ids];ff=ff[ids];mid=ss[:-1].mean(axis=0)
        refl=2*mid-ss[-1];fr=objective(refl,beta,r)
        if fr<ff[0]:
            ex=mid+2*(refl-mid);fe=objective(ex,beta,r)
            ss[-1],ff[-1]=(ex,fe) if fe<fr else (refl,fr)
        elif fr<ff[-2]:ss[-1],ff[-1]=refl,fr
        else:
            co=mid+.5*(ss[-1]-mid);fc=objective(co,beta,r)
            if fc<ff[-1]:ss[-1],ff[-1]=co,fc
            else:
                ss[1:]=ss[0]+.5*(ss[1:]-ss[0]);ff[1:]=[objective(x,beta,r) for x in ss[1:]]
        if np.max(np.abs(ss-ss[0]))<1e-8:break
    ii=int(np.argmin(ff));return ss[ii],float(ff[ii])

def run(tau,seed):
    beta=(1-3*tau*tau)/(1+3*tau*tau);r=4-12*tau/(1+3*tau*tau)
    rng=np.random.default_rng(seed)
    points=np.column_stack([rng.uniform(-2,2,800),rng.uniform(-math.pi,math.pi,800),
        rng.uniform(-math.pi,math.pi,800),rng.uniform(-2,2,800),rng.uniform(-math.pi,math.pi,800)])
    values=np.array([objective(x,beta,r) for x in points]);best=np.argsort(values)[:16]
    candidates=[nm(points[i],beta,r) for i in best]
    p,v=min(candidates,key=lambda xx:xx[1]);value,A,plus,minus=objective(p,beta,r,True)
    return {'tau':tau,'beta':beta,'r':r,'minimum_cut_matrix_eigenvalue':value,
            'parameters':list(map(float,p)),'A':list(map(float,A)),
            'Rplus':list(map(float,plus)),'Rminus':list(map(float,minus))}

if __name__=='__main__':
    start=time.time();ans=[]
    for tau in (1/30,1/6,1/5,1/4,.3):
        result=run(tau,6006);ans.append(result);print(json.dumps(result),flush=True)
    (HERE/'full_pc_search_result.json').write_text(json.dumps({'search':ans,'seconds':time.time()-start},indent=2)+'\n')
