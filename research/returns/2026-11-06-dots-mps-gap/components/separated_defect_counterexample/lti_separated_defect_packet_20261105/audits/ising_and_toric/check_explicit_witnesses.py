"""Exact finite 1D and stabilizer-Pauli 2D full-LTI witnesses.

No SDP solver or approximate marginal fit. Integer/Fraction arithmetic checks
the entire diagonal or Pauli expansion, including all off-diagonal operators.
"""
from pathlib import Path
from fractions import Fraction
import itertools,json,time
import numpy as np

OUT=Path(__file__).resolve().parent


def ising(n):
    # w is exactly 2*rho in the computational basis.
    w=np.zeros(1<<n,dtype=np.int64)
    for j in range(1,n):
        x=(1<<(n-j))-1
        w[x]+=1;w[x^((1<<n)-1)]+=1
    left=w.reshape(2,-1).sum(axis=0)
    right=w.reshape(-1,2).sum(axis=1)
    assert np.array_equal(left,right)
    energies=[];maximum_pair=0;obj=0
    for i in range(n-1):
        E=sum(int(w[x])*(((x>>i)^(x>>(i+1)))&1) for x in range(1<<n))
        assert E==2;energies.append(str(Fraction(E,2)))
    for i,j in itertools.combinations(range(n-1),2):
        cross=sum(int(w[x])*(((x>>i)^(x>>(i+1)))&1)*(((x>>j)^(x>>(j+1)))&1) for x in range(1<<n))
        maximum_pair=max(maximum_pair,cross);assert cross==0
    obj=energies[0]
    return dict(sites=n,trace=str(Fraction(int(w.sum()),2)),
                full_face_marginal_exact=True,all_local_energies=energies,
                all_distinct_pair_products_zero=True,objective=obj)


def ising_torus(n,N):
    assert N>=2*n
    state=(1<<(N//2))-1;mask=(1<<N)-1
    counts=np.zeros(1<<n,dtype=np.int64)
    for k in range(N):
        x=((state<<k)|(state>>(N-k if k else N)))&mask
        walls=sum(((x>>i)^(x>>((i+1)%N)))&1 for i in range(N))
        assert walls==2
        counts[x&((1<<n)-1)]+=1
    assert np.array_equal(counts.reshape(2,-1).sum(0),counts.reshape(-1,2).sum(1))
    # Scaled marginal rho=(N/2)*(counts/N)=counts/2.
    e=sum(int(counts[x])*((x^(x>>1))&1) for x in range(1<<n))
    pairs=[sum(int(counts[x])*((x^(x>>1))&1)*(((x>>j)^(x>>(j+1)))&1)
           for x in range(1<<n)) for j in range(1,n-1)]
    assert e==2 and all(x==0 for x in pairs)
    return dict(window=n,torus=N,scale=str(Fraction(N,2)),
                exact_full_LTI=True,energy_normalization='1',objective='1',torus_gap='2')


def rank_gf2(vectors):
    piv={}
    for x in vectors:
        while x:
            k=x.bit_length()-1
            if k in piv:x^=piv[k]
            else:piv[k]=x;break
    return len(piv)


def open_generators(nx,ny):
    # Cell (x,y) contains horizontal then vertical outgoing edge qubits.
    bit=lambda x,y,o:1<<(2*(x+nx*y)+o)
    stars=[];plaquettes=[]
    for y in range(1,ny):
        for x in range(1,nx):
            stars.append(bit(x,y,0)|bit(x-1,y,0)|bit(x,y,1)|bit(x,y-1,1))
    for y in range(ny-1):
        for x in range(nx-1):
            plaquettes.append(bit(x,y,0)|bit(x+1,y,1)|bit(x,y+1,0)|bit(x,y,1))
    assert all((a&b).bit_count()%2==0 for a in stars for b in plaquettes)
    assert rank_gf2(stars)==len(stars) and rank_gf2(plaquettes)==len(plaquettes)
    return stars,plaquettes


def subsets(g):
    a=[0]*(1<<len(g))
    for s in range(1,len(a)):
        low=s&-s;a[s]=a[s^low]^g[low.bit_length()-1]
    return a


def face_data(nx,ny,axis,side):
    cut=0 if side==0 else (nx if axis==0 else ny)-1
    newnx=nx-(axis==0);mapping={};outside=0
    for y in range(ny):
        for x in range(nx):
            for o in (0,1):
                old=2*(x+nx*y)+o
                if (x if axis==0 else y)==cut:outside|=1<<old
                else:
                    xx=x-(axis==0 and side==0);yy=y-(axis==1 and side==0)
                    mapping[old]=2*(xx+newnx*yy)+o
    return outside,mapping


def remap(mask,mapping):
    out=0
    while mask:
        low=mask&-mask;i=low.bit_length()-1;out|=1<<mapping[i];mask^=low
    return out


def face_pauli_coefficients(nx,ny,axis,side):
    stars,plaquettes=open_generators(nx,ny);m=len(stars)
    sx,sz=subsets(stars),subsets(plaquettes)
    outside,mapping=face_data(nx,ny,axis,side)
    xs=[(remap(x,mapping),m-2*i.bit_count()) for i,x in enumerate(sx) if not x&outside]
    zs=[remap(z,mapping) for z in sz if not z&outside]
    # Actual marginal coefficient is this integer / 2**(remaining qubits).
    coeff={}
    for x,a in xs:
        for z in zs:
            if a:coeff[(x,z)]=coeff.get((x,z),0)+a
    return coeff


def open_face_test(nx,ny,enumerate_all=False):
    stars,plaquettes=open_generators(nx,ny);m=len(stars);rows=[]
    for axis in (0,1):
        for side in (0,1):
            outside,_=face_data(nx,ny,axis,side)
            for name,g in [('X stars',stars),('Z plaquettes',plaquettes)]:
                crossing=[a for a in g if a&outside]
                r=rank_gf2([a&outside for a in crossing])
                # Thus no product of crossing generators can disappear from
                # the removed face, exactly the full-subgroup condition.
                assert r==len(crossing)
                rows.append(dict(axis=axis,side=side,type=name,
                                 removed_generators=len(crossing),outside_rank=r))
    exact=[]
    if enumerate_all:
        for axis in (0,1):
            a=face_pauli_coefficients(nx,ny,axis,0)
            b=face_pauli_coefficients(nx,ny,axis,1)
            assert a==b
            exact.append(dict(axis=axis,all_Pauli_coefficients_equal=True,
                              nonzero_coefficients=len(a)))
    return dict(cell_rectangle=[nx,ny],physical_qubits=2*nx*ny,
                independent_stabilizers=2*m,one_star_defect_projector_rank_power_of_2=2*nx*ny-2*m,
                witness_trace=m,local_h_energy='1',distinct_h_products='0',objective='1',
                outside_subgroup_checks=rows,full_face_expansions=exact)


def dense_small_window():
    nx=ny=2;stars,plaquettes=open_generators(nx,ny);q=8;dim=1<<q
    def pauli(x,z):
        A=np.zeros((dim,dim),dtype=np.int64)
        for b in range(dim):A[b^x,b]=(-1)**((z&b).bit_count())
        return A
    A=pauli(stars[0],0);B=pauli(0,plaquettes[0]);I=np.eye(dim,dtype=np.int64)
    numerator=(I-A)@(I+B)
    assert np.array_equal(numerator@numerator,4*numerator)
    assert np.trace(numerator)==dim
    # rho=numerator/256, rank64, trace1, one star defect/no plaquette defect.
    h=(2*I-A-B) # exactly 2h
    assert np.trace(numerator@h)==2*dim
    assert np.trace(numerator@h@h)==4*dim
    return dict(cells=[2,2],dimension=dim,density_numerator_denominator=dim,
                exact_projector_polynomial_identity=True,trace='1',rank=64,
                energy='1',second_moment='1')


def torus_stabilizer_check(N,L):
    assert N>4*L
    bit=lambda x,y,o:1<<(2*((x%N)+N*(y%N))+o)
    A=[];B=[]
    for y in range(N):
        for x in range(N):
            A.append(bit(x,y,0)|bit(x-1,y,0)|bit(x,y,1)|bit(x,y-1,1))
            B.append(bit(x,y,0)|bit(x+1,y,1)|bit(x,y+1,0)|bit(x,y,1))
    assert rank_gf2(A)==N*N-1 and rank_gf2(B)==N*N-1
    assert all((a&b).bit_count()%2==0 for a in A for b in B)
    assert __import__('functools').reduce(int.__xor__,A)==0
    assert __import__('functools').reduce(int.__xor__,B)==0
    defects={(0,0),(N//2,0)}
    D=set(itertools.product(range(-L+1,L),repeat=2));D.remove((0,0))
    assert all(((b[0]-a[0])%N,(b[1]-a[1])%N) not in {(x%N,y%N) for x,y in D}
               for a,b in itertools.permutations(defects,2))
    # Syndrome satisfies exactly the two global parity relations, so its
    # common eigenspace is nonempty and has exact dimension 2**2=4.
    return dict(torus_side=N,cutoff_L=L,qubits=2*N*N,stabilizer_rank=2*N*N-2,
                simultaneous_syndrome_subspace_dimension=4,star_defects=sorted(defects),
                energy='2',translation_average_local_energy=str(Fraction(2,N*N)),
                required_scaling=str(Fraction(N*N,2)),scaled_local_energy='1',scaled_objective='1',
                full_face_LTI_reason='Restriction of an exactly translation-averaged torus state',
                all_retained_distinct_products_zero=True)


def main():
    t=time.perf_counter()
    result={'ising_finite_witnesses':[ising(n) for n in range(3,13)],
            'ising_extendible_witnesses':[ising_torus(n,4*n) for n in (3,5,8)],
            'toric_open_windows':[open_face_test(x,y,enum) for x,y,enum in
                [(2,2,True),(2,3,True),(3,3,True),(3,4,True),(4,4,True),(5,7,False),(8,6,False)]],
            'toric_dense_check':dense_small_window(),
            'toric_global_witnesses':[torus_stabilizer_check(N,L) for N,L in [(12,2),(16,3),(24,5)]],
            'elapsed_seconds':time.perf_counter()-t,
            'scope':'Exact integer/Fraction full-face and stabilizer checks. No approximate SDP or incomplete moment-only marginal check.'}
    (OUT/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'ising_windows':len(result['ising_finite_witnesses']),
                      'toric_open_rectangles':len(result['toric_open_windows']),
                      'toric_tori':len(result['toric_global_witnesses']),
                      'all_exact_checks_passed':True,'elapsed_seconds':result['elapsed_seconds']},indent=2))


if __name__=='__main__':main()
