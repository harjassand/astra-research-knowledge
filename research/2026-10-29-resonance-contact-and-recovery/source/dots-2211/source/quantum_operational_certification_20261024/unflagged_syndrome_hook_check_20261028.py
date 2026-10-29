from pathlib import Path
import json
P={'I':(0,0),'X':(1,0),'Y':(1,1),'Z':(0,1)}
def v(w):return tuple(P[c][0] for c in w)+tuple(P[c][1] for c in w)
def add(a,b):return tuple(x^y for x,y in zip(a,b))
def sp(a,b):return sum(a[i]*b[i+5]+a[i+5]*b[i] for i in range(5))%2
G=list(map(v,['XZZXI','IXZZX','XIXZZ','ZXIXZ']));syn=lambda a:tuple(sp(a,g) for g in G)
cor={syn(v('IIIII')):'IIIII'}
for i in range(5):
 for p in 'XYZ':
  w='I'*i+p+'I'*(4-i);cor[syn(v(w))]=w
hook='IIZXI';s=syn(v(hook));c=cor[s];res=add(v(hook),v(c));logical=(sp(res,v('ZZZZZ')),sp(res,v('XXXXX')))
assert s==(0,1,0,0) and c=='IIIIZ' and logical==(1,0)
out={'status':'PASS_EXACT_UNFLAGGED_HOOK_BOUNDARY','fault':'AncillaX after firsttwo controlledPaulis of g0=XZZXI measurement','data_hook':hook,'syndrome':s,'minimum_weight_correction':c,'residual_logical_XZ_bits':logical,'source_draws':0,'scope':'One explicit standard unflagged syndrome circuit; not a no-go for fault-tolerant syndrome gadgets.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
