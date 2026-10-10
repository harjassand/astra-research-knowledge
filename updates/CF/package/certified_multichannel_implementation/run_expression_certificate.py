"""Certify the exact endpoint produced by a saved empirical panel proposal.

The saved proposal has no trusted numerical accuracy: it supplies only dyadic
panel endpoints and algorithm parameters. Reconstructed finite expressions are
certified against the original rational coefficient input. All replay cost is
added to the original cold proposal cost, not hidden as free preprocessing.
"""
import argparse,json,time,hashlib,resource,gzip
from pathlib import Path
from fractions import Fraction
import numpy as np
import sympy as sp
import prototype_numpy as proto
import certify_finite_expression as cert
BASE=Path(__file__).parent

def validate_input(row):
 t,u=sp.symbols('t u');eta=sp.Rational(row['eta']);omega=sp.Rational(row['omega'])
 coeff=[sp.Matrix([[sp.Rational(x) for x in rr] for rr in a]) for a in row['coefficients_ascending_t']]
 H=sum((a*t**j for j,a in enumerate(coeff)),sp.zeros(3));A=(omega*eta*H.subs(t,sp.Rational(1,2)+eta*u)).applyfunc(sp.expand)
 target=(sp.Rational(2)**row['frequency_offset'])*sp.Matrix([[u*u-1,1,sp.Rational(1,3)],[1,u/3,2],[sp.Rational(1,3),2,-u*u-u/3+1]])
 assert A==target

def run(rowid,seconds=30):
 start=time.perf_counter();manifest=json.loads((BASE/'benchmark_manifest.json').read_text())
 if (BASE/'benchmark_extra_B6.json').exists():manifest['rows']+=json.loads((BASE/'benchmark_extra_B6.json').read_text())
 row=next(r for r in manifest['rows'] if r['id']==rowid);validate_input(row)
 proposals=json.loads((BASE/'exploratory_manifest_results.json').read_text())
 if (BASE/'extra_B6_proposal.json').exists():proposals['rows']+=json.loads((BASE/'extra_B6_proposal.json').read_text())
 proposal=next(r for r in proposals['rows'] if r['id']==rowid)['candidate'];assert proposal['status']=='complete_uncertified'
 records=proposal['panels'];B=row['B'];f=row['frequency_offset'];s=row['precision_bits'];L=proposal['L'];end=2.**(B-1)
 prev=Fraction(-end)
 for p in records:
  aa,bb=Fraction(p['a']),Fraction(p['b']);assert aa==prev and bb>aa;prev=bb
 assert prev==Fraction(end)
 count={'eigensystems':0,'projector_jet_orders':0,'normal_form_stages':0,'_capture_polynomials':True}
 U=(cert.Q*np.eye(3,dtype=object),cert.zero());error=0;cert_records=[];witness_panels=[];status='complete';assembly_seconds=certificate_seconds=0.
 for p in records:
  if time.perf_counter()-start>seconds:status='censored';break
  a,b=p['a'],p['b'];c=(a+b)/2;h=(b-a)/2
  assert Fraction(c)-Fraction(h)==Fraction(a) and Fraction(c)+Fraction(h)==Fraction(b)
  groups=[];i=0
  for size in p['groups']:groups.append(list(range(i,i+size)));i+=size
  ts=time.perf_counter();_,_,_,meta=proto.panel(c,h,2.**f,L,p['N'],groups,count);assembly_seconds+=time.perf_counter()-ts
  ts=time.perf_counter()
  Cs=[[cert.ipair(x) for x in poly] for poly in meta['_polys']]
  Ph=[[round(Fraction(float(x))*cert.Q) for x in phi] for phi in meta['_phases']]
  V,local,bounds=cert.certify_integer_panel(c,h,2.**f,Cs,Ph);U,error=cert.compose(V,U,error,local)
  witness_panels.append({'a':str(Fraction(a)),'b':str(Fraction(b)),'c':str(Fraction(c)),'h':str(Fraction(h)),'C_integer_pairs':[[[[[str(int(x)) for x in rr] for rr in mat] for mat in pair] for pair in poly] for poly in Cs],'phase_integer_coefficients':[[str(x) for x in phi] for phi in Ph]})
  certificate_seconds+=time.perf_counter()-ts
  cert_records.append({'a':a,'b':b,'groups':p['groups'],'N':p['N'],**bounds,'global_error_upper_dyadic_integer':str(error)})
 witness={'row':row,'coefficient_fraction_bits':cert.P,'phase_fraction_bits':cert.EP,'global_error_fraction_bits':cert.CP,'panel_witnesses':witness_panels}
 witness_path=BASE/f'coefficient_witness_{rowid}.json.gz'
 with gzip.open(witness_path,'wt',encoding='utf-8') as fw:json.dump(witness,fw,separators=(',',':'))
 elapsed=time.perf_counter()-start
 result={'row_id':rowid,'status':status,'coefficient_witness':witness_path.name,'coefficient_witness_sha256':hashlib.sha256(witness_path.read_bytes()).hexdigest(),'requested_operator_error':2.**(-s),'proof_mode':'exact-integer residual and endpoint certificate','proposal_is_trusted_for_accuracy':False,'proposal_cold_seconds':proposal['cold_row_seconds'],'certificate_replay_seconds':elapsed,'reconstructed_expression_seconds':assembly_seconds,'exact_certificate_seconds':certificate_seconds,'total_charged_seconds':proposal['cold_row_seconds']+elapsed,'coefficient_fraction_bits':cert.P,'phase_fraction_bits':cert.EP,'global_error_fraction_bits':cert.CP,'global_operator_error_upper_integer':str(error),'global_operator_error_upper':float(Fraction(error,cert.CQ)),'certified_target_met':status=='complete' and error<=cert.CQ//(2**s),'panels_certified':len(cert_records),'separated_panels_certified':sum(p['N']>0 for p in cert_records),'counters':count,'panel_certificates':cert_records,'memory_high_water_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
 if status=='complete':
  result['endpoint_exact_dyadic_integer_pairs']=[[[str(U[0][i,j]),str(U[1][i,j])] for j in range(3)] for i in range(3)]
  result['endpoint_denominator_power_of_two']=cert.P
  computed=np.array([[complex(float(Fraction(U[0][i,j],cert.Q)),float(Fraction(U[1][i,j],cert.Q))) for j in range(3)] for i in range(3)])
  old=np.array([[complex(*v) for v in rr] for rr in proposal['endpoint']]);result['observed_disagreement_from_uncertified_proposal']=float(np.linalg.norm(computed-old,2))
 result['code_sha256']={name:hashlib.sha256((BASE/name).read_bytes()).hexdigest() for name in ['certify_finite_expression.py','prototype_numpy.py','run_expression_certificate.py']}
 out=BASE/f'certified_expression_{rowid}.json';out.write_text(json.dumps(result,indent=2)+'\n')
 return result
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--row',default='B4_f0_s20');ap.add_argument('--seconds',type=float,default=30);a=ap.parse_args();r=run(a.row,a.seconds)
 print(json.dumps({k:v for k,v in r.items() if k not in ('panel_certificates','endpoint_exact_dyadic_integer_pairs')},indent=2))
