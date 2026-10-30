"""A's independent literal angular/family consumer; stdlib only.

Reads certificate data, never producer code. Determinants use division-free
subset expansion, not the producer's Bareiss elimination. Sturm uses exact
Fraction long division with positive content normalization. No point grid,
optimizer, source model or PDE is executed. Writes only this review folder.
"""
from fractions import Fraction as Q
from math import gcd, lcm, comb
from pathlib import Path
from functools import reduce
import json, hashlib, time


def plus(*polys):
    out = {}
    for p in polys:
        for e, v in p.items():
            out[e] = out.get(e, 0) + v
    return {e:v for e,v in out.items() if v}


def times(p, q):
    out = {}
    for a, x in p.items():
        for b, y in q.items():
            e = tuple(a[i]+b[i] for i in range(len(a)))
            out[e] = out.get(e, 0) + x*y
    return {e:v for e,v in out.items() if v}


def by(p, c): return {e:v*c for e,v in p.items() if v*c}


def derivative(p, i):
    out = {}
    for e,v in p.items():
        if e[i]:
            f=list(e); f[i]-=1; out[tuple(f)]=v*e[i]
    return out


def substitute_signed(p, perm, signs):
    out = {}
    for e,v in p.items():
        f=[0]*len(e)
        for i,n in enumerate(e): f[perm[i]]=n; v*=signs[i]**n
        out[tuple(f)]=v
    return out


def coordinate(i): return {tuple(int(j==i) for j in range(4)):1}


def canonical(p):
    out={}
    for e,v in p.items():
        if not e[2]: out[(e[1],e[3])]=out.get((e[1],e[3]),0)+v
    return {e:v for e,v in out.items() if v}


def all_leading_determinants(a):
    # det(first |S| rows, columns S); expand its LAST row.
    dp={0:{(0,0):1}}
    for mask in range(1,1<<len(a)):
        columns=[j for j in range(len(a)) if mask>>j&1]
        row=len(columns)-1
        dp[mask]=plus(*(by(times(a[row][j],dp[mask^(1<<j)]),
                          (-1)**(row+position))
                        for position,j in enumerate(columns)))
    return [dp[(1<<i)-1] for i in range(1,len(a)+1)]


def trim(p):
    while p and not p[-1]: p.pop()
    return p


def normalize(p):
    p=trim(list(p))
    if not p: return []
    d=lcm(*(Q(x).denominator for x in p))
    integers=[int(Q(x)*d) for x in p]
    g=reduce(gcd,(abs(x) for x in integers))
    return [x//g for x in integers]  # ONLY positive rescaling.


def eval_at(p,x):
    z=0
    for c in reversed(p): z=z*x+c
    return z


def remainder(a,b):
    # Ordinary rational long division, normalizing by a positive scalar.
    a=normalize(a)
    while len(a)>=len(b):
        c=Q(a[-1],b[-1]); offset=len(a)-len(b)
        a=[Q(x) for x in a]
        for j,v in enumerate(b): a[j+offset]-=c*v
        a=normalize(a)
    return a


def sturm_positive(p):
    assert p and eval_at(p,0)>0
    a=normalize(p); endpoints=[]
    for x in (-1,1):
        count=0
        while len(a)>1 and not eval_at(a,x):
            # Division by z-x, exact with integer x.
            b=[0]*(len(a)-1); b[-1]=a[-1]
            for j in range(len(b)-2,-1,-1): b[j]=a[j+1]+x*b[j+1]
            assert a[0]+x*b[0]==0
            a=normalize(b); count+=1
        endpoints.append(count)
    seq=[a]
    if len(a)>1: seq.append(normalize([i*a[i] for i in range(1,len(a))]))
    while len(seq)>1:
        r=remainder(seq[-2],seq[-1])
        if not r: break
        seq.append([-x for x in r])
    def variation(x):
        signs=[(v>0)-(v<0) for q in seq if (v:=eval_at(q,x))]
        return sum(a!=b for a,b in zip(signs,signs[1:]))
    v=(variation(-1),variation(1)); assert v[0]==v[1]
    return {'degree':len(p)-1,'endpoints':endpoints,'variations':v}


def convolution(p,q):
    out=[0]*(len(p)+len(q)-1)
    for i,x in enumerate(p):
        for j,y in enumerate(q): out[i+j]+=x*y
    return trim(out)


def monomials(n,variables):
    if variables==1: yield(n,); return
    for i in range(n+1):
        for tail in monomials(n-i,variables-1): yield(i,)+tail


def main():
    start=time.perf_counter(); here=Path(__file__).resolve().parent
    root=here.parent; cert_path=root/'b_angular_repair/PRIMITIVE_CERTIFICATE.json'
    cert=json.loads(cert_path.read_text()); D=lcm(*(Q(v).denominator for _,_,v in cert['primitive_terms']))
    P=[{} for _ in range(4)]
    for i,e,v in cert['primitive_terms']:
        assert len(e)==4 and sum(e)==5 and tuple(e) not in P[i]
        c=Q(v)*D; assert c.denominator==1; P[i][tuple(e)]=int(c)
    a=[coordinate(i) for i in range(4)]
    T=plus(*(times(x,x) for x in a)); T2=times(T,T)
    det=plus(times(a[0],a[3]),by(times(a[1],a[2]),-1))
    X=plus(*(by(times(a[i],a[i]),s) for i,s in enumerate((1,-1,1,-1))))
    f=plus(T2,by(times(det,det),12),by(times(det,X),4))
    B=(0,1,3,4); E=(1,2,4,5)
    C=[[{} for _ in range(6)] for _ in range(6)]
    for i in range(4):
        for j in range(4):
            H=by(times(T2,derivative(derivative(f,i),j)),2*D)
            for indices in (B,E): C[indices[i]][indices[j]]=plus(C[indices[i]][indices[j]],H)
            W=plus(times(T,plus(derivative(P[j],i),by(derivative(P[i],j),-1))),
                   by(plus(times(a[i],P[j]),by(times(a[j],P[i]),-1)),-2))
            C[B[i]][E[j]]=plus(C[B[i]][E[j]],W)
            C[E[j]][B[i]]=plus(C[E[j]][B[i]],W)
    assert all(C[i][j]==C[j][i] for i in range(6) for j in range(6))
    # Verify WHOLE polynomial-density congruences, not merely alpha's signs.
    hp=(2,1,0,5,4,3); ap=(1,0,3,2)
    hs=(1,-1,1,-1,1,-1); az=(1,-1,-1,1)
    for i in range(6):
        for j in range(6):
            assert substitute_signed(C[hp[i]][hp[j]],ap,(1,)*4)==C[i][j]
            assert by(substitute_signed(C[i][j],range(4),az),hs[i]*hs[j])==C[i][j]
            lie={}
            for z,(index,sgn) in enumerate(((2,-1),(3,-1),(0,1),(1,1))):
                lie=plus(lie,by(times(derivative(C[i][j],z),a[index]),sgn))
            ki=(i+3,1) if i<3 else (i-3,-1)
            kj=(j+3,1) if j<3 else (j-3,-1)
            assert not plus(lie,by(C[ki[0]][j],ki[1]),by(C[i][kj[0]],kj[1]))
    mapped=time.perf_counter()
    minors=all_leading_determinants([[canonical(p) for p in row] for row in C])
    determinant_seconds=time.perf_counter()-mapped
    reports=[]; exceptional=None
    for k,(description,actual) in enumerate(zip(cert['leading_minor_factorizations'],minors),1):
        assert description['k']==k
        product={(0,0):1}
        for index,factor in enumerate(description['factors']):
            p={tuple(e):int(v) for e,v in factor['terms']}
            for _ in range(factor['power']): product=times(product,p)
            assert all(e[0]%2==0 for e in p)
            slices=[]
            for power in range(max(e[0] for e in p)//2+1):
                s=[0]*(max(e[1] for e in p)+1)
                for (i,j),v in p.items():
                    if i==2*power: s[j]+=v
                s=trim(s); slices.append(s)
                if s and (k,index,power)!=(6,1,1): reports.append(sturm_positive(s))
            assert slices[0]  # strict positivity includes b=0.
            if (k,index)==(6,1): exceptional=slices
        multiplier=Q(description['constant'])*(2*D)**k
        assert multiplier>0 and actual==by(product,multiplier)
    p0,p1,p2=exceptional[:3]
    disc=convolution(p0,p2); disc=[4*x for x in disc]
    sq=convolution(p1,p1); disc+= [0]*max(0,len(sq)-len(disc))
    for i,v in enumerate(sq): disc[i]-=v
    discriminant=sturm_positive(trim(disc))
    # Exact all-35 coefficient receiver for root's robust support cuts.
    fp=root/'root_angular/EXPLICIT_FAMILY.json'; family=json.loads(fp.read_text())
    powers=list(monomials(4,4)); assert powers==[tuple(p) for p in family['monomial_order']]
    tables={}
    for name,R in [('plus',(0,200,-1,0)),('minus',(1,0,0,-2))]:
        rows=[]
        for degree in range(3):
            row=[]
            for i,j,k,l in powers:
                row.append(sum(comb(i,v)*comb(l,degree-v)*R[0]**(i-v)*R[3]**(l-degree+v)*R[1]**j*R[2]**k
                               for v in range(max(0,degree-l),min(i,degree)+1)))
            rows.append(row)
        assert rows==family['support_line_rows'][name]
        norms=[sum(abs(v) for v in row) for row in rows]
        assert norms==family['support_row_l1_norms'][name]
        for label,p in [('Fstar',f),('T2',T2)]:
            assert [sum(v*p.get(e,0) for v,e in zip(row,powers)) for row in rows]==family['literal_seed_and_buffer_coefficients'][name][label]
        tables[name]=norms
    epsilon=Q(family['epsilon']); rho=Q(family['coefficient_inf_ball_radius'])
    U=(4808+160004*epsilon+120603*rho)/200
    L=(48-24*epsilon-42*rho+(8+20*epsilon-49*rho)**2/(4*(97+25*epsilon+31*rho)))/2
    assert U==Q(family['universal_support_upper']) and L==Q(family['universal_support_lower'])
    assert L-U==Q(family['strict_non_PC_gap']) and L-U>Q(3,100)
    assert epsilon-420*rho==epsilon/2 and (epsilon-420*rho)/4==Q(1,800000)
    assert Q(3,4)-Q(23,4)*Q(8,23)**2==Q(5,92)
    out={'scope':'independent exact supplied-certificate and full-family arithmetic; analytic QC/cover reviewed separately',
         'no_producer_imports':True,'scientific_source_queries':0,'solver_calls':0,'new_point_grid':False,
         'density_reconstructed':True,'whole_density_discrete_congruences':True,'whole_density_rotation_Lie_identity':True,
         'determinant_algorithm':'division-free subset expansion; not producer Bareiss',
         'all_six_factorizations_exact':True,'strict_positive_univariate_slices':len(reports),
         'discriminant':discriminant,'all35_family_rows_and_rational_support_gap':True,
         'strong_QC_modulus_if_seed':'1/800000','common_denominator':str(D),
         'determinant_seconds':determinant_seconds,'total_seconds':time.perf_counter()-start,
         'inputs':{str(p.relative_to(root)):{'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size} for p in [cert_path,fp]},
         'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (here/'EXACT_CONSUMPTION.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__=='__main__': main()
