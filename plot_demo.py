import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from math import pi
from bokeh.io import show
from bokeh.models import LinearColorMapper, LogColorMapper, LogTicker,FixedTicker, AdaptiveTicker,BasicTicker, LogTickFormatter, PrintfTickFormatter, ColorBar
from bokeh.plotting import figure
from math import pow
#import matplotlib

def base_data(data_file):
    '''
    :param: data_file
    :rtype: str
    
    return state data (male and female)
    '''
    assert isinstance(data_file,str)
    
    data = pd.read_csv(data_file)
    data = data[data.state!='United States']
    data = data[data.gender!='both']

    return data

def gender_all_data(data_file,gender):
    '''
    :param: data_file
    :type: str
    :param: gender
    :type: str
    :rtype: pd.Dataframe
    
    return gender data at all age
    
    '''
    assert isinstance(data_file,str)
    assert isinstance(gender,str)
    
    data = pd.read_csv(data_file)
    data = data[data.age=='all']
    data = data[data.gender==gender]

    return data

def both_data(data_file):
    '''
    :param: data_file
    :type: str
    :rtype: pd.Dataframe
    
    return both gender data

    '''
    assert isinstance(data_file,str)
    
    data = pd.read_csv(data_file)
    data = data[data.gender=='both']

    return data


def top_10_causeofdeath(data):
    '''
    :param: data
    :type: pd.Dataframe
    
    plot US top 10 cause of death (barplot)
    
    '''
    assert isinstance(data,pd.DataFrame)
    
    target_data = data.groupby('name')['d'].sum().to_frame().sort_values(by='d', ascending=False)
    target_data = target_data.reset_index(level=['name'])
    total_mortal = 2813503
    target_data['d'] = target_data['d'] / total_mortal * 100
    
    f, ax = plt.subplots(figsize=(10, 8))
    splot = sns.barplot(x="d", y="name", data=target_data.iloc[:10], color='orangered')
    
    for p in splot.patches:
        plt.text(p.get_width(),p.get_y()+p.get_height()/2,'%.2f %%' % p.get_width()) 
    
    ax.set_title('2017 Top 10 Death Cause in US', fontsize =20)
    ax.set_ylabel('Name of Death Cause',fontsize=16)
    ax.set_xlabel('Percentage of Deaths',fontsize=16)
    ax.yaxis.set_tick_params(labelsize=16)
    ax.xaxis.set_tick_params(labelsize=14)
    plt.show()
    
    
def gender_related(target_m, target_fm, order):
    '''
    :param: target_m
    :type: pd.Dataframe
    :param: target_fm
    :type: pd.Dataframe
    :param: order
    :type: str
    
    plot gender_related cause of death (scatter plot)
    
    '''
    assert isinstance(target_fm,pd.DataFrame)
    assert isinstance(target_m,pd.DataFrame)
    
    merge = pd.merge(target_m,target_fm,on='name',how='outer')
    merge = merge.fillna(0)
    merge['diff'] = merge['female_rate'] - merge['male_rate']
    
    if order=='first':
        merge = merge.iloc[:35]
    else:
        merge = merge.iloc[35:]
    sns.set(style="darkgrid")
    f, ax = plt.subplots(figsize=(12, 12))
    plt.scatter(merge['diff'],merge['name'],s=100,c=merge['diff'],cmap=plt.cm.coolwarm)
    
    ax.set(xlim=(-0.03,0.03))
    ax.set_title('Gender-Related Death Cause in the US, 2017', fontsize =20)
    ax.set_ylabel('Name of Death Cause',fontsize=16)
    ax.set_xlabel('Difference between Percentage of Deaths',fontsize=16)
    ax.yaxis.set_tick_params(labelsize=16)
    ax.xaxis.set_tick_params(labelsize=14)
    ax.get_yticklabels()[1].set_color("red")
    ax.get_yticklabels()[7].set_color("red")

def age_related_heatmap(data):
    '''
    :param: data
    :type: pd.Dataframe
    
    plot age_related cause of death (heatmap)
    
    '''
    assert isinstance(data,pd.DataFrame)
    
    tmp1 = data.groupby(['name','age'])['p'].sum().to_frame()
    tmp1['d'] = data.groupby(['name','age'])['d'].sum().to_frame()
    tmp1['d'] = tmp1['d']/tmp1['p'] *1e5
    tmp1 = tmp1.reset_index(level=['name','age'])
    tmp1 = tmp1.drop(columns=['p'])
    df = tmp1
    
    names = list(df.groupby('name').max().index)
    
    range_age =list(df.groupby('age').max().index)
    
    colors = ['#fff7ec','#fee8c8','#fdd49e','#fdbb84','#fc8d59','#ef6548','#d7301f','#b30000','#7f0000']
    n_color = len(colors)
    mapper = LogColorMapper(palette=colors,low=df.d.min(), high=df.d.max())
    
    TOOLS = "hover,save,pan,box_zoom,reset,wheel_zoom"
    
    p = figure(title="Death Causes distribution in US  ({0} - {1})".format(names[0], names[-1]),
               x_range= names, y_range=list(reversed(range_age)),
               x_axis_location="below", plot_width=1200, plot_height=700,
               tools=TOOLS, toolbar_location='below',
               tooltips=[('disease', '@name'), ('Death Rate/100k', '@d')])
    
    p.title.align = 'center'
    p.title.text_font_size = '20pt'
    p.grid.grid_line_color = None
    p.axis.axis_line_color = None
    p.axis.major_tick_line_color = None
    p.axis.major_label_text_font_size = "10pt"
    p.axis.major_label_standoff = 0
    p.xaxis.major_label_orientation = pi / 3
    p.xaxis.major_label_text_font_style='bold'
    p.yaxis.major_label_text_font_style='bold'
    p.xaxis.axis_label = "Death Casue"
    p.yaxis.axis_label = "Age"
    p.xaxis.axis_label_text_font_size = "15pt"
    p.yaxis.axis_label_text_font_size = "15pt"
    
    p.rect(x="name", y="age", width=1, height=1,
           source=df,
           fill_color={'field': 'd', 'transform': mapper},
           line_color=None)
    
    e = round(pow(df.d.max(), 1/n_color),5)-0.00001
    ticks = []
    for i in range(n_color+1):
        tick = int(e**i)
        if len(ticks)>0 and tick == ticks[len(ticks)-1]:
            ticks.append(tick+1)
        else:
            ticks.append(tick)
    print(ticks)
    color_bar = ColorBar(color_mapper=mapper, major_label_text_font_size="9pt",
                         ticker=FixedTicker(ticks=ticks), 
                         location=(0, 0))
    
    p.add_layout(color_bar, 'right')
    show(p)      # show the plot
    
    
def age_related(data,age):
    '''
    :param: data
    :type: pd.Dataframe
    
    plot age_related cause of death at certain causes of death(line plot)
    
    '''
    assert isinstance(data,pd.DataFrame)
    assert isinstance(age,str)
    if age=='Age-unrelated':
        plot = ['Drownings','Road Traffic Accidents','Suicide']
        range_ = [ 0.000,0.05]
    elif age=='Age-related(child)':
        plot = ['Birth Trauma','Low Birth Weight']
        range_ = [ 0.000,0.01]
    elif age=='Age-related(The Middle-aged)':
        plot = ['Drug Use','HIV/AIDS','Homicide','Hepatitis B', 'Hepatitis C','Poisonings']
        range_ = [ 0.000,0.05]
    else:
        plot = ['Coronary Heart Disease','Diabetes Mellitus', 'Endocrine Disorders', \
                'Hypertension', 'Lung Cancer', 'Pancreas Cancer','Prostatic Hypertrophy',\
                'Schizophrenia', 'Stomach Cancer', 'Stroke']
        
    print(plot)
    drate = data.loc[:,['name','age','drate']]
    drate['drate'] = drate['drate']*100
    tmp = drate[drate['name'].isin(plot)]
    sns.set(style="whitegrid")
    f, ax = plt.subplots(figsize=(10, 10))
    ax = sns.lineplot(x="age",y="drate", hue='name',\
                      markers=True, data=tmp,palette="tab10", linewidth=1) 
    ax.legend(loc='best',fontsize='large', title_fontsize='15')
    ax.set_title(f'{age} Death Cause in the US, 2017', fontsize='20')
    ax.set_xlabel('Age',fontsize=20)
    ax.set_ylabel('Death Rate (%)',fontsize=20)
    if age!='Age-related(The Elderly)':
        ax.set_ylim(range_)
    ax.yaxis.set_tick_params(labelsize=14)
    ax.xaxis.set_tick_params(labelsize=14)
    
