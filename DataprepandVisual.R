#R script

input <- read.csv(file="email.csv",head=TRUE,sep=",")
#checking for rows with null values
new_DF <- input[rowSums(is.na(input)) > 0,]

#removing row with null values
input <- input[-c(59976), ]

#remove duplicates

input <- unique( input)
input2<-input
#removing categorical variables for correlation matrix and checking distribution
input2<-within(input2,rm(from_domain_hash,Domain_extension,day))
#look into distribution
summary(input2)
hist(input2$read_rate)
hist(input2$campaign_size)
hist(input2$unique_user_cnt)
hist(input2$avg_domain_read_rate)
hist(input2$avg_domain_inbox_rate)
hist(input2$avg_user_avg_read_rate)
hist(input2$avg_user_domain_avg_read_rate)
hist(input2$mb_superuser)
hist(input2$mb_engper)
hist(input2$mb_engsec)
hist(input2$mb_inper)
hist(input2$mb_insec)
hist(input2$mb_unengsec)
hist(input2$mb_idlesub)
hist(input2$mb_superuser)


##remove outliers in inpu
input2<-subset(input2,read_rate<0.65 & campaign_size<15000 & avg_user_avg_read_rate<0.6 & avg_domain_read_rate<0.45 & avg_user_domain_avg_read_rate<0.6 & mb_supersub<0.5 & mb_inper<0.44982 &  mb_insec<0.6 & mb_unengsec<0.55 & mb_idlesub<0.1 & mb_engsec<0.5 & mb_superuser<0.5)
summary(input2)


library(reshape2)
library(ggplot2)

ggplot(data = melt(input2), mapping = aes(x = value)) + 
  geom_histogram(bins = 10) + facet_wrap(~variable, scales = 'free_x')

hist(input$read_rate)



#plot correlation matrix
install.packages("corrplot")
library(corrplot)
M <- cor(input2)
corrplot(M, method="square")


#plotting days
day<-input['day']
barplot(prop.table(table(day)))

#preparing data for regression


input<-subset(input,read_rate<0.65 & campaign_size<15000 & avg_user_avg_read_rate<0.6 & avg_domain_read_rate<0.45 & avg_user_domain_avg_read_rate<0.6 & mb_supersub<0.5 & mb_inper<0.44982 &  mb_insec<0.6 & mb_unengsec<0.55 & mb_idlesub<0.1 & mb_engsec<0.5 & mb_superuser<0.5)
rownames(input) <- input$id
input<-within(input,rm(from_domain_hash,Domain_extension))


#creating dummy code for days
inds <- model.matrix(~ factor(input$day) - 1)
day<-as.data.frame(inds)
day["id"]<-input["id"]
input<-merge(input,day,by="id")

input$day<-NULL
input$id<-NULL
input$ campaign_size<-NULL

#save the y parameter

y<-input$read_rate
input$read_rate<-NULL
#scaling the data
mmnorm <-
  function (data,minval=0,maxval=1) 
  {
    #This is a function to apply min-max normalization to a matrix or dataframe.
    #Min-max normalization subtracts the minimum of an attribute from each value
    #of the attribute and then divides the difference by the range of the attribute.
    #These new values are multiplied by the given range of the attribute
    #and finally added to the given minimum value of the attribute.
    #These operations transform the data into [minval,mxval].
    #Usually minval=0 and maxval=1.
    #Uses the scale function found in the R base package.
    #Input: data= The matrix or dataframe to be scaled
    
    
    #store all attributes of the original data
    d=dim(data)
    c=class(data)
    cnames=colnames(data)
    
    #remove classes from dataset
    classes=data[,d[2]]
    data=data[,-d[2]]
    
    minvect=apply(data,2,min)
    maxvect=apply(data,2,max)
    rangevect=maxvect-minvect
    zdata=scale(data,center=minvect,scale=rangevect)
    
    #remove attributes added by the function scale and turn resulting
    #vector back into a matrix with original dimensions
    #attributes(zdata)=NULL
    #zdata=matrix(zdata,dim(data)[1],dim(data)[2])
    
    newminvect=rep(minval,d[2]-1)
    newmaxvect=rep(maxval,d[2]-1)
    newrangevect=newmaxvect-newminvect
    zdata2=scale(zdata,center=FALSE,scale=(1/newrangevect))
    zdata3=zdata2+newminvect
    
    zdata3=cbind(zdata3,classes)
    
    if (c=="data.frame") zdata3=as.data.frame(zdata3)
    colnames(zdata3)=cnames
    return(zdata3)
    
  }
input<-mmnorm(input)

#added because of problems in residual plot

#log transformation
#input[,1:20]<-log(input[,1:20]+1)


input["read_rate"]<-y

library(data.table)
setnames(input, old = c('factor(input$day)Mon','factor(input$day)Sat','factor(input$day)Sun','factor(input$day)Thurs','factor(input$day)Tues','factor(input$day)Wed'), new = c('Mon','Sat','Sun','Thurs','Tues','Wed'))
setnames(input,old=c('factor(input$day)Fri'),new = c('Fri'))

















