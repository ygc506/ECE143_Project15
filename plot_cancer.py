from matplotlib import cm
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def calculate_rate(file_name, gender):
    '''
    :param: file_name
    :type: str
    :param: gender
    :type: str
    :rtype: float
    
    return death rate at each gender for cancer 
    '''
    assert isinstance(file_name,str)
    assert isinstance(gender,str)
    
    # load male data for a plot 
    data1 = pd.read_csv(file_name)
    data1 = data1[data1.gender ==gender]
    data = data1[data1.age== 'all']
    tmp = list(data1.name.unique())
    cancer_list = [i for i in tmp if i.endswith('Cancer') or i.endswith('Cancers')]
    
    # get male_death number for each state
    data_tmp= data[data['name'].isin(cancer_list)]
    death = data_tmp.groupby('state').sum() # get the death number
    death = death.reset_index() # reset index 
    
    
    # get male_population for each state
    population = data_tmp.groupby('state').max() # get the population
    population = population.reset_index() # reset the index 
    population
    
    # calculate the total death number,total population for all the states, and male_drate
    drate = (death.d.sum()/population.p.sum())

    return drate

def cancer_study(file_name):
    '''
    :param: file_name
    :type: str
    
    return pie plot of cancer cause of death for each gender.
    '''
    male_drate = calculate_rate(file_name,'male')
    female_drate = calculate_rate(file_name,'female')

    # Data to plot
    labels = 'Male cancer \ndeath rate', 'Female cancer \n death rate'
    sizes = [male_drate / (male_drate+female_drate), female_drate/(male_drate + female_drate)]
    colors = ['lightcoral', 'lightskyblue']
    explode = (0.05, 0)  # explode 1st slice
    
    # Plot
    f,ax = plt.subplots (figsize=(20,10))
    plt.pie(sizes, explode=explode, labels=labels, colors=colors,pctdistance = 0.6,
    autopct='%1.1f%%', shadow=True, startangle=140, textprops={"fontsize": 20})
    ax.set_title ('Cancer disease death rate (Male vs Female) in 2017', fontsize = 22)
    plt.axis('equal')
    ax.title.set_position([.5, 1.05])
    plt.show()
    
    
    
def cancer_age(file_name):
    '''
    :param: file_name
    :type: str
    
    return pie plot of cancer cause of death for each range.
    
    '''

    # load male data for a plot 
    data1 = pd.read_csv(file_name)
    data1 = data1[data1.gender =='both']
    
    tmp = list(data1.name.unique())
    cancer_list = [i for i in tmp if i.endswith('Cancer') or i.endswith('Cancers')]
    data_tmp= data1[data1['name'].isin(cancer_list)]
    
    all_age= data_tmp.groupby('age').sum() # get all_age death number for cancer
    all_age_pop = data1.groupby('age').max()
    
    
    target_data= pd.concat([all_age.d, all_age_pop.p],axis=1)
    target_data['drate'] = target_data.d /target_data.p
    target_data['percentage']=target_data.drate / target_data.drate.sum()
    target_data = target_data[target_data.percentage != 0]
    
    
    
    # Data to plot
    labels = ['25-34', '35-44','45-54', '55-64', '65-74', '75+']
    
    sizes = list(target_data['percentage'])
    cs = cm.Set3(np.arange(len(sizes))/len(sizes))
    explode = np.ones((len(sizes)))
    

    explode[-1] = 0;
    explode[:-1]*= 0.05
    
    cs = cm.Set3(np.arange(len(sizes))/len(sizes))
    # Plot
    f,ax = plt.subplots (figsize=(20,10))
    plot_data = target_data['percentage'].to_list()
    wedges, texts = ax.pie(plot_data, explode = explode, wedgeprops=dict(width=1), colors=cs, shadow=True,  startangle=140)
    
    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
    kw = dict(arrowprops=dict(arrowstyle="-"),
              bbox=bbox_props, zorder=0, va="center")
    
    for i, p in enumerate(wedges):
        ang = (p.theta2 - p.theta1)/2. + p.theta1
        y = np.sin(np.deg2rad(ang))
        x = np.cos(np.deg2rad(ang))
        str = 'Ages: {}:\n {:.2f} %'.format(labels[i],plot_data[i]*100)
        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        connectionstyle = "angle,angleA=0,angleB={}".format(ang)
        kw["arrowprops"].update({"connectionstyle": connectionstyle})
        
        if i==0:
            ax.annotate(str, xy=(x, y), xytext=(1.3*np.sign(x), 1.55*y),
                        horizontalalignment=horizontalalignment, fontsize=18, **kw)
        elif i==1:
            ax.annotate(str, xy=(x, y), xytext=(1.3*np.sign(x), 1.25*y),
                        horizontalalignment=horizontalalignment, fontsize=18, **kw)
        else:    
            ax.annotate(str, xy=(x, y), xytext=(1.3*np.sign(x), 1.05*y),
                        horizontalalignment=horizontalalignment, fontsize=18, **kw)
    
    
    ax.set_title ('Cancer disease death rate based on different age range in 2017', fontsize = 22)
    ax.title.set_position([.5, 1.05])
    plt.axis('equal')
    plt.show()
