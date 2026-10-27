"""Actual full three-label affine balancing fails; reproducible 60-digit witness."""
from three_star_high_precision_value import *
p=m.mpf(1)/6;d=p/3
x=[m.mpf(49)/60,m.mpf(1)/120,m.mpf(1)/120]
c=[m.mpf(3)/40,m.mpf(1)/560,m.mpf(1)/560]
xb=[(1-p)/3]*3;cb=[sum(c)/3]*3
assert all(d*x[i]>c[i]**2 for i in range(3))
a=value(p,x,c);b=value(p,xb,cb)
print('actual:',m.nstr(a,55));print('balanced:',m.nstr(b,55));print('gap:',m.nstr(a-b,55));assert a-b < -m.mpf('.0001497')
def ell(a,b):return m.log(a/b)/(a-b) if a!=b else 1/a
def k(t):return ell(d,t)+ell(p,t/3)/3-2*ell(d,t/3)/3
ratio=k(xb[0])*sum(1/k(t) for t in x)/3
print('necessary Hessian ratio:',m.nstr(ratio,45));assert ratio>m.mpf('1.253')
# Independent full original TP source replay, not merely dual Gram spectra.
exec(open('three_block_pure_success_overlap_probe.py').read().split('for case')[0])
pf=float(p);xf=np.array(list(map(float,x)));cf=np.array(list(map(float,c)))
w=xf/(1-pf);r=cf**2/(pf*xf/3)
rb=float(cb[0]**2/(d*xb[0]))
va=val(pf,w,r);vb=val(pf,np.ones(3)/3,np.ones(3)*rb)
assert abs(va-float(a))<1e-12 and abs(vb-float(b))<1e-12
print('full original source replay PASS:',va,vb)
