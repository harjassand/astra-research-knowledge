# Exact additive-quaternary coupling gate

10 October 2026. This is a restricted construction, not a general sunflower theorem or a verified novelty claim.

## Native input and theorem
Let L_i:F_2^m -> V_i, i=1,...,w, be explicitly given binary linear maps, with dim(V_i)<=2. Embed each V_i injectively and F_2-linearly into F_4=F_2[omega]/(omega^2+omega+1). Let M be the w-by-m matrix over F_4 representing these embedded maps on binary inputs, and r=rank_F4(M).

Choose z uniformly from ker_F4(M), write z=u+omega v with u,v in F_2^m, and independently choose a uniform in F_2^m. Output the three latent rows (a,a+u,a+v), and apply the original block maps.

Every replica is uniform. In block i, Mz=0 gives L_i(u)=omega L_i(v) in the embedded image. Thus either both are zero or they are distinct nonzero values, in which case 0,L_i(u),L_i(v) are distinct. Every observed block is consequently all-equal or all-distinct. The one-dimensional output case necessarily has both values zero, since its nonzero F_2-line is not invariant under multiplication by omega.

The output latent triple uniquely recovers (a,u,v), hence (a,z). Its law is uniform on 2^m*4^(m-r) triples. Relative entropy against three independent uniform latent replicas is exactly r*log(4)<=w*log(4). Applying observed maps cannot increase this relative entropy. If the combined original map is injective, the observed mapping preserves it exactly.

If the combined map is injective and m>w, select any nonzero kernel vector z. Neither u nor v can be zero, nor can u=v: each case, together with Mz=0, would put a nonzero binary vector in the joint original kernel. Therefore the construction gives three distinct codewords forming a sunflower. A sunflower-free jointly injective additive code of this output-rank class must have m<=w and at most 2^w rows.

## Native cost
Finite-field Gaussian elimination constructs a kernel basis in polynomial time in the explicit w-by-m input; all field operations are on two-bit field elements. Sampling uses exactly m+2(m-r) independent unbiased random bits and polynomially many field operations. Original maps and embeddings are explicit inputs. No hitting-set, representation acquisition, or sampling oracle is assumed. This does not acquire a suitable additive representation for an arbitrary family.

## Boundary
For output rank above two, a single F_4-valued binary linear functional need not be injective. A nonzero rank-one observed pair may lie in that functional's kernel, so the proof does not extend simply by compression. No general m<=w or m<=Cw additive-code theorem is established here. No external certification or priority verification has been obtained.

## Exact reproduction
Run quaternary_coupling.py using Python's standard library. Sixty fixed-seed cases check 36,800 distinct latent coupling triples, their validity, exact marginals, kernel dimension and likelihood ratio. Forty-one cases have jointly injective original maps. The proof, not these finite checks, establishes the general rank-at-most-two statement.

check_kernels.py exhaustively checks small general-rank cases (m,w)=(3,2),(4,3), finding no counterexample among 64 and 40,205 jointly injective distinct-kernel collections respectively. Repeated kernels cannot add plane coverage; a full-space kernel pads smaller collections. random_gate.py checks 100,000 seeded draws for (5,4), of which 98,651 are jointly injective, finding no counterexample. The latter is random falsification only; none of these checks proves a general-rank theorem.
