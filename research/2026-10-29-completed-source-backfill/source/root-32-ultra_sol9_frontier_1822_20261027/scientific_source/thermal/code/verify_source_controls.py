"""Exact finite source controls, separate from the independent agent audit.

These check literal small source coefficients and analytic spin addition.
The all-size thermal conclusion is proved by the full moment/loop argument.
"""
import json
from fractions import Fraction as F
from acquire_cycle_moments import acquire,PRIOR,ROOT

def main():
    reference={r['twist']:list(map(int,r['trace_2H_powers']))for r in json.loads((PRIOR/'data/twisted4_moments_exact_degree192.json').read_text())['records']}
    controls=[]
    for kind in ['I','P']:
        record=acquire(4,kind,24);vals=list(map(int,record['trace_2H_powers']))
        if kind=='P':assert vals==reference['P'][:25]
        else:
            energies=[]
            for a in range(5):
                for b in range(5):
                    for j in range(abs(a-b),a+b+1):
                        energies.append((j*(j+1)-a*(a+1)-b*(b+1),2*j+1))
            assert vals==[sum(deg*e**k for e,deg in energies)for k in range(25)]
        controls.append({'cycle_sites':4,'twist':kind,'degree':24,'exact_moment_match':True})
    end={r['n']:list(map(int,r['trace_minus_SzSz_2H_powers']))for r in json.loads((ROOT/'results/end_spin_moments_exact_degree192.json').read_text())['chains']}
    for n in [2,3]:
        values=[]
        for k in range(193):
            value=F(0)
            if n==2:
                for j in range(5):
                    e=F(j*(j+1)-12,2);value-=F(2*j+1,3)*e*(2*e)**k
            else:
                for a in range(5):
                    endpoint=F(a*(a+1)-12,2)
                    for j in range(abs(a-2),a+3):
                        e=F(j*(j+1)-a*(a+1)-6,2)
                        value-=F(2*j+1,3)*endpoint*(2*e)**k
            assert value.denominator==1;values.append(int(value))
        assert values==end[n]
        controls.append({'end_spin_open_sites':n,'degree':192,'exact_analytic_spin_addition_match':True})
    (ROOT/'results/independent_source_controls.json').write_text(json.dumps({'status':'PASS','controls':controls},indent=2)+'\n')
    print('SOURCE CONTROLS PASS')

if __name__=='__main__':main()
