"""Exact receiver for the first overlapping resonance gluing certificate."""
from pathlib import Path
from fractions import Fraction as R
import json,time,contextlib,io
import receive as base
from receive import m,b,dot,quadratic,outer,compose
HERE=Path(__file__).resolve().parent
def phase_moments(p,images):return {e[2:]:co for e,co in compose(p,images,4).items() if e[:2]==(0,0)}
def network():
    frequencies=[(1,0),(0,1),(1,1),(2,1)];phases=[(0,0),(0,0),(-1,0),(-1,-1)]
    original=[[R(1),R(0),R(0),R(0)],[R(0),R(0),R(0),R(1)],[R(1)]*4,[R(1),R(1,2),R(1,2),R(1,4)]];images=[{} for _ in range(4)]
    for k,ph,r in zip(frequencies,phases,original):
        for component in range(4):
            for sign in (-1,1):images[component]=b.add(images[component],{(sign*k[0],sign*k[1],sign*ph[0],sign*ph[1]):r[component]/2})
    return original,images
def phase_coefficients(moment):
    assert set(moment)<={(0,0),(1,1),(-1,-1),(1,-1),(-1,1)}
    assert moment.get((1,1),0)==moment.get((-1,-1),0) and moment.get((1,-1),0)==moment.get((-1,1),0)
    plus=2*moment.get((1,1),0);minus=2*moment.get((1,-1),0)
    return [moment.get((0,0),R(0)),plus+minus,minus-plus]
def main():
    start=time.perf_counter()
    with contextlib.redirect_stdout(io.StringIO()):base.main()
    cert=json.loads((HERE/'overlap_certificate.json').read_text());gd=json.loads((HERE.parent/'graded_stabilization/certificate.json').read_text());basis=[list(map(R,v)) for v in gd['cubic_kernel_basis']];F,_,T=m.acquired();powers=gd['cubic_powers']
    rays=[list(map(R,r)) for r in cert['rays']];weights=list(map(R,cert['weights']));assert len(rays)==8 and all(w>0 for w in weights)
    for r in rays:assert r[0]*r[3]-r[1]*r[2]==0
    original,images=network()
    assert [[sum(w*r[i]*r[j] for w,r in zip(weights,rays)) for j in range(4)] for i in range(4)]==[[sum(r[i]*r[j]/2 for r in original) for j in range(4)] for i in range(4)]
    fc=phase_coefficients(phase_moments(F,images));rc=phase_coefficients(phase_moments(b.mul(T,T),images))
    assert fc==list(map(R,cert['quartic_phase_coefficients'])) and rc==list(map(R,cert['radial_phase_coefficients']))
    targets=[]
    for pw in powers:
        moment=phase_moments({tuple(pw):R(1)},images);assert set(moment)<={(1,0),(-1,0),(0,1),(0,-1)}
        assert moment.get((1,0),0)==moment.get((-1,0),0) and moment.get((0,1),0)==moment.get((0,-1),0)
        targets.append([2*moment.get((1,0),0),2*moment.get((0,1),0)])
    assert targets==[list(map(R,row)) for row in cert['cubic_targets']]
    XX=[list(map(R,row)) for row in cert['X']];YY=[list(map(R,row)) for row in cert['Y']]
    for which,profile in enumerate((XX,YY)):
        functional=[sum(w*sum(b.evaluate(b.diff({tuple(pw):R(1)},j),r)*a[j] for j in range(4)) for w,r,a in zip(weights,rays,profile)) for pw in powers]
        assert all(dot(v,functional)==dot(v,[row[which] for row in targets]) for v in basis)
    HF=[[b.diff(b.diff(F,i),j) for j in range(4)] for i in range(4)];cost=[[R(0) for _ in range(2)] for _ in range(2)]
    for r,w,x,y in zip(rays,weights,XX,YY):
        H=[[b.evaluate(p,r) for p in row] for row in HF]
        for i,a in enumerate((x,y)):
            for j,z in enumerate((x,y)):cost[i][j]+=w*quadratic(H,a,z)/2
    assert cost==[list(map(R,row)) for row in cert['cost_matrix']]
    t1,t2=map(R,cert['phase_budget_diagonal']);f0,fcos,fsin=fc
    P=[[t1-cost[0][0],fcos/2-cost[0][1]],[fcos/2-cost[1][0],t2-cost[1][1]]];Q=[[t1,fsin/2],[fsin/2,t2]]
    assert P==[list(map(R,row)) for row in cert['positive_cosine_matrix']] and Q==[list(map(R,row)) for row in cert['positive_sine_matrix']]
    b.pd(P);b.pd(Q);gap=f0-t1-t2;radmax=rc[0]+abs(rc[1])+abs(rc[2]);assert gap==R(cert['phase_uniform_budget']) and radmax==R(cert['radial_upper_bound']) and gap>23 and gap>radmax/200
    spatial=[[R(1),R(0)],[R(0),R(1)],[R(1),R(1)],[R(2),R(1)]];eta=R(3,50);index=0
    for n in spatial:
        H=[[b.evaluate(p,[*n,R(0),R(0)]) for p in row] for row in HF]
        for k in spatial:
            v=[[k[0],k[1],0,0],[0,0,k[0],k[1]]];den=dot(n,n)*dot(k,k);mat=[[quadratic(H,v[i],v[j])/den for j in range(2)] for i in range(2)]
            assert mat==[list(map(R,row)) for row in cert['cross_matrices'][index]];index+=1
            b.pd([[co-(eta if i==j else 0) for j,co in enumerate(row)] for i,row in enumerate(mat)])
    result={'triad_certificate_replayed':True,'overlapping_cubic_resonances':2,'quartic_phase_interactions_reconstructed':True,
      'positive_rank_one_quadrature_terms':8,'both_cubic_targets_matched_on_entire_admissible_space':True,
      'positive_phase_matrices':2,'all_relative_phases_and_means':True,
      'independent_relative_amplitudes':'NOT_CLASSIFIED','uniform_L4_gap':'1/200',
      'cross_block_positive_matrices':16,'arbitrarily_many_nine_adically_separated_mixed_blocks':True,
      'original_full_face_QC':'NOT_RESOLVED','seconds':time.perf_counter()-start,
      'scope':'Universal ROC-to-variational gluing on the stated overlapping network and separated block closure; no unrestricted QC inference.'}
    (HERE/'overlap_replay.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
