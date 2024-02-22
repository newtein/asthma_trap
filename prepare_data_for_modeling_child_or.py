import math

from make_file_for_odds_ratio_child import GetData
import pandas as pd
from get_population_by_state import GetAgeSex
from calculate_poverty import POVERTY
from calculate_PR_IR import PRIR
from adjust_weights_for_or import AdjustWeightsForOR
from config import CONFIG
from constants import *
import constants
import numpy as np


class ModelingDataChild:
    def __init__(self, measurement_type='no2'):
        self.pop_type = 'CHILD'
        self.measurement_type = measurement_type
        self.dfs = GetData().execute()

    def if_carb(self, x):
        if x in ZEV_STATES:
            return 1
        return 0

    def if_state(self, x):
        if x == self.state_code:
            return 1
        return 0

    def get_primary_risk(self, x):
        if x['CASTHDX2'] == 1:
            if x['CASTHNO2'] == 1:
                return 1
        return 0

    def filter_state_based_on_census_region(self, df):
        acceptable_region = df.loc[df["State Code"]==self.state_code, "region_code"].values[0]
        zev_states_but_not_our_state = [i for i in ZEV_STATES if i != self.state_code]
        df = df[~df['_STATE'].isin(zev_states_but_not_our_state)]
        df = df[df['region_code'] == acceptable_region].reset_index()
        return df

    def merge_for_epa_region(self, df):
        epa_region = pd.read_csv("data/states_and_counties.csv")
        epa_region = epa_region[['State Name','State Code', "EPA Region"]]
        epa_region = epa_region[epa_region['State Code'] != 'CC']
        epa_region['State Code'] = epa_region['State Code'].apply(int)
        epa_region = epa_region.drop_duplicates(['State Code'], keep='first')
        df = df.merge(epa_region, left_on="_STATE", right_on="State Code", how='left')
        return df

    def get_primary_risk_wrap(self, df):
        df = df[df['CASTHDX2'].isin([1, 2])]
        df['ASTHMA'] = df.apply(self.get_primary_risk, axis=1)
        df = df[df['ASTHMA'].isin([0,1])]
        return df

    def filtering_nan_state(self, df):
        df = df[~pd.isna(df["_STATE"])]
        return df

    def get_data_with_epa_region(self):
        years = CONFIG.get("analysis_years")
        years_str = "_".join([str(i) for i in years])
        CONFIG.update({"analysis_years": years})
        DATA_ODDS_RATIO_MODULE = constants.DATA_ODDS_RATIO_MODULE + "/{}".format(years_str)
        fname = "{}/BRFSS_{}_OR.csv".format(DATA_ODDS_RATIO_MODULE, self.pop_type)
        dfs = self.dfs
        mdf = pd.DataFrame()
        for i, year in zip(range(len(dfs)), years):
            dfs[i] = self.filtering_nan_state(dfs[i])
            dfs[i]['year'] = int(year)
            mdf = mdf._append(dfs[i])

        mdf = self.merge_for_epa_region(mdf)
        mdf = self.get_primary_risk_wrap(mdf)
        weight_col = '_CLLCPWT'
        ever_asthma = (mdf['ASTHMA'] == 1)
        new_cols = ["State Name", "_STATE", 'EPA Region', '_CLLCPWT', 'year']
        mdf = mdf[MODELING_COLUMNS_FOR_CHILD+new_cols]
        pr_ir_df, national_avg_row = PRIR(self.pop_type).get_df(mdf, '_CLLCPWT')
        years = CONFIG.get("analysis_years")
        return mdf, national_avg_row

