#finally regression
fit <- lm(log(read_rate+1) ~ unique_user_cnt +avg_domain_read_rate+
          avg_domain_inbox_rate+avg_user_avg_read_rate+avg_user_domain_avg_read_rate
        +mb_superuser+mb_engper+mb_supersub+mb_engsec+mb_inper+mb_insec+mb_unengsec+
          mb_idlesub+Fri+Mon+Sat+Sun+Thurs+Tues+Wed,data=train)

summary(fit)
plot(fit)

#showing problem of heteroskedasticity

fit12 <- lm(read_rate ~ unique_user_cnt +avg_domain_read_rate+
           avg_domain_inbox_rate+avg_user_avg_read_rate+avg_user_domain_avg_read_rate
        +mb_superuser+mb_engper+mb_supersub+mb_engsec+mb_inper+mb_insec+mb_unengsec+
           mb_idlesub+Fri+Mon+Sat+Sun+Thurs+Tues+Wed,data=train)
summary(fit12)
library(sandwich)
library(lmtest)
#variance-covariance matrix
sandwich::vcovHC(fit12, omega = NULL, type = "HC4")

lmtest::coeftest(fit12, df = Inf, vcovHC(fit12, omega = NULL, type = "HC4"))


summary(12)
plot(fit12)
distPred <- predict(fit1w, test)
actuals_preds <- data.frame(cbind(actuals=test$dist, predicteds=distPred))
correlation_accuracy <- cor(actuals_preds) 
head(actuals_preds)
#RMSE calculation
distPred<-predict(fit12,test)
RMSE.baseline <- sqrt(mean((distPred-test$read_rate)^2))
RMSE.baseline

MAE.baseline <- mean(abs(distPred-test$read_rate))
MAE.baseline

#stepwise regression
library(MASS)

step <- stepAIC(fit, direction="both")
step$anova # display results

summary(step)
library(sandwich)
library(lmtest)
#variance-covariance matrix
sandwich::vcovHC(step, omega = NULL, type = "HC4")

lmtest::coeftest(step, df = Inf, vcovHC(fit12, omega = NULL, type = "HC4"))
distPred<-predict(step,test)

RMSE.baseline <- sqrt(mean((distPred-test$read_rate)^2))
RMSE.baseline

MAE.baseline <- mean(abs(distPred-test$read_rate))
MAE.baseline

#decision Tree
library(rattle)
library(rpart)
decision <- rpart(read_rate ~ unique_user_cnt +avg_domain_read_rate+
             avg_domain_inbox_rate+avg_user_avg_read_rate+avg_user_domain_avg_read_rate
           +mb_superuser+mb_engper+mb_supersub+mb_engsec+mb_inper+mb_insec+mb_unengsec+
             mb_idlesub+Fri+Mon+Sat+Sun+Thurs+Tues+Wed,data=train)


tree <- predict(decision,test) 

RMSE.rtree <- sqrt(mean((tree-test$read_rate)^2))
RMSE.rtree

MAE.rtree <- mean(abs(tree-test$read_rate))
MAE.rtree
