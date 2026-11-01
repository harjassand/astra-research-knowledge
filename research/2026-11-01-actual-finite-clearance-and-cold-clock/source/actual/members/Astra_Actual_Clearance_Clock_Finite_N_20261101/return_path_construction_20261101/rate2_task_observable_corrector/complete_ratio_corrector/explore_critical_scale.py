from pathlib import Path
src=Path(__file__).with_name('explore_complete.py').read_text()
exec(src.split('for q in (3,4,6,8,10):')[0])
for p in (3,4,6,8,10):
 for rr in (mp.mpf('.5'),mp.mpf('2')):
  LL=mp.mpf(10)**p;uu=32/(rr*rr*LL*LL);tt=1/LL;aa=mp.mpf('.01');zz=mp.mpf(0);ss=mp.mpf(1)
  val=gen2(rr,uu,tt,aa,zz,ss);mn=meanf(rr,uu,tt,zz,ss)
  print('CRITICAL L',mp.nstr(LL,4),'r',rr,'u',mp.nstr(uu,4),'normalized drift',mp.nstr(val,18),'mean',mp.nstr(mn,12),'F2-R',mp.nstr(f2(rr,uu,tt,aa,zz,ss)-rr,8),flush=True)
