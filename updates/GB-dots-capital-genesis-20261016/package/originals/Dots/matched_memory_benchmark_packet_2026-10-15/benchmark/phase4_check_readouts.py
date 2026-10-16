from independent_audit import *
exe=str(ROOT/'simulator_readouts')
count=0

def recover(s,L,policy):
 global count
 p=subprocess.run([exe,'decode',str(L),policy[-1]],input=' '.join(str(encode(e,L)) for e in sorted(s)),text=True,capture_output=True,check=True)
 lines=p.stdout.splitlines();flag=int(lines[0]);D={decode_id(int(i),L,2) for i in lines[1].split()} if len(lines)>1 else set()
 assert bd(D,L)==s,(L,policy,'boundary')
 count+=1;return flag,D

def rectangle(L,axes,x,width,height):
 out=set()
 for u in range(width):
  for v in range(height):
   z=list(x);z[axes[0]]=(z[axes[0]]+u)%L;z[axes[1]]=(z[axes[1]]+v)%L;out.add((tuple(z),axes))
 return out

def run():
 for L in (16,17):
  for axes in ORI:
   for x in ((0,)*4,(L-1,)*4,(L//2,)*4):
    E={(x,axes)};s=bd(E,L);r=[recover(s,L,p) for p in ('D0','D1','D2')]
    assert r[0]==r[1]==r[2] and not r[0][0] and not hom(E^r[0][1])
   # wide seam disk exceeds strict cutoff but is injectively contractible.
   E=rectangle(L,axes,(L-1,)*4,3,2);s=bd(E,L)
   r0,r1,r2=[recover(s,L,p) for p in ('D0','D1','D2')]
   assert r0[0] and r1[0] and not r2[0] and not hom(E^r2[1])
   assert r0[1]==r1[1]==literal_H(s,L)
   # Pair of winding loops may ONLY be filled jointly. Local component is retained by D1/D2.
   strip=rectangle(L,axes,(0,)*4,L,1);z=(L//2,)*4;local={(z,axes)};s=bd(strip^local,L)
   r0,r1,r2=[recover(s,L,p) for p in ('D0','D1','D2')]
   assert all(r[0] for r in (r0,r1,r2));assert r0[1]==literal_H(s,L)
   expected=local^literal_H(bd(strip,L),L)
   assert r1[1]==r2[1]==expected
 # Consistent connected staircase disk with lift span >=L is NOT injective-box eligible.
 L=16;E={((t%L,(t//2)%L,1,1),(0,1)) for t in range(L+1)};s=bd(E,L)
 r2=recover(s,L,'D2');assert r2[0] and r2[1]==literal_H(s,L)
 res={'status':'PASS','cases':count,'checks':['strict-eligible equality D0 D1 D2','wide seam local disks','winding pair stays combined','eligible fills retained','span>=L rejected','independent recovery boundary']}
 (ROOT/'phase4_independent_readout_results.json').write_text(json.dumps(res,indent=2));print(json.dumps(res))
if __name__=='__main__':run()
