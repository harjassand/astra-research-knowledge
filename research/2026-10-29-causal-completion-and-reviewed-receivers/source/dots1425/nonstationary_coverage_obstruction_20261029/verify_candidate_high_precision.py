import mpmath as m,json
m.mp.dps=80;v=json.load(open('TWO_STEP_OPTIMIZER.json'))['best'];r=m.matrix([[m.mpf(str(v['rho_real'][i][j]))+1j*m.mpf(str(v['rho_imag'][i][j])) for j in range(4)] for i in range(4)])
def F(r):
 z=m.zeros(4)
 for i in range(2):
  for j in range(2):
   z[i,j]=r[2+i,2+j]/2;z[i,2+j]=r[2+i,j]/m.sqrt(2);z[2+i,j]=r[i,2+j]/m.sqrt(2);z[2+i,2+j]=r[i,j]+r[2+i,2+j]/2
 return z
def S(r):
 ev=m.eigh(r,eigvals_only=True);assert min(ev)>0;return -sum(x*m.log(x) for x in ev)
def L(r,o):return S(o)-S(r)+sum((o[i,i]-r[i,i]).real*m.log(m.mpf(1)/3 if i<2 else m.mpf(2)/3) for i in range(4))
rows=[]
for eps in ['1e-12','1e-10','1e-8','1e-6']:
 rr=r+m.mpf(eps)*m.eye(4);rr/=sum(rr[i,i] for i in range(4));o=F(rr);o2=F(o);a=L(rr,o);b=L(rr,o2);rows.append({'regularization':eps,'min_eigenvalue':str(min(m.eigh(rr,eigvals_only=True))),'loss1':str(a),'loss2':str(b),'ratio':str(b/a)})
print(rows);open('HIGH_PRECISION_CHECKS.json','w').write(json.dumps({'precision_digits':80,'scope':'high precision arithmetic, not directed intervals','rows':rows},indent=2)+'\n')
