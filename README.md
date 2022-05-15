# Introduction


# Purpose

Imagine you are tasked to decide the amount of budget for the use of direct mail marketing of one of your EC sites.

<img src="./data/image/diagram_dm_sending.jpg" width=500>


This repository gives a sample 

<img src="./data/image/diagram_optimization_walkflow.jpg" width=750>


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

<img src="./data/image/customer_heatmap.jpg" width=300>


## Conversion probability data

| Name       | Description                                                                                                                      |
|------------|----------------------------------------------------------------------------------------------------------------------------------|
| age_cat    | Age category of customers:<br /> - age\~19<br /> - age20\~34<br /> - age35\~49<br /> - age50\~                                                               |
| freq_cat   | Category by number of conversion in last year:<br /> - freq0: No conversion<br /> - freq1: Once<br /> - freq2: Twice<br /> - freq3~: Three times or more |
| segment_id | Unique ID of customer segment for unique combination of age_cat and freq_cat (An integer between 1-16).                                    |
| prob_dm1   | Probability of conversion when customers receive no direct mail *(DM1)*.                                                                      |
| prob_dm2   | Probability of conversion when customers receive a direct mail with 10 USD coupon *(DM2)*.                                                                  |
| prob_dm3   | Probability of conversion when customers receive a direct mail with 20 USD coupon *(DM3)*.                                                                  |

<img src="./data/image/segment_prob.jpg" width=400>

<img src="./data/image/parallel_plot_of_conversion_probability.jpg" width=400>

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
![](https://latex.codecogs.com/gif.latex?%5Csum_%7Bd%20%5Cin%20D%7Dx_%7Bs%2Cd%7D%3D1%20%5C%20%5C%20%28s%20%5Cin%20S%29)
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

Here's the heatmap of the distribution probabilities (![](https://latex.codecogs.com/gif.latex?x_%7Bs%2Cd%7D)).

<img src="./data/image/heatmap_dm_proportion_10000.jpg" width=750>

The results indicate that for the group with no purchase last year except for age20\~34, we should send some coupon and particularly the group age50\~ will appreciate the higher valued coupon more. 

And here's the heatmap of the count of mails (![](https://latex.codecogs.com/gif.latex?N_%7Bs%7D%20%5Ccdot%20x_%7Bs%2Cd%7D)).

<img src="./data/image/heatmap_dm_number_10000.jpg" width=750>

<br />

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

<img src="./data/image/diagram_optimize_budget.jpg" width=750>

The approach here is to repeat the optimizations again and again over the multiple budget inputs, calculate the ROI for each, and choose the scenario with the largest ROI.

It's worth noting that under each budget scenario, the mail distribution is always optimized so that it will generate the most conversion increase. Therefore, the mail distribution ratios are all different per scenario.

<br />

The notebook XXXXXXXXXXXXXXXXXXX gives the walkthrough of this experiment. The optimizations were repeated every 1,000 USD increment from 5,000 USD to 50,000 USD.

This chart shows the increase of the conversion against the increase of the budget.

<img src="./data/image/scatter_plot_budget_and_conversion_increase.jpg" width=500>

The increase of the conversion is slightly away upward from the diagonal line, which means the uplift of the conversions decays as "low-hanging fruit" is trimmed earlier phase.

<br />

Then this chart shows the ROIs.

<img src="./data/image/scatter_plot_budget_vs_roi.jpg" width=500>

Now we got the champion at the budget of 18,000 USD. If the budget is less than 18,000 USD we miss further gaining opportunity, while if the budget is more than 18,000 USD we will just lose money because we cannot expect the sales is more than we pay.

<br />

Finally we see the grand best solution for the mail distribution with budget 18,000 USD.

<img src="./data/image/heatmap_dm_proportion_number_18000.jpg" width=750>

<br /><br />

# Let's Reveiw the Results
Here let's review the results and discuss what we can think next.

## Can we use budget amount as the decision variable and ROI as the objective?

We can use budget amount as another decision variable and ROI as the objective of the problem. Actually it is more direct. The only reason I did not do that way was because it would make the program non-linear.

The objective function will be like:

![](https://latex.codecogs.com/gif.latex?%5Cfrac%7B%5Csum_%7Bs%20%5Cin%20S%7D%20%5Csum_%7Bd%20%5Cin%20D%7D%20N_%7Bs%7D%28p_%7Bs%2Cd%7D-p_%7Bs%2C1%7D%29x_%7Bs%2Cd%7D%20%5Ccdot%20unit%20%5C%20of%20%5C%20sales%7D%7Bbudget%7D)

Because the decision variable appears both in numerator and denominator, it makes the objective non-linear. Then it goes out of the scope of Python library 'Pulp'.

Since there are many non-linear solvers, it is not a complete deal breaker but I took a simplified approach here.

<br />

## Isn't ROI too low in the case study?

Actually it is. It was 2.25% against the investment of 18,000 USD, which is around 400 USD. This amount of return agains as much investment as 18,000 USD is just a joke--particularly so when we remember we did not take the non-coupon cost or indirect cost out of consideration in this study.

Based on this analysis, just giving up the plan is an idea: we are not a lot better off than executing plan and being disappointed later.

Another considerations may come if we:
- do an adjustment of coupon value. This should be followed by the change of conversion probabilities; as a matter of course, it is natural to believe the coupon value changes cause shifts of their conversion probabilities.
- do a better job in customer segmentation. Again this should lead to the redraft of conversion probabilities.
- grow the customer base. This should be more business-driven approach and will need many got involved but could be fruitful when successful.





Giving more flexibility
- variable coupon values -> natural to assume the conversion probability will also change, but need predictive modeling here, like using ML models.
How to get probability data? 
Prediction including ML
Causality

 (remember here we parameterize the sales per conversion is 30 USD. If the unit sales is different, the ROI curve is also different)

change of coupon amount
LIP -> metaheuristic

MLOps
