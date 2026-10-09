import json,itertools,numpy as np,math
from fractions import Fraction
from pathlib import Path
root=Path('work/discrete_critic');c=json.load(open('work/hidden_equilibrium/certificate.txt'))
a=lambda k:np.array([[float(Fraction(t)) for t in row] for row in c[k]])
v=a('points');H=a('H');z=a('farkas_z')-np.array([.8,0]);L=a('L');K=np.eye(8)+L.T;P=np.eye(10)+a('Q');fa=a('facets');N=.1*fa[:,1:];off=.1*fa[:,0]
Z=np.zeros((10,8));tt=np.sum(z*v,axis=1);Z[:5,0]=-5*tt/6;Z[:5,1:3]=z;Z[:5,3:]=tt[:,None]/6
b=np.einsum('ij,ij->i',Z,-H@L);V=np.column_stack([np.ones(5),v[:,0],v[:,1],v[:,0]**2,v[:,0]*v[:,1]]);q=np.linalg.solve(V,b[:5]);gap=-sum(b)/10
words=np.array(list(itertools.product(range(6),repeat=5)),dtype=int)
labels=np.array([0]*5+list(range(1,6)));inds=np.array([labels==i for i in range(6)])
probs=[]
for w in words:
 u=.1*inds[w[0]]
 for letter in w[1:]:u=(u@P)*inds[letter]
 probs.append(u.sum())
probs=np.array(probs); assert abs(probs.sum()-1)<1e-12
Csq=836/75;Ch=503;Ct=6/5
results=[]
for name,pair in [('least_squares',None)]+[(f'pair_{i}_{j}',[i,j]) for i,j in itertools.combinations(range(5),2)]:
 if pair is None:C=np.linalg.solve(N.T@N,N.T)
 else:
  C=np.zeros((2,5));C[:,pair]=np.linalg.inv(N[pair])
 ff=np.zeros((6,6,8));dd=np.zeros((6,6,5))
 for u,j in itertools.product(range(6),repeat=2):
  if u==0:
   psi=np.array([float(j==k+1) for k in range(5)]);ff[u,j,0]=1;ff[u,j,1:3]=C@(psi-off);dd[u,j]=psi-off-N@ff[u,j,1:3]
  else:ff[u,j,2+u]=1
 fm=ff[words[:,2],words[:,1]];fp=ff[words[:,2],words[:,3]]
 gm=ff[words[:,1],words[:,0]]-fm@K.T;gp=ff[words[:,3],words[:,4]]-fp@K.T
 dm=dd[words[:,2],words[:,1]];dp=dd[words[:,2],words[:,3]]
 st={};st['p0']=(words[:,2]==0).astype(float);st['s2']=np.sum(fm[:,1:3]*fp[:,1:3],axis=1);st['Rh']=np.sum(dm*dp,axis=1);st['Rt']=np.sum(gm*gp,axis=1)
 st['Sq']=q[0]*st['p0']+q[1]/2*(fm[:,1]+fp[:,1])+q[2]/2*(fm[:,2]+fp[:,2])+q[3]*fm[:,1]*fp[:,1]+q[4]/2*(fm[:,1]*fp[:,2]+fm[:,2]*fp[:,1])
 base=st['Sq']+Csq*(st['p0']-st['s2']);A=st['p0']+st['s2'];B=st['p0'];rh=st['Rh'];rt=st['Rt']
 best=(1e100,None)
 for aa in np.linspace(.4,.6,41)*gap:
  for bb in np.geomspace(1e-7,.03,100)*gap:
   target=gap-aa-bb/2
   wv=base+aa*A+bb*B+Ch**2/(4*aa)*rh+Ct**2/(4*bb)*rt
   ran=wv.max()-wv.min();score=ran/target
   if score<best[0]:best=(score,(aa,bb,wv,ran,target))
 aa,bb,wv,ran,target=best[1];mean=float(probs@wv);var=float(probs@(wv+target)**2);n=2*ran**2*math.log(40)/target**2
 r={'name':name,'C':C.tolist(),'Fmax':float(abs(ff).max()),'Dmaxnorm':float(np.linalg.norm(dd,axis=2).max()),'alpha':aa,'beta':bb,'Lambda':Ch**2/(4*aa),'Mu':Ct**2/(4*bb),'min':float(wv.min()),'max':float(wv.max()),'range':float(ran),'target_expectation_exact_formula':-target,'target_expectation_float_enumeration':mean,'target_variance_numeric':var,'Hoeffding_N_each_error_025':n,'Bernstein_target_mean_N_each_error_025':(8*var+4*ran*target/3)*math.log(40)/target**2,'statistics_means':{k:float(probs@val) for k,val in st.items()},'Rh_range':[float(rh.min()),float(rh.max())],'Rt_range':[float(rt.min()),float(rt.max())]}
 results.append(r)
 if name=='least_squares':np.savez(root/'enumerated_ls.npz',words=words,probs=probs,**st)
results.sort(key=lambda r:r['Hoeffding_N_each_error_025']);json.dump({'gap':gap,'q_shifted':q.tolist(),'words':len(words),'target_probability_sum':float(sum(probs)),'results':results},open(root/'ENUMERATION.json','w'),indent=2)
for r in results:print(r['name'],'F',r['Fmax'],'range',r['range'],'var',r['target_variance_numeric'],'gap',-r['target_expectation_exact_formula'],'HoeffdingN',r['Hoeffding_N_each_error_025'])
