#!/usr/bin/env python3
"""Evaluate frozen W17 queries against bounded source-grounded packet systems.

Default run freezes the original ASTRA catalog packet route and an independent
flat lexical BM25 card baseline. No model calls are made. Optional packet adapter
support uses the JSON stdin/stdout contract documented in --help.
"""
from __future__ import annotations
import argparse, hashlib, importlib.util, json, math, os, re, sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
WORK_ROOT = HERE.parents[1]
CORPUS = WORK_ROOT / "outputs/ASTRA_KNOWLEDGE"
BENCHMARK = HERE / "w17_benchmark.json"
PACKET_DIR = HERE / "benchmark_packets"
MAX_BYTES = 6000
MAX_TOKENS = 1500

# The selected retrieval implementation is loaded at runtime, but its ROOT and DB
# are always redirected to the canonical corpus. The default is the preserved
# pre-change baseline copy under this audit directory.
DEFAULT_KNOWLEDGE_SCRIPT = HERE / "baseline/knowledge.py"
knowledge = None
sys.path.insert(0, str(WORK_ROOT / "work/token_count_deps"))
import tiktoken
ENCODER = tiktoken.get_encoding("o200k_base")

def load_knowledge(script_path: Path):
    global knowledge
    spec = importlib.util.spec_from_file_location("astra_selected_knowledge", script_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    module.ROOT = CORPUS
    module.DB = CORPUS / "indexes/knowledge.sqlite3"
    knowledge = module
    return module

def tok_count(text: str) -> int:
    return len(ENCODER.encode(text, disallowed_special=()))

def sha_file(path: Path) -> str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024), b''):
            h.update(block)
    return h.hexdigest()

def corpus_fingerprint(knowledge_script: Path) -> dict:
    # Corpus data and selected retrieval code are fingerprinted separately so
    # baseline versus updated implementations cannot be conflated.
    paths=[CORPUS/'indexes/knowledge.sqlite3', CORPUS/'indexes/chunks.jsonl',
           CORPUS/'indexes/documents.jsonl', CORPUS/'indexes/query_aliases.json'] + sorted((CORPUS/'cards').glob('*.txt'))
    records=[]
    for p in paths:
        rel=p.relative_to(CORPUS).as_posix()
        records.append({'path':rel,'sha256':sha_file(p),'bytes':p.stat().st_size})
    manifest=json.dumps(records,sort_keys=True,separators=(',',':')).encode()
    return {'sha256':hashlib.sha256(manifest).hexdigest(),'file_count':len(records),
            'scope':'corpus card text plus search database and indexes; retrieval implementation is fingerprinted separately',
            'included_corpus_inputs':records,
            'files_index_sha256':sha_file(CORPUS/'indexes/files.jsonl'),
            'retrieval_implementation':{'path':str(knowledge_script),'sha256':sha_file(knowledge_script),
                                        'root_override':str(CORPUS),'database_override':str(CORPUS/'indexes/knowledge.sqlite3')}}

def parse_span(spec: str) -> list[int]:
    out=[]
    for part in spec.split(','):
        part=part.strip()
        if '-' in part:
            a,b=map(int,part.split('-',1)); out.extend(range(a,b+1))
        else: out.append(int(part))
    return out

def source_cards() -> dict[str,dict]:
    cards={}
    for p in sorted((CORPUS/'cards').glob('*.txt')):
        lines=p.read_text(encoding='utf-8').splitlines()
        cid=lines[0].split('|',1)[0].strip()
        cards[cid]={'path':p.relative_to(CORPUS).as_posix(),'lines':lines,'text':p.read_text(encoding='utf-8')}
    return cards
CARDS=source_cards()

def packet_block(card_id: str, lines: list[int], *, kind='passage') -> str:
    card=CARDS[card_id]
    if lines:
        lo,hi=min(lines),max(lines)
        header=f'\n<BLOCK card_id="{card_id}" path="{card["path"]}" lines="{lo}-{hi}" kind="{kind}">\n'
        body=''.join(f'[L{n}] {card["lines"][n-1]}\n' for n in lines)
    else:
        header=f'\n<BLOCK card_id="{card_id}" path="{card["path"]}" kind="{kind}">\n'
        body=card['text']
    return header+body+'</BLOCK>\n'

def fits(text: str) -> bool:
    return len(text.encode('utf-8')) <= MAX_BYTES and tok_count(text) <= MAX_TOKENS

def extract_catalog_blocks(packet: str) -> tuple[list[str],dict[str,str]]:
    # Original packet contains source IDs and paths, but card coverage is counted
    # only for paths that actually resolve to a catalog card.
    blocks=[]; bodies={}
    rx=re.compile(r'<BLOCK\b([^>]*)>\n(.*?)</BLOCK>',re.S)
    for attrs,body in rx.findall(packet):
        pm=re.search(r'path="([^"]+)"',attrs)
        if not pm: continue
        path=pm.group(1)
        blocks.append(path)
        for cid,c in CARDS.items():
            if c['path']==path: bodies[cid]=body
    return blocks,bodies

def catalog_packet(task: dict) -> dict:
    q=task['query']
    # Binary search budget in the original script's own meter. The extra byte
    # constraint is applied after serialization; lower token budgets are retried.
    result=knowledge.packet(q,budget=MAX_TOKENS)
    if fits(result['text']):
        best=result
    else:
        low,high=1,MAX_TOKENS-1;best=None
        while low<=high:
            mid=(low+high)//2
            result=knowledge.packet(q,budget=mid)
            text=result['text']
            if fits(text): best=result; low=mid+1
            else: high=mid-1
    if best is None:
        raise RuntimeError(f'Original catalog header cannot fit both ceilings for {task["id"]}')
    blocks,bodies=extract_catalog_blocks(best['text'])
    return {'text':best['text'],'included_paths':blocks,'included_card_ids':sorted(bodies),
            'card_bodies':bodies,'actual_count_original':best['count'],
            'original_budget_meter':best['budget_meter'],'route':'original_catalog_packet'}

STOP={'the','a','an','of','to','for','in','and','what','how','is','are','does','can','with','on','from','this','that','then','which','it','as','by','or','be','do','not','doesn'}
def terms(text: str) -> list[str]:
    return [x for x in re.findall(r"[a-z0-9]+",text.lower()) if len(x)>1 and x not in STOP]

def build_passages():
    passages=[]
    for cid,c in CARDS.items():
        # Paragraphs preserve source line positions and are the flat corpus units.
        lines=c['lines']; start=1; current=[]
        for no,line in enumerate(lines+[""],1):
            if line.strip():
                if not current: start=no
                current.append((no,line))
            elif current:
                passages.append({'card_id':cid,'line_numbers':[n for n,_ in current],
                                 'raw':' '.join(x for _,x in current),
                                 'lines':current})
                current=[]
    return passages
PASSAGES=build_passages()

def bm25_scores(query: str):
    qterms=set(terms(query))
    docs=[set(terms(p['raw'])) for p in PASSAGES]
    df=Counter(t for d in docs for t in d)
    avgdl=sum(len(d) for d in docs)/max(1,len(docs)); N=len(docs); k1=1.5; b=.75
    scores=[]
    for p,d in zip(PASSAGES,docs):
        dl=len(d); score=0.0
        freq=Counter(terms(p['raw']))
        for t in qterms:
            f=freq[t]
            if not f: continue
            idf=math.log(1+(N-df[t]+.5)/(df[t]+.5))
            score+=idf*(f*(k1+1))/(f+k1*(1-b+b*dl/max(avgdl,1)))
        scores.append(score)
    return sorted(zip(scores,PASSAGES),key=lambda z:(-z[0],z[1]['card_id'],min(z[1]['line_numbers'])))

def bm25_packet(task: dict) -> dict:
    q=task['query']
    header=f'ASTRA FLAT LEXICAL BM25 PACKET | query={q} | budget_meter=o200k_base\nClaims remain source-scoped. Retrieved passages retain source card and line numbers.\n'
    trailer='\nEnd of packet.\n'
    text=header+trailer
    chosen=[]; seen=set()
    ranked=bm25_scores(q)
    for score,p in ranked:
        key=(p['card_id'],tuple(p['line_numbers']))
        if not score or key in seen: continue
        seen.add(key)
        block=packet_block(p['card_id'],p['line_numbers'])
        if fits(header+''.join(chosen)+block+trailer):
            chosen.append(block)
    text=header+''.join(chosen)+trailer
    covered={}
    for score,p in ranked:
        # Only source lines represented in selected packet blocks count.
        marker=f'card_id="{p["card_id"]}" path="{CARDS[p["card_id"]]["path"]}" lines="{min(p["line_numbers"])}-{max(p["line_numbers"])}"'
        if marker in text:
            covered.setdefault(p['card_id'],set()).update(p['line_numbers'])
    return {'text':text,'included_paths':[CARDS[cid]['path'] for cid in sorted(covered)],
            'included_card_ids':sorted(covered),'covered_lines':{k:sorted(v) for k,v in covered.items()},
            'route':'flat_lexical_bm25'}

def exact_span_eval(task: dict, packet: dict) -> dict:
    ids=set(packet.get('included_card_ids',[])); card_hits=0; span_hits=0; span_total=0; details=[]
    for gold in task['mandatory']:
        cid=gold['card_id']; span=gold['span']; path=span['path']; nums=parse_span(span['lines'])
        card_present=cid in ids
        card_hits+=int(card_present)
        span_total+=1
        if 'covered_lines' in packet:
            covered=set(packet['covered_lines'].get(cid,[]))
            full=card_present and all(n in covered for n in nums)
        else:
            body=packet.get('card_bodies',{}).get(cid)
            # Strict line-span test: require the full contiguous source excerpt,
            # including blank lines, to occur in this card's own packet block.
            source=CARDS[cid]['lines']
            # Each annotated group is assessed independently; the compact JSON
            # comma syntax can contain disjoint ranges.
            groups=[]
            for part in span['lines'].split(','):
                part=part.strip()
                a,b=(map(int,part.split('-',1)) if '-' in part else (int(part),int(part)))
                groups.append('\n'.join(source[a-1:b]))
            full=card_present and body is not None and all(g in body for g in groups)
        span_hits+=int(full)
        details.append({'card_id':cid,'card_retrieved':card_present,'annotated_span':span['lines'],
                        'full_span_covered':bool(full),'span_metric_status':'strict_line_content'})
    total=len(task['mandatory'])
    return {'mandatory_cards_retrieved':card_hits,'mandatory_cards_total':total,
            'mandatory_card_recall':card_hits/total if total else None,
            'full_spans_covered':span_hits,'full_spans_total':span_total,
            'full_span_recall':span_hits/span_total if span_total else None,'details':details}

def save_packet(system: str, task_id: str, text: str):
    d=PACKET_DIR/system; d.mkdir(parents=True,exist_ok=True)
    p=d/f'{task_id}.txt'; p.write_text(text,encoding='utf-8')
    return p.relative_to(HERE).as_posix()

def evaluate_route(system: str, tasks: list[dict], fn):
    records=[]; card_num=card_den=span_num=span_den=0
    for task in tasks:
        packet=fn(task); text=packet['text']; by=len(text.encode('utf-8')); tk=tok_count(text)
        assert by<=MAX_BYTES and tk<=MAX_TOKENS, (system,task['id'],by,tk)
        m=exact_span_eval(task,packet)
        card_num+=m['mandatory_cards_retrieved']; card_den+=m['mandatory_cards_total']
        span_num+=m['full_spans_covered']; span_den+=m['full_spans_total']
        records.append({'task_id':task['id'],'query':task['query'],'route':packet['route'],
                        'packet_path':save_packet(system,task['id'],text),
                        'packet_sha256':hashlib.sha256(text.encode()).hexdigest(),
                        'packet_bytes':by,'packet_tokens_o200k_base':tk,
                        'limits':{'max_bytes':MAX_BYTES,'max_tokens':MAX_TOKENS,'compliant':True},
                        'included_card_ids':packet['included_card_ids'],
                        'coverage':m})
    rates=[r['coverage']['mandatory_card_recall'] for r in records]
    return {'system':system,'per_query':records,
            'macro_mandatory_card_recall':sum(rates)/len(rates) if rates else None,
            'micro_mandatory_card_recall':card_num/card_den if card_den else None,
            'macro_full_span_recall':sum(r['coverage']['full_span_recall'] for r in records)/len(records) if records else None,
            'micro_full_span_recall':span_num/span_den if span_den else None,
            'mean_packet_bytes':sum(r['packet_bytes'] for r in records)/len(records) if records else None,
            'mean_packet_tokens_o200k_base':sum(r['packet_tokens_o200k_base'] for r in records)/len(records) if records else None,
            'all_packets_within_both_limits':all(r['limits']['compliant'] for r in records)}

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output',default=str(HERE/'baseline_results.json'))
    ap.add_argument('--knowledge-script',default=str(DEFAULT_KNOWLEDGE_SCRIPT),help='Retrieval script to run against the canonical corpus; defaults to the frozen pre-change baseline copy.')
    ap.add_argument('--system',choices=['baseline_script','flat_bm25','enhanced_script','bundle','all'],default='all')
    ap.add_argument('--expected-benchmark-sha256',default='4a08b020aa1d9455efc0eccae2f9be3705008832c0093407e20cdec2418ebd35')
    ap.add_argument('--adapter',help='Optional enhanced packet adapter module:function. It receives JSON on stdin: {tasks:[{id,query}],max_bytes,max_tokens}; returns {packets:{ID:{text,included_card_ids,covered_lines}}}. Adapter results print to stdout and packets are written under benchmark_packets/<adapter-name>/; this never changes the frozen benchmark or baseline results unless --output is explicitly changed.')
    a=ap.parse_args()
    knowledge_path=Path(a.knowledge_script).resolve()
    load_knowledge(knowledge_path)
    benchmark_hash=sha_file(BENCHMARK)
    if benchmark_hash!=a.expected_benchmark_sha256:
        raise SystemExit(f'Frozen benchmark hash mismatch: {benchmark_hash}')
    bench=json.loads(BENCHMARK.read_text())
    tasks=bench['tasks']
    result={'benchmark_id':bench['benchmark_id'],'benchmark_sha256':benchmark_hash,
            'corpus':corpus_fingerprint(knowledge_path),'evaluator_sha256':sha_file(Path(__file__).resolve()),
            'run_provenance':'pre-change baseline implementation' if sha_file(knowledge_path)=='7c8258fc879938dfefab9d1aff20d9aff6878163cf26c9a8424ebb6c691f0ee9' else 'selected implementation; not the frozen original baseline',
            'protocol':{'byte_limit':MAX_BYTES,'token_limit':MAX_TOKENS,'tokenizer':'o200k_base',
                        'tokenizer_package':'tiktoken 0.14.0','exact_serialized_packet_includes_header_trailer':True,
                        'model_calls':0,'source_mutation':False},
            'systems':[]}
    if not a.adapter:
        if a.system in ('all','baseline_script'):
            result['systems'].append(evaluate_route('baseline_script',tasks,catalog_packet))
        if a.system in ('all','flat_bm25'):
            result['systems'].append(evaluate_route('flat_bm25',tasks,bm25_packet))
        if a.system in ('enhanced_script','bundle'):
            raise SystemExit('--system enhanced_script|bundle requires --adapter module:function')
        out=Path(a.output);out.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
        print(json.dumps({'output':str(out),'benchmark_sha256':benchmark_hash,
                          'systems':[{k:v for k,v in s.items() if k!='per_query'} for s in result['systems']]},indent=2))
    else:
        if a.system not in ('enhanced_script','bundle'):
            raise SystemExit('--adapter is intended for --system enhanced_script or --system bundle')
        modname,funcname=a.adapter.split(':',1)
        modspec=importlib.util.spec_from_file_location('w17_external_packet_adapter',Path(modname).resolve())
        mod=importlib.util.module_from_spec(modspec);modspec.loader.exec_module(mod)
        fn=getattr(mod,funcname)
        payload=fn({'tasks':[{'id':t['id'],'query':t['query']} for t in tasks],
                    'max_bytes':MAX_BYTES,'max_tokens':MAX_TOKENS})
        packets=payload['packets']; adapter_name=Path(modname).stem
        adapter_result=evaluate_route(a.system,tasks,lambda t:dict(packets[t['id']],route=a.system))
        print(json.dumps({'benchmark_sha256':benchmark_hash,'corpus':result['corpus'],
                          'protocol':result['protocol'],'system':adapter_result},indent=2))

if __name__=='__main__': main()
