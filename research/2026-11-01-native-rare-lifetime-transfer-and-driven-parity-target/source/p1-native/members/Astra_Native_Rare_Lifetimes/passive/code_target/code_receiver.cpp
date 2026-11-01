#include <cstdint>
#include <fstream>
#include <iostream>
#include <random>
#include <stdexcept>
#include <vector>

// All receiver choices are exact rational choices. A seeded PRNG is the
// diagnostic realization; the probability theorem assumes independent bits.
using Wide=unsigned __int128;
struct Random {
  std::mt19937_64 rng;
  uint64_t words=0,calls=0,rejections=0;
  explicit Random(uint64_t seed):rng(seed){}
  uint64_t bounded(uint64_t bound) {
    if(!bound)throw std::runtime_error("zero bound");
    ++calls;
    const uint64_t threshold=(-bound)%bound;
    while(true) {
      uint64_t x=rng();++words;
      if(x>=threshold)return x%bound;
      ++rejections;
    }
  }
};
int main(int argc,char**argv) {
  if(argc!=2)return 2;
  std::ifstream in(argv[1]);
  int n,m;uint64_t trials,seed;
  in>>n>>m>>trials>>seed;
  if(!in||n<=m||n>120||m<1||m>64||n-m>=63)return 3;
  const int k=n-m;
  std::vector<uint64_t> column(n);
  for(auto &x:column)in>>x;
  if(!in)return 4;
  for(int i=0;i<m;i++)if(column[i]!=(uint64_t(1)<<i))return 5;
  for(auto x:column)if(!x)return 6;
  Random random(seed);
  uint64_t killed=0,returned=0,events=0,following_flips=0,max_events=0;
  uint64_t codeword_parity_xors=0,initial_membership_xors=0;
  uint64_t initial_membership_bit_inspections=0;
  for(uint64_t trial=0;trial<trials;trial++) {
    // Explicit exact conditional target preparation: uniform z, x=(Pz,z).
    // Although translation symmetry would allow canonical x=0, this run pays
    // for preparation and all n initial membership-coordinate inspections.
    const uint64_t z=random.bounded(uint64_t(1)<<k);
    uint64_t parity=0;
    for(uint64_t w=z;w;w&=w-1) {
      int j=__builtin_ctzll(w);parity^=column[m+j];++codeword_parity_xors;
    }
    const Wide x=Wide(parity)|(Wide(z)<<m);
    uint64_t syndrome=0;
    for(int i=0;i<n;i++) {
      ++initial_membership_bit_inspections;
      if((x>>i)&1) {syndrome^=column[i];++initial_membership_xors;}
    }
    if(syndrome)return 7;
    // Total boundary rate is n. The initial boundary flip is counted separately.
    syndrome^=column[random.bounded(n)];
    if(!syndrome)return 8;
    uint64_t this_events=0;
    while(true) {
      ++events;++this_events;
      // Unit coordinate flips get ten slots each; kill rate1/10 gets one.
      const uint64_t draw=random.bounded(10*n+1);
      if(draw==uint64_t(10*n)) {++killed;break;}
      syndrome^=column[draw/10];++following_flips;
      if(!syndrome) {++returned;break;}
    }
    if(this_events>max_events)max_events=this_events;
  }
  std::cout<<"{\"n\":"<<n<<",\"m\":"<<m<<",\"trials\":"<<trials
    <<",\"seed\":"<<seed<<",\"killed_before_return\":"<<killed
    <<",\"returned_before_kill\":"<<returned<<",\"following_events_including_kills\":"<<events
    <<",\"following_flip_events\":"<<following_flips
    <<",\"initial_boundary_flips\":"<<trials
    <<",\"total_boundary_and_following_events\":"<<trials+events
    <<",\"maximum_following_events_one_trial\":"<<max_events
    <<",\"conditional_samples\":"<<trials
    <<",\"conditional_sample_random_bits\":"<<uint64_t(k)*trials
    <<",\"conditional_codeword_parity_xors\":"<<codeword_parity_xors
    <<",\"initial_membership_bit_inspections\":"<<initial_membership_bit_inspections
    <<",\"initial_membership_xors\":"<<initial_membership_xors
    <<",\"syndrome_transition_xors\":"<<trials+following_flips
    <<",\"uniform_integer_calls\":"<<random.calls
    <<",\"rng64_words_drawn\":"<<random.words
    <<",\"rng_rejections\":"<<random.rejections
    <<",\"boundary_rate\":"<<n
    <<",\"following_total_integer_weight\":"<<10*n+1
    <<",\"flip_integer_weight\":10,\"kill_integer_weight\":1,\"rate_denominator\":10"
    <<",\"H_column_words_stored\":"<<n<<"}\n";
}
