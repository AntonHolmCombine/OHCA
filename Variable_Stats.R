library(readxl)

dataset <- read_excel("Data.xlsx")

vnames <- names(dataset)
y_data <- dataset[vnames[length(vnames)]][[1]]
vnames <- vnames[-length(vnames)]

binaryV <- c("B_Sex","B_CHF","B_Previous_AMI","B_IHD","B_Previous_arrhythmia","B_Previous_cardiac_arrest"
             ,"B_Arterial_hypertension","B_TIA_or_stroke","B_Epilepsy","B_Diabetes"
             ,"B_asthma_COPD","B_Chronic_dialysis","B_Alcoholism","B_Previous_PCI"
             ,"B_Previous_CABG","B_Previous_valvular_surgery","B_ICD"
             ,"B_Pacemaker","P_Bystander_witnessed_arrest","P_Bystander_CPR"
             ,"P_Bystander_defibrillation","P_Automatic_compression_decompression"
             ,"P_Pre_hospital_intubation","P_Seizures_before_admission","A_Pupil_refelx"
             ,"A_Cormeal_reflex","A_Cough_reflex","A_Spontaneous_breathing"
             ,"A_Shock_on_admission","Malignancy")

intervalV <- c("B_Age","B_Length","B_Weight","P_Number_of_defibrillations"
               ,"P_CA_to_ALS_min","No_flow","Lo_flow","P_Dose_of_adrenaline"
               ,"A_Initial_temperature","A_pH")


for (i in 1:2){
  con <- file(paste("Output_Relation_",vnames[i],".txt",sep=""))
  
  if(vnames[i] %in% binaryV){
    goodcount <- c(0,0)
    badcount <- c(0,0)
    xlist <- c(0,1)
    
    for (j in 1:nrow(dataset)){
      if(!is.na(dataset[vnames[i]][[1]][j]) && !is.na(y_data[j])){
        if(dataset[vnames[i]][[1]][j]>=1){
          if(y_data[j]==0){
            goodcount[2]<-goodcount[2] + 1
          } else{
            badcount[2]<-badcount[2] + 1
          }
          
        } else {
          if(y_data[j]==0){
            goodcount[1]<-goodcount[1] + 1
          } else{
            badcount[1]<-badcount[1] + 1
          }
        }
      }
    }
  } else if(vnames[i] %in% intervalV){
    meanV <- mean(dataset[vnames[i]][[1]],na.rm=T)
    stdV <- sd(dataset[vnames[i]][[1]],na.rm=T)
    goodcount <- c(0,0,0,0)
    badcount <- c(0,0,0,0)
    intervals <- list(c(0,meanV-stdV),c(meanV-stdV,meanV),c(meanV,meanV+stdV),c(meanV+stdV,300))
    xlist <- c(paste("<",round(meanV-stdV,digits = 2),sep=""),paste(round(meanV-stdV,digits = 2),"-",round(meanV,digits = 2),sep=""),paste(round(meanV,digits = 2),"-",round(meanV+stdV,digits = 2),sep=""),paste(">",round(meanV+stdV,digits = 2),sep=""))
    
    for (j in 1:nrow(dataset)){
      if(!is.na(dataset[vnames[i]][[1]][j]) && !is.na(y_data[j])){
        indexV <- 0
        if(dataset[vnames[i]][[1]][j]<intervals[[1]][2]){
          indexV <- 1
        } else if(dataset[vnames[i]][[1]][j]>intervals[[4]][1]){
          indexV<-4
        } else if(dataset[vnames[i]][[1]][j]>intervals[[3]][1]){
          indexV <-3
        } else{
          indexV <-2
        }
        if(y_data[j]==0){
          goodcount[indexV]<-goodcount[indexV] + 1
        } else{
          badcount[indexV]<-badcount[indexV] + 1
        }
      }
    }
  }
  tp <- gsub("_"," ",vnames[i])
  tp <- c(tp, paste(paste("\"",xlist,paste(" (",goodcount+badcount,")",sep=""),"\"",sep=""),goodcount,badcount))
  writeLines(tp,con,sep="\n")
}