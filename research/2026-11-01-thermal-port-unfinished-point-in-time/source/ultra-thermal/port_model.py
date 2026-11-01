"""Exact finite stabilizer/thermal-port model used by the control programs.

The [[5,1,3]] perfect code is a small non-CSS fixture, NOT a member of the
primary three-dimensional RX/RZ family. All single-qubit Pauli seeds are
included in the complete port catalogue. Energy selectors are actual
Hamiltonian primitives, not an approximation to unfiltered pair couplings.
"""
from __future__ import annotations
import numpy as np
from scipy.sparse import csr_matrix

I=np.eye(2,dtype=complex)
X=np.array([[0,1],[1,0]],complex)
Y=np.array([[0,-1j],[1j,0]],complex)
Z=np.diag([1,-1]).astype(complex)
PAULIS={'I':I,'X':X,'Y':Y,'Z':Z}
def ten(*args):
    a=np.array([[1]],complex)
    for b in args:a=np.kron(a,b)
    return a
def word(s):return ten(*(PAULIS[c] for c in s))
def comm(a,b):return a@b-b@a
def norm(a):return float(np.linalg.norm(a,2))


def perfect_code():
    checks=[word(s) for s in ('XZZXI','IXZZX','XIXZZ','ZXIXZ')]
    xlog=word('XXXXX');zlog=word('ZZZZZ')
    proj=np.eye(32,dtype=complex)
    for s in checks:proj=proj@(np.eye(32)+s)/2
    pzero=proj@(np.eye(32)+zlog)/2
    values,basis=np.linalg.eigh(pzero)
    zero=basis[:,np.argmax(values)]
    one=xlog@zero;code=np.stack((zero,one),axis=1)
    seeds=[];recoveries={0:np.eye(32,dtype=complex)}
    for site in range(5):
        for axis in 'XYZ':
            label='I'*site+axis+'I'*(4-site);p=word(label)
            syndrome=0
            for j,s in enumerate(checks):
                if norm(s@p-p@s)>1:syndrome|=1<<j
            assert syndrome and syndrome not in recoveries
            recoveries[syndrome]=p
            seeds.append({'site':site,'axis':axis,'label':label,
                          'syndrome':syndrome,'pauli':p})
    assert len(recoveries)==16
    # Coordinate order is logical q, then the 4-bit syndrome s.
    U=np.column_stack([recoveries[s]@code[:,q] for q in range(2) for s in range(16)])
    assert norm(U.conj().T@U-np.eye(32))<1e-12
    energies=np.array([s.bit_count() for s in range(16)],dtype=float)
    h0=sum((np.eye(32)-s)/2 for s in checks)
    assert norm(U.conj().T@h0@U-ten(I,np.diag(energies)))<1e-12
    for seed in seeds:
        p=U.conj().T@seed['pauli']@U
        matrices=[];bad=[]
        for s in range(16):
            target=s^seed['syndrome']
            block=p[np.ix_([target,16+target],[s,16+s])]
            matrices.append(block)
            bad.append(abs(np.trace(block))<1e-8)
        seed['recovery_pauli']=p
        seed['logical_blocks']=matrices
        seed['bad_syndromes']=np.array(bad,dtype=bool)
        assert not bad[0]
    return {'checks':checks,'encoder':code,'recovery_unitary':U,
            'energies':energies,'H0':h0,'seeds':seeds}


def ports(model,seeds=None):
    if seeds is None:seeds=model['seeds']
    entries=[];E=model['energies']
    for seed in seeds:
        t=seed['syndrome'].bit_count()
        # A_omega lowers data energy by omega. Zero components are Hermitian.
        for omega in range(t%2,t+1,2):
            columns=[s for s in range(16) if E[s^seed['syndrome']]-E[s]==-omega]
            selector=np.diag([int(s in columns) for q in range(2) for s in range(16)])
            a=seed['recovery_pauli']@selector
            entries.append({'label':seed['label'],'site':seed['site'],'axis':seed['axis'],
                            'syndrome':seed['syndrome'],'omega':omega,'operator':a,
                            'bad_syndromes':seed['bad_syndromes'],'source_syndromes':columns})
    return entries


def logical_expectation(a,aux_dim):
    """I_Q tensor Tr_Q(a)/2; a is ordered Q then auxiliary coordinates."""
    part=(a[:aux_dim,:aux_dim]+a[aux_dim:,aux_dim:])/2
    return ten(I,part)


def charge_hamiltonians(model,entries,g=.6,bath=None):
    """Sixteen exact total-syndrome-charge blocks; controllers are NOT eliminated.

    One multilevel controller with ground 0 and one excited level per port.
    Optional persistent bath has two levels and one energy-conserving port.
    The complete family construction instead uses a private controller at
    each data site, of bounded dimension; the finite global controller here
    couples only the five data sites in this fixture.
    """
    C=len(entries)+1;B=2 if bath is not None else 1;A=C*B;D=2*A
    tags=[0]+[p['syndrome'] for p in entries]
    gaps=np.array([0]+[p['omega'] for p in entries],dtype=float)
    etag=bath['syndrome'] if bath is not None else 0
    egap=bath['omega'] if bath is not None else 0
    energies=model['energies'];hs=[];good=[]
    def idx(q,c,b):return q*A+c*B+b
    for k in range(16):
        H=np.zeros((D,D),complex)
        for q in range(2):
            for c in range(C):
                for b in range(B):
                    syn=k^tags[c]^(etag if b else 0)
                    H[idx(q,c,b),idx(q,c,b)]=energies[syn]+gaps[c]+b*egap
        for c,p in enumerate(entries,1):
            for b in range(B):
                syn=k^(etag if b else 0)
                target=syn^p['syndrome']
                if energies[target]-energies[syn]!=-p['omega']:continue
                block=p['operator'][np.ix_([target,16+target],[syn,16+syn])]
                left=[idx(q,c,b) for q in range(2)];right=[idx(q,0,b) for q in range(2)]
                H[np.ix_(left,right)]+=g*block
                H[np.ix_(right,left)]+=g*block.conj().T
        if bath is not None:
            p=bath;gb=bath['g']
            for c in range(C):
                syn=k^tags[c];target=syn^etag
                if energies[target]-energies[syn]!=-egap:continue
                block=p['operator'][np.ix_([target,16+target],[syn,16+syn])]
                left=[idx(q,c,1) for q in range(2)];right=[idx(q,c,0) for q in range(2)]
                H[np.ix_(left,right)]+=gb*block
                H[np.ix_(right,left)]+=gb*block.conj().T
        assert norm(H-H.conj().T)<1e-12
        hs.append(csr_matrix(H));good.append(csr_matrix(logical_expectation(H,A)))
    return {'H':hs,'H_good':good,'tags':tags,'gaps':gaps,'bath_tag':etag,
            'bath_gap':egap,'C':C,'B':B,'A':A,'block_dimension':D}
