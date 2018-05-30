library(readxl)
library(mice)
library(VIM)
library(ROCR)
library(party)

dataset <- read_excel("Imputed_data.xlsx")
set.seed(1337)

shuffled_data <- dataset[sample(nrow(dataset)),]
x.evaluate <- shuffled_data[1:200,]
x.train <- shuffled_data[-(1:200),]
treecount <- 1
trycount <- 1

ntreegrid <- c(100,150, 200 ,250, 300, 350, 400 ,450, 500,550, 600,650,700,750,800,850,900,950,1000)
mtrygrid <- c(2,3,4,5,6,7,8)

ntreeAUC <- rep(0,length(ntreegrid))
mtryAUC <- rep(0,length(mtrygrid))

for (ntreev in ntreegrid) {
  trycount <- 1
  for (mtryv in mtrygrid) {
    x.model <- cforest(as.factor(Binary_Sec_Out_180_day_CPC_score) ~ 
                         ., data = x.train,
                       control = cforest_unbiased(mtry=mtryv, ntree = ntreev))
    
    x.predictions <- predict(x.model, newdata = x.evaluate)
    
    x.probabilities <- 1- unlist(treeresponse(x.model,
                                              newdata=x.evaluate)
                                 , use.names=F)[seq(1,nrow(x.evaluate)*2,2)]
    
    pred <- prediction(x.probabilities,x.evaluate$Binary_Sec_Out_180_day_CPC_score)
    
    AUC<- performance(pred,"auc")
    
    mtryAUC[trycount] <- mtryAUC[trycount] + AUC@y.values[[1]]
    ntreeAUC[treecount] <- ntreeAUC[treecount] + AUC@y.values[[1]]
    trycount <- trycount + 1
  }
  treecount <- treecount + 1
}

mtryAUC <- mtryAUC/length(ntreegrid)
ntreeAUC <- ntreeAUC/length(mtrygrid)

par(mfrow=c(1,2))

plot(ntreegrid,ntreeAUC,main="Ntree AUC Values over grid", xlab="Ntree", ylab="Mean AUC")

plot(mtrygrid,mtryAUC,main="Mtry AUC Values over grid", xlab="Mtry",ylab="Mean AUC")