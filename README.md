# ECE143_Project15: Analysis on Causes of Death in the United States 

## Problem:  
Analyzing the overall life expectancy based on the gender, age and disease across 51 states in the United States


## Motivation: 
Mortality is one of healthcare outcome measurements. If we combine the mortality with causes of death, it could be used to evaluate how disease/non-disease affect our life expectancy. 
World health organization (WHO) and the United States centers for disease control and prevention (CDC) make the statistics data public every year. Understanding these data remains a major challenge. To solve this problem, we decided to build up the mortality ranking system, integrate the mortality with causes of death, and visualize them. It helps us to choose the good life style in the future. 

## Dataset:  
World health rankings website: [here](https://www.worldlifeexpectancy.com/usa-cause-of-death-by-age-and-gender)
The entire data are from the public website (shown as above), which contain the death rate, the causes of disease, gender, and the age for different states in the US. 
The house-hould income for 51 states in the United States in 2017, from [here]()

## Methodology:  
### Packages:  
#### 1. Pandas
* Official website: [here]
* Installation
    The best way to get pandas is via conda:
    `conda install pandas`
    OR
    `pip install pandas`

#### 2. Sqlite
* Official website: [here]


#### 3. Numpy
* Official website: [here]


#### 4. Bokeh
* Official website: [here]
* Installation
The best way to get bokeh is via conda:
`conda install bokeh`
OR
`pip install bokeh`


#### 5. Holoviews
* Official website: [here]
* Installation
  `pip install holoviews`
  OR
  `conda install -c pyviz/label/dev holoviews`



#### 6. Plotly
* Official website: [here]



#### 7. Matplotlib
* Official website: [here]
* Installation
  `python -m pip install -U pip`
  `python -m pip install -U matplotlib`



#### 8. Seaborn
* Official website: [here]
*	Installation
  The best way to get bokeh is via conda:
  `conda install seaborn`
  OR
  `pip install seaborn`


## The plan: 
Our proposed solution is to use a python package (BeautifulSoup) to extract data from the websites (shown above) and build up the overall health ranking system  and house-hould income across 51 states. Firstly, we organize the data according to gender, ages, and states.  Then we are going to visualize the data by showing the number of deaths vs. different causes.
Our system can provide health advice to people who input their location, age, and gender.

## File Details:
**demo.ipynb**: demonstrate all visualization figures and plots.  
**plot_demo.py**: functions used for general plots.  
**plot_map_income.py**: functions used for plotting US map and correlation between death rate and household income.  
**plot_cancer.py**: functions used for plotting one certain cause of death-cancer.  
**plot_CA.py**: functions used for plotting one certain state analysis - California.  

**All .csv data files is in the data folder **
