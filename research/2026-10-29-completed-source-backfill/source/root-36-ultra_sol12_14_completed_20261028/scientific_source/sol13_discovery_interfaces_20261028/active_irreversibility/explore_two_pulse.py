from model import *
from pathlib import Path
import json,time
START=time.monotonic();OUT=Path(__file__).resolve().parent
pi=[F(1,6)]*6;rows=[];count=0
for d in [F(2),F(4),F(1,2)]:
    mats={t:tick(tilt(Q,t)[0]) for t in [F(1),d]};found=None
    for size in range(3,22):
        for a in range(1,size-1):
            for b in range(1,size-a):
                c=size-a-b
                if min(a,b,c)<1:continue
                fields=[F(1)]+[d]*a+[F(1)]*b+[d]*c+[F(1)]
                w=[1]+[0]*(len(fields)-1)+[2]
                f=controlled_word([mats[t] for t in fields],pi,w)
                r=controlled_word([mats[t] for t in reversed(fields)],pi,w[::-1]);count+=1
                if f!=r:
                    found={'d':str(d),'abc':[a,b,c],'fields':list(map(str,fields)),'word':w,'forward':str(f),'reverse':str(r),'difference':str(f-r),'display_difference':float(f-r)};break
            if found:break
        if found:break
    rows.append(found);print(found,flush=True)
(OUT/'TWO_PULSE_EXPLORATION.json').write_text(json.dumps({'results':rows,'candidates':count,'seconds':time.monotonic()-START},indent=2)+'\n')
