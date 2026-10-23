# Missing-data bound for the literal BG block source

## Setup

Fix (k\ge 2) and (r\ge1). The free input is ((X,Y)\), with independent uniform strings (X,Y\in[k]^r). On the designated block source Alice's reported answers at coordinate (i) are the full-string answers
\[
  A_i=(X,i),\qquad B_i=(Y,i).
\]
This is the literal BG block strategy: it uses index (i), returns the entire input string, and its graph test additionally checks ((X,Y)\in E(\Gamma)\).

In the oracularized check Bob receives a tag string \(\sigma\in\{A,B\}^r\) and only the selected symbols
\[
 Z_i=X_i\ (\sigma_i=A),\qquad Z_i=Y_i\ (\sigma_i=B).
\]
He may apply any joint instrument to his share of arbitrary prior entanglement, and his output is checked against Alice's selected coordinate answers. Assume \(\sigma\) is sampled independently and uniformly from \(\{A,B\}^r\).

## Claim

For every fixed mixed tag \(\sigma\) (at least one (A) and one (B\)), the probability of passing all consistency checks is at most \(k^{-r}\). This holds for arbitrary finite or infinite-dimensional shared states and arbitrary local instruments. Averaged over uniform tags, consistency success is at most
\[
  2^{1-r}+(1-2^{1-r})k^{-r}.
\]
The graph test can only reduce full-game success.

## Proof including Alice's instrument

Let \(\rho_{AB}\) be the shared state, independent of the free inputs. Alice may use any input-dependent complete instrument, including hidden fine outcomes. Sum over all fine outcomes and retain only her prescribed public answer. The resulting map \(\mathcal E_{XY}\) on her system is trace preserving. Non-signalling, equivalently invariance of the other marginal under a local trace-preserving map, gives
\[
 \operatorname{Tr}_A[(\mathcal E_{XY}\otimes\mathrm{id})(\rho_{AB})]=\rho_B
 \quad\text{for every }X,Y.
\]
Because the public answers in this source are the fixed values \((X,i),(Y,i)\), conditioning on those reported answers does not refine Bob's state. Thus Bob's conditional output law, for any quantum measurement/instrument he chooses from \((\sigma,Z)\), depends on \(\sigma,Z\) and the shared state, but not on the unobserved input symbols. Shared classical randomness is independent of inputs and can be conditioned on throughout.

For fixed \(\sigma,Z\), define the missing string
\[
 W_i=Y_i\ (\sigma_i=A),\qquad W_i=X_i\ (\sigma_i=B).
\]
Since the pairs \((X_i,Y_i)\) are independent uniform pairs, (W\) is uniform on \([k]^r\), even after conditioning on \((\sigma,Z)\). If \(\sigma\) is mixed, at least one selected Alice answer is of the form \((X,i)\) and at least one is \((Y,j)\). Passing all consistency checks therefore forces Bob's answers to contain the exact full strings (X) and (Y), hence to determine the entire missing string (W). For any possibly randomized/quantum-generated guess \(\widehat W\) whose law depends only on \((\sigma,Z)\),
\[
 \Pr[\widehat W=W\mid\sigma,Z]
 = k^{-r}\sum_{w\in[k]^r}\Pr[\widehat W=w\mid\sigma,Z]
 \le k^{-r}.
\]
This proves the conditional bound. Exactly two of the (2^r) tag strings are homogeneous; on them Bob sees all of (X) or all of (Y), so consistency may pass with probability one. Averaging the mixed and homogeneous cases yields the stated bound.

## Scope

The input-independence step relies on the source's public Alice answers being fixed deterministically as ((X,i),(Y,i)). It is not a bound for arbitrary Alice answer strategies whose random outputs may correlate with Bob's output. It also does not prove a quantum/commuting value gap for the BG graph game: it only quantifies the consistency penalty for this literal full-string block source under mixed-coordinate oracularization.
