import numpy as np, math, json
from scipy.special import gammaln, xlogy
from scipy.optimize import brentq

def calc(D,eta,nu=1.,tail=1e-14):
 G=1+(1-eta)*nu; tau=eta/G; q=(G-1)/G; a=tau/(G-1); b=1-tau
 N=np.arange(max(100,int(D*(G-1)+30*np.sqrt(D*G*(G-1))+100)))
 ld=gammaln(N+D)-gammaln(N+1)-gammaln(D)
 logc=-D*np.log(G)+N*np.log(q)
 mass=np.exp(ld+logc)*(b+a*N/D)
 w=np.zeros_like(mass)
 w[1:]=N[1:]/(N[1:]+D-1)/D*(b+a*(N[1:]+D-1))/(b+a*N[1:]/D)
 # d_N/d_{N-1}=(N+D-1)/N; m0/d_N=D-N/(N+D-1)
 rat=np.zeros_like(mass); rat[1:]=np.log2((N[1:]+D-1)/N[1:])
 ent=-(xlogy(w,w)+xlogy(1-w,1-w))/np.log(2)
 val=w*rat-(1-w)*np.log2(D-N/(N+D-1))-ent
 return {'D':D,'eta':eta,'Ic':float(mass@val),'mass':float(mass.sum()),'mean_input_photons':1}
if __name__=='__main__':
 vals=[calc(D,e) for D in [2,3,4,8,16,32,64,128] for e in [.75,.78,.8,.85,.9]]
 roots=[]
 for D in [2,3,4,8,16,32,64,128]:
  roots.append({'D':D,'eta_zero':brentq(lambda e:calc(D,e)['Ic'],.75,.999)})
 print(json.dumps({'values':vals,'roots':roots},indent=2))
