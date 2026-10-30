import numpy as np,json
rng=np.random.default_rng(3427)
def herm(n):
 a=rng.normal(size=(n,n))+1j*rng.normal(size=(n,n));return (a+a.conj().T)/2
def adj(O,H,Js):
 z=1j*(H@O-O@H)
 for L in Js:
  D=L.conj().T@L;z+=L.conj().T@O@L-(D@O+O@D)/2
 return z
I2=np.eye(2);I3=np.eye(3);P0=np.diag([1.,0,0]);Pe=np.diag([0.,1,0]);P1=np.diag([0.,0,1]);Ba=P0+Pe
# layout Q,spare,router,bath
S=np.zeros((4,4));
for q in range(2):
 for b in range(2):S[2*b+q,2*q+b]=1
G=np.kron(np.kron(np.eye(4),P0)+np.kron(S,Pe+P1),I2)
PD=np.kron(np.kron(np.eye(4),P1),I2);PA=np.eye(24)-PD
R=np.zeros((3,3),complex);R[:2,:2]=[[2.35,-.5j],[.5j,2.]]
a=np.linalg.eigvalsh(R)[-1];Vr=I3+.13*R/a
F=np.diag([1.,np.exp(.7)]);W=np.kron(np.kron(np.kron(F,I2),Vr),I2)
# embed old-Q/bath H and L by explicit finite legs
rows=[]
for j in range(10):
 h=herm(4);l=rng.normal(size=(4,4))+1j*rng.normal(size=(4,4))
 def emb(O):
  ret=np.zeros((24,24),complex)
  for q in range(2):
   for b in range(2):
    for c in range(3):
     for e in range(2):
      i=((q*2+b)*3+c)*2+e
      for qq in range(2):
       for ee in range(2):
        k=((qq*2+b)*3+c)*2+ee;ret[i,k]=O[2*q+e,2*qq+ee]
  return ret
 H=G@emb(h)@G;L=G@emb(l)@G
 z=adj(W,H,[L]);res=np.linalg.norm(z-PA@z@PA)
 # full relative bound restricts exactly to active corner
 ev,U=np.linalg.eigh(W);wi=(U*(ev**-.5))@U.conj().T
 C=np.linalg.norm(wi@z@wi,2);slack=C*PA@W-z
 low=float(np.linalg.eigvalsh(slack)[0]);rows.append({'corner_residual':float(res),'relative_C':float(C),'upper_slack_min':low})
assert max(r['corner_residual'] for r in rows)<1e-10
assert min(r['upper_slack_min'] for r in rows)>-1e-10
# Complete-loss compression: exact outgoing gains are positive for W commuting cut.
P=np.diag([1.,1.,0.,0.]);Q=np.eye(4)-P;W4=np.diag([1.,2.,3.,4.]);H=herm(4);L=herm(4)+1j*herm(4)
full=P@adj(W4,H,[L])@P
Pc=P@W4@P;hp=P@H@P;lp=P@L@P;D=P@L.conj().T@L@P
killed=1j*(hp@Pc-Pc@hp)+lp.conj().T@Pc@lp-(D@Pc+Pc@D)/2
out=P@L.conj().T@Q@W4@Q@L@P
assert np.linalg.norm(full-killed-out)<1e-10
print(json.dumps({'hot_joint_bath_fixtures':rows,'killed_identity_residual':float(np.linalg.norm(full-killed-out)),'min_outgoing_gain':float(np.linalg.eigvalsh(out)[0])},indent=2))
