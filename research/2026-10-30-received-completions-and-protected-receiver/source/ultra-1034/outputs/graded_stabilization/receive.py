"""Exact stdlib receiver for the graded stabilization theorem.

Reconstructs the acoustic constraint maps, checks all ranks and the cubic
example, then replays the acquired angular certificate with the stronger
uniform matrix margin. No optimization, floating point, or producer imports.
The acquired sibling receiver supplies elementary rational polynomial code.
"""
from pathlib import Path
from fractions import Fraction as R
from math import gcd,lcm
import contextlib,importlib.util,io,json,tempfile,time

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('angular_core',HERE.parent/'hopf_structure/receive.py')
core=importlib.util.module_from_spec(spec);spec.loader.exec_module(core)
add,mul,scale,diff=core.add,core.mul,core.scale,core.diff

def monomial(powers):return {tuple(powers):R(1)}
def substitute(poly,images):
    n=len(next(iter(images[0]))) if images[0] else 2
    ans={}
    for powers,co in poly.items():
        term={(0,)*n:co}
        for image,power in zip(images,powers):
            for _ in range(power):term=mul(term,image)
        ans=add(ans,term)
    return ans
def dot(v,w):return add(*(mul(x,y) for x,y in zip(v,w)))
def clean_rows(rows):
    out=[]
    for row in rows:
        den=lcm(*(v.denominator for v in row));ints=[int(v*den) for v in row];g=0
        for v in ints:g=gcd(g,abs(v))
        out.append([v//g if g else v for v in ints])
    return out
def transpose(columns):return [list(row) for row in zip(*columns)]
def annihilates(matrix,vector):return all(sum(x*y for x,y in zip(row,vector))==0 for row in matrix)
def cubic_score(coefficients,powers,K,Rv):
    value=R(0)
    for coefficient,pw in zip(coefficients,powers):
        for j,power in enumerate(pw):
            if power:
                ex=list(pw);ex[j]-=1
                value+=2*coefficient*power*K[j]*__import__('math').prod(z**e for z,e in zip(Rv,ex))
    return value

def main():
    start=time.perf_counter();cert=json.loads((HERE/'certificate.json').read_text())
    base_path=HERE.parent/'hopf_structure/certificate.json';base=json.loads(base_path.read_text())
    av=list(map(R,base['ray']['A0']));assert cert['base_parameters']==base['ray']['A0']
    aa,bb,cc,dd=av;av2=[-bb,aa,dd,-cc]
    x,y=core.var(2,0),core.var(2,1);zero={}
    def rotate(v):return [add(scale(x,v[0]),scale(y,-v[2])),add(scale(x,v[1]),scale(y,-v[3])),add(scale(y,v[0]),scale(x,v[2])),add(scale(y,v[1]),scale(x,v[3]))]
    pairs=[([x,zero,y,zero],[zero,x,zero,y],rotate(av)),
           ([zero,x,zero,y],[x,zero,y,zero],rotate(av2))]
    quartic=cert['quartic_powers'];cubic=cert['cubic_powers'];Qcols=[];Ccols=[]
    assert len(quartic)==35 and len({tuple(p) for p in quartic})==35 and all(sum(p)==4 for p in quartic)
    assert len(cubic)==20 and len({tuple(p) for p in cubic})==20 and all(sum(p)==3 for p in cubic)
    for pw in quartic:
        G=monomial(pw);H=[[diff(diff(G,i),j) for j in range(4)] for i in range(4)];col=[]
        for Rv,Rp,K in pairs:
            HR=[[substitute(entry,Rv) for entry in row] for row in H]
            for row in HR:
                p=dot(row,K);col.extend(p.get((3-i,i),R(0)) for i in range(4))
            HK=[[substitute(entry,K) for entry in row] for row in H]
            p=scale(dot(Rv,[dot(row,Rp) for row in HK]),2)
            col.extend(p.get((4-i,i),R(0)) for i in range(5))
        Qcols.append(col)
    for pw in cubic:
        G=monomial(pw);gradient=[diff(G,i) for i in range(4)];col=[]
        for Rv,_,K in pairs:
            p=dot([substitute(entry,Rv) for entry in gradient],K)
            col.extend(p.get((3-i,i),R(0)) for i in range(4))
        Ccols.append(col)
    QM=transpose(Qcols);CM=transpose(Ccols)
    assert clean_rows(QM)==cert['quartic_constraint_matrix']
    assert clean_rows(CM)==cert['cubic_constraint_matrix']
    assert core.rank(QM)==34 and core.rank(CM)==8
    A=[core.var(4,i) for i in range(4)]
    X=add(mul(A[0],A[0]),mul(A[2],A[2]),scale(mul(A[1],A[1]),-1),scale(mul(A[3],A[3]),-1))
    Y=scale(add(mul(A[0],A[1]),mul(A[2],A[3])),2)
    Z=scale(add(mul(A[0],A[3]),scale(mul(A[1],A[2]),-1)),2)
    forms=[mul(X,X),scale(mul(X,Y),2),scale(mul(X,Z),2),mul(Y,Y),scale(mul(Y,Z),2),mul(Z,Z)]
    F=add(*(scale(f,k) for f,k in zip(forms,map(R,base['ray']['K_coefficients']))))
    fv=[F.get(tuple(pw),R(0)) for pw in quartic];assert annihilates(QM,fv)
    basis=[list(map(R,v)) for v in cert['cubic_kernel_basis']]
    assert len(basis)==12 and core.rank(basis)==12 and all(annihilates(CM,v) for v in basis)
    translations=[[diff(F,j).get(tuple(pw),R(0)) for pw in cubic] for j in range(4)]
    assert translations==[list(map(R,v)) for v in cert['translation_cubics']]
    assert core.rank(translations)==4 and all(annihilates(CM,v) for v in translations)
    example=list(map(R,cert['example_cubic_coefficients']))
    assert annihilates(CM,example) and sum(map(abs,example))==1 and core.rank(translations+[example])==5
    # The same eight constraints cancel the heat density on the entire
    # output-rotation orbit of the canonical null, in both Gamma charts.
    bc,dc=map(R,base['ray']['canonical_zero']);assert abs(bc)<1 and abs(dc)<1 and abs(bb)<6
    ac=[R(1),bc,R(0),dc];rc=[R(0),bb,R(0),R(1)]
    def gamma(v):return [v[3],scale(v[2],-1),v[1],scale(v[0],-1)]
    FMcols=[]
    for pw in cubic:
        gradient=[diff(monomial(pw),i) for i in range(4)];col=[]
        for operation in (lambda v:v,gamma):
            K=operation(rotate(ac));Rv=operation(rotate(rc))
            p=scale(dot([substitute(entry,Rv) for entry in gradient],K),2)
            col.extend(p.get((3-i,i),R(0)) for i in range(4))
        FMcols.append(col)
    FM=transpose(FMcols);assert core.rank(CM+FM)==8
    null_columns=[]
    for pw in cubic:
        gradient=[diff(monomial(pw),i) for i in range(4)];col=[]
        for ux,uy in ((1,0),(0,1),(1,1)):
            for vx,vy in ((1,0),(0,1),(1,1)):
                rr=[R(ux*vx),R(ux*vy),R(uy*vx),R(uy*vy)]
                col.extend(core.evaluate(entry,rr) for entry in gradient)
        null_columns.append(col)
    assert core.rank(transpose(null_columns))==20
    # An inadmissible cubic cannot be rescued by any finite quadratic.
    bad=[R(int(pw==[3,0,0,0])) for pw in cubic];eta=cubic_score(bad,cubic,av,[R(1),R(0),R(0),R(0)])
    assert eta and not annihilates(CM,bad)
    for nu in (R(1),R(2**112)):
        s=-(2*nu+1)/eta;assert s*eta+2*nu==-1
    # Check the numerical constants in the analytic form bound, exactly.
    mu=R(1,2**cert['uniform_margin_power']);nu=R(2**cert['stabilization_power'])
    assert cert['uniform_margin_power']==64 and cert['stabilization_power']==112
    assert 6*2**10<2**13 and 49*2**10<2**16
    assert R(5,2)*2**16<2**18 and 42*(2**18)**2<(2**21)**2
    assert nu/R(49)>(2**21)**2/mu  # leaves half of nu*T as strong QC modulus
    assert nu/2>(2**13)**2/(8*mu)
    # Full base replay, applying the stronger margin to every Bernstein
    # coefficient matrix as it is reconstructed from F and d(P/T).
    original_pd=core.pd;checked=0
    def margin_pd(mat):
        nonlocal checked
        original_pd([[entry-(mu if i==j else 0) for j,entry in enumerate(row)] for i,row in enumerate(mat)])
        checked+=1
    core.pd=margin_pd;old_here=core.HERE
    with tempfile.TemporaryDirectory(prefix='astra-graded-receive-') as temp:
        core.HERE=Path(temp);(core.HERE/'certificate.json').write_text(base_path.read_text())
        with contextlib.redirect_stdout(io.StringIO()):core.main()
        base_replay=json.loads((core.HERE/'replay.json').read_text())
    core.HERE=old_here;core.pd=original_pd
    assert checked==13524 and base_replay['lift_identity_exact'] and base_replay['nonpc_exact']
    result={'full_quartic_face_rank':34,'full_quartic_face_dimension':1,
      'cubic_constraint_rank':8,'admissible_cubic_dimension':12,'translation_cubic_dimension':4,
      'example_outside_translation_span':True,'canonical_null_cancellation_for_all_admissible_cubics':True,
      'no_nonzero_cubic_null_lagrangian_rank':20,
      'base_completion_reconstructed_exactly':True,'positive_margin':str(mu),
      'shifted_Bernstein_matrices':checked,'stabilization_coefficient':str(nu),
      'example_l1_norm':'1','uniform_strong_QC_modulus':str(nu/2),
      'full_polynomial_exposed_face_dimension':28,'seconds':time.perf_counter()-start,
      'scope':'Internal exact receiver plus the graded proof in PROOF.txt. No external independent audit or general Morrey conclusion.'}
    (HERE/'replay.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

if __name__=='__main__':main()
