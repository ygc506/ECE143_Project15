import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import cm
import numpy as np

def read_california(data_file):
    '''
    :param: data_file
    :type:str
    :rtype: pd.Dataframe
    
    return CA data at all age
    
    '''
    assert isinstance(data_file,str)
    data = pd.read_csv(data_file)
    data = data[data.state=='California']
    data = data[data.age=='all']
    return data



def cal_gender(data):
    '''
    :param: data
    :type: pd.Dataframe
    
    calculate the death rate at each gender and show a pie plot.
    
    '''
    assert isinstance(data,pd.DataFrame)
    
    male_data = data[data.gender=='male']
    female_data = data[data.gender=='female']
    male_rate = male_data['d'].sum()/male_data['p'].max()
    female_rate = female_data['d'].sum()/female_data['p'].max()
    labels = 'Male', 'Female'
    sizes = [male_rate*1e4,female_rate*1e4]
    colors = ['lightcoral', 'lightskyblue']
    explode = (0.05 ,0)
    
    # Plot
    f, ax = plt.subplots(figsize=(20, 10))
    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
    autopct='%1.1f%%', shadow=True, startangle=140 ,textprops={'fontsize': 20})
    ax.set_title('Death Rate (Male vs Female) in California, 2017', fontsize =20)
    plt.axis('equal')
    plt.show()


def calculate_cal_gender(data,gender):
    '''
    :param: data
    :type: pd.Dataframe
    :param: gender
    :type: str
    :rtype: pd.DataFrame
    
    return processed data for each gender
    '''
    assert isinstance(data,pd.DataFrame)
    assert isinstance(gender,str)
    
    data = data[data.gender==gender]
    data = data.sort_values(by='d',ascending=False).reset_index()
    data = data.drop(data.columns[[0]],axis=1)
    
    target_data_m = data[['name','d']].iloc[:10].sort_values('name')
    other_data = data[['d']].iloc[10:].sum()
    target_data_m.loc[10] = data[['name','d']].iloc[10]
    target_data_m.at[10,'name'] = 'Others'
    target_data_m.at[10,'d'] = other_data
    
    return target_data_m
        
def plot_cal_gender(target_data_m,gender):
    '''
    :param: target_data_m
    :type: pd.Dataframe
    
    create pie plot show CA death rate at each gender
    '''
    assert isinstance(target_data_m,pd.DataFrame)
    assert isinstance(gender,str)
    
    labels = list(target_data_m.name)
    sizes = list(target_data_m.d)
    cs = cm.Set3(np.arange(len(sizes))/len(sizes))
    explode = np.ones((len(sizes)))
    explode*=0.1
    explode[5]=0
    # Plot
    f, ax = plt.subplots(figsize=(20, 10))
    plt.pie(sizes,explode=explode, labels=labels, colors=cs, pctdistance=0.8,
    autopct='%1.1f%%', shadow=True, startangle=150,textprops={'fontsize': 18})
    ax.set_title(f'Top 10 Death Causes ({gender}) in California, 2017', fontsize =22)
    ax.title.set_position([.5, 1.05])
    plt.axis('equal')
    plt.show()

def cal_gender_compare(data):
    '''
    :param: data
    :type: pd.Dataframe
    
    focus at CA each gender's death rate and return a pie plot
    '''
    assert isinstance(data,pd.DataFrame)

    target_data_m = calculate_cal_gender(data,'male')
    target_data_f = calculate_cal_gender(data,'female')
    
    set_A = set(target_data_m.name) & set(target_data_f.name)
    list_set_A = list(set_A)
    list_set_B = list(set_A)
    target_data_m.index = target_data_m.name
    target_data_f.index = target_data_f.name
    
    male_dif = list(set(target_data_m.name).difference(set_A))
    female_dif = list(set(target_data_f.name).difference(set_A))
    
    list_set_A.extend(male_dif)
    list_set_B.extend(female_dif)
    target_data_m = target_data_m.reindex(list_set_A)
    target_data_f = target_data_f.reindex(list_set_B)
    # -------------------------------------------------------------------------
    
    plot_cal_gender(target_data_m,'male')
    plot_cal_gender(target_data_f,'female')


def cal_age(data_file):
    '''
    :param: data_file
    :type: str
    
    calculate CA death rate at each age range and return a pie plot
    '''
    assert isinstance(data_file,str)
    
    data = pd.read_csv(data_file)
    data = data[data.state=='California']
    data = data[data.gender=='both']
    data = data[data.age!='all']
    
    tmp = data.groupby('age')['d'].sum().to_frame()
    tmp['p'] = data.groupby('age')['p'].sum().to_frame()
    tmp = tmp.reset_index(level='age')
    
    labels = list(tmp.age)
    sizes = list(tmp.d)
    cs = cm.Set3(np.arange(len(sizes))/len(sizes))
    explode = np.ones((len(sizes)))
    explode[-1]=0
    explode[:-1]*=0.1
    
    # Plot
    f, ax = plt.subplots(figsize=(20, 10))
    plt.pie(sizes, explode = explode, labels=labels, colors=cs, pctdistance=0.8,
    autopct='%1.1f%%', shadow=True, startangle=40 ,textprops={'fontsize': 20})
    ax.set_title('Deaths (Ages) in California, 2017', fontsize =20)
    plt.axis('equal')
    
    plt.show()



def cal_youth(data_file):
    '''
    :param: data_file
    :type: str
    
    calculate CA death rate at 15-34 range and return a pie plot
    '''
    assert isinstance(data_file,str)
    
    data = pd.read_csv(data_file)
    data = data[data.state=='California']
    
    data = data[data['age'].isin(['15_24','25_34'])]
    data = data[data.gender=='both']
    data = data.groupby('name')['d'].sum().to_frame().reset_index()
    data = data.sort_values(by='d',ascending=False).reset_index()
    data = data.drop(data.columns[[0]],axis=1)
    
    target_data = data[['name','d']].iloc[:10]
    other_data = data[['d']].iloc[10:].sum()
    target_data.loc[10] = data[['name','d']].iloc[10]
    target_data.at[10,'name'] = 'Others'
    target_data.at[10,'d'] = other_data
    
    labels = list(target_data.name)
    sizes = list(target_data.d)
    cs = cm.Set3(np.arange(len(sizes))/len(sizes))
    explode = np.ones((len(sizes)))
    explode[-1]=0
    explode[:-1]*=0.1
    # Plot
    f, ax = plt.subplots(figsize=(20, 10))
    plt.pie(sizes,explode=explode, labels=labels, colors=cs, pctdistance=0.8,
    autopct='%1.1f%%', shadow=True, startangle=50,textprops={'fontsize': 18})
    ax.set_title('Top 10 Death Causes (Male & Female, 15-34) in California, 2017', fontsize =22)
    ax.title.set_position([.5, 1.05])
    plt.axis('equal')
    plt.show()