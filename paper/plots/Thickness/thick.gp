reset
set term pdfcairo font "Helvetica,14" size 5,5
set output 'thick_final.pdf'
set ylabel 'D_{HH} [nm]'
unset xlabel

set key above
unset colorbox

set palette defined ( 0 "#ff7b7b", 1 "#FF0000", 2 "#a70000", 3 "#4e91fd", 4 "#2c2cff", 5 "#00059f", 6 "#1E5631", 7 "#A4DE02", 8 "#cc7722", 9 "#76BA1B", 10 "#4C9A2A", 11 "#888888", 12 "#cccccc")


set xtics ('Slipids' 0, 'Charmm36' 1, 'LIPID17' 2, 'Berger' 3, 'Gromos43a1-s3' 4, 'Gromos-CKP' 5, 'Martini 2.2' 6, 'Martini 3.0 beta 3.2' 7, 'Sirah 2.1' 8, 'Martini 2.2p' 9, 'Martini 2.3p' 10, 'Dry Martini (2014)' 11, 'Dry Martini (2016)' 12) rotate by 45 right

set xrange [-1:13]

#set xtics border in scale 0,0 nomirror rotate by 90  offset character -1, -4, 0


set style rect fc lt -1 fs solid 0.15 noborder

#set obj rect from -1, 0.631 to 14, 0.654
#set obj rect from -1, 0.668 to 14, 0.695


p 'thick.dat' u 0:2:3 w yerr lc 'black' lw 1.5 notitle, 'thick.dat' u 0:2:0 w p palette lw 5 pt 7 ps 1 notitle, 'thick.dat' u 0:2 w p lw 1 pt 6 ps 1.35 lc 'black' notitle, 3.7 w l dt 2 lw 3 lc 'black' t 'Kučerka et al. (2006)', 3.65 w l dt 4 lw 3 lc 'black' t 'Kučerka et al. (2011)'

