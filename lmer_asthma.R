library("lme4")
library(MASS)
library(pscl)
library(dplyr)

#
fname = "C:/Users/harsh/OneDrive - University of Toronto/Projects/asthma_trap/output_files/model_AC_2013_2019_no2.csv"
data <- read.csv(fname)

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
data$year_fixed <- log(data$year_fixed-2)
data$state_code = factor(data$state_code)
data$EPA_Region = factor(data$EPA_Region)
data$ev_sales_log <- log(data$ev_sales)
data$nonev_sales_log <- log(data$nonev_sales)

data$all_vec = data$Truck + data$Bus + data$Auto
data$all_vec_log <- log(data$all_vec)

# +   (1|EPA_Region/state_code)
formula = "AC ~   ev_sales_log + all_vec_log + offset(log(population)) +(1|EPA_Region/state_code)"
model <- glmer.nb(formula,  data=data)
summary(model)

AC_baseline = 1603.6888998897568
coefficients <- summary(model)$coefficients
beta_ev <- coefficients["ev_sales_log", "Estimate"]
beta_nonev <- coefficients["all_vec_log", "Estimate"]
RR_ev <- exp(beta_ev)
RR_nonev <- exp(beta_nonev)
Delta_AC_nonev <- AC_baseline * (RR_nonev - 1)
Delta_AC_ev <- AC_baseline * (1 - RR_ev)
EV_marketshare <- (Delta_AC_ev / (Delta_AC_nonev + Delta_AC_ev)) * 100
EV_marketshare



