library(readxl)
library(mice)
library(VIM)
library(ROCR)
library(party)

set.seed(1337)

dataset <- read_excel("Imputed_Data.xlsx")


shuffled_data <- dataset[sample(nrow(dataset)),]

k <- 8
rows <- nrow(shuffled_data)
increments <- floor(rows/k)
perfs <- list()
total_AUC <- 0

for (i in 1:k) {
  
  
  x.evaluate <- shuffled_data[(increments*(i-1)+1):(i*increments),]
  x.train <- shuffled_data[-((increments*(i-1)+1):(i*increments)),]
  
  
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
colorbar <- c()
for (i in 1:length(final_vimp)){
  colorbar[i] <- paste("#00",as.hexmode(floor(255-((i-1)*(200/length(final_vimp))))),"00",sep="")
}
colorbar <- rev(colorbar)

par(mfrow=c(1,2),mar = c(5,5,5,5))

plot(perfs[[1]], main="ROC Curves",colorize=T,legend= FALSE)

for (j in 2:k) {
  par(new=T)
  plot(perfs[[j]], main = "ROC Curves", colorize=T)
}

text(0.5,0.5,paste("Mean AUC = ",format(final_AUC,digits=5,scientific=F)))
par(new=F,mar=c(5,14,3,3))
barplot(final_vimp[order(final_vimp)],horiz=T,main="Relative Variable Importance",col=colorbar,las=1)

con <- file("TestVimp.txt")

final_vimp <- final_vimp[order(-final_vimp)]

writeLines(paste(1:length(final_vimp),names(final_vimp),final_vimp[names(final_vimp)]),con)

for (j in 1:length(perfs)){
  con <- file(paste("TestAUC_",j,".txt",sep=""))
  writeLines(paste(1:length(perfs[[j]]@x.values[[1]]),perfs[[j]]@x.values[[1]],perfs[[j]]@y.values[[1]]),con)
  
}