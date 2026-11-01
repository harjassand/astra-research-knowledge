#include <algorithm>
#include <cstdint>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <random>
#include <vector>
// Rational categorical uniformization, including marked null moves.
// The PRNG provides a reproducible numerical experiment, not physical data.
struct Move {
 int type,i,j,inverse; uint64_t weight;
 uint64_t apply(uint64_t x) const {
  if(type==0) return x^(uint64_t(1)<<i);
  static constexpr int fwd[4]={1,3,2,0}, rev[4]={3,0,2,1};
  int old=int((x>>i)&1)+2*int((x>>j)&1);
  int next=inverse?rev[old]:fwd[old];
  uint64_t clear=(uint64_t(1)<<i)|(uint64_t(1)<<j);
  return (x&~clear)|(uint64_t(next&1)<<i)|(uint64_t((next>>1)&1)<<j);
 }
};
int main(int argc,char** argv) {
 if(argc!=2) {std::cerr<<"usage: short_excursions model.txt\n";return 2;}
 std::ifstream in(argv[1]); int n,m;
 uint64_t mask,pattern,killing,seed,trials;
 in>>n>>m>>mask>>pattern>>killing>>seed>>trials;
 if(!in||n<1||n>64||killing==0||trials==0) return 3;
 std::vector<Move> moves(m);std::vector<uint64_t> cumulative,rcumulative;
 std::vector<int> relevant;uint64_t total=0,rtotal=0;
 for(int k=0;k<m;k++) {
  auto &a=moves[k];in>>a.type>>a.i>>a.j>>a.inverse>>a.weight;
  if(!in||a.i<0||a.i>=n||a.weight==0) return 4;
  total+=a.weight;cumulative.push_back(total);
  uint64_t support=(uint64_t(1)<<a.i);
  if(a.type) support|=(uint64_t(1)<<a.j);
  if(support&mask) {relevant.push_back(k);rtotal+=a.weight;rcumulative.push_back(rtotal);}
 }
 if(rtotal==0) return 5;
 std::mt19937_64 rng(seed);
 std::uniform_int_distribution<uint64_t> first(0,rtotal-1),event(0,total+killing-1);
 uint64_t successes=0,exits=0,steps=0,largest=0;
 for(uint64_t trial=0;trial<trials;trial++) {
  uint64_t x=rng();if(n<64)x&=((uint64_t(1)<<n)-1);x=(x&~mask)|pattern;
  auto k=std::upper_bound(rcumulative.begin(),rcumulative.end(),first(rng))-rcumulative.begin();
  x=moves[relevant[k]].apply(x);
  if((x&mask)==pattern)continue;exits++;uint64_t count=0;
  while(true) {
   count++;uint64_t v=event(rng);
   if(v<killing){successes++;break;}v-=killing;
   auto a=std::upper_bound(cumulative.begin(),cumulative.end(),v)-cumulative.begin();
   x=moves[a].apply(x);if((x&mask)==pattern)break;
  }
  steps+=count;largest=std::max(largest,count);
 }
 std::cout<<std::setprecision(17)<<"{\"trials\":"<<trials<<",\"successes\":"<<successes
 <<",\"initial_exits\":"<<exits<<",\"events\":"<<steps<<",\"initial_boundary_proposals\":"<<trials
 <<",\"total_proposal_calls\":"<<steps+trials<<",\"max_events_one_trial\":"<<largest
 <<",\"theta_hat\":"<<double(successes)/trials<<",\"total_weight\":"<<total
 <<",\"relevant_weight\":"<<rtotal<<",\"killing_weight\":"<<killing<<"}\n";
}
