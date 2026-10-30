"""Exact cubic obstruction over the exposed angular quartic branch.

All new writes stay in this phase2 directory. Local SymPy only. This file
does not import or mutate the completed partner snapshot.
"""
from pathlib import Path
import json
import time
import sympy as s
from sympy.polys.matrices import DomainMatrix

HERE = Path(__file__).resolve().parent
a,b,c,d,t,x,y,tau = s.symbols('a b c d t x y tau')
av = (a,b,c,d)
powers = [(i,j,k,3-i-j-k) for i in range(4)
          for j in range(4-i) for k in range(4-i-j)]
monomials = [s.prod(z**e for z,e in zip(av,p)) for p in powers]


def construct():
    B,H = 1-3*tau*tau,1+3*tau*tau
    domain = s.QQ.frac_field(tau)
    m = s.Poly(B*B*(1-t*t)**2
               -(1-4*tau+3*tau*tau)*H*(1+t*t)**2,t,domain=domain).monic()
    K = s.Matrix([
        -B*(tau*(1-t*t)+H*t*t)*(1+t*t),
        B*t*(H-tau*(1-t*t))*(1+t*t),
        B*B*t*(1-t*t)-tau*H*t*(1+t*t)**2,
        B*B*t*t*(1-t*t)+tau*H*(1+t*t)**2,
    ]).applyfunc(lambda z:s.Poly(z,t,domain=domain).rem(m).as_expr())
    Ku = s.Matrix([x*K[0]-y*K[2],x*K[1]-y*K[3],
                   y*K[0]+x*K[2],y*K[1]+x*K[3]])
    substitution = dict(zip(av,(x,x*t,y,y*t)))
    columns = []
    for mon in monomials:
        p = sum(s.diff(mon,z).subs(substitution,simultaneous=True)*kk
                for z,kk in zip(av,Ku))
        pp = s.Poly(s.expand(p),x,y)
        column = []
        for ix in range(4):
            remainder = s.Poly(pp.coeff_monomial(x**ix*y**(3-ix)),t,domain=domain).rem(m)
            column.extend(remainder.nth(j) for j in range(4))
        columns.append(column)
    L = s.Matrix.hstack(*map(s.Matrix,columns))
    T = sum(z*z for z in av)
    q,X = a*d-b*c,a*a+c*c-b*b-d*d
    F = s.expand(T*T+4*(3-12*tau/H)*q*q+4*B/H*q*X)
    translations = s.Matrix([
        [s.Poly(s.diff(F,z),*av).coeff_monomial(mon) for z in av]
        for mon in monomials])
    assert all(s.cancel(z)==0 for z in L*translations)
    return L,translations,F,m,K


def open_roots(poly):
    pp = s.Poly(poly,tau).sqf_part()
    return (int(pp.count_roots(0,s.Rational(1,3)))
            -int(pp.eval(0)==0)-int(pp.eval(s.Rational(1,3))==0))


def exact_minor(L, columns):
    minor = L[:,columns]
    denominators = []
    for i in range(minor.rows):
        den = s.Poly(1,tau)
        for j in range(minor.cols):
            den = s.lcm(den,s.Poly(s.denom(s.cancel(minor[i,j])),tau))
        den = s.expand(den.as_expr())
        denominators.append(den)
        for j in range(minor.cols):
            minor[i,j] = s.cancel(minor[i,j]*den)
            assert s.denom(minor[i,j])==1
    value = DomainMatrix.from_Matrix(minor).convert_to(s.QQ.poly_ring(tau)).det().as_expr()
    value = s.factor(value)
    return {
        'columns':list(columns),
        'row_denominators':list(map(str,denominators)),
        'cleared_determinant':str(value),
        'factors':[{'polynomial':str(p),'multiplicity':int(n),
                    'open_interval_roots':open_roots(p)}
                   for p,n in s.factor_list(value,tau)[1]],
    }


def main():
    start = time.perf_counter()
    L,D,F,m,K = construct()
    seed_outputs = []
    for value in (s.Rational(1,30),s.Rational(1,6)):
        LL,DD = L.subs(tau,value),D.subs(tau,value)
        assert LL.rank()==16 and DD.rank()==4
        assert LL*DD==s.zeros(16,4)
        seed_outputs.append({'tau':str(value),'constraint_rank':16,
                             'cubic_nullity':4,'translation_rank':4})
        print('Seed exact cubic rigidity:',value,flush=True)
    _, columns = L.subs(tau,s.Rational(1,30)).rref()
    record = exact_minor(L,list(columns))
    assert all(item['open_interval_roots']==0 for item in record['factors'])
    assert all(open_roots(s.sympify(p,locals={'tau':tau}))==0
               for p in record['row_denominators'])
    expected = (62208*tau**10*(3*tau*tau-1)**32*(3*tau*tau+1)**8
                *(3*tau*tau-3*tau+1)**10*(3*tau*tau-2*tau+1)**4
                *(9*tau**4-18*tau**3+18*tau*tau-6*tau+1)**4)
    assert s.expand(s.sympify(record['cleared_determinant'],locals={'tau':tau})-expected)==0
    positive_quartic = 9*tau**4-18*tau**3+18*tau*tau-6*tau+1
    assert s.expand(positive_quartic-((3*tau*tau-3*tau+1)**2+3*tau*tau))==0
    translation_minor = s.factor(D[16:20,:].det())
    assert translation_minor == (12288*tau**2*(3*tau*tau-3*tau+1)**2
                                  /(3*tau*tau+1)**4)
    print('First generic minor:',record['cleared_determinant'],flush=True)
    out = {
        'monomial_powers':powers,
        'constraint_shape':[L.rows,L.cols],
        'constraint_entries':[list(map(str,row)) for row in L.tolist()],
        'translation_entries':[list(map(str,row)) for row in D.tolist()],
        'seed_results':seed_outputs,
        'first_minor':record,
        'translation_minor_rows':list(range(16,20)),
        'translation_minor_determinant':str(translation_minor),
        'rank_16_on_entire_open_branch':True,
        'translation_rank_4_on_entire_open_branch':True,
        'seconds':time.perf_counter()-start,
    }
    path = HERE/'cubic_rigidity_data.json'
    path.write_text(json.dumps(out,indent=2)+'\n')
    print('Saved',path,flush=True)


if __name__=='__main__':
    main()
