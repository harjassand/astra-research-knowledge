from pathlib import Path
r=Path(__file__).parent
exec((r/'certify_cholam_cached.py').read_text().split('st=time.time()')[0])
js=json.load(open(root/'isolated_roots_cache.json'));(a,b),mult=js[15];a,b=s.Rational(a),s.Rational(b);st=time.time();print('root15 endpoints',float(a),float(b),flush=True)
aa,bb=s.polys.polytools.refine_root(uni,a,b,eps=s.Rational(1,2**64),fast=True);print('refined seconds',time.time()-st,flush=True)
(root/'root15_fast_refinement.json').write_text(json.dumps(dict(initial=[str(a),str(b)],refined=[str(aa),str(bb)],seconds=time.time()-st))+'\n')
