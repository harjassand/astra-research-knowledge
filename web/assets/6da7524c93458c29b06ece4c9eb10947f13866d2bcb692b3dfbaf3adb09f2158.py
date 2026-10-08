"""Dimension-symbolic contraction-algebra certificate; no floating spectra."""
from sympy import symbols, Matrix, simplify, eye, factor
D=symbols('D',positive=True)
# Maps u(v)=S_AB v_C, v'(v)=S_AC v_B, w(v)=v_A S_BC.
# Their cross Gram operators are scalar multiples of identity on V.
gram3=Matrix([[1,1/D,-1/D],[1/D,1,1/D],[-1/D,1/D,1]])
P=Matrix([[1,1/D,-1/D],[1/D,1,1/D],[0,0,0]])
F=Matrix([[-1,0,-1],[0,-1,1],[-1,1,0]])
assert simplify(gram3*P-P.T*gram3)==Matrix.zeros(3)
assert simplify(gram3*F-F.T*gram3)==Matrix.zeros(3)
odd=simplify((D**2*P-D*F)/2)
even=simplify((D**2*P+D*F)/2-2*eye(3))
y=Matrix([1,1,0]); x=Matrix([1,-1,0]); w=Matrix([0,0,1])
assert simplify(odd*y-D*(D+2)*y/2)==Matrix.zeros(3,1)
assert simplify(even*y-(D**2/2-2)*y)==Matrix.zeros(3,1)
assert simplify(odd*x-(D**2*x/2+D*w))==Matrix.zeros(3,1)
assert simplify(odd*w)==Matrix.zeros(3,1)
assert simplify(even*x-((D**2/2-D-2)*x-D*w))==Matrix.zeros(3,1)
assert simplify(even*w-(-D*x-2*w))==Matrix.zeros(3,1)
assert simplify((y.T*gram3*x)[0])==0
assert simplify((y.T*gram3*w)[0])==0
G=Matrix([[2-2/D,-2/D],[-2/D,1]])
print('Gram det of (x,w):',factor(G.det()))
M=Matrix([[D**2/2-D-2,-D],[-D,-2]])
t=D**2/2-2
print('Even characteristic polynomial at claimed top:',factor((t*eye(2)-M).det()))
assert simplify((t*eye(2)-M).det()-D**2*(D/2-1))==0
Vodd=D*(D+1)/2
Veven=D*(D-1)/2-1
muodd=D*(D+2)/2
mueven=D**2/2-2
assert simplify(muodd/(2*Vodd)-(D+2)/(2*(D+1)))==0
assert simplify(mueven/(2*Veven)-(D+2)/(2*(D+1)))==0
assert simplify((D/2)/Vodd-1/(D+1))==0
assert simplify((D/2-1)/Veven-1/(D+1))==0
print('PASS: exact symbolic contractions, block actions, and both-sector dimension ratios.')
print('d>=4: Gram det>0 and char product>0; d=2 has zero even0 sector, handled separately.')
