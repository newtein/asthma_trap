import pandas as pd

class compile:
    def __init__(self, measurement_types=('no2',), years=tuple(range(2010, 2020))):
        self.measurement_types = measurement_types
        self.years = years
        self.filepath = "odds_ratio_module/data/{}/PR_IR.csv"

    def execute(self):
        for pollutant in self.measurement_types:
            df = pd.DataFrame()
            for year in range(self.years[0], self.years[-1]+1):
                f = self.filepath.format(year, pollutant)
                try:
                    tdf = pd.read_csv(f)
                    tdf['year'] = year
                    df = df.append(tdf)
                except Exception as e:
                    print(year, e)
                    continue
            df.to_csv("output_files/PR_IR_{}_{}_with_na.csv".format(self.years[0], self.years[-1]), index=False)
            print("{} done.".format(pollutant))

if __name__ == "__main__":
    obj = compile().execute()