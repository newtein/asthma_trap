library("lme4")
library(MASS)
library(pscl)
library(dplyr)
library(broom.mixed)


set.seed(32)
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

#data$Auto = data$Auto - data$total_ev - data$nonev_sales
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
#data$AC  <- as.integer(data$AC)
data$year_fixed <- log(data$year_fixed-2)
data$state_code = factor(data$state_code)
data$EPA_Region = factor(data$EPA_Region)
data$ev_sales_log <- log(data$ev_sales)
data$nonev_sales_log <- log(data$nonev_sales)

#data$all_vec = data$Truck + data$Bus + data$Auto
data$all_vec= data$nonev_sales
data$all_vec_log <- log(data$all_vec)

# +   (1|EPA_Region/state_code)
formula = "AC ~  nonev_sales_log + ev_sales_log + year_fixed + offset(log(population)) +(1|EPA_Region/state_code)"
control <- glmerControl(optimizer = "bobyqa", optCtrl = list(maxfun = 2e5))
model <- glmer.nb(formula,  data=data, control = control)

#formula2 = "AC ~   ev_sales_log + year_fixed + offset(log(population)) +(1|EPA_Region/state_code)"
#model2 <- glmer.nb(formula2,  data=data, control = control)



AC_baseline = 1603.6888998897568
coefficients <- summary(model)$coefficients
#coefficients2 <- summary(model)$coefficients

beta_ev <- coefficients["ev_sales_log", "Estimate"]
beta_nonev <- coefficients["nonev_sales_log", "Estimate"]
RR_ev <- exp(beta_ev)
RR_nonev <- exp(beta_nonev)
Delta_AC_nonev <- AC_baseline * (RR_nonev - 1)
Delta_AC_ev <- AC_baseline * (1 - RR_ev)
Delta_AC_ev
Delta_AC_nonev
EV_marketshare <- (Delta_AC_ev / (Delta_AC_nonev + Delta_AC_ev)) * 100
EV_marketshare

calculate_CI_for_variable <- function(model_summary, AC_baseline, variable_name) {
  beta <- model_summary$coefficients[variable_name, "Estimate"]
  se_beta <- model_summary$coefficients[variable_name, "Std. Error"]
  z_value <- 1.96
  RR <- exp(beta)
  cat(se_beta)
  if(variable_name == "nonev_sales_log") {
  Delta_AC <- AC_baseline * (RR - 1)
} else if(variable_name == "ev_sales_log") {
  cat("here")
  Delta_AC <- AC_baseline * (1 - RR)
}
  # Calculate the margin of error
  margin_error <- z_value * se_beta

	 if(variable_name == "nonev_sales_log") {
  		CI_lower_adjusted <- AC_baseline * (exp(beta - z_value * se_beta) - 1)
  		CI_upper_adjusted <- AC_baseline * (exp(beta + z_value * se_beta) - 1)
	} else if(variable_name == "ev_sales_log") {
  		 CI_lower_adjusted <- AC_baseline * (1 - exp(beta - z_value * se_beta))
 		 CI_upper_adjusted <- AC_baseline * (1 - exp(beta + z_value * se_beta))
}
  return(list(
    adjusted = c(Delta_AC, CI_lower_adjusted, CI_upper_adjusted)
    
  ))
}

# Example usage for nonev_sales_log
CI_nonev_sales_log <- calculate_CI_for_variable(summary(model), AC_baseline, "nonev_sales_log")
CI_nonev_sales_log
# Example usage for ev_sales_log
CI_ev_sales_log <- calculate_CI_for_variable(summary(model), AC_baseline, "ev_sales_log")
CI_ev_sales_log

