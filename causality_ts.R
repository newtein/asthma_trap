library("lme4")
library(MASS)
library(pscl)
library(glmmTMB)
library(vars)

fname = "C:/Users/harsh/OneDrive - University of Toronto/Projects/asthma_trap/output_files/model_AC_2013_2019_no2.csv"
data <- read.csv(fname)
data$AP = as.integer(data$population*data$PR*data$SAF)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
data$year_fixed <- log(data$year_fixed-2)
data$state_code = factor(data$state_code)
data$EPA_Region = factor(data$EPA_Region)

data$total_ev_log <- log(cumsum(data$ev_sales))


#data$ev_sales_log <- log(data$ev_sales)
#data$nonev_sales_log <- log(data$nonev_sales)

data$heavy_duty = data$Truck + data$Bus + data$Auto + data$Motorcycle
data$heavy_duty_log <- log(data$heavy_duty)


data$population_log <- log(data$population)

# Fit the VAR model (you need to choose the appropriate lag 'p')
var_model <- VAR(data[, c("heavy_duty_log", "AP")], p = 0)  # Example with lag 2

# Perform Granger causality test
granger_result <- causality(var_model, cause = "total_ev_log")
print(granger_result)