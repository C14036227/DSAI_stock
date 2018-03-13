# DSAI_stock
##  DSAI Hw1, predict stock, beat buy-and-hold

---

This project is to make more money than buy-and-sold strategy

Using "Moving average" to accomplish the goal

* If short-term average crosses long-term and going downwards, it`s time to sell
* If short-term average crosses long-term and going upwards, it`s time to buy
* Moving Average: 
**  5, 20, 60, 180 days
**  to calculate the average from past days

version 1 is only considered 5-days line with other lines 
* 'sig1' 'sig2' 'sig3' are three signals, which means two MA lines crossed
* 'rule1' : 5 MA line is higher and crossed, buy
* 'rule2' : 5 MA line is lower and crossed, sell



import packages: numpy, pandas, matplotlib

