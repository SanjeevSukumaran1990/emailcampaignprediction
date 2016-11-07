
#plotting correlation matrix
from pandas import scatter_matrix
scatter_matrix(input, diagonal='kde')

san=input.corr()
corr=pd.DataFrame(san)

#plotting categorical variables
san=input.day
san.value_counts().plot(kind='bar')


#looking for unique domains:
len(set(input.from_domain_hash))


#Performing anova test to see which days in week are statistically different from each other
import scipy.stats as stats 
groups = input.groupby("day").groups
# Etract individual groups
Mon = input[groups["Mon"]]
Tues= input[groups["Tues"]]
Wed = input[groups["Wed"]]
Thurs = input[groups["Thurs"]]
Fri = input[groups["Fri"]]
Sat = input[groups["Sat"]]
Sun = input[groups["Sun"]]
# Perform the ANOVA
stats.f_oneway(Mon, Tues, Wed, Thurs, Fri,Sat,Sun)

#set id as index
input=input.set_index(['id'])

#Delete website related information

input.drop('from_domain_hash', axis=1, inplace=True)
input.drop('Domain_extension', axis=1, inplace=True)

# convert week variables into dummy variables

input_day = pd.get_dummies(input['day'])
input= pd.concat([input,input_day], axis=1)
input

#drop variable for day
input.drop('day',axis=1,inplace=True)
#seperating the output from input
read_rate=input.read_rate
input.drop('read_rate', axis=1, inplace=True)
