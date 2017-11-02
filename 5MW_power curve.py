__author__ = 'sebasanper'
#  GNUPLOT FIT: fit f(x) 'measured.dat' using 3:($7-5) via 'start.par'
#  Diameter 126 m
#  Hub height: 90 m
#  0.46 Thrust Coefficient Ct between 4 and 11 m/s

def power5MW_kW(U):
    if U < 3.0:
        return 0.0
    elif U < 11.76:
        return -7.99901 * U ** 3.0 + 235 * U ** 2.0 - 1487.76 * U + 2880.96
    elif U < 25.0:
        return 5000.0
    else:
        return 0.0
