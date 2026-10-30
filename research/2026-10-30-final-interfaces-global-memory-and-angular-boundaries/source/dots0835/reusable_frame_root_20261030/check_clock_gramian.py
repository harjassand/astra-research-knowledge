import numpy as np, json
rows=[]
for m in range(2,9):
 labels=[('r',g) for g in range(m)]+[('e',a,b) for a in range(m) for b in range(m) if a!=b]
 index={x:i for i,x in enumerate(labels)}; n=len(labels)
 for v in range(m):
  H=np.zeros((n,n),complex); R=H.copy(); loss=H.copy(); gain=H.copy()
  for g in range(m):
   if g==v: continue
   a=index['r',g]; b=index['e',g,v]
   H[a,b]=H[b,a]=1
   R[a,a]=2.25; R[b,b]=2; R[a,b]=-.5j; R[b,a]=.5j
  for a in range(m):
   for b in range(m):
    if a==b:continue
    e=index['e',a,b]; target=index['r',b]
    if b!=v:R[e,e]=3.25
    loss[e,e]=1
  for a in range(m):
   for b in range(m):
    if a!=b:gain[index['e',a,b],index['e',a,b]]=R[index['r',b],index['r',b]]
  A=np.eye(n); A[index['r',v],index['r',v]]=0
  residual=1j*(H@R-R@H)+gain-(loss@R+R@loss)/2+A
  rows.append({'m':m,'v':v,'residual':float(np.max(np.abs(residual))),'Rmax':float(np.linalg.eigvalsh(R)[-1]),'Rmin_active':float(np.linalg.eigvalsh(R)[1])})
assert max(r['residual'] for r in rows)<1e-12
print(json.dumps(rows,indent=2))
