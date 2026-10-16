import numpy as np,json
from pathlib import Path
p=Path(__file__).resolve().parent.parent/'data'
# All entries transcribed as printed, including non-Hermitian last-digit discrepancies.
E0=[
[[.246,-.256+.233j,-.024-.011j,-.018+.249j],[-.256-.234j,.488,.016+.034j,.253-.240j],[-.024+.011j,.016-.034j,.005,-.013-.022j],[-.018-.249j,.253+.240j,-.013+.022j,.268]],
[[.266,-.012+.012j,.245+.265j,.002-.238j],[-.012-.012j,.002,-.001-.022j,-.008+.013j],[.245-.265j,0+.022j,.493,-.239-.227j],[.002+.238j,-.008-.013j,-.239+.227j,.233]],
[[.246,.025+.002j,-.233-.257j,.006-.244j],[.025-.002j,.003,-.025-.024j,-.003-.024j],[-.233+.257j,-.025+.024j,.500,.251+.243j],[.006+.244j,-.003+.024j,.251-.243j,.250]],
[[.243,.243-.248j,.012+.003j,.010+.233j],[.243+.248j,.507,.009+.012j,-.242+.251j],[.012-.003j,.009-.012j,.002,.002+.007j],[.010-.233j,-.242-.251j,.002-.007j,.249]]]
E4=[
[[.237,-.120+.264j,-.153-.072j,-.022+.243j],[-.120-.264j,.372,-.004+.208j,.297-.087j],[-.153+.072j,-.004-.208j,.121,-.060-.166j],[-.022-.243j,.297+.087j,-.060+.166j,.273]],
[[.271,-.060+.165j,.284+.132j,.010-.241j],[-.059-.165j,.115,.017-.203j,-.148+.048j],[.284-.132j,.017+.203j,.373,-.098-.265j],[.010+.241j,-.148-.048j,-.098+.265j,.233]],
[[.241,.071-.140j,-.281-.120j,.010-.243j],[.071+.140j,.108,-.012-.208j,.142-.062j],[-.281+.120j,-.012+.208j,.401,.102+.285j],[.010+.243j,.142+.062j,.102-.285j,.251]],
[[.251,.108-.288j,.149+.060j,.002+.241j],[.108+.288j,.405,-.001+.203j,-.291+.101j],[.149-.060j,-.001-.203j,.106,.056+.146j],[.002-.241j,-.291-.101j,.056-.146j,.244]]]
out={}
for name,E in [('theta0',E0),('theta_pi_over_4',E4)]:
 E=np.array(E); H=(E+E.conj().transpose(0,2,1))/2
 np.save(p/f'huang_{name}_printed.npy',E)
 for k,M in enumerate(E): np.savetxt(p/f'huang_{name}_E{k+1}.csv',M,delimiter=',')
 out[name]={'hermiticity_max_abs':float(np.max(abs(E-E.conj().transpose(0,2,1)))),'completeness_operator_norm_after_hermitization':float(np.linalg.norm(H.sum(0)-np.eye(4),2)),'eigenvalues_after_hermitization':np.linalg.eigvalsh(H).tolist(),'traces':np.trace(E,axis1=1,axis2=2).real.tolist(),'completeness_printed_real':(E.sum(0)-np.eye(4)).real.tolist(),'completeness_printed_imag':(E.sum(0)-np.eye(4)).imag.tolist()}
(p/'huang_matrix_diagnostics.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
