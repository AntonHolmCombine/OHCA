parseTree <- function(x.model){
  
  for (i in 37:length(x.model@ensemble)){
    
    atree <- prettytree(x.model@ensemble[[i]], names(x.model@data@get("input"))) 
    
    con <- file(paste("TreeTxt_",i,".txt",sep=""))
    sink(con,append=TRUE)
    print(atree)
    sink()
  }
  sink()
  
}


