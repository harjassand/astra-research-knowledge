"""Independent literal common separator and strict ROC replay; stdlib only."""
from fractions import Fraction as F
from itertools import combinations_with_replacement as cwr,combinations
from pathlib import Path
import json,hashlib,time,argparse
N=10
def clean(p):return {e:c for e,c in p.items() if c}
def add(*ps):
    z={}
    for p in ps:
        for e,c in p.items():z[e]=z.get(e,F(0))+c
    return clean(z)
def scale(p,c):return clean({e:c*v for e,v in p.items()})
def mul(p,q):
    z={}
    for e,c in p.items():
        for f,d in q.items():
            g=tuple(i+j for i,j in zip(e,f));z[g]=z.get(g,F(0))+c*d
    return clean(z)
def product(ps):
    p={(0,)*N:F(1)}
    for q in ps:p=mul(p,q)
    return p
def var(j):
    e=[0]*N;e[j]=1;return {tuple(e):F(1)}
def diff(p,j):
    z={}
    for e,c in p.items():
        if e[j]:
            f=list(e);f[j]-=1;z[tuple(f)]=c*e[j]
    return z
def invariants(a):
    aa,b,c,d=a
    return add(mul(aa,aa),mul(c,c)),add(mul(b,b),mul(d,d)),add(mul(aa,b),mul(c,d)),add(mul(aa,d),scale(mul(b,c),-1))
def bases(a):
    u,v,w,q=invariants(a)
    return [mul(u,u),mul(v,v),mul(u,v),mul(w,w),mul(u,w),mul(v,w),mul(q,u),mul(q,v),mul(q,w)]
def shifted(p,values):
    z={}
    for e,c in p.items():z=add(z,scale(product(values[i] for i in range(4) for j in range(e[i])),c))
    return z
def positive_matrix(A,pivots):
    """Schur complement elimination, then independent full reconstruction."""
    n=len(A);W=[row.copy() for row in A];L=[[F(i==j) for j in range(n)] for i in range(n)];D=[]
    assert all(A[i][j]==A[j][i] for i in range(n) for j in range(n))
    for k in range(n):
        d=W[k][k];assert d>0,(k,d);D.append(d)
        for i in range(k+1,n):L[i][k]=W[i][k]/d
        for i in range(k+1,n):
            for j in range(i,n):W[i][j]=W[j][i]=W[i][j]-W[i][k]*W[j][k]/d
    assert D==list(map(F,pivots))
    assert all(A[i][j]==sum(L[i][k]*D[k]*L[j][k] for k in range(n)) for i in range(n) for j in range(n))
    return D
def coefficient(p,exponent):return p.get(tuple(exponent),F(0))
def quadratic_matrix(p):
    out=[]
    for i in range(4):
        row=[]
        for j in range(4):
            e=[0]*N;e[i]+=1;e[j]+=1;row.append(coefficient(p,e)/(1 if i==j else 2))
        out.append(row)
    return out
def acoustic_matrix(f):
    aa=quadratic_matrix(diff(diff(f,0),0));ab=quadratic_matrix(diff(diff(f,0),1));bb=quadratic_matrix(diff(diff(f,1),1))
    return [[(aa if i<4 and j<4 else bb if i>=4 and j>=4 else ab)[i%4][j%4] for j in range(8)] for i in range(8)]


def main(write=False):
    start=time.monotonic();root=Path(__file__).resolve().parent
    path=root/'EXACT_COMMON_SEPARATOR.json';raw=path.read_bytes();r=json.loads(raw)
    a=[var(i) for i in range(4)];x=[var(i+4) for i in range(4)];jet=[var(i+4) for i in range(6)]
    order=[tuple(e)+(0,0) for e in r['PC_monomial_order']]
    lp=dict(zip(order,map(F,r['PC_lambda'])));assert len(lp)==658==len(order)
    def pc(p):
        assert set(p)<=set(lp)
        return sum((c*lp[e] for e,c in p.items()),F(0))
    zpc=[product([ai,x[j],x[k]]) for ai in a for j,k in cwr(range(4),2)]
    zpc += [product([x[i],x[j],x[k]]) for i,j,k in cwr(range(4),3)]
    assert len(zpc)==60
    assert set(lp)=={next(iter(mul(p,q))) for p in zpc for q in zpc}
    Mp=[[pc(mul(p,q)) for q in zpc] for p in zpc]
    dp=positive_matrix(Mp,r['PC_positive_LDL_pivots'])
    pairs4=list(cwr(range(4),2));pairs6=list(cwr(range(6),2));heat_monomials=[product([a[i],a[j],jet[k],jet[l]]) for i,j in pairs4 for k,l in pairs6]
    lh={next(iter(p)):F(c) for p,c in zip(heat_monomials,r['heat_lambda'])};assert len(lh)==210
    def heat(p):
        assert set(p)<=set(lh)
        return sum((c*lh[e] for e,c in p.items()),F(0))
    zh=[mul(ai,b) for ai in a for b in jet]
    Mh=[[heat(mul(p,q)) for q in zh] for p in zh]
    dh=positive_matrix(Mh,r['heat_positive_LDL_pivots'])
    norm=add(*(mul(xi,xi) for xi in x));detx=invariants(x)[3]
    selector_pairings=[pc(product([norm,a[i],a[j],detx])) for i,j in pairs4]
    assert selector_pairings==[0]*10
    J1=[jet[0],jet[1],jet[3],jet[4]];J2=[jet[1],jet[2],jet[4],jet[5]]
    formpairs=list(combinations(range(4),2));triples=list(combinations(range(4),3));eta=list(map(F,r['closedness_dual_eta']))
    assert len(eta)==16
    # Literal exterior derivative proves annihilation of the full closed space,
    # without importing a nullspace basis or trusting its dimension.
    closure_rows=[[F(0)]*60 for i in range(16)]
    for component,(i,j) in enumerate(formpairs):
        for mono,(s,t) in enumerate(pairs4):
            q=mul(a[s],a[t]);pull=mul(q,add(mul(J1[i],J2[j]),scale(mul(J1[j],J2[i]),-1)))
            def omega(u,v):
                if (u,v)==(i,j):return q
                if (v,u)==(i,j):return scale(q,-1)
                return {}
            rhs=F(0)
            for h,(u,v,w) in enumerate(triples):
                closed=add(diff(omega(v,w),u),scale(diff(omega(u,w),v),-1),diff(omega(u,v),w))
                for index in range(4):
                    e=[0]*N;e[index]=1;c=coefficient(closed,e)
                    closure_rows[4*h+index][10*component+mono]=c;rhs+=eta[4*h+index]*c
            assert heat(pull)==rhs
    basis=bases(a);shift=[add(ai,xi) for ai,xi in zip(a,x)];gp=[];gh=[]
    for f in basis:
        breg=add(shifted(f,shift),scale(f,-1),*(scale(mul(diff(f,i),x[i]),-1) for i in range(4)))
        gp.append(pc(mul(norm,breg)))
        diss=add(*(mul(mul(J[i],J[j]),diff(diff(f,i),j)) for J in [J1,J2] for i in range(4) for j in range(4)))
        gh.append(heat(diss))
    assert gp==gh==list(map(F,r['shared_energy_normal']))
    p=list(map(F,r['target_coefficients']));pair=sum(c*g for c,g in zip(p,gp))
    assert pair==F(r['target_pairing'])<0
    minor_pair=gp[2]-gp[3];assert minor_pair>=0
    # Literal strict ROC reconstruction, independent of source matrices.
    roc_path=root/'heat_normal_extreme_ROC.json';roc_raw=roc_path.read_bytes();roc=json.loads(roc_raw)
    assert list(map(F,roc['coefficients']))==p
    f=add(*(scale(q,c) for q,c in zip(basis,p)));s,t=jet[0],jet[1]
    target_acoustic=add(mul(mul(s,s),diff(diff(f,0),0)),scale(mul(mul(s,t),diff(diff(f,0),1)),2),mul(mul(t,t),diff(diff(f,1),1)))
    zz=[mul(s,ai) for ai in a]+[mul(t,ai) for ai in a];Q=[[F(c) for c in row] for row in roc['matrix']]
    assert len(Q)==8 and all(len(row)==8 for row in Q)
    assert target_acoustic==add(*(scale(mul(zz[i],zz[j]),Q[i][j]*(1 if i==j else 2)) for i in range(8) for j in range(i,8)))
    rho=F(roc['positive_shift']);assert rho==F(1,200000)
    dr=positive_matrix([[Q[i][j]-(rho if i==j else 0) for j in range(8)] for i in range(8)],roc['shifted_LDL_pivots'])
    acoustic_maps=[acoustic_matrix(q) for q in basis]
    canonical=[[sum(p[k]*acoustic_maps[k][i][j] for k in range(9)) for j in range(8)] for i in range(8)]
    K=[[F(0)]*4 for i in range(4)]
    for (i,j),c in zip(formpairs,map(F,roc['skew_parameters'])):K[i][j]=c;K[j][i]=-c
    assert all(Q[i][j]-canonical[i][j]==(K[i][j-4] if i<4 and j>=4 else -K[i-4][j] if i>=4 and j<4 else 0) for i in range(8) for j in range(8))
    S=sum(abs(c) for M in acoustic_maps for row in M for c in row);G=sum(abs(c) for c in gp)
    radius=min(rho/(2*S),-pair/(2*G));assert radius>0
    bits=max(max(abs(d.numerator).bit_length(),d.denominator.bit_length()) for d in dp+dh+dr)
    out={'status':'EXACT_STRICT_ROC_AND_COMMON_CLASS_SEPARATOR_LITERAL_PASS',
         'separator_sha256':hashlib.sha256(raw).hexdigest(),'ROC_sha256':hashlib.sha256(roc_raw).hexdigest(),
         'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'PC_positive_pivots':len(dp),'heat_positive_pivots':len(dh),'ROC_shifted_positive_pivots':len(dr),
         'selector_annihilators':list(map(str,selector_pairings)),'closedness_identity':'ALL60_LITERAL_PULLBACKS_EQUAL_ETA_TIMES_EXTERIOR_DERIVATIVE',
         'shared_basis_pairings':list(map(str,gp)),'target_pairing':str(pair),'det_square_pairing':str(minor_pair),
         'acoustic_perturbation_entry_l1_bound':str(S),'dual_normal_l1':str(G),
         'full9_coefficient_box_radius':str(radius),'ROC_shift':'1/200000',
         'maximum_pivot_integer_bits':bits,'seconds':time.monotonic()-start,'imports':'PYTHON_STDLIB_ONLY',
         'scope':'Excludes PC norm-level1 plus identity-Laplacian closedquadratic/bilinearSOS heat, including det²removal. TruePC, highermultipliers, otherflows andQC are not excluded.'}
    if write:(root/'VERIFY_COMMON.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--write-receipt',action='store_true')
    main(parser.parse_args().write_receipt)
