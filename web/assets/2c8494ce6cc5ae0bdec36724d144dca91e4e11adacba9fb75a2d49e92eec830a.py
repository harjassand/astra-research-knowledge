"""Post-exposure originator32 check through independent Fraction algebra."""
from pathlib import Path
src=Path(__file__).with_name('check_full_weights_fraction.py').read_text()
exec(src.split('params=')[0])
origin=Path(__file__).parents[2]/'spin1_anisotropic_sol'/'triaxial_symbolic_certificate.json'
data=json.loads(origin.read_text())
inputs={'A_allactive':[(2,3,1),(1,3,1),(1,2,1)],'B1_twoactive':[(2,2,1),(1,1,1),(1,0,0)],'B2_twoactive':[(2,3,1),(1,3,1),(1,2,0)],'C_oneactive':[(2,2,1),(1,1,0),(1,0,0)]}
checked=0
for cone in data['cones']:
    name=cone['name'];H=[linear(*v) for v in inputs[name]]
    if name.startswith('A'):Z=[add(*H,scale(H[i],-2)) for i in range(3)]
    elif name.startswith('B'):Z=[scale(add(scale(H[1],2),scale(H[0],-1)),F(2,3)),scale(add(scale(H[0],2),scale(H[1],-1)),F(2,3)),scale(add(H[0],H[1]),F(2,3))]
    else:Z=[{},H[0],H[0]]
    W=[mul(h,h) for h in H];Q=[add(*W,scale(W[i],-1),mul(Z[i],Z[i])) for i in range(3)]
    Mdict={}
    for i in range(3):
        j,k=[a for a in range(3) if a!=i];qi,qj,qk=Q[i],Q[j],Q[k];wi,wj,wk=W[i],W[j],W[k]
        # Starting from blind reviewer's rational congruent symmetric block.
        M=[[qi,ZERO,scale(wk,-2),ZERO,scale(wj,-2)],
           [ZERO,scale(add(scale(qi,3),scale(qj,2)),F(1,5)),scale(wk,2),ZERO,ZERO],
           [scale(wk,-2),scale(wk,2),scale(add(qi,scale(qj,4)),F(2,5)),ZERO,scale(wi,-2)],
           [ZERO,ZERO,ZERO,scale(add(scale(qi,3),scale(qk,2)),F(1,5)),scale(wj,2)],
           [scale(wj,-2),ZERO,scale(wi,-2),scale(wj,2),scale(add(qi,scale(qk,4)),F(2,5))]]
        order=[0,1,3,2,4];sign=[1,-1,-1,1,1];rescale=[F(1),F(1),F(1),F(1,2),F(1,2)]
        Mdict[f'parity{i+1}']=[[scale(M[order[a]][order[b]],5*sign[a]*sign[b]*rescale[a]*rescale[b]) for b in range(5)] for a in range(5)]
    N=[[ZERO for _ in range(3)] for _ in range(3)]
    for i in range(3):
        N[i][i]=add(scale(Q[i],2),*Q)
        for j in range(i+1,3):N[i][j]=N[j][i]=scale(W[3-i-j],-5)
    Mdict['odd']=N
    for label,record in cone['minors'].items():
        kind,size=label.split('_leading');size=int(size)
        M=Mdict[kind];P=det([row[:size] for row in M[:size]])
        undo=2 if kind.startswith('parity') and size==4 else 4 if kind.startswith('parity') and size==5 else 1
        P=scale(P,undo)
        expected={tuple(term['powers']):F(term['coefficient']) for term in record['positive_terms']+record['negative_terms']}
        assert P==expected,(name,label)
        assert P and all(c>=0 for c in P.values()) and any(c>0 for c in P.values())
        checked+=1
    print('PASS originator',name,'all8 coefficient identities via blind-block congruence.')
assert checked==32
print('PASS all32 originator exact coefficient identities; strict interior Sylvester criterion valid.')
