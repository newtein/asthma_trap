library(lme4)
library(nlme)
library(mgcv)
library(dplyr) 
library(broom.mixed)

options(show.error.messages = TRUE)


set.seed(32)
args <- commandArgs(trailingOnly = TRUE)
filename = args[1]
wfname1 = args[2]
target_var = args[3]

filepath = "output_files"
fname = paste(filepath, filename, sep="/")
data = read.csv(fname)

if (target_var == "AC") {
  data$AP <- as.integer(data$population * data$PR * data$SAF)
  primary_var = "AP"
} else if (target_var == "AC_5") {
  data$AP_5 <- as.integer(data$population * data$PR * data$SAF_5)
  primary_var = "AP_5"

} else if (target_var == "AC_95") {
  data$AP_95 <- as.integer(data$population * data$PR * data$SAF_95)
  primary_var = "AP_95"

}

cat("Primary var", primary_var)

calculate_and_combine_results <- function(model1, model2, filepath, wfname1) {
  # Tidying and calculating 95% CI for model1
  tidy_lmfit <- broom::tidy(model1)
  z_value <- qnorm(1 - (0.05 / 2)) # Get the z-value for a 95% confidence interval
  tidy_lmfit$CI_lower <- tidy_lmfit$estimate - z_value * tidy_lmfit$std.error
  tidy_lmfit$CI_upper <- tidy_lmfit$estimate + z_value * tidy_lmfit$std.error
  tidy_lmfit$model <- "model1" # Adding a column to identify the model
  
  # Tidying and calculating 95% CI for model2
  tidy_lmfit2 <- broom::tidy(model2)
  tidy_lmfit2$CI_lower <- tidy_lmfit2$estimate - z_value * tidy_lmfit2$std.error
  tidy_lmfit2$CI_upper <- tidy_lmfit2$estimate + z_value * tidy_lmfit2$std.error
  tidy_lmfit2$model <- "model2" # Adding a column to identify the model
  
  # Combining the results of both models
  combined_results <- rbind(tidy_lmfit, tidy_lmfit2)
  
  # Writing to file
  wfname11 <- paste(filepath, wfname1, sep="/")
  write.csv(combined_results, wfname11)
}


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

data$total_vec = data$Auto 
#data$total_vec = data$Truck + data$Bus + data$Auto 
data$total_vec_log  <- log(data$total_vec)

control <- glmerControl(optimizer = "bobyqa", optCtrl = list(maxfun = 2e5))

formula_str = " ~ total_ev_log + offset(log(population)) + (1|EPA_Region/state_code)"
formula_str <- paste(primary_var, formula_str)
formula1 <- as.formula(formula_str)

model1 = glmer.nb(formula1, data = data, control =control)
cat("Model1 done\n")

tryCatch({
formula_str = " ~ total_vec_log + offset(log(population)) + (1|EPA_Region/state_code)"
formula_str <- paste(primary_var, formula_str)
formula2 <- as.formula(formula_str)
model2 <- glmer.nb(formula2, data = data, control = control)

summary_text <- capture.output(summary(model2))
calculate_and_combine_results(model1, model2, filepath, wfname1)
cat("end of the main block")

}, error = function(e) {
    cat("An error occurred:\n")
    cat(conditionMessage(e), "\n")
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

calculate_and_combine_results(model1, model2, filepath, wfname1)
cat("end of the warning block")

}
})




