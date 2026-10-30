import numpy as np,json
I2=np.eye(2);I3=np.eye(3);P0=np.diag([1.,0]);K=[P0,np.array([[0.,1.],[0.,0.]])]
def mat(d,a,b):
 M=np.zeros((d,d));M[a,b]=1;return M
def op(d,a,b):return np.kron(np.kron(d,a),b)
P=[op(I2,mat(3,0,0),I3),op(I2,I3,mat(3,0,0))]
Q=[np.eye(18)-p for p in P]
V=[sum(op(K[s],mat(3,s+1,0),I3) for s in range(2)),sum(op(K[s],I3,mat(3,s+1,0)) for s in range(2))]
E=[v@v.T for v in V];C=[Q[h]-P[1-h]@E[h] for h in range(2)]
H=sum(P[1-h]@(V[h]+V[h].T) for h in range(2))
# Monomial completion swaps (data1,label1) with (data0,label2), guarded neighbor ready.
Us=[]
for h in range(2):
 U=np.eye(18)
 def ix(d,a,b):return d*9+a*3+b
 x=ix(1,1,0) if h==0 else ix(1,0,1)
 y=ix(0,2,0) if h==0 else ix(0,0,2)
 U[x,x]=U[y,y]=0;U[x,y]=U[y,x]=1;Us.append(U)
U=Us[0]@Us[1]
Ls=[[op(I2,mat(3,0,s),I3) if h==0 else op(I2,I3,mat(3,0,s)) for s in (1,2)] for h in range(2)]
norm=lambda A:float(np.max(np.abs(A)))
checks={
 'flags_projectors':max(norm(c@c-c) for c in C),
 'flags_commute':norm(C[0]@C[1]-C[1]@C[0]),
 'flags_H_commute':max(norm(c@H-H@c) for c in C),
 'reset_no_new_flags':max(norm(C[j]@l@(np.eye(18)-C[j])) for j in range(2) for ls in Ls for l in ls),
 'own_flag_cleared':max(norm(C[h]@l) for h,ls in enumerate(Ls) for l in ls),
 'gauge_factors_commute':norm(Us[0]@Us[1]-Us[1]@Us[0]),
}
Cg=[Q[h]-P[1-h]@(op(I2,mat(3,1,1),I3) if h==0 else op(I2,I3,mat(3,1,1))) for h in range(2)]
checks['gauged_flags_clock_only']=max(norm(U.T@C[h]@U-Cg[h]) for h in range(2))
Hg=sum(P[1-h]@(op(I2,mat(3,0,1)+mat(3,1,0),I3) if h==0 else op(I2,I3,mat(3,0,1)+mat(3,1,0))) for h in range(2))
checks['full_H_scalar_gauge']=norm(U.T@H@U-Hg)
checks['reset_partial_monomial']=all(np.max(np.count_nonzero(U.T@l@U,axis=0))<=1 and np.max(np.count_nonzero(U.T@l@U,axis=1))<=1 for ls in Ls for l in ls)
assert all(v is True or v==0 for v in checks.values())
print(json.dumps({'dimension':18,'all_checks_exact_binary_float':True,'checks':checks},indent=2))
