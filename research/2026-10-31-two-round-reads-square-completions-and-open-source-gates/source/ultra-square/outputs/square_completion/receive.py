"""Independent exact receiver for all linear-square completion directions.

Stdlib rational and quadratic-field arithmetic only. Rebuild the rank
exclusion identities, exceptional cubic space, closed forms, both heat
lifts, and global constants. No Groebner, optimizer, float, or work import.
The global classification and heat/Stokes argument are in PROOF.txt.
"""
from pathlib import Path
from fractions import Fraction as R
from itertools import combinations,permutations
from math import gcd,lcm,isqrt
import importlib.util,json,time,sys,contextlib,io

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('square_shared_core',HERE.parent/'degenerate_completion/receive.py')
d=importlib.util.module_from_spec(spec);spec.loader.exec_module(d)
b=d.b;add,mul,scale,diff=d.add,d.mul,d.scale,d.diff
zh=zk=R(0)
class Q:
    def __init__(self,a=0,c=0):
        if isinstance(a,Q):self.a,self.c=a.a,a.c
        else:self.a,self.c=R(a),R(c)
    def __add__(self,v):v=Q(v);return Q(self.a+v.a,self.c+v.c)
    __radd__=__add__
    def __neg__(self):return Q(-self.a,-self.c)
    def __sub__(self,v):return self+-Q(v)
    def __rsub__(self,v):return Q(v)+-self
    def __mul__(self,v):v=Q(v);return Q(self.a*v.a+self.c*v.c*zk,self.a*v.c+self.c*v.a+self.c*v.c*zh)
    __rmul__=__mul__
    def __truediv__(self,v):
        v=Q(v);norm=v.a*v.a+v.a*v.c*zh-v.c*v.c*zk
        if not norm:raise ZeroDivisionError
        return self*Q((v.a+v.c*zh)/norm,-v.c/norm)
    def __rtruediv__(self,v):return Q(v)/self
    def __pow__(self,n):
        assert isinstance(n,int) and n>=0
        out=Q(1);v=self
        while n:
            if n%2:out=out*v
            v=v*v;n//=2
        return out
    def __bool__(self):return bool(self.a or self.c)
    def __eq__(self,v):v=Q(v);return self.a==v.a and self.c==v.c
    def upper(self):return abs(self.a)+R(2,3)*abs(self.c)
    def literal(self):return [str(self.a),str(self.c)]
def readpoly(rows):return {(int(a),int(c)):R(v) for a,c,v in rows if R(v)}
def constant(v):return {(0,0):R(v)} if v else {}
def determinant(M):
    n=len(M);out={}
    for pp in permutations(range(n)):
        sign=(-1)**sum(pp[i]>pp[j] for i in range(n) for j in range(i+1,n));term=constant(sign)
        for i,j in enumerate(pp):term=mul(term,M[i][j])
        out=add(out,term)
    return out
def primitive(P):
    den=lcm(*(v.denominator for v in P.values()));gg=0
    for v in P.values():gg=gcd(gg,abs(int(v*den)))
    return {pw:R(int(v*den)//gg) for pw,v in P.items()}
def mat0(n,m=None):return [[Q(0) for _ in range(n if m is None else m)] for _ in range(n)]
def main():
    global zh,zk
    start=time.perf_counter();cert=json.loads((HERE/'certificate.json').read_text());base=json.loads((HERE.parent/'hopf_structure/certificate.json').read_text())
    pco=list(map(R,cert['zeta_minimal_polynomial_monic']));assert len(pco)==3 and pco[0]==1
    zh=-pco[1];zk=-pco[2];disc=zh*zh+4*zk
    assert disc>0 and not (isqrt(disc.numerator)**2==disc.numerator and isqrt(disc.denominator)**2==disc.denominator)
    lo,hi=map(R,cert['zeta_chosen_interval']);assert (lo,hi)==(R(-2,3),R(-33,50))
    def peval(t):return t*t-zh*t-zk
    assert peval(lo)>0>peval(hi) and 2*hi-zh<0 and pco[2]<0 and peval(1)<0
    alpha=R(cert['eta_equals_alpha_zeta']);eta0,zeta0=map(R,base['ray']['canonical_zero']);assert alpha==eta0/zeta0
    assert (1+alpha*alpha)*R(4,9)<1
    eta,zeta=b.var(2,0),b.var(2,1);one=constant(1)
    av=list(map(R,base['ray']['A0']));a0,b0,c0,_=av;nulls=[av,[-b0,a0,R(1),-c0]]
    nL=[(add(constant(a0),scale(eta,b0),zeta),add(constant(-c0),scale(eta,-1),scale(zeta,b0))),
        (add(constant(-b0),scale(eta,a0),scale(zeta,-c0)),add(constant(-1),scale(eta,c0),scale(zeta,a0)))]
    ells=[(one,{}),(eta,zeta)];N=[]
    for side in (0,1):
        rows=[[],[],[]]
        for j in range(5):
            mm=[R(int(i==j)) for i in range(4)];lam=R(int(j==4));ma,mb,mc,md=mm
            nm=(a0*ma+b0*mb+c0*mc+md,-c0*ma-mb+a0*mc+b0*md) if side==0 else (-b0*ma+a0*mb+mc-c0*md,-ma+c0*mb-b0*mc+a0*md)
            mi=(ma,mc) if side==0 else (mb,md);li=ells[side];ni=nL[side];delta=1 if side==0 else -1
            vals=[add(scale(ni[0],2*mi[0]),scale(li[0],nm[0]),constant(lam*delta)),
                  add(scale(ni[1],2*mi[0]),scale(ni[0],2*mi[1]),scale(li[0],nm[1]),scale(li[1],nm[0])),
                  add(scale(ni[1],2*mi[1]),scale(li[1],nm[1]),constant(lam*delta))]
            for k,p in enumerate(vals):rows[k].append(p)
        N+=rows
    assert N==[[readpoly(p) for p in row] for row in cert['rank_bracket_matrix']]
    minors=[primitive(determinant([row for i,row in enumerate(N) if i!=omit])) for omit in range(6)]
    assert minors==[readpoly(p) for p in cert['primitive_five_by_five_minors']]
    H=[readpoly(p) for p in cert['rank_exclusion_polynomials']]
    for target,multipliers in zip(H,cert['exact_combination_multipliers']):assert target==add(*(mul(minor,readpoly(mm)) for minor,mm in zip(minors,multipliers)))
    P={(0,2):R(1),(0,1):pco[1],(0,0):pco[2]}
    qco=list(map(R,cert['rank_exclusion_positive_quadratic_monic']));assert qco[0]==1 and qco[1]*qco[1]-4*qco[2]<0
    QQ={(0,2):R(1),(0,1):qco[1],(0,0):qco[2]}
    assert H[1]==scale(mul(mul(P,P),QQ),R(cert['rank_exclusion_degree_six_leading_coefficient']))
    square=mul(add(eta,scale(zeta,-alpha)),add(eta,scale(zeta,-alpha)))
    assert R(cert['rank_exclusion_square_coefficient'])>0
    assert H[0]==add(scale(square,R(cert['rank_exclusion_square_coefficient'])),mul(P,readpoly(cert['rank_exclusion_square_quotient'])))
    # These literal identities prove the universal REAL rank exclusion.
    # No Groebner computation, root approximation, or numerical rank is used.
    Z=Q(0,1);EE=alpha*Z;ell=[Q(1),EE,Q(0),Z]
    Nq=[[b.evaluate(p,[EE,Z]) for p in row] for row in N];assert b.rank(Nq)==3
    factors=[[Q(*v) for v in row] for row in cert['factored_cubic_basis']]
    assert len(factors)==2 and b.rank(factors)==2
    assert all(not sum(a*v for a,v in zip(row,coef)) for row in Nq for coef in factors)
    powers=cert['cubic_powers'];assert len(powers)==20 and len({tuple(p) for p in powers})==20 and all(sum(p)==3 for p in powers)
    A=[b.var(4,i) for i in range(4)];L=add(*(scale(v,q) for v,q in zip(A,ell)));detA=add(mul(A[0],A[3]),scale(mul(A[1],A[2]),-1));cubics=[]
    for coef,literal in zip(factors,cert['cubic_basis']):
        M=add(*(scale(v,q) for v,q in zip(A,coef[:4])));C=add(mul(mul(L,L),M),scale(mul(detA,L),coef[4]))
        cv=[Q(*v) for v in literal];assert [C.get(tuple(pw),Q(0)) for pw in powers]==cv
        assert sum(v.upper() for v in cv)==1
        cubics.append(C)
    assert b.rank([[C.get(tuple(pw),Q(0)) for pw in powers] for C in cubics])==2
    x,y=b.var(2,0),b.var(2,1);zero={}
    def rotatepoly(v):return [add(scale(x,v[0]),scale(y,-v[2])),add(scale(x,v[1]),scale(y,-v[3])),add(scale(y,v[0]),scale(x,v[2])),add(scale(y,v[1]),scale(x,v[3]))]
    for C in cubics:
        for side in (0,1):
            Rp=[x,zero,y,zero] if side==0 else [zero,x,zero,y];kr=rotatepoly(nulls[side])
            assert not add(*(mul(d.compose(diff(C,i),Rp),kr[i]) for i in range(4)))
    # Rank-one quadratic heat: exactly two rows, four-dimensional kernel.
    rows=[[Q(1),EE,Q(0),Q(0),Z,Q(0)],[Q(0),Q(1),EE,Q(0),Q(0),Z]]
    kernel=[[EE*EE,-EE,Q(1),Q(0),Q(0),Q(0)],[Q(0),Q(0),Q(0),Q(1),Q(0),Q(0)],[-Z,Q(0),Q(0),Q(0),Q(1),Q(0)],[EE*Z,-Z,Q(0),Q(0),Q(0),Q(1)]]
    assert b.rank(rows)==2 and b.rank(kernel)==4 and all(not sum(a*v for a,v in zip(row,k)) for row in rows for k in kernel)
    assert sum(v*v for v in rows[0])==1+EE*EE+Z*Z and sum(v*v for v in rows[1])==1+EE*EE+Z*Z
    assert sum(a*v for a,v in zip(*rows))==EE and EE.upper()<R(1,2)
    # Thus the nonzero eigenvalues of rows^T rows exceed 1/2.
    p1=(0,1,3,4);p2=(1,2,4,5);pairs4=list(combinations(range(4),2));pairs6=list(combinations(range(6),2));wedges=[]
    for i,j in pairs4:
        W=[[R(0)]*6 for _ in range(6)]
        for ii,jj,sign in ((p1[i],p2[j],1),(p2[j],p1[i],1),(p1[j],p2[i],-1),(p2[i],p1[j],-1)):W[ii][jj]+=R(sign,2)
        wedges.append(W)
    dep=[pairs4.index((i,j))*4+k for i,j,k in combinations(range(4),3)];free=[i for i in range(24) if i not in dep]
    solution=[[Q(*v) for v in row] for row in cert['heat_lift_coefficients']];assert len(solution)==80 and all(len(row)==2 for row in solution)
    m=R(0)
    for ic,C in enumerate(cubics):
        v=[row[ic] for row in solution];omega=[Q(0)]*24
        for k,i in enumerate(free):omega[i]=v[k]
        for i,j,k in combinations(range(4),3):omega[pairs4.index((i,j))*4+k]=omega[pairs4.index((i,k))*4+j]-omega[pairs4.index((j,k))*4+i]
        assert all(not (omega[pairs4.index((j,k))*4+i]-omega[pairs4.index((i,k))*4+j]+omega[pairs4.index((i,j))*4+k]) for i,j,k in combinations(range(4),3))
        XX=[]
        for a in range(4):
            ea=[R(int(i==a)) for i in range(4)];Hc=[[b.evaluate(diff(diff(C,i),j),ea) for j in range(4)] for i in range(4)];raw=mat0(6)
            for ids in (p1,p2):
                for i in range(4):
                    for j in range(4):raw[ids[i]][ids[j]]+=Hc[i][j]
            corrected=[[raw[i][j]+sum(omega[p*4+a]*W[i][j] for p,W in enumerate(wedges)) for j in range(6)] for i in range(6)]
            Xa=[[q/2 for q in row] for row in corrected]
            for k,(i,j) in enumerate(pairs6):Xa[i][j]+=v[20+15*a+k];Xa[j][i]-=v[20+15*a+k]
            assert all(Xa[i][j]+Xa[j][i]==corrected[i][j] for i in range(6) for j in range(6))
            assert all(not sum(Xa[i][j]*kh[j] for j in range(6)) for i in range(6) for kh in kernel)
            XX.append(Xa)
        for side in (0,1):
            Ar=rotatepoly(nulls[side]);kh=[{} for _ in range(6)];kh[0 if side==0 else 2]=x;kh[3 if side==0 else 5]=y
            for j in range(6):assert not add(*(scale(mul(kh[i],Ar[a]),XX[a][i][j]) for a in range(4) for i in range(6)))
        ac=[R(1),eta0,R(0),zeta0];kc=[R(0),R(0),b0,R(0),R(0),R(1)]
        for gamma in (0,1):
            ar=ac if not gamma else [ac[3],-ac[2],ac[1],-ac[0]];kr=kc if not gamma else [kc[5],-kc[4],kc[3],kc[2],-kc[1],kc[0]];Ar=rotatepoly(ar)
            kh=[add(scale(x,kr[i]),scale(y,-kr[i+3])) for i in range(3)]+[add(scale(y,kr[i]),scale(x,kr[i+3])) for i in range(3)]
            for j in range(6):assert not add(*(scale(mul(kh[i],Ar[a]),XX[a][i][j]) for a in range(4) for i in range(6)))
        m=max(m,max(sum(XX[a][i][j].upper() for a in range(4)) for i in range(6) for j in range(6)))
    assert m==R(cert['exact_lift_entry_l1_upper_bound']);kk=0
    while 2**kk<m:kk+=1
    power=86+2*kk;assert power==cert['completion_power']==92
    assert R(2)**power>R(2)**83*m*m and cert['leading_uniform_margin_power']==64
    # At the canonical point L=a the second column vanishes, so its
    # acoustic equation cannot be divided by L(R2). Rebuild the extra
    # completed-root gamma coefficients directly instead. Together with
    # the three first-column equations these have full rank five.
    zero_case=[[b.evaluate(p,[R(0),R(0)]) for p in row] for row in N[:3]]
    zero_case += [[R(0),-2*b0,R(0),R(0),R(-1)],[R(0),R(-2),R(0),-2*b0,R(0)],[R(0),R(0),R(0),R(-2),R(-1)]]
    assert b.rank(zero_case)==5
    result={'all_linear_square_quadratic_directions_classified':True,'nonzero_cubic_requires_one_exceptional_SO2_Gamma_orbit':True,'real_rank_exclusion_ideal_identities_verified':2,'exact_primitive_five_by_five_minors':6,'zero_second_column_acoustic_constraint_rank':5,'quadratic_field_irreducible_and_root_isolated':True,'exceptional_cubic_dimension':2,'both_factored_cubics_and_acoustic_admissibility_verified':True,'closed_linear_two_forms':2,'all_heat_lift_identities_verified':True,'rank_one_quadratic_heat_rank':2,'bottom_heat_kernel_dimension':4,'nonzero_heat_eigenvalue_lower_bound':'1/2 before multiplication by 2nu','cubic_basis_coefficient_l1_upper_bound':'1','exact_heat_entry_coefficient_l1_upper_bound':str(m),'completion_power':power,'completion_coefficient':str(2**power),'leading_uniform_margin_power':64,'all_actual_L4_gradients_and_all_means':'QC by the globally bounded heat Gram and Stokes in PROOF.txt','external_independent_audit':'NOT_PERFORMED'}
    if '--replay-leading' in sys.argv:
        with contextlib.redirect_stdout(io.StringIO()):d.g.main()
        result['leading_shifted_Bernstein_matrices_replayed']=13524
    result.update({'seconds':time.perf_counter()-start,'scope':'Universal finite stabilizability by every nonnegative quadratic of rank one. It does not classify optimal coefficients, arbitrary higher-rank quadratic directions, or the full ROC/QC face.'})
    (HERE/'replay.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
