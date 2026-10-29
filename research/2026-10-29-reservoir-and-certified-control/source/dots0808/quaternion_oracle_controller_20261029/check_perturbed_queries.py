from quartic_sos_oracle import *
root=Path(__file__).parent;rng=np.random.default_rng(20261029);T=60000;p=Q(1,2);d=35;R0=math.ceil(720*math.sqrt(T/(d*float(p))));M=2**math.ceil(math.log2(4*d*T*T));eps=Q(R0,4*T*T)
reports=[];start_all=time.time()
for fixture in ['one_axis','drift']:
 bank=json.load(open(root/f'bank_{fixture}.json'))
 for edge in range(3):
  raw=bank_polynomial(bank,edge);centered=add(raw,mul(Qpoly,Qpoly),-3*bank['probe_calls'])
  for rep in range(4):
   perturb={e:Q(R0*(2*int(rng.integers(M))+1-M),M) for e in exps}
   query={e:Q(centered.get(e,0),4*p)+perturb[e]/2 for e in exps}
   maxc=max(abs(x) for x in query.values());power=max(0,maxc.numerator.bit_length()-maxc.denominator.bit_length()+1);scale=2**power;f={e:x/scale for e,x in query.items()}
   st=time.time();g0,gq,ns=gram_param(f);qr,up=find_candidate(f,seed=rep+edge*20,starts=24)
   xx,tr=barrier_search(g0,gq,ns,mu_final=1e-12);lo,ys,G,piv,tries=rational_certificate(g0,gq,ns,xx,bits=50,repair_start_bits=48);verify_identity(f,lo,G)
   gap=(up-lo)*scale
   cert=dict(fixture=fixture,edge=edge,rep=rep,query_coefficients=[str(query[e]) for e in exps],exponents=exps,scale=scale,quaternion=[str(x) for x in qr],upper=str(up),lower=str(lo),gram=[[str(x) for x in row] for row in G],requested_gap=str(eps),actual_gap=str(gap),success=gap<=eps,seconds=time.time()-st)
   (root/f'perturbed_{fixture}_{edge}_{rep}.json').write_text(json.dumps(cert,indent=2)+'\n')
   row={k:cert[k] for k in ['fixture','edge','rep','success','seconds']};row['gap']=float(gap);reports.append(row);print(json.dumps(row),flush=True)
result=dict(T=T,p=str(p),perturbation_radius=R0,midpoint_grid_size=M,requested_absolute_gap=str(eps),queries=reports,successes=sum(x['success'] for x in reports),seconds=time.time()-start_all,scope='Actual cumulative acquired-bank FTPL-style perturbation queries; exact SOS certificates checked. Not an online controller run, and failures require declared fallback.')
(root/'perturbed_queries_summary.json').write_text(json.dumps(result,indent=2)+'\n')
