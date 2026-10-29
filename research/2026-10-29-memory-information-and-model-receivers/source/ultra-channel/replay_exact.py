"""Separate Fraction-only finite consumer. Imports no producer or SymPy.

Checks the declared algebraic receivers; it is not an independent scientific audit.
"""
from fractions import Fraction as Q
import hashlib,json
from pathlib import Path
from time import perf_counter

HERE=Path(__file__).resolve().parent

def tr(p):
    p=list(p)
    while len(p)>1 and p[-1]==0:p.pop()
    return p or [Q(0)]
def add(a,b):
    return tr([(a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0) for i in range(max(len(a),len(b)))])
def sc(a,c):return tr([v*c for v in a])
def mul(a,b):
    z=[Q(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):z[i+j]+=x*y
    return tr(z)
def power(a,n):
    z=[Q(1)]
    for _ in range(n):z=mul(z,a)
    return z
def div(a,b):
    a=tr(a);b=tr(b);out=[Q(0)]*max(1,len(a)-len(b)+1)
    while a!=[0] and len(a)>=len(b):
        k=len(a)-len(b);z=a[-1]/b[-1];out[k]+=z
        a=add(a,[Q(0)]*k+sc(b,-z))
    return tr(out),tr(a)
def deriv(a):return tr([i*a[i] for i in range(1,len(a))])
def ev(a,x):
    v=Q(0)
    for c in reversed(a):v=v*x+c
    return v
def sig(x):return (x>0)-(x<0)
def sig0(a):return next((sig(x) for x in a if x),0)
def variation(a):
    a=[x for x in a if x]
    return sum(x!=y for x,y in zip(a,a[1:]))
def pol(a):return tr([Q(x) for x in reversed(a)])
def gcd(a,b):
    while b!=[0]:a,b=b,div(a,b)[1]
    return sc(a,1/a[-1])

def rows(d,name):return [{int(i):Q(x) for i,x in r.items()} for r in d[name]]
def poles(d):
    out={}
    for sign,name in [(-1,'P'),(1,'Q')]:
        for r in rows(d,name):
            if len(r)==2:
                i,j=sorted(r);a,b=r[i],r[j]
                z=out.setdefault((i,j),{});z[a/b]=z.get(a/b,Q(0))+sign*a
    return {e:{r:c for r,c in z.items() if c} for e,z in out.items()}

def check_order(d,rec):
    n=d['n']
    for name in ['P','Q']:
        rr=rows(d,name)
        assert all(all(x>0 for x in r.values()) and len(r)<=2 for r in rr)
        assert all(sum(r.get(i,0) for r in rr)==1 for i in range(n))
    pp=poles(d)
    assert len(pp)==rec['support_edges']
    for er in rec['edges']:
        edge=tuple(er['edge']);z=pp[edge]
        assert sorted(z.items())==[(Q(r),Q(c)) for r,c in er['poles']]
        D=[Q(1)]
        for r in z:D=mul(D,[r,Q(1)])
        N=[Q(0)]
        for r,c in z.items():
            quotient,rem=div(D,[r,Q(1)]);assert rem==[0]
            N=add(N,sc(quotient,c))
        assert D==pol(er['denominator']) and N==pol(er['numerator'])
        assert all(c>=0 for c in D) and D[0]>0
        if er['zero']:
            assert N==[0] and er['nonnegative'];continue
        fac=[Q(er['content'])];odd_roots=0
        for f in er['factors']:
            a=pol(f['factor']);assert gcd(a,deriv(a))==[1]
            fac=mul(fac,power(a,f['multiplicity']))
            chain=list(map(pol,f['chain']))
            assert chain[0]==a and chain[1]==deriv(a)
            for j in range(2,len(chain)):
                assert chain[j]==sc(div(chain[j-2],chain[j-1])[1],-1)
            assert div(chain[-2],chain[-1])[1]==[0]
            v0=variation([sig0(a) for a in chain]);vi=variation([sig(a[-1]) for a in chain])
            assert (v0,vi,v0-vi)==(f['variation_zero_plus'],f['variation_infinity'],f['positive_roots'])
            if f['multiplicity']%2:odd_roots+=v0-vi
        assert fac==N
        ok=sig0(N)>0 and odd_roots==0
        assert ok==er['nonnegative']
        if not ok:
            t=Q(er['negative_t']);assert t>0 and ev(N,t)/ev(D,t)==Q(er['negative_kernel'])<0
    w=rec['failure_witness']
    if w is not None:
        p=list(map(Q,w['p']));h=list(map(Q,w['h']))
        assert min(p)>0 and sum(p)==1 and sum(h)==0
        def fisher(name):
            return sum(sum(c*h[i] for i,c in r.items())**2/sum(c*p[i] for i,c in r.items()) for r in rows(d,name))
        a,b=fisher('P'),fisher('Q')
        assert (a,b,a-b)==(Q(w['gP']),Q(w['gQ']),Q(w['gap'])) and a<b
    assert rec['complete_order']==all(e['nonnegative'] for e in rec['edges'])

def ga(a,b=0):return (Q(a),Q(b))
def plus(a,b):return (a[0]+b[0],a[1]+b[1])
def times(a,b):return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def neg(a):return (-a[0],-a[1])
def conj(a):return (a[0],-a[1])
def zero():return [[ga(0) for _ in range(2)] for _ in range(2)]
def eye():return [[ga(int(i==j)) for j in range(2)] for i in range(2)]
def ma(A,B):return [[plus(x,y) for x,y in zip(a,b)] for a,b in zip(A,B)]
def ms(A,c):return [[times(x,ga(c)) for x in a] for a in A]
def mm(A,B):return [[plus(times(A[i][0],B[0][j]),times(A[i][1],B[1][j])) for j in range(2)] for i in range(2)]
def mt(A):return plus(A[0][0],A[1][1])
def real(z):assert z[1]==0;return z[0]
def loadM(A):return [[ga(*x) for x in row] for row in A]
def pd(A):
    assert A[0][0][1]==A[1][1][1]==0 and A[0][1]==conj(A[1][0])
    assert A[0][0][0]>0 and real(plus(times(A[0][0],A[1][1]),neg(times(A[0][1],A[1][0]))))>0
def solve(A,b):
    A=[list(r)+[v] for r,v in zip(A,b)];n=len(A)
    for k in range(n):
        j=next(j for j in range(k,n) if A[j][k]);A[k],A[j]=A[j],A[k]
        p=A[k][k];A[k]=[x/p for x in A[k]]
        for j in range(n):
            if j!=k:
                c=A[j][k];A[j]=[x-c*y for x,y in zip(A[j],A[k])]
    return [r[-1] for r in A]
def vec(A):return [real(A[0][0]),real(A[1][1]),A[0][1][0],A[0][1][1]]
def maddsum(A):
    z=zero()
    for a in A:z=ma(z,a)
    return z

def check_quantum(ch,qr,nb):
    M=list(map(loadM,qr['primitive']));E=list(map(loadM,qr['E']));F=list(map(loadM,qr['F']))
    lo,hi=map(Q,nb['input_contract']['primitive_bounds'])
    for A in M:pd(ma(A,ms(eye(),-lo)));pd(ma(ms(eye(),hi),ms(A,-1)))
    assert maddsum(M)==eye()
    coords=[[vec(A)[i] for A in M] for i in range(4)]
    for r,e in zip(rows(ch,'P'),E):assert e==maddsum([ms(M[i],v) for i,v in r.items()])
    for r,f in zip(rows(ch,'Q'),F):assert f==maddsum([ms(M[i],v) for i,v in r.items()])
    for source in (E,F):
        assert maddsum(source)==eye()
        for A in source:pd(A)
    D=ma(loadM(qr['rho_plus']),ms(eye(),Q(-1,2)))
    pd(loadM(qr['rho_plus']));pd(loadM(qr['rho_minus']))
    assert real(mt(loadM(qr['rho_plus'])))==real(mt(loadM(qr['rho_minus'])))==1
    signed=[real(mt(mm(A,D))) for A in M]
    assert signed==[Q(1,16),Q(-1,16),Q(0),Q(0)]
    succ=[]
    for name,source in [('E',E),('F',F)]:
        scores=[real(mt(mm(A,D))) for A in source]
        assert scores==list(map(Q,qr['binary_guessing'][name]['scores']))
        prob=(1+sum(map(abs,scores)))/2
        assert prob==Q(qr['binary_guessing'][name]['guess_success']);succ.append(prob)
    assert succ[1]-succ[0]==Q(1,640)
    eta,tau=Q(nb['eta']),Q(nb['effect_opnorm_radius'])
    # Actual arbitrary coherent query, independently solve its primitive coordinates.
    for name,base in [('E',E),('F',F)]:
        cand=list(map(loadM,nb['candidate'][name]['effects']));assert maddsum(cand)==eye()
        for j,(A,B) in enumerate(zip(cand,base)):
            pd(A);coef=solve(coords,vec(A));old=solve(coords,vec(B))
            assert coef==list(map(Q,nb['candidate'][name]['primitive_coefficients'][j]))
            assert max(abs(a-b) for a,b in zip(coef,old))<=eta
            diff=ma(A,ms(B,-1))
            assert diff==zero() or mm(diff,diff)==ms(eye(),tau*tau)
        prob=(1+sum(abs(real(mt(mm(A,D)))) for A in cand))/2
        assert prob==Q(nb['candidate_guessing'][name])
    assert Q(nb['candidate_guessing_reversal'])>0

def check_neighbourhood(ch,order,nb):
    n=4;m,M=map(Q,nb['input_contract']['primitive_bounds']);delta=Q(nb['input_contract']['delta']);lam=Q(nb['input_contract']['graph_lambda'])
    for er in order['edges']:
        D,N=pol(er['denominator']),pol(er['numerator'])
        quo,rem=div(D,[Q(1),Q(1)]);assert rem==[0]
        assert add(N,sc(quo,-delta))==[Q(4,25),Q(-8,25),Q(4,25)]
    L=[[Q(0) for _ in range(4)] for _ in range(4)]
    for i,j in [(0,1),(1,2),(2,3)]:L[i][i]+=1;L[j][j]+=1;L[i][j]-=1;L[j][i]-=1
    C=[[1,0,0],[0,1,0],[0,0,1],[-1,-1,-1]]
    B=[[L[i][j]-lam*(Q(int(i==j))-Q(1,4)) for j in range(4)] for i in range(4)]
    A=[[sum(C[i][a]*B[i][j]*C[j][b] for i in range(4) for j in range(4)) for b in range(3)] for a in range(3)]
    assert A==[list(map(Q,r)) for r in nb['graph_restricted_matrix']]
    piv=[]
    for k in range(3):
        p=A[k][k];assert p>0;piv.append(p)
        for i in range(k+1,3):
            for j in range(k+1,3):A[i][j]-=A[i][k]*A[k][j]/p
    assert piv==list(map(Q,nb['graph_LDL_pivots']))
    alpha=delta*m*lam/(2*M*M);assert alpha==Q(nb['alpha'])==Q(1,300)
    eta=Q(nb['eta']);K=Q(0)
    for name in ['P','Q']:
        for r in rows(ch,name):
            mass=sum(r.values());assert eta<=m*mass/2
            K+=4*2/m+2*n/(m*mass)+2/(m*m)
    assert K==Q(nb['K']) and K*eta==Q(nb['K_eta'])<alpha/2
    assert alpha-K*eta==Q(nb['remaining_coercivity'])
    assert Q(nb['uniform_guessing_reversal_lower'])==Q(1,640)-23*eta/16>0

def main():
    start=perf_counter()
    ch=json.loads((HERE/'CHANNELS.json').read_text());syn=json.loads((HERE/'SYNTHESIS.json').read_text());nb=json.loads((HERE/'NEIGHBOURHOOD.json').read_text())
    assert hashlib.sha256((HERE/'CHANNELS.json').read_bytes()).hexdigest()==nb['source_channels_sha256']
    assert hashlib.sha256((HERE/'SYNTHESIS.json').read_bytes()).hexdigest()==nb['synthesis_sha256']
    check_order(ch,syn['ordered_source'])
    check_order(dict(n=ch['n'],P=ch['Q'],Q=ch['P']),syn['reversed_same_source'])
    check_neighbourhood(ch,syn['ordered_source'],nb)
    check_quantum(ch,syn['ordered_source']['quantum_receiver'],nb)
    out={'status':'PASS','implementation':'stdlib Fraction only; no producer imports',
         'scope':['literal channels','all edge rational identities and Sturm decisions','faithful classical failure witness',
                  'strict noncommuting POVMs and exact guessing reversal','coherent query matrices and signed coefficients',
                  'graph gap and neighbourhood scalar budget'],
         'seconds':perf_counter()-start,'reference_dimensions_enumerated':0,'SDPs':0,
         'not_scope':'independent mathematical audit, source inference, physical acquisition, priority'}
    (HERE/'EXACT_REPLAY.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))

if __name__=='__main__':main()
