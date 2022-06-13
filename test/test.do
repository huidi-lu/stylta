use "http://www.stata-press.com/data/r14/auto", clear

use ".\some folder\mydata.dta", clear

import delimited output.txt, rowrange(4:l) varnames(4) delimiters(space, collapse)

sysuse auto, clear

// Make a list of cars I might be interested in buying.
// This simulates a long line.
list make price mpg rep78 headroom trunk weight length turn displacement gear_ratio foreign if price<4000 | (price<5000 & rep78>3)

// Count the number of luxury cars
count if price > 6000

export excel output.xlsx, firstrow(varlabels) sheet("output1")