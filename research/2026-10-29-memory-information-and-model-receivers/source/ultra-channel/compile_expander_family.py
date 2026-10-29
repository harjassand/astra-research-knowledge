"""All-q symbolic Pauli/MGG family, with one finite exact receiver.

No graph optimization, channel fitting, sampled reference or dense quantum state.
"""
from collections import Counter
from fractions import Fraction as Q
import argparse,hashlib,json,math
from pathlib import Path
from time import perf_counter

HERE=Path(__file__).resolve().parent

def ldl(A):
    A=[r[:] for r in A];piv=[]
    for k in range(len(A)):
        p=A[k][k];assert p>0;piv.append(p)
        for i in range(k+1,len(A)):
            for j in range(k+1,len(A)):A[i][j]-=A[i][k]*A[k][j]/p
    return piv

def fisher(rows,p,h):
    return sum(sum(c*h[i] for i,c in r.items())**2/sum(c*p[i] for i,c in r.items()) for r in rows)

def build(q):
    start=perf_counter();d=2**q;D0=d*d-1
    side=math.isqrt(2*D0)
    if side*side<2*D0:side+=1
    n=side*side
    def idx(x,y):return (x%side)*side+(y%side)
    edges=[]
    for x in range(side):
        for y in range(side):
            v=idx(x,y)
            for z in [idx(x+2*y,y),idx(x+2*y+1,y),idx(x,y+2*x),idx(x,y+2*x+1)]:edges.append((v,z))
    degree=Counter()
    for i,j in edges:degree[i]+=1;degree[j]+=1
    assert set(degree.values())=={8} and len(edges)==4*n
    w=Q(1,16);e=Q(3,10);cross=Q(1,10);gamma=Q(1,2000)
    P=[];F=[]
    for i,j in edges:
        if i==j:
            P.extend([{i:w*(1-e)},{i:w*(1-e)},{i:2*w*e}])
            F.extend([{i:w},{i:w}])
        else:
            P.extend([{i:w*(1-e)},{j:w*(1-e)},{i:w*e,j:w*e}])
            F.extend([{i:w*(1-cross),j:w*cross},{i:w*cross,j:w*(1-cross)}])
    for i in range(n):P.append({i:Q(1,2)});F.append({i:Q(1,2)})
    G=[{i:(1-gamma)*a for i,a in r.items()} for r in P]+[{i:gamma for i in range(n)}]
    for rr in [P,F,G]:assert all(sum(r.get(i,0) for r in rr)==1 for i in range(n))
    assert (len(P),len(F),len(G))==(13*n,9*n,13*n+1)
    # Primitive labels0,1 are selected Pauli's signs; swap1 with graph vertex(side,0).
    def perm(i):return side if i==1 else 1 if i==side else i
    primitive=[]
    for a in range(1,D0+1):
        for sign in [1,-1]:primitive.append({'vertex':perm(len(primitive)),'pauli':a,'I':str(Q(1,n)),'W':str(Q(sign,2*n))})
    for i in range(2*D0,n):primitive.append({'vertex':perm(i),'pauli':None,'I':str(Q(1,n)),'W':'0'})
    assert sorted(z['vertex'] for z in primitive)==list(range(n))
    assert sum(Q(z['I']) for z in primitive)==1
    for a in range(1,D0+1):assert sum(Q(z['W']) for z in primitive if z['pauli']==a)==0
    signed=[Q(0)]*n;signed[0]=Q(1,4*n);signed[side]=-Q(1,4*n)
    def guess(rr):return (1+sum(abs(sum(c*signed[i] for i,c in r.items())) for r in rr))/2
    scores={name:guess(rr) for name,rr in [('E',P),('F',F),('erasedE',G)]}
    multiplicity=sum({i,j}=={0,side} for i,j in edges if i!=j)
    assert multiplicity>=1
    assert scores['F']-scores['E']==multiplicity*Q(1,640*n)>0
    assert scores['F']>scores['erasedE']
    # Literal finite spectral certificate; the all-q gap is the credited MGG theorem.
    lap=[[Q(0) for j in range(n)] for i in range(n)]
    for i,j in edges:
        if i!=j:lap[i][i]+=1;lap[j][j]+=1;lap[i][j]-=1;lap[j][i]-=1
    lam=Q(4,5)
    # Restrict L-lambda I to sum-zero coordinates e_i-e_last.
    R=[[lap[i][j]-lap[i][-1]-lap[-1][j]+lap[-1][-1]-lam*(int(i==j)+1) for j in range(n-1)] for i in range(n-1)]
    piv=ldl(R)
    m=Q(1,2*n);M=Q(3,2*n);delta=Q(3,800)
    assert delta*m*lam/(2*M)==gamma
    adjacency={frozenset((i,j)) for i,j in edges if i!=j}
    j=next(j for j in range(1,n) if frozenset((0,j)) not in adjacency)
    exponent=0
    while True:
        masses=[Q(1,2**exponent)]*n;masses[0]=masses[j]=1
        Z=sum(masses);p=[x/Z for x in masses]
        h=[pi*(int(i==0)-p[0]) for i,pi in enumerate(p)]
        a,b=fisher(G,p,h),fisher(F,p,h)
        if a<b:break
        exponent+=1
    assert min(p)<m
    def jsrows(rr):return [{str(i):str(a) for i,a in r.items()} for r in rr]
    inputs={'q':q,'d':d,'side':side,'n':n,'edges':edges,'primitive':primitive,
            'P':jsrows(P),'Q':jsrows(F),'erasedP':jsrows(G)}
    ibytes=(json.dumps(inputs,indent=2)+'\n').encode()
    (HERE/'EXPANDER_INPUTS.json').write_bytes(ibytes)
    out={'q':q,'d':d,'primitive_outcomes':n,'Pauli_settings':D0,'identity_fillers':n-2*D0,
         'MGG_side':side,'edges_including_loops':len(edges),'loops':sum(i==j for i,j in edges),
         'degree':8,'P_outputs':len(P),'Q_outputs':len(F),'erased_P_outputs':len(G),
         'primitive_effect_bounds':[str(m),str(M)],'delta':str(delta),'graph_gap_lower':str(lam),
         'all_q_gamma':'1/2000','all_quantum_reference_MI_factor':'1999/2000',
         'selected_edge_multiplicity':multiplicity,'quantum_guessing':{k:str(v) for k,v in scores.items()},
         'guessing_F_minus_E':str(scores['F']-scores['E']),
         'guessing_F_minus_erasedE':str(scores['F']-scores['erasedE']),
         'finite_graph_LDL_pivots':list(map(str,piv)),
         'latent_classical_failure':{'vertices':[0,j],'dyadic_exponent':exponent,'p':list(map(str,p)),
                                     'h':list(map(str,h)),'g_erasedP':str(a),'g_Q':str(b),'gap':str(a-b),
                                     'violates_primitive_probability_floor':True},
         'inputs_sha256':hashlib.sha256(ibytes).hexdigest(),'compile_seconds':perf_counter()-start,
         'source_scope':'symbolic mathematical Pauli readout; no physical preparations or measurements',
         'spectral_scope':'all-q graph bound credited to MGG; literal finite graph additionally qualified by exact LDL',
         'cost_scope':'O(d²) settings/outcomes; exponential in qubit count; no full-state reconstruction or practical advantage claim'}
    (HERE/'EXPANDER_FAMILY.json').write_text(json.dumps(out,indent=2)+'\n')
    return out

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--qubits',type=int,default=2);args=ap.parse_args()
    if args.qubits<1:raise ValueError('positive qubit count required')
    out=build(args.qubits)
    print(json.dumps({k:out[k] for k in ['q','d','primitive_outcomes','P_outputs','Q_outputs','all_q_gamma','guessing_F_minus_E','compile_seconds']}))

if __name__=='__main__':main()
