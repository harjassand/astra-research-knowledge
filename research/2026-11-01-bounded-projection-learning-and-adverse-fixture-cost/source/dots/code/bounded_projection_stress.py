"""Exact rational small-QP diagnostic ONLY; no new full receiver implementation.

Hidden vectors appear only in this audit. All scalar means are adversarial-error
emulations, not sampled episodes. Exhaustive active-face optimization is only a
small-dimensional diagnostic, not the proposed polynomial production solver.
"""
from fractions import Fraction as F
from itertools import combinations, product
from receiver import mm,mv,transpose,inverse,quad,psd,sqrt_upper,required_shots

def dot(x,y):return sum((a*b for a,b in zip(x,y)),F(0))
def qp(A,k,B):
    n=len(k); candidates=[]
    c=mv(inverse(A),k)
    if sum(map(abs,c))<=B:candidates.append(c)
    for size in range(1,n+1):
        for support in combinations(range(n),size):
            for signs in product((-1,1),repeat=size):
                matrix=[[A[i][j] for j in support]+[F(signs[h])] for h,i in enumerate(support)]
                matrix.append([F(s) for s in signs]+[F(0)])
                sol=mv(inverse(matrix),[k[i] for i in support]+[F(B)])
                if any(s*x<0 for s,x in zip(signs,sol)):continue
                c=[F(0)]*n
                for i,x in zip(support,sol):c[i]=x
                candidates.append(c)
    c=min(candidates,key=lambda x:quad(A,x)-2*dot(k,x))
    grad=[2*(a-b) for a,b in zip(mv(A,c),k)]
    gap=dot(grad,c)+B*max(map(abs,grad))
    assert gap==0, ('exact optimum diagnostic failed',gap)
    return c,gap

def main():
    H=4; eps=F(1,4);lam=eps/(128*H**4)
    t=F(1,10**12);c=(1-t*t)/(1+t*t);s=2*t/(1+t*t)
    ops={'r':[[c,-s],[s,c]],'R':[[c,s],[-s,c]],'b':[[F(0),F(1)],[F(1),F(0)]]}
    adj={'r':'R','R':'r','b':'b'};states={():[F(1),F(0)]}
    def state(w):
        if w not in states:states[w]=mv(ops[w[-1]],state(w[:-1]))
        return states[w]
    words=[(),('r',),('b',)];m=len(words);B=m;b=4
    alpha=lam/(128*(b+4)*b*b);cache={};jobs=[]
    W=sum(len(ops)**j for j in range(H+1));W1=1+len(ops)*W
    Nmax=(W.bit_length()+1)*(W1*W1+1);beta=F(1,100)/(W+1)**64
    shots=required_shots(alpha,beta/Nmax)
    def mean(u,v):
        key=tuple(sorted((u,v)))
        if key not in cache:
            truth=dot(state(u),state(v))
            estimate=max(F(-1),min(F(1),truth+(-1 if len(cache)%2 else 1)*alpha/3))
            assert abs(estimate-truth)<=alpha
            cache[key]=estimate;jobs.append((key,truth,estimate))
        return cache[key]
    G=[[mean(u,v) for v in words] for u in words]
    A=[[G[i][j]+(m*alpha if i==j else 0) for j in range(m)] for i in range(m)]
    assert psd(A,strict=True)
    K={a:[[mean(u,v+(a,)) for v in words] for u in words] for a in ops}
    HH={a:[[mean(u+(a,),v+(a,)) for v in words] for u in words] for a in ops}
    def project(a,d):return qp(A,mv(K[a],d),B)[0]
    def trajectory(w):
        cs=[[F(1),F(0),F(0)]];norms=[]
        for a in w:
            d=cs[-1];z=project(a,d)
            rad=quad(HH[a],d)-2*dot(z,mv(K[a],d))+quad(G,z)+4*B*B*alpha
            assert rad>=0
            norms.append(sqrt_upper(rad,eps/(128*H*H*(B+1))))
            cs.append(z)
        return cs,norms
    certificates=[]
    for w in [('r','b','r','b'),('b','R','b'),('r','r','r','r'),('b','b')]:
        forward,R=trajectory(w);backward,S=trajectory(tuple(adj[a] for a in reversed(w)))
        output=dot(G[0],forward[-1]);l=len(w)
        for i,a in enumerate(w,1):
            residual_cross=[x-y for x,y in zip(mv(K[a],forward[i-1]),mv(G,forward[i]))]
            output+=dot(backward[l-i],residual_cross)
        cert=(B+2*l*B*B)*alpha+sum((R[i-1]*sum(S[:l-i],F(0)) for i in range(1,l+1)),F(0))
        truth=state(w)[0]
        assert abs(output-truth)<=cert<=eps
        certificates.append((w,float(abs(output-truth)),float(cert)))
    determinant=1-dot(state(()),state(('r',)))**2
    assert 0<determinant<alpha**2
    # A genuinely far prefix gives a measured convex-distance witness, no inverse Gram.
    A1=[[mean((),())+alpha]];k1=[mean((),('b',))]
    z,gap=qp(A1,k1,1)
    empirical=quad(A1,z)-2*dot(z,k1)+mean(('b',),('b',))
    lower=empirical-gap-5*alpha
    assert lower>lam/2
    print('PASS: exact rational active-face QP has zero FW gap in every diagnostic solve')
    print('PASS: near-collinear physical Gram determinant =',determinant)
    print('Entry alpha =',alpha,'; determinant < alpha^2; no determinant-based calibration')
    for row in certificates:print('word, true error, outward certificate:',row)
    print('PASS: far-prefix convex-distance lower witness > lambda/2')
    print('Validated emulated means:',len(jobs),'physical episodes: 0')
    print('Theoretical UNEXECUTED calibrated episodes:',len(jobs)*shots)
    print('Not a full online receiver test; enumerated QP solver is a small-instance diagnostic only')

if __name__=='__main__':main()
