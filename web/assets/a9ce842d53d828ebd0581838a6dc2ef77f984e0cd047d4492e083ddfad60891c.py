"""Independent exact audit fixtures. No imports or writes from peer scripts."""
import json
import time
from pathlib import Path
import sympy as s

t0 = time.perf_counter()
checks = {}

def geometry(entries, velocity):
    c = s.MutableDenseNDimArray.zeros(3, 3, 3)
    for i, j, k, value in entries:
        c[i,j,k], c[j,i,k] = value, -value
    ga = s.MutableDenseNDimArray.zeros(3, 3, 3)
    for i in range(3):
        for j in range(3):
            for k in range(3):
                ga[i,j,k] = (c[i,j,k]-c[j,k,i]+c[k,i,j])/2
    grad = s.Matrix(3, 3, lambda k,i: s.simplify(velocity*ga[i,0,k]))
    strain = s.simplify((grad+grad.T)/2)
    div = s.Matrix(3, 1, lambda k,j: s.simplify(sum(
        ga[i,l,k]*strain[l,i]-strain[k,l]*ga[i,i,l]
        for i in range(3) for l in range(3))))
    ric = s.Matrix(3,3,lambda j,k: s.simplify(sum(
        ga[j,k,l]*ga[i,l,i]-ga[i,k,l]*ga[j,l,i]-c[i,j,l]*ga[l,k,i]
        for i in range(3) for l in range(3))))
    return grad, strain, div, ric

a,b,v,nu = s.symbols('a b v nu', real=True)
g,S,div,Ric = geometry([(0,1,1,-a),(0,2,2,a),(1,2,0,b)],v)
checks['sl2_gradient'] = s.simplify(g-s.Matrix([[0,0,0],[0,a*v,b*v/2],[0,-b*v/2,-a*v]])) == s.zeros(3)
checks['sl2_strain'] = S == s.diag(0,a*v,-a*v)
checks['sl2_stress_divergence'] = div == s.Matrix([-2*a*a*v,0,0])
checks['sl2_scalar_curvature'] = s.simplify(s.trace(Ric)+2*a*a+b*b/2) == 0
checks['sl2_power'] = s.simplify(-2*nu*div[0]*v-4*nu*a*a*v*v) == 0

k = s.symbols('k', positive=True)
T = s.Matrix([[1,0,0],[0,1/s.sqrt(1+k*k),1/s.sqrt(1+k*k)],[0,k/s.sqrt(1+k*k),-k/s.sqrt(1+k*k)]])
gram = s.simplify(T.T*T)
checks['sasaki_proposed_inner_product'] = s.simplify(gram[1,2]-(1-k*k)/(1+k*k)) == 0
checks['sasaki_k2_is_not_orthogonal'] = gram.subs(k,2)[1,2] == -s.Rational(3,5)
gs,Ss,ds,rs = geometry([(0,1,2,-k*k),(0,2,1,-1),(1,2,0,1)],s.S.One)
checks['sasaki_actual_strain'] = Ss == s.Matrix([[0,0,0],[0,0,(1+k*k)/2],[0,(1+k*k)/2,0]])
checks['sasaki_actual_strain_norm'] = s.simplify(s.trace(Ss.T*Ss)-(1+k*k)**2/2) == 0
checks['sasaki_actual_force'] = s.simplify(-2*nu*ds[0]-nu*(1+k*k)**2) == 0
checks['sasaki_entropy_power_residual'] = s.simplify(-2*nu*ds[0]-4*nu*k*k-nu*(k*k-1)**2) == 0
checks['sasaki_k2_claim_refuted'] = s.simplify(-2*ds[0]).subs(k,2) == 25
checks['sasaki_k1_equality_retained'] = s.simplify(-2*ds[0]-4*k*k).subs(k,1) == 0

n = s.symbols('n', positive=True)
frame = s.diag(-1/(2*n),1,-n/2)
checks['l07_revision03_fixed_volume'] = s.simplify(frame.det()-s.Rational(1,4)) == 0
checks['l07_revision03_fixed_generator'] = frame[:,0]*n == s.Matrix([-s.Rational(1,2),0,0])
checks['l07_revision03_exact_equality'] = s.simplify((-2*nu*div[0]*v).subs({a:1/n,b:n*n,v:n})-4*nu) == 0
checks['l07_revision03_scalar'] = s.simplify(s.trace(Ric).subs({a:1/n,b:n*n})+2/n**2+n**4/2) == 0

d = s.sqrt(n*n-1)
A = s.Matrix([[n,1],[n*n-1,n]])
P = s.Matrix([[1,1],[d,-d]])/n
checks['l04_monodromy_determinant'] = A.det() == 1
checks['l04_monodromy_diagonalization'] = s.simplify(A*P-P*s.diag(n+d,n-d)) == s.zeros(2)
checks['l04_lattice_covolume'] = s.simplify(2*d/n**2/(-P.det())) == 1
short = P.inv()*s.Matrix([0,1])
checks['l04_short_loop_squared'] = s.simplify((2*d/n**2)*(short.dot(short))-1/d) == 0

out = {'status':'PASS' if all(checks.values()) else 'FAIL',
       'checks':checks,'sasaki_proposed_gram':str(gram),
       'sasaki_actual_strain':str(Ss),'sasaki_actual_divergence':str(ds),
       'runtime_seconds':time.perf_counter()-t0,'sympy_version':s.__version__,
       'scope':'Exact algebra/transcription fixtures only; analytic entropy, global quotient, physical force implementation, novelty, and finite-bit acquisition are not certified.'}
Path(__file__).with_name('claim_checks.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
assert all(checks.values())
