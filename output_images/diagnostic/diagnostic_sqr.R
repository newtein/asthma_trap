library(lme4)
library(broom.mixed)
library(nlme)
library(ggplot2)

set.seed(32)
filename = "model_AC_2013_2019_no2.csv"
wfname1 = "dignostic.csv"
wfname2 = "dianostic_2.csv"

filepath = "C:/Users/harsh/OneDrive - University of Toronto/Projects/asthma_trap/output_files"
fname = paste(filepath, filename, sep="/")
data = read.csv(fname)

data$ev_sales_sq = data$ev_sales * data$ev_sales

data$state_code = factor(data$state_code)
formula = "AC ~ ev_sales_sq + nonev_sales + year_fixed + (1|EPA_Region/state_code)"
model2 <- lmer(formula, data=data)


ggplot(data.frame(eta=predict(model2,type="link"),pearson=residuals(model2,type="pearson")),
      aes(x=eta,y=pearson)) +
    geom_point() +
    theme_bw()

ggplot(data.frame(x1=data$ev_sales,pearson=residuals(model,type="pearson")),
      aes(x=x1,y=pearson)) +
    geom_point() +
    theme_bw()

ggplot(data.frame(x1=data$nonev_sales,pearson=residuals(model,type="pearson")),
      aes(x=x1,y=pearson)) +
    geom_point() +
    theme_bw()

means <- aggregate(data[,c("ev_sales","nonev_sales")],by=list(data$year_fixed),FUN=mean)
lmcoefs <- summary(lm(AC ~ ev_sales + nonev_sales + year_fixed, data=data))$coefficients[,"Estimate"]
means$effects <- c(0,lmcoefs[substr(names(lmcoefs),1,2) == "year_fixed"])
means$effects <- means$effects - mean(means$effects)
cor(means[,c("ev_sales","nonev_sales","effects")])


fixef(model)
lmcoefs[1:3]

qqnorm(residuals(model))


#tidy_lmfit <- tidy(model)
#wfname11 = paste(filepath, wfname1, sep="/")
#write.csv(tidy_lmfit, wfname11)