import sys,json,subprocess,time
from pathlib import Path
from math import comb
P=Path(__file__).parent;sys.path.insert(0,str(P/'source'))
from construct_inner import sp,rbasis,transform,low_errors
subprocess.run(['g++','-O3','-std=c++17',str(P/'independent_distance.cpp'),'-o',str(P/'independent_distance')],check=True)
results=[]
for h in [2,3,4,5]:
 z=json.loads((P/'source'/f'inner_h{h}.json').read_text());n=z['n'];k=z['k'];rows=[int(x,16) for x in z['generators']];assert len(rbasis(rows))==n-k and all(sp(a,b,n)==0 for a in rows for b in rows)
 data=[f'{n} {h}']
 for j in range(n):
  for a in [1,2,3]:
   e=((a&1)<<j)|((a>>1)<<(n+j));s=sum(sp(e,v,n)<<i for i,v in enumerate(rows));data.append(f'{s&((1<<64)-1)} {s>>64}')
 start=time.time();cp=subprocess.run([str(P/'independent_distance')],input='\n'.join(data),capture_output=True,text=True,check=True);count,zeros=map(int,cp.stdout.split());assert zeros==0 and count==sum(comb(n,w)*3**w for w in range(1,h))
 gs=z['decoder_gates'];maxphase=0
 for row in rows:
  q,ph=transform(row,0,gs,n);assert q&((1<<n)-1)==0 and q>>(2*n-k)==0
 for e in low_errors(n,(h-1)//2):
  q,ph=transform(e,(e&(e>>n)).bit_count()%4,gs,n);sy=q&((1<<(n-k))-1);l=((q&((1<<n)-1))>>(n-k))|((q>>(2*n-k))<<k)
  assert z['syndrome_table'][str(sy)]['logical']==l
 results.append({'h':h,'n':n,'distance_at_least':h,'independently_enumerated':count,'zero_syndrome_errors':zeros,'elapsed_seconds':time.time()-start,'all_saved_table_entries_recomputed':True})
(P/'independent_results.json').write_text(json.dumps(results,indent=2)+'\n');print(results)
