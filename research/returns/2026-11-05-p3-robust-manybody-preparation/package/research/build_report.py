"""Build the robust many-body preparation report; full proofs and checks accompany it."""
from pathlib import Path
import hashlib, html, json, sys, re
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image, Table, TableStyle
)
from PIL import Image as PILImage
from matplotlib.mathtext import math_to_image
import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["mathtext.fontset"] = "dejavuserif"
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent
OUT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT.parent / "deliverables"
OUT.mkdir(exist_ok=True)
TMP = ROOT / "equations"
TMP.mkdir(exist_ok=True)
FIG = ROOT / "figures"
FIG.mkdir(exist_ok=True)
FONT = Path("/usr/share/fonts/truetype/dejavu")
for name, filename in (
    ("DSerif", "DejaVuSerif.ttf"), ("DSerif-Bold", "DejaVuSerif-Bold.ttf"),
    ("DSans", "DejaVuSans.ttf"), ("DSans-Bold", "DejaVuSans-Bold.ttf"),
):
    pdfmetrics.registerFont(TTFont(name, str(FONT / filename)))
for family in ("DSerif", "DSans"):
    pdfmetrics.registerFontFamily(
        family, normal=family, bold=family+"-Bold",
        italic=family, boldItalic=family+"-Bold"
    )
INK = colors.HexColor("#172D3D")
TEAL = colors.HexColor("#247A82")
MUTED = colors.HexColor("#586973")
PALE = colors.HexColor("#EDF4F5")
WIDTH = A4[0] - 96
styles = {
    "body": ParagraphStyle("body", fontName="DSerif", fontSize=10.3,
                           leading=15.4, spaceAfter=8, textColor=INK),
    "small": ParagraphStyle("small", fontName="DSerif", fontSize=9.1,
                            leading=13.2, spaceAfter=6, textColor=INK),
    "caption": ParagraphStyle("caption", fontName="DSans", fontSize=8.6,
                              leading=12, spaceAfter=8, textColor=MUTED),
    "h1": ParagraphStyle("h1", fontName="DSans-Bold", fontSize=18.5,
                         leading=24, spaceAfter=14, textColor=INK),
    "h2": ParagraphStyle("h2", fontName="DSans-Bold", fontSize=11.7,
                         leading=15.7, spaceBefore=8, spaceAfter=7, textColor=TEAL),
    "title": ParagraphStyle("title", fontName="DSans-Bold", fontSize=27,
                            leading=33, spaceAfter=18, textColor=INK),
    "label": ParagraphStyle("label", fontName="DSans-Bold", fontSize=9,
                            leading=13, spaceAfter=12, textColor=TEAL),
    "table": ParagraphStyle("table", fontName="DSerif", fontSize=8.8,
                            leading=12.5, spaceAfter=0, textColor=INK),
}
story, plain = [], []
def p(text, style="body"):
    rendered = text.replace("⁻¹ᐟ²", "<super>−1/2</super>").replace("¹ᐟ²", "<super>1/2</super>")
    for symbol in ("ℓ", "≼"):
        rendered = rendered.replace(symbol, '<font name="DSans">'+symbol+'</font>')
    story.append(Paragraph(rendered, styles[style]))
    plain.append(text)
def h(text):
    p(text, "h2")
def page(title):
    if story:
        story.append(PageBreak())
    p(title, "h1")
def eq(tex, fontsize=13):
    tex = " ".join(tex.split())
    tex = re.sub(r"\\le(?![A-Za-z])", r"\\leq", tex)
    tex = re.sub(r"\\ge(?![A-Za-z])", r"\\geq", tex)
    tex = re.sub(r"\\ne(?![A-Za-z])", r"\\neq", tex)
    def fractions(s):
        result, i = "", 0
        while i < len(s):
            if s[i] == "{" and (i == 0 or s[i-1] != "\\"):
                j, depth = i+1, 1
                while j < len(s) and depth:
                    if s[j] == "{" and s[j-1] != "\\": depth += 1
                    if s[j] == "}" and s[j-1] != "\\": depth -= 1
                    j += 1
                inside = fractions(s[i+1:j-1])
                k, level, split = 0, 0, None
                while k < len(inside):
                    if inside[k] == "{" and (k == 0 or inside[k-1] != "\\"): level += 1
                    if inside[k] == "}" and (k == 0 or inside[k-1] != "\\"): level -= 1
                    if level == 0 and inside.startswith("\\over", k) and (k+5 == len(inside) or not inside[k+5].isalpha()): split = k; break
                    k += 1
                if split is not None:
                    inside = "\\frac{"+inside[:split]+"}{"+inside[split+5:]+"}"
                result += "{"+inside+"}"
                i = j
            else:
                result += s[i]
                i += 1
        return result
    tex = fractions(tex)
    tex = re.sub(r"\\mathbb\s+([A-Za-z])", r"\\mathbb{\1}", tex)
    tex = re.sub(r"\\(mathcal|overline|mathbf)\s+([A-Za-z])", r"\\\1{\2}", tex)
    tex = re.sub(r"\\sqrt([0-9])", r"\\sqrt{\1}", tex)
    tex = tex.replace(r"\mathbf1", r"\mathbf{1}")
    tex = re.sub(r"\\frac([0-9])([0-9])", r"\\frac{\1}{\2}", tex)
    tex = re.sub(r"\}([0-9])", r"}{\1}", tex)
    key = hashlib.sha256((str(fontsize)+tex).encode()).hexdigest()[:15]
    f = TMP / (key + ".png")
    if not f.exists():
        math_to_image("$" + tex + "$", str(f), dpi=240,
                      format="png", color="#172D3D")
    with PILImage.open(f) as im:
        w, ht = im.size
    width = min(WIDTH, w * fontsize / 10 * 72 / 240)
    image = Image(str(f), width=width, height=ht*width/w)
    image.hAlign = "CENTER"
    story.extend([Spacer(1, 3), image, Spacer(1, 10)])
    plain.append("MATH: " + tex)
def table(rows, widths):
    data = [[Paragraph(c, styles["table"]) for c in row] for row in rows]
    t = Table(data, colWidths=widths, hAlign="LEFT", repeatRows=1)
    t.setStyle(TableStyle([
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("BACKGROUND", (0,0), (-1,0), PALE),
        ("LINEBELOW", (0,0), (-1,0), .7, TEAL),
        ("LINEBELOW", (0,1), (-1,-1), .3, colors.HexColor("#D8E0E4")),
        ("LEFTPADDING", (0,0), (-1,-1), 7),
        ("RIGHTPADDING", (0,0), (-1,-1), 7),
        ("TOPPADDING", (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
    ]))
    story.extend([t, Spacer(1, 9)])
    plain.extend(" | ".join(row) for row in rows)
def link(url, label):
    return '<link href="%s" color="#247A82">%s</link>' % (
        html.escape(url, quote=True), html.escape(label)
    )

def figure(path, maxheight=340, caption=None):
    with PILImage.open(path) as im:
        iw, ih = im.size
    scale = min(WIDTH / iw, maxheight / ih)
    pic = Image(str(path), width=iw*scale, height=ih*scale)
    pic.hAlign = "CENTER"
    story.extend([Spacer(1, 5), pic, Spacer(1, 7)])
    if caption:
        p(caption, "caption")

def theorem(label, text):
    p("<b>" + label + ".</b> " + text)

# The artifact-operation marker was run once before this file was authored.

p("ASTRA RESEARCH / CONSTRUCTIVE RESOLUTION / 5 NOVEMBER 2026", "label")
p("Thermal quantum states through imperfect apparatus", "title")
p("A uniform local-noise preimage theorem for one-dimensional Gibbs states at every fixed positive temperature", "h2")
p("<b>Completed consequence.</b> Every bounded-range one-dimensional qubit Gibbs family at fixed finite inverse temperature admits a constructive ensemble of bounded contiguous blocks with a uniform positive spectral floor. A nonzero amount of independent local output noise can therefore be precompensated, uniformly in system size. The accepted noisy Bell/tree boundary compiler turns this representation into unencoded global-state preparation to arbitrary accuracy at fixed component noise in its stated Pauli apparatus model.")
eq(r"\rho_\beta=\mathbb{E}_{\mu}\bigotimes_{A\in\mathcal{P}_{\mu}}\tau_{\mu,A},\qquad |A|\leq B,\qquad \tau_{\mu,A}\succeq \eta I_A/2^{|A|}")
p("B and η depend on temperature and interaction range, not chain length or requested accuracy. The proof modifies a recent pure-block Gibbs preparation theorem, preserves its classical sampling mechanism, and removes the rank-deficient factors that obstruct noisy delivery.")
p("<b>Scientific status.</b> This report gives the derivation, independent mathematical audit, compatible physical composition, a sharp attained two-qubit boundary, and executable finite checks. It is a research construction, not a peer-reviewed priority determination or experimental result.")
p("<b>Resource status.</b> The sufficient constants are prohibitive. Paid protected control, routing, acquisition and reset remain. No total-energy, space-time or practical threshold advantage is established. Ordinary active preparation may use the same new theorem.")
p("The companion research archive contains the complete technical notes, code, check results and the preceding accepted noisy-interface archive unchanged.","small")

page("1. The selected question and its consequence")
p("The previous register operation established that noisy apparatus can prepare a positive preimage of a target syndrome law. Its useful lesson is task dependence: a known mixed state can absorb a specified final noise channel if its positive input state can be prepared. The selected question is whether this extends to interacting quantum states with noncommuting Hamiltonians and entangled targets, while retaining arbitrary global output accuracy.")
table([
 ["Layer", "Completed result"],
 ["Structural theorem", "All fixed-temperature finite-range 1D Gibbs states have uniformly full-rank bounded-block ensembles."],
 ["Mathematical consequence", "Every sufficiently weak product of local CPTP channels has a positive constructive preimage, with a size-independent radius."],
 ["Physical operation", "The acquired product-Pauli boundary and protected controller deliver the specified state to arbitrary global trace accuracy at fixed primitive noise."],
 ["Sharp limitation", "The exact optimal residual error for a Heisenberg dimer under compulsory local depolarization is computed and attained."],
], [126,WIDTH-126])
p("A full resolution needs positivity, constructive sampling, and physical noisy delivery. Those are separate operations in this report. The first two are new mathematical consequences of the modified representation; the third uses the already earned interface at its actual scope.")
p("The new endpoint is a digitally specified quantum state at a scheduled release time. Global trace accuracy controls all later measurement probabilities by data processing. Further storage and noisy computation have their own costs and models.")
p("The earlier memory, passive bath, unknown-reference input/output, intrinsic passive-time coupling, syndrome-prefix, repair, burst, productive-control and first-event results remain at their accepted scopes. This construction does not extend passive holding to noncommuting target Hamiltonians or turn a mixed Gibbs state into a chosen purification.")

page("2. Theorem and thermal-specific inputs")
p("Let H=Σⱼhⱼ act on an N-qubit chain or ring. Each term has support on at most r consecutive sites and operator norm at most one, with one term per starting position. Bounded multiplicity is absorbed into the strength normalization. Fix finite β≥0 and r. Terms may be noncommuting and spatially inhomogeneous.")
eq(r"\rho_\beta(H)=e^{-\beta H}/\operatorname{Tr}(e^{-\beta H})")
theorem("Uniformly mixed block theorem", "There are computable B(β,r)&lt;∞ and η(β,r)&gt;0 such that the cover-page ensemble exists for every N. Blocks are contiguous, each normalized block has the stated spectral floor, and prescriptions can be sampled to any global trace accuracy in polynomial time in N and inverse accuracy at fixed β,r, in the source's numerical-input convention.")
p("Pilatowsky-Cameo, Styliaris, Bakshi and Malz already proved a pure bounded-block decomposition and polynomial classical sampler [1]. Bakshi, Choi and Pilatowsky-Cameo supply its local invertible dressing construction [2]. These are primary inputs. The new proof retains full rank through the superblock decomposition and stops before a pure-state refinement.")
eq(r"\rho_\beta\ \propto\ M\left[\sum_\nu w_\nu\bigotimes_jG_j^{(\nu)}\right]M^\dagger")
p("The positive elementary matrices Gⱼ have uniformly bounded conditioning at fixed β,r. M is a product of local invertible dressings with bounded norm and inverse norm. Each elementary block has a midpoint product-cut operator satisfying G′ⱼ≼Gⱼ≼exp(7m)G′ⱼ. No dressing crosses a selected midpoint cut. The first-stage label law includes its required trace weight.")
p("These are the only thermal-specific inputs to the central new algebra. The complete inherited first-stage cost remains polynomial(N,1/ε); only the final finite-state chain sampling phase is linear in chain length at fixed physical parameters. No near-linear cost is assigned to the full classical source.")

page("3. Preserve positive slack at the spectral step")
p("The original cut decomposition can lose rank by subtracting the entire cut operator and by resolving a remainder with sharp projectors. Halve the cut operator instead:")
eq(r"F_j=G'_j/2,\qquad a=e^{-7m}/2,\qquad \Delta_j=G_j-F_j")
eq(r"aG_j\preceq F_j\preceq G_j/2,\qquad G_j/2\preceq\Delta_j\preceq(1-a)G_j")
p("Now Aⱼ=Gⱼ⁻¹ᐟ²ΔⱼGⱼ⁻¹ᐟ² has eigenvalues in [1/2,1−a]. Choose a rank-one orthogonal spectral resolution with eigenvalues λⱼₜ and projectors Pⱼₜ. Let dⱼ be its dimension, s=a/2, and λ̄ⱼ its mean eigenvalue.")
eq(r"Q_{j,t}=(1-s)P_{j,t}+sI/d_j,\qquad b_{j,t}=\frac{\lambda_{j,t}-s\overline{\lambda}_j}{1-s}")
eq(r"\sum_tQ_{j,t}=I,\quad\sum_tb_{j,t}Q_{j,t}=A_j,\quad 0\leq b_{j,t}\leq1-a/2")
p("The equalities follow by collecting spectral coefficients and identity terms. The bounds follow from the admitted eigenvalue interval. Any orthonormal basis in a degenerate eigenspace works. Define")
eq(r"E_{j,t}=G_j^{1/2}Q_{j,t}G_j^{1/2}\succeq(s/d_j)G_j")
eq(r"\sum_tE_{j,t}=G_j,\qquad\sum_tb_{j,t}E_{j,t}=\Delta_j")
p("Every factor is full rank, yet its scalar remainder coefficient is uniformly below one. This exact replacement for the sharp spectral factors is the central new operation. A fixed sufficiently long superblock makes the residual central perturbation small enough to resolve with mixed product states.")

page("4. Resolve the exceptional term with mixed states")
p("For a superblock of L elementary blocks labelled 0,...,L−1, use the exact first-cut expansion:")
eq(r"\bigotimes_jG_j=\sum_{b=1}^{L-1}\left(\bigotimes_{j<b}\Delta_j\right)\otimes F_b\otimes\left(\bigotimes_{j>b}G_j\right)+R+\bigotimes_j\Delta_j",11)
eq(r"R=F_0\otimes\bigotimes_{j>0}G_j")
p("Each summand outside the final pair has a product cut and strictly positive factors. Substituting the softened identities into that pair leaves factors Eⱼₜ and a central factor F₀¹ᐟ²(I+Kₜ)F₀¹ᐟ², where")
eq(r"K_{\mathbf t}=\left(\prod_{j>0}b_{j,t_j}\right)F_0^{-1/2}\Delta_0F_0^{-1/2},\qquad\|K_{\mathbf t}\|\leq a^{-1}e^{-a(L-1)/2}")
p("Choose L so this norm is at most 8⁻ᵐ/4, leaving numerical slack. Expand K=ΣPαPP. Set u=1/2, c=1+αI, and wP=|αP|u to the power minus the Pauli weight. Since the sum of those inverse powers is 7ᵏ≤8ᵐ, the nonidentity weights sum to at most 1/4.")
eq(r"I+K=\left(c-\sum_{P\ne I}w_P\right)I+\sum_{P\ne I}w_P\left[I+\operatorname{sgn}(\alpha_P)u^{\mathrm{wt}(P)}P\right]")
p("Each bracket has a positive parity mixture of products of (I±uPᵢ)/2. Choose signs uniformly with the desired full parity; all proper sign products vanish. Every local factor has minimum eigenvalue 1/4. Identity slots are maximally mixed. The central congruence preserves the midpoint cut. Thus every superblock has a selected product cut, with full-rank factors on both sides.")
p("This is an exact positive ensemble. It requires neither negative sampling weights nor application of a nonphysical inverse channel to unknown data.")

page("5. Geometry, explicit constants and spectral floor")
p("Use the source's arbitrary anchor positions with gaps in [m₀,2m₀] and put m=2m₀. No local dressing crosses a midpoint cut. Merge an incomplete final superblock into its predecessor. B=4mL safely bounds the final contiguous block sizes after dressing.")
eq(r"m_0=\left\lceil\exp\left[r\max(1,\beta)(2240)^{2r}\right]\right\rceil,\qquad m=2m_0")
eq(r"L=\left\lceil1+\frac{2}{a}\left[\log(4/a)+m\log8\right]\right\rceil,\qquad B=4mL")
p("Increase m₀ for parity rounding. The conservative finite-volume bound Λ=exp[2r max(1,β)m₀] controls both local dressing norms and inverse norms. Let")
eq(r"\kappa_g=64^me^{2\beta m},\qquad K_0=2^{m+1}\kappa_g/s")
p("The condition numbers of G, Δ, softened E and central mixed factors are at most K₀. Each dressing congruence contributes at most Λ⁴. At most B factors and dressings occur in one final block. Normalization yields the uniform floor with")
eq(r"\eta=\min\left\{(K_0\Lambda^4)^{-B},\ e^{-2\beta B}\right\}>0")
p("The second term handles a chain shorter than B directly. To handle open boundaries through the ring theorem, add a mathematical buffer of 2B maximally mixed noninteracting sites and trace it out. No length-B block bridges that buffer; partial trace preserves the normalized floor. No dummy output qubits need be physically emitted.")
p("The displayed constants are existence bounds. At r=2 and β=1, the exponent defining m₀ is already about 5.0×10¹³. The later superblock and noise-radius bounds are still worse. They do not imply a useful block size or physical noise threshold.")

page("6. Sampling and finite precision")
p("For every first-stage label ν, the modified decomposition sums exactly to the original product of Gⱼ. Its first-stage law is unchanged. The new superblock alphabet is finite at fixed β,r. Each final dressed block depends on two neighboring labels, so its trace weight factors along a finite-state chain. The source's forward-backward algorithm applies; stop before its final pure-state refinement.")
h("No extensive conditioning loss")
p("Let Tₛ be the exact positive sum for superblock s. Compute positive, cut-preserving approximants satisfying")
eq(r"(1-\zeta)T_s\preceq\widetilde T_s\preceq(1+\zeta)T_s")
p("Local dimensions and spectral floors are fixed. Use a residual-controlled orthonormal diagonalization, clip eigenvalues to the admitted interval, and construct softened Q explicitly. The central expansion has strict slack; tiny nonnegative scalar weights may be dropped within the local operator budget. The added matrix precision is O(log(1/ζ)) plus fixed β,r-dependent constants.")
p("Tensoring multiplies the Loewner factors; congruence by the global M preserves their order exactly. Trace normalization gives O(Nζ) error even when M is globally ill-conditioned. Choose ζ=O(ε/N). Positive normalized edge factors allow rescaled transfer arithmetic. The local floors can retain η/2.")
h("The inherited numerical-input convention")
p("The first-stage source sampler uses truncated quasilocal terms, weighted sampling and backtracking. Its actual polynomial is charged as Pβ,r(N,1/ε,input description). The source papers do not state a separate tight bit-complexity theorem for every inherited oracle; this report does not invent one. The new bounded-matrix precision analysis is explicit, and the original source polynomial remains an input.")
p("Prepare the inverse of each actual finite-accuracy block. Its forward image is that same sampled block. One need not approximate the exact global inverse state, and no global inverse norm amplifies the original sampler error.")
h("A literal finite-bit fallback")
p("Physical existence also has a direct fallback. The exact preimage has minimum eigenvalue at least (η/4)<super>N</super>. Compute the full digital Gibbs matrix and tensor inverse to error below ε and a fraction of this floor, paying the inverse norm in precision. This takes exponential matrix/synthesis work and O(N log(4/η)+βN+log(1/ε)) bits at fixed δ. The same noisy controller and acquired boundary implement it. Thus existence does not require an exact-real sampling oracle; this fallback gives no efficient-resource claim.","small")

page("7. Uniform local-noise preimages")
p("Let Λᵢ be arbitrary single-site CPTP maps with full diamond distance ‖Λᵢ−id‖≤δ&lt;1. This mathematical result allows heterogeneous, nonunital and non-Pauli channels. Their inverses exist by the Neumann series and preserve trace and Hermiticity. Tensor telescoping gives")
eq(r"\|\Lambda_i^{-1}\|_\diamond\leq(1-\delta)^{-1},\qquad\|\Lambda_A^{-1}-\mathrm{id}\|_\diamond\leq(1-\delta)^{-|A|}-1")
p("For a block τA the operator-norm displacement is bounded by the same quantity, while its minimum eigenvalue is at least η/2<super>|A|</super>. Therefore")
eq(r"\delta\leq\delta_0:=1-\left(1+\frac{\eta}{2^{B+1}}\right)^{-1/B}")
eq(r"\sigma_{\mu,A}=\Lambda_A^{-1}(\tau_{\mu,A})\succeq\frac{\eta}{2}\frac{I_A}{2^{|A|}},\qquad\operatorname{Tr}\sigma_{\mu,A}=1")
p("Averaging the positive tensor products with the same ensemble weights gives an exact global preimage:")
eq(r"\sigma_\beta=\mathbb{E}_{\mu}\bigotimes_A\sigma_{\mu,A},\qquad\left(\bigotimes_i\Lambda_i\right)(\sigma_\beta)=\rho_\beta")
p("The global Gibbs minimum eigenvalue may vanish exponentially with N; the admitted local-noise radius does not. This is a family-wide many-body interior theorem. It does not assert that Λ⁻¹ is a physical channel on arbitrary inputs. Its output is a computed known positive state to be prepared.")
p("For finite sampled blocks with floor η/2, replace 2 to the power B+1 in the radius by 2 to the power B+2. This leaves inverse floor η/4. Require the actual endpoints to have half this radius, and acquire physical channel estimates within the full radius. The margin covers numerical state synthesis.")
p("The forward map restores each actual sampled leaf. Delivered approximation error is inherited from the original mixture. Approximating the exact global inverse state is neither necessary nor asserted.")

page("8. The physical model and complete operation")
p("The completed apparatus route retains the accepted homogeneous stationary independent Pauli model: each outgoing primitive wire has the same unknown Pauli channel, independently in space and time. Native gates, preparation, reset, idle, measurement and capture templates are specified, without additional independently unknown SPAM maps. The same noisy code protects mutable classical computation. Nonlocal links, routing, cooling, ancillas and occupied time remain paid resources.")
p("The accepted Bell/tree compiler exports any protected known-state circuit through acquired independent product Pauli channels Kᵢ, up to arbitrarily small execution and history-coupling error. Their strengths are O(p) uniformly in circuit size. Fine Bell and tree records are discarded; pre-existing references and retained external records keep the earned guarantee.")
table([
 ["Stage", "Actual work"],
 ["Commission", "Noisy opposite-sign idle contrasts; protected acquisition/simulation of explicit endpoint templates."],
 ["Sample", "Protected computation of mixed-block labels and matrices; finite arithmetic and physical random-bit generation."],
 ["Prepare", "Bounded-block inverse matrices; actual noisy ancillas, synthesis, protected conditional scheduling and routing."],
 ["Export", "Bell/tree delivery at a common prescribed time, retaining the compulsory terminal physical noise."],
 ["Reset / reuse", "Paid erasure or discard of fresh ensemble labels and garbage; every new preparation and exposure counted."],
], [83,WIDTH-83])
p("Choose p below the accepted controller threshold and the new radius divided by twice its endpoint constant. This nonzero threshold depends on β,r and the fixed compiler, not N or ε. It may be catastrophically small.")
p("H is a supplied digital target. No target Hamiltonian fabrication, isolatable check couplers or Davies bath is needed. This does not identify an unknown material or supply noncommuting passive holding. The general-channel mathematical radius does not itself extend the physical compiler to arbitrary noise.")

page("9. Error budget and a usable delivered state")
p("For acquired endpoints K̂ᵢ and actual sampled blocks τ̃A, prepare σ̂A=K̂A⁻¹(τ̃A). These are valid positive matrices. Forward-channel telescoping gives")
eq(r"D\left(K(\widehat\sigma),\widehat K(\widehat\sigma)\right)\leq\frac12\sum_i\|K_i-\widehat K_i\|_\diamond")
p("D denotes half trace norm. No global inverse factor multiplies the calibration error. The full budget is")
eq(r"D(\rho_{\rm out},\rho_\beta)\leq\epsilon_{\rm source}+\epsilon_{\rm numeric}+\epsilon_{\rm exec}+\epsilon_{\rm tree}+\epsilon_{\rm cal}+\epsilon_{\rm fail}+\epsilon_H")
p("Each term can be made arbitrarily small at fixed physical p. Statistical precision increases trial counts; it does not require reducing the component fault probability. Effective channel uncertainty acts on an ordinary prepared state.")
h("Target description and physical acquisition are distinct")
eq(r"D\left(\rho_\beta(H),\rho_\beta(\widehat H)\right)\leq\beta\|H-\widehat H\|\leq\beta N\xi")
p("Here ξ bounds each local-term error. Differentiate the normalized Gibbs operator and use Schatten Hölder on the Duhamel integral. Thus O(log(N/ε)) coefficient bits suffice at fixed β, provided they are supplied or acquired. Both target and approximate Hamiltonian must obey the declared norm bound, enlarged by any known approximation margin.")
h("Records and repeated use")
p("Fresh ensemble labels are erased, or their actual correlated extension is declared. Conditional on a label, the state is generally a different block-product state. Retained calibration records are compatible with a uniform confidence-set bound and charged failure probability. The target is a known Gibbs state, not a prescribed purification or an unknown-input identity channel.")
p("Fresh calls with errors εⱼ compose with total error at most Σεⱼ, including adaptive digital targets within fixed uniform parameters. Every reset, preparation, routing operation and occupied location is charged. The delivered global trace bound controls every subsequent CPTP use; further holding or processing requires its own implementation.")

page("10. Resource accounting and unfavorable constants")
p("The bill includes the actual source polynomial, bounded-block matrix work exponential in B, state synthesis, protection, output regeneration, metrology and disposal. A safe block purification circuit has a 4 to the power B factor times precision work. These constants remain even when β,r are formally fixed.")
p("For 2N ternary control roots, α=21s&lt;1 and inherited raw-pool error q_c, take")
eq(r"h=\max\left(0,\left\lceil\frac{\log(2Nq_c/\epsilon_{\rm tree})}{\log(1/\alpha)}\right\rceil\right),\qquad N_{\rm leaves}=2N3^h")
p("This is of order N(N/ε) to the power κ, κ=log3/log(1/α). It is polynomial in inverse accuracy and additional to ordinary protection overhead. For protected circuit size V, the recursion pℓ₊₁≤apℓ² uses ℓ=O(log log(V/εexec)); physical locations include V times g to the power ℓ for the actual gadget constant g. The inherited conservative base already has 2047 physical qubits per logical qubit.")
p("With Gmax stochastic locations per endpoint template, acquiring the primitive law to O(εcal/(NGmax)) costs O((NGmax/εcal)² log(1/εfail)) noisy trials plus protected capture. Conservatively acquiring N distinct endpoint laws needs O(N³εcal⁻² log(N/εfail)) simulated samples times their actual template costs. Identical templates may share calibration. The special direct-assay result later in this report is not substituted into this general bill.")
eq(r"E_{\rm total}=E_{\rm fabrication}+E_{\rm acquisition}+E_{\rm control}+E_{\rm gates}+E_{\rm routing}+E_{\rm reset}+E_{\rm cooling}+E_{\rm idle}",11)
p("Space-time integrates all occupied quantum and controller registers over physical time. Fabrication, reset heat, refrigeration, communication duration and acquisition are real costs. No platform values are supplied from which to calculate a numerical advantage. Erasure bounds concern conditional entropy, not an assigned energy for every syntactic reset.")
p("The theorem establishes a fixed noise radius in N and ε. Its displayed bounds do not give a practical architecture or threshold. The same resources and the same new theorem are available to the strongest ordinary active-preparation comparator.")

page("11. An exact attained entangled-state boundary")
eq(r"H=\frac{XX+YY+ZZ}{3},\qquad\rho_\beta=\frac{I-t(XX+YY+ZZ)}4,\qquad t=\frac{e^{4\beta/3}-1}{e^{4\beta/3}+3}",11)
p("Let both compulsory final channels be depolarizers with Bloch contraction λ. A Werner input with parameter u becomes one with parameter λ²u, and its positivity range is −1/3≤u≤1. Thus exact delivery is possible precisely when t≤λ²; the attaining input has u=t/λ².")
eq(r"\inf_{\sigma}D\left[(\mathcal D_\lambda\otimes\mathcal D_\lambda)(\sigma),\rho_\beta\right]=\frac34(t-\lambda^2)_+")
p("To prove optimality over every input, twirl it by U⊗U. This fixes the target, commutes with depolarization and cannot increase trace distance. Minimizing over Werner inputs gives 3|t−λ²u|/4. A singlet input attains the residual floor if t&gt;λ². At λ=0 the sole output is maximally mixed.")
p("The target is entangled for t&gt;1/3, so λ²&gt;1/3 gives a nonempty entangled interval with exact positive precompensation. At λ=0.8 this is 0.823959&lt;β≤1.569926. λ is an endpoint parameter; this is not a claim that the full compiler tolerates 20 percent primitive error.")
p("For fixed λ&lt;1, t tends to one as β grows. Sufficiently cold dimers are unreachable even with arbitrary input preparation, cooling and computation before these compulsory terminal channels. A better algorithm cannot remove that range obstruction. Physical preparation of the attaining input is still paid through an actual entangling factory or the accepted compiler.")
p("A single spin with H=−hZ similarly requires λ≥tanh(βh). Bounded local strength and fixed temperature are therefore substantive for a uniform family threshold. One-dimensionality is used in our proof; it is not claimed to be a universal impossibility boundary for higher-dimensional families.")

page("12. Broad deductions and record-sensitive scope")
h("A thermodynamic interior")
p("Fix one compatible family of local channels on the infinite chain within the uniform radius. Along any finite-volume Gibbs sequence with a local limit, positive preimages have a weak-star subsequential limit. Local tensor channels commute with that limit. The limiting thermal state is therefore in the image of the infinite product channel. The result survives increasing volume without using the global smallest eigenvalue.")
h("Remote heralding preserves a local floor")
p("For the exact Gibbs representation choose depolarizers with replacement probability γ within the radius. Any nonzero-probability outcome of a measurement on the complement of a retained set A leaves")
eq(r"\rho_{A\mid y}\succeq\gamma^{|A|}I_A/2^{|A|}")
p("The complement instrument induces a positive conditional input on A. The remaining product channel has an all-sites-replaced term of weight γ to the power |A|. This proves the floor even for rare outcomes. For an approximately delivered state, conditioning additionally costs at most 2ε/q when the target outcome probability q&gt;ε. No uniform implemented floor for arbitrarily rare postselection is claimed. Nor is priority over existing Gibbs local-comparability results claimed.")
h("Known targets do not remove unknown-input limits")
p("This operation chooses a positive known state before noise so its output is a selected mixed target. It does not reverse noise on arbitrary reference-entangled inputs. The predecessor's raw-port floor stands unchanged. A canonical TFD is also a different target: its specified purification is not supplied by discarding the ensemble records.")
h("The capability belongs to compatible controllers generally")
p("An ordinary active fault-tolerant processor may use the same inverse-block ensemble and independent boundary. An autonomous controller may do so when its initialization, acquisition and output interfaces are bridged. The new theorem expands their available tasks; it does not establish a proprietary protocol advantage or total-resource separation.")

page("13. The strongest existing methods")
table([
 ["Method", "Established operation", "Relation to this result"],
 ["Pre-compensation [3]", "Known-channel inverse states and SDP optimization, including entangled targets.", "Uniform many-body positivity and constructive input ensembles are the added content."],
 ["1D constant-depth source [1]", "All fixed-temperature pure bounded-block mixtures and polynomial classical sampling.", "Direct source; the new full-rank modification supplies noise margin."],
 ["Quantum DS sampler [4]", "All finite-temperature 1D mixing; N polylog(N/ε) ideal gates and classical work at fixed bounded parameters.", "Stronger ideal runtime. Hamiltonian stability does not cancel uncontrolled output noise."],
 ["FT I/O and qLDPC [5,6]", "Controlled noisy boundaries; constant quantum-space-overhead state preparation with residual local-stochastic output noise.", "Internal protection is available; general residual noise is not automatically independent product noise."],
 ["Autonomous 2D v3 [7]", "Dissipative QCA with noisy controller repair and universal encoded computation.", "A different physical dynamics and output model; a valid controller alternative with earned interfaces."],
], [110,195,WIDTH-305])
p("All comparators receive the same cooling, gates, routing, acquisition, switching and input access. They may use the new theorem. Our classical source has worse stated N,ε dependence than the strongest ideal quantum sampler. No exclusive hardware, time, energy or space-time advantage follows.","small")

page("14. Further comparisons and changed restrictions")
p("Ding, Li and Zhang's all-temperature system-bath algorithm [8] gives roughly N/ε expected Hamiltonian evolution time with Θ(N) resettable bath ancillas. Its coupling and approximation depend on requested accuracy. The evolution-time metric does not include all calibration, resets and uncontrolled apparatus-noise costs.")
p("Brunner et al. [9] genuinely analyze noisy Gibbs preparation under ETH. Their asymptotic bound retains a noise-dependent residual Bλ/[1−(1−λ)exp(−α)]. This is useful resilience, with a different guarantee from arbitrary global accuracy at fixed λ. Local thermal or energy objectives may also be useful when the full-state target here is unnecessary.")
table([
 ["Restriction", "Status"],
 ["Commuting target Hamiltonian", "Removed for the one-dimensional state-preparation task."],
 ["Target Davies bath / equilibration", "Unnecessary: H is a digital target and the state is prepared actively."],
 ["Individually isolatable target checks", "Unnecessary for supplied H; unknown-material identification is not claimed."],
 ["Homogeneous stationary Pauli apparatus", "Retained in completed acquisition and delivery."],
 ["Nonlocal links and protected control", "Retained and paid. Finite noisy block cells alone do not resolve faulty partition selection."],
 ["Independent endpoint channels", "Essential to the composition. Arbitrary local channels are covered mathematically, not by a new physical compiler."],
 ["Fixed temperature / bounded terms", "Substantive; the one-spin and dimer obstructions show why."],
 ["One-dimensional geometry", "Used by the all-temperature proof, without a claim of universal necessity."],
], [156,WIDTH-156])

page("15. High temperature and weak local apparatus")
p("BLMT already established high-temperature classical product-state preparation [10]. Putterman, Zlokapa and Cotler improve its temperature regime and cover long-range bounded-site-strength Pauli systems [11]. Separability and the absence of quantum entangling gates in those ideal operations are established prior capabilities.")
p("A constructive corollary of BLMT's coefficient slack uses an imperfect local palette. Let H=ΣₐJₐEₐ, with Pauli locality K and dual-graph degree d. Suppose site i can actually deliver every (I±rᵢσₐ)/2, with independent refreshed outputs and rᵢ&gt;0. Set")
eq(r"J_{\rm app}=\max_a |J_a|\prod_{i\in\operatorname{supp}E_a}r_i^{-1},\qquad\beta J_{\rm app}\leq\frac{1}{200K\max(1,d)}")
p("The weighted Pauli norm is submultiplicative. The source's degree-t coefficient bound ensures that each sampled factor I+cP has |c|≤the product of its rᵢ, with positive slack. Choose signs whose full parity has mean c divided by that product. All lower sign products vanish; their physical mixed-state product averages exactly to the intended factor. Replacing only the final pure-state decomposition preserves the source's delivered approximation error.")
p("For actual local Bloch vectors vⱼ, classical mixtures reach precisely conv{vⱼ}. Six linear programs decide whether every ±reₐ lies inside and produce attaining settings. A sufficient radius is 1−√3δ if each actual vertex is within Euclidean distance δ of its ideal Pauli vertex.")
p("Entanglement-breaking local devices with nonzero output radius can support this sufficiently mixed known-target task. Their lack of quantum capacity is irrelevant to that endpoint. Actual acquisition, independent reset and noisy selection remain required; convex geometry alone does not supply a generic observable apparatus oracle.")
p("Independent one-site factories cannot cover the entangled all-temperature family. For M disjoint thermal dimers of singlet overlap F&gt;1/2, a Bell-projector count yields distance at least 1−2exp[−M(F−1/2)²/2] from every fully separable state. The full proof and attaining local mixtures are in the boundary note.")

page("16. Direct distribution programming from assays")
p("A separate finite-factory construction asks whether apparatus parameters must be estimated to inverse-system-size accuracy when only a randomized corrective decision is required. Established Bernoulli-factory results are the appropriate comparator [12,13]. The following explicit finite-deadline method counts actual fresh assays.")
p("Suppose a real assay produces Bernoulli(p). An affine f(p)=ap+b remains in [δ,1−δ] on the promised domain. Draw n fresh assays, count K, and generate a known-probability coin with probability clip(f(K/n)). Unclipped expectation equals f(p); clipping occurs only on a large-deviation event. If M bounds the clipping displacement,")
eq(r"|\mathbb E\operatorname{clip}(aK/n+b)-f(p)|\leq2M\exp(-2n\delta^2/a^2)")
p("The parameter estimate still fluctuates at order one over square root n. Exponentially small marginal coin bias follows from unbiased affine expectation and rare clipping, not exponentially accurate estimation.")
p("For strictly positive rational weights wⱼ=Pⱼ/ΣPₖ on a compact outer assay box, degree elevation produces positive tensor-Bernstein coefficients. Choose j uniformly, generate binomial counts, and accept with its coefficient divided by a common maximum. The accepted label law is exactly w. With acceptance at least a₀, d coordinates, degree D, per-coin error η and a B-attempt deadline,")
eq(r"d_{\rm TV}\leq(1-a_0)^B+BdD\eta+\epsilon_{\rm arithmetic}")
p("At fixed templates and strict positivity margins, R factors need O(R log²(R/ε)) actual assay invocations. Arithmetic, selector, reset and per-assay costs remain. Every generated coin uses fresh trials; one random parameter estimate reused everywhere can introduce unwanted correlations. Fine assay records are discarded or their actual joint extension is specified.")
p("A growing-depth controller tree cannot be called a fixed-degree microscopic polynomial. Its operational assay would require a separately proved, paid implementation. This supplementary construction does not replace the earned general acquisition route in the all-temperature theorem.")

page("17. A concrete noisy scalar factory")
p("Suppose complete actual requested-sign routines output σ±=(I±κZ)/2. An additional real operation has the same Z contraction κ. A stationary noisy measurement/capture has expectation c+Az. Fair opposite-sign contrasts generate observable coin means m₁=Aκ and m₂=Aκ², cancelling the unknown offset.")
eq(r"w_+=\frac{m_2+rm_1}{2m_2}=\frac{1+r/\kappa}{2},\qquad w_+\sigma_++(1-w_+)\sigma_-=\frac{I+rZ}{2}")
p("An explicit primitive realization includes a symmetric raw-selector contraction b_c followed by quantum Pauli contraction λ_q, giving κ=b_cλ_q. A nominal-zero selector-controlled X followed by the same Pauli noise implements the matching additional operation. Actual selector and output noise are included. Complementarity, homogeneity, stationarity and independent refresh are explicit restrictions.")
p("For target r=1/2, actual m₁,m₂∈[0.8,1] and outer box [0.7,1.1]², the numerator polynomials m₂±rm₁ have positive corner coefficients. The affine/Bernstein race samples the desired sign law without estimating κ or meter visibility A to output accuracy. The final quantum outputs are freshly reset after the classical assay computation finishes, at a common deadline.")
p("Constants remain substantial: the conservative checked schedule for R=1000 and total ε=0.001 uses 222,912 assay-template invocations per output. Each template's operations, resets and captures count. This proves an accuracy-scaling distinction from point estimation, not practical economy or optimality against every competing method.")
p("A general six-palette application needs actual output vectors to be identifiable functions of finite observable assay parameters. Arbitrary SPAM has gauge ambiguities: a shared rotation of sources and meters can be invisible internally while changing the external target. The scalar construction does not solve that problem. Competing preparation methods are free to use the same probability-programming technique.")

page("18. Finite verification and its scope")
figure(ROOT / "noncommuting" / "verification_summary.png",maxheight=240,
 caption="Left: finite five-spin inverse-positivity thresholds, not a uniform-in-size bound. Right: exact Heisenberg-dimer boundary; the darker region also has an entangled target. Endpoint channel parameters are not primitive-noise threshold estimates.")
table([
 ["Check", "Observed result"],
 ["Softened spectral identities, 16 random positive sandwiches", "Maximum residual 4.64×10⁻¹⁵"],
 ["Mixed-Pauli reconstruction, 172 positive three-qubit components", "Trace error 4.44×10⁻¹⁶; minimum eigenvalue 4⁻³"],
 ["Nine-qubit ring, variable cuts and nonunitary local dressings", "Mixture trace error 3.26×10⁻¹⁶; transfer weights verified"],
 ["Heterogeneous nonunital inverse and finite noncommuting Gibbs matrices", "Norm bound and forward restoration verified; entangled example included"],
 ["Dimer boundary and rational probability race", "Exact dimer formula checked; Bernstein residual below 9×10⁻¹⁶"],
], [288,WIDTH-288])
p("Both verification scripts ran successfully. These are checks of identities and decisive finite examples. They do not implement the astronomically large source sampler, simulate an apparatus or lifetime, or establish favorable scaling and resource advantage.","small")

page("19. Useful failures, preservation and reproduction")
h("A finite-cell shortcut remains unproved")
p("A uniform block floor can place every target inside the convex hull of an isolated finite cell's noisy preparations. This alone does not schedule a random partition on a fixed chain. Faulty masks, selectors and couplers can create cross-block interactions. The completed all-temperature operation retains protected scheduling and routing. Elimination of growing error-correcting codes is not claimed.")
h("The boundary conditions remain substantive")
p("The general mathematical channel radius does not validate arbitrary coherent or correlated apparatus errors. Digital target input does not identify an unknown material. Finite calibration does not certify indefinite stationarity. A retained source label changes the conditional target. Known mixed-state preparation does not remove the unknown-input raw-port floor or supply a canonical TFD. Postselection on very rare outcomes can amplify an implementation error.")
h("Reproduce the new checks")
p("The archive contains the full robust-block proof, independent proof audit, physical operation note, current primary comparisons, high-temperature palette derivation, local-factory boundaries, direct-assay proof and both verification scripts. Run noncommuting/verify_robust_blocks.py and boundaries/verify_boundary_constructions.py with Python, NumPy, SciPy and Matplotlib. Machine-readable results and the figure are included.")
p("The preceding accepted noisy-interface package is preserved byte for byte, with its original SHA-256 in the manifest. It already retains the previous register/source/bath, burst, productive-control, repair, direct-prevention and first-event packages. No predecessor scope is broadened or re-audited here.")
p("The completed scientific contribution is the uniformly mixed block theorem and its compatible fixed-noise Gibbs preparation operation. The strongest ordinary active method can use it too. Better constants, a cheaper full controller and broader physical noise interfaces remain improvements to be earned, not hidden assumptions in the result.")

page("References and exact primary sources")
refs=[
 ("1","Pilatowsky-Cameo, Styliaris, Bakshi and Malz. One-dimensional quantum Gibbs states in constant circuit depth. arXiv:2609.35973v1, 28 Sep 2026. Theorems 1-2 and Appendices A-C.","https://arxiv.org/pdf/2609.35973"),
 ("2","Bakshi, Choi and Pilatowsky-Cameo. Entanglement in quantum spin chains is strictly finite at any temperature. arXiv:2602.13386v2, 2 Nov 2026. Lemma 8.4 and Section 9.","https://arxiv.org/pdf/2602.13386"),
 ("3","Zhang, Li, Lu, Yuan and Duan. Quantum error pre-compensation for quantum noisy channels. Physical Review A 106, 042440 (2022); arXiv:2309.01434.","https://arxiv.org/pdf/2309.01434"),
 ("4","Rouzé and Stilck França. Rapid mixing of Gibbs samplers via quantum Dobrushin-Shlosman conditions. arXiv:2610.03578v1, 2 Oct 2026. Theorems 3.11 and 5.1.","https://arxiv.org/pdf/2610.03578"),
 ("5","Christandl, Fawzi and Goswami. Fault-tolerant quantum input/output. arXiv:2408.05260v3, 2 Dec 2025.","https://arxiv.org/html/2408.05260v3"),
 ("6","Christandl, Fawzi and Goswami. Fault-tolerant interfaces for quantum LDPC codes. arXiv:2602.16948v2, 29 Sep 2026. Theorem 44.","https://arxiv.org/html/2602.16948v2"),
 ("7","Dünnweber, Styliaris and Trivedi. Quantum Memory and Autonomous Computation in Two Dimensions. arXiv:2601.20818v3, 25 Sep 2026. Sections V-VII.","https://arxiv.org/html/2601.20818v3")]
for num,title,url in refs:
    p("["+num+"] "+title+" "+link(url,"Primary text"),"small")
p("The targeted literature check found no prior statement of the precise uniformly interior block theorem constructed here. This is not an exhaustive priority determination. Comparisons distinguish ideal algorithms, physical noise, acquisition and delivered endpoints.","caption")

page("References, continued")
refs2=[
 ("8","Ding, Li and Zhang. Efficient thermalization of one-dimensional noncommuting Hamiltonians via system-bath interactions with Θ(n) ancilla qubits. arXiv:2611.03422v1, 2 Nov 2026.","https://arxiv.org/pdf/2611.03422"),
 ("9","Brunner et al. Lindblad engineering for quantum Gibbs state preparation under the eigenstate thermalization hypothesis. Quantum 9, 1843 (2025); arXiv:2412.17706v3. Section 6.","https://arxiv.org/html/2412.17706v3"),
 ("10","Bakshi, Liu, Moitra and Tang. High-Temperature Gibbs States are Unentangled and Efficiently Preparable. arXiv:2403.16850v2, 24 Feb 2025. Theorem 4.18 and Section 5.","https://arxiv.org/pdf/2403.16850"),
 ("11","Putterman, Zlokapa and Cotler. When quantum thermal states look classical. arXiv:2607.28536v2, 5 Oct 2026. Theorems 1-2 and Section 6.","https://arxiv.org/pdf/2607.28536"),
 ("12","Nacu and Peres. Fast simulation of new coins from old. Annals of Applied Probability 15 (2005), 93-115.","https://arxiv.org/pdf/math/0309222"),
 ("13","Morina, Latuszynski, Nayar and Wendland. From the Bernoulli factory to a dice enterprise via perfect sampling of Markov chains. Annals of Applied Probability 32 (2022), 327-359.","https://arxiv.org/abs/1912.09229"),
 ("14","Aharonov and Ben-Or. Fault-Tolerant Quantum Computation With Constant Error Rate. Protected-control machinery used through the accepted predecessor.","https://arxiv.org/pdf/quant-ph/9906129")]
for num,title,url in refs2:
    p("["+num+"] "+title+" "+link(url,"Primary text"),"small")
p("Accepted Astra input: Astra_Noisy_Thermal_Interface_Research_Package.zip, unchanged predecessor package dated 5 November 2026, included with its original source and scope records.","small")

def footer(canvas, doc):
    canvas.saveState()
    w,hpage=A4
    canvas.setStrokeColor(colors.HexColor("#D8E0E4"))
    canvas.line(48,43,w-48,43)
    canvas.setFont("DSans",8)
    canvas.setFillColor(MUTED)
    canvas.drawString(48,29,"ASTRA / THERMAL PREPARATION THROUGH FIXED NOISE")
    canvas.drawRightString(w-48,29,str(doc.page))
    canvas.restoreState()

pdf=OUT / "Astra_Robust_Many_Body_Preparation.pdf"
doc=SimpleDocTemplate(str(pdf),pagesize=A4,rightMargin=48,leftMargin=48,
                      topMargin=43,bottomMargin=58,
                      title="Thermal quantum states through imperfect apparatus",
                      author="Astra research construction",subject="Robust block mixtures and local-noise preimages")
doc.build(story,onFirstPage=footer,onLaterPages=footer)
(ROOT / "report_text.txt").write_text("\n\n".join(plain))
print(json.dumps({"pdf":str(pdf),"bytes":pdf.stat().st_size},indent=2))

