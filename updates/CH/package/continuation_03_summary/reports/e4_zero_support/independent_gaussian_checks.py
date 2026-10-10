"""Independent high-precision eigensolver diagnostics for the interval certificate.
This is NOT the sign certificate; the latter uses a bounded convergent series.
"""
import mpmath as mp,json
mp.mp.dps=90

def symmetric_function(A,fun):
 vals,vecs=mp.eigsy(A)
 return vecs*mp.diag([fun(x) for x in vals])*vecs.T

def gp_direct(Q,P):
 Pm=symmetric_function(P,lambda x:1/mp.sqrt(x))
 C=Pm*(Q**-1)*Pm/4
 C=(C+C.T)/2
 F=symmetric_function(C,lambda x:mp.atanh(mp.sqrt(x))/mp.sqrt(x))
 return Pm*F*Pm

def direct():
 eta=mp.mpf(3803)/5000;u=mp.mpf(11)/2;w=mp.mpf(10)**6;t=mp.mpf(1)/1800;s=mp.mpf(140)
 ch=(1+t*t)/(1-t*t);sh=2*t/(1-t*t)
 r=u*ch*ch+w*sh*sh;a=w*ch*ch+u*sh*sh;c=(u+w)*sh*ch
 v=mp.mpf(3)/2;ce=mp.sqrt(2);se=mp.sqrt(eta);sl=mp.sqrt(1-eta)
 Qb=mp.matrix([[r,se*c*s],[se*c*s,eta*a*s*s+(1-eta)*v]])
 Pb=mp.matrix([[r,-se*c/s],[-se*c/s,eta*a/s/s+(1-eta)*v]])
 Qe=mp.matrix([[r,-sl*c*s,0],[-sl*c*s,(1-eta)*a*s*s+eta*v,se*ce],[0,se*ce,v]])
 Pe=mp.matrix([[r,sl*c/s,0],[sl*c/s,(1-eta)*a/s/s+eta*v,-se*ce],[0,-se*ce,v]])
 dr=mp.mpf(3377)/4000;da=mp.mpf(-1)
 db=mp.matrix([dr,se*da]);de=mp.matrix([dr,-sl*da,0])
 b=(db.T*gp_direct(Qb,Pb)*db)[0];e=(de.T*gp_direct(Qe,Pe)*de)[0]
 return {'twice_D_B_nats':mp.nstr(b,75),'twice_D_E_nats':mp.nstr(e,75),'twice_gap_nats':mp.nstr(e-b,75),
 'input_A_photon_mean_sigma':mp.nstr((a*s*s+a/s/s-1)/2,35),'reference_photon_mean_sigma':mp.nstr(r-mp.mpf('.5'),35)}

def unref(eta,N,nu=1):
 eta=mp.mpf(eta);N=mp.mpf(N);nu=mp.mpf(nu);a=N+mp.mpf('.5');v=nu+mp.mpf('.5')
 ae=(1-eta)*a+eta*v;ce=mp.sqrt(eta*nu*(nu+1));dis=mp.sqrt((ae+v)**2-4*ce**2)
 l1=(dis+ae-v)/2;l2=(dis-ae+v)/2
 rr=mp.atanh(2*ce/(ae+v))/2
 beta=lambda x:mp.log((x+mp.mpf('.5'))/(x-mp.mpf('.5')))
 be=mp.cosh(rr)**2*beta(l1)+mp.sinh(rr)**2*beta(l2)
 gap=(1-eta)*be-eta*beta(eta*a+(1-eta)*v)
 coef=(v*(1-2*eta)+eta**2*nu*(nu+1)*mp.log((nu+1)/nu))/(eta*(1-eta))
 return {'eta':str(eta),'N':str(N),'N_squared_gap':mp.nstr(N*N*gap,45),'asymptotic_coefficient':mp.nstr(coef,45)}

if __name__=='__main__':
 out={'status':'independent numerical diagnostics only','direct_eigensolver_check':direct(),
 'unreferenced_asymptotic_checks':[unref(e,10**9) for e in ['.75','.7606','.7841','.79']],
 'unreferenced_coefficient_zero':mp.nstr((3-mp.sqrt(9-12*mp.log(2)))/(4*mp.log(2)),65)}
 print(json.dumps(out,indent=2))
 with open('work/continuation_03/reports/e4_zero_support/independent_gaussian_checks.json','w') as f:json.dump(out,f,indent=2)
