"""Equally informed full-teacher trie on the ALREADY DECLARED T8 source.

No producer geometry/projection/source sampler or optimizer is imported/run.
This ordinary exponential-size competitor is useful at this short horizon.
"""
from pathlib import Path
import time,json

HERE=Path(__file__).resolve().parent


class SameTeacher:
    def __init__(self,T):self.T=T;self.calls=0;self.locked=False
    def _mass(self,h):
        ones=sum(h);n=len(h)
        p=.41*.18**ones*.82**(n-ones)+.59*.72**ones*.28**(n-ones)
        half=self.T//2
        if n<=half:r=2.**(-n)
        else:r=2.**(-half) if h[half:]==h[:n-half] else 0.
        return .98*p+.02*r
    def next(self,h):
        if self.locked:raise RuntimeError('teacher unavailable after compilation')
        self.calls+=1
        p=self._mass(h+(0,))/self._mass(h)
        return p,1-p


def compile_trie(teacher,T):
    rows={};front=[()]
    for _ in range(T):
        children=[]
        for h in front:
            rows[h]=teacher.next(h)
            children.extend([h+(0,),h+(1,)])
        front=children
    return rows


def evaluate(rows,T):
    masses={():1.}
    for t in range(T):
        for h in [w for w in masses if len(w)==t]:
            for o in (0,1):masses[h+(o,)]=masses[h]*rows[h][o]
    return {h:p for h,p in masses.items() if len(h)==T}


def main():
    T=json.loads((HERE/'ENGINEERING_PROTOCOL.json').read_text())['source']['T']
    teacher=SameTeacher(T)
    started=time.perf_counter();rows=compile_trie(teacher,T);compilation=time.perf_counter()-started
    teacher.locked=True;before=teacher.calls
    started=time.perf_counter();law=evaluate(rows,T);inference=time.perf_counter()-started
    assert teacher.calls==before==2**T-1
    # Source-known validation is OUTSIDE the learner/compiler.
    truth={h:.41*.18**sum(h)*.82**(T-sum(h))+.59*.72**sum(h)*.28**(T-sum(h)) for h in law}
    tv=sum(abs(law[h]-truth[h]) for h in law)/2
    import math
    kl=sum(truth[h]*math.log(truth[h]/law[h]) for h in law)
    record={'status':'same-input ordinary full-teacher trie; floating diagnostic',
            'T':T,'teacher_compilation_next_calls':before,'teacher_inference_calls':teacher.calls-before,
            'P_samples_required':0,'stored_categorical_rows':len(rows),
            'compilation_seconds':compilation,'exhaustive_inference_seconds':inference,
            'TV':tv,'KL_P_to_trie':kl,'law_sum':sum(law.values()),
            'scaling':'O(O^T) queries/storage, so not a polynomial general-rank compiler',
            'conclusion':'ordinary trie beats proposed engineering compiler at this SAME finite input; no practical advantage',
            'law':[{'word':list(h),'probability':p} for h,p in law.items()]}
    (HERE/'ORDINARY_TRIE.json').write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps({k:v for k,v in record.items() if k!='law'},indent=2))


if __name__=='__main__':main()
