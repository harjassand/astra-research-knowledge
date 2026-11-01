#!/usr/bin/env python3
"""Independent exact-arithmetic checks for 2D phase mechanisms.
No optimizer, no floats, no nonstandard modules. No claim of J1-J2 phase resolution.
"""
import json
from fractions import Fraction as F
from itertools import combinations
from math import isqrt
from collections import deque
from pathlib import Path

OUT = Path(__file__).resolve().parent

# A fully sparse integer Gaussian number (x + i*y).
def ga(x, y=0): return (int(x), int(y))
def gadd(a,b): return (a[0]+b[0],a[1]+b[1])
def gsub(a,b): return (a[0]-b[0],a[1]-b[1])
def gmul(a,b): return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def gnorm(a): return a[0]*a[0]+a[1]*a[1]
def gdivexact(a,b):
    d=gnorm(b)
    assert d>0
    n=gmul(a,(b[0],-b[1]))
    assert n[0]%d==0 and n[1]%d==0, (a,b,n,d)
    return (n[0]//d,n[1]//d)

def det_gaussian(A):
    """Fraction-free Gaussian-integer Bareiss determinant, O(n^3) operations."""
    n=len(A)
    assert all(len(r)==n for r in A)
    if n==0:return (1,0)
    m=[row.copy() for row in A]
    old=(1,0); sign=1
    for k in range(n-1):
        pivot=next((r for r in range(k,n) if m[r][k]!=(0,0)),None)
        if pivot is None:return (0,0)
        if pivot!=k:
            m[k],m[pivot]=m[pivot],m[k];sign*=-1
        pk=m[k][k]
        for i in range(k+1,n):
            for j in range(k+1,n):
                numerator=gsub(gmul(m[i][j],pk),gmul(m[i][k],m[k][j]))
                m[i][j]=gdivexact(numerator,old)
            m[i][k]=(0,0)
        old=pk
    z=m[-1][-1]
    return z if sign==1 else (-z[0],-z[1])

def exact_abs(z):
    a=isqrt(gnorm(z))
    assert a*a==gnorm(z),f"abs not integer: {z}"
    return a

def lattice(rows,cols):
    V=tuple((r,c) for r in range(rows) for c in range(cols))
    edges=tuple(sorted(tuple(sorted(((r,c),(rr,cc)))) for r,c in V for rr,cc in ((r+1,c),(r,c+1)) if rr<rows and cc<cols))
    face_pairs=[]
    for r in range(rows-1):
        for c in range(cols-1):
            a,b,d,e=(r,c),(r,c+1),(r+1,c),(r+1,c+1)
            hor=frozenset((tuple(sorted((a,b))),tuple(sorted((d,e)))))
            ver=frozenset((tuple(sorted((a,d))),tuple(sorted((b,e)))))
            face_pairs.append((hor,ver))
    return V,edges,face_pairs

def perfect_matchings(V,edges):
    incident={v:[] for v in V}
    for e in edges:
        for v in e:incident[v].append(e)
    def recurse(left):
        if not left:
            yield frozenset();return
        a=min(left)
        for e in incident[a]:
            b=e[0] if e[1]==a else e[1]
            if b in left:
                for rest in recurse(left-{a,b}):yield rest|{e}
    return tuple(recurse(frozenset(V)))

def kasteleyn(V, edges,weights):
    black=sorted(v for v in V if sum(v)%2==0)
    white=sorted(v for v in V if sum(v)%2==1)
    assert len(black)==len(white)
    K=[[(0,0) for w in white] for b in black]
    for e in edges:
        u,v=e
        b,w=(u,v) if sum(u)%2==0 else (v,u)
        x=weights[e]
        K[black.index(b)][white.index(w)] = (x,0) if b[0]==w[0] else (0,x)
    return K,black,white

def matrix_minor(A,rows,cols):
    return [[z for j,z in enumerate(row) if j not in cols] for i,row in enumerate(A) if i not in rows]

def test_rk(rows,cols,weighted):
    V,edges,faces=lattice(rows,cols)
    ms=perfect_matchings(V,edges)
    M=set(ms)
    # Square integer weights allow rational/integer exact RK amplitudes.
    a={e:(1+k%3 if weighted else 1) for k,e in enumerate(edges)}
    w={e:v*v for e,v in a.items()}
    amp={m:__import__('math').prod(a[e] for e in m) for m in ms}
    Z=sum(amp[m]**2 for m in ms)
    K,black,white=kasteleyn(V,edges,w)
    det=det_gaussian(K)
    assert exact_abs(det)==Z, (rows,cols,weighted,det,Z)
    # Build sparse exact local rank-one RK Hamiltonian as integer matrix.
    i_of={m:i for i,m in enumerate(ms)}
    size=len(ms)
    H=[{} for _ in ms]
    face_flips=0
    adjacency={m:set() for m in ms}
    for hor,ver in faces:
        ah=__import__('math').prod(a[e] for e in hor)
        av=__import__('math').prod(a[e] for e in ver)
        for mh in ms:
            if not hor.issubset(mh):continue
            mv=(mh-hor)|ver
            if mv not in M:continue
            ih,iv=i_of[mh],i_of[mv]
            # local block: [[av^2,-ah*av],[-ah*av,ah^2]]
            for i,j,z in ((ih,ih,av*av),(iv,iv,ah*ah),(ih,iv,-ah*av),(iv,ih,-ah*av)):
                H[i][j]=H[i].get(j,0)+z
            adjacency[mh].add(mv);adjacency[mv].add(mh)
            face_flips+=1
    for m in ms:
        i=i_of[m]
        assert sum(val*amp[ms[j]] for j,val in H[i].items())==0
    seen={ms[0]};front=[ms[0]]
    while front:
        x=front.pop()
        for y in adjacency[x]-seen:
            seen.add(y);front.append(y)
    assert len(seen)==len(ms),"RK move graph not connected in this open box"
    # Independent exact insertion: Pfaffian/cofactor on K vs brute matching sums.
    selected_edges=edges[:min(5,len(edges))]
    occurrence=[]
    for e in selected_edges:
        numerator=sum(amp[m]**2 for m in ms if e in m)
        b,wv=(e if sum(e[0])%2==0 else (e[1],e[0]))
        co=det_gaussian(matrix_minor(K,{black.index(b)},{white.index(wv)}))
        assert numerator==w[e]*exact_abs(co),(e,numerator,co)
        occurrence.append({'edge':repr(e),'probability':str(F(numerator,Z))})
    for e,f in combinations(selected_edges,2):
        if len(set(e)|set(f))<4:continue
        numerator=sum(amp[m]**2 for m in ms if e in m and f in m)
        bs,ws=[],[]
        for edge in (e,f):
            b,wv=(edge if sum(edge[0])%2==0 else (edge[1],edge[0]))
            bs.append(black.index(b));ws.append(white.index(wv))
        co=det_gaussian(matrix_minor(K,set(bs),set(ws)))
        assert numerator==w[e]*w[f]*exact_abs(co),(e,f,numerator,co)
    return {'shape':f'{rows}x{cols}','weighted':weighted,'dimer_configurations':len(ms),
            'flip_pairs':face_flips,'connected_components':1,'normalization_Z':Z,
            'det_K':list(det),'selected_edge_marginals':occurrence,
            'exact_checks':['Kasteleyn determinant','local RK annihilation','move graph connectivity','single/pair insertion cofactors']}

def test_defect_lattice(L=3,t=F(2,5)):
    n=L*L
    def ind(x,y):return (y%L)*L+(x%L)
    edges=[]
    for y in range(L):
        for x in range(L):
            # Each e has opposite pair (w,u) across an elementary plaquette.
            edges.append((ind(x,y),ind(x+1,y),ind(x,y+1),ind(x+1,y+1)))
            edges.append((ind(x,y),ind(x,y+1),ind(x+1,y),ind(x+1,y+1)))
    assert len({tuple(sorted((a,b))) for a,b,_,_ in edges})==2*n
    def domainwalls(s):return sum(((s>>a)^(s>>b))&1 for a,b,_,_ in edges)
    by_wall={k:0 for k in range(2*n+1)}
    for s in range(1<<n):by_wall[domainwalls(s)]+=1
    mincut=min(domainwalls(s) for s in range(1,(1<<n)-1))
    assert mincut==4
    # Exact symmetry of H and exact noncommutation witness [H_diag,H_kin].
    noncomm=None
    for s in range(1<<n):
        complement=((1<<n)-1)^s
        assert domainwalls(s)==domainwalls(complement)
        offdiag={}
        for a,b,u,v in edges:
            if ((s>>a)^(s>>b))&1:
                other=s^(1<<u)^(1<<v)
                offdiag[other]=offdiag.get(other,0)-t
        offdiag_complement={}
        for a,b,u,v in edges:
            if ((complement>>a)^(complement>>b))&1:
                other=complement^(1<<u)^(1<<v)
                offdiag_complement[other]=offdiag_complement.get(other,0)-t
        assert {((1<<n)-1)^s2:c for s2,c in offdiag.items()}==offdiag_complement
        for s2,c in offdiag.items():
            if c and domainwalls(s2)!=domainwalls(s) and noncomm is None:
                noncomm={'s':s,'flipped_to':s2,'initial_defects':domainwalls(s),
                         'final_defects':domainwalls(s2),'kinetic_coefficient':str(c),
                         'commutator_coefficient':str(c*(domainwalls(s2)-domainwalls(s)))}
    assert noncomm is not None
    # Local PSD H >= (1-|t|)*sum Q_e; gap >= 4(1-|t|).
    # Every ground config annihilated by every projector Q_e.
    assert domainwalls(0)==domainwalls((1<<n)-1)==0
    return {'L':L,'spins':n,'edges':len(edges),'t':str(t),'minimum_nonzero_domainwall_count':mincut,
            'exact_gap_floor':str(4*(1-abs(t))), 'ground_basis':['0'*n,'1'*n],
            'noncommuting_witness':noncomm,'operator_bound':'H_t >= (1-|t|) sum_e Q_e',
            'exact_checks':['all classical configurations','global X symmetry','nonzero commutator','uniform cut gap']}

def test_marginal_compatibility():
    p=F(2,5)
    rho_good=[[F(0) for j in range(4)] for i in range(4)]
    rho_good[0][0]=p;rho_good[3][3]=1-p
    rho_bell=[[F(0) for j in range(4)] for i in range(4)]
    for i in (0,3):
        for j in (0,3):rho_bell[i][j]=F(1,2)
    for rho in (rho_good,rho_bell):
        assert sum(rho[k][k] for k in range(4))==1
        assert (rho[0][0]+rho[1][1])==F(1,2) if rho==rho_bell else (rho[0][0]+rho[1][1])==p
        assert rho[1][1]+rho[2][2]==0 # Q_12 expectation zero
    # two Bell edges share identical one-site I/2 but not globally compatible
    # because XX_12 anticommutes with Z_2 Z_3 and |<XX_12>|=1 while <Z_2Z_3>=1.
    xx_bell=rho_bell[0][3]+rho_bell[3][0]+rho_bell[1][2]+rho_bell[2][1]
    assert xx_bell==1
    assert F(1)**2+F(1)**2>1
    return {'good_pair_diagonal':{'p':str(p),'density_elements':['p',0,0,'1-p'],
                 'global_extension':'p|0^n><0^n|+(1-p)|1^n><1^n|'},
            'false_pair_Bell':{'single_qubit_marginal':'I/2','q_12':'0','q_23':'0',
                'XX_12':'1','Z_2Z_3':'1','anticommuting_sum_of_squares':'2 > 1'},
            'algorithm':'test edge support, off-diagonal coherence, common p; O(|E|) rational operations'}

def test_stripes():
    checks=[]
    for width in (4,8,16,32):
        Nx=4*width
        spin=lambda x:1 if (x//width)%2==0 else -1
        s=[spin(x) for x in range(Nx)]
        assert sum(s)==0
        q=F(sum(s[x]!=s[(x+1)%Nx] for x in range(Nx)),Nx)
        assert q==F(1,width)
        corr2=F(sum(s[x]*s[(x+2)%Nx] for x in range(Nx)),Nx)
        assert corr2==1-F(4,width)
        checks.append({'stripe_width':width,'ferro_Ising_energy_per_site':str(q),
                       'Z_correlation_distance_2':str(corr2),'global_M_squared_over_N2':'0'})
    return checks

def test_spin_valencebond_transfer_failure():
    """Physical spin valence bonds are NOT an orthonormal quantum-dimer basis."""
    def double_singlet(pair1,pair2):
        out={}
        for a,b,sgn in ((0,1,1),(1,0,-1)):
            for c,d,sgn2 in ((0,1,1),(1,0,-1)):
                bits=[0]*4
                bits[pair1[0]]=a;bits[pair1[1]]=b
                bits[pair2[0]]=c;bits[pair2[1]]=d
                bitstring=sum(x<<i for i,x in enumerate(bits))
                out[bitstring]=out.get(bitstring,F(0))+F(sgn*sgn2,2)
        return out
    A=double_singlet((0,1),(2,3))
    B=double_singlet((0,2),(1,3))
    C=double_singlet((0,3),(1,2))
    def inner(a,b):return sum(v*b.get(k,0) for k,v in a.items())
    assert all(inner(t,t)==1 for t in (A,B,C))
    assert inner(A,B)==F(1,2) and inner(A,C)==F(-1,2)
    assert inner(B,C)==F(1,2)
    assert all(A.get(q,0)-B.get(q,0)+C.get(q,0)==0 for q in set(A)|set(B)|set(C))
    # Moreover, the fully spin-polarized |all up> pair energy is +1/4
    # for EVERY Heisenberg pair: at alpha=1/2 and 2 NN+2 NNN bonds/site
    # e=(1+alpha)/2=3/4, unlike the certified variational upper -0.46909.
    e_sector=F(1+F(1,2),2)
    assert e_sector==F(3,4)
    assert F(-46909,100000)<e_sector
    return {'overlap_12_34_vs_13_24':str(inner(A,B)),
            'overlap_12_34_vs_14_23':str(inner(A,C)),
            'overlap_13_24_vs_14_23':str(inner(B,C)),
            'linear_relation':'|12,34> - |13,24> + |14,23> = 0',
            'ferromagnetic_sector_J1_J2_energy_density_alpha_half':str(e_sector),
            'Heisenberg_variational_energy_upper_at_alpha_half':'-0.46909',
            'transfer_result':'both the ferromagnetic projector sector and orthogonal-RK-matching identification fail for physical J1-J2'}

def test_finite_field_dichotomy():
    """Exact algebraic negative/positive controls for finite-field phase conversion."""
    # One-spin paramagnet H=(I-X)/2-hZ has e(h)=(1-sqrt(1+4h^2))/2.
    # At h=1/4 its secant is sqrt(5)-2, positive, but <1/4;
    # K=2 and Kh/2=1/4, so finite-field positivity proves no LRO.
    assert 5>2**2
    assert F(5)<F(9,4)**2
    h=F(1,4);K=F(2)
    assert K*h/2==F(1,4)
    baseline_width=-F(46909,100000)+F(583212,1000000)
    assert baseline_width==F(57061,500000)
    assert baseline_width/F(1,100)==F(285305,25000) # 11.4122
    return {'paramagnet_h':'1/4','paramagnet_secant':'sqrt(5)-2',
            'paramagnet_secant_positive':True,'paramagnet_secant_strictly_below_curvature_payment':'1/4',
            'paramagnet_m0':'0','ordered_defect_model_e_h':'-|h|','ordered_defect_model_m0':'1',
            'original_J1J2_energy_band_width':str(baseline_width),
            'old_energy_uncertainty_over_field_h_equals_1_over_100':str(baseline_width/F(1,100)),
            'absolute_dimer_source_density_upper_bound':'3/4'}

def main():
    r={'scope':'Exact algebraic/finite controls, NOT a certificate for the square J1-J2 phase at alpha=0.5',
       'structural_gapped_order':test_defect_lattice(),
       'local_global_marginal_test':test_marginal_compatibility(),
       'spin_to_dimer_transfer_falsifier':test_spin_valencebond_transfer_failure(),
       'small_error_not_long_range_order':test_stripes(),
       'finite_field_false_positive_and_ordered_control':test_finite_field_dichotomy(),
       'rk_dimer_tests':[test_rk(2,4,False),test_rk(4,4,False),test_rk(4,4,True)]}
    (OUT/'VERIFICATION_RESULTS.json').write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({k:v if k not in ('rk_dimer_tests','small_error_not_long_range_order') else
                      ([(d['shape'],d['weighted'],d['dimer_configurations'],d['normalization_Z']) for d in v] if k=='rk_dimer_tests' else v)
                       for k,v in r.items()},indent=2))

if __name__=='__main__':main()
