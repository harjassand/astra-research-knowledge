from fractions import Fraction
import json
count=0
for d in range(1,65):
 M=d+1; C=Fraction(1,2)+4*d; K=8*d*d+2*d+1
 assert K==M+2*d*C and K>=2*d
 for j in range(20):
  for z in range(500):
   N=j+max(0,Fraction(z,2*d)-C*j)
   assert M*j+z<=K*N
   count+=1
# Independent first-removal accounting: sum added <= eps*z/(2(1-eps));
# bad first-removed mass <= (1-3eps/2)/eps * sum added < z/2.
eps=Fraction(1,12)
bad_fraction=(1-Fraction(3,2)*eps)/(2*(1-eps))
assert bad_fraction<Fraction(1,2)
print(json.dumps({'scalar_cases':count,'all_passed':True,'bad_original_mass_fraction_upper_bound_at_eps_1_12':str(bad_fraction),'initial_good_move_gain_fraction_strictly_exceeds':str(1-3*eps)},indent=2))
