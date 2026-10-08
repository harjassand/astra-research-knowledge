from pathlib import Path
import json
import mpmath as mp
mp.mp.dps=80
rows=[]
for aa in (1,4,16,64):
    a=mp.mpf(aa); q=mp.pi/a; lam=mp.mpf(1)/4+q*q
    den=1-mp.exp(-a); c=mp.sqrt(2*den/a)
    def r(x): return c*mp.exp(x/2)*mp.sin(q*x)
    def rp(x): return c*mp.exp(x/2)*(mp.sin(q*x)/2+q*mp.cos(q*x))
    def phi(x): return (-rp(x)+r(x))/lam
    def expect(f): return mp.quad(lambda x:f(x)*mp.exp(-x)/den,[0,a/4,a/2,3*a/4,a])
    ex=1-a/(mp.exp(a)-1)
    var=1-a*a*mp.exp(a)/(mp.exp(a)-1)**2
    meanr=mp.sqrt(2/a)*q*(1+mp.exp(-a/2))/(mp.sqrt(den)*lam)
    residuals={
      'mass':abs(expect(lambda x:r(x)**2)-1),
      'energy':abs(expect(lambda x:rp(x)**2)-lam),
      'mean_r':abs(expect(r)-meanr),
      'mean_r_prime':abs(expect(rp)-meanr),
      'center_phi':abs(expect(phi)),
      'gap_rayleigh':abs(expect(lambda x:r(x)**2)-lam*expect(lambda x:phi(x)**2)),
      'mean_X':abs(expect(lambda x:x)-ex),
      'variance_X':abs(expect(lambda x:(x-ex)**2)-var),
      'gradient_equation':max(abs(-mp.diff(r,x,2)+rp(x)-lam*r(x)) for x in (a/7,a/3,5*a/7)),
      'phi_gradient':max(abs(mp.diff(phi,x)-r(x)) for x in (a/7,a/3,5*a/7)),
    }
    rows.append({'A':aa,'P':str(1/lam),'normalized_covariance':str(var*lam),'mean_R':str(meanr),'residuals':{k:str(v) for k,v in residuals.items()}})
    assert max(residuals.values())<mp.mpf('1e-55')
multipliers=[]
for ll in (1,2,8,32):
    l=mp.mpf(ll)
    numerical=mp.quad(lambda u:mp.mpf(1)/2/((1+u/l)**2*(1+(1+1/l)*u)),[0,1,l,mp.inf])
    exact=((l+1)/l*mp.log(l+1)-1)/2
    assert abs(numerical-exact)<mp.mpf('1e-60')
    multipliers.append({'L':ll,'kappa':str(exact),'quadrature_residual':str(abs(numerical-exact))})
out={'status':'finite_high_precision_diagnostic_pass','dps':mp.mp.dps,'eigenfields':rows,'multipliers':multipliers,'not_tested':['full KL mixture integral','asymptotic limit as A goes to infinity','historical novelty','KLS']}
Path(__file__).with_name('CHECK_RESULTS.json').write_text(json.dumps(out,indent=2))
print('PASS: 4 eigenfield fixtures, 10 checks each; 4 independent multiplier quadratures, 80 decimal digits.')
