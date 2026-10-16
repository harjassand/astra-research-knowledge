from independent_audit import *
data=json.loads((ROOT/'phase4_endpoint_toom.json').read_text());L=data['L'];S={decode_id(i,L,1) for i in data['S']};unseen=set(S);bad=[];count=0
while unseen:
 x,a=min(unseen);lift={x:x};queue=[x];component=set();consistent=True
 for x in queue:
  for a in range(4):
   for sign in (-1,1):
    y=list(x);y[a]=(y[a]+sign)%L;y=tuple(y);base=x if sign==1 else y;e=(base,(a,))
    if e not in S:continue
    component.add(e);unseen.discard(e);z=list(lift[x]);z[a]+=sign;z=tuple(z)
    if y not in lift:lift[y]=z;queue.append(y)
    elif lift[y]!=z:consistent=False
 coords=[{x[a] for x in lift} for a in range(4)]
 diameter=[max(min(abs(u-v),L-abs(u-v)) for u in c for v in c) for c in coords]
 spans=[max(x[a] for x in lift.values())-min(x[a] for x in lift.values()) for a in range(4)]
 count+=1
 if not consistent or max(diameter)*8>=L:bad.append(dict(edges=len(component),vertices=len(lift),consistent=consistent,wrapped_coordinate_diameters=diameter,lift_box_spans=spans,D2_eligible=consistent and max(spans)<L))
res=dict(components=count,strict_ineligible=bad);(ROOT/'phase4_ineligible_geometry.json').write_text(json.dumps(res,indent=2));print(json.dumps(res))
