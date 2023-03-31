from AF_calculations.merge_no2_exposure_with_population import MergeExAndPop
import pandas as pd
import numpy as np
from constants import *


class calculateAF:
    def __init__(self, pr_ir_df, years, measurement_type='no2'):
        self.pr_ir_df = pr_ir_df
        self.measurement_type = measurement_type
        self.fw = "output_files/PR_IR_AF_{}_{}_{}.csv".format(years[0], years[-1], self.measurement_type)

    def get_AF(self, RR, RR_unit, exposure_level):
        power = (np.log(RR) / RR_unit) * exposure_level
        RRdiff = np.e ** power
        AF = 1 - (1 / RRdiff)
        return AF

    def calculate_AF(self, exposure_level):
        # CRF for NO2 Alotaibi et al 2019 Equation 3
        # NO2 was 1.05 (95% CI = 1.02–1.07) per 4 μg/m3,
        # for PM2.5 it was 1.03 (95% CI = 1.01–1.05) per 1 μg/m3,
        # and for PM10 it was 1.05 (95% CI = 1.02–1.08) per 2 μg/m3.
        if self.measurement_type == 'no2':
            RR_unit = 4
            RR = 1.05
        elif self.measurement_type == 'pm2.5':
            RR_unit = 1
            RR = 1.03
        elif self.measurement_type == 'pm10':
            RR_unit = 2
            RR = 1.05
        AF = self.get_AF(RR, RR_unit, exposure_level)
        return AF

    def calculate_AF_5(self, exposure_level):
        # CRF for NO2 Alotaibi et al 2019 Equation 3
        # NO2 was 1.05 (95% CI = 1.02–1.07) per 4 μg/m3,
        # for PM2.5 it was 1.03 (95% CI = 1.01–1.05) per 1 μg/m3,
        # and for PM10 it was 1.05 (95% CI = 1.02–1.08) per 2 μg/m3.
        if self.measurement_type == 'no2':
            RR_unit = 4
            RR = 1.02
        elif self.measurement_type == 'pm2.5':
            RR_unit = 1
            RR = 1.01
        elif self.measurement_type == 'pm10':
            RR_unit = 2
            RR = 1.02
        AF = self.get_AF(RR, RR_unit, exposure_level)
        return AF

    def calculate_AF_95(self, exposure_level):
        # CRF for NO2 Alotaibi et al 2019 Equation 3
        # NO2 was 1.05 (95% CI = 1.02–1.07) per 4 μg/m3,
        # for PM2.5 it was 1.03 (95% CI = 1.01–1.05) per 1 μg/m3,
        # and for PM10 it was 1.05 (95% CI = 1.02–1.08) per 2 μg/m3.
        if self.measurement_type == 'no2':
            RR_unit = 4
            RR = 1.07
        elif self.measurement_type == 'pm2.5':
            RR_unit = 1
            RR = 1.05
        elif self.measurement_type == 'pm10':
            RR_unit = 2
            RR = 1.08
        AF = self.get_AF(RR, RR_unit, exposure_level)
        return AF

    def cal_statewise_AF(self, df):
        columns = ['state_code', 'population', 'PR', 'at_risk','incidence_cases', 'AC', 'IR', 'AC_5', 'AC_95', 'year']
        agg_dict = {'population': 'sum',
                    'PR': 'first',
                    'at_risk': 'sum',
                    'incidence_cases': 'sum',
                    'AC': 'sum',
                    'AC_5': 'sum',
                    'AC_95': 'sum',
                    'IR': 'first'
        }
        sdf = df[columns].groupby(['state_code', 'year']).agg(agg_dict).reset_index()
        sdf['SAF'] = sdf['AC']/sdf['incidence_cases']
        sdf['SAF_5'] = sdf['AC_5']/sdf['incidence_cases']
        sdf['SAF_95'] = sdf['AC_95']/sdf['incidence_cases']
        return sdf

    def get_df(self):
        pop_df = MergeExAndPop(measurement_type=self.measurement_type).get_df()
        pop_df['state_code'] = pop_df['state_code'].astype(float)
        df = pop_df.merge(self.pr_ir_df[['_STATE', 'PR', 'IR', 'year']], left_on=['state_code', 'year'], right_on=['_STATE', 'year'], how='left')

        df['at_risk'] = df['population'] * (1-df['PR'])
        df['incidence_cases'] = df['at_risk'] * df['IR']
        df['AF'] = df['pred_wght'].apply(self.calculate_AF)
        df['AF_5'] = df['pred_wght'].apply(self.calculate_AF_5)
        df['AF_95'] = df['pred_wght'].apply(self.calculate_AF_95)

        df['AC'] = df['incidence_cases'] * df['AF']
        df['AC_5'] = df['incidence_cases'] * df['AF_5']
        df['AC_95'] = df['incidence_cases'] * df['AF_95']
        # print(df['state_code'].unique().shape)
        sdf = self.cal_statewise_AF(df)
        print(sdf)
        # print(sdf['state_code'].unique().shape)
        # print(sdf.isna())
        # sdf = sdf.dropna()
        # print(sdf['state_code'].unique().shape)
        sdf = sdf[~sdf['state_code'].isin(EXCLUDE)]
        sdf = sdf[sdf['AC']!=0]
        sdf.to_csv(self.fw, index=False)
        return sdf

if __name__ == "__main__":
    obj = calculateAF()
    print(obj.cal_inc_cases())

