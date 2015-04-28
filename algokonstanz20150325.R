#Author: Mehwish Nasim (University of Konstanz), mehwish.nasim@uni-konstanz.de
#Date: 25 March 2015
#version: 2.1
#changes: 1. updated Adamic Adar zero condition
#         2. damping factor for katz index
#         3. file name convention  
#         4. added cosine similarity
#         - removed. clustering coeff*
#         6. Added Network perturbation*
#         7. added more readable comments after Features names 
#         8. Add gender attribute - in next version
## function for automatically installing and loading of packages
pkgLoad <- function(x)
{
  chooseCRANmirror(ind = 33)
  if (!require(x,character.only = TRUE))
  {
    install.packages(x,dep=TRUE)
    if(!require(x,character.only = TRUE)) stop("Package not found")
  }
  #now load library and suppress warnings
  suppressPackageStartupMessages(library(x, character.only=TRUE))
}

#Network perturbation-randomly assume that some percentage of users do not have their friendship lists visible.
perturb <- function(adj, val){
  
  val = val*0.01
  newadj = as.matrix(adj)
  newadj[lower.tri(newadj, diag=TRUE)] =0
  samp = which(newadj==1)
  #sampsize = round((length(adj)-length(adj[1,]))*0.5*val)
  sampsize = round(length(samp)*val)
  
  s = sample(1:length(samp), sampsize, replace=F)  
  newadj[samp[s]] = 0
  newadj = symmetrize(as.matrix(newadj), rule="upper", return.as.edgelist=FALSE)
  return(newadj)
}




pkgLoad("calibrate")
pkgLoad("igraph")
pkgLoad("aod")
pkgLoad("boot")
pkgLoad("ROSE")
pkgLoad("ggplot2")
pkgLoad("pamr")
pkgLoad("vecsets")
pkgLoad("pROC")
pkgLoad("randomForest")
pkgLoad("rjson")
pkgLoad("caret")
pkgLoad("sna")
pkgLoad("arules")

library(calibrate)
library(igraph)
library(aod)
library(boot)
library(ROSE)
library(ggplot2)
library(pamr)
library(vecsets)
library(pROC)
library(randomForest)
library(rjson)
library(caret)
library(sna)
library(arules)
#how much error to create in the network
pVal = 50

workingDir = "/home/data/algopol/algopolapp/Raphael/Indicators/csa"
outputPath = "/home/data/algopol/algopolapp/Raphael/Indicators/ninety/"
# workingDir = "C:\\Users\\Mehwish\\Documents\\Link Prediction\\algopol-5egos-csa-nolinks\\algopol-5egos-csa-nolink-new\\Sample\\"
# outputPath = "C:\\Users\\Mehwish\\Documents\\Link Prediction\\algopol-5egos-csa-nolinks\\algopol-5egos-csa-nolink-new\\newoutput\\"

setwd(workingDir)
fnames = list.files(workingDir)

Utrain = matrix(0,0 ,18) #our temp feature matrix

for (findex in 1: length(fnames)){
  possibleError <- tryCatch({
    
    print(paste(workingDir,fnames[findex], sep="/"))
    
    #setwd(paste(workingDir,fnames[findex], sep="/"))
    setwd(paste(workingDir,fnames[findex], sep="/"))
  ###############read statuses
  
  statusesFile <- readLines("statuses.jsons.gz")
  
  lengthStatus = length(statusesFile)
  m=matrix(1, 0,lengthStatus)
  
  tempcommentLinkList = matrix(0,0,2)
  
  commentLinkList = matrix(0,0,2)
  
  for (i in 1:lengthStatus)
  {
    statuses = fromJSON( statusesFile[i], method = "C", unexpected.escape = "error" )
    #print(statuses[[i]]$type)
    comment = matrix(0,0,length(statuses$comments))
    
    if(length(statuses$comments )== 0)
    {next}
    
    for(j in 1:length(statuses$comments))
    {
      #comment[j]=statuses[[i]]$comments[[j]]$from$id
      if(length(statuses$comments[[j]]$from$id) != 0)
      {
        tempcommentLinkList[1]= statuses$id
        tempcommentLinkList[2]= statuses$comments[[j]]$from$id
        commentLinkList=rbind(commentLinkList,tempcommentLinkList)
      }
      
      
    }
    
  }
  
  
  #rm(statusesFile) # remove the status file from memory
  ################# FRIENDS #####################
  
  
  friendsFile <- readLines("friends.jsons.gz")
  
  lengthFriends = length(friendsFile)
  if (lengthFriends>250)
    next;
  
  
  tempattributeLinkList = matrix(0,0,2)
  attributeLinkList = matrix(0,0,2)
  
  tempfriendLinkList = matrix(0,0,2)
  friendLinkList = matrix(0,0,2)
  
  tempvisibleList = matrix(0,0,1)
  notvisibleList = matrix(0,0,1)
  
  for (i in 1:lengthFriends)
  {
    
    #mutual friends here
    #print(i)
    friends = fromJSON( friendsFile[i], method = "C", unexpected.escape = "error" )
    if(length(friends)>1)
    {
      
      friend = matrix(0,0,length(friends$mutual))
      
      if(length(friends$mutual)== 0)
      {
        tempvisibleList[1]= friends$id
        
        notvisibleList=rbind(notvisibleList,tempvisibleList)
        
        next
      }  
      
      for(j in 1:length(friends$mutual))
        
      {
        
        
        tempfriendLinkList[1]= friends$id
        tempfriendLinkList[2]= friends$mutual[[j]]$id
        friendLinkList=rbind(friendLinkList,tempfriendLinkList)
        
        
      }
    }
    
    
    
  }
  
  #rm(friendsFile) # remove the status file from memory
  #write content to make graphs
  # writecontent = t(friendLinkList)
  #  writefile =paste(fnames[findex],"friends.csv",sep="")
  # write(writecontent,file=writefile, ncolumns=2, sep=",")
  
  
  t = commentLinkList
  t = t[-which(t[,2]==fnames[findex]),]
  
  w=friendLinkList #list read from jsons
  
  
  
  
  first=unique(t[,1])
  second=unique(t[,2])
  extract=function(x){
    rle=rle(sort(x));
    r=matrix(0,1,length(first));
    colnames(r)=first;
    if(rle$lengths > 0){
      #r[1,rle$values] = rle$lengths;
      r[1,rle$values] = 1;
    }
    
    
    return(r)
  }
  
  h=tapply(t[,1], t[,2], extract, simplify=F)
  
  m=matrix(0, 0,length(first))
  colnames(m)=first
  for(line in h) m=rbind(m,line)
  rownames(m)=names(h)
  
  
  g <- graph.data.frame(w, directed=FALSE)
  g=simplify(g)
  adj=get.adjacency(g)
  
  # sampling for perturbing the network:
  adjnew = perturb (adj,pVal)
  g2 = graph.adjacency(adjnew)
  
  # create similarity indexes here:
  jaccardNetwork = similarity.jaccard(g2)
  adjnew = get.adjacency(g2)
  
  
  #cosine similarity
  
  cosineSim = as.matrix(dissimilarity(as.matrix(adjnew),method="cosine"))
  
  #adamicadar: issues with 0/1 neighbors
  adamicAdarGraph = similarity.invlogweighted(g2)
  
  #katz score:
  I = diag(dim(adjnew)[1])
  E = eigen(adjnew)
  beta = (1/(E$values[1]))*0.1
  katz = (solve(I-beta*adjnew)) - I
  
  U = matrix(0,0 ,19) #our final feature matrix
  y = matrix(0,1 ,19) #temp matrix to hold values for features
  u = 1 #number of node pairs
  
  # extract discussion features
  
  commenters = length(m[,1])
  
  for (i in 1:commenters)
  {
    #print (i)
    
    j =i
    commonN=0
    commonMinN=0
    commonMaxN=0
    jaccardfriends=0
    commonEdgeNeigh=0
    commonEdgeNormalized=0
    exclusiveN=0
    exclusiveEdgeNeigh=0
    exclusiveEdgeNormalized=0 
    cosineN=0
    adamicAdar=0
    preferential=0
    katzScore=0
    
    for(j in i:commenters)
    {
      if(i==j)
      {next}
      
      
      
      a= which(rownames(adj)[]==rownames(m)[i])
      b= which(rownames(adj)[]==rownames(m)[j])
      
      if((length(a)!=0) && (length(b)!=0))
      {
        y[u,1] = rownames(m)[i]
        y[u,2] = rownames(m)[j]
        y[u,3] = as.integer(adj[a,b])
        
        
        # extract network features
        row1=adjnew[a,]
        row2 = adjnew[b,]
        
        
        commonNindex = which((row1+row2)==2)
        
        
        count = length(commonNindex) 
        commonN=count
      
        
        if((sum(row1)!=0) && (sum(row2)!=0))
        {
          commonMinN= count/(min(sum(row1),sum(row2)))
          commonMaxN = count/(max(sum(row1),sum(row2)))
        }else
        {
          commonMinN=0
          commonMaxN=0
          
        }
        jaccardfriends = jaccardNetwork[a,b]
        
        
        cosineN = cosineSim[a,b]
        adamicAdar = adamicAdarGraph[a,b]          
        preferential= length(which(row1==1)) * length(which(row2==1))
        katzScore = katz[a,b]
        
        
      }else{
        
        
        
        next;
        y[u,3]=0
        commonN=0
        commonMinN=0
        commonMaxN=0
        jaccardfriends=0
        commonEdgeNeigh=0
        commonEdgeNormalized=0
        exclusiveEdgeNeigh=0
        exclusiveEdgeNormalized=0
        cosineN=0
        adamicAdar=0
        preferential=0
        katzScore=0}
      
      y[u,4] = commonN
      y[u,5] = commonMinN
      y[u,6] = commonMaxN
      y[u,7] = jaccardfriends
      y[u,8] = commonEdgeNeigh
      y[u,9] =commonEdgeNormalized
      
      y[u,10] = adamicAdar
      y[u,11] = preferential
      y[u,12] = katzScore
      y[u,13] = cosineN
      
      
      
      
      
      row1 =m[i,]
      row2=m[j,]
      count = row1+row2
      commontalks=which(count==2)
      count = length(commontalks) 
      commonD=count
      if((sum(row1)!=0) && (sum(row2)!=0))
      {
        commonMinD= count/(min(sum(row1),sum(row2)))
        commonMaxD = count/(max(sum(row1),sum(row2)))
      }else
      {
        commonMinD=0
        commonMaxD=0
        
      }
      
      
      subset = which((m[i,]+m[j,])==2)
      intsec = length(subset)
      union= length(which((m[i,]+m[j,])!=0))
      
      if (union!=0)
      {
        jaccarddiscussions = intsec/union
      }
      else
      {jaccarddiscussions = 0}
      
      if(length(subset)!=0){
        #smallest
        if(length(subset)==1)
        { c =sum(m[,subset])
          
        }else{ c =colSums(m[,subset])}
        
        smallestDiscussion = as.integer(c[which.min(c)])
        
        #largest
        largestDiscussion = as.integer(c[which.max(c)])
      }else{smallestDiscussion=0
            largestDiscussion=0}
      
      
      
      y[u,14] = commonD
      y[u,15] = commonMinD
      y[u,16] = commonMaxD
      y[u,17] = jaccarddiscussions
      y[u,18] = smallestDiscussion
      y[u,19] = largestDiscussion
      
      U=rbind(U,y)
      y = matrix(0,1,19)
      
      
    }
    
  }
  
  y = as.factor(U[,3])
  x4 = (as.numeric(U[,4])) #common neighbors
  x5 = as.integer(U[,5] ) #common neighbors normalized(min)
  x6 = as.integer(U[,6] ) #common neighbors normalized (max)
  x7 = as.numeric(U[,7] )#jaccard
  #x8 = as.numeric(U[,8]) #Edges between common neighbors
  #x9 = as.numeric(U[,9]) #edges between common neighbors normalized (max. possible edges)
  x10 = as.numeric(U[,10]) #Adamic Adar distance
  x11= as.numeric(U[,11]) #Preferential attachment score
  x12 = as.numeric(U[,12]) #katz index
  x13= as.numeric(U[,13]) # cosine similarity
  x14 = as.numeric(U[,14]) # common discussions
  x15 = as.numeric(U[,15]) # common discussions normalized (min)
  x16 = as.numeric(U[,16]) # common discussions normalized (max)
  x17 = as.numeric(U[,17]) # jaccard discussions
  x18 = as.numeric(U[,18]) #smallest discussion size
  x19 = as.numeric(U[,19]) # largest discussion size
  
  
  
  
  #rm(U)
  data    <- data.frame(y, x4,x5,x6,x7,x10,x11,x12,x13,x14,x15,x16,x17,x18,x19) 
  # write dataframe to a file
  setwd(outputPath)
  print(getwd())
  writefile = paste(outputPath,pVal,"_", fnames[findex],".csv", sep="")
  write.csv(data, file = writefile,row.names=FALSE)

  }, error = function(e){e})

      if(inherits(possibleError, "error")){
        print("error")
        print(possibleError)
        next
      } else{    
        print("no error")
      }


}


rm(t)
rm(w)
rm(m)



