"""Check exact two-site/onsite gate lists on two commuting stabilizers ZZ,XX.
Arbitrary DATA inputs represented by all matrix columns, not selected states.
"""
import numpy as np,json
from pathlib import Path
I=np.eye(4,dtype=complex)
X=np.array([[0,1],[1,0]],complex);Z=np.diag([1,-1]);i2=np.eye(2)
S=[np.kron(Z,Z),np.kron(X,X)]
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
H=np.array([[1,1],[1,-1]],complex)/np.sqrt(2)
def readgates():
    g=[]
    for j,P in enumerate([Z,X]):
        g.append(lambda a,j=j:one(a,2+j,H))
        for r in [0,1]:g.append(lambda a,j=j,r=r,P=P:controlled(a,2+j,r,P))
        g.append(lambda a,j=j:one(a,2+j,H))
    return g
read=readgates();errs=[];rollerrs=[];leak=[]
for av in range(4):
    def table(a,av=av):
        b=np.zeros_like(a)
        for n in range(len(a)):
            bv=(n>>2)&3;d=av^bv;mask=((d&1)<<4)|(((d>>1)&1)<<6)
            b[n^mask]+=a[n]
        return b
    gates=read+[table]
    for r in [0,1]:
        gates += [lambda a,r=r:controlled(a,6+r,r,Z),lambda a,r=r:controlled(a,4+r,r,X)]
    a=np.zeros((256,4),complex);a[:4]=I;prefix=[a]
    for g in gates:prefix.append(g(prefix[-1]))
    for ell in range(len(prefix)):
        back=prefix[ell]
        for g in reversed(gates[:ell]):back=g(back)
        rollerrs.append(float(np.max(np.abs(back-a))))
    for bv in range(4):
        d=av^bv;mask=((d&1)<<4)|(((d>>1)&1)<<6)
        rows=[di|(bv<<2)|mask for di in range(4)]
        actual=prefix[-1][rows]
        projector=(I+((-1)**(bv&1))*S[0])@(I+((-1)**((bv>>1)&1))*S[1])/4
        # q0 is the least significant DATA bit in matrix row order.
        pauli=np.linalg.matrix_power(np.kron(i2,X),d&1)@np.linalg.matrix_power(np.kron(i2,Z),(d>>1)&1)
        errs.append(float(np.max(np.abs(actual-pauli@projector))))
    goodrows=set(di|(bv<<2)|(((av^bv)&1)<<4)|((((av^bv)>>1)&1)<<6) for bv in range(4) for di in range(4))
    leak.append(float(np.max(np.abs(prefix[-1][[n for n in range(256) if n not in goodrows]]))))
assert max(errs+rollerrs+leak)<1e-12
out={'programs':4,'syndrome_outcomes_per_program':4,'alice_gate_count':len(read),'bob_gate_count':len(gates),'native_gate_types':['onsite Hadamard','hub/resource controlled-Pauli','onsite reversible finite table'], 'max_exact_bob_kraus_error':max(errs),'max_prefix_inverse_error':max(rollerrs),'max_wrong_workspace_label_amplitude':max(leak),'all_data_matrix_columns_tested':True,'scope':'2-qubit commuting XX/ZZ fixture; abstract fixed GPT table energy properties remain inherited'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
