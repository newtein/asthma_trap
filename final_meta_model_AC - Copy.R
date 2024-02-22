library(lme4)
library(broom.mixed)
library(nlme)

set.seed(32)
args <- commandArgs(trailingOnly = TRUE)
filename = args[1]
wfname1 = args[2]
wfname2 = args[3]

filepath = "C:/Users/harsh/OneDrive - University of Toronto/Projects/asthma_trap/output_files"
fname = paste(filepath, filename, sep="/")
data = read.csv(fname)

data$state_code = factor(data$state_code)
formula = "AC ~ ev_sales + nonev_sales + year_fixed + (1|EPA_Region/state_code)"
model <- lmer(formula, data=data)
tidy_lmfit <- tidy(model)
wfname11 = paste(filepath, wfname1, sep="/")
write.csv(tidy_lmfit, wfname11)

ml <- lme(AC ~ ev_sales + nonev_sales + year_fixed, random=~1|EPA_Region/state_code,data=data)
tidy_lmfit2 <- tidy(ml)
wfname22 = paste(filepath, wfname2, sep="/")
write.csv(tidy_lmfit2, wfname22)
