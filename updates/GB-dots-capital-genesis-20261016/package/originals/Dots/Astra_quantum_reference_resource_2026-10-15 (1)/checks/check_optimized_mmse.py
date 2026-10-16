import sympy as s,json
from pathlib import Path
q=s.Rational;I=s.eye(2);floor=q(1,100000)
factors=[[(135,694),(0,0),(631,-437)],[(0,0),(684,176),(473,-603)]]
states=[]
for factors_sign in factors:
 bs=[s.Matrix(v)*s.Matrix(v).T for v in factors_sign];tr=sum(s.trace(b) for b in bs)
 blocks=[(1-6*floor)*b/tr+floor*I for b in bs]
 assert sum(s.trace(b) for b in blocks)==1
 assert all(b[0,0]>0 and b.det()>0 and b==b.T for b in blocks)
 states.append(blocks)
E=s.Matrix([[q(149,500),q(1,1000),q(1,1000)],[q(1,1000),q(149,500),q(1,1000)],[q(1,1000),q(1,1000),q(149,500)],[q(7,10)]*3])
F=s.Matrix([[q(199,300),q(101,600),q(101,600)],[q(101,600),q(199,300),q(101,600)],[q(101,600),q(101,600),q(199,300)]])
record=json.loads(Path(__file__).with_name('optimized_binary_mmse_certificate.json').read_text())
def test(M,key):
 means=0;seconds=0;gain=0;fourth=0
 for j in range(M.rows):
  P=sum((M[j,k]*states[0][k] for k in range(3)),s.zeros(2));Q=sum((M[j,k]*states[1][k] for k in range(3)),s.zeros(2));A=(P+Q)/2;K=(P-Q)/2
  op= s.kronecker_product(I,A)+s.kronecker_product(A,I)
  rhs=s.Matrix([2*K[0,0],2*K[1,0],2*K[0,1],2*K[1,1]])
  v=op.inv()*rhs;O=s.Matrix([[v[0],v[2]],[v[1],v[3]]])
  assert O==O.T and A*O+O*A==2*K
  assert O==s.sympify(record[key][j]['observable_matrix'],locals={'Matrix':s.Matrix})
  assert all((I+sgn*O)[0,0]>0 and (I+sgn*O).det()>0 for sgn in [-1,1])
  # Direct first and second moments of squared loss for spectral O measurement.
  means+=s.trace(P*(I-O)**2+Q*(-I-O)**2)/2
  seconds+=s.trace(P*(I-O)**4+Q*(-I-O)**4)/2
  gain+=s.trace(K*O);fourth+=s.trace(A*O**4)
 mean=s.factor(means);variance=s.factor(seconds-means**2)
 assert mean==1-gain and s.factor(variance-(4*gain-gain**2-3*fourth))==0
 return mean,variance
ME,VE=test(E,'source_conditional_observables');MF,VF=test(F,'target_conditional_observables')
delta=s.factor(ME-MF);assert delta>0
assert ME==s.Rational(record['source_optimal_MSE']) and MF==s.Rational(record['target_optimal_MSE'])
assert VE==s.Rational(record['source_single_shot_loss_variance']) and VF==s.Rational(record['target_single_shot_loss_variance'])
den=2*(VE+VF)+q(16,3)*delta;n=int(s.ceiling(3*den/delta**2));assert n==144811
assert n*delta**2>=3*den
out={'pass':True,'source_MSE':float(ME),'target_MSE':float(MF),'target_advantage':float(delta),'variance_sum':float(VE+VF),'trials_per_device':n,'Bernstein_exponent_at_least_3':True,'probability_bound':'exp(-3) < 0.05','assumptions':'Independent IID trials and label draws for the two fixed calibrated device/receiver protocols; no receiver learning or calibration cost included.'}
assert json.loads(Path(__file__).with_name('optimized_mmse_check.json').read_text()) == out, 'Exact MMSE fixture mismatch';print(out)
