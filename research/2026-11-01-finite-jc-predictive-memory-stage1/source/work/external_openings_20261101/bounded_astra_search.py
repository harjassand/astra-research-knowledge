"""Reproduce three bounded operation searches over pinned public score shards.

Uses six terms, twelve shards, the published two score lanes and parent
deduplication. No concept expansion and no scientific inference from ranking.
All fetched bytes, including the catalog, are checked against the pinned
search manifest before use. No archive crawl or backend execution.
"""
import hashlib,json
from collections import defaultdict
from pathlib import Path
BASE=Path(__file__).resolve().parent/'sources'
OUT=BASE.parents[2]/'outputs/external_openings_20261101'
def read(path):
    raw=(BASE/path).read_bytes();expected=manifest['outputs']['knowledge/current/'+path.replace('astra_shards/','').replace('postings_','postings/').replace('lexical_','lexical/')]
    assert hashlib.sha256(raw).hexdigest()==expected,path
    return json.loads(raw)
manifest=json.loads((BASE/'astra_search_manifest.json').read_text())
raw=(BASE/'astra_catalog.json').read_bytes()
assert hashlib.sha256(raw).hexdigest()==manifest['outputs']['knowledge/current/catalog.json']
data=json.loads(raw);rows=[]
for query in ('heterodyne mode','receiver freshness','memory entropy'):
    scores=defaultdict(float);lex=defaultdict(float)
    for term in query.split():
        shard=hashlib.sha256(term.encode()).hexdigest()[:2]
        for folder,dest in (('postings',scores),('lexical',lex)):
            for index,score in read('astra_shards/'+folder+'_'+shard+'.json').get(term,[]):dest[index]+=score
    selected=[];seen=set()
    for index,score in sorted(scores.items(),key=lambda z:(-z[1],z[0])):
        record_index,source=data['documents'][index];r=data['records'][record_index]
        group=(r.get('parents') or [r['record_id']])[0]
        if group in seen:continue
        seen.add(group);selected.append({'id':r['record_id'],'title':r['title'],'score':score,'kind':'source_window' if source else r['kind']})
        if len(selected)==5:break
    lexwin=None
    if lex:
        index,score=sorted(lex.items(),key=lambda z:(-z[1],z[0]))[0]
        r=data['records'][data['documents'][index][0]]
        lexwin={'id':r['record_id'],'title':r['title'],'score':score}
    rows.append({'query':query,'content_contract_lane':selected,'independent_full_card_lexical_winner':lexwin})
result={'revision':'26eeb0093987ab60313707097acd4e2c93a46de2','input_version':manifest['input_version'],
        'all_13_input_hashes_match':True,'searches':rows,
        'scope':'bounded lexical operation search, not exhaustive field search or applicability evidence'}
(OUT/'astra_bounded_search.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
