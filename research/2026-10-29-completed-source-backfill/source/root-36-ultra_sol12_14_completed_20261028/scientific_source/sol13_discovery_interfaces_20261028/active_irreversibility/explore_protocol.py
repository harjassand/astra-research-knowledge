"""Search zero-work marker-to-marker words under a closed control pulse."""
from model import *
from itertools import product
from pathlib import Path
import json,time
START=time.monotonic();OUT=Path(__file__).resolve().parent
rows=[];checked=0
for d in [F(2),F(4),F(1,2)]:
    mats={t:tick(tilt(Q,t)[0]) for t in [F(1),d]}
    ordinary={t:tick(tilt(S,t)[0]) for t in [F(1),d]}
    first=None
    for total in range(3,20):
        for a in range(1,total-1):
            for b in range(1,total-a):
                c=total-a-b;fields=[F(1)]*a+[d]*b+[F(1)]*c
                w=[1]+[0]*(total-1)+[2];pi=[F(1,6)]*6
                f=controlled_word([mats[t] for t in fields],pi,w)
                r=controlled_word([mats[t] for t in reversed(fields)],pi,w[::-1]);checked+=1
                if f!=r:
                    aa=controlled_word([ordinary[t] for t in fields],pi,w)
                    bb=controlled_word([ordinary[t] for t in reversed(fields)],pi,w[::-1]);assert aa==bb
                    first={'d':str(d),'fields':list(map(str,fields)),'word':w,'forward':str(f),'reverse':str(r),'difference':str(f-r),'display_difference':float(f-r),'ordinary_difference':'0'};break
            if first:break
        if first:break
    rows.append(first);print(first,flush=True)
(OUT/'PROTOCOL_EXPLORATION.json').write_text(json.dumps({'results':rows,'candidates':checked,'seconds':time.monotonic()-START},indent=2)+'\n')
