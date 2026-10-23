"""One independent exact-rational full-tree check; not an asymptotic proof."""
from fractions import Fraction as F
from math import isqrt, factorial
from pathlib import Path
import argparse, json, time

def square_root(x):
    a,b=isqrt(x.numerator),isqrt(x.denominator)
    assert a*a==x.numerator and b*b==x.denominator
    return F(a,b)

parser=argparse.ArgumentParser()
parser.add_argument('--output',type=Path,default=Path(__file__).with_suffix('.json'))
args=parser.parse_args()
started=time.perf_counter(); cpu_started=time.process_time()
D,m,n=4,2,16
alpha=beta=F(1,2); b=F(3,5); z=F(1,64); p=F(1,64)
labels=[()]
for i in range(1,m+1):
    labels.extend([t+(k,) for t in labels.copy() if len(t)==i-1 for k in range(D)])
labels.append('star'); N=len(labels); star=N-1
level=[len(t) if t!='star' else m+1 for t in labels]
q=[b*z**i/D**i for i in level[:-1]]
pi=[p*F(1,n**(2*(m-i)))/D**i for i in level[:-1]]
q.append(1-sum(q));pi.append(1-sum(pi))
assert all(x>0 for x in q+pi)
Q=[[F(0) for _ in labels] for _ in labels]
for x,t in enumerate(labels[:-1]):
    if len(t)<m:
        for k in range(D):
            y=labels.index(t+(k,)); Q[x][y]=Q[y][x]=F(1,D+1)
for x in range(N):Q[x][x]=1-sum(Q[x])
assert all(sum(row)==1 for row in Q)
assert all(Q[x][y]==Q[y][x] for x in range(N) for y in range(N))
W=[pi[x]/q[x] for x in range(N)]
# Exact KL<1 certificate: nonterminal tree weights are below one, while
# log(W_leaf)<5 and log(pi_star/q_star)<93/100. These logarithm bounds
# follow from finite positive exponential-series sums, not floating logs.
assert all(W[x]<1 for x in range(N-1) if level[x]<m)
assert pi[star]<F(197,200) and q[star]>F(39,100)
assert sum(F(93,100)**k/factorial(k) for k in range(7))>F(197,78)
assert W[partitions_m_index := next(x for x in range(N) if level[x]==m)]==F(320,3)
assert F(8,3)**5>F(320,3)  # e>1+1+1/2+1/6=8/3.
kl_upper=F(197,200)*F(93,100)+5*p
assert kl_upper<1
G=[[F(0) for _ in labels] for _ in labels]
L=[[F(0) for _ in labels] for _ in labels]
for x in range(N):
    for y in range(N):
        if x==y:continue
        G[x][y]=q[y]*min(1,W[y]/W[x])
        if Q[x][y]:
            r=square_root(q[y]/q[x])
            L[x][y]=Q[x][y]*min(1,r)*min(1,(pi[y]/pi[x])/r)
    G[x][x]=1-sum(G[x]);L[x][x]=1-sum(L[x])
C=[[(F(x==y)+alpha*G[x][y]+beta*L[x][y])/2 for y in range(N)] for x in range(N)]
assert all(sum(row)==1 for row in C)
assert all(pi[x]*C[x][y]==pi[y]*C[y][x] for x in range(N) for y in range(N))
partitions=[[x for x in range(N) if level[x]==i] for i in range(m+2)]
bar=[]
for i,B in enumerate(partitions):
    rows=[[sum(C[x][y] for y in A) for A in partitions] for x in B]
    assert all(row==rows[0] for row in rows)
    bar.append(rows[0])
ql=[sum(q[x] for x in B) for B in partitions]
pil=[sum(pi[x] for x in B) for B in partitions]
assert all(pil[i]*bar[i][j]==pil[j]*bar[j][i] for i in range(m+2) for j in range(m+2))
s=square_root(z/D); f=beta*F(D,2*(D+1))*s
for x in range(N-1):
    i=level[x]
    if i<m:
        assert sum(beta*L[x][y]/2 for y in partitions[i+1])==f
    if i>0:
        assert sum(beta*L[x][y]/2 for y in partitions[i-1])==f/n**2
leaf_exit=alpha*(1-p)/(2*W[partitions[m][0]])+f/n**2
assert all(sum(C[x][y] for y in range(N) if y not in partitions[m])==leaf_exit for x in partitions[m])
# Compare the full and genuinely lumped laws, exact at a fixed nonasymptotic horizon.
u=q[:];v=ql[:]
for _ in range(12):
    u=[sum(u[x]*C[x][y] for x in range(N)) for y in range(N)]
    v=[sum(v[x]*bar[x][y] for x in range(m+2)) for y in range(m+2)]
assert [sum(u[x] for x in B) for B in partitions]==v
# Transitivity plus uniform q within each level preserves per-level uniformity.
assert all(all(u[x]==u[B[0]] for x in B) for B in partitions)
full_tv=sum(abs(u[x]-pi[x]) for x in range(N))/2
lump_tv=sum(abs(v[i]-pil[i]) for i in range(m+2))/2
assert full_tv==lump_tv
out={
 'purpose':'Independent exact finite check of aggregation, multiplicity factor, full-law preservation and KL<1 via rational exponential-series bounds; no asymptotic extrapolation.',
 'parameters':{'D':D,'m':m,'n_label':n,'b':str(b),'z':str(z),'p':str(p),'eta':'1/2','alpha':str(alpha)},
 'full_states':N,'lumped_states':m+2,'checked_horizon':12,
 'labels':[list(t) if t!='star' else 'star' for t in labels],
 'q':[str(x) for x in q],'pi':[str(x) for x in pi],
 'lumped_q':[str(x) for x in ql],'lumped_pi':[str(x) for x in pil],
 'lumped_C':[[str(x) for x in row] for row in bar],
 'screen':str(s),'marked_forward':str(f),'marked_reverse':str(f/n**2),
 'reverse_acceptance':'D*n^-2*s', 'leaf_set_exit':str(leaf_exit),
 'exact_KL_upper':str(kl_upper),
 'exact_full_tv_at_horizon':str(full_tv),
 'all_checks_passed':True,
 'wall_seconds':time.perf_counter()-started,'cpu_seconds':time.process_time()-cpu_started
}
args.output.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['full_states','lumped_states','checked_horizon','screen','marked_forward','marked_reverse','leaf_set_exit','all_checks_passed','wall_seconds','cpu_seconds']},indent=2))
