"""Propose a counted triplet transfer mode using exact physical end spins.

This file only uses float64 SU(2) recoupling for discovery. The independent
integer/CRT producer and interval consumer certify the same physical input.
"""
import pathlib,json,time,functools
import numpy as np
import scipy.linalg as la
from fugacity_messages import blocks,paths,racah,ROOT

@functools.lru_cache(None)
def swaps(n,total):
    sub=[p for p in paths(n) if p[-1]==total]
    out=[]
    from sympy.physics.wigner import wigner_6j
    for edge in range(n-1):
        mat=np.zeros((len(sub),len(sub))); groups={}
        for i,p in enumerate(sub):
            groups.setdefault(p[:edge+1]+p[edge+2:],[]).append((i,p))
        for group in groups.values():
            ids=[i for i,p in group];a=group[0][1][edge];d=group[0][1][edge+2]
            es=tuple(p[edge+1]for i,p in group)
            fs=[f for f in range(5)if abs(a-f)<=d<=a+f]
            u=np.array([[float(wigner_6j(a,2,e,2,d,f))*np.sqrt((2*e+1)*(2*f+1))for f in fs]for e in es])
            mat[np.ix_(ids,ids)]=(u*np.array([(-1)**f for f in fs]))@u.T
        out.append(mat)
    return out

@functools.lru_cache(None)
def correlation_edges(edges):
    n=len(edges)+1
    ans=0.0
    for total,bs in blocks(n):
        h=np.tensordot(edges,bs,axes=1)
        es,us=la.eigh(h,check_finite=False,overwrite_a=True)
        # Move the rightmost physical spin to position1 while preserving0.
        # Conjugation of h01 then produces h0,n-1.
        q=bs[0].copy()
        for edge in range(1,n-1):
            swap=swaps(n,total)[edge]
            q=swap@q@swap
        diagonal=np.sum(us*(q@us),axis=0)
        ans+=(2*total+1)*np.dot(diagonal,np.exp(-es))
    return -ans/3

def correlation(n,beta):return correlation_edges((beta,)*(n-1))

def enriched(beta,rs=(.6,.8,1.,1.2,1.4)):
    messages=[(r,d)for r in rs for d in [0,1]]
    mats=[]
    for shift in [0,1,2]:
        mat=np.zeros((len(messages),len(messages)))
        for i,(r,d)in enumerate(messages):
            for j,(s,e)in enumerate(messages[:i+1]):
                power=d+e+shift
                edges=(beta*r*s,)if power==0 else (beta*r,)+(beta,)*(power-1)+(beta*s,)
                mat[i,j]=mat[j,i]=(-1)**power*correlation_edges(edges)/5**power
        mats.append(mat)
    g,h,h2=mats;scale=1/np.sqrt(np.diag(g))
    g=scale[:,None]*g*scale[None,:];h=scale[:,None]*h*scale[None,:];h2=scale[:,None]*h2*scale[None,:]
    vals,vecs=la.eigh(g);keep=vals>1e-10*vals[-1];q=vecs[:,keep]/np.sqrt(vals[keep])
    es,us=la.eigh(q.T@h@q);c=q@us[:,-1]
    theta=c@h@c/(c@g@c);var=c@h2@c/(c@g@c)-theta**2
    return {'beta':beta,'messages':messages,'candidate_coefficients':(c*scale).tolist(),
            'retained_rank':int(sum(keep)),'Gram_eigenvalues_scaled':vals.tolist(),
            'Ritz_spectrum_minus_J':es.tolist(),
            'theta_minus_J':float(theta),'variance_J':float(var),
            'scope':'ENRICHED_NUMERICAL_DISCOVERY_ONLY'}

def propose(beta):
    moments=[correlation(n,beta)/5**(n-2) for n in range(2,7)]
    # f_alpha transforms in spin1. Use -K/5 so the AF branch is positive.
    signed=np.array([(-1)**r*x for r,x in enumerate(moments)])
    g=np.array([[signed[i+j]for j in range(2)]for i in range(2)])
    h=np.array([[signed[i+j+1]for j in range(2)]for i in range(2)])
    h2=np.array([[signed[i+j+2]for j in range(2)]for i in range(2)])
    es,us=la.eigh(h,g);c=us[:,-1];c/=max(abs(c))
    theta=c@h@c/(c@g@c);var=c@h2@c/(c@g@c)-theta**2
    return {'beta':beta,'physical_end_spin_moments':moments,
            'candidate_coefficients':c.tolist(),'theta_minus_J':float(theta),
            'variance_J':float(var),'scope':'NUMERICAL_DISCOVERY_ONLY'}

def main():
    start=time.monotonic();rows=[]
    for beta in [.75,1.5]:
        row=enriched(beta);rows.append(row);print(row,flush=True)
    result={'rows':rows,'seconds':time.monotonic()-start}
    (ROOT/'results/triplet_enriched_discovery.json').write_text(json.dumps(result,indent=2)+'\n')

if __name__=='__main__':main()
