"""One matched augmentation of the unchanged frozen ten-vector source span.

Adds only the two new finite-relative-time bilocal sources. No new fugacity
grid, no larger physical depth, no repeated expansion after this test.
"""
from pathlib import Path
import time,json
import numpy as np
from bilocal_time_preview import Physical,ROOT,WORK,OLD
from contact_jet_preview import analyze

def main():
    start=time.monotonic();old=json.loads((OLD/'results/wider_time_projection.json').read_text())
    oldtr=json.loads((OLD/'results/wider_time_trace_inputs.json').read_text())
    oldtr={tuple(round(float(t),12)for t in k.split(',')):v for k,v in oldtr.items()}
    fresh=json.loads((ROOT/'results/bilocal_time_source_inputs.json').read_text())
    values={(x['n']-2,1.,x['right_delta']):(x['C_projected_degree16'],x['C_equal_time'])for x in fresh if x['left_delta']is None}
    oldmats=[next(x for x in old['rows']if x['channel']==channel and x['span']=='wide_five_r')for channel in ('zero_frequency','matched_equal_time')]
    messages=oldmats[0]['messages'];deltas=(.125,.25);physical={};inputs=[]
    def value(p,r,delta):
        key=(p,r,delta)
        if key in values:return values[key]
        edges=(3*r,)if p==0 else(3*r,)+(3.,)*(p-1)+(3.,)
        model=physical.setdefault((p,r),None)
        if model is None:model=physical[p,r]=Physical(p+2,edges=edges)
        before=model.trace_calls
        c8,pieces=model.source_integral(None,delta,8);c16,_=model.source_integral(None,delta,16)
        relative=abs(c16-c8)/max(1.,abs(c16));assert relative<1e-6
        equal=model.source_trace(None,delta,0.)
        row={'p':p,'n':p+2,'old_fugacity':r,'new_delta':delta,'edges':edges,
             'C_projected_degree8':c8,'C_projected_degree16':c16,'C_equal_time':equal,
             'relative_degree8_vs16_difference':relative,'quadrature_pieces':pieces,
             'time_ordered_trace_calls':model.trace_calls-before}
        inputs.append(row);values[key]=(c16,equal)
        print('CROSS',row,'seconds',time.monotonic()-start,flush=True)
        (ROOT/'results/frozen_span_new_inputs.json').write_text(json.dumps(inputs,indent=2)+'\n')
        return values[key]
    matrices=[[],[]];prior=np.load(ROOT/'results/bilocal_time_matrices.npz')
    for channel in range(2):
        sc=[]
        for r,d in messages:
            p=2*d;edges=(3*r*r,)if p==0 else(3*r,)+(3.,)*(p-1)+(3*r,)
            k=tuple(round(t,12)for t in edges)
            raw=oldtr[min(k,k[::-1])][channel]/5**p
            assert raw>0;sc.append(1/np.sqrt(raw))
        newg=prior['G0'if channel==0 else'G1'];newsc=1/np.sqrt(np.diag(newg)[2:])
        for q,label in enumerate(('G','H','M2')):
            m=np.zeros((12,12));m[:10,:10]=oldmats[channel][label]
            newraw=prior[('G0','H0','M20')[q]if channel==0 else('G1','H1','M21')[q]]
            m[10:,10:]=newsc[:,None]*newraw[2:,2:]*newsc[None,:]
            for i,(r,d)in enumerate(messages):
                for j,delta in enumerate(deltas):
                    p=d+q;c=value(p,r,delta)[channel]
                    m[i,10+j]=m[10+j,i]=(-1)**(p+1)*c/5**p*sc[i]*newsc[j]
            matrices[channel].append(m)
    source=json.loads((OLD/'results/spin_projection_preview.json').read_text())
    source=next(x for x in source['rows']if x['beta']==3 and x['angle_samples']==64)
    a5=json.loads((WORK/'sol9_frontier_20261028/thermal/results/a5_preview.json').read_text())
    a5=next(x for x in a5['rows']if x['beta']==3)
    rows=[]
    for channel,name in enumerate(('P0','matched_unprojected')):
        rows.append(analyze([m[:10,:10]for m in matrices[channel]],source,a5,f'{name}_frozen10_control'))
        rows.append(analyze(matrices[channel],source,a5,f'{name}_frozen10_plus2_bilocal'))
    out={'status':'ONE_MATCHED_FROZEN_SPAN_AUGMENTATION_NUMERICAL_PREVIEW',
         'beta':3,'old_messages_unchanged':messages,'new_relative_time_separations':deltas,
         'rows':rows,'new_distinct_three_point_integrals':len(inputs),
         'new_full_Hamiltonian_eigensystems':len(physical),'maximum_new_physical_sites':5,
         'new_time_ordered_trace_calls':sum(x.trace_calls for x in physical.values()),
         'maximum_degree8_vs16_relative_difference':max(x['relative_degree8_vs16_difference']for x in inputs),
         'seconds':time.monotonic()-start,'new_validated_source_acquisition':False,
         'scope':'Frozen ten-vector control preserved exactly; two new temporal sources only. All sectors and Gram cutoffs retained. Quadrature/eigenpair/roundoff not certified; scalar interval unchanged.'}
    np.savez(ROOT/'results/frozen_span_augmented_matrices.npz',G0=matrices[0][0],H0=matrices[0][1],M20=matrices[0][2],G1=matrices[1][0],H1=matrices[1][1],M21=matrices[1][2])
    (ROOT/'results/frozen_span_augmentation.json').write_text(json.dumps(out,indent=2)+'\n')
    for row in rows:print('SUMMARY',row['name'],row['rows'][0],flush=True)

if __name__=='__main__':main()
