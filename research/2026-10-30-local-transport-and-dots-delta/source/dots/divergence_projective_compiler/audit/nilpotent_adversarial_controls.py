"""Independent symbolic controls for strong versus pointwise Jacobian nilpotence.
No producer code is imported. Outputs exact checks and explicit mixed witnesses.
"""
import hashlib,json
from pathlib import Path
import sympy as s
ROOT=Path(__file__).resolve().parents[1]
x,y,z,w=s.symbols('x y z w')

def zero(mat):
    return all(s.expand(v)==0 for v in mat)

def certify(N, xs, mixed_points):
    X=s.Matrix(xs); J=N.jacobian(xs)
    out={'variables':list(map(str,xs)), 'N':list(map(str,N)),
         'N_at_zero_is_zero':zero(N.subs(dict.fromkeys(xs,0))),
         'JN_at_zero_is_zero':zero(J.subs(dict.fromkeys(xs,0))),
         'pointwise_nilpotent':zero(J**len(xs)),
         'quasitranslation_JN_times_N_zero':zero(J*N)}
    product=s.eye(len(xs))
    for p in mixed_points: product=product*J.subs(dict(zip(xs,p)))
    out['mixed_points']=mixed_points
    out['mixed_product']=[[str(v) for v in row] for row in product.tolist()]
    out['strong_nilpotence_falsified']=not zero(product)
    return out

# Campbell 1999 Example 3 with phi(t)=t^2. Both inverse identities are checked.
N=s.Matrix([z*(x+z*y)**2,-(x+z*y)**2,0]); X=s.Matrix([x,y,z]);
quasi=certify(N,(x,y,z),[[1,0,0],[1,0,1],[1,0,0]])
F=X+N; G=X-N
quasi['F_after_G_identity']=zero(F.subs(dict(zip((x,y,z),G)),simultaneous=True)-X)
quasi['G_after_F_identity']=zero(G.subs(dict(zip((x,y,z),F)),simultaneous=True)-X)
assert all(quasi[k] for k in ['N_at_zero_is_zero','JN_at_zero_is_zero','pointwise_nilpotent','quasitranslation_JN_times_N_zero','strong_nilpotence_falsified','F_after_G_identity','G_after_F_identity'])

# Homogenization of Campbell Example 4, phi(t)=t, to homogeneous degree four.
N4=s.Matrix([y*w**3-x*x*w*w,z*w**3+2*x*y*w*w-2*x**3*w,-y*y*w*w+2*x*x*y*w-x**4,0])
pointwise=certify(N4,(x,y,z,w),[[0,0,0,1],[1,0,0,1],[0,0,0,1],[1,0,0,1]])
assert pointwise['pointwise_nilpotent'] and pointwise['strong_nilpotence_falsified']
assert pointwise['JN_at_zero_is_zero']

# Two tame shears: invertible normalized chart with Jacobian not even pointwise nilpotent.
X2=s.Matrix([x,y]); F2=s.Matrix([x+y*y,y+(x+y*y)**2]); G2=s.Matrix([x-(y-x*x)**2,y-x*x]); JN2=(F2-X2).jacobian((x,y))
shear={'F':list(map(str,F2)), 'G':list(map(str,G2)),
       'det_JF':str(s.factor(F2.jacobian((x,y)).det())),
       'trace_JN':str(s.factor(s.trace(JN2))),
       'pointwise_nilpotent':zero(JN2**2),
       'F_after_G_identity':zero(F2.subs(dict(zip((x,y),G2)),simultaneous=True)-X2),
       'G_after_F_identity':zero(G2.subs(dict(zip((x,y),F2)),simultaneous=True)-X2)}
assert not shear['pointwise_nilpotent'] and shear['F_after_G_identity'] and shear['G_after_F_identity']

# Exact output bit growth of the quadratic chain inverse at z=(0,...,0,2).
bitgrowth=[]
for n in [2,3,4,6,8,12,16]:
    values=[2]
    for _ in range(n-1): values.insert(0,-values[0]**2)
    degree=2**(n-1)
    assert abs(values[0]).bit_length()==degree+1
    bitgrowth.append({'n':n,'inverse_degree':degree,'first_coordinate_exact_output_bits':degree+1})

out={'quasitranslation_nonstrong':quasi,'pointwise_nonstrong_homogeneous':pointwise,
     'invertible_tame_nonstrong':shear,'exact_output_bitgrowth':bitgrowth,
     'source_script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
(ROOT/'audit'/'nilpotent_adversarial_controls.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
