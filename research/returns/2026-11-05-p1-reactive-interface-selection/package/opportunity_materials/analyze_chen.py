from pathlib import Path
import re,json
import pandas as pd
p=Path(__file__).parent
rows=[]
# Factual table-only extraction from the original supplement is retained for
# portable reproduction without redistributing the full paper text.
table_source=p/'chen_target_tables.txt'
if not table_source.exists(): table_source=p/'chen_si.txt'
for page in table_source.read_text().split('\f'):
 if 'Table 1. Temperature, XRD intensities' not in page: continue
 target=page.split('Table 1.')[0].strip().splitlines()[-1].strip()
 tbl=page.split('Table 1.')[1].split('Table 2.')[0]
 vals=[]
 for line in tbl.splitlines():
  m=re.search(r'\b(\d{3,4})\s+(\d+(?:\.\d+)?)\s+(\d+(?:\.\d+)?)\s+(\d+(?:\.\d+)?)\s*$',line)
  if m: vals.append(tuple(map(float,m.groups())))
 split=next((i for i in range(1,len(vals)) if vals[i][0]<vals[i-1][0]),len(vals)//2)
 for i,(t,a,b,c) in enumerate(vals):
  rows.append({'target':target,'route':'traditional' if i<split else 'predicted','temperature_c':int(t),'target_intensity_million':a,'residual_intensity_million':b,'xrd_score':c})
df=pd.DataFrame(rows);df.to_csv(p/'chen_extracted_temperature_rows.csv',index=False)
pa=df.pivot_table(index=['target','temperature_c'],columns='route',values='xrd_score').dropna();pa['diff']=pa.predicted-pa.traditional
pa.to_csv(p/'chen_matched_temperatures.csv')
fig=pd.read_csv(p/'chen_fig4c.csv');diff=fig.p_t_score_diff
cross=[]
for target,g in pa.groupby('target'):
 if g['diff'].min() < -.10 and g['diff'].max()>.10:
  cross.append({'target':target,'min_diff':g['diff'].min(),'max_diff':g['diff'].max(),'rows':g.reset_index().to_dict('records')})
summary={'extracted_rows':len(df),'targets':int(df.target.nunique()),'matched_target_temperature_pairs':len(pa),'fig4_predicted_improved_gt10pp':int((diff>.1).sum()),'fig4_similar_10pp':int((diff.abs()<=.1).sum()),'fig4_traditional_improved_gt10pp':int((diff<-.1).sum()),'fig4_mean_diff':diff.mean(),'fig4_median_diff':diff.median(),'matched_improved_gt10pp':int((pa['diff']>.1+1e-8).sum()),'matched_worse_gt10pp':int((pa['diff']<-.1-1e-8).sum()),'matched_similar10pp':int((pa['diff'].abs()<=.1+1e-8).sum()),'matched_mean_diff':pa['diff'].mean(),'crossovers_gt10pp_each_direction':cross}
(p/'chen_reanalysis_summary.json').write_text(json.dumps(summary,indent=2))
print(json.dumps(summary,indent=2))
