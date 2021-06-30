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

# lIBRARIES
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

# IMPORT DATASET
gdp = pd.read_csv("data/2019-GDP.csv",header=4,skip_blank_lines=True)
pop = pd.read_csv("data/2020-Population.csv",header=12,skip_blank_lines=True)
vac = pd.read_csv("data/Vaccinations.csv",header=0,skip_blank_lines=True)

# # Data Wrangling

# ## 1. Vaccination Dataset

vac.shape
vac.head()
vac.tail()
vac.info()
vac.describe()
vac

# ### 1.1 Filter columns: 'country', 'people_fully_vaccinated', 'daily_vaccinations', 'vaccines'

vac_country = vac[['country','people_fully_vaccinated','daily_vaccinations','vaccines']]

vac_country

# ### 1.2 Concatenate the rows of values within each columns from the same country by summing the population

fun ={'people_fully_vaccinated':'sum','daily_vaccinations':'sum'}

vaccination = vac_country.groupby(['country','vaccines']).agg(fun).rename(
    {"people_fully_vaccinated":"People fully vaccinated",
     "daily_vaccinations":"Total vaccinations"},
axis=1,).reset_index()

vaccination

# ### 1.3 Filter South East Asian (SEA) Countries

# SEA countries including Singapore, Indonesia, Cambodia, and Myanmar which are present in the *vaccinations.csv* dataset. Therefore, only four countries listed below.

countries = ['Singapore','Indonesia','Cambodia','Myanmar']
filt = vaccination['country'].isin(countries)
vaccination_SEA =  vaccination[filt].sort_values('country', ascending=True).reset_index().drop(['index'],axis=1)

vaccination_SEA

# ## 2. Population Dataset

pop.shape
pop.head()
pop.tail()
pop.info()

# ### 2.1 Filter Subregion: South-Easthern Asia

# South-Easthern Asia countries begin at index 136 to 146 (11 countries). Index 147 is a SDG region not a country thus it is not within the range.

pop.loc[pop['Type'] == 'Subregion']

# The countries within the index range from 136 to 146 is selected and sorted by alphabetical order.

country = pop.loc[136:146].rename({'Region, subregion, country or area *':'country'},axis=1).sort_values('country', ascending=True).reset_index()

country

# ### 2.2 Filter population in 2019

# Due to the fact that the *2019-GDP.csv* dataset was collected in 2019, the populaton in 2019 within the *2020-Populations.csv* is selected for this analysis.

country_2019 = country[['2019']].rename({'2019':'Population(2019)'},axis=1)

# The population data are formated with spaces. Thus, the spaces needed to be removed and then converted from a string to integer.

country_2019['Population(2019)'] = pd.to_numeric(country_2019['Population(2019)'].replace(' ','',regex=True), errors = 'ignore')

country_2019

# ## 3. GDP Dataset

gdp.shape
gdp.head()
gdp.tail()
gdp.info()

# ### 3.1 Assign names to the columns

gdp = gdp[['Unnamed: 3','Unnamed: 4']].rename({'Unnamed: 3':'country',
                                               'Unnamed: 4':'GDP'},axis=1)

gdp

# ### 3.2 Filter the SEA countries

# The SEA countries are sorted in alphabetical order and the GDP values are re-formated by removing the ',' symbol.

countries = ['Malaysia','Singapore','Lao PDR','Philippines','Vietnam','Brunei Darussalam','Indonesia','Cambodia','Timor-Leste','Myanmar','Thailand']
filt = gdp['country'].isin(countries)
df_gdp = gdp[filt].sort_values('country', ascending=True).reset_index().drop(['index'],axis=1)

df_gdp['GDP'].replace(',','',regex=True)

# The GDP data was then converted from string into numerical format.

df_gdp['GDP'] = pd.to_numeric(df_gdp['GDP'].replace(',','',regex=True), errors='ignore')
df_gdp

# ## 4. Merge Tables: GDP, Vaccination, Population

merge_population = df_gdp.join(country_2019)

# The GDP in *population.csv* was recorded in $10^{6}$ (millions) of US dollar, where as the total population was recorded in $10^{3}$ (thousand) of population.

merge_population['GDP'] = (10**6)*merge_population['GDP']

merge_population['Population(2019)'] = (10**3)*merge_population['Population(2019)']

merge_population

# ### 4.1 Mutate perCapitaGDP column

population_GDP = merge_population.assign(perCapitaGDP=lambda x: x['GDP']/x['Population(2019)'])

population_GDP

# ### 4.2 Merge vaccination dataset to population and GDP datasets

merge_population

pop_vac_SEA = population_GDP.merge(vaccination_SEA,how='left')

pop_vac_SEA 

# ## Discussion

# ### Estimation of vaccinated population number for each vaccine type in South East Asian population

vaccines = pop_vac_SEA.groupby('vaccines').agg({'Total vaccinations':'sum'}).reset_index()

vaccines = vaccines[['vaccines','Total vaccinations',]]

vaccines['log(Total vaccinations)'] = np.log(vaccines['Total vaccinations'])

vaccines

# BARGRAPH: Estimate vaccinations in South East Asia Population 
plot_vac = plt.bar(vaccines['vaccines'],vaccines['Total vaccinations'])
plt.title("Estimate vaccinations in South East Asia Population")
plt.xlabel("Vaccine Type")
plt.ylabel("Total Vaccinated Population")
plt.xticks(rotation=45)

# BARGRAPH: Estimate vaccinations in South East Asia Population (LOG10)
plot_vac = plt.bar(vaccines['vaccines'],vaccines['log(Total vaccinations)'])
plt.title("Estimate vaccinations in South East Asia Population")
plt.xlabel("Vaccine Type")
plt.ylabel("Total Vaccinated Population(Log10)")
plt.xticks(rotation=45)


# SCATTER PLOT: Total vaccinations against per capita GDP
countries = ['Singapore','Indonesia','Cambodia','Myanmar']
filt = pop_vac_SEA['country'].isin(countries)
capGDP_totVAC =  pop_vac_SEA[filt].sort_values('country', ascending=True).reset_index().drop(['index'],axis=1)


GDP_VAC = capGDP_totVAC[['vaccines','perCapitaGDP','Total vaccinations']]

plot_scatter = GDP_VAC.plot.scatter(x='perCapitaGDP',
                                    y='Total vaccinations')
plt.title("Scatter plot of Total vaccinations against per capita GDP")

GDP_VAC

# ### Comparison between the number of  total vaccinations, popuplation, and fully vaccinated in South East Asia Countries' Population

vac_country = pop_vac_SEA[['country','Population(2019)','Total vaccinations','People fully vaccinated']]

vac_country

numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
for c in [c for c in vac_country.columns if vac_country[c].dtype in numerics]:
    vac_country[c] = np.log(vac_country[c])

vac_country_log = vac_country.set_index('country')

vac_country_log

plot_country = vac_country_log.plot(kind='bar')
plt.title("Vaccinations in South East Asia Countries' Population")
plt.xlabel("Countries")
plt.ylabel("Log(Vaccinated Population)")
plt.xticks(rotation=50)
plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')

pop_vac_SEA 


# ### Daily vaccination and total vaccination in Singapore from January to February 2021 

vac
vac_date = vac[['country','date','people_fully_vaccinated','daily_vaccinations']]
vac_date

SG = ['Singapore']
filt_country = vac['country'].isin(SG)
vac_SG = vac_date[filt_country].reset_index(drop=True, inplace=False)
vac_SG['days'] = np.arange(len(vac_SG))

vac_SG

vac_SG['daily_vaccinations'] = vac_SG['daily_vaccinations'].fillna(0)
vac_SG['Total_vaccinations'] = vac_SG['daily_vaccinations'].fillna(0).cumsum()

vac_SG


# #### LINE GRAPH: Daily vaccination over time

vac_SG.plot.line(x='days', y='daily_vaccinations')
plt.title("Population fo Daily Vaccination in Singapore")
plt.xlabel("Time (Days)")
plt.ylabel("Daily vaccinations")


# #### LINE GRAPH: Total vaccination over time

vac_SG.plot.line(x='days', y='Total_vaccinations')
plt.title("Population fo Total Vaccination in Singapore")
plt.xlabel("Time (Days)")
plt.ylabel("Total vaccinations")

pop_vac_SEA 

