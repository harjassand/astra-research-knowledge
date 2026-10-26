"""Independent checks of Q63's capacity anchor, transients and noise claims.

No candidate scientific routines are imported. The only imported local helpers
are this reviewer's earlier Fraction elimination and exact square root.
"""
from fractions import Fraction as F
from pathlib import Path
import csv
import json
import math
import random

import numpy as np
from independent_checks import invert, fsqrt

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
FROZEN = ROOT/'review_material/Q63/stage2'


def rational_recover(y,n,t):
    r = [[F(0)]*n for _ in range(n)]
    r[0][0] = y[0]
    pos = 1
    for i in range(1,n):
        d1,d2 = y[0]-y[pos],y[0]-y[pos+1]
        p = (2*d1-d2)/(2*t*(d2-d1))
        a = fsqrt(d1*(1+t*p)/t)
        r[i][i],r[0][i],r[i][0] = p,a,a
        pos += 2
    for i in range(1,n):
        for j in range(i+1,n):
            a,c,p,q = r[0][i],r[0][j],r[i][i],r[j][j]
            loss = y[0]-y[pos]
            u,v = 1+t*p,1+t*q
            const = (a*a*v+c*c*u)/t-loss*u*v/t**2
            root = (a*c-fsqrt(a*a*c*c-loss*const))/loss
            assert 0 < root <= min(a*q/c,c*p/a)
            r[i][j]=r[j][i]=root
            pos += 1
    return invert(r)


def exact_capacity_anchor():
    rng = random.Random(632026)
    count = 0
    for n in range(2,8):
        for dense in (False,True):
            k = [[F(i==j)*rng.randint(1,4) for j in range(n)] for i in range(n)]
            for i in range(n):
                for j in range(i+1,n):
                    if dense or j==i+1:
                        w = F(rng.randint(1,5),rng.randint(1,3))
                        k[i][i]+=w; k[j][j]+=w
                        k[i][j]=k[j][i]=-w
            c = [F(rng.randint(1,5),rng.randint(1,4)) for _ in range(n)]
            scale = [F(1)]+[F(rng.randint(1,5),rng.randint(1,5)) for _ in range(n-1)]
            h = [v*v for v in scale]
            t,s1,s2 = F(2,3),F(1,3),F(5,2)
            commands = [[F(0)]*n]
            for i in range(1,n):
                for amp in (t,2*t):
                    d=[F(0)]*n;d[i]=amp;commands.append(d)
            for i in range(1,n):
                for j in range(i+1,n):
                    d=[F(0)]*n;d[i]=d[j]=t;commands.append(d)
            bs=[]
            for s in (s1,s2):
                y=[]
                for d in commands:
                    mat = [[k[i][j]+(s*c[i]+h[i]*d[i] if i==j else 0)
                            for j in range(n)] for i in range(n)]
                    y.append(invert(mat)[0][0])
                bs.append(rational_recover(y,n,t))
            b1,b2=bs
            assert all(b2[i][j]==b1[i][j] for i in range(n) for j in range(n) if i!=j)
            recovered_h=[(s2-s1)*c[i]/(b2[i][i]-b1[i][i]) for i in range(n)]
            assert recovered_h==h
            roots=[fsqrt(v) for v in recovered_h]
            recovered_k=[[roots[i]*b1[i][j]*roots[j]-(s1*c[i] if i==j else 0)
                          for j in range(n)] for i in range(n)]
            assert recovered_k==k
            count+=1
    return {'new_exact_cases':count,'n_range':[2,7],'command_amplitude':'2/3',
            'real_Laplace_points':['1/3','5/2'],'K_and_gains_exact':True}


def positive_exponential(m,dt):
    # Nonnegative uniformization series with a conservative absolute tail bound.
    rate=max(1.,float(np.max(-np.diag(m))))
    p=np.eye(len(m))+m/rate
    assert p.min()>=0
    term=np.eye(len(m)); total=term.copy()
    theta=rate*dt; normp=float(np.max(np.sum(p,axis=1)))
    scale=math.exp(-theta)
    for j in range(1,1000):
        term=np.einsum('ik,kj->ij',term,p,optimize=False)*(theta/j)
        total+=term
        ratio=theta*normp/(j+1)
        if ratio<1:
            tail=scale*float(np.max(np.sum(term,axis=1)))*ratio/(1-ratio)
            if tail<1e-45:
                return scale*total
    raise RuntimeError('positive exponential failed to converge')


def operator(k,c,schedule,dt):
    n=len(k);steps=len(schedule);fault=n-1
    state=np.zeros((2*n,steps));out=np.zeros((steps,steps));cache={}
    for i,d in enumerate(schedule):
        key=tuple(d)
        if key not in cache:
            aug=np.zeros((2*n+1,2*n+1))
            kp=k.copy();kp[fault,fault]+=1
            aug[:n,:n]=-(k+np.diag(d))/c[:,None]
            aug[n:2*n,n:2*n]=-(kp+np.diag(d))/c[:,None]
            aug[fault,n+fault]=1/c[fault]
            aug[n,-1]=1/c[0]
            e=positive_exponential(aug,dt)
            cache[key]=(e[:2*n,:2*n],e[:2*n,-1])
        a,b=cache[key]
        state=np.einsum('ik,kj->ij',a,state,optimize=False)
        state[:,i]+=b
        out[i]=state[0]
    return out


def transient_checks():
    raw=json.loads((FROZEN/'transient_data.json').read_text())
    checks=[]
    for f in raw:
        k=np.array(f['K']);c=np.array(f['C_diagonal']);n=len(k)
        saved=np.array(f['unloaded_operator'])
        zero=np.zeros((len(saved),n))
        own=operator(k,c,zero,.5)
        relative=math.sqrt(float(np.sum((own-saved)**2)/np.sum(saved**2)))
        assert relative<1e-10
        loaded=operator(k,c,np.array(f['best_tested_loaded_schedule']),.5)
        assert np.all(loaded<=own*(1+2e-11))
        gain0=float(np.linalg.svd(own,compute_uv=False)[0])
        gain1=float(np.linalg.svd(loaded,compute_uv=False)[0])
        assert gain1<=gain0*(1+2e-11)
        checks.append({'n':n,'relative_operator_difference_from_positive_series':relative,
                       'unloaded_gain':gain0,'best_saved_schedule_gain_ratio':gain1/gain0})
    return checks


def covariance_cost(q,reverse):
    if abs(q)<1e-3:
        return sum(((-1.)**i)*(i-1 if reverse else 1)/i*q**i for i in range(2,16))
    return math.log1p(q)-q/(1+q) if reverse else q-math.log1p(q)


def noise_checks():
    fixtures=json.loads((FROZEN/'withheld_networks.json').read_text())
    maxratio=[0.,0.]; count=0
    for f in fixtures:
        k=np.array(f['K']);n=len(k)
        def infos(load):
            r=np.linalg.inv(k+np.diag(load))
            diff=r[0,-1]**2/(1+r[-1,-1]);f0=r[0,0];f1=f0-diff
            result=[]
            for a,nu in ((1.,0.),(0.,1.),(.01,.1)):
                v0,v1=a+nu*f0,a+nu*f1
                q=nu*diff/v1
                result.append((.5*(covariance_cost(q,False)+diff*diff/v1),
                               .5*(covariance_cost(q,True)+diff*diff/v0)))
            return result
        baseline=infos(np.zeros(n))
        for load in f['loads']:
            for pair,base in zip(infos(np.array(load)),baseline):
                for direction in (0,1):
                    ratio=pair[direction]/base[direction]
                    assert ratio<=1+2e-10
                    maxratio[direction]=max(maxratio[direction],ratio)
                    count+=1
    return {'Gaussian_KL_direction_checks':count,'maximum_forward_reverse_ratios':maxratio}


if __name__=='__main__':
    result={'capacity_anchor':exact_capacity_anchor(),
            'independent_transients':transient_checks(),'quasistatic_noise':noise_checks()}
    (HERE/'independent_stage2_q63_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
