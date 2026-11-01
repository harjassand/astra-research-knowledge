#!/usr/bin/env python3
"""Independent rational-endpoint replay; does not import constructor code.

The recurrence is the formal identity 2*(s+3e^2/4)^2*s'=1,
implemented via the reciprocal series. All proof decisions use int/Fraction.
The interval implementation stores Fraction endpoints (not constructor ticks),
and independently rounds products and reciprocals outward to the dyadic grid.
"""
import argparse
import ast
from fractions import Fraction as R
import hashlib
import json
from pathlib import Path
import sys

BITS = 120
D = 1 << BITS
count = dict(add=0, mul=0, div=0)

def floor_grid(x):
    y = R(x) * D
    return R(y.numerator // y.denominator, D)

def ceil_grid(x):
    return -floor_grid(-R(x))

class Box:
    def __init__(self, lower, upper=None):
        self.lower = floor_grid(lower)
        self.upper = ceil_grid(lower if upper is None else upper)
        assert self.lower <= self.upper
    def __add__(self, other):
        other = other if isinstance(other, Box) else Box(other)
        count['add'] += 1
        return Box(self.lower + other.lower, self.upper + other.upper)
    __radd__ = __add__
    def __neg__(self):
        return Box(-self.upper, -self.lower)
    def __mul__(self, other):
        other = other if isinstance(other, Box) else Box(other)
        count['mul'] += 1
        extrema = [x*y for x in (self.lower,self.upper) for y in (other.lower,other.upper)]
        return Box(min(extrema), max(extrema))
    __rmul__ = __mul__
    def inv(self):
        count['div'] += 1
        assert self.lower > 0 or self.upper < 0
        if self.upper < 0:
            return -((-self).inv())
        return Box(1/self.upper, 1/self.lower)
    def __truediv__(self, other):
        other = other if isinstance(other, Box) else Box(other)
        return self * other.inv()
    def power(self, n):
        z = Box(1)
        for _ in range(n):
            z = z*self
        return z
    def contains(self, x):
        return self.lower <= x <= self.upper

def product(a,b):
    out = {}
    for i,x in a.items():
        for j,y in b.items():
            out[i+j] = out.get(i+j,R(0)) + x*y
    return {i:x for i,x in out.items() if x}

def evaluate(poly,x):
    return sum((c*x**i for i,c in poly.items()),R(0))

def initial(degree):
    poly = {}
    for n in range(degree):
        square = product(poly,poly)
        fourth = product(square,square)
        c = (R(2) if n == 2 else R(0)) + 3*square.get(n-1,R(0)) + R(9,8)*fourth.get(n,R(0))
        if c:
            poly[n+1] = c/(n+1)
    square = product(poly,poly)
    fourth = product(square,square)
    residual = {2:R(2)}
    for i,c in square.items():
        residual[i+1] = residual.get(i+1,R(0)) + 3*c
    for i,c in fourth.items():
        residual[i] = residual.get(i,R(0)) + R(9,8)*c
    for i,c in poly.items():
        residual[i-1] = residual.get(i-1,R(0)) - i*c
    assert all(c >= 0 for c in poly.values())
    assert all(c >= 0 for c in residual.values())
    assert all(residual.get(i,R(0)) == 0 for i in range(degree))
    t = R(1,2)
    L = R(105,128)
    residual_max = evaluate(residual,t)
    delta = residual_max/(1-L*t)
    lower = evaluate(poly,t)
    upper = lower+t*delta
    assert upper < R(1,4)
    a = ceil_grid(upper)
    result = Box(t,t+(a-lower)/(2*t*t))
    fields = {'polynomial_degree':degree,'s0':str(t),'forward_e_lower':str(lower),
        'forward_e_upper':str(upper),'residual_max':str(residual_max),
        'linear_barrier_delta':str(delta),'lipschitz':str(L),
        'inverse_e_start':str(a),'inverse_s_lower':str(result.lower),
        'inverse_s_upper':str(result.upper),'startup_time_width':str(result.upper-result.lower),
        'residual_coefficients_nonnegative':True,'matched_coefficients_zero':True}
    return a,result,fields

def series(u,z,N):
    state = [z]
    denominator = []
    reciprocal = []
    coord_square = [u*u,2*u,Box(1)]
    for k in range(N):
        d = state[k] + (R(3,4)*coord_square[k] if k<3 else 0)
        denominator.append(d)
        if k == 0:
            reciprocal.append(d.inv())
        else:
            c = Box(0)
            for j in range(1,k+1):
                c = c + denominator[j]*reciprocal[k-j]
            reciprocal.append((-reciprocal[0])*c)
        c = Box(0)
        for j in range(k+1):
            c = c + reciprocal[j]*reciprocal[k-j]
        state.append(c/R(2*(k+1)))
    return state

def arithmetic_tests():
    examples = [R(-7,3),R(-1,7),R(0),R(1,11),R(3,2),R(123456789,100)]
    for x in examples:
        for y in examples:
            a,b = Box(x),Box(y)
            assert (a+b).contains(x+y)
            assert (a*b).contains(x*y)
            if y:
                assert (a/b).contains(x/y)
    x,y = R(2,3),R(5,4)
    w = y+R(3,4)*x*x
    v = 1/(2*w*w)+R(3,2)*x
    c = series(Box(x),Box(y),3)
    assert c[1].contains(1/(2*w*w))
    assert c[2].contains(-v/(2*w**3))
    assert c[3].contains((3*v*v/w**4+v/w**6-R(3,2)/w**3)/6)

def advance(x,h,previous,N):
    midpoint_ticks = ((previous.lower+previous.upper)*D).numerator//2
    # Endpoints are grid points, so denominator in the sum above is one.
    assert ((previous.lower+previous.upper)*D).denominator == 1
    midpoint = R(midpoint_ticks,D)
    radius = max(midpoint-previous.lower,previous.upper-midpoint)
    hh = Box(h)
    c = series(Box(x),Box(midpoint),N)
    polynomial = c[-1]
    for coefficient in c[-2::-1]:
        polynomial = polynomial*hh+coefficient
    tube = Box(midpoint,(Box(midpoint)+hh*c[1]).upper)
    cnext = series(Box(x,x+h),tube,N+1)[-1]
    local = polynomial+cnext*hh.power(N+1)
    answer = Box(local.lower-radius,local.upper+radius)
    assert answer.lower > 0
    return answer,local.upper-local.lower,2*radius-(previous.upper-previous.lower)

def decimal(x,digits,up):
    scaled = R(x)*10**digits
    n = -( (-scaled.numerator)//scaled.denominator ) if up else scaled.numerator//scaled.denominator
    return '{}.{:0{}d}'.format(n//(10**digits),n%(10**digits),digits)

def compute(N,p,E,degree):
    count.update(add=0,mul=0,div=0)
    arithmetic_tests()
    count.update(add=0,mul=0,div=0)  # Solver counts exclude arithmetic tests.
    a,state,startup = initial(degree)
    initial_width = state.upper-state.lower
    steps = 0
    local_width = R(0)
    centering_width = R(0)
    checkpoints = []
    while a<E:
        annulus = 1
        while 2*annulus <= a:
            annulus *= 2
        h = min(R(annulus,2**p),E-a)
        state,lw,cw = advance(a,h,state,N)
        local_width += lw
        centering_width += cw
        a += h
        steps += 1
        if steps%64 == 0 or a == E:
            checkpoints.append({'step':steps,'e':str(a),'s_lower':str(state.lower),
              's_upper':str(state.upper),'width':str(state.upper-state.lower)})
    if N >= 3:
        assert count == {'add': steps*(2*N*N+5*N+4),
                         'mul': steps*(2*N*N+8*N+14),
                         'div': steps*(2*N+3)}
    lo,hi = state.lower,state.upper
    leading = R(8,27)/E**3
    U = hi+leading
    assert 0<lo<=hi<U<2
    baseline = max(R(0),leading-R(128,135)/E**5)
    tail_lo = leading-R(64,135)*U/E**5
    tail_hi = leading-R(64,135)*lo/E**5+R(128,189)*lo**2/E**7
    assert 0<tail_lo<=tail_hi<=leading
    lower,upper = lo+tail_lo,hi+tail_hi
    assert hi-lo == initial_width+local_width+centering_width
    return {
        'bits':BITS,'taylor_order':N,'grid_power':p,'terminal_e':str(E),'steps':steps,
        'startup':startup,'s_at_E_lower':str(lo),'s_at_E_upper':str(hi),
        'startup_width':str(initial_width),
        'inverse_taylor_and_rounding_width':str(hi-lo-initial_width),
        'sum_local_interval_widths':str(local_width),
        'tail_basic_upper':str(leading),'tail_baseline_lower_using_s_le_2':str(baseline),
        'tail_refined_lower':str(tail_lo),'tail_refined_upper':str(tail_hi),
        'tail_width':str(tail_hi-tail_lo),'s_star_lower':str(lower),'s_star_upper':str(upper),
        's_star_decimal_outward':[decimal(lower,18,False),decimal(upper,18,True)],
        'total_width':str(upper-lower),'total_width_decimal_upper':decimal(upper-lower,24,True),
        'checkpoints':checkpoints,'integer_interval_operations':count.copy(),
        'arithmetic_selftest_pass':True,
    },{'midpoint_padding_ticks':str(centering_width*D),'inverse_global_U_lt_2':True,
       'all_proof_arithmetic_exact':True}

def no_float_literal_code(path):
    tree=ast.parse(path.read_text())
    assert not any(isinstance(n,ast.Constant) and isinstance(n.value,float) for n in ast.walk(tree))
    return True

def check(cert_path,source_path=None):
    data = json.loads(cert_path.read_text())
    generated,extra = compute(data['taylor_order'],data['grid_power'],R(data['terminal_e']),data['startup']['polynomial_degree'])
    for field,expected in generated.items():
        assert data.get(field) == expected, 'field mismatch: '+field
    if source_path:
        assert data['code_sha256'] == hashlib.sha256(source_path.read_bytes()).hexdigest()
        no_float_literal_code(source_path)
    # Timing metadata is not accepted as a proof field. Report it explicitly if present.
    floating_paths=[]
    def visit(v,path):
        if isinstance(v,float): floating_paths.append(path)
        elif isinstance(v,list):
            for i,y in enumerate(v): visit(y,path+'/'+str(i))
        elif isinstance(v,dict):
            for k,y in v.items(): visit(y,path+'/'+k)
    visit(data,'')
    assert not floating_paths, 'float-valued fields in certificate: '+str(floating_paths)
    extra.update(status='PASS',certificate=str(cert_path),fields_exactly_replayed=len(generated),
       s_star_decimal_outward=generated['s_star_decimal_outward'],
       total_width_decimal_upper=generated['total_width_decimal_upper'],
       integer_interval_operations=generated['integer_interval_operations'],
       checkpoint_count=len(generated['checkpoints']))
    return extra

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('certificate',type=Path)
    ap.add_argument('--source',type=Path)
    ap.add_argument('--output',type=Path)
    a=ap.parse_args()
    result=check(a.certificate,a.source)
    text=json.dumps(result,indent=2)+'\n'
    if a.output: a.output.write_text(text)
    print(text,end='')

if __name__ == '__main__': main()
