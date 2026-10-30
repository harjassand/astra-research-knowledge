"""Full workspace/operator regression for native LOCC raw exponential energy.
XX/ZZ data fixture; every workspace column is retained until complete reset.
Tests actual full and partial ownership-forest payloads, not clean channels only.
"""
import numpy as np,json
from pathlib import Path
from scipy.linalg import eigvalsh
X=np.array([[0,1],[1,0]],complex);Z=np.diag([1,-1]).astype(complex);I2=np.eye(2);I4=np.eye(4)
H=np.array([[1,1],[1,-1]],complex)/np.sqrt(2)
S=[np.kron(Z,Z),np.kron(X,X)]
Pi=[(I4+(-1)**(s&1)*S[0])@(I4+(-1)**((s>>1)&1)*S[1])/4 for s in range(4)]
def one(a,q,U):
    b=np.zeros_like(a)
    for n in range(len(a)):
        for v in range(2):b[(n&~(1<<q))|(v<<q)]+=U[v,(n>>q)&1]*a[n]
    return b
def controlled(a,c,t,P):
    b=np.zeros_like(a)
    for n in range(len(a)):
        if not (n>>c)&1:b[n]+=a[n]
        else:
            for v in range(2):b[(n&~(1<<t))|(v<<t)]+=P[v,(n>>t)&1]*a[n]
    return b
def readgates():
    gs=[]
    for j,P in enumerate([Z,X]):
        gs.append((0,lambda a,j=j:one(a,2+j,H)))
        for r in [0,1]:gs.append((r,lambda a,j=j,r=r,P=P:controlled(a,2+j,r,P)))
        gs.append((0,lambda a,j=j:one(a,2+j,H)))
    return gs
read=readgates();s_exp=.17;Rt=3.;RB=3.;JA=3;RA=2+Rt*JA+1
results={'bob_full_cases':0,'bob_bad_mask_cases':0,'alice_full_cases':0,'alice_bad_mask_cases':0,'alice_dirty_partial_abort_cases':0}
min_gap=1e100;max_cross=0.;max_unitary=0.;bad_partial_nonmonomial=0.;max_label_collision=0
pc=lambda n:int(n).bit_count()
def op_data(fun):return sum(np.exp(s_exp*fun(v))*Pi[v] for v in range(4))
def check_gap(Vin,pull):
    global min_gap
    gap=(Vin-pull);gap=(gap+gap.conj().T)/2
    val=float(eigvalsh(gap,subset_by_index=[0,0])[0]);min_gap=min(min_gap,val)
    assert val>=-2e-11,val
for a in range(4):
    def table(v,a=a):
        out=np.zeros_like(v)
        for n in range(len(v)):
            b=(n>>2)&3;d=a^b;mask=((d&1)<<4)|(((d>>1)&1)<<6)
            out[n^mask]+=v[n]
        return out
    gs=read+[(0,table)]
    for r in [0,1]:gs.extend([(r,lambda v,r=r:controlled(v,6+r,r,Z)),(r,lambda v,r=r:controlled(v,4+r,r,X))])
    dim=256;W=64
    for mask in range(4):
        U=np.eye(dim,dtype=complex)
        for r,g in gs:U=g(U) if mask>>r&1 else np.eye(dim,dtype=complex)
        max_unitary=max(max_unitary,float(np.linalg.norm(U.conj().T@U-np.eye(dim))))
        for sa in range(4):
            vout=np.kron(np.eye(W),op_data(lambda sb:pc(sa^sb)))
            pull=U.conj().T@vout@U
            blocks=[op_data(lambda sb,w=w:pc(sa^sb)+Rt*(a!=sa)+RB*(mask!=3 or w!=0)) for w in range(W)]
            vin=np.zeros((dim,dim),complex)
            for w,b in enumerate(blocks):vin[4*w:4*w+4,4*w:4*w+4]=b
            check_gap(vin,pull)
            if mask==3:
                results['bob_full_cases']+=1
                cross=float(np.linalg.norm(pull[:4,4:]));max_cross=max(max_cross,cross);assert cross<2e-11
            else:results['bob_bad_mask_cases']+=1
# Explicit full label bijection for every program and arbitrary b,c input.
for a in range(4):
    images=[]
    for raw in range(4):
        for b in range(4):
            for c in range(16):
                bo=b^raw;d=a^bo;co=c^((d&1)|(((d>>1)&1)<<2))
                # Pauli on data 0/1: ZZ flips by x parity; XX by z parity.
                delta=((co&1)^((co>>1)&1))|((((co>>2)&1)^((co>>3)&1))<<1)
                images.append((raw^delta,bo,co))
    assert len(set(images))==len(images)
# Alice output includes CURRENT truth of its newly written pointer.
for mask in range(4):
    prefixes=[np.eye(16,dtype=complex)]
    for r,g in read:prefixes.append(g(prefixes[-1]) if mask>>r&1 else np.eye(16,dtype=complex))
    U=prefixes[-1]
    for sb in range(4):
        for other in [(0,0),(1,2),(3,1)]:
            for old in [None,0,1,2,3]:
                def oldcost(sa):return sum(sa!=v for v in other)+(old is not None and old!=sa)
                def newcost(sa,y):return sum(sa!=v for v in other)+(y!=sa)
                pull=np.zeros((16,16),complex)
                for y in range(4):
                    K=U[4*y:4*y+4,:]
                    out=op_data(lambda sa,y=y:pc(sa^sb)+Rt*newcost(sa,y))
                    pull+=K.conj().T@out@K
                vin=np.zeros((16,16),complex)
                for w in range(4):vin[4*w:4*w+4,4*w:4*w+4]=op_data(lambda sa,w=w:pc(sa^sb)+Rt*oldcost(sa)+RA*(mask!=3 or w!=0))
                check_gap(vin,pull)
                if mask==3:
                    results['alice_full_cases']+=1
                    cross=float(np.linalg.norm(pull[:4,4:]));max_cross=max(max_cross,cross);assert cross<2e-11
                else:results['alice_bad_mask_cases']+=1
    # Every attached dirty R prefix is wholly bad, even for complete ownership.
    for Up in prefixes:
        for sb in range(4):
            other=(0,1,3)
            v=op_data(lambda sa:pc(sa^sb)+Rt*sum(sa!=v for v in other))
            pull=Up.conj().T@np.kron(np.eye(4),v)@Up
            vin=np.exp(s_exp*RA)*np.kron(np.eye(4),v)
            check_gap(vin,pull);results['alice_dirty_partial_abort_cases']+=1
            bad_partial_nonmonomial=max(bad_partial_nonmonomial,float(np.linalg.norm(pull[:4,4:])))
assert bad_partial_nonmonomial>1e-4 # prefixes really need the all-bad envelope
out={'cases':results,'exponent':s_exp,'R_token':Rt,'R_B':RB,'R_A':RA,'Alice_affected_token_bound':JA,'minimum_raw_reset_gap_eigenvalue':min_gap,'maximum_good_dirty_terminal_cross_norm':max_cross,'maximum_unitarity_error':max_unitary,'nonzero_dirty_prefix_cross_norm':bad_partial_nonmonomial,'full_label_maps_bijective':True,'all_checks_pass':True,'scope':'full dirty workspace and malformed-mask XX/ZZ fixture; not a global continuous-noise theorem'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
