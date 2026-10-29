from pathlib import Path
import importlib.util,json,itertools,random,hashlib
root=Path(__file__).resolve().parent.parent
source=root/'outer_grs_distillation_20261028'/'grs_wrapper_v1.py'
spec=importlib.util.spec_from_file_location('reviewed_grs',source);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
g=mod.GF(3,0b1011);J=5;t=1;c=mod.construct(g,J,t);count=0
# Exhaust all union-support<=1 qudit Pauli patterns, including simultaneous nonzero X/Z.
patterns=[([0]*J,[0]*J)]
for i in range(J):
 for a,b in itertools.product(range(g.q),repeat=2):
  if a or b:
   e=[0]*J;f=[0]*J;e[i]=a;f[i]=b;patterns.append((e,f))
for e,f in patterns:
 x,z=mod.decoded_error(g,c,e,f);s=c['s'];ell=c['ell'];d_first=x[:s];d_last=x[s+ell:]
 se=[g.dot(row,d_last) for row in c['HRt']];sf=d_first
 assert se==[g.dot(h,e) for h in c['H']] and sf==[g.dot(h,f) for h in c['H']]
 eh,ok1=mod.decode_syndrome(g,c,se);fh,ok2=mod.decode_syndrome(g,c,sf);xh,zh=mod.decoded_error(g,c,eh,fh)
 assert ok1 and ok2 and all(a==b for a,b in zip(x[s:s+ell],xh[s:s+ell])) and all(a==b for a,b in zip(z[s:s+ell],zh[s:s+ell]));count+=1
# Total fallback beyond correction radius always returns an explicit logical Pauli.
rng=random.Random(2026102908)
for _ in range(100):
 e=[rng.randrange(g.q) for _ in range(J)];f=[rng.randrange(g.q) for _ in range(J)];x,z,ok=mod.one_way_correction(g,c,e,f);assert len(x)==len(z)==c['ell'] and all(0<=a<g.q for a in x+z)
print(json.dumps({'source_path':str(source.relative_to(root)),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'field':'GF(8), polynomial x^3+x+1','J':J,'t':t,'encoded_logical_symbols':c['ell'],'exact_correctable_union_support_patterns_checked':count,'beyond_radius_total_fallback_patterns':100,'direct_single_sided_syndrome_orientation_checked':True,'scope':'Exact finite-field and Clifford-label circuit fixture; not a noisy hardware run or a simulation of all 8^5 amplitudes'},indent=2))
