# The Hustle around H-1B visas

![960x0](https://user-images.githubusercontent.com/77983487/117752330-2fee4d00-b1dc-11eb-9a2e-d9a36e547dfc.jpg)

This non-immigrant classification applies to people who wish to perform services in a specialty occupation, services of exceptional merit and ability relating to a Department of Defense (DOD) cooperative research and development project, or services as a fashion model of distinguished merit or ability. Prospective specialty occupation and distinguished fashion model employers/agents must obtain a certification of an LCA (Labour Condition Application) from the DOL before filing for H1-B. This application includes certain attestations, a violation of which can result in fines, bars on sponsoring nonimmigrant or immigrant petitions, and other sanctions to the employer/agent. The application requires the employer/agent to attest that it will comply with all the labor requirements for H-1B visas. The number of LCA filings can help us in approximating the number of H1-B that will be approved.

## Hypothesis 1: How has the LCA approval rate varied over the years in different industries.

H0:The overall trend of employing foreign workers in speciality occupations (for which H1B is required) has increased due to globalisation and development in the means of communication and transport.

H1:There was no change seen in employment of foreign workers.

### Result:
We observe that LCA filings have increased over the years for mostly all the service sector industries. However there has been a decrease in the LCA filings for primary sector industries like agriculture, mining and other industries such as healthcare, entertainment, educational services and food services. Thus, we reject our hypothesis and conclude that even with increased means of communication and development in the IT sector, some sectors of the economy in US still have a low proportion of speciality jobs for foreign workers.
![image](https://user-images.githubusercontent.com/77983689/117743586-aaaf6c00-b1cc-11eb-9680-c27cdebc684b.png)



## Hypothesis 2: There has been a notable change in the number of H1-B being approved based on who was there in the White House and a certain preference was given to applicants of a particular nationality.

H0: The "Obama" and the "Trump" government favored citizens from a certain nationality in approving H1-B visas based on the relations of United States with that particular nation.

H1: The government in power was not biased towards citizens from any particular nation while approving H1-B visas.

### Result:
For the period between 2009-17, the Democrats were at the Centre and lead by President Barak Obama whereas the Republicans were in power from 2017-2021, headed by President Donald Trump. We neglected the year 2020 in our analysis as this was the year affected by pandemic and is obvious to observe a decline in H1-B visas.We initially based our hypothesis on the fact that maybe the foreign policies during the Republican government might have affected the approvals of H1-B visas for the years 2017-2019 especially for countries like China( Mainland, Taiwan) , Mexico and Russia. But looking at the plots below we can reject our hypothesis, as it is clearly seen that the government in the Centre and its foreign policies does not affect the approvals of H1-B.

![image](https://user-images.githubusercontent.com/77983689/117743825-2c9f9500-b1cd-11eb-959b-1bec321ca736.png)



## Hypothesis 3: To test whether market value of an organisation has any impact on the DOL(Department of Labor) certifying the Labor Condition Applications.

H0: Market value of an organisation has an impact on the DOL(Department of Labor) certifying the Labor Condition Applications.

H1: There is no impact of market value of an organisation in certifying the Labor Condition Applications.

### Result:
From the tables below we find that even the companies with a small market capital have a higher success rate of LCA approvals compared to the companies with a higher market capital. Thus, we reject our null hypothesis which states that a company with a higher market capital which has better resources, would have a better chance at securing an LCA approval for employing a foreign worker.

![image](https://user-images.githubusercontent.com/77983689/117744050-8e5fff00-b1cd-11eb-86b0-5e9070f013de.png)

![image](https://user-images.githubusercontent.com/77983689/117744024-843e0080-b1cd-11eb-9e42-cf0e82858269.png)


All the data files used in the program can be found on the below link:
Download these files to run the code in the local with the same folder structure.
https://drive.google.com/drive/folders/1MGVg2kT_17szLGbT42BRYRGL7iDqlSX0?usp=sharing

The dataset for LCA approvals is available at the this link:
https://www.dol.gov/agencies/eta/foreign-labor/performance

The datset for companies in different sectors is available at this link:
https://www.kaggle.com/dhimananubhav/nasdaq-company-list

The dataset for Nonimmigrant Visa Issuances by Visa Class and by Nationality:
https://travel.state.gov/content/travel/en/legal/visa-law0/visa-statistics/nonimmigrant-visa-statistics.html

## References:

https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.subplot.html
https://www.python-course.eu/matplotlib_subplots.php
https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.nlargest.html
https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.legend.html#:~:text=The%20location%20of%20the%20legend,edge%20of%20the%20axes%2Ffigure.
https://stackoverflow.com/questions/47851072/plotting-a-pandas-dataframe-row-by-row
