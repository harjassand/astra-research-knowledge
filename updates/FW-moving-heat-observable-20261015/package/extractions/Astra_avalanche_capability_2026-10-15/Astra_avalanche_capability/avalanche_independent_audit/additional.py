from pathlib import Path
exec(open(str(Path(__file__).resolve().parent.parent / 'avalanche_independent_audit/check.py')).read().split("res={'recomputed_certificates':[]}")[0])
# Compile exponential-only accessor from the audited source.
(a/'exp.cpp').write_text('#define main original_main\n'+src+'\n#undef main\nint main(){while(std::cin){U x=readU();if(!std::cin)break;I z=exwide(x,x);std::cout<<z.l<<" "<<z.h<<"\\n";}}')
subprocess.run(['g++','-O3','-std=c++17',str(a/'exp.cpp'),'-o',str(a/'exp')],check=True)
random.seed(803);xs=[0,1]+[x+d for k in range(8) for x in [M*2**k//2] for d in [-1,0,1]]+[random.randrange(70*M) for _ in range(1000)]
rows=subprocess.check_output([str(a/'exp')],input='\n'.join(map(str,xs))+'\n',text=True).splitlines();mp.mp.dps=100
for x,row in zip(xs,rows):
 l,h=map(int,row.split());v=mp.exp(-mp.mpf(x)/M);assert mp.mpf(l)/M<=v<=mp.mpf(h)/M
safety=[]
for f in b.glob('large_input*.txt'):
 lines=f.read_text().splitlines();n,limit=map(int,lines[0].split());upper=[int(row.split()[1]) for row in lines[1:1+n]]
 rows=subprocess.check_output([str(a/'exp')],input='\n'.join(map(str,upper))+'\n',text=True).splitlines();lams=[int(row.split()[0]) for row in rows]
 assert min(lams)*limit//D>=64*M
 assert limit*M < 2**128
 safety.append({'input':f.name,'min_lower_rate_numerator':min(lams),'all_tail_cutoffs_verified':True,'rectangle_sum_max_bits':(limit*M).bit_length()})
# Rational arithmetic recurrence versus explicit subsets, with many ties/equalities.
for case in range(120):
 n=random.randrange(1,9);s=sorted([Q(random.randrange(5),4) for _ in range(n)],reverse=True);F=Q(random.randrange(0,9),4);p=[Q(random.randrange(5),4) for _ in range(n)]
 js=[0]+[sum(v*m>F for v in s) for m in range(1,n+1)];pref=[Q(1)]+[Q(0)]*n;save={0:pref.copy()}
 for j in range(n):
  pref=[(1-p[j])*pref[c]+(p[j]*pref[c-1] if c else 0) for c in range(n+1)];save[j+1]=pref.copy()
 h=[Q(1)]*(n+1);hs={n:h.copy()}
 for j in range(n-1,-1,-1):
  h=[(1-p[j])*h[c]*int(c==0 or s[j]*c<=F)+(p[j]*h[c+1]*int(s[j]*(c+1)<=F) if c<n else 0) for c in range(n+1)];hs[j]=h.copy()
 got=[save[js[m]][m]*hs[js[m]][m] if js[m]>=m else Q(0) for m in range(n+1)];want=[Q(0)]*(n+1)
 for bits in itertools.product([0,1],repeat=n):
  k=max([0]+[c for c in range(1,n+1) if sum(x and v*c>F for x,v in zip(bits,s))>=c]);w=Q(1)
  for x,pi in zip(bits,p):w*=pi if x else 1-pi
  want[k]+=w
 assert got==want,(case,s,F,p,got,want)
result={'exp_100_digit_tests':len(xs),'exact_rational_PMF_cases':120,'fixture_overflow_checks':safety};(a/'additional_result.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
