from sympy import Matrix, symbols, sqrt, Rational as R, simplify, factor, eye
from itertools import product, combinations
a,b,r,t=symbols('a b r t',real=True)
bs=list(product([-1,0,1],repeat=3)); idx={x:i for i,x in enumerate(bs)}
D=Matrix.zeros(27)
for state,i in idx.items():
    mA,mB,mC=state
    q=lambda m:a if m==0 else b
    D[i,i]=(3*q(mA)+q(mB)+q(mC))/5+r*mA*(mB+mC)
    for who in [1,2]:
        for shift in [-1,1]:
            state2=list(state);state2[0]+=shift;state2[who]-=shift
            state2=tuple(state2)
            if state2 in idx: D[idx[state2],i]+=1
assert D==D.T
blocks=[]
for M in [3,2,1,0]:
    states=[q for q in bs if sum(q)==M]
    for parity in [1,-1]:
        seen=set();vecs=[]
        for state in states:
            if state in seen: continue
            other=(state[0],state[2],state[1]);seen.update([state,other])
            if state==other:
                if parity<0: continue
                v=Matrix.zeros(27,1);v[idx[state]]=1
            else:
                v=Matrix.zeros(27,1);v[idx[state]]=1/sqrt(2);v[idx[other]]=parity/sqrt(2)
            vecs.append(v)
        if not vecs: continue
        S=Matrix.hstack(*vecs);B=simplify(S.T*D*S)
        assert simplify(S.T*S)==eye(S.cols)
        if M==0:
            refl=Matrix(27,27,lambda i,j:1 if bs[i]==tuple(-m for m in bs[j]) else 0)
            Rf=simplify(S.T*refl*S)
            for sign in [1,-1]:
                basis=(Rf-sign*eye(Rf.rows)).nullspace()
                if not basis: continue
                orth=[]
                for v in basis:
                    for u in orth: v=simplify(v-(u.T*v)[0]*u)
                    v=simplify(v/sqrt((v.T*v)[0]));orth.append(v)
                H=Matrix.hstack(*orth);C=simplify(H.T*B*H)
                blocks.append((f'M{M}_swap{parity}_flip{sign}',C))
        else: blocks.append((f'M{M}_swap{parity}',B))
assert sum(B.rows*(1 if name.startswith('M0_') else 2) for name,B in blocks)==27
for name,B in blocks:print(name,B)

regimes={'low':(R(34,9),t*t+R(13,9)), 'mid':(t*t-4*t+6,2*t*t+1),'high':(2,2*t*t+1)}
for regime,(aa,bb) in regimes.items():
    print('REGIME',regime)
    for name,B in blocks:
        C=B.subs({a:aa,b:bb,r:t*t})
        leading=[factor(C[:k,:k].det()) for k in range(1,C.rows+1)]
        print(name,leading)
