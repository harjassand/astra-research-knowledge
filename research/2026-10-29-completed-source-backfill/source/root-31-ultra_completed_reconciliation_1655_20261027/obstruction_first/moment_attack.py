"""Optimal square-polynomial diagnostic for the finite initialization.

Uses every available moment M4,...,M8 in a Christoffel/Gram polynomial filter.
All spectral inputs in this script are numerical, not rigorous enclosures.
The optional dominant eigenvalue >=1 and trial normalization are optimistic
premises deliberately favorable to the attempted bootstrap, not acquired facts.
"""
import pathlib,sys,json,math
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[2]/'sol6_openings_20261027/positive_current_operation/vendor'))
import mpmath as mp
import numpy as np
mp.mp.dps=70
ROOT=pathlib.Path(__file__).resolve().parent


def partition(data,beta,shift):
    # The spectral inputs are double-precision diagnostics already. Long-double
    # summation avoids adding a much larger summation error; it does not make
    # the eigenvalues exact, nor does it turn this into a trace enclosure.
    total=np.longdouble(0)
    for r in data['sectors']:
        e=np.asarray(r['values'],dtype=np.longdouble)
        total+=r['multiplicity']*np.sum(np.exp(-np.longdouble(str(beta))*(e+np.longdouble(str(shift))*data['n'])),dtype=np.longdouble)
    return mp.mpf(str(total))


def filter_cap(moments):
    # F(x)=x^4*(a+b*x+c*x^2)^2. For z=(x²,x³,x⁴), the maximal
    # F(x)/sum_i F(lambda_i) over coefficients is z^T M^-1 z.
    # Every actual eigenvalue therefore lies where this kernel is <=1.
    gram=mp.matrix([[moments[i+j]for j in range(2,5)]for i in range(2,5)])
    inv=gram**-1
    def kernel(x):
        z=mp.matrix([x*x,x**3,x**4]);return (z.T*inv*z)[0]
    bound=moments[8]**mp.mpf('0.125')*mp.mpf('1.001')
    caps=[]
    for sign in [-1,1]:
        last=None;last_x=None
        for i in range(1000,-1,-1):
            x=bound*i/1000
            if kernel(sign*x)<=1:last_x=x;break
            last=x
        if last_x is None:raise ArithmeticError('no admissible point')
        lo,hi=last_x,last or bound
        for _ in range(150):
            mid=(lo+hi)/2
            if kernel(sign*mid)<=1:lo=mid
            else:hi=mid
        caps.append(hi)
    return max(caps),caps,gram,inv


def capped(m,h,r):
    if m<=0:return mp.mpf(0)
    q=mp.floor(m/h);return q*h**r+(m-q*h)**r


def iterate(p,q,steps=30):
    def f(x):return x*x/(2*(1-x)**2)
    history=[]
    for j in range(steps):
        if not(0<=p<1 and 0<=q<1):return False,history
        if max(p,q)<mp.mpf('1e-8'):return True,history
        argument=1-(1-p)**2*(1-q)
        if argument>=1:return False,history
        p=f(argument)
        if p>=1:return False,history
        argument=1-(1-q)**2*(1-p)
        if argument>=1:return False,history
        q=f(argument);history.append((float(p),float(q)))
    return False,history


def attack(shift='4.76124816', output=None):
    shift=mp.mpf(shift);data={}
    for n in range(4,9):
        for p in range(2):
            j=json.loads((ROOT/f'data/spin2_n{n}_p{p}.json').read_text())
            assert 'seconds' in j and all(r['full'] for r in j['sectors'])
            data[n,p]=j
    rows=[]
    for beta in [2,3,4,5,6,8,10,12,16,20,24,32,40,50]:
        beta=mp.mpf(beta);z={};J={};N={}
        for n in range(4,9):
            z[n]=[partition(data[n,p],beta,shift)for p in range(2)]
            J[n]=(z[n][0]+3*z[n][1])/4;N[n]=(z[n][0]-z[n][1])/4
        uj,cj,gj,ij=filter_cap(J);un,cn,gn,inn=filter_cap(N)
        best=None;passing=[]
        for n in range(8,2049,8):
            r=mp.mpf(n)/8
            # Grant one J eigenvalue of modulus >=1, and normalization
            # Z_(2n)(beta)>1. These are not derived from the numerical table.
            def remainder(k):return capped(J[8]-1,uj**8,mp.mpf(k)/8)+3*capped(N[8],un**8,mp.mpf(k)/8)
            R=remainder(n);zupper=uj**(2*n)+remainder(2*n)
            p=1-(1+R)**-2;q=1-zupper**-2
            passes,history=iterate(p,q)
            score=max(p,q)
            if best is None or score<best[0]:best=(score,n,p,q)
            if passes:passing.append(n)
        row={'beta':float(beta),'shift':str(shift),'moments':{str(n):{'Z':str(z[n][0]),'Z_P':str(z[n][1]),'J':str(J[n]),'N':str(N[n])}for n in range(4,9)},'J_cap':str(uj),'N_cap':str(un),'J_signed_caps':list(map(str,cj)),'N_signed_caps':list(map(str,cn)),'J_m8':str(J[8]),'N_m8':str(N[8]),'best_granted_seed':{'n':best[1],'p_upper':str(best[2]),'q_upper':str(best[3])},'passing_n':passing}
        rows.append(row);print('beta',float(beta),'caps',mp.nstr(uj,8),mp.nstr(un,8),'m8',mp.nstr(J[8],8),mp.nstr(N[8],8),'best',best[1],mp.nstr(best[2],7),mp.nstr(best[3],7),'PASS',passing[:3],flush=True)
    result={'status':'NUMERICAL_OPTIMISTIC_FILTER_FAMILY_DIAGNOSTIC_NO_GAP_PROOF','rows':rows}
    pathlib.Path(output or ROOT/'data/moment_attack.json').write_text(json.dumps(result,indent=2));return result


if __name__=='__main__':attack()
