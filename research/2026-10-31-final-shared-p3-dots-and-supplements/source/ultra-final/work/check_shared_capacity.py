"""Independent actual-field and sharp-cost checks for shared-mode gluing."""
from pathlib import Path
from fractions import Fraction as R
from itertools import permutations
import sys,json,time
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root/'outputs/shared_mode_gluing'))
import receive as r,construct as co,capacity as ca
start=time.perf_counter();data=r.setup();cert=json.loads((co.HERE/'certificate.json').read_text())
# Every order cone is exercised at a strictly interior amplitude point,
# with nonzero relative phases, output rotation, signs and a mean.
cases=0
for order in permutations(range(4)):
    amps=[None]*4
    for j,i in enumerate(order):amps[i]=R(j+1)*(-1 if i%2 else 1)
    result=co.construct(amps,(R(3,5),R(4,5),R(-5,13),R(12,13)),(1,-2,0,1),(R(3,5),R(4,5)))
    assert result['selected_order']==list(order);cases+=1
for amps in ((0,0,0,0),(0,1,2,3),(1,0,2,3),(1,2,0,3),(1,2,3,0),(1,0,2,0),(1,1,1,1),(R(1,10**5),1,2,3),(1,R(1,10**5),2,3),(1,2,R(1,10**5),3),(1,2,3,R(1,10**5))):
    co.construct(amps,(1,0,-1,0),(0,1,-1,2));cases+=1
# The zero-phase physical field can also be evaluated directly as a
# Laurent gradient, independently of the phase/amplitude moment formula.
amps=[R(2),R(-3),R(1),R(1,2)];M=[R(1),R(-2),R(0),R(1)]
result=co.construct(amps,(1,0,1,0),M)
modes=[{'frequency':list(k),'sine':list(map(str,v))} for k,v in zip(((1,0),(0,1),(1,1),(2,1)),((amps[0],0),(0,amps[1]),(amps[2],amps[2]),(2*amps[3],amps[3])))]
G=r.m.gradient(modes);GM=[r.m.add(g,{(0,0):v}) for g,v in zip(G,M)]
F,C,T=r.m.acquired();P=r.b.add(F,C,r.b.scale(T,1859));actual=r.m.average(P,GM)-r.b.evaluate(P,M)
assert actual==R(result['fixture_actual_energy_gap']);cases+=1
# Canonical simultaneous gluing, now using the 4 translation + 8 quotient
# basis, instead of the independent basis used to acquire the certificate.
qc=json.loads((root/'outputs/quadratic_boundary/certificate.json').read_text());basis=[list(map(R,row)) for row in qc['normal_form_basis']]
assert all(basis[j]==[r.b.diff(F,j).get(tuple(pw),R(0)) for pw in data['powers']] for j in range(4))
polys=[{tuple(pw):c for pw,c in zip(data['powers'],row) if c} for row in basis]
targets=[[r.dot(row,[t[e] for t in data['targets']]) for e in range(2)] for row in basis]
def gradients(rays):return [[[r.b.evaluate(r.b.diff(p,j),ray) for p in polys] for j in range(4)] for ray in rays]
original=data['original'];modes_unit=[{'frequency':list(k),'sine':list(map(str,v))} for k,v in zip(((1,0),(0,1),(1,1),(2,1)),((1,0),(0,1),(1,1),(2,1)))];Gunit=r.m.gradient(modes_unit)
Hactual=[[r.m.average(p,Gunit) for p in row] for row in data['HF']]
Bactual=[[r.m.average(r.b.diff(p,j),Gunit) for p in polys[4:]] for j in range(4)]
vactual=[r.m.average(r.b.diff(F,j),Gunit) for j in range(4)];cactual=[r.m.average(p,Gunit) for p in polys[4:]]
factual=r.m.average(F,Gunit);fulltarget=[row[0]+row[1] for row in targets]
assert fulltarget==vactual+cactual
canonical_examples=[];qresults=[]
for bi in (0,1):
    weights=[R(1,4)]*3+[R(1,4)*eta for eta in data['eta']]+[R(1,2)]
    cap=ca.canonical(data['H'][bi],gradients(data['rays'][bi]),weights,targets);assert cap['capacity_rank']==12
    W=cap['capacity_matrix'];assert [row[:4] for row in W[:4]]==Hactual and [row[4:] for row in W[:4]]==Bactual
    q=ca.quotient(W,fulltarget,factual);assert q['quotient_rank']==8
    mincost=sum(row[0]+row[1] for row in cap['cost_matrix'])
    assert factual-mincost==q['quartic_budget']
    canonical_examples.append({'base_exchange':bi,'capacity_rank':12,'quotient_rank':8,'canonical_cost_matrix':[list(map(str,row)) for row in cap['cost_matrix']],'canonical_quartic_budget':str(q['quartic_budget']),'leading_budget_a':str(q['leading_budget_a']),'correlation_cost':str(q['correlation_cost'])});qresults.append(q)
    print('canonical',bi,'budget',float(q['quartic_budget']),flush=True)
    # For the actual chart selected at equal amplitudes, verify the exact
    # Loewner minimum against the independently rounded literal sources.
    if bi==1:
        case=next(row for row in cert['charts'] if row['order']==[0,1,2,3]);Zs=[[[R(v) for v in row] for row in X] for X in case['sources']]
        K=[[sum(r.quadratic(H,Zs[e][i],Zs[f][i])/(2*w) for i,(H,w) in enumerate(zip(data['H'][bi],weights))) for f in range(2)] for e in range(2)]
        difference=[[K[i][j]-cap['cost_matrix'][i][j] for j in range(2)] for i in range(2)];r.psd(difference)
        # The cross terms with the canonical minimizer vanish identically.
        for e in range(2):
            for f in range(2):
                cross=sum(r.quadratic(H,[cap['sources'][i][j][e] for j in range(4)],[Zs[f][i][j]-cap['sources'][i][j][f] for j in range(4)])/(2*w) for i,(H,w) in enumerate(zip(data['H'][bi],weights)))
                assert cross==0
assert qresults[0]['correlation_target']==qresults[1]['correlation_target'] and qresults[0]['leading_budget_a']==qresults[1]['leading_budget_a']
assert qresults[0]['quotient_capacity']!=qresults[1]['quotient_capacity']
# The original three rays have an actual catalogue obstruction, not a QC
# counterexample. The added covariance exchange removes this obstruction.
try:
    ca.canonical(data['H'][0][:3],gradients(original[:3]),[R(1,2)]*3,[[row[0]] for row in targets])
    raise AssertionError('Expected the previously established catalogue obstruction')
except ca.RangeObstruction as obstruction:
    coefficients=[sum(y*v[j] for y,v in zip(obstruction.annihilator,basis)) for j in range(20)]
    poly={tuple(pw):c for pw,c in zip(data['powers'],coefficients) if c}
    assert all(r.b.evaluate(r.b.diff(poly,j),ray)==0 for j in range(4) for ray in original[:3])
    moment=r.dot(coefficients,[row[0] for row in data['targets']]);assert moment and moment==obstruction.target_values[0]
    obstruction_example={'fixed_catalogue':'E11, E22, ones','annihilating_cubic_coefficients':list(map(str,coefficients)),'actual_triad_cubic_moment':str(moment),'scope':'Exact failure of this fixed three-ray catalogue only. The six-ray positive exchange repairs it.'}
summary={'constructor_cases':cases,'all_24_order_cones_exercised':True,'zero_amplitudes_and_small_mode_values_exercised':True,'independent_actual_Laurent_energy_check':True,'simultaneous_canonical_minimum_checked':True,'exact_Loewner_cost_difference_positive':True,'canonical_cross_terms_zero':True,'covariance_exchange_preserves_translation_and_mixed_blocks':True,'only_eight_dimensional_quotient_capacity_changes':True,'fixed_catalogue_annihilator_verified':True,'seconds':time.perf_counter()-start}
(co.HERE/'capacity_example.json').write_text(json.dumps({'canonical_examples':canonical_examples,'fixed_catalogue_obstruction':obstruction_example,'verification':summary},indent=2)+'\n');print(json.dumps(summary,indent=2),flush=True)
