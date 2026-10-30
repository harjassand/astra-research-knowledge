"""Exact receiver for completion by the rank-two quadratic b^2+c^2.

No numerical optimizer or work/ module is imported. Rebuild the cubic
space, all closed forms, every heat-lift identity, and the bound constants.
With --replay-leading, also reconstruct all 13,524 shifted leading signs.
The global argument and its actual-gradient quantifier are in PROOF.txt.
"""
from pathlib import Path
from fractions import Fraction as R
from itertools import combinations
import importlib.util,json,time,sys

HERE=Path(__file__).resolve().parent
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module
b=load('degenerate_angular_core',HERE.parent/'hopf_structure/receive.py')
g=load('degenerate_graded_core',HERE.parent/'graded_stabilization/receive.py')
add,mul,scale,diff=b.add,b.mul,b.scale,b.diff
def compose(p,images):return g.substitute(p,images)
def dotpoly(v,w):return add(*(mul(x,y) for x,y in zip(v,w)))
def zero_matrix(n,m=None):return [[R(0) for _ in range(n if m is None else m)] for _ in range(n)]
def apply_matrix(A,v):return [sum((a*x for a,x in zip(row,v)),R(0)) for row in A]

def derive():
    cert=json.loads((HERE/'certificate.json').read_text())
    base=json.loads((HERE.parent/'hopf_structure/certificate.json').read_text())
    powers=cert['cubic_powers'];assert len(powers)==20 and len({tuple(p) for p in powers})==20 and all(sum(p)==3 for p in powers)
    CC=[list(map(R,row)) for row in cert['cubic_basis']]
    assert len(CC)==4 and b.rank(CC)==4 and all(sum(map(abs,row))==1 for row in CC)
    cubics=[{tuple(pw):co for pw,co in zip(powers,row) if co} for row in CC]
    av=list(map(R,base['ray']['A0']));aa,bb,cc,dd=av;nulls=[av,[-bb,aa,dd,-cc]]
    x,y=b.var(2,0),b.var(2,1);z={}
    def rotate(v):return [add(scale(x,v[0]),scale(y,-v[2])),add(scale(x,v[1]),scale(y,-v[3])),add(scale(y,v[0]),scale(x,v[2])),add(scale(y,v[1]),scale(x,v[3]))]
    columns=[];vcolumns=[]
    roots=[[R(1),R(0),R(0),R(0)],[R(0),R(0),R(0),R(1)]]
    root_nulls=[nulls[0],[-nulls[1][2],-nulls[1][3],nulls[1][0],nulls[1][1]]]
    tangent=[[R(0),R(1),R(0),R(0)],[R(0),R(0),R(1),R(0)]]
    for pw in powers:
        P={tuple(pw):R(1)};grad=[diff(P,i) for i in range(4)];row=[]
        for side in (0,1):
            root=[x,z,y,z] if side==0 else [z,x,z,y]
            pp=dotpoly([compose(q,root) for q in grad],rotate(nulls[side]))
            row.extend(pp.get((3-i,i),R(0)) for i in range(4))
        vcolumns.append(row[:])
        for side in (0,1):
            row.extend(b.evaluate(q,roots[side]) for q in grad)
            H=[[b.evaluate(diff(q,j),roots[side]) for j in range(4)] for q in grad]
            row.append(sum(root_nulls[side][i]*H[i][j]*tangent[side][j] for i in range(4) for j in range(4)))
        columns.append(row)
    conditions=list(map(list,zip(*columns)));vconditions=list(map(list,zip(*vcolumns)))
    assert b.rank(vconditions)==8 and b.rank(conditions)==16
    assert all(all(sum(a*c for a,c in zip(row,cv))==0 for row in conditions) for cv in CC)
    # Reconstruct the leading polynomial, and prove no translation cubic
    # lies in this four-dimensional boundary space.
    A=[b.var(4,i) for i in range(4)]
    X=add(mul(A[0],A[0]),mul(A[2],A[2]),scale(mul(A[1],A[1]),-1),scale(mul(A[3],A[3]),-1))
    Y=scale(add(mul(A[0],A[1]),mul(A[2],A[3])),2)
    Z=scale(add(mul(A[0],A[3]),scale(mul(A[1],A[2]),-1)),2)
    forms=[mul(X,X),scale(mul(X,Y),2),scale(mul(X,Z),2),mul(Y,Y),scale(mul(Y,Z),2),mul(Z,Z)]
    F=add(*(scale(f,k) for f,k in zip(forms,map(R,base['ray']['K_coefficients']))))
    translations=[[diff(F,j).get(tuple(pw),R(0)) for pw in powers] for j in range(4)]
    assert b.rank(CC+translations)==8
    p1=(0,1,3,4);p2=(1,2,4,5);pairs4=list(combinations(range(4),2));pairs6=list(combinations(range(6),2))
    wedges=[]
    for i,j in pairs4:
        W=zero_matrix(6)
        for a0,b0,sign in ((p1[i],p2[j],1),(p2[j],p1[i],1),(p1[j],p2[i],-1),(p2[i],p1[j],-1)):
            W[a0][b0]+=R(sign,2)
        wedges.append(W)
    dependent=[pairs4.index((i,j))*4+k for i,j,k in combinations(range(4),3)]
    free=[i for i in range(24) if i not in dependent]
    assert len(free)==20
    coefficients=[list(map(R,row)) for row in cert['heat_lift_coefficients']]
    assert len(coefficients)==80 and all(len(row)==4 for row in coefficients)
    allX=[];allOmega=[];m=R(0)
    for ic,P in enumerate(cubics):
        v=[row[ic] for row in coefficients];omega=[R(0)]*24
        for k,i in enumerate(free):omega[i]=v[k]
        for i,j,k in combinations(range(4),3):omega[pairs4.index((i,j))*4+k]=omega[pairs4.index((i,k))*4+j]-omega[pairs4.index((j,k))*4+i]
        assert all(omega[pairs4.index((j,k))*4+i]-omega[pairs4.index((i,k))*4+j]+omega[pairs4.index((i,j))*4+k]==0 for i,j,k in combinations(range(4),3))
        XX=[]
        for a in range(4):
            ea=[R(int(a==i)) for i in range(4)]
            H=[[b.evaluate(diff(diff(P,i),j),ea) for j in range(4)] for i in range(4)]
            raw=zero_matrix(6)
            for ids in (p1,p2):
                for i in range(4):
                    for j in range(4):raw[ids[i]][ids[j]]+=H[i][j]
            corrected=[[raw[i][j]+sum(omega[p*4+a]*W[i][j] for p,W in enumerate(wedges)) for j in range(6)] for i in range(6)]
            Xa=[[q/2 for q in row] for row in corrected]
            for k,(i,j) in enumerate(pairs6):Xa[i][j]+=v[20+15*a+k];Xa[j][i]-=v[20+15*a+k]
            assert all(Xa[i][j]+Xa[j][i]==corrected[i][j] for i in range(6) for j in range(6))
            assert all(Xa[i][j]==0 for i in range(6) for j in (0,5))
            XX.append(Xa)
        for side in (0,1):
            Ar=rotate(nulls[side]);kh=[{} for _ in range(6)];kh[0 if side==0 else 2]=x;kh[3 if side==0 else 5]=y
            for j in range(6):
                assert not add(*(scale(mul(kh[i],Ar[a]),XX[a][i][j]) for a in range(4) for i in range(6)))
        # Directly check the actual canonical null in both Gamma charts,
        # before any normalization of the output multiplier.
        eta0,zeta0=map(R,base['ray']['canonical_zero'])
        assert eta0==-(aa*bb+cc)/(1+bb*bb) and zeta0==(bb*cc-aa)/(1+bb*bb)
        ac=[R(1),eta0,R(0),zeta0];kc=[R(0),R(0),bb,R(0),R(0),R(1)]
        for gamma in (0,1):
            ar=ac if not gamma else [ac[3],-ac[2],ac[1],-ac[0]]
            kr=kc if not gamma else [kc[5],-kc[4],kc[3],kc[2],-kc[1],kc[0]]
            Ar=rotate(ar)
            kh=[add(scale(x,kr[i]),scale(y,-kr[i+3])) for i in range(3)]+[add(scale(y,kr[i]),scale(x,kr[i+3])) for i in range(3)]
            for j in range(6):assert not add(*(scale(mul(kh[i],Ar[a]),XX[a][i][j]) for a in range(4) for i in range(6)))
        # This bound is on literal coefficient l1 norms, with exact rationals.
        m=max(m,max(sum(abs(XX[a][i][j]) for a in range(4)) for i in range(6) for j in range(6)))
        allX.append(XX);allOmega.append(omega)
    k=0
    while 2**k<m:k+=1
    power=84+2*k
    assert cert['leading_uniform_margin_power']==64 and cert['completion_power']==power,(power,str(m))
    # Local: ||N||^2 <=42*(28mL)^2; T^2<=9. Away: ||X||<=12mL.
    assert 9*42*28**2<2**19 and 9*12**2<2**11
    assert R(2)**(power+1)>2**(64+19)*m*m
    # The prescribed quadratic is exactly b^2+c^2; its heat kernel is
    # span(e0,e5). All cross columns on this kernel were verified above.
    assert cert['quadratic_powers']==[[0,2,0,0],[0,0,2,0]]
    return {'admissible_cubic_dimension':4,'full_cubic_constraint_rank':16,'isotropic_admissibility_rank':8,'no_nonzero_translation_in_boundary_space':True,'closed_linear_two_forms_verified':4,'heat_cross_columns_0_and_5_identically_zero':True,'all_output_acoustic_row_identities':True,'normalized_cubic_basis_l1':'1','exact_lift_entry_l1_bound':str(m),'lift_entry_bound_power':k,'completion_power':power,'completion_coefficient':str(2**power),'leading_margin':str(R(1,2**64))},(cert,cubics,allX,allOmega,F)

def main():
    start=time.perf_counter();result,_=derive()
    if '--replay-leading' in sys.argv:
        # The sibling receiver reconstructs F, primitive, symmetries,
        # factorization, coverage, and EVERY shifted sign independently.
        import contextlib,io
        with contextlib.redirect_stdout(io.StringIO()):g.main()
        replay=json.loads((HERE.parent/'graded_stabilization/replay.json').read_text())
        assert replay['shifted_Bernstein_matrices']==13524 and replay['positive_margin']==str(R(1,2**64))
        result['leading_shifted_Bernstein_matrices_replayed']=13524
    result.update({'seconds':time.perf_counter()-start,'scope':'Exact algebra and analytic global form bound in PROOF.txt. The previously acquired leading margin is re-received with --replay-leading. Global QC and ROC completion are characterized only along positive multiples of b^2+c^2.'})
    (HERE/'replay.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
