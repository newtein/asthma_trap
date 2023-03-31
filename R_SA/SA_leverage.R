library(lme4)
library(broom.mixed)
library(nlme)
library(ggplot2)

set.seed(32)
filename = "model_AC_95_2013_2019_no2.csv"
wfname1 = "dignostic.csv"
wfname2 = "dianostic_2.csv"

filepath = "C:/Users/harsh/OneDrive - University of Toronto/Projects/asthma_trap/output_files"
fname = paste(filepath, filename, sep="/")
data = read.csv(fname)

data$AC = data$AC_95
data$state_code = factor(data$state_code)
formula = "AC ~ ev_sales + nonev_sales + year_fixed + (1|EPA_Region/state_code)"
model <- lmer(formula, data=data)

levId <- which(hatvalues(model) >= .17)
data[levId,c("AC","State","ev_sales","nonev_sales")]
summary(data[,c("AC","ev_sales","nonev_sales")])

mmLev <- lmer(AC ~ ev_sales + nonev_sales + year_fixed + (1|EPA_Region/state_code), data=data[-c(levId),])
mmLevCD <- data.frame(effect=fixef(model),
                     change=(fixef(mmLev) - fixef(model)),
                     se=sqrt(diag(vcov(model)))
                     )
rownames(mmLevCD) <- names(fixef(mmLev))
mmLevCD$multiples <- abs(mmLevCD$change / mmLevCD$se)
mmLevCD