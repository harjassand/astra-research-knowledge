"""Late PR92 copy-only calculation audit and exact conditional continuation check."""
from pathlib import Path
from fractions import Fraction as F
import hashlib, json, math, os, platform, shutil, subprocess, sys, tempfile, time

OUT=Path(__file__).resolve().parent
W=Path('/Users/harjas/Documents/ChatGPT/ultra/work/astra-pr92-audit-20261015')
PIN='5eb2441c93011d4fefb819b6f751f33537427dc3'
PREFIX='updates/FT-foundational-capability-20261015'
P=W/PREFIX/'package'
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def git(*args): return subprocess.check_output(['git','-C',str(W),*args],text=True).strip()
def snapshot():
 paths=git('ls-files','--',PREFIX).splitlines()
 return {p:sha(W/p) for p in paths}
def save(name,data): (OUT/name).write_text(json.dumps(data,indent=2)+'\n')
before=snapshot()
assert git('rev-parse','HEAD')==PIN
assert not git('status','--porcelain=v1','--untracked-files=all')
copy=Path(tempfile.mkdtemp(prefix='pr92-capital-review-'))/'package'
shutil.copytree(P,copy,ignore=shutil.ignore_patterns('__pycache__','*.pyc','sources','replays','*.pdf','*.png'))
logs=OUT/'replay_logs'; logs.mkdir(exist_ok=True)
specs=['root/isotope_renewal.py','workers/physical_path/calculate.py','workers/scientific_operation/verify_operation.py','workers/abelian_sampler_audit/exact_audit.py','workers/abelian_sampler_audit/hnf_audit.py']
results=[]
for rel in specs:
 argv=[sys.executable,'-B',str(copy/rel)]
 start=time.perf_counter()
 proc=subprocess.run(argv,cwd=(copy/rel).parent,capture_output=True,text=True,timeout=45,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
 stem=rel.replace('/','__').removesuffix('.py')
 stdout=logs/(stem+'.stdout.txt'); stderr=logs/(stem+'.stderr.txt')
 stdout.write_text(proc.stdout); stderr.write_text(proc.stderr)
 results.append({'script':rel,'input_sha256':sha(P/rel),'argv':argv,'cwd':str((copy/rel).parent),'exit_code':proc.returncode,'status':'PASS' if proc.returncode==0 else 'FAIL','wall_seconds':time.perf_counter()-start,'stdout':str(stdout.relative_to(OUT)),'stdout_sha256':sha(stdout),'stderr':str(stderr.relative_to(OUT)),'stderr_sha256':sha(stderr)})
 assert proc.returncode==0, rel
# Independent exact toy: p=1/2, rates H=1,L=2, d=log4.
a=F(1,2)*F(1,4)+F(1,2)*F(1,16)
q=F(1,2)*F(1,4)/a
m=F(1,2)*(1-F(1,4))+F(1,4)*(1-F(1,16))
mean=m/a
failure_transform=F(1,4)*(1-F(1,16))+F(1,3)*(1-F(1,64))
laplace=(a*F(1,4))/(1-failure_transform)
assert (a,q,mean,laplace)==(F(5,32),F(4,5),F(39,10),F(5,56))
qstar=F(2,3)
final=qstar+(q-qstar)*laplace
retained=q*laplace
assert final==F(19,28) and retained==F(1,14)
assert math.exp(-float(mean))<float(laplace)
# Check transform recursion and its derivative against independent mean formula.
def L(s,p,sh,sl,d):
 aa=p*math.exp(-sh*d)+(1-p)*math.exp(-sl*d)
 fail=p*sh/(sh+s)*(-math.expm1(-(sh+s)*d))+(1-p)*sl/(sl+s)*(-math.expm1(-(sl+s)*d))
 return aa*math.exp(-s*d)/(1-fail)
num_checks=[]
for p,sh,sl,d in [(.5,1.,2.,math.log(4)),(.01109,.21,5.66,.12271163490724202),(.4,0.,2.,.9)]:
 aa=p*math.exp(-sh*d)+(1-p)*math.exp(-sl*d)
 mm=(p*(-math.expm1(-sh*d))/sh if sh else p*d)+(1-p)*(-math.expm1(-sl*d))/sl
 # At s=0 with sh=0, define absent failure term continuously as zero.
 def ell(s):
  fail=(p*sh/(sh+s)*(-math.expm1(-(sh+s)*d)) if sh or s else 0.)+(1-p)*sl/(sl+s)*(-math.expm1(-(sl+s)*d))
  return aa*math.exp(-s*d)/(1-fail)
 h=1e-6
 deriv=-(ell(h)-ell(-h))/(2*h)
 assert abs(ell(0)-1)<1e-13
 assert abs(deriv-mm/aa)<1e-6*max(1,mm/aa)
 num_checks.append({'p':p,'sigma_H':sh,'sigma_L':sl,'d':d,'L0':ell(0),'derivative_mean':deriv,'renewal_mean':mm/aa})
save('CONTINUATION_CHECKS.json',{'status':'PASS_CONDITIONAL_ARITHMETIC_ONLY','toy':{'p':'1/2','sigma_H':'1','sigma_L':'2','screen_d':'log4','acceptance':str(a),'accepted_H':str(q),'expected_total_dose':str(mean),'L_D_at_1':str(laplace),'neutral_refill_final_H_when_b_eta_1':str(final),'same_atom_H_retention_when_sigma_H_eta_1':str(retained)},'transform_mean_checks':num_checks,'scope':'Exact rational toy and finite derivative checks; analytic proof is separate; no measured beam, isotope operation or advantage.'})
after=snapshot()
assert before==after
assert not git('status','--porcelain=v1','--untracked-files=all')
save('CHECK_RECEIPT.json',{'schema':'astra.late-pr92.capital-review.v1','head':PIN,'tree':git('rev-parse','HEAD^{tree}'),'base':'b7cada92d2eb304578be5ed974f1e44b10a89928','python':sys.version,'executable':sys.executable,'platform':platform.platform(),'disposable_copy':str(copy),'fresh_selected_replay':results,'all_five_pass':True,'source_tracked_files_checked':len(before),'source_before_after_equal':True,'readonly_worktree_status_after':'clean','source_hashes':before,'scope':'Five source scripts executed only in disposable copy, not source tree. Bounded arithmetic and tiny adapter/model checks only; not full PR replay, independent theorem/priority review or physical validation.'})
print(json.dumps({'all_five_pass':True,'source_unchanged':True,'tracked_FT_files':len(before),'continuation_exact_checks':'PASS','output':str(OUT)},indent=2))
