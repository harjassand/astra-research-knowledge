"""Independent portable exact checks for Schur composition and small tensor algebra.

Uses only the Python standard library. It never loads pickle or executes a
supplied binary. The discrete expansion is restricted to n<=8 and is charged
as a small verification reference, never part of the large witness algorithm.
"""
from pathlib import Path
from fractions import Fraction as Q
from itertools import combinations
import argparse,json,random,time,hashlib

def dot(a,b):return sum((x*y for x,y in zip(a,b)),Q())
def T(a):return list(map(list,zip(*a)))
def mm(a,b):return [[dot(row,col) for col in T(b)] for row in a]
def add(a,b,k=1):return [[x+k*y for x,y in zip(ra,rb)] for ra,rb in zip(a,b)]
def scale(a,k):return [[k*x for x in row] for row in a]
def sub(a,rows,cols):return [[a[i][j] for j in cols] for i in rows]
def inv(a):
    n=len(a);w=[list(row)+[Q(i==j) for j in range(n)] for i,row in enumerate(a)]
    for j in range(n):
        k=next(i for i in range(j,n) if w[i][j]);w[j],w[k]=w[k],w[j]
        z=w[j][j];w[j]=[x/z for x in w[j]]
        for i in range(n):
            if i!=j:
                z=w[i][j];w[i]=[x-z*y for x,y in zip(w[i],w[j])]
    return [row[n:] for row in w]
def det(a):
    if not a:return Q(1)
    w=[row.copy() for row in a];v=Q(1)
    for j in range(len(a)):
        ks=[i for i in range(j,len(a)) if w[i][j]]
        if not ks:return Q()
        k=ks[0]
        if k!=j:w[j],w[k]=w[k],w[j];v=-v
        z=w[j][j];v*=z
        for i in range(j+1,len(a)):
            f=w[i][j]/z
            for k in range(j+1,len(a)):w[i][k]-=f*w[j][k]
    return v
checks=0
def check(b):
    global checks
    assert b;checks+=1
def psd(a):
    check(a==T(a))
    for k in range(1,len(a)+1):
        for ids in combinations(range(len(a)),k):check(det(sub(a,ids,ids))>=0)
def quadratic(a,x):return mm(T(x),mm(a,x))[0][0]
def schur_value(D,a,G):
    n=len(D);ids=list(range(n));last=[n]
    K=add(D,sub(G,ids,ids),-1);b=add(a,sub(G,ids,last),-1)
    z=mm(inv(K),b);F=G[n][n]+quadratic(inv(K),b)
    return F,K,b,z

def graph(rng,n,no=2,patches=False):
    A=[[Q() for j in range(n)] for i in range(n)]
    for i in range(n):A[i][i]+=Q(rng.randint(1,5),rng.randint(1,5))
    for i in range(n):
        for j in range(i):
            if patches and i>=no and j>=no and (i-no)//2!=(j-no)//2:continue
            c=Q(rng.randint(1,5),rng.randint(1,5))
            A[i][i]+=c;A[j][j]+=c;A[i][j]-=c;A[j][i]-=c
    m=[[Q(rng.randint(1,5),rng.randint(1,5))] for i in range(n)]
    return A,m

def schur_audit():
    rng=random.Random(1400265);rows=[]
    for case in range(24):
        A,m=graph(rng,5);O=[0,1];I=[2,3,4]
        D=sub(A,O,O);a=sub(m,O,[0]);H=sub(A,I,I);J=sub(A,I,O);h=sub(m,I,[0])
        B=[r+s for r,s in zip(J,h)];W=mm(inv(H),B)
        V=scale(W,Q(99,100));R=add(B,mm(H,V),-1)
        G=mm(T(B),W);G0=add(add(mm(T(B),V),mm(T(V),B)),mm(T(V),mm(H,V)),-1)
        Gamma=mm(T(R),mm(scale(inv(H),2),R));E=add(G,G0,-1)
        check(E==mm(T(R),mm(inv(H),R)));psd(E);psd(add(Gamma,E,-1))
        F=quadratic(inv(A),m);F0,K0,b0,z0=schur_value(D,a,G0)
        Fp,Kp,bp,zp=schur_value(D,a,add(G0,Gamma))
        check(F0<=F<=Fp)
        eta=sum(mm(inv(K0),sub(Gamma,O,O))[i][i] for i in range(2))
        psd(add(scale(K0,eta),sub(Gamma,O,O),-1));check(0<=eta<1)
        v0=[[-x[0]] for x in z0]+[[Q(1)]];d0=quadratic(Gamma,v0)
        c=add(mm(sub(Gamma,O,O),z0),sub(Gamma,O,[2]),-1)
        check(Fp-F0==d0+quadratic(inv(Kp),c))
        check(Fp<=F0+d0/(1-eta))
        rows.append({'eta':str(eta),'F':str(F),'F0':str(F0),'Fplus':str(Fp),'gap_bound':str(d0/(1-eta))})
    # Patch addition: hidden blocks are deliberately independent given O.
    for case in range(8):
        A,m=graph(rng,6,patches=True);O=[0,1];I=[2,3,4,5]
        B=[r+s for r,s in zip(sub(A,I,O),sub(m,I,[0]))]
        G=mm(T(B),mm(inv(sub(A,I,I)),B));summed=[[Q() for i in range(3)] for j in range(3)]
        for ids in [[2,3],[4,5]]:
            Bj=[r+s for r,s in zip(sub(A,ids,O),sub(m,ids,[0]))]
            summed=add(summed,mm(T(Bj),mm(inv(sub(A,ids,ids)),Bj)))
        check(G==summed)
    # Exact physical zero combined-residual example: boundary error is large.
    A=[[Q(2),Q(-1)],[Q(-1),Q(1)]];m=[[Q(1)],[Q(1)]]
    G0=[[Q(-3),Q(-9)],[Q(-9),Q(-15)]];Gamma=[[Q(40),Q(80)],[Q(80),Q(160)]]
    F0,K0,b0,z0=schur_value([[Q(2)]],[[Q(1)]],G0);v0=[[-z0[0][0]],[Q(1)]]
    check(F0==5==quadratic(inv(A),m));check(quadratic(Gamma,v0)==0)
    check(Gamma[0][0]>K0[0][0]);check(K0[0][0]-Gamma[0][0]<0)
    # Abstract positive-Gram completions, with positive Schur matrices, preserve F.
    # The t=1/10 completion is the displayed physical two-state graph.
    for t in [Q(1,10),Q(21,200),Q(11,100)]:
        Gt=add(G0,scale(Gamma,t));psd(Gt)
        F,K,b,z=schur_value([[Q(2)]],[[Q(1)]],Gt)
        check(K[0][0]>0);check(F==5)
    return {'physical_networks':24,'independent_patch_checks':8,'zero_error_example':{'F':'5','mean':'5/2','d0':'0','boundary_relative_error':'8'},'samples':rows}

def window_mean(n,q,eps,root):
    N=1<<n;K=[[Q() for i in range(N)] for j in range(N)]
    mass=[q**x.bit_count()*(1-q)**(n-x.bit_count()) for x in range(N)]
    for x in range(N):
        for i in range(n):
            fac=root if i==0 else (Q(1) if x&(1<<(i-1)) else eps)
            rate=(1-q if x&(1<<i) else q)*fac
            K[x][x]+=rate;K[x][x^(1<<i)]-=rate
        K[x][x]+=q*(Q(1) if x&(1<<(n-1)) else eps)
    v=mm(inv(K),[[Q(1)] for i in range(N)])
    return sum(m*x[0] for m,x in zip(mass,v))

def window_audit():
    rows=[]
    for q,eps in [(Q(1,5),Q(1,100)),(Q(1,26),Q(1,10000))]:
        for n in [3,4,5]:
            full=window_mean(n,q,eps,Q(1))
            for w in range(1,n):
                low=window_mean(w,q,eps,eps+(1-eps)*q)
                high=window_mean(w,q,eps,eps)
                check(low<=full<=high)
                rows.append({'n':n,'w':w,'q':str(q),'eps':str(eps),'lower':str(low),'full':str(full),'upper':str(high)})
    # The averaged-boundary argument requires an omitted parent coordinate.
    full=window_mean(1,Q(1,2),Q(1,4),Q(1))
    guessed=window_mean(1,Q(1,2),Q(1,4),Q(5,8))
    check(guessed>full)
    return {'finite_exact_window_comparisons':len(rows),'all_require_w_less_than_n':True,'same_size_average_boundary_transfer_refuted':{'n':1,'full':str(full),'incorrect_lower':str(guessed)},'samples':rows}

def discrete_audit(prefix):
    p=Path(prefix);it=iter(map(int,p.with_suffix('.dyadic.txt').read_text().split()))
    n,k,en,ed=[next(it) for _ in range(4)];check(2<=n<=8)
    cores=[];psum=0;previous=1
    for _ in range(n):
        l,r,e=[next(it) for _ in range(3)];check(l==previous);previous=r;psum+=e
        ar=[next(it) for _ in range(l*2*r)];cores.append((l,r,ar))
    check(previous==1)
    try:next(it);raise AssertionError('extra payload')
    except StopIteration:pass
    # Enumerate only the 2**n small coefficient vector, with its work charged.
    vs=[]
    for x in range(1<<n):
        row=[1]
        for i,(l,r,a) in enumerate(cores):
            bit=(x>>(n-1-i))&1
            row=[sum(row[j]*a[(j*2+bit)*r+t] for j in range(l)) for t in range(r)]
        vs.append(row[0])
    den=k*k+1;D=ed*den*den;ys=[]
    for x,v in enumerate(vs):
        bits=[(x>>(n-1-i))&1 for i in range(n)]
        y=D*bits[0]*v+en*den*den*sum(bits[1:])*v+en*den*v
        for i in range(1,n):
            if bits[i]:
                prev=bits[i-1];flip=x^(1<<(n-i))
                y+=(ed-en)*den*((k*k if prev else 1)*v-k*vs[flip])
        last=bits[-1];y+=(ed-en)*((k*k if last else 1)*v-k*vs[x^1])
        ys.append(y)
    raw={a:int(b) for a,b in (ln.split() for ln in p.with_suffix('.exact_raw.txt').read_text().splitlines())}
    check(raw['p']==psum);check(raw['D']==D);check(raw['source']==vs[0]);check(raw['Hsource']==ys[0])
    check(raw['energy']==sum(a*b for a,b in zip(vs,ys)));check(raw['Hnorm']==sum(y*y for y in ys))
    for j in range(n+1):
        key='sector'+str(j)
        if key in raw:check(raw[key]==sum(y*y for x,y in enumerate(ys) if x.bit_count()==j))
    return {'prefix':p.name,'coefficient_dimension':1<<n,'source_integer_and_energy_and_norm_and_sector_checks':'PASS','n':n,'scope':'Small exact verification reference; never used by large-state certificate algorithm.'}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--discrete-prefix');ap.add_argument('--output',default='source_schur_check_results.json');args=ap.parse_args()
    st=time.perf_counter();s=schur_audit();w=window_audit();d=discrete_audit(args.discrete_prefix) if args.discrete_prefix else None
    out={'status':'PASS','exact_assertions':checks,'seconds':time.perf_counter()-st,'schur':s,'window_scope_checks':w,'small_discrete_backend_check':d,
        'scope':'Finite exact implementation checks; universal claims rest on written proof; no external validation.',
        'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    Path(args.output).write_text(json.dumps(out,indent=2));print(json.dumps({k:v for k,v in out.items() if k not in ['schur']},indent=2))
if __name__=='__main__':main()
