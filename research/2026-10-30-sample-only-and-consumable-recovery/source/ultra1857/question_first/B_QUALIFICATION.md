# Qualify a resolution before the unknown payload, not a lost-frame decoder

B/C question-first construction,30October2026. B proposed pre-payload
qualification of the unitary-invariant recovery PROPERTY; C and root
independently reconstruct the held-out Bell argument. This is ordinary
held-out testing combined with the actual common-frame interface. It is
not a new general statistical principle or an executed quantum experiment.

## 1. The acquired property

For a fixed channel F:k->B define

`f*(F)=sup_(R CPTP) F_e(R F,I_k/k)`.

It is invariant under an isometry/unitary change of F's occupied output
frame. The frame and an optimizing R need not be known to evaluate a
sound LOWER confidence bound: any physical candidate R supplies one.

Predeclare a FINITE collection of rational filter resolutions a_i and
their finite random thresholds t_i, plus all sample/error budgets. Let
F_i be the corresponding ideal actual-source filtered channels from
B_SPECTRAL_PORT.md. Each has known support cap floor(1/a_i)+1, without
an exact-rank promise on the original N. The source is the SAME fixed
memoryless N during qualification and all future service.

## 2. One qualification batch has a shared frame

For candidate i acquire N_i training Choi programs and v_i HELD-OUT
Choi programs by actual calls of F_i, with their logical Bell references
untouched. Perform ONE reference-joint compression on ALL these outputs.
The exact common-frame identity gives the mathematical state

`integral J_(F_i,U)^tensor(N_i+v_i) dU`.

Train only on the first N_i programs. On every training outcome z the
candidate R_(i,z) must be a PHYSICAL CPTP map, including all fallback
branches. It may be the finite ridge/Petz receiver; no optimum is needed.
Freeze it before inspecting the held-out measurements. Apply it to each
held-out small output and Bell-measure against that program's original
logical reference.

Conditional on one latent U and training outcome z, these v_i outcomes
are independent Bernoulli with mean

`p_i(U,z)=F_e(R_(i,z) F_i,U,I/k)<=f*(F_i)`.             (1)

The inequality is output-unitary invariance. The conditioning is a proof
representation of the actual joint state, not access to U. It remains
valid after averaging with the TRUE posterior of U given z.

For the empirical success fhat_i and any s_i>0, Hoeffding therefore gives

`Pr[fhat_i-s_i>f*(F_i)]<=exp(-2v_i s_i^2)`.            (2)

No training-tomography success event is needed for this FALSE-ACCEPT
bound; even a bad physical candidate has success<=f*. In particular, one
does not infer that its old small matrix is reusable on a later ambient
payload. Non-CP rounded candidates would invalidate the argument and are
forbidden by the supplied physical fallback.

## 3. Finite implementation, multiplicity and selection

Let eps_i be a FULL diamond error bound for the COMPLETE qualification
processor against its ideal version, on good thresholds. This includes
ALL source-copy filters, joint compression, candidate synthesis and Bell
measurement. Event probabilities differ by at most eps_i (a conservative
bound). Let q_i bound the bad-threshold probability. Define

`beta_qual=sum_i [exp(-2v_i s_i^2)+eps_i+q_i]`.         (3)

Then, except with total probability beta_qual, ALL reported lower bounds
`ell_i=max(0,fhat_i-s_i)` satisfy `ell_i<=f*(F_i)` and the required
threshold gaps hold. Any selection of an index from this predeclared
finite list based on its records is covered by the SAME event. No
independence between candidates is required. Repeated unbudgeted searches
or optional continuation are not covered by(3).

Every v_i validation program is an actual source use. All its output and
reference storage, filters and global source-call simulations count.
The complete eps_i must be divided across the entire declared operation,
not assigned independently to every program for free. A finite integer
schedule may choose H_i with2^H_i>=1/beta_i and
`v_i=ceil[H_i/(2s_i^2)]`, giving the relevant exponential term<=beta_i
without a log oracle.

The public record ell_i is a lower bound on an EXISTENCE optimum, not
proof that the old R_(i,z) belongs to a future coordinate frame.

## 4. A genuinely fresh future decoder

Only after qualification, choose a candidate with ell_i>=ell and set
`kappa_F=1-ell`. Before the unknown payload arrives, acquire a FRESH
independent training/program batch for this selected F_i. Its old fixed
threshold t_i is retained. Do not reuse the previously compressed
coordinate frame, nor retry a payload damaged during a rejected trial.
Source stationarity/memorylessness over this interval is substantive.

The fresh N1291-type agnostic recovery theorem needs only existence of a
competitor with Bell infidelity<=kappa_F. It yields, on the valid
qualification event, a new averaged physical decoder with

`halfdiamond(decoded,id_k)
 <= k sqrt(2kappa_F+3delta_new)+beta_new+gamma_new`.    (4)

Here delta_new is its good-event small-channel estimation error,
beta_new the fresh estimation failure weight and gamma_new the COMPLETE
implementation error. Its full new training, reference and unknown
payload outputs must again participate in ONE common compression.
Formula(4) concerns arbitrary logical payload/reference inputs. The
payload may arrive late, but is protected through that batch's fitting
and decoder synthesis. It is not a learned reusable classical decoder.

If the independently admitted RDS/programmed-Petz route replaces this
fresh batch, its OWN source/rank/support/consistency/resource theorem must
be substituted. This qualification lemma does not silently establish
that stronger route.

## 5. The acceptance probability must stay in the theorem

Let p_acc be the probability of choosing a qualifying candidate. All
qualification precedes and is independent of the unknown payload input.
If e is the uniform bound in(4), the accepted subnormalized service map
Lambda_acc obeys the conservative complete instrument bound

`(1/2)||Lambda_acc-p_acc id_k||_diamond
 <=p_acc e+beta_qual`.                               (5)

Bad accepted histories have total weight at most beta_qual. Good
histories have uniform complete error<=e using the fresh independent
program, so they sum with weight at most p_acc. If p_acc>0, a conditional
service bound follows only AFTER division:

`halfdiamond(Lambda_acc/p_acc,id_k)
 <=e+beta_qual/p_acc`.                               (6)

Without a lower bound on yield, no confidence conditional on acceptance
is asserted. The procedure may abort without touching an unknown payload.

For success/yield analysis, standard source promises can be used: if one
candidate has a sufficiently accurate recovery competitor and its
training procedure succeeds with high probability, its held-out mean
exceeds ell+2s and it passes except with its training, validation and
implementation failures. Root's recoverability/effective-tail bound
supplies one such condition. Those promises are not needed for the sound
bad-accept statement(3), and are not inferred from a finite record.

## 6. What supplier was removed, and what was not

The algorithm can search a predeclared finite resolution budget without
being given a true effective rank, microscopic model, junk spectrum or
recovery map. If it passes, it has acquired an operationally useful
recovery PROPERTY and a valid resolution choice for later acquisition.
It has not acquired the old coordinate frame for streaming reuse.

Known logical/carrier dimensions, trusted coherent controls, the fixed
source across calls, coherent storage and all finite-copy resources
remain required. There is no success or optimal-resolution guarantee for
an arbitrary source. No protected hardware, measurement calibration,
actual quantum sample, practical gain or priority determination is
claimed. This is a finite-budget mathematical operation and handoff;
there is no new source case or optimizer run in this packet.
