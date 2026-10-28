"""Root derivative receiver. No producer imports or floating premises."""
from replay_offaxis import Q,OUT,WAVE,mon,add,sc,mul,sq,value,diff,inputs
import json,time
def main():
 start=time.perf_counter();F,p,q,T=inputs();k,e,sigma=Q(1,20000000),Q(199999,20000000),Q(1,34)
 H=add(F,sc(-k,sq(q)));ph=add(p,sc(-2*k,mul(q,sq(T))));D=sq(add(T,{(0,0,0,0):sigma}))
 cof=[{mon((i,)):Q(s)} for i,s in [(3,1),(2,-1),(1,-1),(0,1)]]
 NB=[add(mul(D,add(diff(H,i),{mon((i,)):2*e})),sc(-1,mul(ph,cof[i]))) for i in range(4)]
 raw=json.loads((WAVE/'smooth_conic_interface/LOCAL_EVALUATION.json').read_text())
 r,rb,rs=Q(1,4000),Q(1,32000),Q(1,10000);B=2*rb
 C,P=sum(map(abs,H.values()),Q(0)),sum(map(abs,ph.values()),Q(0))
 k0=P*r**6/sigma**2;k1=6*P*r**5/sigma**2+4*P*r**7/sigma**3
 k2=30*P*r**4/sigma**2+52*P*r**6/sigma**3+24*P*r**8/sigma**4
 hd=36*C*r*r+24*C*r*B+k2*(rs+r*r/2+r*B)+2*k1*(r+B)+k0
 assert hd==Q(raw['open_box']['Hessian_deviation_from_minus2eI']) and hd<e
 Lj=12*C*r*r+2*e+r*k1+k0+k1;rows=[]
 for ex in raw['examples']:
  z=list(map(Q,ex['query']));c=ex['certificate'];a=list(map(Q,c['anchor']));l=list(map(Q,c['linear_residual']))
  assert sum(t*t for t in a)<r*r and max(map(abs,z[:4]))<rb and abs(z[4])<rs
  distance=2*sum(map(abs,l),Q(0))/(sigma*sigma*e);err=Lj*distance
  j=[value(pp,a)/value(D,a) for pp in NB+[ph]];g=[v+2*k*t for v,t in zip(j,z)]
  pair=sum(v*t for v,t in zip(g,z));dl=pair-Q(c['upper']);du=pair-Q(c['lower'])+err*err/(4*k)
  rows.append({'query':ex['query'],'rational_gradient_proposal':list(map(str,g)),'gradient_display':[float(v) for v in g],'uniform_component_error':str(err),'gradient_Euclidean_error':str(err),'error_display':float(err),'anchor_distance_bound':str(distance),'global_inverse_query':list(map(str,g)),'global_inverse_distance_bound':str(err/(2*k)),'inverse_distance_display':float(err/(2*k)),'conjugate_lower':str(dl),'conjugate_upper':str(du),'conjugate_width_display':float(du-dl)})
 out={'status':'EXACT_LOCAL_GRADIENT_RECEIVER_PASSED','root_ball_radius':str(r),'strong_concavity_floor':str(e),'Hessian_deviation_replayed':str(hd),'j_Jacobian_bound':str(Lj),'examples':rows,'seconds':time.perf_counter()-start,'scope':'Two off-axis derivatives conditional on proved root in the certified ball; independent Hessian bound replay, no global smoothness claim.'}
 (OUT/'GRADIENT_RECEIVER.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps({'status':out['status'],'errors':[v['error_display'] for v in rows],'seconds':out['seconds']},indent=2))
if __name__=='__main__':main()
