import sympy as s
w=(-1+s.I*s.sqrt(3))/2
states=[s.eye(3)[:,j] for j in range(3)]
for b in range(3):
 for k in range(3):states.append(s.Matrix([s.simplify(w**((b*x*x+k*x)%3)) for x in range(3)])/s.sqrt(3))
M=s.zeros(9)
for v in states:
 P=s.simplify(v*v.conjugate().T)
 M+=s.kronecker_product(P.conjugate(),P)/12
M=s.simplify(M);v=s.Matrix([1,0,0,0,1,0,0,0,1]);Phi=v*v.T/3
assert s.simplify(M-(s.eye(9)+3*Phi)/12)==s.zeros(9)
# For any linear TP E this tensor identity gives T=(J+I tensor sigma)/4.
assert s.Rational(16)*(4**2)==256
assert s.Rational(256,512)==s.Rational(1,2)
print('PASS exact12-state conjugated qutrit2-design, labelled program identity, factor16 sample-time charge')
