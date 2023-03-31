import pandas as pd

from prepare_data_for_modeling_child_or import ModelingDataChild
from compile_PR_IR_AF_files import compile
from config import CONFIG
from constants import *
import constants
import os
import sys
from merge_with_ev_sales import MergeWithEVSales
from call_lme4_in_R import callR
from AF_calculations.calculate_AF import calculateAF
from incidence_rate_logic import IRLogic


import warnings
warnings.filterwarnings("ignore")

class OddsRatio:
    def __init__(self, pop_type='ADULT', state_code = None, write_file=True, identifier='', other_filters={},
                 use_smote=False, measurement_type = 'no2'):
        self.write_file = write_file
        self.pop_type = pop_type
        self.measurement_type = measurement_type

        years = CONFIG.get("analysis_years")
        years_str = "_".join([str(i) for i in years])
        self.DATA_ODDS_RATIO_MODULE = constants.DATA_ODDS_RATIO_MODULE + "/{}".format(years_str)
        try:
            os.mkdir(self.DATA_ODDS_RATIO_MODULE)
        except:
            pass

    def get_data(self):
        self.df, national_avg_row = ModelingDataChild(measurement_type=self.measurement_type).get_data_with_epa_region()
        return self.df, national_avg_row

def incidence_rate_logic_and_AF(measurement_type):
    # picking up the middle year/last year in the series (most recent population)
    pr_ir_df = IRLogic(years).execute()
    af_df = calculateAF(pr_ir_df, years, measurement_type=measurement_type).get_df()
    # mdf = mdf.merge(af_df, right_on=['state_code'], left_on=['_STATE'], how='left')
    # print("File written {}: {}".format(self.pop_type, fname))
    return

if __name__ == "__main__":

    # measurement_types = ['no2', 'pm2.5', 'pm10']
    measurement_types = ['no2']
    years = list(range(2010, 2020))
    # years = [2010]
    national_avg_data = []

    for measurement_type in measurement_types:
        for year in years:
            CONFIG.update({"analysis_years": [year]})
            print(CONFIG.get("analysis_years"))
            obj = OddsRatio(pop_type='CHILD', measurement_type=measurement_type)
            _, national_avg_row = obj.get_data()
            national_avg_row['year'] = year
            national_avg_row['measurement_type'] = measurement_type
            national_avg_data.append(national_avg_row)
            print("{} {} done.".format(measurement_type, year))
        incidence_rate_logic_and_AF(measurement_type)

    national_avg_df = pd.DataFrame(columns=['_STATE', 'population', 'PR', 'IR', 'year', 'measurement_type'], data=national_avg_data)
    national_avg_df.to_csv("output_files/national_avg_df.csv", index=False)
    # compile(measurement_types=measurement_types, years=years).execute()
    # confidence_intervals = ['AC', 'AC_5', 'AC_95']
    confidence_intervals = ['AC']
    for measurement_type in measurement_types:
        obj = MergeWithEVSales(measurement_type)
        for col in confidence_intervals:
            obj.execute(col)
            callR(col, 'model_{}_2013_2019_{}.csv'.format(col, measurement_type),
                  'results_{}_{}.csv'.format(measurement_type, col), 'results_{}_{}_pvalue.csv'.format(measurement_type, col)).execute()
