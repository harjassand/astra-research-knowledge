#include <algorithm>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <iomanip>
#include <iostream>
#include <random>
#include <vector>
using namespace std;
using Clock=chrono::steady_clock;
struct Query{ double x,t; };
struct Edit{ int j; double u; };

struct Fenwick {
  int n; vector<double> bit;
  Fenwick(const vector<double>& a):n((int)a.size()),bit(n+1,0.0){
    for(int j=0;j<n;j++) bit[j+1]=a[j];
    for(int i=1;i<=n;i++){int p=i+(i&-i);if(p<=n)bit[p]+=bit[i];}
  }
  double sum(int end) const { double s=0; for(int i=end;i;i-=i&-i)s+=bit[i];return s; }
  void add(int j,double d){for(int i=j+1;i<=n;i+=i&-i)bit[i]+=d;}
};

struct RMQ {
  int n,P; vector<double> mn,lazy; vector<int> arg;
  RMQ()=default;
  explicit RMQ(const vector<double>& v){ build(v); }
  void build(const vector<double>& v){
    n=(int)v.size();P=1;while(P<n)P*=2;
    mn.assign(2*P,INFINITY);lazy.assign(2*P,0.0);arg.assign(2*P,-1);
    for(int i=0;i<n;i++){mn[P+i]=v[i];arg[P+i]=i;}
    for(int p=P-1;p;p--)pull(p);
  }
  void pull(int p){int a=2*p,b=a+1;if(mn[a]<=mn[b]){mn[p]=mn[a];arg[p]=arg[a];}else{mn[p]=mn[b];arg[p]=arg[b];}}
  void apply(int p,double d){mn[p]+=d;lazy[p]+=d;}
  void push(int p){if(lazy[p]!=0){apply(2*p,lazy[p]);apply(2*p+1,lazy[p]);lazy[p]=0;}}
  void add(int ql,int qr,double d){if(ql<qr&&d!=0) addrec(1,0,P,ql,qr,d);}
  void addrec(int p,int l,int r,int ql,int qr,double d){
    if(ql<=l&&r<=qr){apply(p,d);return;}
    push(p);int m=(l+r)/2;
    if(ql<m)addrec(2*p,l,m,ql,qr,d);
    if(qr>m)addrec(2*p+1,m,r,ql,qr,d);
    pull(p);
  }
  void setpoint(int idx,double val){setrec(1,0,P,idx,val);}
  void setrec(int p,int l,int r,int idx,double val){
    if(r-l==1){mn[p]=val;arg[p]=idx;lazy[p]=0;return;}
    push(p);int m=(l+r)/2;if(idx<m)setrec(2*p,l,m,idx,val);else setrec(2*p+1,m,r,idx,val);pull(p);
  }
  double minimum()const{return mn[1];}
};

static inline double cand(const Query&q,double a,double b,double u,double ca,double cb){
  double y=q.x-q.t*u;
  if(y<a)return ca+(q.x-a)*(q.x-a)/(2*q.t);
  if(y>b)return cb+(q.x-b)*(q.x-b)/(2*q.t);
  return ca+u*(q.x-a)-0.5*q.t*u*u;
}
static inline double leftcand(const Query&q,double x0,double u){
  double y=q.x-q.t*u;
  if(y<=x0)return u*(q.x-x0)-.5*q.t*u*u;
  return (q.x-x0)*(q.x-x0)/(2*q.t);
}
static inline double rightcand(const Query&q,double xn,double u,double c){
  double y=q.x-q.t*u;
  if(y>=xn)return c+u*(q.x-xn)-.5*q.t*u*u;
  return c+(q.x-xn)*(q.x-xn)/(2*q.t);
}
vector<double> potential_values(const vector<double>& breaks,const vector<double>& state,
                                const vector<Query>& qs,double left,double right){
  int n=(int)state.size();vector<double> c(n+1,0.0);
  for(int j=0;j<n;j++)c[j+1]=c[j]+state[j]*(breaks[j+1]-breaks[j]);
  vector<double> out(qs.size());
  for(size_t qi=0;qi<qs.size();qi++){
    const auto&q=qs[qi];double m=min(leftcand(q,breaks[0],left),rightcand(q,breaks[n],right,c[n]));
    for(int j=0;j<n;j++)m=min(m,cand(q,breaks[j],breaks[j+1],state[j],c[j],c[j+1]));
    out[qi]=m;
  }
  return out;
}

static inline double column_cost(const Query&q,int col,const vector<double>&breaks,
                                const vector<double>&state,const vector<double>&c,
                                double left,double right){
  int n=(int)state.size();
  if(col==0)return leftcand(q,breaks[0],left);
  if(col==n+1)return rightcand(q,breaks[n],right,c[n]);
  int j=col-1;return cand(q,breaks[j],breaks[j+1],state[j],c[j],c[j+1]);
}
void smawk_rec(const vector<int>& rows,const vector<int>& cols,
               const vector<Query>&qs,const vector<double>&breaks,
               const vector<double>&state,const vector<double>&c,
               double left,double right,vector<int>&argmin,long long& evals){
  if(rows.empty())return;
  vector<int> reduced;reduced.reserve(min(rows.size(),cols.size()));
  for(int col:cols){
    while(!reduced.empty()){
      int row=rows[reduced.size()-1];
      double newer=column_cost(qs[row],col,breaks,state,c,left,right);evals++;
      double older=column_cost(qs[row],reduced.back(),breaks,state,c,left,right);evals++;
      if(newer<older)reduced.pop_back();else break;
    }
    if(reduced.size()<rows.size())reduced.push_back(col);
  }
  vector<int> odd;odd.reserve(rows.size()/2);
  for(size_t i=1;i<rows.size();i+=2)odd.push_back(rows[i]);
  smawk_rec(odd,reduced,qs,breaks,state,c,left,right,argmin,evals);
  for(size_t i=0;i<rows.size();i+=2){
    int lo=0,hi=(int)reduced.size()-1;
    if(i>0){auto it=lower_bound(reduced.begin(),reduced.end(),argmin[rows[i-1]]);lo=(int)(it-reduced.begin());}
    if(i+1<rows.size()){auto it=lower_bound(reduced.begin(),reduced.end(),argmin[rows[i+1]]);hi=(int)(it-reduced.begin());}
    double best=INFINITY;int bestcol=reduced[lo];
    for(int k=lo;k<=hi;k++){
      double v=column_cost(qs[rows[i]],reduced[k],breaks,state,c,left,right);evals++;
      if(v<best){best=v;bestcol=reduced[k];}
    }
    argmin[rows[i]]=bestcol;
  }
}

vector<double> grouped_smawk_values(const vector<double>&breaks,const vector<double>&state,
                                    const vector<Query>&qs,const vector<vector<int>>&groups,
                                    double left,double right,long long&evals){
  int n=(int)state.size();vector<double> c(n+1,0.0);
  for(int j=0;j<n;j++)c[j+1]=c[j]+state[j]*(breaks[j+1]-breaks[j]);
  vector<double> out(qs.size());evals=0;
  vector<int> cols(n+2);for(int j=0;j<n+2;j++)cols[j]=j;
  for(const auto&g:groups){
    vector<int> rows(g.size());for(size_t k=0;k<g.size();k++)rows[k]=(int)k;
    vector<Query> sortedq;sortedq.reserve(g.size());for(int i:g)sortedq.push_back(qs[i]);
    vector<int> arg(g.size(),-1);
    smawk_rec(rows,cols,sortedq,breaks,state,c,left,right,arg,evals);
    for(size_t k=0;k<g.size();k++)out[g[k]]=column_cost(sortedq[k],arg[k],breaks,state,c,left,right);
  }
  return out;
}

struct BlockEngine {
  int n,Mleaf,B,K; double left,right;
  vector<double> breaks,state;
  vector<Query> qs;
  Fenwick area;
  vector<RMQ> trees;
  BlockEngine(const vector<double>& br,const vector<double>& st,const vector<Query>& q,
              double l,double r,int block)
   :n((int)st.size()),Mleaf(n+2),B(block),K((Mleaf+B-1)/B),left(l),right(r),
    breaks(br),state(st),qs(q),area([&](){vector<double>a(n);for(int j=0;j<n;j++)a[j]=st[j]*(br[j+1]-br[j]);return a;}()){
    vector<double> pref(n+1,0.0);for(int j=0;j<n;j++)pref[j+1]=pref[j]+state[j]*(breaks[j+1]-breaks[j]);
    trees.reserve(qs.size());
    for(const auto&query:qs){vector<double> bm(K,INFINITY);for(int leaf=0;leaf<Mleaf;leaf++){
      double v;
      if(leaf==0)v=leftcand(query,breaks[0],left);
      else if(leaf<=n){int j=leaf-1;v=cand(query,breaks[j],breaks[j+1],state[j],pref[j],pref[j+1]);}
      else v=rightcand(query,breaks[n],right,pref[n]);
      bm[leaf/B]=min(bm[leaf/B],v);
    }trees.emplace_back(bm);}
  }
  double blockmin(int b,const Query&q,double c){
    int lo=b*B,hi=min((b+1)*B,Mleaf);
    double v=INFINITY;
    for(int leaf=lo;leaf<hi;leaf++){
      if(leaf==0)v=min(v,leftcand(q,breaks[0],left));
      else if(leaf<=n){int j=leaf-1;double c2=c+state[j]*(breaks[j+1]-breaks[j]);v=min(v,cand(q,breaks[j],breaks[j+1],state[j],c,c2));c=c2;}
      else v=min(v,rightcand(q,breaks[n],right,c));
    }
    return v;
  }
  void update(int j,double value){double old=state[j],d=(value-old)*(breaks[j+1]-breaks[j]);int b=(j+1)/B;
    state[j]=value;area.add(j,d);double base=area.sum(max(0,b*B-1));
    for(size_t qi=0;qi<qs.size();qi++){trees[qi].add(b+1,K,d);trees[qi].setpoint(b,blockmin(b,qs[qi],base));}
  }
  vector<double> minima()const{vector<double>x;for(const auto&t:trees)x.push_back(t.minimum());return x;}
};

int main(int argc,char**argv){
  int n=argc>1?atoi(argv[1]):1024;
  int m=argc>2?atoi(argv[2]):64;
  int reps=argc>3?atoi(argv[3]):1000;
  uint64_t seed=argc>4?strtoull(argv[4],nullptr,10):5;
  int B=argc>5?atoi(argv[5]):16;
  int L=argc>6?atoi(argv[6]):4;
  mt19937_64 gen(seed);uniform_real_distribution<double> U01(0,1), Ustate(-.8,.8), Ux(-1.8,1.8), Uw(.015,.08);
  vector<double> breaks(n+1),state(n);for(int j=0;j<=n;j++)breaks[j]=-2.0+4.0*j/n;for(double&v:state)v=Ustate(gen);
  vector<double> initial=state;
  vector<Query> q;vector<double> times(L);for(int z=0;z<L;z++)times[z]=.03+.5*z/max(1,L-1);
  for(int i=0;i<m;i++){double x=Ux(gen),w=Uw(gen),t=times[gen()%times.size()];q.push_back({x-w/2,t});q.push_back({x+w/2,t});}
  vector<Edit> edits(reps);for(auto&e:edits){e.j=gen()%n;e.u=Ustate(gen);}
  const double left=.15,right=-.12;
  vector<double> groupTimes;vector<vector<int>> groups;
  for(size_t i=0;i<q.size();i++){auto it=find(groupTimes.begin(),groupTimes.end(),q[i].t);if(it==groupTimes.end()){groupTimes.push_back(q[i].t);groups.push_back({(int)i});}else groups[it-groupTimes.begin()].push_back((int)i);}
  for(auto&g:groups)sort(g.begin(),g.end(),[&](int a,int b){return q[a].x<q[b].x;});
  auto t0=Clock::now();Fenwick area([&](){vector<double>a(n);for(int j=0;j<n;j++)a[j]=state[j]*(breaks[j+1]-breaks[j]);return a;}());
  vector<double> initialC(n+1,0.0);for(int j=0;j<n;j++)initialC[j+1]=initialC[j]+state[j]*(breaks[j+1]-breaks[j]);
  vector<RMQ> trees;trees.reserve(q.size());
  for(const auto&query:q){vector<double> v(n+2);v[0]=leftcand(query,breaks[0],left);for(int j=0;j<n;j++)v[j+1]=cand(query,breaks[j],breaks[j+1],state[j],initialC[j],initialC[j+1]);v[n+1]=rightcand(query,breaks[n],right,initialC[n]);trees.emplace_back(v);}
  auto t1=Clock::now();
  double csum=0;
  for(auto e:edits){double old=state[e.j],d=(e.u-old)*(breaks[e.j+1]-breaks[e.j]);double cleft=area.sum(e.j);for(size_t qi=0;qi<q.size();qi++){trees[qi].add(e.j+2,n+2,d);trees[qi].setpoint(e.j+1,cand(q[qi],breaks[e.j],breaks[e.j+1],e.u,cleft,cleft+e.u*(breaks[e.j+1]-breaks[e.j])));}area.add(e.j,d);state[e.j]=e.u;for(auto&tr:trees)csum+=tr.minimum();}
  auto t2=Clock::now();
  vector<double> scanstate(n);for(int j=0;j<n;j++)scanstate[j]=0; // reset below to exact same initial state
  // Recover initial field deterministically by replaying the PRNG stream.
  mt19937_64 gen2(seed);uniform_real_distribution<double> Ustate2(-.8,.8);for(double&v:scanstate)v=Ustate2(gen2);
  double ssum=0;
  for(auto e:edits){scanstate[e.j]=e.u;auto v=potential_values(breaks,scanstate,q,left,right);for(double z:v)ssum+=z;}
  auto t3=Clock::now();
  vector<double> groupstate=initial;long long gevals=0,totalgevals=0;double gsum=0;
  for(auto e:edits){groupstate[e.j]=e.u;auto v=grouped_smawk_values(breaks,groupstate,q,groups,left,right,gevals);totalgevals+=gevals;for(double z:v)gsum+=z;}
  auto t4=Clock::now();
  auto onlinefinal=vector<double>();onlinefinal.reserve(q.size());for(auto&tr:trees)onlinefinal.push_back(tr.minimum());
  auto scanfinal=potential_values(breaks,scanstate,q,left,right);
  long long finaleval=0;auto groupfinal=grouped_smawk_values(breaks,scanstate,q,groups,left,right,finaleval);
  double err=0,gerr=0;for(size_t i=0;i<q.size();i++){err=max(err,abs(onlinefinal[i]-scanfinal[i]));gerr=max(gerr,abs(groupfinal[i]-scanfinal[i]));}
  auto sec=[](auto a,auto b){return chrono::duration<double>(b-a).count();};
  long long p=1;while(p<n+2)p*=2;double mb=(double)q.size()*2*p*(sizeof(double)*2+sizeof(int))/1048576.;
  auto b0=Clock::now();BlockEngine block(breaks,initial,q,left,right,B);auto b1=Clock::now();
  double bsum=0;for(auto e:edits){block.update(e.j,e.u);for(double z:block.minima())bsum+=z;}auto b2=Clock::now();
  auto blockfinal=block.minima();double berr=0;for(size_t i=0;i<q.size();i++)berr=max(berr,abs(blockfinal[i]-scanfinal[i]));
  if(err>1e-8||gerr>1e-8||berr>1e-8||abs(csum-ssum)>1e-7||abs(bsum-ssum)>1e-7||abs(gsum-ssum)>1e-7)return 2;
  long long bp=1;while(bp<(n+2+B-1)/B)bp*=2;double bmb=(double)q.size()*2*bp*(sizeof(double)*2+sizeof(int))/1048576.;
  cout<<setprecision(10)<<"{\"N\":"<<n<<",\"M\":"<<m<<",\"Q\":"<<q.size()<<",\"proposals\":"<<reps
      <<",\"online_setup_s\":"<<sec(t0,t1)<<",\"online_updates_s\":"<<sec(t1,t2)
      <<",\"scan_recomputes_s\":"<<sec(t2,t3)<<",\"proposal_speedup\":"<<sec(t2,t3)/sec(t1,t2)
      <<",\"online_total_s\":"<<sec(t0,t2)<<",\"scan_total_s\":"<<sec(t2,t3)
      <<",\"total_speedup\":"<<sec(t2,t3)/sec(t0,t2)<<",\"tree_storage_MiB\":"<<mb
      <<",\"distinct_times\":"<<groups.size()<<",\"grouped_smawk_total_s\":"<<sec(t3,t4)
      <<",\"online_tree_vs_grouped_speedup\":"<<sec(t3,t4)/sec(t0,t2)<<",\"block_vs_grouped_speedup\":"<<sec(t3,t4)/sec(b0,b2)<<",\"grouped_eval_count_per_proposal\":"<<(double)totalgevals/reps
      <<",\"grouped_final_abs_error\":"<<gerr
      <<",\"block_size\":"<<B<<",\"block_setup_s\":"<<sec(b0,b1)<<",\"block_updates_s\":"<<sec(b1,b2)
      <<",\"block_speedup_vs_scan\":"<<sec(t2,t3)/sec(b1,b2)<<",\"block_total_speedup_vs_scan\":"<<sec(t2,t3)/sec(b0,b2)
      <<",\"block_storage_MiB\":"<<bmb<<",\"block_final_abs_error\":"<<berr
      <<",\"max_final_abs_error\":"<<err<<",\"checksum_abs_delta\":"<<abs(csum-ssum)<<",\"block_checksum_abs_delta\":"<<abs(bsum-ssum)
      <<",\"grouped_checksum_abs_delta\":"<<abs(gsum-ssum)<<",\"status\":\"pass\"}\n";
}
