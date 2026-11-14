"""Independent symbolic audit of the sharp uniform-Schmidt interval.

Parses only arithmetic matrix expressions via AST, never imports or executes
the producer's Python. Independently recomputes generalized characteristic
polynomials, sharp eigenvectors, inequalities, and positive denominator signs.
"""
import ast
from pathlib import Path
import hashlib,json,time
import sympy as sp

d=sp.Symbol('d',real=True,positive=True)
x=sp.Symbol('x',real=True,nonnegative=True)
z=sp.Symbol('z',real=True)


def parse_arithmetic(node):
    if isinstance(node,ast.Constant) and isinstance(node.value,int):return sp.Integer(node.value)
    if isinstance(node,ast.Name) and node.id=='d':return d
    if isinstance(node,ast.UnaryOp):
        val=parse_arithmetic(node.operand)
        if isinstance(node.op,ast.USub):return -val
        if isinstance(node.op,ast.UAdd):return val
    if isinstance(node,ast.BinOp):
        a=parse_arithmetic(node.left);b=parse_arithmetic(node.right)
        if isinstance(node.op,ast.Add):return a+b
        if isinstance(node.op,ast.Sub):return a-b
        if isinstance(node.op,ast.Mult):return a*b
        if isinstance(node.op,ast.Div):return a/b
        if isinstance(node.op,ast.Pow):return a**b
    raise ValueError(ast.dump(node))


def parse_matrix(text):
    node=ast.parse(text,mode='eval').body
    assert isinstance(node,ast.Call) and isinstance(node.func,ast.Name) and node.func.id=='Matrix'
    assert len(node.args)==1 and not node.keywords
    rows=node.args[0];assert isinstance(rows,ast.List)
    assert all(isinstance(row,ast.List) for row in rows.elts)
    return sp.Matrix([[parse_arithmetic(v) for v in row.elts] for row in rows.elts])


def positive_rational(expr):
    value=sp.cancel(expr.subs(d,x+3));num,den=sp.fraction(value)
    ncoeff=sp.Poly(num,x).all_coeffs();dcoeff=sp.Poly(den,x).all_coeffs()
    assert all(v>=0 for v in ncoeff) and num.subs(x,0)>0
    assert all(v>=0 for v in dcoeff) and den.subs(x,0)>0
    return {'numerator_at_d_x_plus3':str(sp.factor(num)),
            'denominator_at_d_x_plus3':str(sp.factor(den)),'strictly_positive':True}


def main():
    start=time.perf_counter();root=Path(__file__).parent
    source=root/'uniform_source_sharp.json';data=json.loads(source.read_text())
    C0=parse_matrix(data['C_trivial']);S0=parse_matrix(data['S_trivial']);G0=parse_matrix(data['G_trivial'])
    C1=parse_matrix(data['C_adjoint']);S1=parse_matrix(data['S_adjoint']);G1=parse_matrix(data['G_adjoint'])
    a=d-1;b=5*d-4;ell=-(5*d+1)/(9*a);v=-(6*d*d-13*d+4)/(3*a*b)
    Q=27*a*b*z*z+(15*d*d-90*d+24)*z-(6*d*d+19*d+4)
    def cp(M):return M.charpoly(z).as_expr().subs(next(s for s in M.charpoly(z).as_expr().free_symbols if s.name=='z'),z)
    checks={
      'G0C0_symmetric':(G0*C0-(G0*C0).T).applyfunc(sp.simplify)==sp.zeros(2),
      'G0S0_symmetric':(G0*S0-(G0*S0).T).applyfunc(sp.simplify)==sp.zeros(2),
      'G1C1_symmetric':(G1*C1-(G1*C1).T).applyfunc(sp.simplify)==sp.zeros(4),
      'G1S1_symmetric':(G1*S1-(G1*S1).T).applyfunc(sp.simplify)==sp.zeros(4),
      'trivial_generalized_charpoly':sp.factor(cp(C0.inv()*S0)-(z-1)*(z-ell))==0,
      'traceless_generalized_charpoly':sp.factor(cp(C1.inv()*S1)-(z-1)*(z-v)*Q/(27*a*b))==0,
      'Q_at1_identity':sp.factor(Q.subs(z,1)-16*(d-2)*(9*d-4))==0,
      'Q_atell_identity':sp.factor(Q.subs(z,ell)-2*d*d*(41*d+28)/(3*a))==0}
    w=sp.Matrix([4*d-5,5*d-4]);f=sp.Matrix([1,0])
    checks['upper_endpoint_f']=((S0-C0)*f).applyfunc(sp.factor)==sp.zeros(2,1)
    checks['lower_endpoint_w']=((S0-ell*C0)*w).applyfunc(sp.factor)==sp.zeros(2,1)
    cw=(w.T*G0*C0*w)[0]
    checks['sharp_C_quadratic_form']=sp.factor(cw-sp.Rational(9,4)*d*a*(d+1)*b)==0
    checks['sharp_S_quadratic_form']=sp.factor((w.T*G0*S0*w)[0]-ell*cw)==0
    positive={name:positive_rational(expr) for name,expr in [
       ('ell_plus1',ell+1),('minus_ell',-ell),('minus_v',-v),('v_minusell',v-ell),
       ('Q_leading',27*a*b),('minus_Q_constant',-Q.subs(z,0)),
       ('Q_at1',Q.subs(z,1)),('Q_atell',Q.subs(z,ell)),('sharp_C_form',cw)]}
    ratios={(-1,-1):(d*d-19*d+12)/(9*a*b),(-1,1):-(d*d-9*d+4)/(3*a*b),
            (1,-1):-(d*d-9*d+4)/(3*a*b),(1,1):(d*d+d-4)/(a*b)}
    for (ea,eb),ratio in ratios.items():
        C=(1-sp.Rational(ea,2))*(1-sp.Rational(eb,2))
        S=sp.Rational(ea+eb,4)/a+(d*d-9*d+4)*ea*eb/(4*a*b)
        checks[f'scalar_ratio_{ea}_{eb}']=sp.factor(S/C-ratio)==0
        positive[f'scalar_{ea}_{eb}_minusell']=positive_rational(ratio-ell)
        positive[f'one_minus_scalar_{ea}_{eb}']=positive_rational(1-ratio)
    assert all(checks.values())
    out={'status':'INDEPENDENT_EXACT_SHARP_UNIFORM_SPECTRAL_AUDIT_PASSED',
         'scope':'full uniform Schmidt rank d in exactly dxd pair, integer d>=3; no inactive/nonuniform extension',
         'producer_snapshot_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
         'sharp_lower_endpoint':str(ell),'checks':checks,'strict_positive_certificates':positive,
         'tensor_consequence':'Any finite disjoint collection of such d>=3 full uniform pairs and remaining product sites has normalized co-Choi spectrum in [-1,1], hence C_total-S_total>=0 and the restricted rank<=2 q_k consequence.',
         'proof_reason_for_Q_roots':'Positive leading coefficient and negative constant give one negative and one positive real root; Q(ell)>0 at ell<0 and Q(1)>0 put both roots strictly between ell and1.',
         'elapsed_code_seconds':time.perf_counter()-start}
    (root/'uniform_sharp_audit.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()
