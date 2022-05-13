# Introduction




# Purpose


# Data

Data was copied from this repository (https://github.com/ohmsha/PyOptBook/tree/main/4.coupon)

## Customer data

| Name        | Description                                                                                                                     |
|-------------|---------------------------------------------------------------------------------------------------------------------------------|
| customer_id | Unique ID of customers (An integer between 1-5000)                                                                                                 |
| age_cat     | Age category of customers:<br /> > age\~19<br /> > age20\~34<br /> > age35\~49<br /> > age50\~                                                              |
| freq_cat    | Category by number of conversion in last year:<br /> > freq0: No conversion<br /> > freq1: Once<br /> > freq2: Twice<br /> > freq3\~: Three times or more |


## Conversion probability data

| Name       | Description                                                                                                                      |
|------------|----------------------------------------------------------------------------------------------------------------------------------|
| age_cat    | Age category of customers:<br /> > age\~19<br /> > age20\~34<br /> > age35\~49<br /> > age50\~                                                               |
| freq_cat   | Category by number of conversion in last year:<br /> > freq0: No conversion<br /> > freq1: Once<br /> > freq2: Twice<br /> > freq3~: Three times or more |
| segment_id | Unique ID of segment for unique combination of age_cat and freq_cat:(An integer between 1-16)                                    |
| prob_dm1   | Probability of conversion when customers receive no coupon.                                                                      |
| prob_dm2   | Probability of conversion when customers receive 10 USD coupon.                                                                  |
| prob_dm3   | Probability of conversion when customers receive 20 USD coupon.                                                                  |