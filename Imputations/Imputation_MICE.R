library(xlsx)
library(readxl)
library(mice)

dataset <- read_excel("Data_Smart_Zeros.xlsx",sheet = 1)

imputed_data <- mice(dataset, m=20, maxit=40, method="pmm", seed = 500)

complete_data <- complete(imputed_data)
attributes(complete_data)$class <- c("data.frame")

write.xlsx(complete_data, "Imputed_Data_Smart_Zero.xlsx", row.names = F)