# Introduction




# Purpose

Imagine you are tasked to decide the amount of budget for the use of direct mail marketing of one of your EC sites.



This repository gives a sample 

<br /><br />

# Data

Data was copied from this repository (https://github.com/ohmsha/PyOptBook/tree/main/4.coupon)

There are two data files used:

- customer data ("./data/external/customers.csv")
- conversion probablity data ("./data/external/visit_probability.csv")


## Customer data

| Name        | Description                                                                                                                     |
|-------------|---------------------------------------------------------------------------------------------------------------------------------|
| customer_id | Unique ID of customers (An integer between 1-5000).                                                                                                 |
| age_cat     | Age category of customers:<br /> - age\~19<br /> - age20\~34<br /> - age35\~49<br /> - age50\~                                                              |
| freq_cat    | Category by number of conversion in last year:<br /> - freq0: No conversion<br /> - freq1: Once<br /> - freq2: Twice<br /> - freq3\~: Three times or more |

![](./data/image/customer_heatmap.jpg)


## Conversion probability data

| Name       | Description                                                                                                                      |
|------------|----------------------------------------------------------------------------------------------------------------------------------|
| age_cat    | Age category of customers:<br /> - age\~19<br /> - age20\~34<br /> - age35\~49<br /> - age50\~                                                               |
| freq_cat   | Category by number of conversion in last year:<br /> - freq0: No conversion<br /> - freq1: Once<br /> - freq2: Twice<br /> - freq3~: Three times or more |
| segment_id | Unique ID of customer segment for unique combination of age_cat and freq_cat (An integer between 1-16).                                    |
| prob_dm1   | Probability of conversion when customers receive no direct mail *(DM1)*.                                                                      |
| prob_dm2   | Probability of conversion when customers receive a direct mail with 10 USD coupon *(DM2)*.                                                                  |
| prob_dm3   | Probability of conversion when customers receive a direct mail with 20 USD coupon *(DM3)*.                                                                  |

![](./data/image/segment_prob.jpg)

![](./data/image/parallel_plot_of_conversion_probability.jpg)

<br /><br />

# Model
## Define notations
Let ![](https://latex.codecogs.com/gif.latex?x_%7Bs%2Cd%7D) denote the probability to send the customer segment ![](https://latex.codecogs.com/gif.latex?s) the direct mail type ![](https://latex.codecogs.com/gif.latex?d), where ![](https://latex.codecogs.com/gif.latex?s%20%5Cin%20%5C%7B1%2C2%2C...%2C16%5C%7D%20%3D%20S) and ![](https://latex.codecogs.com/gif.latex?d%20%5Cin%20%5C%7Bdm1%2Cdm2%2Cdm3%5C%7D%20%3D%20D), which means there are 16 different types of customers (in this time's example, defined by customer age group and last year conversion frequency group; and three different types of direct mail.

Each direct mail type represents:
- ![](https://latex.codecogs.com/gif.latex?dm1): No direct mail sent. The default option.
- ![](https://latex.codecogs.com/gif.latex?dm2): A direct mail with with 10 USD coupon sent.
- ![](https://latex.codecogs.com/gif.latex?dm3): A direct mail with with 20 USD coupon sent.

The same index notations will be used hereinafter.

Let ![](https://latex.codecogs.com/gif.latex?p_%7Bs%2Cd%7D) denote the probability of conversion when the customers belonging to segment ![](https://latex.codecogs.com/gif.latex?s) receive the direct mail of type ![](https://latex.codecogs.com/gif.latex?d).

Let ![](https://latex.codecogs.com/gif.latex?c_%7Bd%7D) denote the amount of coupon attached to each direct mail types. We will ignore the non-coupon costs in this study.

Let ![](https://latex.codecogs.com/gif.latex?N_%7Bs%7D) denote the number of customers belonging to the segment ![](https://latex.codecogs.com/gif.latex?s).

<br /><br />

## Formulate objectives and constraints
### Objective: maximizing the expected increase of conversion
By optimizing ![](https://latex.codecogs.com/gif.latex?x_%7Bs%2Cd%7D), we want to maximize the increase of conversion by sending direct mails. This leads the maximization of the following:

![](https://latex.codecogs.com/gif.latex?%5Csum_%7Bs%20%5Cin%20S%7D%5Csum_%7Bd%20%5Cin%20D%7DN_%7Bs%7D%28p_%7Bs%2Cd%7D-p_%7Bs%2C1%7D%29x_%7Bs%2Cd%7D)
<br /><br />

### Constraint 1: the sum of probabilities to the same segment for all direct mail type is 1
![](https://latex.codecogs.com/gif.latex?%5Csum_%7Bd%20%5Cin%20D%7Dx_%7Bs%2Cd%7D%20%5C%20%5C%20%28s%5Cin%20S%29)
<br /><br />

### Constraint 2: expected total amount of coupon redeemed is within budget
Since we only care about the amount the coupon is actually redeemed, the amount is the number of (expected) conversion, rather than the number of coupons sent.

![](https://latex.codecogs.com/gif.latex?%5Csum_%7Bs%20%5Cin%20S%7D%5Csum_%7Bd%20%5Cin%20D%7DN_%7Bs%7D%20%5Ccdot%20c_%7Bs%2Cd%7D%20%5Ccdot%20x_%7Bs%2Cd%7D%20%5Cleq%20max%20%5C%20budget)
<br /><br />

### Constraint 3: letting any types of direct mail cover at least 10% of customers of every segment

![](https://latex.codecogs.com/gif.latex?x_%7Bs%2Cd%7D%20%5Cgeq%200.1%20%5C%20%5C%20%28x%20%5Cin%20S%2C%20d%20%5Cin%20D%29)

<br /><br />

# Result
## Fixed budget
For the ease of the problem, let's first remove some flexibility and define the followings as exogenous parameters:
- ![](https://latex.codecogs.com/gif.latex?c_%7Bdm1%7D%20%3D%200), ![](https://latex.codecogs.com/gif.latex?c_%7Bdm2%7D%20%3D%2010), and ![](https://latex.codecogs.com/gif.latex?c_%7Bdm3%7D%20%3D%2020).
- ![](https://latex.codecogs.com/gif.latex?max%20%5C%20budget%20%3D%2010%2C000)

This notebook (./opt_step_by_step.ipynb) gives the modeling walkthrough using `Pulp`. 

Here's the heatmap of ![](https://latex.codecogs.com/gif.latex?x_%7Bs%2Cd%7D).

The results indicate that for the group with no purchase last year except for age20\~34, we should send some coupon and particularly the group age50\~ will appreciate the higher valued coupon more. 

And here's the heatmap of ![](https://latex.codecogs.com/gif.latex?N_%7Bs%7Dx_%7Bs%2Cd%7D)

<br /><br />

## Variable budget and finding optimal
Then let's see how we can solve the original question: defining the optimal amount of budget.

Then what we next think of should be "to what we optimize?" We are likely to have monotonically more conversions as the budget increases, because it will give chances to send more coupon and more coupon results in more conversions. So, if we say the increase of conversions is what we target, it will end with "the best coupon for everyone". Intuitively this is not right, but why?

This is because we first distribute the coupons to the customers with the most possiblity of conversions (i.e. "low-hanging fruit") and as we keep going, the fruits go higher and higher until in the end we will reach the point when it makes no sense to add budget.

<br />

If we formulate this situation, we want to stop the budget at the point when the expected increase of sales from conversions will get less than the increase of budget: meaning even if we add more budget the expected sales is less than the additional budget--we will lose money if we go farther.

This can be discussed looking at the ROI (return on investment).

![](https://latex.codecogs.com/gif.latex?ROI%20%3D%20%5Cfrac%7Bexpected%20%5C%20increase%20%5C%20of%20%5C%20sales%7D%7Bbudget%20%5C%20amount%7D%20%3D%20%5Cfrac%7Bexpected%20%5C%20increase%20%5C%20of%20%5C%20conversion*unit%20%5C%20sales%7D%7Bbudget%20%5C%20amount%7D)

And maximizing ROI will give the cutoff point to increase the budget. There, the increase of denominator gets more than the increase of numerator.

Now there we have ![](https://latex.codecogs.com/gif.latex?unit%20%5C%20sales) as a new exogenous parameter. These are all the exogenous parameters and their inputs for our case study this time:
- ![](https://latex.codecogs.com/gif.latex?c_%7Bdm1%7D%20%3D%200), ![](https://latex.codecogs.com/gif.latex?c_%7Bdm2%7D%20%3D%2010), and ![](https://latex.codecogs.com/gif.latex?c_%7Bdm3%7D%20%3D%2020).
- ![](https://latex.codecogs.com/gif.latex?unit%20%5C%20sales%3D30)

<br />


xxxxxxxxxxxxx

<br /><br />

# What's Next

Giving more flexibility
- variable budget -> objective function. no longer linear.
- variable coupon values -> natural to assume the conversion probability will also change, but need predictive modeling here, like using ML models.
How to get probability data? 
Prediction including ML
Causality

ROI evaluation
change of coupon amount
LIP -> metaheuristic

MLOps
