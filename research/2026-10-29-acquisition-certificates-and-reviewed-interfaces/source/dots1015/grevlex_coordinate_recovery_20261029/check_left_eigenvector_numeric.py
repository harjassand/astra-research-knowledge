from check_adjugate_coordinates import *
from scipy.linalg import eig
st=time.time();m=[np.array([[float(x) for x in c] for c in a]).T for a in raw];I=np.eye(40);Q=I+sum(a@a for a in m);powers=[[I,a,a@a,a@a@a] for a in m];num=np.zeros_like(I)
for e,c in terms:
 v=I
 for j,k in enumerate(e):v=v@powers[j][k]
 num+=float(c)*v
L=np.linalg.solve(Q,num)/4;vals,vec=eig(L.T);root=json.loads((SRC/'root_candidate_certificate.json').read_text());mid=sum(F(x) for x in root['least_real_value_interval'])/2;i=np.argmin(abs(vals-float(mid)));w=vec[:,i]/vec[0,i];coords=[w[basis_i] for basis_i in [3,2,1]]
out={'status':'FLOATING_CONDITIONING_DIAGNOSTIC_ONLY','Q_condition_number':float(np.linalg.cond(Q)),'selected_eigenvalue':[float(vals[i].real),float(vals[i].imag)],'target_midpoint':float(mid),'coordinates':[[float(x.real),float(x.imag)] for x in coords],'normalized_eigen_residual':float(np.linalg.norm(L.T@w-vals[i]*w)/np.linalg.norm(w)),'seconds':time.time()-st};(OUT/'left_eigenvector_numeric.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
