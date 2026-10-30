"""Stdlib symbolic receiver for an entire parameter family of full faces.

Reconstructs the acoustic coefficient maps, proves the determinant identities
by exact degree-bounded interpolation, and replays the primary-source
closed-form heat certificate as a polynomial identity in BOTH parameters.
"""
from fractions import Fraction as R
from pathlib import Path
from math import lcm
import importlib.util,json,time
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('core',HERE.parent/'hopf_structure/receive.py');b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
add,mul,scale,diff=b.add,b.mul,b.scale,b.diff
def constant(n,c=1):return {(0,)*n:R(c)} if c else {}
def powpoly(p,n):
    ans=constant(len(next(iter(p))) if p else 1)
    for _ in range(n):ans=mul(ans,p)
    return ans
def substitute(p,images,n):
    ans={}
    for powers,co in p.items():
        term=constant(n,co)
        for v,power in zip(images,powers):
            for _ in range(power):term=mul(term,v)
        ans=add(ans,term)
    return ans
def determinant(mat):
    n=len(mat);den=lcm(*(v.denominator for row in mat for v in row));a=[[int(v*den) for v in row] for row in mat];last=1;sign=1
    for k in range(n-1):
        pivot=next((i for i in range(k,n) if a[i][k]),None)
        if pivot is None:return R(0)
        if pivot!=k:a[k],a[pivot]=a[pivot],a[k];sign=-sign
        val=a[k][k]
        for i in range(k+1,n):
            for j in range(k+1,n):
                value=a[i][j]*val-a[i][k]*a[k][j];assert value%last==0;a[i][j]=value//last
        last=val
    return R(sign*a[-1][-1],den**n)
def family():
    A=[b.var(5,i) for i in range(4)];z=b.var(5,4);T=add(*(mul(v,v) for v in A));D=add(mul(A[0],A[3]),scale(mul(A[1],A[2]),-1))
    F=add(mul(T,T),scale(mul(mul(z,T),D),-4),mul(add(scale(mul(z,z),6),constant(5,-2)),mul(D,D)))
    theta=[scale(A[2],-1),scale(A[3],-1),A[0],A[1]];zeta=[scale(A[1],-1),A[0],scale(A[3],-1),A[2]]
    q1=add(scale(mul(z,T),3),scale(mul(add(constant(5),scale(mul(z,z),-2)),D),6))
    q2=add(scale(T,3),scale(mul(z,D),-6));P=[add(mul(q1,u),mul(q2,v)) for u,v in zip(theta,zeta)]
    return A,z,F,P
def coefficient_polynomial(p,pw):return {(e[4],):co for e,co in p.items() if e[:4]==tuple(pw)}
def main():
    start=time.perf_counter();cert=json.loads((HERE/'certificate.json').read_text());A,z,F,P=family()
    assert [coefficient_polynomial(F,pw) for pw in cert['quartic_powers']]==[b.literal(p,1) for p in cert['F']]
    trans=[[coefficient_polynomial(diff(F,i),pw) for pw in cert['cubic_powers']] for i in range(4)]
    assert trans==[[b.literal(p,1) for p in col] for col in cert['translation_cubics']]
    x,y,s,t,zz=[b.var(5,i) for i in range(5)];Rv=[mul(x,s),mul(x,t),mul(y,s),mul(y,t)]
    K=[add(mul(mul(zz,x),s),mul(y,t)),add(mul(mul(zz,x),t),scale(mul(y,s),-1)),
       add(mul(mul(zz,y),s),scale(mul(x,t),-1)),add(mul(mul(zz,y),t),mul(x,s))]
    images=Rv+[zz]
    def coefficients(p):
        assert all(e[0]+e[1]==3 and e[2]+e[3]==3 for e in p)
        return [{(e[4],):c for e,c in p.items() if e[:4]==(3-i,i,3-j,j)} for i in range(4) for j in range(4)]
    Ccols=[];Qcols=[]
    for pw in cert['cubic_powers']:
        G={tuple(pw)+(0,):R(1)};score=add(*(mul(substitute(diff(G,j),images,5),K[j]) for j in range(4)));Ccols.append(coefficients(score))
    for pw in cert['quartic_powers']:
        G={tuple(pw)+(0,):R(1)};col=[]
        for i in range(4):col.extend(coefficients(add(*(mul(substitute(diff(diff(G,i),j),images,5),K[j]) for j in range(4)))))
        Qcols.append(col)
    CM=[list(row) for row in zip(*Ccols)];QM=[list(row) for row in zip(*Qcols)]
    assert CM==[[b.literal(p,1) for p in row] for row in cert['cubic_matrix']]
    assert QM==[[b.literal(p,1) for p in row] for row in cert['quartic_matrix']]
    for row in CM:
        for column in trans:assert not add(*(mul(p,q) for p,q in zip(row,column)))
    for row in QM:assert not add(*(mul(p,b.literal(q,1)) for p,q in zip(row,cert['F'])))
    # Exact determinant identities with explicit degree bounds.
    z1=b.var(1,0);z2=mul(z1,z1);d1=add(z2,constant(1,-1));d3=add(scale(z2,9),constant(1,-1))
    facts={'cubic_minor':scale(mul(powpoly(d1,2),powpoly(d3,4)),81),
           'quartic_minor':scale(mul(powpoly(d1,4),powpoly(d3,7)),-6347497291776),
           'translation_minor':scale(powpoly(d1,2),256)}
    matrices={'cubic_minor':CM,'quartic_minor':QM,'translation_minor':[list(row) for row in zip(*trans)]};checks=0
    for name,mat in matrices.items():
        info=cert[name];poly=b.literal(info['polynomial'],1);assert poly==facts[name]
        sub=[[mat[i][j] for j in info['columns']] for i in info['rows']]
        degree=len(sub)*max((e[0] for row in sub for p in row for e in p),default=0)
        assert max(e[0] for e in poly)<=degree
        for value in range(degree+1):
            numeric=[[b.evaluate(p,[R(value)]) for p in row] for row in sub]
            assert determinant(numeric)==b.evaluate(poly,[R(value)]);checks+=1
    # The acoustic Hessian at E11 proves ROC for |z|<=1.
    HF=[[diff(diff(F,i),j) for j in range(4)] for i in range(4)]
    atR=[constant(1),{},{},{},z1];H0=[[substitute(p,atR,1) for p in row] for row in HF]
    expected=[[constant(1,12),{},{},scale(z1,-12)],
      [{},constant(1,4),scale(z1,4),{}],[{},scale(z1,4),constant(1,4),{}],
      [scale(z1,-12),{},{},scale(z2,12)]];assert H0==expected
    # Rotation invariance of F AND the actual cubic primitive.
    actions=[([scale(A[2],-1),scale(A[3],-1),A[0],A[1]],[P[2],P[3],scale(P[0],-1),scale(P[1],-1)]),
             ([scale(A[1],-1),A[0],scale(A[3],-1),A[2]],[P[1],scale(P[0],-1),P[3],scale(P[2],-1)])]
    for vector,extra in actions:
        assert not add(*(mul(diff(F,j),vector[j]) for j in range(4)))
        for i in range(4):assert not add(*(mul(diff(P[i],j),vector[j]) for j in range(4)),extra[i])
    # Rebuild d alpha and the compatible heat density, then identify a
    # sum of squares polynomially in z and the signed singular ratio rho.
    p1=(0,1,3,4);p2=(1,2,4,5);B=[[{} for _ in range(6)] for _ in range(6)]
    for mapping in (p1,p2):
        for i in range(4):
            for j in range(4):B[mapping[i]][mapping[j]]=add(B[mapping[i]][mapping[j]],HF[i][j])
    for i in range(4):
        for j in range(4):
            w=scale(add(diff(P[j],i),scale(diff(P[i],j),-1)),R(1,2))
            B[p1[i]][p2[j]]=add(B[p1[i]][p2[j]],w);B[p2[j]][p1[i]]=add(B[p2[j]][p1[i]],w)
    rho,ss=b.var(2,0),b.var(2,1);diag=[constant(2),{},{},rho,ss]
    B=[[substitute(p,diag,2) for p in row] for row in B]
    L=add(constant(2),scale(mul(ss,rho),-1));M=add(rho,scale(ss,-1));delta=add(constant(2),scale(mul(ss,ss),-1))
    terms=[(constant(2,3),[scale(L,2),{},L,{},M,{}]),(constant(2),[{},{},L,{},scale(M,-1),{}]),
      (scale(delta,4),[{},{},rho,{},constant(2,-1),{}]),
      (constant(2,3),[{},L,{},M,{},scale(M,2)]),(constant(2),[{},L,{},scale(M,-1),{},{}]),
      (scale(delta,4),[{},rho,{},constant(2,-1),{},{}])]
    sos=[[add(*(mul(weight,mul(v[i],v[j])) for weight,v in terms)) for j in range(6)] for i in range(6)]
    assert B==sos
    # Literal exceptional ranks are scoped failures of cubic rigidity.
    for point,expected_ranks in cert['exceptional_ranks'].items():
        point=R(point)
        assert b.rank([[b.evaluate(p,[point]) for p in row] for row in CM])==expected_ranks['cubic']
        assert b.rank([[b.evaluate(p,[point]) for p in row] for row in QM])==expected_ranks['quartic']
    result={'full_quartic_acoustic_map_rank':34,'cubic_acoustic_map_rank':16,'translation_rank':4,
      'parameter_wide_minor_identities':True,'exact_interpolation_determinants':checks,
      'quartic_ROC_identity':True,'closed_primitive_and_both_rotation_symmetries':True,
      'heat_sum_of_squares_identity_for_all_parameters':True,'common_polynomial_face_dimension':20,
      'scope_parameters':'-1<z<1, z != -1/3,1/3',
      'nonPC_parameters':'1/3<abs(z)<1, positive leading coefficient, every finite lower tail',
      'exceptional_cubic_kernel_dimensions':{'z=1/3':8,'z=-1/3':8},
      'seconds':time.perf_counter()-start,
      'scope':'Internal symbolic replay plus the theorem in PROOF.txt. The family includes an exact primary-source QC primitive; no priority or general Morrey claim.'}
    (HERE/'replay.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
