# Introduction




# Purpose


# Data

Data was copied from this repository (https://github.com/ohmsha/PyOptBook/tree/main/4.coupon)

There are two data files used:

- customer data ("./data/external/customers.csv")
- conversion probablity data ("./data/external/visit_probability.csv")


## Customer data

| Name        | Description                                                                                                                     |
|-------------|---------------------------------------------------------------------------------------------------------------------------------|
| customer_id | Unique ID of customers (An integer between 1-5000).                                                                                                 |
| age_cat     | Age category of customers:<br /> > age\~19<br /> > age20\~34<br /> > age35\~49<br /> > age50\~                                                              |
| freq_cat    | Category by number of conversion in last year:<br /> > freq0: No conversion<br /> > freq1: Once<br /> > freq2: Twice<br /> > freq3\~: Three times or more |

![](./data/image/customer_heatmap.jpg)


## Conversion probability data

| Name       | Description                                                                                                                      |
|------------|----------------------------------------------------------------------------------------------------------------------------------|
| age_cat    | Age category of customers:<br /> > age\~19<br /> > age20\~34<br /> > age35\~49<br /> > age50\~                                                               |
| freq_cat   | Category by number of conversion in last year:<br /> > freq0: No conversion<br /> > freq1: Once<br /> > freq2: Twice<br /> > freq3~: Three times or more |
| segment_id | Unique ID of customer segment for unique combination of age_cat and freq_cat (An integer between 1-16).                                    |
| prob_dm1   | Probability of conversion when customers receive no direct mail *(DM1)*.                                                                      |
| prob_dm2   | Probability of conversion when customers receive a direct mail with 10 USD coupon *(DM2)*.                                                                  |
| prob_dm3   | Probability of conversion when customers receive a direct mail with 20 USD coupon *(DM3)*.                                                                  |

![](./data/image/segment_prob.jpg)


# Model

Let $x_{s,d}$ denote the probability to send the customer segment $s$ the DM type $d$, where $s \in [1,16]$ and $d \in {'dm1','dm2','dm3'}$. 



# Result