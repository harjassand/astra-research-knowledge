"""Check actual norm-map indexing and expose its physical infinitesimal target.

This is a four-site orientation diagnostic, not larger-ring evidence. The
all-m power-trace and infinitesimal statements are proved in PROOF.md.
"""
import pathlib,json
import numpy as np
import scipy.linalg as la
from local_gibbs_gate import exact_spin2,gate,apply_pair

ROOT=pathlib.Path(__file__).resolve().parent

def pair_matrix(h,n,i,j):
    ident=np.eye(5**n)
    return np.column_stack([apply_pair(ident[:,k],h,i,j,n)for k in range(5**n)])

def run():
    exact=exact_spin2();d=.001;a,b,g,h,_=gate(d,exact)
    normmap=sum(np.kron(x,x)for x in b)
    # Row vectorization orders ket1,ket2,bra1,bra2. The derivative graph is
    # the four-cycle0-1-3-2. Construct its physical Hamiltonian separately.
    edges=[(0,1),(2,3),(0,2),(1,3)]
    hh=sum(pair_matrix(h,4,i,j)for i,j in edges)
    i25=np.eye(25);i5=np.eye(5)
    # First derivative directly from E=Ad_g o(Phi tensor Phi), independently
    # of the physical-bond application code. The two Phi act across ket/bra.
    direct_derivative=-np.kron(h,i25)-np.kron(i25,h)
    for generator in exact[0]:
        gg=np.array(generator,dtype=float)
        left=np.kron(gg,i5);right=np.kron(i5,gg)
        direct_derivative+=np.kron(left,left)+np.kron(right,right)
    assert np.max(np.abs(direct_derivative+hh))<1e-13
    ev=la.eigvals(normmap,check_finite=False)
    assert np.max(np.abs(ev.imag))<1e-10
    ev=np.sort(ev.real)[::-1]
    physical_energies=la.eigvalsh(hh,check_finite=False)
    # A separate symmetric physical checkerboard product has the same full
    # spectrum. This catches the periodic trace closure and ordering.
    sq=la.sqrtm(g).real
    even=np.eye(625);odd=np.eye(625)
    for i,j in [(0,1),(2,3)]:even=np.column_stack([apply_pair(even[:,k],sq,i,j,4)for k in range(625)])
    for i,j in [(0,2),(1,3)]:odd=np.column_stack([apply_pair(odd[:,k],g,i,j,4)for k in range(625)])
    physical=even@odd@even
    pev=la.eigvalsh(physical,check_finite=False)[::-1]
    err=float(np.max(np.abs(ev-pev)));assert err<3e-12
    rows=[]
    for delta in [.001,.0001]:
        if delta==d:vals=ev
        else:
            _,bb,_,_,_=gate(delta,exact)
            vals=np.sort(la.eigvals(sum(np.kron(x,x)for x in bb),check_finite=False).real)[::-1]
        rows.append({'delta':delta,'Perron_log_gap_div_delta':float(np.log(vals[0]/vals[1])/delta)})
    result={'status':'FOUR_SITE_INDEX_DIAGNOSTIC_AND_ALL_SIZE_REDUCTION',
        'physical_n':4,'CP_matrix_order':25,'superoperator_dimension':625,
        'cycle_order':[0,1,3,2],'full_spectral_match_max_error':err,
        'physical_ground_energy_numeric':float(physical_energies[0]),
        'physical_gap_numeric':float(physical_energies[1]-physical_energies[0]),
        'infinitesimal_diagnostics':rows,
        'all_m_identity':'Tr(E_m^N)=Tr(T_(4m),delta^N) for every positive integer N; equal finite dimensions imply equal spectra with algebraic multiplicity.',
        'gap_boundary':'A dimension-uniform first-order Perron contraction of E_m as delta tends to0 would itself prove a uniform gap of the corresponding spin-two rings. This is not a no-go for finite-m compressed certificates.'}
    (ROOT/'data/cp_generator_equivalence.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2));return result

if __name__=='__main__':run()
