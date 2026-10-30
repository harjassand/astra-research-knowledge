"""Exact receiver for universal resonant gluing, standard library only.

Checks the cubic identities on the ENTIRE admissible space, the symbolic
wave moments at all amplitudes, six-ray covariance exchange, three positive
cost certificates, all eight correlation modes, and the cross-block bound.
"""
from pathlib import Path
from fractions import Fraction as R
from itertools import product
import importlib.util,json,time
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('shape_core',HERE.parent/'quadratic_boundary/check_shape.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
b=m.core
def dot(v,w):return sum((x*y for x,y in zip(v,w)),R(0))
def quadratic(H,v,w=None):
    w=v if w is None else w
    return sum((v[i]*H[i][j]*w[j] for i in range(len(v)) for j in range(len(w))),R(0))
def outer(v):return [[x*y for y in v] for x in v]
def congruence(H,B):
    return [[sum(B[i][a]*H[i][j]*B[j][c] for i in range(len(H)) for j in range(len(H))) for c in range(len(B[0]))] for a in range(len(B[0]))]
def compose(p,images,n):
    out={}
    for powers,co in p.items():
        term={(0,)*n:co}
        for image,power in zip(images,powers):
            for _ in range(power):term=b.mul(term,image)
        out=b.add(out,term)
    return out
def main():
    start=time.perf_counter();cert=json.loads((HERE/'certificate.json').read_text());gd=json.loads((HERE.parent/'graded_stabilization/certificate.json').read_text());base=json.loads((HERE.parent/'hopf_structure/certificate.json').read_text())
    F,_,T=m.acquired();A=[b.var(4,i) for i in range(4)];K=list(map(R,base['ray']['K_coefficients']))
    X=b.add(b.mul(A[0],A[0]),b.mul(A[2],A[2]),b.scale(b.mul(A[1],A[1]),-1),b.scale(b.mul(A[3],A[3]),-1));Y=b.scale(b.add(b.mul(A[0],A[1]),b.mul(A[2],A[3])),2);Z=b.scale(b.add(b.mul(A[0],A[3]),b.scale(b.mul(A[1],A[2]),-1)),2)
    forms=[b.mul(X,X),b.scale(b.mul(X,Y),2),b.scale(b.mul(X,Z),2),b.mul(Y,Y),b.scale(b.mul(Y,Z),2),b.mul(Z,Z)]
    assert F==b.add(*(b.scale(p,c) for p,c in zip(forms,K)))
    JA=[b.scale(A[2],-1),b.scale(A[3],-1),A[0],A[1]];assert not b.add(*(b.mul(b.diff(F,j),JA[j]) for j in range(4)))
    HF=[[b.diff(b.diff(F,i),j) for j in range(4)] for i in range(4)];powers=cert['cubic_powers'];assert powers==gd['cubic_powers']
    basis=[list(map(R,v)) for v in gd['cubic_kernel_basis']];assert b.rank(basis)==12
    # Eight ACTUAL acoustic pairs force every globally ROC lower cubic into
    # this space. These are not an inferred selector or a sampled admission.
    av=list(map(R,base['ray']['A0']));aa,bb,cc,dd=av;av2=[-bb,aa,dd,-cc];constraints=[]
    for spatial,K0 in ((0,av),(1,av2)):
        for x,y in ((1,0),(0,1),(1,1),(1,-1)):
            Rv=[R(x if spatial==0 else 0),R(x if spatial==1 else 0),R(y if spatial==0 else 0),R(y if spatial==1 else 0)]
            Kv=[x*K0[0]-y*K0[2],x*K0[1]-y*K0[3],y*K0[0]+x*K0[2],y*K0[1]+x*K0[3]]
            HR=[[b.evaluate(p,Rv) for p in row] for row in HF];assert all(dot(row,Kv)==0 for row in HR)
            row=[sum(b.evaluate(b.diff({tuple(pw):R(1)},j),Rv)*Kv[j] for j in range(4)) for pw in powers];constraints.append(row)
    assert b.rank(constraints)==8 and all(dot(row,v)==0 for row in constraints for v in basis)
    rays=[list(map(R,v)) for v in cert['rays']];assert rays[:3]==[[1,0,0,0],[0,0,0,1],[1,1,1,1]]
    for r in rays:assert r[0]*r[3]-r[1]*r[2]==0
    assert rays[3:]==[[1,t,t,t*t] for t in (R(-1),R(1,2),R(2))]
    eta=[R(1,9),R(16,9),R(1,9)];outers=[outer(r) for r in rays]
    assert [[sum(eta[k]*outers[k+3][i][j] for k in range(3)) for j in range(4)] for i in range(4)]==[[sum(outers[k][i][j] for k in range(3)) for j in range(4)] for i in range(4)]
    HH=[[[b.evaluate(p,r) for p in row] for row in HF] for r in rays]
    # Reconstruct all amplitude moments as Laurent polynomials in the two
    # frequencies and ordinary polynomials in the THREE wave amplitudes.
    frequencies=[(1,0),(0,1),(1,1)];images=[{} for _ in range(4)]
    for k,(freq,ray) in enumerate(zip(frequencies,rays[:3])):
        amp=tuple(int(i==k) for i in range(3))
        for component in range(4):
            for sign in (-1,1):
                ee=(sign*freq[0],sign*freq[1])+amp;images[component]=b.add(images[component],{ee:ray[component]/2})
    def moments(p):return {ee[2:]:co for ee,co in compose(p,images,5).items() if ee[:2]==(0,0)}
    target=list(map(R,cert['cubic_moment_unit']))
    for pw,co in zip(powers,target):assert moments({tuple(pw):R(1)})==({(1,1,1):co} if co else {})
    FM=[[R(0) for _ in range(3)] for _ in range(3)]
    for i in range(3):FM[i][i]=R(3,8)*b.evaluate(F,rays[i])
    for i,j in ((0,1),(0,2),(1,2)):FM[i][j]=FM[j][i]=quadratic(HH[i],rays[j])/16
    assert FM==[list(map(R,row)) for row in cert['quartic_moment_matrix']]
    def quartic_from_matrix(mat):
        out={}
        for i in range(3):
            ee=tuple(4*int(k==i) for k in range(3));out[ee]=mat[i][i]
        for i,j in ((0,1),(0,2),(1,2)):
            ee=tuple(2*int(k in (i,j)) for k in range(3));out[ee]=2*mat[i][j]
        return {e:c for e,c in out.items() if c}
    assert moments(F)==quartic_from_matrix(FM)
    radial=moments(b.mul(T,T));RM=[[R(0) for _ in range(3)] for _ in range(3)]
    for i in range(3):RM[i][i]=radial.get(tuple(4*int(k==i) for k in range(3)),R(0))
    for i,j in ((0,1),(0,2),(1,2)):RM[i][j]=RM[j][i]=radial.get(tuple(2*int(k in (i,j)) for k in range(3)),R(0))/2
    assert radial==quartic_from_matrix(RM)
    # These are the ONLY cubic resonances; quartic ones have zero signed
    # multiplicity separately in each wave, so arbitrary phases are covered.
    signed=[(j,sign,(sign*k[0],sign*k[1])) for j,k in enumerate(frequencies) for sign in (-1,1)]
    for n in (3,4):
        for terms in product(signed,repeat=n):
            if any(sum(v[2][k] for v in terms) for k in range(2)):continue
            counts=[sum(v[1] for v in terms if v[0]==j) for j in range(3)]
            if n==3:assert counts in ([1,1,-1],[-1,-1,1])
            else:assert counts==[0,0,0]
    features=[]
    for r in rays:
        for j in range(4):features.append([b.evaluate(b.diff({tuple(pw):R(1)},j),r) for pw in powers])
    reduced=[[dot(v,col) for col in features] for v in basis];rhs=[dot(v,target) for v in basis]
    assert b.rank(reduced)==12
    own=[row[:12] for row in reduced];assert b.rank(own)==10 and b.rank([row+[co] for row,co in zip(own,rhs)])==11
    for chartdata in cert['charts']:
        minimum=chartdata['minimum'];XX=[list(map(R,row)) for row in chartdata['X']];xx=[v for row in XX for v in row]
        assert all(dot(row,xx)==co for row,co in zip(reduced,rhs))
        energy=[quadratic(H,x) for H,x in zip(HH,XX)];assert energy==list(map(R,chartdata['energy'])) and all(e>=0 for e in energy)
        newenergy=sum(e/q for e,q in zip(energy[3:],eta));D=[row[:] for row in FM]
        for i in range(3):
            j,k=[a for a in range(3) if a!=i];co=energy[i]+(newenergy if i==minimum else 0);D[j][k]-=co;D[k][j]-=co
        chart=[[R(int(i==j)) for j in range(3) if j!=minimum]+[R(1)] for i in range(3)];Dc=congruence(D,chart)
        P=[list(map(R,row)) for row in chartdata['positive_matrix']];N=[list(map(R,row)) for row in chartdata['nonnegative_matrix']]
        b.pd(P);assert P==list(map(list,zip(*P))) and N==list(map(list,zip(*N))) and all(v>=0 for row in N for v in row)
        assert [[P[i][j]+N[i][j]+(R(1,8) if i==j else 0) for j in range(3)] for i in range(3)]==Dc
        Tc=congruence(RM,chart);assert all(v>=0 for row in Tc for v in row) and max(sum(row) for row in Tc)<=25
    # All eight nontranslation correlation modes occur INSIDE this class.
    detection=[]
    for case in cert['resonance_detection_fields']:
        aa,bb,cc=case['amplitudes'];x,y=case['output_rotation_scale'];vv=[[aa*x,aa*y],[-bb*y,bb*x],[cc*(x-y),cc*(x+y)]]
        assert case['modes']==[{'frequency':list(k),'sine':list(map(str,v))} for k,v in zip(frequencies,vv)]
        G=m.gradient(case['modes']);H=[[m.average(p,G) for p in row] for row in HF];v=[m.average(b.diff(F,i),G) for i in range(4)];sv=m.linear_solve(H,v);row=[]
        for pw in powers:
            p={tuple(pw):R(1)};w=[m.average(b.diff(p,i),G) for i in range(4)];row.append(m.average(p,G)-dot(sv,w))
        assert row==list(map(R,case['functional']));detection.append([dot(row,v) for v in basis])
    assert b.rank(detection)==8
    # Nine 2x2 inequalities control cross-block quartic interactions, with
    # arbitrary relative output rotations. This supplies a uniform L4 gap
    # on any finite five-adically separated union of the resonant blocks.
    spatial=[[R(1),R(0)],[R(0),R(1)],[R(1),R(1)]];lower=R(3,50);index=0
    for n in spatial:
        H=[[b.evaluate(p,[n[0],n[1],R(0),R(0)]) for p in row] for row in HF]
        for k in spatial:
            vecs=[[k[0],k[1],R(0),R(0)],[R(0),R(0),k[0],k[1]]];den=dot(n,n)*dot(k,k)
            mat=[[quadratic(H,vecs[i],vecs[j])/den for j in range(2)] for i in range(2)]
            assert mat==[list(map(R,row)) for row in cert['cross_matrices'][index]];index+=1
            b.pd([[v-(lower if i==j else 0) for j,v in enumerate(row)] for i,row in enumerate(mat)])
    assert R(1,8)/25==R(1,200) and lower/2==6*R(1,200)
    # Convexity on the symmetric subspace is an actual FAILED ordinary
    # explanation: the exact Hessian value in these two symmetric matrices
    # is strictly negative. The gluing proof does not use convexity there.
    H=[[b.evaluate(p,[R(1),R(0),R(0),R(-1)]) for p in row] for row in HF]
    assert quadratic(H,[R(1),R(0),R(0),R(1)])<0
    result={'acoustic_constraints_rank':8,'admissible_cubic_dimension':12,
      'own_wave_hessian_feature_rank':10,'own_waves_plus_required_cubic_moment_rank':11,
      'auxiliary_six_ray_feature_rank':12,'exact_covariance_exchange':True,
      'all_amplitude_moment_identities':True,'all_phase_resonance_structure':True,
      'universal_cost_charts':3,'positive_cost_matrices':3,'nonnegative_cost_matrices':3,
      'resonant_class_detects_all_nontranslation_modes_rank':8,
      'cross_block_positive_matrices':9,'uniform_quartic_gap':'1/200',
      'arbitrarily_many_resonance_separated_blocks':True,
      'global_QC_of_original_face':'NOT_RESOLVED',
      'seconds':time.perf_counter()-start,
      'scope':'Universal theorem for the explicit resonant wave class, not all compatible gradients. Analytic Hessian-quadrature and lacunarity arguments are in PROOF.txt.'}
    (HERE/'replay.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
