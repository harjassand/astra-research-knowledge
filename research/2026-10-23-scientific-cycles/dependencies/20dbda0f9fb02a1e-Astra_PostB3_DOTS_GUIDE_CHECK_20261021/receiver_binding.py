"""Specific post-B3 receiver boundary. Not a universal scientific certificate."""
import argparse,hashlib,json,zipfile,math,copy,time
from pathlib import Path
EXPECTED='2a064407a4b4ff875f71f7631ae30e4309cb625d5cb3b5cbff3f03f40dac7953'
INPUT='5da0485aed81b23bda57b4a7b4510a394682d54911416db89b4846ff6dd34732'
def require(x,msg):
 if not x:raise ValueError(msg)
def bind(p,r):
 require(p['input_sha256']==INPUT,'independently pinned input')
 require(r['bootstrap_completed']==7 and r['inference_status'].startswith('NOT_COMPUTED'),'partial inference cannot be promoted')
 require(r['leave_one_control_out_status'].startswith('NOT_PERFORMED'),'no unexecuted control omission')
 for row in r['point_summary']:
  v=p['point'][row['representation']][int(row['direction'][0])-1]
  for k in ['gain','ordinary_mse','transfer_mse','additive_mse']:
   require(math.isclose(row[k],math.fsum(v[k])/105,rel_tol=2e-12,abs_tol=2e-12),'aggregate '+k)
  for e,t,g in zip(v['ordinary_mse'],v['transfer_mse'],v['gain']):require(math.isclose(e-t,g,rel_tol=2e-12,abs_tol=2e-12),'individual gain')
def main():
 a=argparse.ArgumentParser();a.add_argument('--archive',required=True);a.add_argument('--output',required=True);a=a.parse_args();start=time.monotonic();p=Path(a.archive);require(hashlib.sha256(p.read_bytes()).hexdigest()==EXPECTED,'independently pinned producer archive')
 with zipfile.ZipFile(p) as z:
  prefix='Astra_PostB3_ULTRA_GUIDE_RESULT_20261021/';point=json.loads(z.read(prefix+'results/POINT_RESULT.json'));r=json.loads(z.read(prefix+'results/RESULT.json'))
 bind(point,r);rejected=[]
 for label in ['changed_input_and_claim','changed_aggregate','promoted_inference']:
  p1,r1=copy.deepcopy(point),copy.deepcopy(r)
  if label=='changed_input_and_claim':p1['input_sha256']='0'*64
  if label=='changed_aggregate':r1['point_summary'][0]['gain']=1.
  if label=='promoted_inference':r1['inference_status']='COMPLETED'
  try:bind(p1,r1)
  except ValueError:rejected.append(label)
  else:raise AssertionError(label+' passed')
 out={'status':'PASS_BOUND_RECEIPT','producer_sha256':EXPECTED,'input_sha256':INPUT,'actual_summary_binding':True,'hostile_rejections':rejected,'scope':'Envelope and reported scalar checks only; independent RNA/design evidence provided separately. No inference guarantee.','wall_s':time.monotonic()-start};Path(a.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':main()
