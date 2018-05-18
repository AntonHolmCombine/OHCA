library(readxl)
library(mice)
library(VIM)
library(ROCR)
library(party)

dataset <- read_excel("Imputed_data.xlsx")


shuffled_data <- dataset[sample(nrow(dataset)),]

k <- 4
rows <- nrow(shuffled_data)
increments <- floor(rows/k)

data_labels <- labels(shuffled_data)[[2]]
rand_labels <- sample(1:42,10)
new_data <- shuffled_data[,c(rand_labels,43)]
perfs <- list()
total_AUC <- 0

for (i in 1:k) {
  
  
  x.evaluate <- new_data[(increments*(i-1)+1):(i*increments),]
  x.train <- new_data[-((increments*(i-1)+1):(i*increments)),]
  
  
  x.model <- cforest(as.factor(Binary_Sec_Out_180_day_CPC_score) ~ 
                       ., data = x.train,
                     control = cforest_unbiased(mtry=5, ntree = 400))
  
  x.predictions <- predict(x.model, newdata = x.evaluate)
  
  x.correct <- x.predictions == x.evaluate$Binary_Sec_Out_180_day_CPC_score
  
  x.probabilities <- 1- unlist(treeresponse(x.model,
                                            newdata=x.evaluate)
                               , use.names=F)[seq(1,nrow(x.evaluate)*2,2)]
  
  pred <- prediction(x.probabilities,x.evaluate$Binary_Sec_Out_180_day_CPC_score)
  perf <- performance(pred,"tpr","fpr")
  perfs[[i]] = perf
  
  AUC<- performance(pred,"auc")
  AUC_value <- AUC@y.values[[1]]
  total_AUC <- total_AUC + AUC_value
  
  if(i==1){
    total_vimp <- varimp(x.model, conditional = T)
  } else {
    total_vimp <- total_vimp + varimp(x.model, conditional = T)
  }
}

final_AUC <- total_AUC/k
final_vimp <- total_vimp/k


par(mfrow=c(1,2))

plot(perfs[[1]], main="ROC Curves",colorize=T)
for (j in 2:k) {
  par(new=T)
  plot(perfs[[j]], main = "ROC Curves", colorize=T)
}

text(0.5,0.5,paste("Mean AUC = ",format(final_AUC,digits=5,scientific=F)))
par(new=F)

dotchart(final_vimp[order(final_vimp)])