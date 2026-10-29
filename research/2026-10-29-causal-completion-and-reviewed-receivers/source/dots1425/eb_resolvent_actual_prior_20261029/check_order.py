import sympy as s,json
E=s.Matrix([[s.Rational(1,2),s.Rational(3,4)],[0,0]]);R=s.Matrix([[0,0],[s.Rational(1,2),s.Rational(1,4)]]);L=(s.eye(2)-R).inv()*E;F=E*(s.eye(2)-R).inv();assert L==s.Matrix([[s.Rational(1,2),s.Rational(3,4)],[s.Rational(1,3),s.Rational(1,2)]]);assert F==s.Matrix([[1,1],[0,0]])
out={'left_column_sums':[str(sum(L[:,j])) for j in range(2)],'right_column_sums':[str(sum(F[:,j])) for j in range(2)],'exact_symbolic_checks':'pass'};print(out);open('ORDER_CHECKS.json','w').write(json.dumps(out,indent=2)+'\n')
