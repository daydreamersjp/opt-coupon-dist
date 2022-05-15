# Introduction




# Purpose

Imagine you are tasked to decide the amount of budget for the use of direct mail marketing of one of your EC sites.



This repository gives a sample 


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


# Model
## Define notations
Let $$x_{s,d}$$ denote the probability to send the customer segment $$s$$ the DM type $$d$$, where $$s \in \{1,2,...,16\} = S$$ and $$d \in \{dm1,dm2,dm3\} = D$$, which means there are 16 different types of customers (in this time's example, defined by customer age group and last year conversion frequency group; and three different types of direct mail. The same index notations will be used hereinafter.

Let $$p_{s,d}$$ denote the probability of conversion when the customers belonging to segment $$s$$ receive the direct mail of type $$d$$.

Let $$c_{d}$$ denote the amount of coupon attached to each direct mail types. $$c_{dm1} = 0$$, $$c_{dm2} = 10$$, and $$c_{dm3} = 20$$.

Let $$N_{s}$$ denote the number of customers belonging to the segment $$s$$.

We will ignore the non-coupon costs in this study.

## Formulate objectives and constraints




# Result




# What's Next

How to get probability data? 
Prediction including ML
Causality

MLOps