MANDATORY_BRFSS_COLUMNS = ["_STATE", "FMONTH", "IDATE", "IMONTH", "IDAY", "IYEAR",
                     "LADULT", "CADULT",
                    "DISPCODE", "NUMADULT", "NUMMEN", "NUMWOMEN", "CSTATE1",
                    "HHADULT", "HLTHPLN1", "MEDCOST", "ASTHMA3", "ASTHNOW",
                    "CHCCOPD1", "EDUCA", "RENTHOM1", "EMPLOY1", "INCOME2",
                    "SMOKE100", "SMOKDAY2", "STOPSMK2", "LASTSMK2", "USENOW3",
                    "ECIGARET", "ECIGNOW",
                    "MEDICARE", "NOCOV121",
                    "LSTCOVRG", "MEDBILL1",
                    "CASTHDX2", "CASTHNO2", "_CHISPNC", "_CRACE1",
                    "_CPRACE", "_HCVU651", "_LTASTH1", "_CASTHM1", "_ASTHMS1",
                    "_PRACE1", "_MRACE1", "_RACEG21", "_CHLDCNT", "_INCOMG",
                    "_SMOKER3", "_RFSMOK3", "_LLCPWT2", "_CLLCPWT", "MSCODE"]

OUTPUT_FILE = 'output_files'
OUTPUT_IMAGE = 'output_images'
US_CENSUS_DIR = "us_census"
TRAP_INCIDENCE = 'data/TRAP/khreis_2021.xlsx'
TRAP_INCIDENCE_v2 = 'data/TRAP/gujral_sme_trap.csv'
CENSUS_DATA_PATH = US_CENSUS_DIR+"/2010_2019_population.csv"
ATMOS_BY_STATE = 'data/ATMOS_VOL/atmos_size_by_state.csv'
# POP_LUR_FILE = 'data/lur_no2/lur_no2_merged_with_pop.csv'
AMBIENT_AIR_DATA = "data/ambient_no2"
HEAVY_DUTY_DATA = "../cali_zev/data/heavy_duty/heavy_duty_preprocessed_2019.csv"
# California, Connecticut, Maine, Maryland, Massachusetts, New Jersey, New York, Oregon, Rhode Island, Vermont
ZEV_STATES = [6, 9, 23, 24,25, 34, 36, 41, 44, 50]
# CARB = [6, 8, 41, 9, 23, 24,25, 34, 36, 44, 50]

# Arizona (lev repeled), Colarado (zev MY 2022), Delaware (nz), District Of Columbia (nz), Minnesota,
# New Mexico (lev repealed), Pennsylvania (nz), Washington (nz)
# 4 CARB states don't have ZEV mandates
# 2 states AZ and NM has LEV repealed
# Colarado and Manisota has ZEV, but model year are well-beyound (2022).
# EXCLUDE_STATES = [4, 8, 10, 11, 27, 35, 42, 53]

## Update 1: we are not excluding LEV states (they will be treated as NonZEV states); also places where ZEV is repealed
# Colarado (8, zev MY 2022),
#  Minnesota (27, 2025, https://www.greencarreports.com/news/1133027_minnesota-adopts-california-ev-mandate-makes-it-tougher-for-plug-in-compliance-cars),
# Nevada (32)
# New Mexico (35, https://westernresourceadvocates.org/blog/new-mexico-adopts-clean-cars-standards/)
# Virginia (51, 2025, https://www.greencarcongress.com/2021/03/20210330-virginia.html)
# EXCLUDE_STATES = [8, 27, 32, 35, 51]

## Update 2: I'm considering the states that have adopted ZEV after model year 2021 as Other states
# Do need to remove anything
EXCLUDE_STATES = []
# 2, 15
EXCLUDE = [66, 72, 78, 80, 0]

## Odds Ratio
DATA_ODDS_RATIO_MODULE = "odds_ratio_module/data"
COLUMNS_FOR_ODD_RATIO = ["SMOKE100", "_STATE", "ASTHMA3", "ASTHNOW", "_AGEG5YR", "SEX", "_RACE_G1",
"INCOME2", "_INCOMG", "EDUCA", "_EDUCAG", "_BMI5", "_BMI5CAT", "CHILDREN", "NUMADULT", "HHADULT", "_CHLDCNT", "_LLCPWT2", "MSCODE"]
COLUMNS_FOR_ODD_RATIO_FOR_CHILD = ["_STATE", "CASTHDX2", "CASTHNO2", "RCSGENDR", "_CPRACE",
"INCOME2", "_INCOMG", "CHILDREN", "NUMADULT", "HHADULT", "_CHLDCNT", "_CLLCPWT", "MSCODE"]

RENAME  = {
    "SEX1": "SEX",
    "SOMKE100": "SMOKE100",
}

# MODELING_COLUMNS = ["TAILPIPE", "_AGEG5YR", "SEX", "_RACE_G1", 'POVERTY', 'POPEST2017_CIV', "_EDUCAG", "_BMI5CAT",
#                     "ASTHMA"]
# MODELING_COLUMNS_FOR_CHILD = ["TAILPIPE", "RCSGENDR", "_CPRACE", 'POVERTY', 'POPEST2017_CIV', "ASTHMA"]
# MODELING_COLUMNS = ["NONCARB", "_AGEG5YR", "SEX", "_RACE_G1", 'POVERTY', 'DENSITY', "_EDUCAG", "_BMI5CAT",
#                     "ASTHMA"]

MODELING_COLUMNS = ["NONCARB", "_AGEG5YR", "SEX", "_RACE_G1", 'POVERTY', 'DENSITY', "_EDUCAG", "_BMI5CAT",
                    "ASTHMA", "_LLCPWT2"]
MODELING_COLUMNS_FOR_CHILD = [ "RCSGENDR"  ,"_CPRACE", "ASTHMA"]

CENSUS_REGIONS = {

    1: "Connecticut, Maine, Massachusetts, New Hampshire, Rhode Island, Vermont, New Jersey, New York, Pennsylvania",
    2: "Illinois, Indiana, Michigan, Ohio, Wisconsin, Iowa, Kansas, Minnesota, Missouri, Nebraska, North Dakota, South Dakota",
    3: "Delaware, Florida, Georgia, Maryland, North Carolina, South Carolina, Virginia, Washington, District Of Columbia, West Virginia, Alabama, Kentucky, Mississippi, Tennessee, Arkansas, Louisiana, Oklahoma, Texas",
    4: "Arizona, Colorado, Idaho, Montana, Nevada, New Mexico, Utah, Wyoming, Alaska, California, Hawaii, Oregon, Washington"

}
REGION_DICT = {i: [k.strip() for k in j.split(",")] for i, j in CENSUS_REGIONS.items()}
REGION_DATA = [[k, i] for i, j in REGION_DICT.items() for k in j]





