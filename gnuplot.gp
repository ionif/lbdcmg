set terminal pdf
set output "bars.pdf"
set boxwidth 0.5
set style fill solid
set title "Kinderminer vs. Marker Database"
set xlabel "Cell Type"
set ylabel "Percent of Kinderminer/Marker Database"
set yrange [0:1]
set autoscale x
plot "gnuplot.dat" using 2:xtic(1) with boxes
