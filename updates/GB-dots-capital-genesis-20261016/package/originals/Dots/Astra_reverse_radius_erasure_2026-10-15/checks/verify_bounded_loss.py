from fractions import Fraction as F
for m in (3,8,100):
    lam=-F(1,m-1)
    col=[lam*(F(int(y==0))-F(1,m)) for y in range(m)]
    diamond=sum(map(abs,col)); assert diamond==F(2,m)
    # Equiprobable labels encoded in two different classical basis inputs.
    plus=[F(int(y!=0),m-1) for y in range(m)]
    minus=[F(int(y!=1),m-1) for y in range(m)]
    explained=sum((a-b)**2/(2*(a+b)) if a+b else 0 for a,b in zip(plus,minus))
    risk_T=1-explained; assert risk_T==1-F(1,m-1)
    q=F(1,2*(m-1)); risk_E=1-q; gap=risk_E-risk_T
    assert F(0)<gap<=min(F(1),F(4,m))
    print('m=',m,'exact diamond=',diamond,'MMSE(T)=',risk_T,'q=',q,'actual gap=',gap,'universal bound=',min(F(1),F(4,m)))
