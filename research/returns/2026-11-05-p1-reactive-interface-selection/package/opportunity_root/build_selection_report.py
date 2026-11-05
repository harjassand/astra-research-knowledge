"""Build the complete evidence-founded scientific selection record."""
from pathlib import Path
from xml.sax.saxutils import escape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image as PILImage
import matplotlib

ROOT=Path(__file__).resolve().parent
OUT=ROOT.parent/'output'/'selection'
OUT.mkdir(parents=True,exist_ok=True)
F=Path(matplotlib.get_data_path())/'fonts'/'ttf'
for n,f in [('DV','DejaVuSans.ttf'),('DVB','DejaVuSans-Bold.ttf'),('DVI','DejaVuSans-Oblique.ttf')]:
    pdfmetrics.registerFont(TTFont(n,str(F/f)))
pdfmetrics.registerFontFamily('DV',normal='DV',bold='DVB',italic='DVI',boldItalic='DVB')
INK=colors.HexColor('#25374b');TEAL=colors.HexColor('#147d92');MUTED=colors.HexColor('#5b6979')
ss=getSampleStyleSheet()
ss.add(ParagraphStyle(name='B',fontName='DV',fontSize=9.1,leading=13.7,textColor=INK,spaceAfter=8))
ss.add(ParagraphStyle(name='S',parent=ss['B'],fontSize=7.5,leading=10.8,textColor=MUTED,spaceAfter=6))
ss.add(ParagraphStyle(name='H',fontName='DVB',fontSize=20,leading=25,textColor=INK,spaceAfter=13))
ss.add(ParagraphStyle(name='H2',fontName='DVB',fontSize=11.7,leading=16,textColor=TEAL,spaceBefore=8,spaceAfter=6))
ss.add(ParagraphStyle(name='L',parent=ss['B'],fontSize=11.7,leading=17.5,spaceAfter=13))
ss.add(ParagraphStyle(name='C',parent=ss['B'],fontSize=7.8,leading=11.3,spaceAfter=0))
ss.add(ParagraphStyle(name='E',parent=ss['B'],fontSize=10.5,leading=17,leftIndent=12,spaceBefore=5,spaceAfter=10))
story=[]
def p(t,s='B'):story.append(Paragraph(t,ss[s]))
def h(t):p(t,'H2')
def title(n,t):p(f'SCIENTIFIC OPPORTUNITY SELECTION / {n:02d}','S');p(t,'H')
def page():story.append(PageBreak())
def table(rows,widths):
    rr=[[Paragraph(str(x),ss['C']) for x in row] for row in rows]
    t=Table(rr,colWidths=widths,hAlign='LEFT',repeatRows=1)
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#eef4f6')),('VALIGN',(0,0),(-1,-1),'TOP'),('LINEBELOW',(0,0),(-1,0),.7,TEAL),('LINEBELOW',(0,1),(-1,-1),.25,colors.HexColor('#d8e1e6')),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7)]))
    story.append(t);story.append(Spacer(1,8))
def figure(n,cap):
    f=OUT/n
    with PILImage.open(f) as im:w,hh=im.size
    story.append(Image(str(f),width=495,height=495*hh/w));p(cap,'S')

title(1,'From local reaction physics to reliable material construction')
p('Decision record | 5 November 2026','S')
p('<b>Selected question:</b> Can independently determined laws for reactive interfaces be composed to predict and control a complete inorganic powder-synthesis pathway in physical time, including the new interfaces created by reactions, without fitting the new recipe?','L')
p('The initial domain is oxide and phosphate synthesis with competing crystalline products. The intended full consequence is the ability to turn a target phase and material-quality requirements into a tested preparation and heating procedure, with uncertainty and complete production costs. The scientific object is an evolving collection of reacting interfaces, rather than a ranking of stable bulk compounds.')
h('Why this question survives the comparison')
p('Three distinctions survive direct checks. A useful thermodynamic rule has a real failure region after inventory and source-label problems are removed. A stronger precursor selector improves measured endpoints on average, while the better route can reverse with the thermal intervention. The strongest recent kinetic model already makes a substantial advance through correlated transport, but its local physics does not independently set the bulk reaction clock. These comparisons identify a missing constructive operation without treating known kinetic effects as unexplained physics.')
p('This is a judgment about a valuable and testable question. It is <b>not evidence that a finite pairwise closure already exists</b>. That remains the central scientific challenge. A representation of contacts, another transport correction, or a fitted time scale would not satisfy the full target.')
table([['Completed','Status'],['37-reaction audit and 26 original phase-fraction sheets','Reanalysis of measurements with explicit exclusions and sensitivity checks'],['100 matched target-temperature comparisons','Descriptive endpoints under common treatment conditions'],['2026 transport-model audit and conditional clock calculation','Comparison with the strongest relevant kinetic construction'],['1,035-pair ledger and alternative-domain audits','Evidence adequacy checks and rejection of already-explained openings']],[240,255])
p('The reflection-defect theorem, exact four-state separation and finite-record procedures remain preserved at their stated stationary, all-even hidden-CTMC scope. This record makes no alteration to them. No new synthesis experiment, transferable interface law or civilization-changing discovery is claimed here.','S')

page();title(2,'A failure region that survives the representation audit')
p('Szymanski et al. report in-situ diffraction for 37 precursor pairs. I transcribed Table S2 and read the unchanged original workbook: 26 experiments and 1,318 temperature rows. The tested rule chooses the candidate with the largest compositionally unconstrained Gibbs driving force. [1]')
table([['Comparison','Matches','Disagreements'],['All published cases','23 / 37','14'],['Energy margin ≥60 meV/atom','14 / 14','0'],['Energy margin <60 meV/atom','9 / 23','14'],['Observed phase included; source conflict excluded','23 / 33','10'],['Same comparable subset, margin <60','9 / 19','10']],[315,85,95])
p('Three disagreements involve observed phases absent from the ranked stable-phase inventory: Na₂Nb₄O₁₁, LiV₂O₅ and NaₓV₂O₅. An additional NaNO₃-TiO₂ case has conflicting energy labels between Table S2 and the text. I retain the conflict and exclude that case in the conservative comparison. Ten disagreements remain.')
figure('synthesis_evidence.png','Left: this audit of [1]. Right: matched LiMgPO₄ endpoints extracted from [2]. Lines join separate experiments and are visual guides; no per-cell replicate uncertainty is supplied.')
p('The 60 meV boundary was selected on this cohort; energies were evaluated at observed onset temperatures. It is neither an externally validated universal constant nor an onset-time prediction. Free-energy error can also change close rankings. The remaining disagreements do not uniquely identify nucleation, diffusion, geometry or another cause.')
p('The result is a bounded limitation of a useful method, not a claim that 85% of all chemistry is unpredictable. A database extrapolation under an assumed threshold is not an empirical failure rate.','S')

page();title(3,'What the measurements can and cannot identify')
h('Phase identity is more robust than inferred onset')
p('I repeated first-appearance detection on each original sheet at 1%, 2%, 5% and 10% refined weight fraction, requiring two consecutive qualifying observations. This sensitivity diagnostic is distinct from the authors\' full diffraction-pattern detection procedure.')
table([['Threshold','Published first phase included in detected first set'],['1%','26 / 26'],['2%','26 / 26'],['5%','26 / 26'],['10%','24 / 26']],[145,350])
p('At 1-5% the phase identities agree throughout. Onset temperature is less robust: the median span across the four thresholds is 30°C, and one extreme span reaches 460°C because weak early fitted fractions can trigger a low threshold. Normalized weight fractions sum to within 0.002 of unity. These are checks of the published table; they do not create missing replicate errors.')
h('Conditions and uncertainty')
p('The source combines synchrotron Li-Nb-O and Li-Mn-O studies with an in-house stepped-temperature campaign. Heating schedules and scan cadence differ. Temperature is not a common elapsed-time coordinate. Refined fractions are conditional on the fitted phase models; some distinct Li-Mn-O compositions share a diffraction framework and were approximated with nominal formulas. The workbook supplies no independent replicate-derived uncertainty intervals. [1]')
p('Missing candidate phases, source inconsistency, weak onset resolution and residual rank disagreements have different scientific implications. A perfect rate law cannot predict a product excluded from its inventory; a perfect equilibrium calculation need not determine which allowed product first appears.')
h('A second campaign tests a useful constructive endpoint')
p('Chen et al. select precursors using competing-phase thermodynamics. Their reported campaign contains 224 syntheses over 35 targets. I separately analyzed the deposited best-temperature scores and joined the supplementary routes at the same target and temperature. The measured score is target-only fitted diffraction intensity divided by target-plus-residual intensity; it is not a multiphase mass fraction. [2]')
table([['Comparison','Better >10 points','Within 10','Worse >10','Mean gain'],['Best tested temperature per route; 35 targets','15','16','4','15.04 points'],['Same target and temperature; 100 pairs','40','44','16','10.51 points']],[205,75,65,75,75])
p('The 100 comparisons are correlated within targets, selected rather than random, and use rounded scores. They are not independent randomized trials. The headline median gain is 3.62 points. The source prose mentions 20%, but its figure caption and data reproduce 15/16/4 using an absolute 10-point cutoff; this report uses the numeric definition explicitly.','S')

page();title(4,'The thermal intervention changes which route is better')
table([['LiMgPO₄, 8 h treatment','Selected MgO + LiPO₃','Traditional route','Difference'],['800°C','0.70','0.29','+0.41'],['900°C','0.60','0.75','-0.15']],[160,120,120,95])
p('The traditional route uses Li₂CO₃, MgO and NH₄H₂PO₄. All four scores exceed 0.2 and all four target intensities exceed the source detection cutoff. The route advantage changes by 0.56 between temperatures, so this example survives the source\'s low-signal cautions. It is an observed descriptive reversal, not a calibrated significance result: the four cells lack matched synthesis replicates.')
p('The shared preparation includes prolonged milling, drying and eight-hour air annealing without regrinding. The separate reproducibility campaign reports a 7.6-point standard deviation of paired score differences. This background cannot be substituted for four cell-specific error bars. Six targets in the extracted tables exhibit route advantages above +10 points at one temperature and below -10 at another.')
h('What this comparison decides')
p('Thermodynamic precursor selection is genuinely useful and should remain a baseline. Yet a static route ranking cannot stand in for a process law. A target-oriented construction must predict the effect of the heating intervention on competing pathways. The evidence does not select one microscopic explanation of the reversal; that is why fitting this example would not complete the research question.')
h('Coverage and version honesty')
p('The supplement yields 202 numeric route-temperature rows, with 100 matched pairs and two additional traditional-only rows. The raw-XRD workbook contains 219 patterns in 36 sheets, including an extra target and filename ambiguities. Several deposited headline and supplementary scores differ beyond rounding. This audit preserves the sources separately; it does not claim to reconcile all 224 reported syntheses or silently invent missing runs.')
h('Why this is more than a benchmark-selection exercise')
p('The desired response is a material produced under an intervention, not a label attached to a database row. Independent microscopic inputs must determine intermediate phase amounts, timing and usable final output. A model could score well on the deposited endpoints while failing as soon as a heating schedule, particle distribution or precursor combination changes. Those physical changes therefore define the full test.')
p('The original source data, parsed factual target tables, matched rows, code and numerical summaries are preserved in the reproduction archive. This makes both the positive method comparison and the exceptions auditable.','S')

page();title(5,'The strongest kinetic model rules out the easy contribution')
p('Karan et al. already calculate correlated ion transport in liquidlike analogues of candidate Ba-Ti-O products and incorporate it into ReactCA. Their four-stoichiometry comparison improves pathway agreement over simpler thermodynamic and self-diffusion alternatives. Adding correlated diffusion is therefore not the proposed contribution. [3]')
p('Its macroscopic traces are indexed by reaction steps. The construction uses an assumed common particle radius of 0.1 µm and a chemical-system scoring scale chosen to place onset near 1000 K. The supplementary sensitivity calculation shows why that calibration matters:')
table([['Scale s','Maximum timewise BaTiO₃ mole fraction'],['1 × 10¹³','0.392'],['2 × 10¹³','0.534'],['5 × 10¹³, selected','0.932'],['1 × 10¹⁴','0.482']],[240,255])
p('Doubling the selected scale changes the peak fraction by 0.450. These are separate temporal maxima, not final yields or new measurements. The comparison establishes that fitting this parameter changes competitive outcomes as well as clock placement. Supplying another fitted value would not earn predictive construction.')
figure('synthesis_clock.png','Left: source Table S3 in [3]. Right: a conditional shell calculation from the reported coefficient units and assumed particle radius; it is not an observed bulk reaction time or the full simulator\'s prediction.')
p('The physical explanation deserves credit even though absolute time transfer remains unestablished. A model can explain selectivity without independently predicting a useful production schedule. The opportunity is to supply that missing operation, not to declare its transport mechanism false.')

page();title(6,'A concrete opening: earn the clock while creating new interfaces')
p('For a homogeneous, already transport-active layer with constant coefficient, the source\'s idealized shell equation gives an exact conditional result:')
p('dh/dt = K<sub>D</sub>/h;  h²(t) = 2 K<sub>D</sub>t;  t<sub>shell</sub> = r₀²/(2 K<sub>D</sub>).','E')
p('At 1000 K, the reported coefficients and r₀ = 0.1 µm imply shell traversal times from about 30 microseconds to 0.95 milliseconds; BaTiO₃ gives about 41 microseconds. These numbers are algebra, not experimental conversion times. They assume the active layer, geometry and uninterrupted supply that the full powder process must actually generate. They do not establish a contradiction with macroscopic measurements.')
p('This identifies the constructive join: a local transport coefficient must be connected to how much reactive interface exists, which species can reach it, which phases appear there, and what interfaces remain afterward. Predicting conversion and predicting the next available interfaces must be part of the same state update.')
h('The required operation')
p('A reusable local law would take temperature, electrochemical potentials, local composition, geometry and a physically specified interfacial state. It must return species fluxes, phase creation or dissolution rates, and new geometry/state. Bulk assembly joins these laws through shared inventories and chemical-potential fields. The state is adequate only if its law survives changed surroundings and thermal history without being re-estimated for the new recipe.')
p('Standard transport and conservation are starting machinery. Near equilibrium, J = -L∇μ̃ requires a positive-semidefinite dissipative response in conjugate variables, the appropriate reference-frame constraint and electrical conditions. For phase amounts n, stoichiometric matrix S, rates r and elemental-composition map A:')
p('dn/dt = Sr,  AS = 0,  n ≥ 0.','E')
p('These equations enforce bookkeeping; they do not supply the unknown constitutive physics. Nucleation and strongly driven transformations may need more than linear response. Reaction-diffusion and phase-field models already implement coupled physical evolution when adequate constitutive inputs are supplied. They are mandatory comparators. [4,5]')
h('Where invention must earn its value')
p('The missing achievement is a closed, transferable law for interfaces that create or destroy other reactive interfaces. A successful representation may need composition-dependent disorder, wetting, defect populations or nonlocal supply; the evidence does not yet choose these. If a compact state fails, the construction must expose and include the missing physical context. An endpoint classifier or an impossibility theorem about unobserved rates would not earn the manufacturing consequence.')

page();title(7,'The comparison that would decide the full construction')
p('The evidence justifies choosing the unresolved capability. It does not prove the proposed local closure. A random split of endpoint rows would fail to test the central claim of reusable physical composition.')
table([['Test','Fixed','Changed','What success establishes'],['Chemical transfer','Independently determined local laws','Untrained precursor combination or family','Composition beyond fitted recipes'],['Process transfer','Chemistry and calibrated local laws','Ramp, hold, cooling or atmosphere history','Intervention prediction with a clock in seconds'],['Geometry transfer','Chemistry and constitutive parameters','Measured size/contact distribution','Preparation as input rather than fitted rate correction'],['Constructive control','Predictions frozen before synthesis','Model-selected preparation and schedule','Usable target output at stated resources']],[100,130,130,135])
p('Required responses include phase amounts through time, major intermediate identities, appearance and consumption times, unassigned or amorphous material, delivered product quality and full cost. Prediction tolerances must be tied to measurement precision and the intended application before evaluating held-out results.')
h('Equal information for strong alternatives')
p('Thermodynamic route selection, ARROWS³ feedback, transport-augmented ReactCA and a properly parameterized reaction-diffusion/phase-field model should receive the same physical preparation inputs. Extra microscopy, a favorable product inventory or hidden recipe calibration cannot be reserved for the proposed construction. ARROWS³ already reuses experimentally learned pairwise intermediates; experimental feedback is not itself the missing operation. [6]')
p('The first finite construction should replace macroscopic time scaling in the audited Ba-Ti-O system with a unitful assembly, then move to a held-out chemistry and changed process or geometry. The current records establish relevant phenomena and baselines, but do not supply all needed interface measurements. Those constitutive inputs must actually be acquired or calculated; endpoint fitting cannot substitute for them.')
h('What would close or falsify the opportunity')
p('If an equally informed existing model already passes these tests at practical cost, the proposed opening closes and that method should be adopted. If new recipe-specific fits remain necessary, the compositional hypothesis fails in its present form. A successful one-chemistry clock fit is an intermediate check, not the full result. The target remains useful physical construction rather than a theorem restricting observation.')

page();title(8,'Large collections and apparent anomalies: evidence boundaries')
p('The acquired Precursor Genome ledger contains 1,035 distinct unordered pairs of 46 precursors, exactly all pair choices; 1,351 diffraction scans; and 1,950 candidate refinements. This is broad first-contact coverage, but not a kinetic closure experiment. [7]')
table([['Exact ledger audit','Count'],['Actual temperature profiles','981'],['Recorded 60-minute / 240-minute holds','750 / 231'],['Missing hold temperature/time','54'],['Duplicate unordered precursor pairs','0'],['Accepted / rejected / unreviewed refinements','1,161 / 55 / 734'],['Outcome categories','384 transformed; 369 unreacted; 143 completely reacted; 113 partially reacted; 26 unspecified']],[260,235])
p('Temperature differs across pairs. Rescans and alternative refinements are not repeated syntheses. Selected results require the sample\'s active scan index and that scan\'s active case index: 237 records have multiple scans flagged active. Negative mass entries and metadata conflicts require resolution before mass-balance claims. There is no general repeated-pair time/geometry series or higher-order mixture challenge here.')
h('A transport anomaly rejected after checking original uncertainty')
p('A reconstructed mean Onsager matrix from the 2026 spreadsheet was indefinite. The original coefficient archive reports much larger uncertainty for the problematic cross term than its plotted error. An explicit positive-semidefinite matrix satisfying the mass-weighted reference-frame constraint lies within every component\'s archived one-standard-deviation interval. This is interval feasibility, not a joint confidence statement; it is enough to reject the mean-matrix anomaly as evidence selecting a new physical mechanism.')
p('The bounded audit preserves the exact algebra and source comparison. No claim is made that the microscopic mechanism is unphysical. Conjugate-variable consistency, mass conservation and dissipativity remain requirements independently of that noisy estimate.')
h('A withdrawn claim was not used as confirmed evidence')
p('The July 2026 preprint on a transient-liquid origin of reaction onset was withdrawn in August with a coauthor-revision explanation. Its abstract was not treated as independent confirmed measurement evidence; status was checked on the official arXiv record. [8]')
h('Meaning for the selected question')
p('Neither dataset size nor an attractive inconsistency earns the opportunity. The selected question rests on audited constructive limitations and a partial mechanism worth extending, while leaving state completeness and the possibility of transfer open to decisive testing.')

page();title(9,'Rejected openings and the consequence a complete result must earn')
h('Granular memory')
p('The author analysis was reproduced on 147 raw coordinate files, all Git-hash verified, across 27 preparations. With the same SB readout and about 5.1% training amplitude, cycle-three displacements are 0.0010914, 0.0064478 and 0.0115357 box lengths after matched training, orthogonal training and no training, respectively; each group has five preparations. The ratios are 5.91 and 10.57. This rejects amplitude-only memory, but the source already explains learned deformation paths. The collection lacks force/stress histories and rate interventions needed for a new transferable constitutive law. [9]')
h('Electrolyte transport')
p('One matched formulation comparison gives a 68.5% viscosity reduction alongside a 31.7% conductivity reduction. Concentration-corrected inverse-viscosity scaling predicts a conductivity ratio of 2.0004; the observed ratio is 0.68345. The source already measures and explains transport correlations. A stronger irreversible-thermodynamics construction has been tested against concentration and voltage evolution using MRI. This audit found no surviving anomaly against that explanation, and a coefficient is not a demonstrated charging capability. [10,11]')
h('Why the synthesis question remains')
p('It combines a verified predictor limitation, an intervention-dependent material endpoint and a strong partial mechanism that leaves a specific physical assembly operation unearned. That supports effort on a useful question without proving success in advance. Adding ordinary redox or ambipolar coupling would not suffice: those are established transport operations. [12]')
h('The complete consequence and resource boundary')
p('A successful rule would turn independently acquired local knowledge into tested procedures for new assemblies, including useful nonequilibrium phases. This could reduce repeated search in energy, electronic and structural material development. No global energy saving, battery improvement or new material functionality has been demonstrated here.')
p('Costs must include precursor production and purity; milling and drying; geometry characterization; actual furnace energy and heat loss; atmosphere control; cooling; separation, waste and accepted recovery; and model/measurement preparation. Productivity must be measured per mass of accepted functional material, not per inferred fraction of its crystalline component.')
p('The 2026 microscopic protocol itself is substantial: nine compositions × five temperatures × five replicates × 5 ns corresponds to 225 trajectories and 1.125 microseconds of aggregate MD time, alongside a specialized potential trained on 4,628 structures. This arithmetic is not a GPU-hour or monetary estimate. A broad library requires a real scaling and amortization argument.')
p('<b>Earned here:</b> an evidence-founded question, the strongest-method boundary and a concrete transfer criterion. <b>Unearned:</b> the transferable law, a newly constructed procedure or material, and the mission\'s final discovery. Subsequent work should attack the physical construction rather than promote a fitted example into that endpoint.','S')

page();title(10,'Primary sources and reproduction')
refs=[
('1','Szymanski et al. (2024). Quantifying the regime of thermodynamic control for solid-state reactions during ternary metal oxide synthesis. Science Advances. Table S2 and data S1.','https://doi.org/10.1126/sciadv.adp3309'),
('2','Chen et al. (2024). Navigating phase diagram complexity to guide robotic inorganic materials synthesis. Nature Synthesis. Source Fig. 4C and supplementary target tables.','https://doi.org/10.1038/s44160-024-00502-y'),
('3','Karan et al. (2026). Ion correlations explain kinetic selectivity in diffusion-limited solid-state synthesis reactions. Nature Materials. Equations 8-9; SI Table S3; deposited coefficients.','https://doi.org/10.1038/s41563-026-02596-5'),
('4','Gallant et al. (2025). A cellular automaton simulation for predicting phase evolution in solid-state reactions. Chemistry of Materials.','https://doi.org/10.1021/acs.chemmater.4c02301'),
('5','Huang et al. (2023). Phase-field modeling of solid-state metathesis reactions with the charge neutrality constraint. Computational Materials Science.','https://doi.org/10.1016/j.commatsci.2023.112080'),
('6','Szymanski et al. (2023). Autonomous and dynamic precursor selection for solid-state materials synthesis. Nature Communications.','https://doi.org/10.1038/s41467-023-42329-9'),
('7','Walters et al. (2026). The Precursor Genome. Public ledger, experimental metadata and refinement provenance; preprint/data release.','https://zenodo.org/records/21285546'),
('8','Tan et al. (2026). Origin of the reaction temperature in solid-state materials synthesis. Official record marks this preprint withdrawn.','https://arxiv.org/abs/2607.06685'),
('9','Lindeman (2025). Multi-dimensional memory in low-friction granular materials. Soft Matter. Raw data v1.1.','https://doi.org/10.1039/D5SM00470E'),
('10','Bergstrom and McCloskey (2024). Ion Transport in (Localized) High Concentration Electrolytes for Li-Based Batteries. ACS Energy Letters.','https://doi.org/10.1021/acsenergylett.3c01662'),
('11','Wang et al. (2021). Potentiometric MRI of a Superconcentrated Lithium Electrolyte: Testing the Irreversible Thermodynamics Approach. ACS Energy Letters.','https://doi.org/10.1021/acsenergylett.1c01213'),
('12','Bouwmeester, Kruidhof and Burggraaf (1994). Importance of the surface exchange kinetics as rate limiting step in oxygen permeation through mixed-conducting oxides. Solid State Ionics.','https://doi.org/10.1016/0167-2738(94)90145-7')]
for n,t,u in refs:p(f'<b>[{n}]</b> {escape(t)} <link href="{u}" color="#147d92">{u}</link>','S')
p('The archive includes manifests, unchanged numerical inputs, factual source-table extraction, explicit transcription, scripts, derived outputs, figures and bounded evidence audits. Run audit_thermodynamic_control.py, analyze_chen.py, analyze_precursor_genome.py, reproduce_granular.py, compare_measurements.py and audit_onsager_outlier.py from their retained directories.','S')
p('Dependencies: numpy, pandas, scipy, matplotlib and openpyxl; report generation also uses reportlab and Pillow. No raw-diffraction re-refinement, first-principles recalculation, MD rerun, COMSOL rerun or new physical experiment is claimed. Third-party paper texts are referenced rather than needed to regenerate the arithmetic.','S')

def footer(c,d):
    w,hh=d.pagesize;c.saveState();c.setStrokeColor(colors.HexColor('#d9e3e9'));c.line(50,39,w-50,39)
    c.setFillColor(MUTED);c.setFont('DV',7);c.drawString(50,26,'Evidence-founded question selection | 5 November 2026');c.drawRightString(w-50,26,str(d.page));c.restoreState()
doc=SimpleDocTemplate(str(OUT/'reactive_interface_selection.pdf'),pagesize=(595.276,841.89),rightMargin=50,leftMargin=50,topMargin=42,bottomMargin=51,title='Evidence-founded selection: predictive composition of reactive interfaces',author='Research collaboration')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print(OUT/'reactive_interface_selection.pdf')
