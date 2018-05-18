sunBurstPlot <- function(x.model){
  
  library(readr)
  library(stringi)
  library(party)
  library(sunburstR)
  library(randomcoloR)

  treenbr <- 1
  nameList <- c("Good","Bad")
  pathList <- c()
  amountList <- integer()
  visited <- integer()
  visitedLeft <- integer()
  visitedRight <- integer()
  backtrackList <- list()
  keepGoing <- TRUE
  
  pt <- prettytree(x.model@ensemble[[1]], names(x.model@data@get("input")))
  
  while(keepGoing){
    if(pt$terminal==TRUE){
      tempPath <- ""
      for (i in 1:length(backtrackList)){
        tempPath <- paste(tempPath, backtrackList[[i]]$psplit$variableName,"-",sep="")
        
      }
      if(pt$prediction[1]>0.5){
        tempPath <- paste(tempPath,"Bad",sep="")
      } else {
        tempPath <- paste(tempPath,"Good",sep="")
      }

      pathList[length(pathList)+1] <- tempPath
      amountList[length(amountList)+1] <- pt[[10]]
      pt <- backtrackList[[length(backtrackList)]]
      
    } else if(!(pt$nodeID %in% visited)){
      if(!(pt$psplit$variableName %in% nameList)){
        nameList[length(nameList)+1] <- pt$psplit$variableName
      }
      visited[length(visited)+1] <- pt$nodeID
      backtrackList[[length(backtrackList)+1]] <- pt
      visitedLeft[length(visitedLeft)+1] <- pt$nodeID
      pt <- pt$left
      
    } else if(!(pt$nodeID %in% visitedRight)){
      visitedRight[[length(backtrackList)+1]] <- pt$nodeID
      pt <- pt$right
      
    } else {
      if(pt$nodeID == 1){
        keepGoing = FALSE
      } else {
        pt <- backtrackList[[length(backtrackList)-1]]
        backtrackList <- head(backtrackList,-1)
      }

    }
    
  }
  colorList <- c("#00ff00","#ff0000")
  colorList <- c(colorList, randomColor(count=length(nameList)-2,hue="blue",luminosity = "bright"))
  data <- data.frame(pathList,amountList)
  sunburst(data, legend = list(w=250,h=27,r=15,s=5),color=list(range=colorList,domain=nameList),legendOrder = nameList)
}
