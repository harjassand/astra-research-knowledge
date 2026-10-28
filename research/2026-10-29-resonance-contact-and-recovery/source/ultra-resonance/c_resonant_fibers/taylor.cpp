// Exact fixed-point interval Taylor steps for the nonlinear resonant Bloch flow.
// The source's N-site Hilbert space is never allocated. Local intervals restart
// from the returned point; the Python consumer pays accumulated errors using
// the proved rotational stability, rather than silently discarding wrapping.
#include <algorithm>
#include <array>
#include <cassert>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

using Z=__int128_t;
using L=int64_t;
static L D;
static uint64_t adds=0,mults=0,divs=0;
static Z biggest=0;

Z floor_div(Z a,Z b){assert(b>0);Z q=a/b,r=a%b;return q-(r<0);}
Z ceil_div(Z a,Z b){return -floor_div(-a,b);}
L narrow(Z a){assert(a>-(Z(1)<<62)&&a<(Z(1)<<62));biggest=std::max(biggest,a<0?-a:a);return L(a);}
std::string zs(Z a){if(a==0)return "0";bool neg=a<0;if(neg)a=-a;std::string s;while(a){s.push_back(char('0'+a%10));a/=10;}if(neg)s.push_back('-');std::reverse(s.begin(),s.end());return s;}
struct I{L l=0,u=0;I(){}I(L a,L b):l(a),u(b){assert(a<=b);}};
I operator+(I a,I b){++adds;return {narrow(Z(a.l)+b.l),narrow(Z(a.u)+b.u)};}
I operator-(I a){return {narrow(-Z(a.u)),narrow(-Z(a.l))};}
I operator-(I a,I b){return a+-b;}
I operator*(I a,I b){++mults;Z x[]={Z(a.l)*b.l,Z(a.l)*b.u,Z(a.u)*b.l,Z(a.u)*b.u};auto mm=std::minmax_element(x,x+4);return {narrow(floor_div(*mm.first,D)),narrow(ceil_div(*mm.second,D))};}
I scale(I a,L k){if(k<0)return -scale(a,-k);return {narrow(Z(a.l)*k),narrow(Z(a.u)*k)};}
I divide(I a,L k){assert(k>0);++divs;return {narrow(floor_div(a.l,k)),narrow(ceil_div(a.u,k))};}
using V=std::array<I,3>;
V cross(V a,V b){return {a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]};}

int main(int argc,char**argv){
    assert(argc==3);
    auto start=std::chrono::steady_clock::now();
    std::ifstream input(argv[1]);assert(input);
    int q,steps,order,bits;L initial_rx;
    input>>q>>steps>>order>>bits>>initial_rx;
    assert(q==48&&steps==512&&order==24&&bits==48);D=L(1)<<bits;
    std::vector<I> weights(q);
    std::array<std::vector<I>,2> f{std::vector<I>(q),std::vector<I>(q)},g=f;
    for(int i=0;i<q;++i){
        input>>weights[i].l>>weights[i].u;
        for(int r=0;r<2;++r)input>>f[r][i].l>>f[r][i].u>>g[r][i].l>>g[r][i].u;
        assert(weights[i].l>0);
    }
    assert(input);
    I one(D,D),zero;
    std::vector<std::array<L,3>> points(q,{initial_rx,0,D/2});
    std::vector<std::vector<V>> y(order+1,std::vector<V>(q)),h=y;
    Z sum_local_radius=0;L largest_radius=0;
    Z three_power=1;for(int j=0;j<order;++j)three_power*=3;
    L coordinate_tail=narrow(ceil_div(Z(3)*D,three_power));
    Z largest_norm_squared=0;
    for(int step=0;step<steps;++step){
        for(int i=0;i<q;++i)for(int c=0;c<3;++c)y[0][i][c]=I(points[i][c],points[i][c]);
        for(int k=0;k<order;++k){
            I zm;
            std::array<I,2> fx{},fy{},gg{};
            for(int i=0;i<q;++i){
                zm=zm+weights[i]*y[k][i][2];
                for(int r=0;r<2;++r){
                    fx[r]=fx[r]+weights[i]*(f[r][i]*y[k][i][0]);
                    fy[r]=fy[r]+weights[i]*(f[r][i]*y[k][i][1]);
                    gg[r]=gg[r]+weights[i]*(g[r][i]*((k==0?one:zero)-y[k][i][2]));
                }
            }
            for(int i=0;i<q;++i){
                h[k][i][0]=divide(scale(f[0][i]*fx[0],3)+f[1][i]*fx[1],3);
                h[k][i][1]=divide(scale(f[0][i]*fy[0],3)+f[1][i]*fy[1],3);
                I base=(k==0?one:zero)-zm;
                h[k][i][2]=-divide(scale(base-g[0][i]*gg[0],3)+(base-g[1][i]*gg[1]),3);
                V conv{};
                for(int j=0;j<=k;++j){V z=cross(h[j][i],y[k-j][i]);for(int c=0;c<3;++c)conv[c]=conv[c]+z[c];}
                for(int c=0;c<3;++c)y[k+1][i][c]=divide(conv[c],512*(k+1)); // 2*dt=1/512
            }
        }
        L maxrad=0;
        for(int i=0;i<q;++i){
            Z normsq=0;
            for(int c=0;c<3;++c){
                I endpoint;
                for(int k=0;k<=order;++k)endpoint=endpoint+y[k][i][c];
                L mid=narrow(floor_div(Z(endpoint.l)+endpoint.u,2));
                assert(mid>=-2*D&&mid<=2*D);
                L rad=std::max(mid-endpoint.l,endpoint.u-mid)+coordinate_tail;
                maxrad=std::max(maxrad,rad);points[i][c]=mid;normsq+=Z(mid)*mid;
            }
            largest_norm_squared=std::max(largest_norm_squared,normsq);
            assert(Z(10000)*normsq<=Z(10201)*D*D); // every restart has norm <=1.01
        }
        sum_local_radius+=Z(2)*maxrad; // sqrt(3)<=2, in fixed units
        largest_radius=std::max(largest_radius,maxrad);
    }
    auto end=std::chrono::steady_clock::now();
    std::ofstream out(argv[2]);assert(out);
    out<<"{\n  \"fixed_fractional_bits\": "<<bits<<",\n  \"nodes\": "<<q<<",\n  \"steps\": "<<steps<<",\n  \"order\": "<<order<<",\n  \"interaction_clock\": \"1/2\",\n  \"time_step\": \"1/1024\",\n";
    out<<"  \"sum_local_Euclidean_error_fixed_upper\": \""<<zs(sum_local_radius)<<"\",\n  \"largest_coordinate_error_fixed_upper\": \""<<largest_radius<<"\",\n  \"coordinate_Taylor_tail_fixed_upper\": \""<<coordinate_tail<<"\",\n";
    out<<"  \"largest_restart_norm_squared_fixed\": \""<<zs(largest_norm_squared)<<"\",\n  \"largest_interval_endpoint_absolute\": \""<<zs(biggest)<<"\",\n";
    out<<"  \"interval_additions\": "<<adds<<",\n  \"interval_multiplications\": "<<mults<<",\n  \"interval_scalar_division_operations\": "<<divs<<",\n";
    out<<"  \"computation_seconds_before_serialization\": "<<std::chrono::duration<double>(end-start).count()<<",\n  \"returned_point_Bloch_fixed\": [\n";
    for(int i=0;i<q;++i){out<<"    [\""<<points[i][0]<<"\", \""<<points[i][1]<<"\", \""<<points[i][2]<<"\"]"<<(i+1<q?",":"")<<"\n";}
    out<<"  ],\n  \"source_N_loop\": false,\n  \"state_vector_or_density_matrix_allocated\": false\n}\n";
    std::cout<<"PASS exact interval Taylor; "<<steps<<" steps, "<<q<<" modes; seconds="<<std::chrono::duration<double>(end-start).count()<<"\n";
}
