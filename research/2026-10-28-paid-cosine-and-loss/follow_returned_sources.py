"""Target-known owner source use through actual returned navigation, misses retained."""
from pathlib import Path
import json
from knowledge.retrieve import Library

here=Path(__file__).resolve().parent
data=json.loads((here/'evaluation/CURRENT_FULL.json').read_bytes())
library=Library();rows=[]
for row in data['results']:
    case=row['case'];target=case['target'];selected=None
    for method in ('agent','structured','content'):
        response=next(m for m in row['methods']if m['method']==method)
        for rank,hit in enumerate(response['results'],1):
            if hit['id']==target:
                selected=dict(method=method,rank=rank,selection='primary',action=hit['next']['packet']);break
            for alternate_rank,alternate in enumerate(hit.get('within_family',[]),1):
                if alternate.get('next')==['packet',target]:
                    selected=dict(method=method,rank=rank,selection='within_family',alternate_rank=alternate_rank,action=alternate['next']);break
            if selected:break
        if selected:break
    if not selected:
        rows.append(dict(case_id=case['id'],target=target,status='target_not_reached_in_returned_top5_or_alternatives',source_read=None))
        continue
    assert selected['action']==['packet',target]
    packet=library.packet([selected['action'][1]],max_bytes=65536)
    record=library.resolve(selected['action'][1]);passages=[]
    for index,ref in enumerate(record['evidence']):
        value=library.source(selected['action'][1],index,max_bytes=65536)
        assert value['source']['path']==ref['path']and value['source']['sha256']==ref['sha256']
        assert ref['quote']in value['text']
        passages.append(dict(action=['source',selected['action'][1],'--evidence',str(index)],**value))
    rows.append(dict(case_id=case['id'],target=target,status='actual_returned_packet_and_all_governing_passages_read',navigation=selected,
        packet_bytes=len(json.dumps(packet,ensure_ascii=False).encode()),contract=record['contract'],reviews=record['review_overlays'],passages=passages))
out=dict(exposure=data['exposure'],input_version=data['input_version'],scope='Target-known source-informed owner navigation,not unassisted or held-out. Inspect complete saved passages and qualifications; route reachability is not a scientific acceptance decision.',results=rows)
(here/'evaluation/SOURCE_USE.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print([(r['case_id'],r['status'],r.get('navigation'))for r in rows])
