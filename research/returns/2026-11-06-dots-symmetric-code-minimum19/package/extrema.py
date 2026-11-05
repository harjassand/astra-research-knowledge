exec(open('pi_code_bound_20261105/shadow_screen.py').read().split('for n in [')[0])
n=18;D=n+1;M=s.Matrix([[s.Rational(x) for x in row] for row in json.loads((r/f'transform_n{n}.json').read_text())]);N=np.array(M,float);G=2*N-np.eye(D);S=N*np.array([(-1)**l for l in range(D)])[None,:];H=np.vstack([G,S]);eq=np.vstack([np.eye(D)[0],np.ones(D),G[1:5]]);rhs=np.r_[1,D/2,np.zeros(4)]
for i in range(D):
 o=linprog(-np.eye(D)[i],A_ub=-H,b_ub=np.zeros(len(H)),A_eq=eq,b_eq=rhs,bounds=(0,None)); print(i,o.status,-o.fun if o.status==0 else None)
