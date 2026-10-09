"""Exact rational certificate for the qubit depolarizing Gram/RLD value 3/8.

Requires SymPy. No floating-point numbers or SDP solver are used.
This verifies a finite instance, not the universal analytical theorem.
"""
from pathlib import Path
import json
import sympy as s


def depol(x):
    return x/2 + s.eye(2)*s.trace(x)/4


def blockmap(x):
    return s.BlockMatrix([[depol(x[2*i:2*i+2, 2*j:2*j+2])
                           for j in range(x.cols//2)]
                          for i in range(x.rows//2)]).as_explicit()


def ptrace(x):
    return s.Matrix(x.rows//2, x.cols//2,
                    lambda i,j: s.trace(x[2*i:2*i+2, 2*j:2*j+2]))


def main():
    eta=s.Rational(3,8)
    fs=[]
    for i in range(2):
        for j in range(2):
            f=s.zeros(2); f[i,j]=1; fs.append(f)
    a=s.Matrix.vstack(*(depol(f) for f in fs))
    alpha=s.Matrix([(1-eta)*s.trace(f)/2 for f in fs])
    ac=a-s.kronecker_product(alpha,s.eye(2))
    g=s.BlockMatrix([[depol(f*h.H) for h in fs] for f in fs]).as_explicit()
    defect=eta*g-ac*ac.H
    evals=defect.eigenvals()
    assert evals == {s.Rational(0):2,s.Rational(3,32):4,s.Rational(15,128):2}
    z=s.Matrix.hstack(*defect.nullspace())
    proj=z*(z.H*z).inv()*z.H
    c=proj/2
    b=c*ac
    assert s.trace(c)==1 and c.is_hermitian
    assert ptrace(b)==s.zeros(4,1)
    # C is half an orthogonal projection, so C^+=4C exactly.
    cp=4*c
    assert c*cp*c==c and cp*c*cp==cp
    nc=blockmap(c); nb=blockmap(b)
    ncp=nc.pinv()
    qi=s.simplify(s.trace(b.H*cp*b))
    qo=s.simplify(s.trace(nb.H*ncp*nb))
    assert qo/qi==eta
    assert c*cp*b==b and nc*ncp*nb==nb
    # Upper certificate: sigma=I/2, unnormalized Choi J.
    omega=s.Matrix([1,0,0,1])
    choi=omega*omega.H/2+s.eye(4)/4
    sig=s.eye(4)/2
    weighted=s.simplify(sig*choi.inv()*sig)
    tr_b=ptrace(weighted)
    assert tr_b==s.Rational(8,5)*s.eye(2)
    assert 1-1/s.Rational(8,5)==eta
    out={
      'status':'PASS',
      'arithmetic':'Exact SymPy rational arithmetic; no floating point',
      'scope':'One finite qubit depolarizing Gram/RLD instance; NOT a formalization of the general theorem',
      'eta':'3/8', 'M':'8/5',
      'gram_defect_eigenvalues':{str(k):v for k,v in evals.items()},
      'input_RLD_quadratic_form':str(qi),
      'output_RLD_quadratic_form':str(qo),
      'partial_trace_B':'exactly zero',
      'C':[[str(v) for v in row] for row in c.tolist()],
      'B':[[str(v) for v in row] for row in b.tolist()],
    }
    path=Path(__file__).with_suffix('.json')
    path.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ['C','B']},indent=2))

if __name__=='__main__': main()
