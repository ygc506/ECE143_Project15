# ECE143_Project (Group 15): Analysis on Causes of Death in the United States 

## Problem:  
Analyzing the overall life expectancy based on the gender, age and disease across 51 states in the United States


## Motivation: 
Mortality is one of healthcare outcome measurements. If we combine the mortality with causes of death, it could be used to evaluate how disease/non-disease affect our life expectancy. 
World health organization (WHO) and the United States centers for disease control and prevention (CDC) make the statistics data public every year. Understanding these data remains a major challenge. To solve this problem, we decided to build up the mortality ranking system, integrate the mortality with causes of death, and visualize them. It helps us to choose the good life style in the future. 

## Conclusions:


## Data sources:  
* **World health rankings website**, from [here](https://www.worldlifeexpectancy.com/usa-cause-of-death-by-age-and-gender)
The main data are from the public website (shown as above), which contain the death rate, the causes of disease, gender, and the age for different states in the US. 
* **The household income for 51 states in the United States in 2017**, from [here](https://www2.census.gov/programs-surveys/cps/tables/time-series/historical-income-households/h08.xls)
## File Structure
```
Root
|
+----data                       Saved data to be used on demand 
|   | state_population_ages_all_wo_us.csv
|   |                       Death data in the US, 2017 including sum of all ages                    
|   |
|   | state_population_ages_wo_us.csv
|   |                       Death data in the US, 2017 without sum of all ages
|   |           
|   | h08.csv             US income data
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
### Files Details:
**demo.ipynb**: demonstrate all visualization figures and plots.  
                combinations of the use of functions provided in the below .py files
**plot_demo.py**: functions used for general plots.  
**plot_map_income.py**: functions used for plotting US map and correlation between death rate and household income.  
**plot_cancer.py**: functions used for plotting one certain cause of death-cancer.  
**plot_CA.py**: functions used for plotting one certain state analysis - California.  

**All .csv data files is in the `data` folder **
[Bokeh plot](https://github.com/ygc506/ECE143_Project15/blob/master/img/bokehplot.html)
## Instructions on running the code
### Required packages: 
make sure to install below packages to process the data and generate the plots
**Python version**: `3.6.8`
#### 1. Pandas
* Official website: [here](https://pandas.pydata.org/)
* Installation
    The best way to get pandas is via conda:
    `conda install pandas`
    OR
    `pip install pandas`

#### 2. SQLite
* SQLite comes in Python Standard Library
* Document [here](https://docs.python.org/3.6/library/sqlite3.html)

#### 3. Scientific Python distributions
* Official website: [here](https://www.scipy.org/install.html)
* Installation 
`python -m pip install --user numpy scipy matplotlib ipython jupyter pandas sympy nose`

#### 4. Bokeh
* Official website: [here](https://bokeh.pydata.org/en/latest/)
* Installation
The best way to get bokeh is via conda:
`conda install bokeh`
OR
`pip install bokeh`

#### 5. Plotly
* Official website: [here](https://plot.ly/python/)
* Installation
`pip install plotly`

#### 6. Matplotlib
* Official website: [here](https://matplotlib.org/)
* Installation
  `python -m pip install matplotlib`

#### 7. seaborn
* Official website: [here](https://seaborn.pydata.org/)
* Installation
  The best way to get bokeh is via conda:
  `conda install seaborn`
  OR
  `pip install seaborn`

#### 8. Flask
* Official website: [here](http://flask.pocoo.org/)
* Installation
`pip install Flask`

#### 9. xlrd
* You may not have xlrd to process Excel files
* Installation
`pip install xlrd`

If it complains not having any other packages when running. Just run `pip install (package name here)` for a quick fix.

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
Run Jupyter Notebook
```bash
$ jupyter notebook
```
A browser window should show up. Select `demo.ipynb`
## The plan: 
Our proposed solution is to use a python package (BeautifulSoup) to extract data from the websites (shown above) and build up the overall health ranking system  and household income across 51 states. Firstly, we organize the data according to gender, ages, and states.  Then we are going to visualize the data by showing the number of deaths vs. different causes.
Our system can provide health advice to people who input their location, age, and gender.



## Health System Demo:
Instrunction: Input age, gender and state, then click submit. The system will find fata matching those information the user input and display the list of top five causes of death for that group of people.
![Health System Animation](https://github.com/ygc506/ECE143_Project15/blob/master/img/healthsystem.gif)
