from pathlib import Path
exec(open(Path(__file__).resolve().parent/'certify.py').read())
inds=[(i,i,0)for i in range(4)]+[(i,j,0)for i in range(4)for j in range(i+1,4)]+[(i,j,1)for i in range(4)for j in range(i+1,4)]
results=[]
for tau in [s.Rational(1,2000),s.Rational(1,1000)]:
 upper=0
 for i,j,im in inds:
  lo=[];hi=[];coeff=[]
  for e,l in zip(E,Ls):
   vals=[s.im(e[i,j]),-s.im(e[j,i])] if im else [s.re(e[i,j]),s.re(e[j,i])]
   lo.append(max(vals)-tau);hi.append(min(vals)+tau)
   coeff.append(s.simplify((2 if i!=j else 1)*(s.im(l[i,j])if im else s.re(l[i,j]))))
  target=s.Integer(1 if i==j else 0);remain=target-sum(lo);assert remain>=0 and target<=sum(hi)
  order=sorted(range(4),key=lambda k:float(coeff[k]),reverse=True)
  for k,l in zip(order,order[1:]):assert coeff[k]>=coeff[l]
  vals=lo.copy()
  for k in order:
   inc=min(remain,hi[k]-lo[k]);vals[k]+=inc;remain-=inc
  assert remain==0
  upper+=sum(v*c for v,c in zip(vals,coeff))
 upper=s.simplify(upper);g45=s.simplify(source45-upper);g43=s.simplify(source43-upper)
 if tau==s.Rational(1,2000):assert g45>s.Rational(245,10**6)
 if tau==s.Rational(1,1000):assert g43>s.Rational(4602,10**6)
 results.append({'component_tolerance':str(tau),'risk_upper_decimal':float(upper),'gap_q45_lower_decimal':float(g45),'gap_q43_lower_decimal':float(g43),'risk_upper_exact':str(upper)})
(root/'tight_box_certificate.json').write_text(json.dumps(results,indent=2));print(json.dumps(results,indent=2))
