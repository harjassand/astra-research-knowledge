import unittest,random,copy,json
from fractions import Fraction as F
from acquire_threshold_source import ThresholdSource,verify_spec,ceil_log2_positive

class ThresholdTests(unittest.TestCase):
    def small(self,n=3):
        return ThresholdSource([[1,2] for _ in range(n)],[[[3,2],[2,3]] for _ in range(n-1)])

    def test_malformed(self):
        bad=[([],[]),([[1]],[]),([[0,1]],[]),([[True,1]],[]),([[1.,1]],[]),([[1,1]],[[[1,1],[1,1]]]),([[1,1],[1,1]],[]),([[1,1],[1,1]],[[[1,1],[1]]])]
        for u,e in bad:
            with self.assertRaises(ValueError): ThresholdSource(u,e)

    def test_labels(self):
        s=self.small()
        for x in (-1,8,True,1.0):
            with self.assertRaises(ValueError): s.column(x)
        with self.assertRaises(ValueError): s.map(-1,0)

    def test_exact_columns_and_erasure(self):
        for n in range(1,5):
            s=self.small(n)
            for x in range(1<<n):
                rows=s.column(x)
                self.assertEqual(len(rows),2*len(s.colors))
                self.assertEqual(sum((r['probability'] for r in rows),F(0)),1)
                for row in rows:
                    if not row['probability']: continue
                    f,y,j=row['color'],row['y'],row['slot']; c=s.colors[f]
                    self.assertEqual(s.map(f,y),x)
                    self.assertEqual(j,0 if s.map(f,y)==y else 1)
                    self.assertEqual(row['probability']*s.probability(x),c.delta/s.R*s.probability(y))

    def test_exact_classical_law_and_balance(self):
        rng=random.Random(90731)
        for trial in range(32):
            n=1+trial%4
            s=ThresholdSource([[rng.randint(1,5),rng.randint(1,5)] for _ in range(n)],[[[rng.randint(1,5) for _ in range(2)] for _ in range(2)] for _ in range(n-1)])
            d=1<<n
            forward=[[F(0) for _ in range(d)] for _ in range(d)]
            quantum=[[F(0) for _ in range(d)] for _ in range(d)]
            for x in range(d):
                for f,c in enumerate(s.colors): forward[s.map(f,x)][x]+=c.delta/s.R
                for row in s.column(x): quantum[row['y']][x]+=row['probability']
                for i in range(n):
                    y=x^(1<<i); rate=s.rates[i,(x>>i)&1,s.context(x,i)]
                    self.assertEqual(forward[y][x],rate/s.R)
                self.assertEqual(sum((forward[y][x] for y in range(d)),F(0)),1)
            self.assertEqual(forward,quantum)
            for x in range(d):
                for y in range(d): self.assertEqual(s.probability(x)*forward[y][x],s.probability(y)*forward[x][y])

    def test_messages_and_means(self):
        for n in range(1,5):
            s=self.small(n); d=1<<n
            self.assertEqual(sum((s.probability(x) for x in range(d)),F(0)),1)
            self.assertEqual(s.pi_min,min(s.probability(x) for x in range(d)))
            for x in range(d):
                p=s.first[x&1]
                for i in range(1,n): p*=s.conditional[i-1][(x>>(i-1))&1][(x>>i)&1]
                self.assertEqual(p,s.probability(x))
            for mask in range(d):
                expected=sum((s.probability(x)*(-1 if (x&mask).bit_count()%2 else 1) for x in range(d)),F(0))
                self.assertEqual(s.parity_mean(mask),expected)

    def test_dense_stinespring(self):
        import numpy as np
        for n in range(1,5):
            s=self.small(n); d=1<<n
            W=np.zeros((len(s.colors)*d,d))
            for x in range(d):
                for row in s.column(x): W[row['color']*d+row['y'],x]=float(row['probability'])**.5
            psi=np.array([float(s.probability(x))**.5 for x in range(d)])
            c=np.array([float(col.delta/s.R)**.5 for col in s.colors])
            self.assertLess(np.linalg.norm(W.T@W-np.eye(d)),1e-12)
            self.assertLess(np.linalg.norm(W@psi-np.kron(c,psi)),1e-12)

    def test_n64_symbolic_no_source_table(self):
        n=64
        s=ThresholdSource([[1,1] for _ in range(n)],[[[11,10],[10,11]] for _ in range(n-1)])
        self.assertLessEqual(len(s.colors),8*n)
        self.assertGreater(s.kappa,0)
        self.assertIsNotNone(s.return_m)
        for x in (0,(1<<n)-1,int('10'*32,2)):
            self.assertEqual(sum((r['probability'] for r in s.column(x)),F(0)),1)
        self.assertEqual(s.parity_mean(1),0)
        self.assertTrue(verify_spec(s.specification([0,1,(1<<64)-1])))

    def test_weak_and_unadmitted(self):
        self.assertGreater(self.small().kappa,0)
        # Strong 3-site ferromagnet can fail Dobrushin, though source remains valid.
        s=ThresholdSource([[1,1]]*3,[[[100,1],[1,100]]]*2)
        self.assertLessEqual(s.kappa,0)
        self.assertIsNone(s.return_m)
        self.assertEqual(sum((r['probability'] for r in s.column(0)),F(0)),1)

    def test_spec_tampering(self):
        s=self.small(); spec=s.specification([0,3])
        self.assertTrue(verify_spec(spec)); self.assertTrue(verify_spec(json.loads(json.dumps(spec))))
        for field,value in [('R','1'),('n',3.0),('version',True),('return_m',1),('pi_min','1'),('scope','claimed quantum simulator')]:
            changed=copy.deepcopy(spec); changed[field]=value; self.assertFalse(verify_spec(changed))
        changed=copy.deepcopy(spec); changed['colors'][0]['delta']='999'; self.assertFalse(verify_spec(changed))
        changed=copy.deepcopy(spec); changed['parity_means']['3']='999'; self.assertFalse(verify_spec(changed))
        changed=copy.deepcopy(spec); changed['onsite'][0][0]='0'; self.assertFalse(verify_spec(changed))

    def test_dyadic_return_arithmetic(self):
        for x,j in [(F(1),0),(F(3,2),1),(F(2),1),(F(17),5)]: self.assertEqual(ceil_log2_positive(x),j)
        for n in range(1,5):
            s=self.small(n)
            if s.return_m is not None:
                # These small instances permit exact power verification too.
                self.assertLessEqual(F(n)/s.pi_min*(1-s.kappa/s.R)**s.return_m,F(1,16))

if __name__=='__main__': unittest.main(verbosity=2)
