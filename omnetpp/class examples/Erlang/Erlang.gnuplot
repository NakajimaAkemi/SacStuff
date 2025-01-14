set terminal pngcairo enhanced font "Helvetica,12"
set output "TrespErlang.png"

rho=0.8

set xlabel "K"
set ylabel "Time [s]"
set key top left
set pointsize 1.5
p [][0:]\
"results/sens_K_erlang.data" using 1:12:13 title "T_{Resp} (sim)" with errorbars linecolor 1 pointtype 4, \
"results/sens_K_erlang.data" using 1:12 notitle with lines linecolor 1, \
"results/sens_K_erlang.data" using 1:8:9 title "T_{Srv} (sim)" with errorbars linecolor 2 pointtype 5, \
"results/sens_K_erlang.data" using 1:8 notitle with lines linecolor 2, \
"results/sens_K_erlang.data" using 1:10:11 title "T_{Wait} (sim)" with errorbars linecolor 3 pointtype 6, \
"results/sens_K_erlang.data" using 1:10 notitle with lines linecolor 3, \


#0.1*(1+ ((1+(x)**2)/2)*rho/(1-rho))+0.1 title "M/G/1 (theory)" with lines linecolor 6, \
#0.1*(1/(1-rho))+0.1 title "M/M/1 (theory)" with lines linecolor 7


set output "HistErlang.png"

# Ln f(x; k, mu)
# Commonly, we denote a = alpha = k and b = beta = 1/mu.
ln_f(x, a, b) = a*log(b) - lgamma(a) + (a-1)*log(x) - b*x

# f(x; k, mu)
f(x, k, mu) = (x<0)? 0 : (x==0)? ((k<1)? 1/0 : (k==1)? mu : 0) : (mu==0)? 0 : exp(ln_f(x, k, 1.0/mu))

rho=0.8

sumfile(f)= real(system(sprintf("awk '{ sum += $2 } END { print sum }'  %s", f)))
interfile1(f)= real(system(sprintf("tail -n2 %s | cut -f1", f)))
interfile2(f)= real(system(sprintf("tail -n-1 %s | head -n1 | cut -f1", f)))
interfile3(f)= real(system(sprintf("head -n3 %s | tail -n1 | cut -f1", f)))
normalize(f)=1.0/(sumfile(f)*interfile3(f))

set xlabel "T_{Resp} [s]"
set ylabel "PDF"
set key top right
set pointsize 1.5
p [0:5][]\
"results/Erlang_K1_SinkTimeH.data" using ($1):($2*(normalize("results/Erlang_K1_SinkTimeH.data"))) title "K=1" with linespoints linecolor 1 pointtype 4, \
f(x, 1.0, 0.5) notitle linecolor 1, \
"results/Erlang_K2_SinkTimeH.data" using ($1):($2*(normalize("results/Erlang_K2_SinkTimeH.data"))) title "K=2" with linespoints linecolor 2 pointtype 5, \
f(x, 2.0, 0.5) notitle linecolor 2, \
"results/Erlang_K3_SinkTimeH.data" using ($1):($2*(normalize("results/Erlang_K3_SinkTimeH.data"))) title "K=3" with linespoints linecolor 3 pointtype 6, \
f(x, 3.0, 0.5) notitle linecolor 3, \
"results/Erlang_K4_SinkTimeH.data" using ($1):($2*(normalize("results/Erlang_K4_SinkTimeH.data"))) title "K=4" with linespoints linecolor 4 pointtype 7, \
f(x, 4.0, 0.5) notitle linecolor 4

