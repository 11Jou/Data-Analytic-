#!/usr/bin/env python
# coding: utf-8

# # About the Data:-
# The dataset includes:
# 
# WuzzufJobPosts_Sample : a sample of jobs posted on WUZZUF during 2014-2016.
# 
# WuzzufApplicationsSample : the corresponding applications (Excluding some entries).
# 
# Note: The jobs are mainly in Egypt but other locations are included.
# 
# Note: This Exploration is only about WuzzufJobPosts_Sample dataset

# In[3]:


get_ipython().system('pip install plotly.express')
get_ipython().system('pip install wordcloud')


# ## Importing libraries:

# In[4]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
import plotly.express as px
import plotly.graph_objs as go


# In[5]:


import warnings
warnings.filterwarnings('ignore')


# ## Gathering:

# In[6]:


df=pd.read_csv('Wuzzuf_Job_Posts_Sample.csv')


# # Assessing Data:

# In[7]:


df.head()


# ### Using info(): to know columns names ,datatypes and the non null count.

# In[8]:


df.info()


# ### Using describe(): to know the summation of each column ,if there missing value or not , And some statistics operations like(mean,max,min,….)

# In[9]:


df.describe()


# ### using duplicated():to know if there any duplicated value.

# In[10]:


df.duplicated().value_counts()


# ## Data issues:-
# ##### 1- wrong data types in some columns
# ##### 2- some columns that do not affect the analysis need to be dropped
# ##### 3-job_category columns have some irrelevant data
# ##### 4-job_category1 need to be fixed (the categories is in one cell and need to be separated ) 
# ##### 5-the same isuues in job industry columns
# ##### 6-city column in inconsistent

# # Cleaning 

# In[11]:


df.drop(['job_description','job_requirements'],axis=1,inplace=True)
df.head()


# In[12]:


df_1=df


# # 

# In[13]:


df['job_category']=df['job_category1']+'/'+df['job_category2']+'/'+df['job_category3']
df.drop(['job_category1','job_category2','job_category3'],axis=1,inplace=True)
sub_df=df[['id','job_category']]
sub_df['job_category']=sub_df['job_category'].str.split('/')
sub_df


# In[14]:


iterator=0
flat_list_jc=[]
flat_list_id=[]
job_category=list(sub_df['job_category'])
while iterator < 21850 :
    for i in job_category[iterator]:
        flat_list_jc.append(i)
        flat_list_id.append(sub_df.iloc[iterator][0])
    iterator=iterator+1       


# In[15]:


t_df= pd.DataFrame(list(zip(flat_list_id, flat_list_jc)),columns =['id', 'job_category'])
t_df.head()


# In[16]:


df.drop('job_category',axis=1,inplace=True)
semi_final_df=pd.merge(t_df,df,on='id',how='left')


# In[17]:


semi_final_df.head()


# In[18]:


ind=semi_final_df[semi_final_df['job_category']=='Select'].index
semi_final_df.drop(ind,inplace=True)


# In[19]:


semi_final_df['job_industry']=semi_final_df['job_industry1']+'/'+semi_final_df['job_industry2']+'/'+semi_final_df['job_industry3']
semi_final_df.drop(['job_industry1','job_industry2','job_industry3'],axis=1,inplace=True)
sub_df=semi_final_df[['id','job_industry']]
sub_df['job_industry']=sub_df['job_industry'].str.split('/')
sub_df


# In[20]:


iterator=0
flat_list_jc=[]
flat_list_id=[]
job_category=list(sub_df['job_industry'])
while iterator < 21850 :
    for i in job_category[iterator]:
        flat_list_jc.append(i)
        flat_list_id.append(sub_df.iloc[iterator][0])
    iterator=iterator+1       


# In[21]:


t_df= pd.DataFrame(list(zip(flat_list_id, flat_list_jc)),columns =['id', 'job_industry'])
t_df.head()


# In[22]:


semi_final_df.drop('job_industry',axis=1,inplace=True)
final_df=pd.merge(t_df,semi_final_df,on='id',how='left')
ind=final_df[final_df['job_industry']=='Select'].index
final_df.drop(ind,inplace=True)
final_df


# In[23]:


df_1['post_date']=pd.to_datetime(df_1['post_date'])
df_1['year']=df_1['post_date'].dt.year
df_1['month']=df_1['post_date'].dt.month


# In[24]:


df_1


# In[25]:


df_1.info()


# In[26]:


final_df.info()


# In[27]:


final_df['city'].value_counts().head(6)


# In[28]:


final_df['job_industry'].value_counts()


# In[29]:


import re 
l = final_df.experience_years.values
range_exps =[]
for i in l:
    pattern =re.findall('\\b\\d+\\b', i)
    if len(pattern) == 0:
        #min_exp = min([int(s) for s in i if s.isdigit()])
        max_exp = max([int(s) for s in i if s.isdigit()])
    else:
        #min_exp = min([int(s) for s in pattern])
        max_exp = max([int(s) for s in pattern])
    # check for the + sign
    if '+' in i:
        max_exp += 3
    # add to our cleaned list
    if max_exp == 0 :
        range_exp = 'Fresh'
    elif 0 < max_exp <= 5:
        range_exp = 'below 5'
    elif 5 < max_exp <= 10:
        range_exp = '5-10'
    elif 10 < max_exp <= 15:
        range_exp = '10-15'
    elif 15 < max_exp <= 20:
        range_exp = '15-20'
    elif 20 < max_exp <= 25:
        range_exp = '20-25'
    else:
        range_exp = 'above 25'
    range_exps.append(range_exp)


# In[30]:


len(range_exps) == final_df.shape[0]


# In[31]:


final_df['experience_range'] = range_exps


# In[32]:


final_df.experience_range.unique()


# In[33]:


final_df['experience_range'].value_counts()


# In[34]:


final_df.info()


# In[35]:


Top10_jobs=final_df.job_category.sort_values().value_counts().head(10)
Top10_jobs


# In[36]:


Top10_salary=final_df.salary_maximum.sort_values().value_counts().head(10)
Top10_salary


# # 

# 
# # 1) univariate 

# # 

# ### What is the most popular job industries?
# ###### it's obvious that computer science, IT services, and computer-related industries are the most popular industries on WUZZUF
# ###### then we have  marketing , engineering & education 
# ###### then business-related industries
# 

# In[37]:


plt.figure(figsize=[8,8])
order=final_df['job_industry'].value_counts()
order=pd.DataFrame(order)
order=order.head(35)
order=order.index
blue=sb.color_palette()[0]
sb.countplot(data=final_df,y='job_industry',order=order,color=blue);
plt.title("job industry according its count");
plt.ylabel('job industry');


# # 

# ### What is the most popular job categories ?
# 
# ###### software-related categories are the most popular
# ###### then business-related 
# ###### then engineering

# In[38]:


plt.figure(figsize=[8,8])
order=final_df['job_category'].value_counts()
order=pd.DataFrame(order)
order=order.head(35)
order=order.index
sb.countplot(data=final_df,y='job_category',order=order,color=blue);
plt.title("job category according its count ");
plt.ylabel('job category');


# ## What is the Top 10 popular job categories ?
# ##### 1)IT&Software Development
# ##### 2)Business Development
# ##### 3)Sales
# ##### 4)Retail
# ##### 5)Engineering 
# ##### 6)Customer Service
# ##### 7)Support 
# ##### 8)Marketing
# ##### 9)Design

# In[39]:


jobs=['IT','Software Development','Business Development','Sales' ,'Retail' ,'Engineering','Customer Service','Support','Marketing','Design']
fig = px.bar(x=jobs,y=Top10_jobs,color=jobs)
# Create the dropdown
dropdown_buttons = [
{'label': 'All','method': 'update','args': [{'visible': [False, True, True,True, True,True, True,True,True,True]},{'title': 'All'}]},    
{'label': 'IT','method': 'update','args': [{'visible': [True,False, False,False, False,False, False,False,False, False]},{'title': 'IT'}]},
{'label': 'Software Development','method': 'update','args': [{'visible': [False, True, False,False, False,False, False,False,False, False]},{'title': 'Software Development'}]},
{'label': "Business Development",'method': "update",'args': [{"visible": [False, False, True,False, False,False, False,False,False, False]},{'title': 'Business Development'}]},
{'label': 'Sales','method': 'update','args': [{'visible': [False, False, False,True, False,False, False,False,False, False]},{'title': 'Sales'}]},
{'label': 'Retail','method': 'update','args': [{'visible': [False, False, False,False, True,False, False,False,False, False]},{'title': 'Retail'}]},
{'label': 'Engineering','method': 'update','args': [{'visible': [False, False, False,False, False,True, False,False,False, False]},{'title': 'Engineering'}]},
{'label': 'Customer Service','method': 'update','args': [{'visible': [False, False, False,False, False,False,True,False,False, False]},{'title': 'Customer Service'}]},
{'label': 'Support','method': 'update','args': [{'visible': [False, False, False,False, False,False,False,True,False,False]},{'title': 'Support'}]},
{'label': 'Marketing','method': 'update','args': [{'visible': [False,False,False,False, False,False, False,False,True,False]},{'title': 'Marketing'}]},
{'label': 'Design','method': 'update','args': [{'visible': [False, False, False,False, False,False,False,False, False,True]},{'title': 'Design'}]}
]
fig.update_layout({'updatemenus':[{'type': "dropdown",'x':1.3,'y': 0.35,'showactive': True,'active': 0,'buttons': dropdown_buttons}]
})
fig.show()


# # 

# ### What is the most active cities in posting jobs?
# ###### You can see that Cairo, Giza & Alexandria are more active in posing jobs than the others

# In[40]:


from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
c_list=[]
for i in final_df['city']:
    c_list.append(i.lower())
   
plt.figure(figsize=[18,6]);
words = ' '.join(c_list);


# Generate a word cloud image
wordcloud = WordCloud().generate(words)


# lower max_font_size
wordcloud = WordCloud(max_font_size=40,background_color="white").generate(words)

plt.imshow(wordcloud, interpolation="bilinear")

plt.axis("off")

plt.show()


# # 

# ### What is the top job titles ?
# ###### Call center , sales engineer, customer servies, graphing designer and social media

# In[41]:


from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
plt.figure(figsize=[18,6]);
words = ' '.join(final_df['job_title']);


# Generate a word cloud image
wordcloud = WordCloud().generate(words)


# lower max_font_size
wordcloud = WordCloud(max_font_size=40,background_color="white").generate(words)

plt.imshow(wordcloud, interpolation="bilinear")

plt.axis("off")

plt.show()


# # 

# ### Describe Minimum & Maximum salary in Egyptian Pound
# ###### - in minimum salaries  the majority From 1000 LE to 3500 LE vs from 2000 LE to 6000 LE in maximum salaries 
# ###### - in minimum salaries, from 3500 LE to 8000 LE is common knowing it's reducing starting from 3500 LE , after 8000 LE is rare
# ###### -in maximum salaries, from 6000 LE to 8000 LE  is common also 10000 , knowing it's reducing starting from 6000 , after 10000 is rare

# In[42]:


sub_df=final_df[final_df['salary_maximum']<=11000]
sub_df=sub_df[['salary_maximum','currency']]
s=px.histogram(data_frame=sub_df,x='salary_maximum',color='currency',nbins=20,title='distribution of salary maximum')
s.show()


# In[43]:


sub_df=final_df[final_df['salary_minimum']<=9000]
sub_df=sub_df[['salary_minimum','currency']]
s=px.histogram(data_frame=sub_df,x='salary_minimum',color='currency',nbins=15,title='distribution of salary minimum')
s.show()


# # 

# # 

# ### what is the chance for a fresh grad to get a job ?
# ###### actually, there are huge amount of opportunities for the fresh grad to get a job as the figure shows 

# In[44]:


E_Y=pd.DataFrame(df_1['experience_years'].value_counts()).head(14)
E_Y['experience_level']=E_Y.index
plt.figure(figsize=[18,6]);
E_Y.index=np.arange(1,15,1)
sb.barplot(data=E_Y,x='experience_level',y='experience_years',color=blue,order=['0-1','0-2','0-3','1+','1-2','1-3','2+',
                                                                                '2-3','2-4','2-5','3+','3-5','4+','5+']);
plt.xlabel('experience years');
plt.ylabel('count');
plt.title('experience years according to its count');


# # 

# # 2) Bivariate 

# # 

# ### What are the most profitable jobs?
# ###### - sports jobs have the highest minimum salary then manegment then business-related
# ###### - training jobs have the highest maximum salary then education-related then business-related

# In[45]:


plt.figure(figsize=[8,8]);
result = final_df.groupby(["job_category"])['salary_minimum'].aggregate(np.mean).reset_index().sort_values('salary_minimum',ascending=False);
result=result.head(35)
sb.barplot(y='job_category',x="salary_minimum", data=final_df, order=result['job_category'],color=blue);
plt.title('job categories according to salary minimum');
plt.ylabel('job category');
plt.xlabel('salary minimum');


# In[46]:


plt.figure(figsize=[8,8]);
result = final_df.groupby(["job_category"])['salary_maximum'].aggregate(np.mean).reset_index().sort_values('salary_maximum',ascending=False);
result=result.head(35)
sb.barplot(y='job_category',x="salary_maximum", data=final_df, order=result['job_category'],color=blue);
plt.title('job categories according to salary maximum');
plt.ylabel('job category');
plt.xlabel('salary maximum');


# # 

# ### Describe the difference in salaries for different career levels 
# 
# ###### salaries are increasing exponentially 

# In[47]:


plt.figure(figsize=[16,8]);
result = final_df.groupby(["career_level"])['salary_minimum'].aggregate(np.mean).reset_index().sort_values('salary_minimum',ascending=True);
sb.barplot(x='career_level',y="salary_minimum", data=final_df, order=result['career_level'],color=blue);
plt.title('career level according to salary minimum');
plt.xlabel('career level');
plt.ylabel('salary minimum');


# # 

# ### What are the most profitable job industries?
# 
# ###### security and surveillance industry has the highest minimum salary then waste management the plastic
# ###### plastic has the highest maximum salary then  security and surveillance then business supplies and equipment

# In[48]:


plt.figure(figsize=[8,8])
result = final_df.groupby(["job_industry"])['salary_minimum'].aggregate(np.mean).reset_index().sort_values('salary_minimum',ascending=False);
result=result.head(35)
sb.barplot(y='job_industry',x="salary_minimum", data=final_df, order=result['job_industry'],color=blue);
plt.title('job industries according to salary minimum');
plt.ylabel('job industry');
plt.xlabel('salary minimum');


# In[49]:


plt.figure(figsize=[8,8])
result = final_df.groupby(["job_industry"])['salary_maximum'].aggregate(np.mean).reset_index().sort_values('salary_maximum',ascending=False);
result=result.head(35)
sb.barplot(y='job_industry',x="salary_maximum", data=final_df, order=result['job_industry'],color=blue);
plt.title('job industries according to salary maximum');
plt.ylabel('job industry');
plt.xlabel('salary maximum');


# # 

# ### If I'm a company that wants to post a job, which month can I post? 
# 
# ###### I recommend posting in September but if you have to post it quickly just don't post it on may 

# In[50]:


plt.figure(figsize=[16,8]);
sb.pointplot(data=df_1,x='month',y='views');
plt.title('views according to months');


# In[51]:


fig = px.histogram(final_df, x="job_category",y="salary_maximum").update_xaxes(categoryorder="total descending")
fig.show()


# # 

# In[52]:


final_df


# # Thank you!

# In[53]:


get_ipython().system('jupyter nbconvert WUZZUF-Slide-Show.ipynb --to slides --post serve  --no-input --no-prompt')


# In[ ]:




