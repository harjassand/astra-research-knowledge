import unittest
from fractions import Fraction
from calibrate_affine_innovations import calibrate, mechanism, matvec, recover, trajectory_pairs, dyadic_confidence_exponent

class CalibrationTests(unittest.TestCase):
    def base(self, **updates):
        args=dict(F=[[1]],G=[[1]],beta=0,transitions=[(0,i%2) for i in range(512)],N=512,radius='1/4',delta='1/4',b=0,T=1,p_slots=0,epsilon_model=18)
        args.update(updates)
        return calibrate(**args)
    def test_exact_pass_threshold(self):
        z=self.base(); self.assertEqual(z['status'],'PASS'); self.assertEqual(z['eta_hat'],'0'); self.assertEqual(z['eta_upper'],z['eta_target']); self.assertEqual(z['model_error_upper_if_good'],'18')
    def test_exact_abort_threshold(self):
        self.assertEqual(self.base(epsilon_model='17999/1000')['status'],'ABORT')
    def test_biased_transcript_aborts(self):
        self.assertEqual(self.base(transitions=[(0,0)]*512)['status'],'ABORT')
    def test_rare_false_pass_is_allowed(self):
        # Under p(0)=9/10, each listed finite balanced transcript has positive
        # probability, yet true eta=4/5 exceeds target1/4. Record validation
        # cannot verify p. The confidence event is not posterior certainty.
        z=self.base(); self.assertEqual(z['status'],'PASS'); self.assertFalse(z['model_promise_verified']); self.assertGreater(Fraction(4,5),Fraction(z['eta_target']))
    def test_insufficient_N(self):
        with self.assertRaises(ValueError): self.base(N=1,transitions=[(0,0)])
    def test_wrong_length(self):
        with self.assertRaises(ValueError): self.base(transitions=[(0,0)]*511)
    def test_invalid_F(self):
        for F in ([[0]],[[1,0]],[[True]]):
            with self.assertRaises(ValueError): self.base(F=F)
    def test_invalid_G(self):
        for G in ([[0]],[[1,1]],[[2]]):
            with self.assertRaises(ValueError): self.base(G=G)
    def test_noncontrollable(self):
        with self.assertRaises(ValueError): mechanism([[1,0],[0,1]],[[1],[0]],0)
    def test_off_image(self):
        with self.assertRaises(ValueError): calibrate([[0,1],[1,0]],[[1],[0]],0,[(0,2)]*512,N=512,radius='1/8',delta='1/4',b=0,T=1,p_slots=0,epsilon_model=18)
    def test_horizon_two(self):
        z=calibrate([[0,1],[1,0]],[[1],[0]],0,[(0,i%2) for i in range(512)],N=512,radius='1/8',delta='1/4',b=0,T=1,p_slots=0,epsilon_model=18)
        self.assertEqual(z['m'],2); self.assertEqual(z['status'],'PASS')
    def test_exact_schedule_boundary(self):
        self.assertEqual(self.base(N=128,transitions=[(0,i%2) for i in range(128)])['status'],'PASS')
        with self.assertRaises(ValueError): self.base(N=127,transitions=[(0,i%2) for i in range(127)])
    def test_all_tick_chain_self_loops(self):
        states=[0]; innovations=[]
        for i in range(512):
            r=i%2; innovations.append(r); states.append(states[-1]^r)
        z=self.base(transitions=trajectory_pairs(states)); self.assertEqual(z['eta_hat'],'0')
        # A change-only list is too short for the fixed acquisition budget.
        pairs=[p for p in trajectory_pairs(states) if p[0]!=p[1]]
        with self.assertRaises(ValueError): self.base(transitions=pairs)
    def test_budget_types(self):
        for kw in ({'radius':.25},{'delta':0},{'b':-1},{'T':-1},{'p_slots':True},{'N':True},{'epsilon_model':0}):
            with self.assertRaises(ValueError): self.base(**kw)
    def test_invalid_labels(self):
        for pair in [(0,2),(True,0),(-1,0),(0,)]:
            with self.assertRaises(ValueError): self.base(transitions=[pair]*512)
    def test_dyadic_exponent(self):
        for delta,j in [(Fraction(1,2),1),(Fraction(1,3),2),(Fraction(1,4),2),(Fraction(3,4),1),(Fraction(1,1024),10)]:
            self.assertEqual(dyadic_confidence_exponent(delta),j)
    def test_injective_decode(self):
        # Enumerate every full-column-rank n<=3 G, every innovation.
        cases=0
        from calibrate_affine_innovations import rank
        for n in range(1,4):
            for k in range(1,n+1):
                for bits in range(1<<(n*k)):
                    G=[[(bits>>(i*k+j))&1 for j in range(k)] for i in range(n)]
                    if rank(G)!=k: continue
                    for r in range(1<<k):
                        self.assertEqual(recover(G,matvec(G,r)),r); cases+=1
        self.assertGreater(cases,1000)

if __name__=='__main__': unittest.main(verbosity=2)
