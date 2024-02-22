import pandas as pd
from config import CONFIG
import numpy as np


class IRLogic:
    def __init__(self, years):
        """
        if 70% of the time state has participated, fill with the mean, else use the national incidence
        """
        self.years = years
        self.fname = "odds_ratio_module/data/{}/PR_IR.csv"

    def merge_pr_ir(self):
        df = pd.DataFrame()
        for year in self.years:
            tdf = pd.read_csv(self.fname.format(year))
            tdf['year'] = year
            df = df._append(tdf)
        return df

    def impute_logic_v1(self,x):
        x_free = [i for i in x if not pd.isna(i)]
        threshold1 = len(self.years) *0.7
        threshold2 = len(self.years) *0.4
        if len(x_free) >= threshold2:
            return x.fillna(x.median())
        #     return x.interpolate(method='linear', order=1, limit=10, limit_direction='both')
        # elif threshold2 <= len(x_free) < threshold1:
        #     return x.fillna(x.median())
        else:
            return [np.nan for i in x]
        # return x


    def pr_impute(self, x, pr_lookup):
        year = x['year']
        pr = x['PR']
        """
        Unquote line below for sa
        """
        # if 1:
        if pd.isna(pr):
            return pr_lookup.get(year)
        else:
            return pr

    def ir_impute(self, x, ir_lookup):
        year = x['year']
        ir = x['IR']
        """
        Unquote the line below for sa
        """
        if 1:
        # if pd.isna(ir):
            return ir_lookup.get(year)
        else:
            return ir

    def execute(self):
        df = self.merge_pr_ir()
        df['PR'] = df.groupby("_STATE")['PR'].transform(self.impute_logic_v1)
        national_df = df[df['_STATE'] ==0]
        pr_lookup = {row['year']:row['PR'] for index, row in national_df.iterrows()}
        ir_lookup = {row['year']:row['IR'] for index, row in national_df.iterrows()}

        df['PR'] = df.apply(self.pr_impute, axis=1, args=(pr_lookup,))

        df['at_risk'] = df['population'] * (1-df['PR'])
        df['IR'] = df['num']/df['at_risk']
        df['IR'] = df.groupby("_STATE")['IR'].transform(self.impute_logic_v1)
        df['IR'] = df.apply(self.ir_impute, axis=1, args=(ir_lookup,))
        df = df[df['_STATE']!=0]
        return df




if __name__ == "__main__":
    obj = IRLogic(list(range(2010, 2020))).execute()