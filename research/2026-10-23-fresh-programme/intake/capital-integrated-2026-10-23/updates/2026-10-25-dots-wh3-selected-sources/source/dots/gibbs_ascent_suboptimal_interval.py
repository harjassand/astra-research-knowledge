import mpmath as m,json
m.iv.dps=60;i=m.iv;e=i.mpf(1)/100
H=lambda ps:-sum([p*i.log(p) for p in ps],i.mpf(0))
Hrho=H([1-8*e/9]+[e/9]*8);Hout=H([(3-2*e)/9]*3+[e/9]*6)
F=Hrho-3*Hout+2*i.log(3);base=-2*i.log(3);gap=F-base
assert gap.a>i.mpf('1.03')
out={'epsilon':'1/100','a':3,'witness_objective':str(F),'product_objective':str(base),'gap':str(gap),'gap_above_1_03':True,'scope':'Faithful exact-spectrum witness; open-basin stability is proved analytically in .md, not inferred from this arithmetic.'}
print(json.dumps(out,indent=2));open(__file__.replace('.py','.json'),'w').write(json.dumps(out,indent=2)+'\n')
