library(lme4)
library(nlme)
library(mgcv)
library(dplyr) 
library(broom.mixed)



set.seed(32)
args <- commandArgs(trailingOnly = TRUE)
filename = args[1]
wfname1 = args[2]
wfname2 = args[3]
# C:/Users/harsh/OneDrive - University of Toronto/Projects/asthma_trap/
filepath = "output_files"
fname = paste(filepath, filename, sep="/")
data = read.csv(fname)

data$state_code = factor(data$state_code)
data$EPA_Region = factor(data$EPA_Region)
data$year_fixed = log(data$year_fixed-2)
data$ev_sales_log <- log(data$ev_sales)
data$nonev_sales_log <- log(data$nonev_sales)

formula = "AC ~ nonev_sales_log + ev_sales_log + offset(log(population)) + year_fixed + (1|EPA_Region/state_code)"
model <- glmer.nb(formula,  data=data, control = glmerControl(optimizer="bobyqa"))

tidy_lmfit <- tidy(model)
# Calculate the 95% confidence interval using the estimate and std.error
z_value <- qnorm(1 - (0.05 / 2)) # Get the z-value for a 95% confidence interval
tidy_lmfit$CI_lower <- tidy_lmfit$estimate - z_value * tidy_lmfit$std.error
tidy_lmfit$CI_upper <- tidy_lmfit$estimate + z_value * tidy_lmfit$std.error

wfname11 = paste(filepath, wfname1, sep="/")
write.csv(tidy_lmfit, wfname11)

