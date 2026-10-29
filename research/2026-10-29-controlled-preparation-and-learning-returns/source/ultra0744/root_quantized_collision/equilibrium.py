"""Exact algebra for the ordinary comparator and one same-bin execution."""
from pathlib import Path
from fractions import Fraction as F
from dataclasses import asdict
import json,random,time
import sympy as s
from flint import arb,ctx
from quantized import Counts,Bits,Normal,const,quantize,ROTATIONS

def main():
    basis = [s.diag(1,0,0),s.diag(0,1,0),s.diag(0,0,1)]
    for i,j in [(0,1),(0,2),(1,2)]:
        e = s.zeros(3);e[i,j]=e[j,i]=1;basis.append(e)
    rs = [s.Matrix(3,3,r) for r in ROTATIONS]
    def vec(a):
        return s.Matrix([a[0,0],a[1,1],a[2,2],a[0,1],a[0,2],a[1,2]])
    generator = s.Matrix.hstack(*[vec((sum((r*e*r.T for r in rs),s.zeros(3))/4-e)/2)
                                 for e in basis])
    gram = s.diag(1,1,1,2,2,2)
    assert generator.T*gram == gram*generator
    assert generator.eigenvals() == {s.Rational(0):1,s.Rational(-1,4):1,
                                     s.Rational(-1,2):1,s.Rational(-3,4):3}
    x = s.symbols('d0:6')
    d = sum((v*e for v,e in zip(x,basis)),s.zeros(3))
    form = 0
    for r in rs:
        a,b = (s.eye(3)+r)/2,(s.eye(3)-r)/2
        p,q = a.T*a,b.T*b
        form += s.trace(d*p*d*p+d*q*d*q)/4
    remainder = s.Poly(s.expand(s.Rational(3,4)*s.trace(d*d)-form),*x)
    assert all(c>=0 for monomial,c in remainder.terms())
    assert all(sum(monomial)==2 and max(monomial)==2 for monomial,c in remainder.terms())
    sigma1 = s.diag(1,s.Rational(21,20),s.Rational(11,10))
    sigma2 = s.Matrix([[s.Rational(26,25),s.Rational(1,25),0],
                      [s.Rational(1,25),s.Rational(26,25),0],[0,0,s.Rational(21,20)]])
    mu = s.trace((sigma1+sigma2)/2)/3
    v0 = sum(s.trace((sigma-mu*s.eye(3))**2) for sigma in [sigma1,sigma2])/2
    assert mu == s.Rational(157,150) and v0 == s.Rational(1,240)
    rng = random.Random(2026102997);counts = Counts();bits = Bits(lambda:rng.getrandbits(1),counts)
    scale = const(F(157,150),counts).sqrt()
    outputs = []
    tick = time.perf_counter()
    for _ in range(200):
        outputs.append([quantize(scale*Normal(bits),F(1,4),counts) for j in range(3)])
    seconds = time.perf_counter()-tick
    ctx.prec = max(ctx.prec,128)
    threshold_test = arb(1)/5*(-arb(100)/8).exp()
    assert threshold_test.upper() < arb('1e-6').lower()
    result = dict(scope='exact six-dimensional algebra and one ordinary approximate-target same-bin sampler execution',
        mean_generator=[list(map(str,generator.row(i))) for i in range(6)],
        exact_eigenvalues={str(k):v for k,v in generator.eigenvals().items()},
        frobenius_metric=list(map(str,gram.diagonal())),
        dispersion_remainder=str(remainder.as_expr()),mu=str(mu),initial_dispersion=str(v0),
        target_accuracy_contract='TV to exact transient bin law <= (1/5)exp(-t/8); t>=100 pays epsilon1e-6',
        strict_arb_t100_bound=str(threshold_test),seed=2026102997,n=200,integer_bins=outputs,
        quantization_width='1/4',counts=asdict(counts),seconds=seconds,
        excluded='not exact transient samples, not a hard-sphere bound, not historical novelty')
    Path(__file__).with_name('EQUILIBRIUM_EXECUTION.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['scope','exact_eigenvalues','dispersion_remainder','mu',
        'initial_dispersion','strict_arb_t100_bound','n','counts','seconds']},indent=2))

if __name__=='__main__':
    main()
