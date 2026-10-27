from robust_decision import *
if __name__=='__main__':
 rows=[];tick=time.monotonic()
 for name in ['V0','Vhalf','V1','V1half','V2','V2half','V3']:
  vals=upper_data(name);src=json.loads((SRC/'results/anchors'/f'{name}.json').read_text())
  rec={'name':name,'V':src['parameters']['V'],'upper_polynomial':src['upper_D_polynomial_exact'],'constants':{k:str(v) for k,v in vals.items()}};rows.append(rec)
  (OUT/'GLOBAL_HOPPING_UPPER_ANCHORS.json').write_text(json.dumps(rows,indent=2)+'\n')
 print('all global upper anchors regenerated',time.monotonic()-tick,flush=True)
