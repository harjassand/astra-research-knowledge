"""Exact crossing-pulse memory-only reorder with intervening correction projectors."""
import sympy as S
from itertools import product
I=S.eye(2);X=S.Matrix([[0,1],[1,0]]);Y=S.Matrix([[0,-S.I],[S.I,0]]);Z=S.diag(1,-1)
k=S.kronecker_product; Im=S.eye(4);Ib=S.eye(2)
c=S.Rational(99,101);s=S.Rational(20,101)
# A first, C first, A last, C last: disjoint memory, one noncommuting bath.
mem=[k(X,I),k(I,Y),k(Y,I),k(I,X)]
bath=[X,Y,Z,X]
reset=[S.diag(1,0),X*S.diag(0,1)]
checks=0
for j,h,ca,cc in product(range(2),repeat=4):
 KC=k(I,reset[j]);KA=k(reset[h],I)
 direct=S.zeros(8)
 for fa,fc in product(range(2),repeat=2):
  gates=[c*S.eye(8)-S.I*s*(-1)**([fa,fc,fa,fc][r])*k(mem[r],bath[r]) for r in range(4)]
  W=gates[3]*k(KA,Ib)*gates[2]*gates[1]*k(KC,Ib)*gates[0]
  direct+=(-1)**(ca*fa+cc*fc)*W/4
 reordered=S.zeros(8)
 for bits in product(range(2),repeat=4):
  if (bits[0]+bits[2])%2!=ca or (bits[1]+bits[3])%2!=cc:continue
  Ms=[mem[r] if bits[r] else Im for r in range(4)]
  Bs=[bath[r] if bits[r] else Ib for r in range(4)]
  EA=Ms[2]*Ms[0]; EC=Ms[3]*Ms[1]
  coefficient=c**(4-sum(bits))*(-S.I*s)**sum(bits)
  # Only memory factors are regrouped. Bath remains B3 B2 B1 B0.
  reordered+=coefficient*k(EC*KA*EA*KC,Bs[3]*Bs[2]*Bs[1]*Bs[0])
 assert direct==reordered
 # For every initial full syndrome, legal correction/representative history predicts output orbit.
 for a0,c0 in product(range(2),repeat=2):
  V=S.zeros(8,2);idx=2*a0+c0;V[2*idx,0]=1;V[2*idx+1,1]=1
  out=direct*V
  allowed=(j==c0 and h==(a0^ca))
  if not allowed: assert out==S.zeros(8,2)
  else:
   # After the A reset and C completion, memory is |0,cc>.
   for r in range(8):
    if r//2!=cc: assert out[r,:]==S.zeros(1,2)
  checks+=1
print('PASS: exact Fourier/reordered operator equality for all 16 correction/character records; '+str(checks)+' initial-syndrome orbit checks; chronological bath factors retained.')
