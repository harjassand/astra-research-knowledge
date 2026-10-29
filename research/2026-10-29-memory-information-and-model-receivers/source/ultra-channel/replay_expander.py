"""Literal family consumer: Fraction-only, no producer imports."""
from fractions import Fraction as Q
from pathlib import Path
from time import perf_counter
import hashlib,json,math

HERE=Path(__file__).resolve().parent

def ldl(A):
    A=[a[:] for a in A];out=[]
    for k in range(len(A)):
        p=A[k][k];assert p>0;out.append(p)
        for i in range(k+1,len(A)):
            for j in range(k+1,len(A)):A[i][j]-=A[i][k]*A[k][j]/p
    return out

def main():
    start=perf_counter();raw=(HERE/'EXPANDER_INPUTS.json').read_bytes()
    a=json.loads(raw);r=json.loads((HERE/'EXPANDER_FAMILY.json').read_text())
    assert hashlib.sha256(raw).hexdigest()==r['inputs_sha256']
    q,d,side,n=a['q'],a['d'],a['side'],a['n'];assert d==2**q and n==side*side
    assert (side-1)**2<2*(d*d-1)<=side**2
    expected=[]
    for x in range(side):
        for y in range(side):
            dest=[((x+2*y)%side,y),((x+2*y+1)%side,y),(x,(y+2*x)%side),(x,(y+2*x+1)%side)]
            expected += [(x*side+y,z*side+w) for z,w in dest]
    edges=list(map(tuple,a['edges']));assert edges==expected
    deg=[0]*n;L=[[Q(0)]*n for _ in range(n)]
    for i,j in edges:
        deg[i]+=1;deg[j]+=1
        if i!=j:L[i][i]+=1;L[j][j]+=1;L[i][j]-=1;L[j][i]-=1
    assert set(deg)=={8} and len(edges)==4*n
    R=[[L[i][j]-L[i][-1]-L[-1][j]+L[-1][-1]-Q(4,5)*(int(i==j)+1) for j in range(n-1)] for i in range(n-1)]
    assert ldl(R)==list(map(Q,r['finite_graph_LDL_pivots']))
    rows={name:[{int(i):Q(v) for i,v in z.items()} for z in a[name]] for name in ['P','Q','erasedP']}
    for rr in rows.values():
        assert all(all(v>0 for v in z.values()) for z in rr)
        assert all(sum(z.get(i,0) for z in rr)==1 for i in range(n))
    assert (len(rows['P']),len(rows['Q']),len(rows['erasedP']))==(13*n,9*n,13*n+1)
    assert rows['erasedP'][:-1]==[{i:Q(1999,2000)*v for i,v in z.items()} for z in rows['P']]
    assert rows['erasedP'][-1]=={i:Q(1,2000) for i in range(n)}
    # Primitive algebra: one signed Pauli per positive effect, plus identity fillers.
    prim=a['primitive'];assert sorted(p['vertex'] for p in prim)==list(range(n))
    assert sum(Q(p['I']) for p in prim)==1
    assert all(Q(p['I'])==Q(1,n) for p in prim)
    for b in range(1,d*d):
        zz=[Q(p['W']) for p in prim if p['pauli']==b]
        assert sorted(zz)==[Q(-1,2*n),Q(1,2*n)]
    assert sum(p['pauli'] is None for p in prim)==n-2*(d*d-1)
    assert all(Q(p['W'])==0 for p in prim if p['pauli'] is None)
    sig=[Q(0)]*n
    for p in prim:
        if p['pauli']==1:sig[p['vertex']]=Q(p['W'])/2
    assert sig[0]==Q(1,4*n) and sig[side]==Q(-1,4*n)
    success={name:(1+sum(abs(sum(v*sig[i] for i,v in z.items())) for z in rr))/2 for name,rr in rows.items()}
    assert success['P']==Q(r['quantum_guessing']['E']) and success['Q']==Q(r['quantum_guessing']['F'])
    assert success['erasedP']==Q(r['quantum_guessing']['erasedE'])
    mult=sum(i!=j and {i,j}=={0,side} for i,j in edges)
    assert success['Q']-success['P']==mult*Q(1,640*n)>0
    assert success['Q']-success['erasedP']==Q(r['guessing_F_minus_erasedE'])>0
    m,M=map(Q,r['primitive_effect_bounds']);delta=Q(r['delta']);lam=Q(r['graph_gap_lower'])
    assert m==Q(1,2*n) and M==Q(3,2*n) and delta==Q(3,800) and lam==Q(4,5)
    assert delta*m*lam/(2*M)==Q(r['all_q_gamma'])==Q(1,2000)
    f=r['latent_classical_failure'];p=list(map(Q,f['p']));h=list(map(Q,f['h']))
    assert sum(p)==1 and min(p)>0 and sum(h)==0 and min(p)<m
    def fisher(rr):return sum(sum(v*h[i] for i,v in z.items())**2/sum(v*p[i] for i,v in z.items()) for z in rr)
    gp,gq=fisher(rows['erasedP']),fisher(rows['Q'])
    assert gp==Q(f['g_erasedP']) and gq==Q(f['g_Q']) and gp-gq==Q(f['gap'])<0
    out={'status':'PASS','implementation':'stdlib Fraction; no producer imports',
         'scope':'literal MGG/Pauli sparse source, full finite graph gap, all row normalizations, global-erasure constant, exact binary nonsimulation and latent input-domain failure',
         'seconds':perf_counter()-start,'not_scope':'independent proof of all-q MGG theorem, physical access, scientific priority'}
    (HERE/'EXPANDER_REPLAY.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))

if __name__=='__main__':main()
