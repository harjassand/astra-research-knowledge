"""Exact receiver for the actual ROC boundary and resonance quotient.

No solvers, floats, work-directory imports, or arbitrary moment measures.
Every variational field is an explicit finite sine series.
"""
from fractions import Fraction as R
from pathlib import Path
import importlib.util,json,time
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('shapes',HERE/'check_shape.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
b=m.core
def substitute(p,images,n):
    out={}
    for pw,c in p.items():
        term={(0,)*n:c}
        for z,e in zip(images,pw):
            for _ in range(e):term=b.mul(term,z)
        out=b.add(out,term)
    return out
def coefficient_vector(p,powers):return [p.get(tuple(pw),R(0)) for pw in powers]
def main():
    start=time.perf_counter();cert=json.loads((HERE/'certificate.json').read_text());F,C,T=m.acquired()
    old=json.loads((HERE.parent/'hopf_structure/certificate.json').read_text());gd=json.loads((HERE.parent/'graded_stabilization/certificate.json').read_text())
    A=[b.var(4,i) for i in range(4)]
    X=b.add(b.mul(A[0],A[0]),b.mul(A[2],A[2]),b.scale(b.mul(A[1],A[1]),-1),b.scale(b.mul(A[3],A[3]),-1))
    Y=b.scale(b.add(b.mul(A[0],A[1]),b.mul(A[2],A[3])),2)
    Z=b.scale(b.add(b.mul(A[0],A[3]),b.scale(b.mul(A[1],A[2]),-1)),2)
    forms=[b.mul(X,X),b.scale(b.mul(X,Y),2),b.scale(b.mul(X,Z),2),b.mul(Y,Y),b.scale(b.mul(Y,Z),2),b.mul(Z,Z)]
    assert F==b.add(*(b.scale(f,k) for f,k in zip(forms,map(R,old['ray']['K_coefficients']))))
    HF=[[b.diff(b.diff(F,i),j) for j in range(4)] for i in range(4)]
    t=b.var(1,0);row=[{(0,):R(1)},t,{},{}]
    H=[[substitute(p,row,1) for p in rr] for rr in HF]
    for size in range(1,5):
        minor=b.determinant_poly([rr[:size] for rr in H[:size]]);power=min(e[0] for e in minor)
        rest={(e[0]-power,):v for e,v in minor.items()}
        assert power==([0,0,0,2][size-1]) and b.root_count(rest)==0 and rest.get((0,),0)>0
    determinant=b.determinant_poly(H);delta={(e[0]-2,):v for e,v in determinant.items()};assert min(e[0] for e in determinant)==2
    assert delta==b.literal(cert['delta'],1)
    adj=[[b.scale(b.determinant_poly([[H[rr][cc] for cc in range(4) if cc!=i] for rr in range(4) if rr!=j]),(-1)**(i+j)) for j in range(4)] for i in range(4)]
    tt,xx,yy=[b.var(3,i) for i in range(3)];Rv=[xx,b.mul(xx,tt),yy,b.mul(yy,tt)]
    grad=[substitute(b.diff(C,i),Rv,3) for i in range(4)]
    h=[b.add(b.mul(xx,grad[0]),b.mul(yy,grad[2])),b.add(b.mul(xx,grad[1]),b.mul(yy,grad[3])),
       b.add(b.scale(b.mul(yy,grad[0]),-1),b.mul(xx,grad[2])),b.add(b.scale(b.mul(yy,grad[1]),-1),b.mul(xx,grad[3]))]
    terms=[]
    for i in range(4):
        for j in range(4):terms.append(b.mul(b.mul(h[i],h[j]),{(e[0],0,0):v for e,v in adj[i][j].items()}))
    raw=b.add(*terms);assert all(e[0]>=2 for e in raw)
    N={(e[0]-2,e[1],e[2]):v for e,v in raw.items()}
    assert max(e[0] for e in N)<=6 and all(e[1]+e[2]==6 for e in N)
    assert N==b.literal(cert['regularized_numerator'],3)
    # A global positive Gram at the proposed upper coefficient.
    upper=cert['ROC_upper'];nu=R(upper['nu']);assert nu==1859
    poly={}
    for (ti,),co in delta.items():
        for ti2 in (ti,ti+2):
            for yp,bc in ((0,1),(2,3),(4,3),(6,1)):
                key=(ti2,6-yp,yp);poly[key]=poly.get(key,R(0))+2*nu*co*bc
    poly=b.add(poly,b.scale(N,-1));scale=R(upper['scale']);Gram=[list(map(R,rr)) for rr in upper['Gram']]
    b.pd(Gram);reconstruction={};mon=upper['Gram_monomials']
    for i in range(16):
        for j in range(16):
            e=tuple(x+y for x,y in zip(mon[i],mon[j]));reconstruction[e]=reconstruction.get(e,R(0))+scale*Gram[i][j]
    assert poly=={e:c for e,c in reconstruction.items() if c}
    # An exact lower obstruction, then a DIRECT negative variational test.
    u=list(map(R,cert['lower_rank_one_output']));xi=list(map(R,cert['lower_rank_one_spatial']));tau=xi[1]/xi[0]
    ratio=b.evaluate(N,[tau,*u])/(2*(sum(z*z for z in u))**3*(1+tau*tau)*b.evaluate(delta,[tau]))
    assert ratio==R(cert['exact_ratio_at_lower_direction']) and ratio>R(cert['ROC_lower'])
    calibration=m.shape_operation(F,C,m.scale(T,R(cert['ROC_lower'])),cert['lower_calibration_modes'])
    assert calibration['all_means_and_amplitudes_nonnegative_for_this_shape'] is False and R(calibration['actual_energy_gap'])<0
    # Reconstruct each cubic functional from an actual compatible field.
    powers=cert['cubic_powers'];rows=[]
    for case in cert['resonance_fields']:
        G=m.gradient(case['modes']);HH=[[m.average(p,G) for p in rr] for rr in HF]
        v=[m.average(b.diff(F,i),G) for i in range(4)];sv=m.linear_solve(HH,v);functional=[]
        for pw in powers:
            p={tuple(pw):R(1)};w=[m.average(b.diff(p,i),G) for i in range(4)]
            functional.append(m.average(p,G)-m.dot(sv,w))
        assert functional==list(map(R,case['functional']));rows.append(functional)
    basis=[list(map(R,v)) for v in gd['cubic_kernel_basis']];translations=[coefficient_vector(b.diff(F,i),powers) for i in range(4)]
    assert b.rank(translations)==4
    assert all(m.dot(row,v)==0 for row in rows for v in translations)
    assert b.rank([[m.dot(row,v) for v in basis] for row in rows])==8
    assert [list(map(R,v)) for v in cert['normal_form_basis'][:4]]==translations
    nf=[list(map(R,v)) for v in cert['normal_form_basis']];op=[list(map(R,v)) for v in cert['normal_form_operator']]
    assert b.rank(nf)==12
    assert [[m.dot(row,v) for v in nf] for row in op]==[[R(i==j) for j in range(12)] for i in range(12)]
    # Translation cubics have IDENTICALLY zero correlation; check an actual
    # resonant field and its translated quadratic as a regression obligation.
    V=[R(1),R(-2),R(0),R(1)];Ct=b.add(*(b.scale(b.diff(F,i),V[i]) for i in range(4)))
    Qt=b.add(T,*(b.scale(HF[i][j],V[i]*V[j]/2) for i in range(4) for j in range(4)))
    translated=m.shape_operation(F,Ct,Qt,cert['resonance_fields'][0]['modes'])
    assert R(translated['r'])==0 and translated['all_means_and_amplitudes_nonnegative_for_this_shape']
    no_resonance=m.shape_operation(F,C,m.scale(T,nu),cert['resonance_fields'][0]['modes'][:2])
    assert R(no_resonance['r'])==0 and no_resonance['all_means_and_amplitudes_nonnegative_for_this_shape']
    result={'actual_ROC_boundary_biform_rebuilt':True,'global_ROC_upper_positive_Gram_size':16,
      'strict_threshold_lower':str(R(cert['ROC_lower'])),'strict_threshold_upper':'1859',
      'lower_obstruction_reconstructed_as_actual_negative_gradient_energy':True,
      'resonance_functional_rank_on_admissible_cubics':8,'translation_kernel_dimension':4,
      'normal_form_dimensions':{'cubic':8,'quadratic_mod_det':9},
      'compatible_fields':8,'translated_and_resonance_free_checks_exact':True,
      'QC_at_near_boundary_fixture':'UNKNOWN','full_face_ROC_QC_equality':'NOT_RESOLVED',
      'seconds':time.perf_counter()-start,
      'scope':'Internal exact proof operations. No QC separation is claimed; the negative calibration lies below the ROC boundary.'}
    (HERE/'calibration_witness.json').write_text(json.dumps(calibration,indent=2)+'\n')
    (HERE/'replay.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
