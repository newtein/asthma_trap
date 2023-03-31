import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import numpy as np
from scipy import stats
from constants import *
from call_lme4_in_R import callR



class MergeWithEVSales:
    def __init__(self, measurement_type, years=tuple(range(2010, 2020))):
        self.measurement_type = measurement_type
        self.years = years
        self.SA_key = 'SA_3'
        self.script_path = 'R_SA/{}'.format(self.SA_key)
        ev_df = pd.read_csv("data/ev_sales/ev_data_preprocessed.csv")
        asthma_df = pd.read_csv("output_files/PR_IR_AF_{}_{}_{}.csv".format(
            self.years[0], self.years[-1], self.measurement_type))
        asthma_df = asthma_df[asthma_df['state_code']!=0]
        self.df = ev_df.merge(asthma_df, how='left', on=['state_code', 'year'])
        self.df = self.df[~self.df['state_code'].isin(EXCLUDE)]

    def clean(self, df):
        df['ev_market_share'] = df['ev_sales'] / df['total']
        df['nonev_market_share'] = df['nonev_sales'] / df['total']
        replace_year = {i: j for i, j in zip(range(2011, 2020), range(1, 12))}
        df['year_fixed'] = df['year'].replace(replace_year)
        df = df.rename(columns={'ZEV Mandates': 'ZEV_Mandates', 'EPA Region': 'EPA_Region'})
        return df

    def filter(self, df, col):
        tdf = df
        tdf = df[df['year'] >= 2013]
        tdf = tdf[tdf['state_code']!=6]
        # print(tdf[['State', 'AC', 'ev_sales', 'year']])
        tdf = tdf[~pd.isna(tdf['AC'])]
        min_per, max_per = 5, 95
        min_trap, max_trap = np.percentile(tdf[col], min_per), np.percentile(tdf[col], max_per)
        min_nonev, max_nonev = np.percentile(tdf['nonev_sales'], min_per), np.percentile(tdf['nonev_sales'], max_per)
        min_ev, max_ev = np.percentile(tdf['ev_sales'], min_per), np.percentile(tdf['ev_sales'], max_per)
        print(min_trap, max_trap, min_nonev, max_nonev)
        # filtr = (tdf['ev_sales'] < max_ev) & (tdf['ev_sales'] > min_ev) & (tdf['nonev_sales'] < max_nonev) & (
        #             tdf['nonev_sales'] > min_nonev) & (tdf[col] < max_trap) & (
        #                     tdf[col] > min_trap)
        # filtr2 =(tdf['ev_sales'] < max_ev) & (tdf['ev_sales'] > min_ev)  & (tdf[col] < max_trap) & (
        #                     tdf[col] > min_trap)
        # filtr2 = (tdf['ev_sales'] < max_ev) & (tdf['ev_sales'] > min_ev)
        # filtr2 = (tdf['ev_sales'] != 0)
        # tdf = tdf[filtr2]
        return tdf

    def write(self, df, col):
        # print(df.shape)
        wfname = "{}_model_{}_2013_{}_{}.csv".format(self.SA_key, col, self.years[-1], self.measurement_type)
        df.to_csv("output_files/{}".format(wfname), index=False)
        return wfname

    def modelR(self, fname, col):
        callR(col, fname,
              '{}_results_{}_{}.csv'.format(self.SA_key, self.measurement_type, col),
              '{}_results_{}_{}_pvalue.csv'.format(self.SA_key, self.measurement_type, col),
              script_path=self.script_path).execute()

    def execute(self, col):
        df = self.clean(self.df)
        # print(df[['State', 'ev_sales', 'incidences_trap', 'AC', 'year']])
        df = self.filter(df, col)
        # print(df.shape)
        wfname = self.write(df, col)
        self.modelR(wfname, col)


if __name__ == "__main__":
    confidence_intervals = ['AC', 'AC_5', 'AC_95']
    measurement_type = 'no2'
    obj = MergeWithEVSales(measurement_type)
    for col in confidence_intervals:
        obj.execute(col)
