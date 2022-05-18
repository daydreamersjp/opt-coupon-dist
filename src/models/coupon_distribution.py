"""
A module to do optimization for planning coupon distritbuion.
"""

import sys
import time
from typing import Tuple, Union
import logging
import pandas as pd
import pulp
import matplotlib.pyplot as plt
import seaborn as sns

NumberTypes = (int, float, complex)

logging.basicConfig(
    stream=sys.stdout,
    format="%(levelname)s %(asctime)s - %(message)s",
    level=logging.INFO)
logger = logging.getLogger()


class CouponDistribution:
    """
    Class to load data, execute optimization, and visualize results for
    coupon distribution planning.
    """

    def __init__(self):
        # Initialize object attributes before assignment.
        self.df_cust = None
        self.df_prob = None
        self._ls_dm = None
        self.df_prob_long = None
        self.df_cust_prob = None
        self.dict_dm_cost = None
        self.unit_sales = None
        self.min_dist_ratio = None
        self.max_budget = None
        self.df_seg_send_prob = None
        self.profit = None
        self.profit_status_quo = None
        self.inc_profit = None

    def load_data(self, customer_data_path: str,
                  segment_prob_data_path: str) -> None:
        """
        Load csv files from paths.

        Customer data given by 'customer_data_path' needs to have
        the following columns.
        - customer_id: str - Unique customer id
        - age_cat: str - Age category of the customer
        - freq_cat: str - Category of past conversion frequency

        Data of probabilities of conversion by type of direct mails
        needs to have the following columns.
        - age_cat: str - Age category of the customer
        - freq_cat: str - Category of past conversion frequency
        - segment_id: str - Unique segment id
        - prob_dm1: float - Proba of conversion if received type 1 dm
        - prob_dm2: float - Proba of conversion if received type 2 dm
        - prob_dm3: float - Proba of conversion if received type 3 dm
        - More prob_dmx can be added
        """
        df_cust = pd.read_csv(customer_data_path)
        df_cust["customer_id"] = df_cust["customer_id"].map(str)
        self.df_cust = df_cust

        df_prob = pd.read_csv(segment_prob_data_path)
        df_prob["segment_id"] = df_prob["segment_id"].map(str)
        self.df_prob = df_prob

        ls_dm = [c.split("_")[-1] for c in df_prob.columns if "prob_dm" in c]
        self._ls_dm = ls_dm

        df_prob_long = df_prob\
            .rename(columns=dict(zip(["prob_" + dm for dm in ls_dm], ls_dm)))\
            .melt(id_vars=['segment_id'], value_vars=ls_dm,
                  var_name='dm', value_name='prob')
        self.df_prob_long = df_prob_long

        df_cust_prob = df_cust.merge(df_prob, on=["age_cat", "freq_cat"])
        self.df_cust_prob = df_cust_prob


    def _optimizer_objects(self) -> Tuple[list, dict]:
        """
        Preparation of objects for the use of the optimizer.
        """
        # Create necessary lists.
        ls_cust = list(self.df_cust['customer_id'].unique())
        ls_age_cat = list(self.df_prob['age_cat'].unique())
        ls_freq_cat = list(self.df_prob['freq_cat'].unique())
        ls_segment_id = list(self.df_prob['segment_id'].unique())
        ls_dm = \
            [c.split("_")[-1] for c in self.df_prob.columns if "prob_dm" in c]

        # Create necessary dictionaries.
        dict_segment_dm_prob = self.df_prob_long.set_index(
            ['segment_id','dm'])['prob'].to_dict()
        dict_segment_count = self.df_cust_prob.groupby(
            ["segment_id"])["customer_id"].count().to_dict()

        return ls_cust, ls_age_cat, ls_freq_cat, ls_segment_id, ls_dm, \
               dict_segment_dm_prob, dict_segment_count


    def run_optimizer(self,
                      dict_dm_cost: dict = {"dm1": 0.0, "dm2": 10.0,
                                            "dm3": 20.0},
                      unit_sales: float = 30.0, min_dist_ratio: float = 0.1,
                      max_budget: Union[float, str] = 10000.0)\
            -> None:
        """
        Run optimizer.
        """

        if not (isinstance(max_budget, NumberTypes) or max_budget == "optimize"):
            raise Exception("max_budget should be a number or 'optimize'.")

        self.dict_dm_cost = dict_dm_cost
        self.unit_sales = unit_sales
        self.min_dist_ratio = min_dist_ratio

        optimize_max_budget = max_budget == "optimize"

        if not optimize_max_budget:
            self.max_budget = max_budget

        _, _, _, ls_segment_id, ls_dm, dict_segment_dm_prob,\
        dict_segment_count = self._optimizer_objects()

        # Optimization
        prob = pulp.LpProblem(name="CouponProblem", sense=pulp.LpMaximize)

        # Set decision variables
        x_sd = {}
        for s in ls_segment_id:
            for d in ls_dm:
                x_sd[s, d] = pulp.LpVariable(
                    name=f"x({s}, {d})", lowBound=0, upBound=1,
                    cat="Continuous")
        if optimize_max_budget:
            max_budget = pulp.LpVariable(name="max_budget", lowBound=1,
                    cat="Continuous")

        # Objective: maximize profit
        prob += \
            pulp.lpSum(
                dict_segment_dm_prob[s, d] * x_sd[s, d] \
                * dict_segment_count[s] * unit_sales
                for s in ls_segment_id
                for d in ls_dm) - \
            pulp.lpSum(
                dict_segment_dm_prob[s, d] * x_sd[s, d] \
                * dict_segment_count[s] * dict_dm_cost.get(d, 0)
                for s in ls_segment_id
                for d in ls_dm)

        # Constraint1: Every customer receives one type of direct mail.
        for s in ls_segment_id:
            prob += pulp.lpSum(x_sd[s, d] for d in ls_dm) == 1

        # Constraint2: Total coupon redeem is max_budget or less.
        prob += pulp.lpSum(
            x_sd[s, d] * dict_dm_cost.get(d, 0) \
            * dict_segment_dm_prob[s, d] * dict_segment_count[s]
            for s in ls_segment_id
            for d in ls_dm) <= max_budget

        # Constraint3: Each type of direct mail is sent to more than or
        # equal to 10% of customers of each segment.
        for s in ls_segment_id:
            for d in ls_dm:
                prob += x_sd[s, d] >= min_dist_ratio

        # Solve optimization
        time_start = time.time()
        status = prob.solve()
        logger.info(f"status: {pulp.LpStatus[status]}")
        time_stop = time.time()
        logger.info(f"Obj Value: {pulp.value(prob.objective):.4}")
        logger.info(f"Compute Time: {(time_stop - time_start):.3}(s)")

        # Store output to pd.DataFrame
        df_send_dm = pd.DataFrame([[x_sd[s, d].value() for d in ls_dm]
                                   for s in ls_segment_id],
                                  columns=["send_prob_" + dm
                                           for dm in ls_dm])
        df_seg_send_prob = pd.concat([
            self.df_prob[["segment_id", "age_cat", "freq_cat"] \
                         + ["prob_" + dm for dm in ls_dm]], df_send_dm],
            axis=1)
        df_seg_send_prob["num_cust"] = df_seg_send_prob["segment_id"]\
                                       .apply(lambda x: dict_segment_count[x])
        for dm in ls_dm:
            df_seg_send_prob["num_send_" + dm] = \
                df_seg_send_prob["send_prob_" + dm] * \
                df_seg_send_prob['num_cust']
        for dm in ls_dm:
            df_seg_send_prob["num_conversion_" + dm] = \
                df_seg_send_prob["prob_" + dm] * \
                df_seg_send_prob["num_send_" + dm]
        df_seg_send_prob["num_conversion_statusquo"] = \
            df_seg_send_prob["num_cust"] * df_seg_send_prob["prob_dm1"]
        for dm in ls_dm:
            df_seg_send_prob["val_coupon_redeem_" + dm] = \
                df_seg_send_prob["num_conversion_" + dm] * \
                dict_dm_cost[dm]
        df_seg_send_prob["val_sales"] = \
            df_seg_send_prob[
                ["num_conversion_" + dm for dm in dict_dm_cost.keys()]]\
                    .sum(axis=1) * unit_sales
        df_seg_send_prob["val_profit"] = \
            df_seg_send_prob["val_sales"] - \
            df_seg_send_prob[
                ["val_coupon_redeem_" + dm for dm in dict_dm_cost.keys()]]\
                    .sum(axis=1)
        df_seg_send_prob["val_profit_status_quo"] = \
            df_seg_send_prob["num_conversion_statusquo"] * \
            (unit_sales - dict_dm_cost["dm1"])
        df_seg_send_prob["val_inc_profit"] = \
            df_seg_send_prob["val_profit"] - \
            df_seg_send_prob["val_profit_status_quo"]

        # Dataframe with result summary.
        self.df_seg_send_prob = df_seg_send_prob

        # Profit
        self.profit = df_seg_send_prob["val_profit"].sum()
        self.profit_status_quo = \
            df_seg_send_prob["val_profit_status_quo"].sum()
        self.inc_profit = df_seg_send_prob["val_inc_profit"].sum()

        # Max budget
        if optimize_max_budget:
            self.max_budget = max_budget.value()


    def visualize_optimized_results(self) -> None:
        """
        Visualize optimized results.
        """
        _, ls_age_cat, _, _, ls_dm, _, _ = self._optimizer_objects()
        len_ls_dm = len(ls_dm)

        ax = {}
        fig, ax = \
            plt.subplots(1, len_ls_dm, figsize=(20, 4))
        for i, ptn in enumerate(["send_prob_" + dm for dm in ls_dm]):
            df_seg_send_pivot = pd.pivot_table(
                data=self.df_seg_send_prob, values=ptn, columns="freq_cat",
                index="age_cat", aggfunc="mean")
            df_seg_send_pivot = df_seg_send_pivot.reindex(ls_age_cat)
            sns.heatmap(
                df_seg_send_pivot, annot=True, fmt=".1%", cmap="Blues",
                vmin=0, vmax=1, ax=ax[i])
            ax[i].set_title(f"{ptn}")
        fig.suptitle("Proportion of Optimal Number of DM Distribution",
                     fontsize=16)
        plt.show()

        ax = {}
        fig, ax = \
            plt.subplots(1, len_ls_dm, figsize=(20, 4))
        for i, ptn in enumerate(["num_send_" + dm for dm in ls_dm]):
            df_cust_send_pivot = pd.pivot_table(
                data=self.df_seg_send_prob, values=ptn, columns="freq_cat",
                index="age_cat", aggfunc="sum")
            df_cust_send_pivot = df_cust_send_pivot.reindex(ls_age_cat)
            sns.heatmap(
                df_cust_send_pivot, annot=True, fmt=".1f", cmap="Blues",
                vmax=800, ax=ax[i])
            ax[i].set_title(f"{ptn}_num")
        fig.suptitle("Optimal Number of DM Distribution", fontsize=16)
        plt.show()
