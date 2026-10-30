"""Constructive exact classification for every diagonal PSD quadratic ray.

For every subset I of the four value coordinates, compute the entire
cubic space admitting F+C+nu sum_{i in I} A_i^2. Necessary completed
ROC cuts and sufficient globally bounded heat lifts coincide exactly.
No sampled polynomial positivity, optimizer, or work/ code is used.
"""
from pathlib import Path
from fractions import Fraction as R
from itertools import combinations,product
import importlib.util,json,time,sys,contextlib,io

HERE=Path(__file__).resolve().parent
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module
d=load('coordinate_completion_core',HERE/'receive.py');b=d.b
ca=load('coordinate_linear_algebra',HERE.parent/'shared_mode_gluing/capacity.py')
add,mul,scale,diff=d.add,d.mul,d.scale,d.diff
p1=(0,1,3,4);p2=(1,2,4,5);pairs4=list(combinations(range(4),2));pairs6=list(combinations(range(6),2))

def nullspace(A,n):
    rows=[list(row) for row in A];p=0;piv=[]
    for j in range(n):
        k=next((i for i in range(p,len(rows)) if rows[i][j]),None)
        if k is None:continue
        rows[p],rows[k]=rows[k],rows[p];v=rows[p][j];rows[p]=[a/v for a in rows[p]]
        for i in range(len(rows)):
            if i!=p and rows[i][j]:v=rows[i][j];rows[i]=[a-v*c for a,c in zip(rows[i],rows[p])]
        piv.append(j);p+=1
        if p==len(rows):break
    out=[]
    for j in range(n):
        if j not in piv:
            v=[R(0)]*n;v[j]=R(1)
            for i,k in enumerate(piv):v[k]=-rows[i][j]
            out.append(v)
    return out
def mat0(n,m=None):return [[R(0) for _ in range(n if m is None else m)] for _ in range(n)]
def embed(H):
    B=mat0(6)
    for ids in (p1,p2):
        for i in range(4):
            for j in range(4):B[ids[i]][ids[j]]+=H[i][j]
    return B
def main():
    start=time.perf_counter();base_receipt,(single,_,_,_,F)=d.derive()
    base=json.loads((HERE.parent/'hopf_structure/certificate.json').read_text());av=list(map(R,base['ray']['A0']));aa,bb,cc,dd=av;nulls=[av,[-bb,aa,dd,-cc]]
    powers=single['cubic_powers'];monomials=[{tuple(pw):R(1)} for pw in powers]
    qc=json.loads((HERE.parent/'quadratic_boundary/certificate.json').read_text());CB=[list(map(R,row)) for row in qc['normal_form_basis']]
    assert qc['cubic_powers']==powers and len(CB)==12 and b.rank(CB)==12
    polys=[{tuple(pw):co for pw,co in zip(powers,row) if co} for row in CB]
    def rotate(v,u):
        x,y=u;return [x*v[0]-y*v[2],x*v[1]-y*v[3],y*v[0]+x*v[2],y*v[1]+x*v[3]]
    # Verify the supplied twelve-dimensional source basis against the
    # actual eight defining polynomial constraints, independently of its name.
    x,y=b.var(2,0),b.var(2,1);zero={}
    for P in polys:
        for side in (0,1):
            Rp=[x,zero,y,zero] if side==0 else [zero,x,zero,y]
            kr=[add(scale(x,nulls[side][0]),scale(y,-nulls[side][2])),add(scale(x,nulls[side][1]),scale(y,-nulls[side][3])),add(scale(y,nulls[side][0]),scale(x,nulls[side][2])),add(scale(y,nulls[side][1]),scale(x,nulls[side][3]))]
            assert not add(*(mul(d.compose(diff(P,i),Rp),kr[i]) for i in range(4)))
    HF=[[diff(diff(F,i),j) for j in range(4)] for i in range(4)]
    # All closed linear two-forms, in exactly the published convention.
    wedges=[]
    for i,j in pairs4:
        W=mat0(6)
        for ii,jj,sign in ((p1[i],p2[j],1),(p2[j],p1[i],1),(p1[j],p2[i],-1),(p2[i],p1[j],-1)):W[ii][jj]+=R(sign,2)
        wedges.append(W)
    dep=[pairs4.index((i,j))*4+k for i,j,k in combinations(range(4),3)];free=[i for i in range(24) if i not in dep];V=mat0(24,20)
    for k,i in enumerate(free):V[i][k]=R(1)
    for i,j,k in combinations(range(4),3):V[pairs4.index((i,j))*4+k]=[a-c for a,c in zip(V[pairs4.index((i,k))*4+j],V[pairs4.index((j,k))*4+i])]
    assert all(V[pairs4.index((j,k))*4+i][l]-V[pairs4.index((i,k))*4+j][l]+V[pairs4.index((i,j))*4+k][l]==0 for i,j,k in combinations(range(4),3) for l in range(20))
    XB=[[[[R(0)]*80 for _ in range(6)] for _ in range(6)] for _ in range(4)]
    for a in range(4):
        for i in range(6):
            for j in range(6):
                for l in range(20):XB[a][i][j][l]=sum(V[p*4+a][l]*wedges[p][i][j]/2 for p in range(6))
        for l,(i,j) in enumerate(pairs6):XB[a][i][j][20+15*a+l]=R(1);XB[a][j][i][20+15*a+l]=R(-1)
    raw=[]
    for a in range(4):
        ea=[R(int(i==a)) for i in range(4)]
        raw.append([embed([[b.evaluate(diff(diff(P,i),j),ea)/2 for j in range(4)] for i in range(4)]) for P in monomials])
    E0=[];rhs0=[]
    for side in (0,1):
        for u in ((1,0),(0,1),(1,1)):
            Ar=rotate(nulls[side],u);kh=[R(0)]*6;kh[0 if side==0 else 2]=R(u[0]);kh[3 if side==0 else 5]=R(u[1])
            for j in range(6):
                E0.append([sum(kh[i]*Ar[a]*XB[a][i][j][l] for a in range(4) for i in range(6)) for l in range(80)])
                rhs0.append([-sum(kh[i]*Ar[a]*raw[a][k][i][j] for a in range(4) for i in range(6)) for k in range(20)])
    assert b.rank(E0)==28
    # Fixed ordinary/closed rank-one cuts. At acoustic roots, the four
    # deflated features have positive definite metric. Else HF_R is PD.
    directions=((1,0),(0,1),(1,1),(1,-1));cuts=[]
    ac=json.loads((HERE.parent/'acoustic_capacity/certificate.json').read_text())
    for u,xi in product(directions,repeat=2):
        Rv=[R(a*c) for a in u for c in xi];side=0 if xi[1]==0 else 1 if xi[0]==0 else None
        if side is None:
            b.pd([[b.evaluate(p,Rv) for p in row] for row in HF]);J=[[b.evaluate(diff(P,i),Rv) for P in polys] for i in range(4)]
        else:
            # Chosen acoustic xi is exactly the corresponding unit axis.
            assert xi in ((1,0),(0,1))
            K=rotate(nulls[side],u);Rp=[R(a*c) for a in u for c in ((0,1) if side==0 else (1,0))]
            perp=[rotate([R(int(i==j)) for i in range(4)],u) for j in range(3)]
            b.pd([[R(v) for v in row] for row in ac['acoustic_charts'][side]['deflated_Hessian_at_zero']])
            J=[[sum(K[i]*b.evaluate(diff(diff(P,i),j),Rv)*Rp[j] for i in range(4) for j in range(4)) for P in polys]]
            J += [[sum(v[i]*b.evaluate(diff(P,i),Rv) for i in range(4)) for P in polys] for v in perp]
        cuts.append((Rv,J))
    records=[];common_power=0
    for bits in product((0,1),repeat=4):
        active=[i for i,q in enumerate(bits) if q]
        J=[row for Rv,rows in cuts if all(not Rv[i] for i in active) for row in rows]
        nn=nullspace(J,12);CC=[[sum(z[k]*CB[k][i] for k in range(12)) for i in range(20)] for z in nn]
        for i,C in enumerate(CC):
            norm=sum(map(abs,C));assert norm>0;CC[i]=[v/norm for v in C]
        # Heat of sum active coordinate squares is diagonal. Its zero
        # columns are determined exactly by the two Hessian embeddings.
        heat=[0]*6
        for ids in (p1,p2):
            for i in active:heat[ids[i]]+=1
        kernel=[j for j,q in enumerate(heat) if not q]
        E=[row[:] for row in E0];rhs=[row[:] for row in rhs0]
        for a in range(4):
            for j in kernel:
                for i in range(6):E.append(XB[a][i][j][:]);rhs.append([-raw[a][k][i][j] for k in range(20)])
        if not CC:
            records.append({'active_coordinates':active,'cubic_dimension':0,'necessary_cut_rank':12,'heat_kernel_coordinates':kernel,'cubic_basis':[],'heat_lift_coefficients':[],'completion_power':0})
            continue
        target=[[sum(a*c for a,c in zip(row,C)) for C in CC] for row in rhs]
        sol,rank=ca.solve_range(E,target)
        assert ca.mm(E,sol)==target
        # Rebuild each lift, and verify every coefficient in the literal
        # symmetry/closure/kernel equations. Bound its coefficient l1 norm.
        m=R(0)
        for ic,C in enumerate(CC):
            Xa=[]
            for a in range(4):
                rawC=[[sum(C[k]*raw[a][k][i][j] for k in range(20)) for j in range(6)] for i in range(6)]
                XX=[[rawC[i][j]+sum(XB[a][i][j][l]*sol[l][ic] for l in range(80)) for j in range(6)] for i in range(6)]
                assert all(not XX[i][j] for i in range(6) for j in kernel)
                omega=[sum(V[p*4+a][l]*sol[l][ic] for l in range(20)) for p in range(6)]
                assert all(XX[i][j]+XX[j][i]==2*rawC[i][j]+sum(omega[p]*wedges[p][i][j] for p in range(6)) for i in range(6) for j in range(6))
                Xa.append(XX)
            for side in (0,1):
                for u in ((1,0),(0,1),(1,1)):
                    Ar=rotate(nulls[side],u);kh=[R(0)]*6;kh[0 if side==0 else 2]=R(u[0]);kh[3 if side==0 else 5]=R(u[1])
                    assert all(not sum(kh[i]*Ar[a]*Xa[a][i][j] for a in range(4) for i in range(6)) for j in range(6))
            eta0,zeta0=map(R,base['ray']['canonical_zero']);acanon=[R(1),eta0,R(0),zeta0];kcanon=[R(0),R(0),bb,R(0),R(0),R(1)]
            for gamma in (0,1):
                avv=acanon if not gamma else [acanon[3],-acanon[2],acanon[1],-acanon[0]]
                kvv=kcanon if not gamma else [kcanon[5],-kcanon[4],kcanon[3],kcanon[2],-kcanon[1],kcanon[0]]
                for u in ((1,0),(0,1),(1,1)):
                    Ar=rotate(avv,u);kh=[u[0]*kvv[i]-u[1]*kvv[i+3] for i in range(3)]+[u[1]*kvv[i]+u[0]*kvv[i+3] for i in range(3)]
                    assert all(not sum(kh[i]*Ar[a]*Xa[a][i][j] for a in range(4) for i in range(6)) for j in range(6))
            m=max(m,max(sum(abs(Xa[a][i][j]) for a in range(4)) for i in range(6) for j in range(6)))
        k=0
        while 2**k<m:k+=1
        power=84+2*k;common_power=max(common_power,power)
        assert R(2)**(power+1)>R(2)**83*m*m
        record={'active_coordinates':active,'cubic_dimension':len(CC),'necessary_cut_rank':12-len(CC),'heat_kernel_coordinates':kernel,'exact_heat_linear_rank':rank,'cubic_basis':[[str(v) for v in row] for row in CC],'heat_lift_coefficients':[[str(v) for v in row] for row in sol],'exact_lift_entry_l1_bound':str(m),'completion_power':power}
        records.append(record)
    summary=[{k:row[k] for k in ('active_coordinates','cubic_dimension','necessary_cut_rank','heat_kernel_coordinates','completion_power')} for row in records]
    result={'coordinate_order':['a','b','c','d'],'all_sixteen_diagonal_quadratic_supports_classified':True,'leading_uniform_margin_power':64,'common_completion_power':common_power,'records':records,'seconds':time.perf_counter()-start,'scope':'For each support I, exactly these cubics admit some finite global ROC completion by nu*sum_I A_i^2, and every such cubic has the constructed global QC completion. Threshold-optimal nu and arbitrary nondiagonal quadratics are not classified.'}
    if '--replay-leading' in sys.argv:
        with contextlib.redirect_stdout(io.StringIO()):d.g.main()
        result['leading_shifted_Bernstein_matrices_replayed']=13524
    (HERE/'coordinate_family.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'supports':summary,'common_completion_power':common_power,'seconds':result['seconds'],'leading_shifted_Bernstein_matrices_replayed':result.get('leading_shifted_Bernstein_matrices_replayed'),'scope':result['scope']},indent=2),flush=True)
if __name__=='__main__':main()
