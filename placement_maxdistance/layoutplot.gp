unset key
plot "hornsrev_poly.dat" w l lw 4, "data.dat" u 1:2 pt 7, "data.dat" u ($1+60):($2+60):3 w labels
pause -1
