import openpyxl, pathlib, json, re
root=pathlib.Path(__file__).resolve().parent
folder=root/'figure 05/raw data/Li uptake experiments/Figure 5A'
raw=openpyxl.load_workbook(folder/'raw data.xlsx', read_only=True, data_only=False).active
groups=[]
for row in raw:
    a,c=row[0].value,row[2].value
    if isinstance(a,str): a=a.strip()
    if isinstance(a,str) and a.startswith('Ch'):
        groups.append({'label':a,'label_cell':row[0].coordinate,'means':[]})
    if c=='Mean' and groups and isinstance(row[3].value,(float,int)):
        groups[-1]['means'].append({'Li_cell':row[3].coordinate,'Li':row[3].value,'Na_cell':row[4].coordinate,'Na':row[4].value})
p=openpyxl.load_workbook(folder/'processing.xlsx', read_only=True, data_only=False).active
out={'source':str(folder.relative_to(root)),'groups':groups,'cycles':[]}
for cycle in range(1,11):
    r=cycle*2; item={'cycle':cycle}
    for name,col,formula in [('CC','B','D'),('Pulsed','H','J')]:
        initial=p[f'{col}{r}'].value; final=p[f'{col}{r+1}'].value
        matches=[g for g in groups if re.search(r'\b'+str(cycle)+r'th\b',g['label']) and g['label'].startswith('Ch3' if name=='CC' else 'Ch1')]
        item[name]={'initial_ppm':initial,'final_ppm':final,'delta_ppm':final-initial,'formula_cell':f'{formula}{r+1}','formula':p[f'{formula}{r+1}'].value,'formula_mg_g':(final-initial)*.1/.158,'formula_implied_mg':(final-initial)*.1,'source_groups':matches}
        for g in matches:
            g['mean_Li']=sum(x['Li'] for x in g['means'])/len(g['means'])
            g['mean_Na']=sum(x['Na'] for x in g['means'])/len(g['means'])
    out['cycles'].append(item)
out['summary']={}
for name,mass in [('CC',.1611),('Pulsed',.1588)]:
    vals=[x[name]['formula_mg_g'] for x in out['cycles']]
    out['summary'][name]={'sum_formula_mg_g':sum(vals),'retention_percent':100*vals[-1]/vals[0],'sum_formula_implied_mg':sum(vals)*.158,'sum_per_filename_mass_mg_g':sum(vals)*.158/mass}
out['summary']['ratio_pulse_CC']=out['summary']['Pulsed']['sum_formula_mg_g']/out['summary']['CC']['sum_formula_mg_g']
out['summary']['ratio_per_filename_mass']=out['summary']['Pulsed']['sum_per_filename_mass_mg_g']/out['summary']['CC']['sum_per_filename_mass_mg_g']
out['raw_mean_discrepancies']=[]
for item in out['cycles']:
    for name in ['CC','Pulsed']:
        rec=item[name]
        for g in rec['source_groups']:
            which='final_ppm' if '0,5h' in g['label'] else 'initial_ppm'
            if abs(g['mean_Li']-rec[which])>1e-10:
                out['raw_mean_discrepancies'].append({'cycle':item['cycle'],'mode':name,'processing_field':which,'processing_value':rec[which],'all_available_mean_value':g['mean_Li'],'source':g})
(root/'icp_cycle_reconciliation.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out['summary'],indent=2))
for x in out['cycles']: print(x['cycle'],*[round(x[n]['formula_mg_g'],8) for n in ['CC','Pulsed']])
for g in groups:
    if g['label'].startswith(('Ch1','Ch3')): print(g['label'],[(x['Li_cell'],x['Li']) for x in g['means']],g['mean_Li'])
