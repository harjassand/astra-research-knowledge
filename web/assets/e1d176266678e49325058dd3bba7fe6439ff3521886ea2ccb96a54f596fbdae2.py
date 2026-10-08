from pathlib import Path
import json, datetime
root=Path(__file__).resolve().parent.parent
cwd=str(root)
rows=[]
for p in Path('/Users/harjas/.codex/sessions/2026/10/08').glob('*.jsonl'):
 try:
  with p.open() as f:
   meta=json.loads(next(f)).get('payload',{})
   if meta.get('cwd')!=cwd:continue
   turn={};usage={}
   for line in f:
    try:r=json.loads(line)
    except ValueError:continue
    if r.get('type')=='turn_context':turn=r.get('payload',{})
    if r.get('type')=='event_msg' and r.get('payload',{}).get('type')=='token_count':usage=(r['payload'].get('info') or {}).get('total_token_usage',{})
  source=meta.get('source',{})
  agent=source.get('subagent',{}).get('thread_spawn',{}).get('agent_path','/root') if isinstance(source,dict) else '/root'
  model=turn.get('model');factor={'gpt-6-astra':5,'gpt-6.1-sol':1,'gpt-6-luna':.05}.get(model)
  u=usage;nominal=None
  if factor is not None and u:nominal=factor*(2*u.get('input_tokens',0)+10*u.get('output_tokens',0))/1e6
  rows.append({'agent':agent,'session_id':meta.get('id'),'started_at':meta.get('timestamp'),'model':model,'reasoning_effort':turn.get('effort'),'sol_price_factor':factor,'usage':u,'nominal_uncached_api_price_usd':nominal,'evidence':str(p)})
 except (OSError,StopIteration):continue
record={'as_of_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Only sessions matching this task cwd. Cumulative token counters include repeated cached context. Nominal prices are accounting proxies, not bills or compute-equivalence. Cached-token discounts and tool charges are not included. Coordinator uses inherited Astra ultra and is charged at 5 Sol token-price equivalents; workers explicitly selected Sol/Luna max.','sources':['https://developers.openai.com/api/docs/models'],'agents':sorted(rows,key=lambda x:x['agent']),'nominal_uncached_api_price_usd':sum(x['nominal_uncached_api_price_usd'] or 0 for x in rows),'total_token_usage':{k:sum(x['usage'].get(k,0) for x in rows) for k in ['input_tokens','cached_input_tokens','output_tokens','reasoning_output_tokens','total_tokens']}}
(root/'work/resource_snapshot.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({'as_of':record['as_of_utc'],'agents':[{k:x[k] for k in ['agent','model','reasoning_effort','sol_price_factor']} for x in record['agents']],'total_token_usage':record['total_token_usage'],'nominal_uncached_api_price_usd':record['nominal_uncached_api_price_usd']},indent=2))
