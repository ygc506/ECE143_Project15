# ECE143_Project (Group 15): Analysis on Causes of Death in the United States 

## Problem
Analyzing the overall life expectancy based on the gender, age and disease across 51 states in the United States


## Motivation
Mortality is one of healthcare outcome measurements. If we combine the mortality with causes of death, it could be used to evaluate how disease/non-disease affect our life expectancy. 
World health organization (WHO) and the United States centers for disease control and prevention (CDC) make the statistics data public every year. Understanding these data remains a major challenge. To solve this problem, we decided to build up the mortality ranking system, integrate the mortality with causes of death, and visualize them. It helps us to choose the good life style in the future. 

## Conclusions
| Death rate highest on|    Cause of death |
| :--------|                : --------| 
| Child |  Birth Trauma, Low Birth Weight |  
| Middle age |   Drug Use, Homicide, AIDS, Poisoning, Hepatitis | 
| Elderly             |  Most | 
| No correlation |  Drownings, Road Traffic Accidents, Suicide |
In 2017, 
- The top one leading cause of death is coronary heart disease in the US. 
- There is the negative correlation between the overall death rate and median household income for the states.
 Specifically, the states around central east areas have higher mortality than those from other areas.
The median household income for the states in central east areas are relatively lower than that for other states. 
- For most cause of deaths, the older, the higher death rate.

| Death rate highest on|    Cause of death |
| :--------|                : --------| 
| Child |  Birth Trauma, Low Birth Weight |  
| Middle age |   Drug Use, Homicide, AIDS, Poisoning, Hepatitis | 
| Elderly             |  Most | 
| No correlation |  Drownings, Road Traffic Accidents, Suicide |

- Some causes of death are related to gender

| Male-related | Female-related|
| :--------     |   : --------| 
|Suicide Road, Road Traffic Accidents, Prostate Cancer, Poisonings| Stroke, Breast Cancer,  Alzheimer's, Uterine Cancer, Ovary Cancer|

- Cancer as one of main cause of deaths, there is no big difference in cancer death rate between male and female at all ages. 
- For people between 15 and 34 in California, they should care more about Road Traffic Safety and Mental Conditions.

## Data sources
- **World health rankings website**, from [here](https://www.worldlifeexpectancy.com/usa-cause-of-death-by-age-and-gender)
The main data are from the public website (shown as above), which contain the death rate, the causes of disease, gender, and the age for different states in the US. 
- **The household income for 51 states in the United States in 2017**, from [here](https://www2.census.gov/programs-surveys/cps/tables/time-series/historical-income-households/h08.xls)

## Methodology 
### Collecting and process data
Our proposed solution is to use BeautifulSoup to extract data from the websites (shown above). Then we use pandas, numpy to clean and organize data. Calculating death rate. Making it easy to access.
### Health System
We build a health ranking system using Flask. Our system can provide health advice to people who input their location, age, and gender.
### Analysis and visualization
Firstly, we reorganize the data based on the variables (ex. gender, ages, and states). Then we select a portion of dimension in data to visualize the data using tools including matplotlib, seaborn, bokeh and plotly to answer the following questions:
- Which are top 10 leading causes of death in the US? 
- Which states have the highest and lowest mortality in the US?
- Is there any correlation between household income state and overall death rate?
- What are the age-related cause of death in the US?
- What are the gender-related cause of death in the US?
- How different is the cancer death rate between male and female?
- How different is the cancer death rate among different age groups?
- Case study: how different is overall death rate between male and female in california?
              how different is overall death rate among different age groups in california?
              


## File Structure
```
Root
|
+----data                       Saved data 
|   | state_population_ages_all_wo_us.csv
|   |                           Death data in the US, 2017 including sum of all ages                    
|   |
|   | state_population_ages_wo_us.csv
|   |                           Death data in the US, 2017 without sum of all ages
|   |           
|   | h08.csv                   US income data
|   | population.xlsx           Scraped population raw data
|   +----states                 A folder containing scraped US death raw data
|
+----img
|   | healthsystem.gif          gif used in readme
|
+----HealthSystem               A web application for searching data
|       |   HealthSystem.py     The main function
|       +----templates          Web Page templates to render
|           |   index.html
|           |   result.html
|
|    Data_crawler.py            Crawling data from web
|    Merge_data.py              Organize crawled data and save to a file
|    Presentation slides.pdf  
|    demo.ipynb                 Shows all visualization for presentation
|    plot_CA.py                 Plot code for California section
|    plot_cancer.py             Plot code for cancer section
|    plot_demo.py               Plot code for gender section
|    plot_map_income.py         Plot code for US death and income correlation section
|    README.md
```
### Files Details
**demo.ipynb**: demonstrate all visualization figures and plots.  
                combinations of the use of functions provided in the below .py files
**plot_demo.py**: functions used for general plots.  
**plot_map_income.py**: functions used for plotting US map and correlation between death rate and household income.  
**plot_cancer.py**: functions used for plotting one certain cause of death-cancer.  
**plot_CA.py**: functions used for plotting one certain state analysis - California.  

**All .csv data files are in the `data` folder **
## Instructions on running the code
### Required packages 
make sure to install below packages to process the data and generate the plots
**Python version**: `3.6.8`
#### 1. [Scientific Python distributions](https://www.scipy.org/install.html)
* Installation 
``` bash
$ python -m pip install --user numpy scipy matplotlib ipython jupyter pandas sympy nose
```
**This includes modules we are using:**
##### [Pandas](https://pandas.pydata.org/)
##### [Matplotlib](https://matplotlib.org/)
##### [Numpy](https://www.numpy.org/)
##### [Jupyter Notebook](https://jupyter.org/)
#### 2. [SQLite](https://docs.python.org/3.6/library/sqlite3.html)
* SQLite comes in Python Standard Library
#### 3. [Bokeh](https://bokeh.pydata.org/en/latest/)
* Installation
The best way to get bokeh is via conda:
``` bash
$ conda install bokeh
```
OR
``` bash
$ pip install bokeh
```
#### 4. [Plotly](https://plot.ly/python/)
* Installation
``` bash
$ pip install plotly
```
#### 5. [seaborn](https://seaborn.pydata.org/)
* Installation
The best way to get seaborn is via conda:
``` bash
$ conda install seaborn
```
OR
``` bash
$ pip install seaborn
```
#### 6. [Flask](http://flask.pocoo.org/)
* Installation
``` bash
$ pip install flask
```
#### 7. xlrd
* You may not have xlrd which is used to process Excel files
* Installation
``` bash
$ pip install xlrd
```

If it complains not having any other packages when running, just run 
``` bash
$ pip install (package name here)
```
for a quick fix.

### Run the code
#### Clone from repository
``` bash
$ git clone https://github.com/ygc506/ECE143_Project15.git
$ cd ECE143_Project15
```
#### Scraping data
This repository already have scraped data. You can skip this step and next one (Process scraped data).
But if you insist scraping yourself. Remove data that comes with clone.
``` bash
$ mv data/h08.csv ./
$ rm -r data/*
$ mv h08.csv data/
$ mkdir data/states
```
Run data crawler:
``` bash
$ python Data_crawler.py
$ rm "data/states/United States.xlsx"
```
#### Process scraped data
``` bash
$ python Merge_data.py
```
#### Run Health System
```bash
$ cd HealthSystem/
$ python HealthSystem.py
>>>  * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```
Then open a browser and go to `http://127.0.0.1:5000/`.
Press `CTRL+C` to quit. To go back:
```bash
$ cd ../
```
#### Run Jupyter Notebook
```bash
$ jupyter notebook
```
A browser window should show up. Select `demo.ipynb` then run all cells.
## Health System Demo
Input age, gender and state, then click submit. The system will find fata matching those information the user input and display the list of top five causes of death for that group of people.
![Health System Animation](https://github.com/ygc506/ECE143_Project15/blob/master/img/healthsystem.gif)
