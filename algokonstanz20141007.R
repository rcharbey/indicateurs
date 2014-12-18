#Author: Mehwish Nasim (University of Konstanz), mehwish.nasim@uni-konstanz.de
#Date: 13 August 2014
#version: 1.0

# ## function for automatically installing and loading of packages
# pkgLoad <- function(x)
# {
#   chooseCRANmirror(ind = 33)
#   if (!require(x,character.only = TRUE))
#   {
#     install.packages(x,dep=TRUE)
#     if(!require(x,character.only = TRUE)) stop("Package not found")
#   }
#   #now load library and suppress warnings
#   suppressPackageStartupMessages(library(x, character.only=TRUE))
# }
# 
# 
# pkgLoad("calibrate")
# pkgLoad("igraph")
# pkgLoad("aod")
# pkgLoad("boot")
# pkgLoad("ROSE")
# pkgLoad("ggplot2")
# pkgLoad("pamr")
# pkgLoad("vecsets")
# pkgLoad("pROC")
# pkgLoad("randomForest")
# pkgLoad("rjson")
# pkgLoad("caret")
# pkgLoad("sna")

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


workingDir = "/home/data/algopol/algopolapp/Raphael/Indicators/csa"
outputPath = "/home/data/algopol/algopolapp/Raphael/Indicators/Mehwish"
setwd(workingDir)
fnames = list.files(workingDir)


Utrain = matrix(0,0 ,18) #our temp feature matrix
egostotalcorrect = matrix(0,0,1)


for (findex in 1: length(fnames)){

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



tempattributeLinkList = matrix(0,0,2)
attributeLinkList = matrix(0,0,2)

tempfriendLinkList = matrix(0,0,2)
friendLinkList = matrix(0,0,2)

tempvisibleList = matrix(0,0,1)
notvisibleList = matrix(0,0,1)

for (i in 1:lengthFriends)
{
  
  #mutual friends here

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
#writecontent = t(friendLinkList)
#writefile =paste(fnames[findex],"friends.csv")


#write(writecontent,file=writefile, ncolumns=2, sep=",")


t = commentLinkList
t = t[-which(t[,2]==fnames[findex]),]

w=friendLinkList #list read from jsons




commentees = unique(t[,2])
allfriends= unique(w[,1])

comm = intersect(commentees,allfriends)
difference= setdiff(allfriends, comm)
# do not remove ppl from the n/w who have not commented.
difference= setdiff(commentees, comm)

# remove non friends
# 
# for (i in 1:length(difference))
# {
#   t = t[-which(t[,2]==difference[i]),]
#   
# }




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

mt =t(m)
mt = as.matrix(mt)

# create similarity indexes here:
jaccardNetwork = similarity.jaccard(g)
#alphacentralityGraph = alpha.centrality(g, alpha = 0.1)/max(alpha.centrality(g, alpha = 0.1))
#compute betweenness here:
#nodeBetweenness= betweenness(g, normalized = TRUE)

#adamicadar
adamicAdarGraph = similarity.invlogweighted(g)

#katz score:
I = diag(dim(adj)[1])
E = eigen(adj)
beta = 1/(E$values[1])
katz = (solve(I-beta*adj)) - I



U = matrix(0,0 ,18) #our final feature matrix
y = matrix(0,1 ,18) #temp matrix to hold values for features
u = 1 #number of node pairs
countones=0
# extract discussion features
userDiscussionLength = length(m[,1])
commenters = length(m[,1])
for (i in 1:commenters)
{
  print (i)

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
      
      if(as.integer(adj[a,b])==1)
      {
        countones= countones+1
      }

      # extract network features
      row1=adj[a,]
      row2 = adj[b,]
      
  
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
      # comment is for a while
      #commonEdgeNeigh =edgesCommonNeighbors(adj[a,], adj[b,], adj)
   
    
      
      commonEdgeNeigh=0
      if (commonN>1) #more than one common neighbor
      {
        for (k in 1:length(commonN))
        {
          kk=k
          for (kk in k : length(commonN))
          {
            if(kk==k)
            {next}
          
            if(adj[commonNindex[k],commonNindex[kk]] == 1)
            {
              commonEdgeNeigh = commonEdgeNeigh +1
              
            }
            else
            {
              #print("not friends")
            }
            
          }
          
          
        }
        maxpossibleEdges = commonN*(commonN-1)/2
        commonEdgeNormalized = commonEdgeNeigh/ maxpossibleEdges
      }      else{
        commonEdgeNormalized=0
      }
#       
      
      adamicAdar = adamicAdarGraph[a,b]
      if (adamicAdar==Inf)
      {
        adamicAdar =0
      }
      
      preferential= length(which(row1==1)) * length(which(row2==1))
      katzScore = katz[a,b]
      
      
      #print(adamicAdar)
      
    }else{ next;
           y[u,3]=0
            commonN=0
           commonMinN=0
           commonMaxN=0
           jaccardfriends=0
           commonEdgeNeigh=0
           commonEdgeNormalized=0
           exclusiveEdgeNeigh=0
           exclusiveEdgeNormalized=0
             adamicAdar=0
             preferential=0
           katzScore=0}
    
    y[u,4] = commonN
    y[u,5] = commonMinN
    y[u,6] = commonMaxN
    y[u,7] = jaccardfriends
    y[u,8] = commonEdgeNeigh
    y[u,9] = commonEdgeNormalized
 
    y[u,10] = adamicAdar
    y[u,11] = preferential
    y[u,12] = katzScore
    
    


   
    row1 =m[i,]
    row2=m[j,]
    count = row1+row2
    count = length(which(count==2)) 
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
     
    #print(commonMinN)
    
    # extract discussion features
    
    y[u,13] = commonD
    y[u,14] = commonMinD
    y[u,15] = commonMaxD
    y[u,16] = jaccarddiscussions
    y[u,17] = smallestDiscussion
    y[u,18] = largestDiscussion
    
    U=rbind(U,y)
    y = matrix(0,1 ,18)
      
    
  }
  
}

y = as.factor(U[,3])
x4 = (as.numeric(U[,4]))
x5 = as.integer(U[,5] )
x6 = as.integer(U[,6] )
x7 = as.numeric(U[,7] )#jaccard
x8 = as.numeric(U[,8])
x9 = as.numeric(U[,9])
x10 = as.numeric(U[,10])
x11= as.numeric(U[,11])
x12 = as.numeric(U[,12])
x13= as.numeric(U[,13])
x14 = as.numeric(U[,14])
x15 = as.numeric(U[,15])
x16 = as.numeric(U[,16])
x17 = as.numeric(U[,17])
x18 = as.numeric(U[,18])

rm(U)
data    <- data.frame(y, x4,x5,x6,x7,x8,x9,x10,x11,x12,x13,x14,x15,x16,x17,x18) 
# write dataframe to a file
setwd(outputPath)
writefile = paste(outputPath,fnames[findex], "00.csv", sep="")
write.csv(data, file = writefile,row.names=FALSE)
}


rm(t)
rm(w)
rm(m)


