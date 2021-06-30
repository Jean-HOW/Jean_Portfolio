#!/usr/bin/env python
# coding: utf-8

# <div style="text-align: center">
#     <h3>Analysis of Early Vaccination Rate and<br>
#         Gross domestic product per Capita<br>
#         in ASEAN Population</h3>
# </div>
# <p style="text-align: center">
#     How Jia Jean<br>
#     <i>1st April 2021</i>
# </p>   _______________________________________________________________________________________________________________________________

# # Introduction

# The report is aimed to study the relationship between the population, GDP, vaccination rate in South-East Asian countries. There are three dataset provided which are '2019-GDP.csv', '2020-Population.csv', and 'Vaccinations.csv'. Firstly, each datasets will gone through data wrangling process. 
# 
# Steps:
# 1. Vaccination Dataset
# 2. Population Dataset
# 3. GDP Dataset
# 4. Merge Vaccination, Population, and GDP into a table
# 5. Discussion
# 6. References

# ## Import libraries and datasets

# In[33]:


# lIBRARIES
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt


# In[34]:


# IMPORT DATASET
gdp = pd.read_csv("data/2019-GDP.csv",header=4,skip_blank_lines=True)
pop = pd.read_csv("data/2020-Population.csv",header=12,skip_blank_lines=True)
vac = pd.read_csv("data/Vaccinations.csv",header=0,skip_blank_lines=True)


# # Data Wrangling

# ## 1. Vaccination Dataset

# In[35]:


vac.shape


# In[36]:


vac.head()


# In[37]:


vac.tail()


# In[41]:


vac.info()


# In[38]:


vac.describe()


# In[10]:


vac


# ### 1.1 Filter columns: 'country', 'people_fully_vaccinated', 'daily_vaccinations', 'vaccines'

# In[42]:


vac_country = vac[['country','people_fully_vaccinated','daily_vaccinations','vaccines']]


# In[43]:


vac_country


# ### 1.2 Concatenate the rows of values within each columns from the same country by summing the population

# In[44]:


fun ={'people_fully_vaccinated':'sum','daily_vaccinations':'sum'}


# In[45]:


vaccination = vac_country.groupby(['country','vaccines']).agg(fun).rename(
    {"people_fully_vaccinated":"People fully vaccinated",
     "daily_vaccinations":"Total vaccinations"},
axis=1,).reset_index()


# In[46]:


vaccination


# ### 1.3 Filter South East Asian (SEA) Countries

# SEA countries including Singapore, Indonesia, Cambodia, and Myanmar which are present in the *vaccinations.csv* dataset. Therefore, only four countries listed below.

# In[47]:


countries = ['Singapore','Indonesia','Cambodia','Myanmar']
filt = vaccination['country'].isin(countries)
vaccination_SEA =  vaccination[filt].sort_values('country', ascending=True).reset_index().drop(['index'],axis=1)


# In[48]:


vaccination_SEA


# ## 2. Population Dataset

# In[49]:


pop.shape


# In[50]:


pop.head()


# In[51]:


pop.tail()


# In[52]:


pop.info()


# ### 2.1 Filter Subregion: South-Easthern Asia

# South-Easthern Asia countries begin at index 136 to 146 (11 countries). Index 147 is a SDG region not a country thus it is not within the range.

# In[53]:


pop.loc[pop['Type'] == 'Subregion']


# The countries within the index range from 136 to 146 is selected and sorted by alphabetical order.

# In[54]:


country = pop.loc[136:146].rename({'Region, subregion, country or area *':'country'},axis=1).sort_values('country', ascending=True).reset_index()


# In[55]:


country


# ### 2.2 Filter population in 2019

# Due to the fact that the *2019-GDP.csv* dataset was collected in 2019, the populaton in 2019 within the *2020-Populations.csv* is selected for this analysis.

# In[56]:


country_2019 = country[['2019']].rename({'2019':'Population(2019)'},axis=1)


# The population data are formated with spaces. Thus, the spaces needed to be removed and then converted from a string to integer.

# In[57]:


country_2019['Population(2019)'] = pd.to_numeric(country_2019['Population(2019)'].replace(' ','',regex=True), errors = 'ignore')


# In[59]:


country_2019


# ## 3. GDP Dataset

# In[60]:


gdp.shape


# In[61]:


gdp.head()


# In[62]:


gdp.tail()


# In[63]:


gdp.info()


# ### 3.1 Assign names to the columns

# In[64]:


gdp = gdp[['Unnamed: 3','Unnamed: 4']].rename({'Unnamed: 3':'country',
                                               'Unnamed: 4':'GDP'},axis=1)


# In[65]:


gdp


# ### 3.2 Filter the SEA countries

# The SEA countries are sorted in alphabetical order and the GDP values are re-formated by removing the ',' symbol.

# In[66]:


countries = ['Malaysia','Singapore','Lao PDR','Philippines','Vietnam','Brunei Darussalam','Indonesia','Cambodia','Timor-Leste','Myanmar','Thailand']
filt = gdp['country'].isin(countries)
df_gdp = gdp[filt].sort_values('country', ascending=True).reset_index().drop(['index'],axis=1)


# In[67]:


df_gdp['GDP'].replace(',','',regex=True)


# The GDP data was then converted from string into numerical format.

# In[68]:


df_gdp['GDP'] = pd.to_numeric(df_gdp['GDP'].replace(',','',regex=True), errors='ignore')


# In[69]:


df_gdp


# 
# ## 4. Merge Tables: GDP, Vaccination, Population

# In[70]:


merge_population = df_gdp.join(country_2019)


# The GDP in *population.csv* was recorded in $10^{6}$ (millions) of US dollar, where as the total population was recorded in $10^{3}$ (thousand) of population.

# In[71]:


merge_population['GDP'] = (10**6)*merge_population['GDP']


# In[72]:


merge_population['Population(2019)'] = (10**3)*merge_population['Population(2019)']


# In[73]:


merge_population


# ### 4.1 Mutate perCapitaGDP column

# In[74]:


population_GDP = merge_population.assign(perCapitaGDP=lambda x: x['GDP']/x['Population(2019)'])


# In[75]:


population_GDP


# ### 4.2 Merge vaccination dataset to population and GDP datasets

# In[76]:


merge_population


# In[77]:


pop_vac_SEA = population_GDP.merge(vaccination_SEA,how='left')


# In[78]:


pop_vac_SEA 


# ## Discussion

# ### Estimation of vaccinated population number for each vaccine type in South East Asian population

# In[79]:


vaccines = pop_vac_SEA.groupby('vaccines').agg({'Total vaccinations':'sum'}).reset_index()


# In[80]:


vaccines = vaccines[['vaccines','Total vaccinations',]]


# In[81]:


vaccines['log(Total vaccinations)'] = np.log(vaccines['Total vaccinations'])


# In[82]:


vaccines


# In[83]:


plot_vac = plt.bar(vaccines['vaccines'],vaccines['Total vaccinations'])
plt.title("Estimate vaccinations in South East Asia Population")
plt.xlabel("Vaccine Type")
plt.ylabel("Total Vaccinated Population")
plt.xticks(rotation=45)


# In[84]:


plot_vac = plt.bar(vaccines['vaccines'],vaccines['log(Total vaccinations)'])
plt.title("Estimate vaccinations in South East Asia Population")
plt.xlabel("Vaccine Type")
plt.ylabel("Total Vaccinated Population(Log10)")
plt.xticks(rotation=45)


# #### Statistical Description

# Assume that the vaccine will be equally distributed to the country's population, the population of total vaccination in SEA are distributed across 4 types of vaccines which are Oxford-AstraZeneca, Pfizer-BioNTech, Sinopharm and Sinovac from Beijing. Owing to the fact that the total vaccinated population shows a signficant difference between each type of vaccines. Thus, logarithmic scale of base 10 is applied to fix this issue.
# 
# Based on the estimate total vaccinations graph, Sinovac is the most widely used within the SEA population. However, there are only four countries that have received the vaccines into their country. This includes Cambodia, Indonesia, Myanmar, and Singapore. Besides, there are missing data from others countries regarding to the type of vaccine used and data of daily vaccination. This has led to significant bias on representing the type of vaccine used across SEA countries. Although Sinovac shows the highest total vaccination simply due to the high population of approximately 270626 thousand people in Indonesia compared to other countries. 
# 
# According to Ong (2021), Malaysia will only receive the first batch of 1 million vaccines only on February 26, when other countries such as Singapore and Indonesia have already launched their vaccination drives in January.This causes the missing data of vaccination in Malaysian population.

# In[85]:


countries = ['Singapore','Indonesia','Cambodia','Myanmar']
filt = pop_vac_SEA['country'].isin(countries)
capGDP_totVAC =  pop_vac_SEA[filt].sort_values('country', ascending=True).reset_index().drop(['index'],axis=1)


# In[86]:


GDP_VAC = capGDP_totVAC[['vaccines','perCapitaGDP','Total vaccinations']]


# In[87]:


plot_scatter = GDP_VAC.plot.scatter(x='perCapitaGDP',
                                    y='Total vaccinations')
plt.title("Scatter plot of Total vaccinations against per capita GDP")


# In[88]:


GDP_VAC


# There is no correlation between per capita GDP and total vaccination as shown above. Country with high per capita GDP could have low number of total vaccination, or vice versa. However, the per capita GDP value has effect on the choice of vaccine used as higher per capita GDP country tend to use Pfizer-BioNtech which has must higher cost ($20 per dose) compared to other 3 vaccines choices (Binding *et al.* 2021).

# ### Comparison between the number of  total vaccinations, popuplation, and fully vaccinated in South East Asia Countries' Population

# In[89]:


vac_country = pop_vac_SEA[['country','Population(2019)','Total vaccinations','People fully vaccinated']]


# In[91]:


vac_country


# In[92]:


numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
for c in [c for c in vac_country.columns if vac_country[c].dtype in numerics]:
    vac_country[c] = np.log(vac_country[c])


# In[93]:


vac_country_log = vac_country.set_index('country')


# In[94]:


vac_country_log


# In[95]:


plot_country = vac_country_log.plot(kind='bar')
plt.title("Vaccinations in South East Asia Countries' Population")
plt.xlabel("Countries")
plt.ylabel("Log(Vaccinated Population)")
plt.xticks(rotation=50)
plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')


# #### Statistical Description

# Indonesia with the population of 270626 thousand people in the year 2019 ranked the highest amongst South East Asian (SEA) countries. Philippines is the second largest population of 108117 thousand people, whereas Brunei Darussalam's population of 433 thousand people ranked the lowest among others SEA countries' population. 
# 
# There are only four countries have introduced the vaccine including Cambodia, Indonesia, Myanmar, and Singapore. Indonesia shows the highest total vaccination's population of 2022788 people. Singapore being the second highest total vaccination of 329630 people, followed by Myanmar with a total vaccination of 82823 people and Cambodia shows the lowest total vaccination among the four countries. 
# 
# People who was vaccinated 2 weeks after their second dose in a 2-dose series, such as the Pfizer or Moderna vaccines, or 2 weeks after a single-dose vaccine, such as Johnson & Johnson's Janssen vaccine are considered fully vaccinated (CDC 2021). This indicates that the people fully vaccinated in Singapore are slightly lesser than the total vaccinations as there are some people have not fulfill the 2 weeks criterion. 
# 
# There is a limitation for using population dataset as it was collected in year 2019, whilst the vaccinated population dataset was collected in year 2021. The countries population should have increased over time, thus the graph shows only the estimate population size of SEA countries instead of the actual population size in 2021.
# 
# The graph is represented with logarithmic scale of base 10 owing to the fact that some countries' population are significantly smaller than others like Brunei. Thus, logarithmic scale graph able to display numerical data over a very wide range of values in a compact way, while difference in population between countries can still be intepreted.

# In[96]:


pop_vac_SEA 


# ### Daily vaccination and total vaccination in Singapore from January to February 2021 

# In[97]:


vac


# In[98]:


vac_date = vac[['country','date','people_fully_vaccinated','daily_vaccinations']]


# In[99]:


vac_date


# In[100]:


SG = ['Singapore']
filt_country = vac['country'].isin(SG)
vac_SG = vac_date[filt_country].reset_index(drop=True, inplace=False)


# In[101]:


vac_SG['days'] = np.arange(len(vac_SG))


# In[102]:


vac_SG


# In[103]:


vac_SG['daily_vaccinations'] = vac_SG['daily_vaccinations'].fillna(0)
vac_SG['Total_vaccinations'] = vac_SG['daily_vaccinations'].fillna(0).cumsum()


# In[104]:


vac_SG


# ### Daily vaccination over time

# In[105]:


vac_SG.plot.line(x='days', y='daily_vaccinations')
plt.title("Population fo Daily Vaccination in Singapore")
plt.xlabel("Time (Days)")
plt.ylabel("Daily vaccinations")


# ### Total vaccination over time

# In[106]:


vac_SG.plot.line(x='days', y='Total_vaccinations')
plt.title("Population fo Total Vaccination in Singapore")
plt.xlabel("Time (Days)")
plt.ylabel("Total vaccinations")


# #### Statistical Description

# According to the Singaporean's daily vaccination over time graph, the population number shows 3 occurence of inconsistent rise and fall. On day 1, the vaccinated population increaseas from 2800 people to 4090 people on day 2. The second occurence was between day 11 and 18, the vaccinated population has raised from 5380 to 10579 people. There was a slight drop on day 27 from  10404 to 9889 people and elevated back to 10411 people on day 32. The daily vaccination graph shows an overall increasing trend over time in the Singapore's population. 
# 
# On the contrary, the total vaccination over time graph shows a consistent increasing linear regression model. This indicates that the population of vaccinated individuals in Singapore has increased from 2800 people and reaches a total of 329630 people vaccinated on the 38th day.
# 
# There are several factors that might give rise to the inconsistency of daily vaccination in Singapore population. According to the Gorvenment of Singapore, the first batch of vaccine from Pfizer-BioNTech was given to individuals at high risk of being infected by COVID-19, including healthcare and frontline workers (gov.sg 2020). 
# 
# Secondly, individuals who are most vulnerable to severe disease and complications if they fall ill with COVID-19 including the elderly and persons with medical comorbidities who experiencing with 2 or more illnesses or diseases simultaneously are given the priority as well  (gov.sg 2020). The differences in number of people per batch resulted in the inconsisntent rise and fall in the daily vaccination.

# ### Does higher per capita GDP mean that the country gets vaccines faster and progresses in the vaccination faster?

# In[110]:


pop_vac_SEA 


# High per capita GDP does not entirely correlated to the vaccination progression of a country. For example, Brunei Darussalam ranked the second highest per capita GDP of 31106.24 USD but the country has just announced that vaccination strategy will be implemented once the vaccine arrives in the country. However, Brunei’s citizens and residents, including foreign nationals with a valid IC, will receive the COVID-19 vaccination for free. This strategy does accelerate the progression of vaccination as more people are accessible to vaccine (The Star 2021). 

# ### Which vaccines are being used by poorer countries?

# Cambodia and Myanmar show per capita GDP of 1643.05 USD and 1407.83 USD respectively. Sinopharm vaccine from Beijing is used by Cambodia, whereas Myanmar uses Oxford vaccine from AstraZeneca.

# ### Will Japan meet its vaccination target fast enough for them to safely host the Olympics?

# I think Japan is facing difficulties to achieve its vaccination target. There are approximately 80 percent of people in Japan want the Games to be cancelled or rescheduled. Besides, holding the Tokyo Games behind closed doors would loss 381.3 billion yen in spending related directly to the games, or 90 percent of the original projection for the events estimated by Katsuhiro Miyamoto (Obo K and Ghani F 2021).
# 
# This will stimulates the household consumption expenditures are halve to 280.8 billion yen and corporate marketing activities will be dampened. Moreover, economic gains from promotional sporting and cultural events after the games will also be reduced by half to 851.4 billion yen (Obo K and Ghani F 2021).

# ### What happens when you apply the latest data? You can keep on updating this and start a channel on #Slack to continue discussing it.

# If the latest data is utilized in this study, there will be more countries received the vaccines and also more varieties in vaccines used shown in the tables and graphs.

# ## References

# A Singapore Government Agency Website (gov.sg) (2020) *What you should know about the COVID-19 vaccine*, accessed 26 March 2021, https://www.gov.sg/article/what-you-should-know-about-the-covid-19-vaccine
# 
# Binding L, Culbertson A and Phillips A (2021) *COVID-19 vaccines: How do the Moderna, Pfizer and Oxford coronavirus jab candidates compare?*, Sky news, accessed 25 March 2-21, https://news.sky.com/story/covid-19-vaccines-how-do-the-moderna-and-pfizer-coronavirus-jab-candidates-compare-12134062
# 
# Centres for Disease Control and Prevention (CDC) (2021) *When You’ve Been Fully Vaccinated*, accessed 25 March 2021, https://www.cdc.gov/coronavirus/2019-ncov/vaccines/fully-vaccinated.html#:~:text=Have%20You%20Been%20Fully%20Vaccinated,as%20Johnson%20%26%20Johnson%27s%20Janssen%20vaccine
# 
# Obo K and Ghani F (2021) *Tokyo Olympic Games will not happen 'without spectators'*, Aljazeera, accessed 26 March 2021, https://www.dw.com/en/coronavirus-japan-confident-it-can-overcome-hurdles-to-host-olympics/a-56438080
# 
# The Star (2021) *Five Covid-19 vaccine candidates for Brunei announced*, accessed 26 March 2021, https://www.thestar.com.my/aseanplus/aseanplus-news/2021/03/12/five-covid-19-vaccine-candidates-for-brunei-announced

# Ong J (2021) *Fitch unit slashes Malaysia’s 2021 GDP forecast by half due to runaway Covid-19 cases, MCO*, Malaymaill, accessed 27 March 2021, https://www.malaymail.com/news/malaysia/2021/02/15/fitch-unit-slashes-malaysias-2021-gdp-forecast-by-half-due-to-runaway-covid/1949827
