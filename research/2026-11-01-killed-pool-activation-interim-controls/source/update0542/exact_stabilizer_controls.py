"""Independent dense controls and compact completeness certificates."""
import hashlib,itertools,json,random,time
import numpy as np
from pathlib import Path
from exact_stabilizer import (ZMatrix,ExactPauliMPS,ghz_phase,paper_algorithm6,
                             independent,pauli_name)

ROOT=Path(__file__).resolve().parents[2]


def zadd(a,b):return a[0]+b[0],a[1]+b[1]
def zmul(a,b):return a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]
def zconj(a):return a[0],-a[1]


def dense_state(tensors):
    out=[]
    for bits in itertools.product((0,1),repeat=len(tensors)):
        row=ZMatrix.make([[1]])
        for site,b in zip(tensors,bits):row=row@site[b]
        out.append(row.scalar())
    return out


def dense_coefficient(psi,label,n):
    flip=0;zmask=0;ys=0
    for i in range(n):
        x=(label>>(2*i))&1;z=(label>>(2*i+1))&1
        flip|=x<<(n-1-i);zmask|=z<<(n-1-i);ys+=x*z
    base=((1,0),(0,1),(-1,0),(0,-1))[ys%4]
    val=(0,0)
    for t,a in enumerate(psi):
        phase=base if not ((t&zmask).bit_count()%2) else (-base[0],-base[1])
        val=zadd(val,zmul(zconj(psi[t^flip]),zmul(phase,a)))
    assert val[1]==0
    return val[0]


def certify(mps,result):
    """Verify completeness using only ordinary single-Pauli contractions.

    k independent stabilizers give a lower dimension bound k. A family of
    2n-k independent NONZERO Pauli coefficients gives the matching upper bound
    by the support-annihilator identity. No energy/zero query is replayed.
    """
    basis=[]
    for v in result['support_basis']:
        assert mps.coefficient(v)!=0 and independent(basis,v)
        basis.append(v)
    gs=[]
    for g in result['generators']:
        assert independent(gs,g['label'])
        assert mps.coefficient(g['label'])==g['sign']*mps.norm
        gs.append(g['label'])
    assert len(gs)+len(basis)==2*mps.n
    return True


def random_mps(n,rng):
    out=[]
    for i in range(n):
        dl=1 if i==0 else 2;dr=1 if i==n-1 else 2
        site=[]
        for _ in (0,1):
            re=[[rng.randrange(-2,3) for _ in range(dr)] for _ in range(dl)]
            im=[[rng.randrange(-1,2) for _ in range(dr)] for _ in range(dl)]
            site.append(ZMatrix.make(re,im))
        out.append(tuple(site))
    return out


def main():
    rng=random.Random(20261101);rows=[];dense_words=0
    cases=[]
    for n in range(1,6):
        for rep in range(3):cases.append((f'random_Gaussian_integer_n{n}_{rep}',random_mps(n,rng)))
    for n in (2,3,5):
        cases.append((f'GHZ_generic_phase_n{n}',ghz_phase(n)))
        cases.append((f'GHZ_Clifford_phase_n{n}',ghz_phase(n,(1,0),(1,0))))
    # Positive and negative Y eigenstates test the complex/phase conventions.
    for sign in (-1,1):
        cases.append((f'Y_eigenstate_sign_{sign}',[(ZMatrix.make([[1]]),ZMatrix.make([[0]],[[sign]]))]))
    cases.append(('fixed_width_input_promoted_to_bigint',[(ZMatrix.make(np.array([[1<<62]],dtype=np.int64)),ZMatrix.make([[1]]))]))
    for name,tensors in cases:
        mps=ExactPauliMPS(tensors);result=mps.extract();assert certify(mps,result)
        psi=dense_state(tensors);n=len(tensors);norm=sum(a*a+b*b for a,b in psi)
        expected=[];actual={0}
        for g in result['generators']:actual|={v^g['label'] for v in list(actual)}
        for v in range(1<<(2*n)):
            c=dense_coefficient(psi,v,n);dense_words+=1
            assert c==mps.coefficient(v)
            if abs(c)==norm:expected.append(v)
        assert set(expected)==actual
        assert result['parity_contractions'] <= (2*n+1)**2
        rows.append({'name':name,'qubits':n,'stabilizer_dimension':result['stabilizer_dimension'],
                     'parity_contractions':result['parity_contractions'],
                     'dense_Paulis_checked':1<<(2*n),'completeness_certificate':'PASS'})
    m=ExactPauliMPS(ghz_phase(2));exact=m.extract();heuristic=paper_algorithm6(m,[2,1])
    assert exact['stabilizer_dimension']==1 and heuristic['dimension']==0
    counter={'unnormalized_state':'5|00>+(3+4i)|11>', 'normalization_squared':50,
             'true_generators':exact['generators'],'displayed_Algorithm6':heuristic,
             'scope':'Literal displayed algorithm with implicit identity and stable I,X,Y,Z ties; no claim about unseen code.'}
    large=[]
    for n in (16,32,64):
        start=time.perf_counter();m=ExactPauliMPS(ghz_phase(n));result=m.extract()
        assert result['stabilizer_dimension']==n-1 and certify(m,result)
        large.append({'qubits':n,'input_MPS_bond':2,'Pauli_MPS_bond':4,
                      'stabilizer_dimension':result['stabilizer_dimension'],
                      'parity_contractions':result['parity_contractions'],
                      'elapsed_seconds':time.perf_counter()-start,'completeness_certificate':'PASS'})
    bits=1024;m=ExactPauliMPS(ghz_phase(2,(1<<bits,0),(1,0)))
    rare=m.extract();assert rare['stabilizer_dimension']==1 and certify(m,rare)
    energy=m.suffix_environments(1)[0][1].scalar()[0]
    total=(1<<m.n)*m.norm**2
    assert energy*(1<<2040)<total
    rare_case={'large_amplitude_input_bits':bits+1,'stabilizer_dimension':rare['stabilizer_dimension'],
               'exact_parity_energy_numerator_bits':energy.bit_length(),
               'normalizing_total_energy_bits':total.bit_length(),
               'normalized_query_mass_less_than':'2^-2040',
               'parity_contractions_for_extraction':rare['parity_contractions'],
               'completeness_certificate':'PASS',
               'scope':'Explicit exact classical MPS; this is not a physical-copy/sample bound.'}
    try:ExactPauliMPS([(ZMatrix.make([[0]]),ZMatrix.make([[0]]))])
    except AssertionError:zero_rejected=True
    else:raise AssertionError('Zero state accepted.')
    result={'status':'PASS exact arithmetic and independent dense controls',
            'small_cases':rows,'independent_dense_Paulis_checked':dense_words,
            'displayed_heuristic_counterexample':counter,'larger_tensor_controls':large,
            'rare_support_case':rare_case,'zero_state_rejected':zero_rejected,
            'scope':'All-input theorem is analytical; finite checks validate the implementation at these inputs. No novelty or broad quantum-simulation advantage claimed.',
            'source_sha256':hashlib.sha256((Path(__file__).parent/'exact_stabilizer.py').read_bytes()).hexdigest(),
            'control_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (ROOT/'outputs/mechanism_selection_20261101/exact_stabilizer_controls.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('status','independent_dense_Paulis_checked','larger_tensor_controls','rare_support_case')},indent=2),flush=True)


if __name__=='__main__':main()
