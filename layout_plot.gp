unset key
set yrange [-10:4000]
set xrange [-10:5500]
do for [i=0:99]{
plot 'gen1_best_layout_ainslie.dat' u ($1):($2) every :::i::i pt 7,-3907/412 * x + 3907, 3907/417*(5457 - x), 3907, 0
pause -1
}
