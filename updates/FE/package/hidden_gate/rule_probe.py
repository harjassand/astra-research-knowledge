"""Strong structure-aware comparator and off-class hidden-gate falsification.
Learning guarantee requires a constant-one or single-parent monotone gate promise.
That promise is stated explicitly; the perturbation deliberately violates it.
"""
from pathlib import Path
ROOT = Path(__file__).resolve().parent
from probe import *
from certify import *


def learn_parent_rule(model,oracle):
    n=model['L']-1
    lookup={(int(i),int(d)):e for e,(i,d) in enumerate(zip(model['a'],model['dims']))}
    parent={};queries=[];answers=[]
    def ask(x,i):
        e=lookup[(int(x),i)];a=float(oracle(e));queries.append(e);answers.append(a)
        return a
    for i in range(n+1):
        a=ask(0,i)
        if a==1.:
            parent[i]=None;continue
        candidates=[j for j in range(n) if j!=i]
        while len(candidates)>1:
            left=candidates[:len(candidates)//2]
            x=sum(1<<j for j in left)
            if ask(x,i)==1.:candidates=left
            else:candidates=candidates[len(candidates)//2:]
        parent[i]=candidates[0]
    return parent,queries,answers

def predicted_fac(model,parent):
    return np.array([1. if parent[int(i)] is None or (int(x)>>parent[int(i)])&1 else model['softness'] for x,i in zip(model['a'],model['dims'])])

if __name__=='__main__':
    out=[]
    for q,eps in [(.05,1e-6),(.005,1e-12)]:
        model=soft_east(10,q,eps);st=time.perf_counter()
        parent,queries,ans=learn_parent_rule(model,lambda e:model['fac'][e])
        learned=predicted_fac(model,parent)
        assert np.array_equal(learned,model['fac'])
        v=spsolve(matrix(model,model['base']*learned),model['m'])
        l,u,d,_=certify_field(model,learned,v)
        record={'L':10,'q':q,'softness':eps,'queries':len(queries),'unique_queries':len(set(queries)),
                'query_indices':queries,'predicted_facilitations_match_all_fixture_edges':True,
                'lower_conditional_on_single_parent_promise':outward(l,True),
                'upper_conditional_on_single_parent_promise':outward(u,False),
                'seconds_including_rational_validation':time.perf_counter()-st}
        # Select a deliberately adversarial, unqueried shortcut using full reference info.
        # This is a falsification fixture, not an independent benchmark or learner input.
        K=inv(matrix(model,model['base']*learned).toarray(),check_finite=False)
        uu,vv,rr=edge_values(K,model['m'],model['a'],model['b'])
        delta=model['base']*(1-learned)
        benefit=delta*vv**2/(1+delta*rr)
        benefit[queries]=-np.inf;e=int(np.argmax(benefit))
        pert=model.copy();pert['fac']=learned.copy();pert['fac'][e]=1.
        pp,qq,aa=learn_parent_rule(pert,lambda k:pert['fac'][k])
        assert qq==queries and aa==ans and pp==parent
        vp=spsolve(matrix(pert,pert['base']*pert['fac']),pert['m'])
        pl,pu,pd,_=certify_field(pert,pert['fac'],vp)
        record['off_class_hidden_shortcut']={'edge':e,'state':int(model['a'][e]),'flip_dimension':int(model['dims'][e]),
                  'selected_adversarially_after_learning':True,'all_learning_answers_unchanged':True,
                  'true_lower':outward(pl,True),'true_upper':outward(pu,False),
                  'unperturbed_over_perturbed_ratio_lower':outward(l/pu,True)}
        # Run the broader-envelope acquisition operation on that modified model.
        rrn=run(pert,'relative',refresh=32);cert=certify_run(pert,rrn)
        record['off_class_hidden_shortcut']['robust_queries']=rrn['queries']
        record['off_class_hidden_shortcut']['shortcut_was_queried']=e in rrn['selected_edges']
        record['off_class_hidden_shortcut']['robust_interval']=[cert['certified_lower'],cert['certified_upper']]
        record['off_class_hidden_shortcut']['robust_ratio']=cert['certified_upper_lower_ratio']
        out.append(record)
        print({k:v for k,v in record.items() if k!='query_indices'},flush=True)
    json.dump(out,open(str(ROOT / 'rule_learning_results.json'),'w'),indent=2)
