library(lme4)
library(nlme)
library(mgcv)
library(dplyr) 
library(broom.mixed)


set.seed(32)
args <- commandArgs(trailingOnly = TRUE)
filename = args[1]
wfname1 = args[2]
primary_var = args[3]
# C:/Users/harsh/OneDrive - University of Toronto/Projects/asthma_trap/
filepath = "output_files"
fname = paste(filepath, filename, sep="/")
data = read.csv(fname)

data <- data %>%
  group_by(state_code) %>%  # Replace 'state' with the actual column name for states in your dataframe
  arrange(year) %>%    # This ensures that the data is in chronological order before applying cumsum
  mutate(
    total_ev = cumsum(ev_sales),
    total_nonev = cumsum(nonev_sales),
  ) %>%
  ungroup()  # This removes the grouping so that the dataframe returns to its normal state

data$Auto = data$Auto - data$total_ev

data$AC  <- as.integer(data$AC)
data$state_code = factor(data$state_code)
data$EPA_Region = factor(data$EPA_Region)
data$year_fixed = log(data$year_fixed-2)
data$ev_sales_log <- log(data$ev_sales)

data$all_vec = data$Truck + data$Bus + data$Auto
data$all_vec_log <- log(data$all_vec)


formula_str = " ~ ev_sales_log + all_vec_log + offset(log(population)) + (1|EPA_Region/state_code)"
formula_str <- paste(primary_var, formula_str)
formula <- as.formula(formula_str)

model <- glmer.nb(formula,  data=data, control = glmerControl(optimizer="bobyqa"))

tidy_lmfit <- tidy(model)
# Calculate the 95% confidence interval using the estimate and std.error
z_value <- qnorm(1 - (0.05 / 2)) # Get the z-value for a 95% confidence interval
tidy_lmfit$CI_lower <- tidy_lmfit$estimate - z_value * tidy_lmfit$std.error
tidy_lmfit$CI_upper <- tidy_lmfit$estimate + z_value * tidy_lmfit$std.error

wfname11 = paste(filepath, wfname1, sep="/")
write.csv(tidy_lmfit, wfname11)

