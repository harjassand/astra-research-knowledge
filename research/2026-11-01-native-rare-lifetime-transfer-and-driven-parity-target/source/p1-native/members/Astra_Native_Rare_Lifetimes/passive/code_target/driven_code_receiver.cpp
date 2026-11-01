#include <cstdint>
#include <fstream>
#include <iostream>
#include <random>
#include <stdexcept>
#include <vector>

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
  if(argc<2||argc>3)return 2;
  std::ifstream in(argv[1]);
  int n,m;uint64_t trials,seed;
  in>>n>>m>>trials>>seed;
  if(argc==3)seed=std::stoull(argv[2]);
  if(!in||n<=m||n>120||m<1||m>64||n-m>=63)return 3;
  const int k=n-m, primitives=2*n-1;
  std::vector<uint64_t> column(n);
  for(auto &x:column)in>>x;
  if(!in)return 4;
  for(int i=0;i<m;i++)if(column[i]!=(uint64_t(1)<<i))return 5;
  for(auto x:column)if(!x)return 6;
  Random random(seed);
  uint64_t killed=0,returned=0,initial_stays=0,initial_nulls=0;
  uint64_t events=0,following_maps=0,following_nulls=0,max_events=0;
  uint64_t codeword_parity_xors=0,initial_membership_xors=0;
  uint64_t initial_membership_bit_inspections=0,final_membership_xors=0;
  uint64_t final_membership_bit_inspections=0,transition_xors=0;
  uint64_t initial_single_bit_moves=0,initial_two_bit_moves=0;
  uint64_t following_single_bit_moves=0,following_two_bit_moves=0;
  auto syndrome_of=[&](Wide x,bool initial) {
    uint64_t y=0;
    for(int i=0;i<n;i++) {
      if(initial)++initial_membership_bit_inspections;
      else ++final_membership_bit_inspections;
      if((x>>i)&1) {
        y^=column[i];
        if(initial)++initial_membership_xors;else ++final_membership_xors;
      }
    }
    return y;
  };
  // Return the number of changed bits. This acts on the full reference state;
  // the nonlinear three-cycle generally does NOT close on syndrome alone.
  auto move=[&](Wide &x,uint64_t &syndrome,int primitive) {
    if(primitive<n) {
      x^=Wide(1)<<primitive;syndrome^=column[primitive];++transition_xors;
      return 1;
    }
    const int i=primitive-n;
    const int old=int((x>>i)&3);
    static const int forward[4]={1,3,2,0},reverse[4]={3,0,2,1};
    const int next=(i&1)?reverse[old]:forward[old];
    const int changed=old^next;
    if(!changed)return 0;
    x=(x&~(Wide(3)<<i))|(Wide(next)<<i);
    int changed_count=0;
    if(changed&1) {syndrome^=column[i];++transition_xors;++changed_count;}
    if(changed&2) {syndrome^=column[i+1];++transition_xors;++changed_count;}
    return changed_count;
  };
  for(uint64_t trial=0;trial<trials;trial++) {
    const uint64_t z=random.bounded(uint64_t(1)<<k);
    uint64_t parity=0;
    for(uint64_t w=z;w;w&=w-1) {
      int j=__builtin_ctzll(w);parity^=column[m+j];++codeword_parity_xors;
    }
    Wide x=Wide(parity)|(Wide(z)<<m);
    uint64_t syndrome=syndrome_of(x,true);
    if(syndrome)return 7;
    int changed=move(x,syndrome,random.bounded(primitives));
    if(changed==0)++initial_nulls;
    else if(changed==1)++initial_single_bit_moves;
    else ++initial_two_bit_moves;
    if(!syndrome) {
      ++initial_stays;
      if(syndrome_of(x,false)!=syndrome)return 8;
      continue; // contributes Bernoulli zero, not a discarded/retried trial
    }
    uint64_t this_events=0;
    while(true) {
      ++events;++this_events;
      uint64_t draw=random.bounded(10*primitives+1);
      if(draw==uint64_t(10*primitives)) {++killed;break;}
      ++following_maps;
      changed=move(x,syndrome,draw/10);
      if(changed==0)++following_nulls;
      else if(changed==1)++following_single_bit_moves;
      else ++following_two_bit_moves;
      if(!syndrome) {++returned;break;}
    }
    if(syndrome_of(x,false)!=syndrome)return 9;
    if(this_events>max_events)max_events=this_events;
  }
  std::cout<<"{\"n\":"<<n<<",\"m\":"<<m<<",\"trials\":"<<trials
    <<",\"seed\":"<<seed<<",\"killed_before_return\":"<<killed
    <<",\"returned_after_initial_exit\":"<<returned
    <<",\"initial_proposals_staying_in_target\":"<<initial_stays
    <<",\"initial_null_proposals\":"<<initial_nulls
    <<",\"initial_single_bit_moves\":"<<initial_single_bit_moves
    <<",\"initial_two_bit_moves\":"<<initial_two_bit_moves
    <<",\"following_events_including_kills\":"<<events
    <<",\"following_primitive_proposals\":"<<following_maps
    <<",\"following_null_proposals\":"<<following_nulls
    <<",\"following_single_bit_moves\":"<<following_single_bit_moves
    <<",\"following_two_bit_moves\":"<<following_two_bit_moves
    <<",\"initial_boundary_proposals\":"<<trials
    <<",\"total_boundary_and_following_events\":"<<trials+events
    <<",\"maximum_following_events_one_trial\":"<<max_events
    <<",\"conditional_samples\":"<<trials
    <<",\"conditional_sample_free_bits\":"<<uint64_t(k)*trials
    <<",\"conditional_codeword_parity_xors\":"<<codeword_parity_xors
    <<",\"initial_membership_bit_inspections\":"<<initial_membership_bit_inspections
    <<",\"initial_membership_xors\":"<<initial_membership_xors
    <<",\"final_membership_bit_inspections\":"<<final_membership_bit_inspections
    <<",\"final_membership_xors\":"<<final_membership_xors
    <<",\"syndrome_transition_xors\":"<<transition_xors
    <<",\"full_state_syndrome_checks\":"<<2*trials
    <<",\"uniform_integer_calls\":"<<random.calls
    <<",\"rng64_words_drawn\":"<<random.words
    <<",\"rng_rejections\":"<<random.rejections
    <<",\"boundary_dominating_rate\":"<<primitives
    <<",\"following_total_integer_weight\":"<<10*primitives+1
    <<",\"primitive_integer_weight\":10,\"kill_integer_weight\":1,\"rate_denominator\":10"
    <<",\"H_column_words_stored\":"<<n<<"}\n";
}
