"""Conventional exact abstraction inference on an Astra scientific interface.
The inference functions consume only observation labels and transition tables.
Known representation predicates are used only after inference, for adjudication.
"""
from pathlib import Path
from itertools import product, permutations
import hashlib, importlib.util, json, resource, sys, time

HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'inputs/max/Astra_Amplification_Cycle9_MAX_20261022/evaluator/meta_representation/source/src/active_ports.py'

def partition(observation, transition):
    def labels(items):
        ids={}; out=[]
        for x in items:
            if x not in ids: ids[x]=len(ids)
            out.append(ids[x])
        return out
    cls=labels(observation); history=[len(set(cls))]
    while True:
        nxt=labels([(observation[i],tuple(cls[j] if j>=0 else -1 for j in row)) for i,row in enumerate(transition)])
        history.append(len(set(nxt)))
        if nxt==cls:return cls,history
        cls=nxt

def safety_simulation(observation, transition):
    n=len(observation)
    relation={(s,t) for s in range(n) for t in range(n) if observation[s]==observation[t]}
    history=[len(relation)]
    while True:
        bad=[]
        for s,t in relation:
            for ss,tt in zip(transition[s],transition[t]):
                if tt>=0 and (ss<0 or (ss,tt) not in relation):
                    bad.append((s,t));break
        if not bad:return relation,history
        relation.difference_update(bad);history.append(len(relation))

def main():
    resource.setrlimit(resource.RLIMIT_CPU,(90,90))
    resource.setrlimit(resource.RLIMIT_AS,(512*1024**2,512*1024**2))
    t0=time.perf_counter(); c0=time.process_time()
    spec=importlib.util.spec_from_file_location('native_count_oracle',SOURCE)
    native=importlib.util.module_from_spec(spec);spec.loader.exec_module(native)
    ports=[]
    for a in range(4):
        for n in product(range(4),repeat=4):
            if not 1<=sum(n)<=3:continue
            for f in range(16):
                if native.valid_port(a,n,f):ports.append((a,n,f))
    sat=(-1,None,0); ports.append(sat); index={p:i for i,p in enumerate(ports)}
    commands=[('extend',c) for c in range(4)]+[('merge',j) for j in range(len(ports)-1)]+[('permute',p) for p in permutations(range(4))]
    def project(a,n,f):return sat if sum(n)==4 else (a,n,f)
    def step(s,cmd):
        a,n,f=s;kind,arg=cmd
        if kind=='permute':
            if n is None:return sat
            nn=[0]*4;ff=0
            for c in range(4):
                nn[arg[c]]=n[c]
                if f>>c&1:ff|=1<<arg[c]
            return (arg[a],tuple(nn),ff)
        if n is None:return None
        if kind=='merge':
            b,m,g=ports[arg]
            if a!=b:return None
            z=native.merge(n,f,m,g)
            return None if z is None else project(a,z[0],z[1])
        # Fill the untouched right port with a valid fixed port; the native
        # extension only acts on the left port and cannot inspect the dummy.
        dummy=(0,(0,1,0,0),0)
        full=(a,dummy[0],n,f,dummy[1],dummy[2])
        z=native.extend(full,'L',arg)
        return None if z is None else (z[0],z[2],z[3])
    transition=[]
    for s in ports:
        row=[]
        for cmd in commands:
            t=step(s,cmd);row.append(-1 if t is None else index[t])
        transition.append(row)
    table_seconds=time.process_time()-c0
    cases={}; learned={}
    for query in ['native_safety','exact_count_query']:
        obs=[('SAT4',) if n is None else ((a,sum(n)) if query=='native_safety' else (a,sum(n),n)) for a,n,f in ports]
        begin=time.process_time()
        cls,ch=partition(obs,transition); rel,rh=safety_simulation(obs,transition)
        cases[query]={'observed_classes':len(set(obs)),'congruence_classes':len(set(cls)),
                      'simulation_pairs':len(rel),'refinement_history':ch,'simulation_history':rh,
                      'cpu_seconds':time.process_time()-begin}
        learned[query]={'classes':cls,'simulation_pairs':sorted(rel)}
    # The historical predicates enter only here, AFTER both inference runs.
    def mask(n):return sum(1<<i for i,x in enumerate(n) if x)
    def expected(s,t,query):
        a,n,f=s;b,m,g=t
        if n is None or m is None:return n is None and m is None
        return a==b and sum(n)==sum(m) and (n==m if query=='exact_count_query' else (mask(n)&mask(m))==mask(n)) and (f&g)==f
    for query in cases:
        relation=set(map(tuple,learned[query]['simulation_pairs']));cls=learned[query]['classes']
        mismatch=[];eq_mismatch=[]
        for i,s in enumerate(ports):
            for j,t in enumerate(ports):
                want=expected(s,t,query)
                if ((i,j) in relation)!=want:mismatch.append([i,j])
                if (cls[i]==cls[j]) != (want and expected(t,s,query)):eq_mismatch.append([i,j])
        cases[query]['historical_order_mismatches']=mismatch
        cases[query]['historical_congruence_mismatches']=eq_mismatch
    s=index[(0,(0,2,1,0),0)]; t=index[(0,(0,1,2,0),0)]
    changed={'ports':[s,t],'concrete':[ports[s],ports[t]],'old_classes':[learned['native_safety']['classes'][i] for i in [s,t]],
             'new_classes':[learned['exact_count_query']['classes'][i] for i in [s,t]],
             'color1_neighbor_counts':[ports[i][1][1] for i in [s,t]]}
    result={'scope':'Conventional semantic inference on supplied count-language; not new science or general invention.',
            'source':{'path':str(SOURCE),'sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest()},
            'states':len(ports),'commands':len(commands),'transition_cells':len(ports)*len(commands),
            'table_cpu_seconds':table_seconds,'cases':cases,'query_change_witness':changed,
            'total_cpu_seconds':time.process_time()-c0,'wall_seconds':time.perf_counter()-t0,
            'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            'full_cost_excludes':'Human/model inference, original oracle invention, source retrieval, proof integration.'}
    (HERE/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    (HERE/'LEARNED_TABLES.json').write_text(json.dumps({'ports':ports,'commands':commands,'transitions':transition,'learned':learned},separators=(',',':'))+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
