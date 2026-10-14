exec(open('work/FO-continuous-calibration/find_sos_gram.py').read().split("x=pa(")[0])
from scipy.optimize import minimize
from scipy.linalg import null_space
Q0=np.load('work/FO-continuous-calibration/gram_numeric.npy')
x0=tox(Q0)
N=null_space(A)
# Keep the starting solution exactly on the affine subspace up to numerical error.
print('nullity',N.shape)
def mat(z,lam):return toQ(x0+N@z)-lam*np.eye(10)
def cons(y):return np.linalg.eigvalsh(mat(y[:-1],y[-1]))
def fun(y):return -y[-1]
y0=np.zeros(N.shape[1]+1);y0[-1]=-1e-6
res=minimize(fun,y0,method='SLSQP',constraints=[{'type':'ineq','fun':cons}],options={'maxiter':20000,'ftol':1e-12,'disp':True})
print(res.success,res.message,res.fun,res.x[-1],np.linalg.eigvalsh(toQ(x0+N@res.x[:-1])))
np.save('work/FO-continuous-calibration/gram_pd.npy',toQ(x0+N@res.x[:-1]))
