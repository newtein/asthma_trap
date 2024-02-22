library("lme4")
library(MASS)
library(pscl)
library(glmmTMB)
library(dplyr) 


set.seed(32)
#  model_AC_2013_2019_no2.csv
fname = "C:/Users/harsh/OneDrive - University of Toronto/Projects/asthma_trap/output_files/model_AC_95_2013_2019_pm10.csv"
data <- read.csv(fname)
data$AP = as.integer(data$population*data$PR*data$SAF_95)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
data$year_fixed <- log(data$year_fixed-2)
data$state_code = factor(data$state_code)
data$EPA_Region = factor(data$EPA_Region)


data <- data %>%
  group_by(state_code) %>%  # Replace 'state' with the actual column name for states in your dataframe
  arrange(year) %>%    # This ensures that the data is in chronological order before applying cumsum
  mutate(
	total_ev = cumsum(ev_sales),
	total_nonev = cumsum(nonev_sales),
) %>%
  ungroup()  # This removes the grouping so that the dataframe returns to its normal state

data$total_ev_log <- log(data$total_ev)
data$total_nonev_log <- log(data$total_nonev)
data$Auto = data$Auto - data$total_ev


#data$ev_sales_log <- log(data$ev_sales)
#data$nonev_sales_log <- log(data$nonev_sales)

#data$total_vec = data$Truck + data$Bus + data$Auto 
data$total_vec = data$Auto 
data$total_vec_log  <- log(data$total_vec)

# +   (1|EPA_Region/state_code)
formula1 = "AP ~   total_ev_log + offset(log(population))+(1|EPA_Region/state_code)"
control <- glmerControl(optimizer = "bobyqa", optCtrl = list(maxfun = 2e5))
model1 <- glmer.nb(formula1, data = data, control = control)
primary_var="AP"

tryCatch({
formula2 = "AP ~ total_vec_log+ offset(log(population))+(1|EPA_Region/state_code)"
control <- glmerControl(optimizer = "bobyqa", optCtrl = list(maxfun = 2e5))
model2 <- glmer.nb(formula2, data = data, control = control)
}, warning = function(w) {
if (grepl("failed to converge", w$message, ignore.case = TRUE)) {
cat("Model 2 failed to converge. Trying models again without EPA_Region...\n")
formula_str = " ~ total_ev_log + offset(log(population)) + (1|state_code)"
formula_str <- paste(primary_var, formula_str)
formula1 <- as.formula(formula_str)

formula_str = " ~ total_vec_log + offset(log(population)) + (1|state_code)"
formula_str <- paste(primary_var, formula_str)
formula2 <- as.formula(formula_str)

control <- glmerControl(optimizer = "bobyqa", optCtrl = list(maxfun = 2e5))
model1 <- glmer.nb(formula1, data = data, control = control)
model2 <- glmer.nb(formula2, data = data, control = control)
}
})
summary(model1)
summary(model2)

AC_baseline = 1603.6888998897568
coefficients1 <- summary(model1)$coefficients
beta_ev <- coefficients1["total_ev_log", "Estimate"]

coefficients2 <- summary(model2)$coefficients
beta_nonev <- coefficients2["total_vec_log", "Estimate"]
RR_ev <- exp(beta_ev)
RR_nonev <- exp(beta_nonev)
Delta_AC_nonev <- AC_baseline * (RR_nonev - 1)
Delta_AC_ev <- AC_baseline * (1 - RR_ev)
EV_marketshare <- (Delta_AC_ev / (Delta_AC_nonev + Delta_AC_ev)) * 100
EV_marketshare

library(tseries)

data2 <- data %>% 
  group_by(state_code) %>% 
  arrange(year) %>%  # Replace 'Year' with your actual time variable
  mutate(
    diff_total_ev_log = c(NA, diff(log(total_ev))),
    diff_heavy_duty_log = c(NA, diff(log(heavy_duty))),
    diff_log_population = c(NA, diff(log(population))),
    diff_AP = c(NA, diff(AP))
  ) %>% 
  ungroup()

data_clean <- na.omit(data2, cols = c("diff_total_ev_log", "diff_heavy_duty_log", "diff_log_population"))

formula <- "AP ~ diff_total_ev_log + diff_heavy_duty_log + offset(diff_log_population)+factor(year)+(1|EPA_Region/state_code)"
control <- glmerControl(optimizer = "bobyqa", optCtrl = list(maxfun = 2e5))
model <- lmer(formula, data = data_clean)
summary(model)


model <- glmer.nb(formula, data = data_clean, control = control)






