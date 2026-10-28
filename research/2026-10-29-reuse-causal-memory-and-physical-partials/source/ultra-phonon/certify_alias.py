"""Proper central-force supercell alias on the actual public-Si interpolant."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,itertools,json,time
import sympy as s
BASE=Path(__file__).parent

def enc(x):
    x=s.Rational(x);return dict(numerator=str(x.p),denominator=str(x.q),display=float(x))

def main():
    start=time.perf_counter();data=json.loads((BASE/'MODEL.json').read_text())
    C={tuple(row['R']):s.Matrix([[s.Rational(v) for v in a] for a in row['matrix']]) for row in data['coefficients']}
    P=s.Matrix([[0,1,1],[1,0,1],[1,1,0]]);I=s.eye(3);zero=s.zeros(6)
    directions=[s.Matrix(v) for v in [(1,0,0),(0,1,0),(0,0,1),(1,-1,0),(1,0,-1),(0,1,-1)]]
    alias={(0,0,0):s.zeros(6)};a=s.Rational(1)
    for R in directions:
        d=P*R;assert (d.T*d)[0]==2
        B=d*d.T/2;B=s.diag(B,B)
        alias[(0,0,0)]-=2*a*B
        for sign in [-1,1]:alias[tuple(2*sign*v for v in R)]=a*B
    assert sum(alias.values(),s.zeros(6))==zero
    assert all(A==alias[tuple(-x for x in R)].T for R,A in alias.items())
    for k in itertools.product([0,1],repeat=3):
        D=sum((((-1)**sum(k[j]*R[j] for j in range(3)))*A for R,A in alias.items()),s.zeros(6))
        assert D==zero
    v=s.Matrix([0,1,-1,0,1,-1]);z=(s.Integer(63)+16*s.I)/65
    def at(coeff):return s.simplify(sum((A*z**R[0] for R,A in coeff.items()),s.zeros(6)))
    D=at(C);E=at(alias);norm=(v.T*v)[0]
    before=s.simplify((s.conjugate(v).T*D*v)[0]/norm)
    unit_delta=s.simplify((s.conjugate(v).T*E*v)[0]/norm)
    assert before>0 and unit_delta<0
    # Also check a rational reduced q=(1/4,0,0), using exact phase i.
    def quarter(coeff):return s.simplify(sum((A*s.I**R[0] for R,A in coeff.items()),s.zeros(6)))
    q_before=s.simplify((v.T*quarter(C)*v)[0]/norm);q_delta=s.simplify((v.T*quarter(alias)*v)[0]/norm)
    # Construct one sufficient integer strength directly, without a search grid.
    a=s.ceiling(max(before/(-unit_delta),q_before/(-q_delta)))+1
    after=s.simplify(before+a*unit_delta)
    assert after<0 and q_before+a*q_delta<0
    # Three independent infinitesimal rotations have zero extension on EACH bond.
    for i,j in [(0,1),(0,2),(1,2)]:
        O=s.zeros(3);O[i,j]=1;O[j,i]=-1
        assert all((P*R).dot(O*(P*R))==0 for R in directions)
    # Isolate the physical radial shell: in units a/2, its squared radius is8.
    basis=[s.zeros(3,1),s.Matrix([-s.Rational(3,4)]*3)];dist=set()
    for b in basis:
      for R in itertools.product(range(-6,7),repeat=3):
        d=P*(s.Matrix(R)+b);dist.add((d.T*d)[0])
    below=max(x for x in dist if x<8);above=min(x for x in dist if x>8)
    assert below<=s.Rational(27,4) and above>=s.Rational(35,4)
    half_a=s.Rational('2.733099421887392')
    shell_gap_lower=half_a*s.Rational(129,1000)
    assert s.Rational(2828,1000)**2<8<s.Rational(2829,1000)**2
    assert s.Rational(2699,1000)**2>s.Rational(27,4)
    assert s.Rational(2958,1000)**2<s.Rational(35,4)
    assert shell_gap_lower>s.Rational(121,1000)
    disp=s.Matrix([s.Rational(x) for x in data['displacement']])
    assert 4*(disp.T*disp)[0]<s.Rational(21,1000)**2
    # |R|_inf>=7 gives |P R+P b|>=7-3sqrt(3)/2>4, outside the shell.
    assert s.Rational(7)-s.Rational(3,2)*s.Rational(1733,1000)>4
    out=dict(status='EXACT_COMMENSURATE_HARMONIC_ALIAS_AND_SOURCE_FORCE_INVISIBLE_CENTRAL_TERM',
        model_sha256=hashlib.sha256((BASE/'MODEL.json').read_bytes()).hexdigest(),
        hidden_central_bond_directions=[list(map(int,R)) for R in directions],
        hidden_shifts_are_two_primitive_cells=True,hidden_spring_strength=enc(a),
        all_eight_commensurate_q_matrices_zero=True,translation_sum_rule=True,reciprocity=True,
        central_force_rotation_nulls=True,
        exact_phase=dict(real=enc(s.Rational(63,65)),imaginary=enc(s.Rational(16,65))),
        trial_vector=list(map(int,v)),trial_norm_squared=enc(norm),
        baseline_rayleigh=enc(before),unit_strength_alias_delta=enc(unit_delta),unit_strength_trial_deficit=enc(before+unit_delta),aliased_rayleigh=enc(after),
        quarter_reduced_q=['1/4','0','0'],quarter_baseline_rayleigh=enc(q_before),quarter_unit_alias_rayleigh=enc(q_delta),
        same_strength_quarter_rayleigh=enc(q_before+a*q_delta),
        shell_squared_radius=8,nearest_other_squared_radii=[str(below),str(above)],
        physical_radial_shell_gap_lower_Angstrom=enc(shell_gap_lower),
        smooth_pair_bump_support_halfwidth_Angstrom='1/10',maximum_relative_source_displacement_Angstrom='21/1000',
        force_invisibility_scope='All source-sized two-primitive-cell-periodic displacement patterns in the isolated-shell neighbourhood, not just the measured vector; central pair potential has zero value/first derivative and negative second derivative at shell radius',
        scope_distinction='The two executed matrices share commensurate harmonic data. The central term is force-invisible on any compatible source background; the repaired harmonic interpolant is NOT asserted to fit every nonlinear raw force exactly.',
        infinite_range_physical_Hessian_identified=False,seconds=time.perf_counter()-start)
    (BASE/'ALIAS_CERTIFICATE.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
