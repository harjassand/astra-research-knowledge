#!/usr/bin/env python3
"""Exact static ledger checks, no scalar solve or numerical parameter search."""
from fractions import Fraction as F
from pathlib import Path
import hashlib,json,ast
ROOT=Path(__file__).resolve().parent
checks=0
def check(ok,label):
 global checks
 assert ok,label
 checks+=1
p=6;max_steps=128+3*64
check(max_steps==320,'annulus step ceiling')
startup_dense=2*sum(k*k+(2*k-1)**2 for k in range(1,29))+2*(29**2+57**2)
check(startup_dense==82128,'startup dense arithmetic count')
check(startup_dense+10000<100000,'startup remaining arithmetic reserve')
per_step=(2*p*p+5*p+4)+(2*p*p+8*p+14)+(2*p+3)
check(per_step==255,'literal interval counts')
pass_upper=100000+4*per_step*max_steps+200*max_steps+20000
check(pass_upper<600000,'one pass bound')
check(3*600000+3*10000<2000000,'all three passes and three receiver runs')
W=8192;B=2000000;overhead=10**18
bundle=256*(W+1)**3
cost=B*bundle+overhead
check(cost==282578068509184000000,'full bit budget')
check(cost<3*10**20,'rounded cost upper')
check(3*10**20<2*10**21-1,'narrow literal-enumerator comparison')
check(10**9*2**28+2**38+10**15<10**18,'control storage hash parse total')
check(4096*8192+2**25+2**24<2**27,'storage live-bank buffers margin')
# Conservative coefficient/Horner numerator/denominator arithmetic.
D112_bound=3*112+7*112
check(D112_bound==1120,'factorial denominator elementary bound')
check((3+D112_bound)+(112+21)<1280,'coefficient bits')
check((3+D112_bound+112)+(112+25)+16<1536,'Horner and barrier bits')
check(1536+80<2048,'ceilq input product')
check(2048+10<4096,'cumulative local-width auxiliary counter')
for name in ('coarse_clock.py','independent_coarse_verify.py','coarse_windows.py','run_cold.py'):
 ast.parse((ROOT/name).read_text());check((ROOT/name).stat().st_size<2**16,('program bytes',name))
cert=json.loads((ROOT/'COARSE_CERTIFICATE.json').read_text())
verify=json.loads((ROOT/'INDEPENDENT_COARSE_CHECK.json').read_text())
check(cert['steps']<=max_steps,'observed exact step count')
check(F(cert['total_width'])<F(1,100000),'computed scalar tolerance')
check(cert['integer_interval_operations']=={'add':315*106,'mul':315*134,'div':315*15},'constructor count formula')
check(verify['integer_interval_operations']==cert['integer_interval_operations'],'different implementation counts')
check(len(verify['mathematical_fields_exactly_rebuilt'])==23,'different verification fields')
for name in ('COARSE_CERTIFICATE.json','INDEPENDENT_COARSE_CHECK.json','COARSE_WINDOWS.json'):
 check((ROOT/name).stat().st_size<2**16,('output byte ceiling',name))
manifest=json.loads((ROOT/'COLD_SOURCE_BINDINGS.json').read_text())
check(len(manifest['files'])<=64,'source count cap')
workspace=ROOT.parent.parent
for row in manifest['files']:
 data=(workspace/row['path']).read_bytes()
 check(hashlib.sha256(data).hexdigest()==row['sha256'],('source binding',row['path']))
check(sum(row['bytes'] for row in manifest['files'])<2**20,'source byte cap')
oldpath=workspace/'clearance_window_receiver_20261101/ACQUISITION_COST_SUMMARY.json'
old=json.loads(oldpath.read_text())
check(old['total_three_acquisition_reserves']==str(3*10**27),'old acquisition reserve retained')
check(old['separate_receiver_reserve']==str(10**24),'old receiver reserve retained')
check(old['separate_completed_loader_repair_regression_reserve']==str(10**24),'old regression reserve retained')
result={'status':'PASS_EXACT_STATIC_LEDGER_CHECKS_AUTHOR_PENDING_INDEPENDENT_COST_REVIEW','checks':checks,
 'scalar_passes':3,'static_maximum_steps_per_pass':max_steps,'arithmetic_bundle_ceiling':B,
 'work_word_bits':W,'bundle_bit_cost':str(bundle),'control_io_storage_bit_reserve':str(overhead),
 'full_bit_cost_upper_exact':str(cost),'rounded_prospective_bit_cost_upper':str(3*10**20),
 'storage_bits_upper':2**27,'new_scientific_precision':cert['total_width_decimal_upper'],
 'old_acquisition_ledger_sha256':hashlib.sha256(oldpath.read_bytes()).hexdigest(),
 'limitations':['reference Python wall time is not bounded','old historical reserves unchanged','fixed two-fixture source-specific algorithm','no advantage over non-enumerative retained/validated predictors']}
(ROOT/'STATIC_COST_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
