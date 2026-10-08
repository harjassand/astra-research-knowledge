"""Exact Clifford-word replay of four attainable Spin(11) pure moments."""
import importlib.util
from pathlib import Path
import sympy as sp
HERE=Path(__file__).parent
spec=importlib.util.spec_from_file_location('spin11_blocks',HERE/'spin11_fullstar_blocks.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

def seed_moments(a,b=None):
    # |0> if b is omitted, otherwise (|a>+|b>)/sqrt(2); chosen seeds have real amplitudes.
    amp={a:sp.Integer(1)} if b is None else {a:sp.Integer(1),b:sp.Integer(1)}
    den=len(amp); result=[]
    for k in range(1,6):
        score=sp.Integer(0)
        for A,ph,w in m.e_basis(k):
            expectation=sp.Integer(0)
            for src,asrc in amp.items():
                out,p=m.apply_word(w,src)
                if out in amp:
                    expectation += sp.conjugate(amp[out])*(sp.I**(ph+p))*asrc/den
            expectation=sp.simplify(expectation)
            if expectation.is_real is not True:raise AssertionError(('nonreal pure expectation',k,A,expectation))
            score+=expectation**2
        result.append(sp.factor(score))
    if sum(result)!=31:raise AssertionError(('Parseval moment sum',result))
    return tuple(result)

seeds={'coherent_basis_state':seed_moments(0)}
for h in (3,4,5):
    seeds[f'two_weight_hamming_{h}']=seed_moments(0,(1<<h)-1)
expected={'coherent_basis_state':(1,5,5,10,10),'two_weight_hamming_3':(0,2,7,8,14),
          'two_weight_hamming_4':(1,1,1,14,14),'two_weight_hamming_5':(0,0,5,10,16)}
if seeds!=expected:raise AssertionError(('seed moment mismatch',seeds,expected))
for name,v in seeds.items():print(name, list(v), 'sum=',sum(v))
print('EXACT SEED MOMENTS PASS: grades 1..5 over all 1023 nonidentity Clifford words.')
