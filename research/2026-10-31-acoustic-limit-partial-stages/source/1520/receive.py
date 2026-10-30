"""Exact acoustic-limit receiver: all eight nontranslation modes are jets."""
from pathlib import Path
from fractions import Fraction as R
import importlib.util,json,time,contextlib,io
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('shared_core',HERE.parent/'shared_mode_gluing/receive.py');r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
spec=importlib.util.spec_from_file_location('capacity_core',HERE.parent/'shared_mode_gluing/capacity.py');ca=importlib.util.module_from_spec(spec);spec.loader.exec_module(ca)
b=r.b;dot=r.dot;quadratic=r.quadratic

def source():
    F,_,T=r.m.acquired();qc=json.loads((HERE.parent/'quadratic_boundary/certificate.json').read_text());hc=json.loads((HERE.parent/'hopf_structure/certificate.json').read_text())
    basis=[list(map(R,row)) for row in qc['normal_form_basis']];powers=qc['cubic_powers'];polys=[{tuple(pw):co for pw,co in zip(powers,row) if co} for row in basis]
    HF=[[b.diff(b.diff(F,i),j) for j in range(4)] for i in range(4)];av=list(map(R,hc['ray']['A0']));aa,bb,cc,dd=av
    return F,T,basis,powers,polys,HF,[av,[-bb,aa,dd,-cc]]

def rotate_poly(v,x,y):
    return [b.add(b.scale(x,v[0]),b.scale(y,-v[2])),b.add(b.scale(x,v[1]),b.scale(y,-v[3])),b.add(b.scale(y,v[0]),b.scale(x,v[2])),b.add(b.scale(y,v[1]),b.scale(x,v[3]))]

def derive():
    F,T,basis,powers,polys,HF,nulls=source();x,y=b.var(2,0),b.var(2,1);zero={};operator=[];records=[]
    for side,K in enumerate(nulls):
        def hco(poly,k):return sum((v for pw,v in poly.items() if not pw[2] and not pw[3] and pw[1-side]==k),R(0))
        Hco=[[[hco(p,k) for p in row] for row in HF] for k in range(3)]
        assert all(dot(row,K)==0 for row in Hco[0]) and quadratic(Hco[1],K)==0
        perp=[[R(int(i==j)) for i in range(4)] for j in range(3)]
        D=[[quadratic(Hco[0],v,w) for w in perp] for v in perp];bv=[quadratic(Hco[1],K,v) for v in perp];aa=quadratic(Hco[2],K)
        Di_b=r.m.linear_solve(D,bv);sigma=aa-dot(bv,Di_b);assert sigma>0
        Hhat=[[aa]+bv]+[[bv[i]]+row for i,row in enumerate(D)];b.pd(Hhat);b.pd(D)
        Dinv,_=ca.solve_range(D,[[R(int(i==j)) for j in range(3)] for i in range(3)])
        Hinv,_=ca.solve_range(Hhat,[[R(int(i==j)) for j in range(4)] for i in range(4)])
        rootimages=[x,zero,y,zero] if side==0 else [zero,x,zero,y];derivimages=[zero,x,zero,y] if side==0 else [x,zero,y,zero]
        Kimages=rotate_poly(K,x,y);perpimages=[rotate_poly(v,x,y) for v in perp];coeffs=[];betas=[];gammas=[];perpfeatures=[]
        for P in polys:
            grad=[r.compose(b.diff(P,i),rootimages,2) for i in range(4)]
            assert not b.add(*(b.mul(Kimages[j],grad[j]) for j in range(4)))
            gp=[b.add(*(b.mul(v[j],grad[j]) for j in range(4))) for v in perpimages]
            gamma={}
            for i in range(4):
                for j in range(4):gamma=b.add(gamma,b.mul(Kimages[i],b.mul(r.compose(b.diff(b.diff(P,i),j),rootimages,2),derivimages[j])))
            beta=b.add(gamma,*(b.scale(g,-co) for g,co in zip(gp,Di_b)))
            assert all(sum(pw)==3 for pw in beta);coeffs.append([beta.get((3-j,j),R(0)) for j in range(4)]);betas.append(beta);gammas.append(gamma);perpfeatures.append(gp)
        # The whole matrix-valued cost jump is proved as a polynomial identity
        # in the output direction. The common |u|^4 denominator is omitted.
        for i in range(12):
            for j in range(12):
                gi=[gammas[i]]+perpfeatures[i];gj=[gammas[j]]+perpfeatures[j]
                limit=b.add(*(b.scale(b.mul(gi[a],gj[c]),Hinv[a][c]) for a in range(4) for c in range(4)))
                ordinary=b.add(*(b.scale(b.mul(perpfeatures[i][a],perpfeatures[j][c]),Dinv[a][c]) for a in range(3) for c in range(3)))
                assert not b.add(limit,b.scale(ordinary,-1),b.scale(b.mul(betas[i],betas[j]),-1/sigma))
        rows=list(map(list,zip(*coeffs)));operator+=rows;assert all(not row[j] for row in rows for j in range(4))
        records.append({'side':side,'null':list(map(str,K)),'sigma':str(sigma),'deflated_Hessian_at_zero':[list(map(str,row)) for row in Hhat],'charge_on_normal_basis':[list(map(str,row)) for row in rows]})
    M=[row[4:] for row in operator];assert b.rank(M)==8
    inverse,_=ca.solve_range(M,[[R(int(i==j)) for j in range(8)] for i in range(8)])
    jetbasis=[[sum(inverse[i][j]*basis[i+4][k] for i in range(8)) for k in range(20)] for j in range(8)]
    return {'charge_coefficient_powers':[[3-j,j] for j in range(4)],'jet_operator_on_normal_basis':[list(map(str,row)) for row in operator],'quotient_rank':8,'acoustic_charts':records,'unit_charge_basis':[list(map(str,row)) for row in jetbasis],'charge_matrix_inverse':[list(map(str,row)) for row in inverse]}

def main():
    start=time.perf_counter()
    with contextlib.redirect_stdout(io.StringIO()):r.base.main()
    cert=json.loads((HERE/'certificate.json').read_text());derived=derive();assert cert==derived
    result={'full_admissible_cubic_dimension':12,'acoustic_limit_charge_rank':8,'charge_kernel_exactly_four_translations':True,'binary_cubic_charge_polynomials':2,'matrix_valued_jump_identities_in_all_output_directions':2,'positive_deflated_acoustic_Hessians':2,'unit_charge_basis_reconstructed':True,'kernel_and_duality_scope':'The continuous closed kernel includes the acoustic limits; actual pseudoinverse values at the roots remain distinct.','full_face_QC':'NOT_RESOLVED','seconds':time.perf_counter()-start}
    (HERE/'replay.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
