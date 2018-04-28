## PROCOP: 

This repository contains open sourced implementations of the software tools included with the
textbook [Copolymerization: Toward a Systematic Approach](http://a.co/3805acW) by Cornel Hagiopol.

### Reactvity Ratios Estimation with Gradient Descent:

The program `ReactivityRatios.py` estimates reactivity ratios `r1` and `r2` by applying gradient descent 
according to the paper [An Improved Method of Calculating Copolymerization Reactivity Ratios](https://onlinelibrary.wiley.com/doi/abs/10.1002/pol.1965.100030137)
by Paul Tidwell and George Mortimer. The notes below show the cost function derivatives and update rule implemented
in the code.

![](figures/equations.PNG)
