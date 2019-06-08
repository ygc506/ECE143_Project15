# -*- coding: utf-8 -*-
"""
Created on Wed May 15 00:29:27 2019

@author: Alan
"""

import requests
import json
from bs4 import BeautifulSoup
import pandas as pd
from collections import defaultdict
from pandas import ExcelWriter


def state_list_fun(url):
    '''
    this function finds out all states plus the US itself name and index from website
    
    :param: url
    :type: str
    :rtype: dict{state name: state index} 
    
    '''
    assert isinstance(url,str)
    
    response = requests.get(url) 
    soup = BeautifulSoup(response.text, "html.parser") 
    s_list = soup.find_all("div",class_="scrolling-content-wrapper")

    state_list , state_index= {},0
    for i in s_list[0].find_all('a'):
        print
        state_list[i.text] = str(state_index) if state_index!=0 else ''
        state_index+=1
    
    return state_list


def drate_collection(state,gender):
    '''
    Given state name and gender, collect death rate and causes of death according to state and gender
    Save the dataframe into .csv file
    
    :param: state
    :type: str
    :param: gender
    :type: str
    
    '''
    age_list = ['d','d_0_14','d_15_24','d_25_34','d_35_44','d_45_54','d_55_64','d_65_74','d_75']
    
    
    index = 0
    for region, _ in state_list.items():
        writer = pd.ExcelWriter(f'data/states/{region}.xlsx')
        state='' if region=='United States' else str(index)
        
        for g in gender:           
            for age in range(len(age_list)):
                        
                # change url to the table we want to collect data now
                url = 'https://www.worldlifeexpectancy.com/j/state-gbd-cause-age?sel={}&sex={}&state={}'.format(age_list[age],g,state)  
                response = requests.get(url)
                html_doc = response.content 
                json_parsed = json.loads(html_doc)
    
    
                # avoid missing number in url, check whether url exists
                while (json_parsed['chart']['countries']['countryitem'])==[]:
                    index+=1
                    state='' if region=='United States' else str(index)
                    url = 'https://www.worldlifeexpectancy.com/j/state-gbd-cause-age?sel={}&sex={}&state={}'.format(age_list[age],g,state)  
                    response = requests.get(url)
                    html_doc = response.content 
                    json_parsed = json.loads(html_doc)
    
                # put data into container
                data=defaultdict(int)
                for i in json_parsed['chart']['countries']['countryitem']:
                    tmp = i[age_list[age]].replace(',','')
                    if tmp.isdigit():
                        tmp = int(tmp)
                    data[i['name']] = tmp
                    
    
                # change format to panda Dataframe
                sort_data = sorted(data.items(),key=lambda i:i[0])
                sort_name = [i[0] for i in sort_data]
                sort_num = [i[1] for i in sort_data]
                
                
                if age_list[age]=='d':
                    col_name ='d_all'
                elif age_list[age]=='d_75':
                    col_name ='d_75+'
                else:
                    col_name = age_list[age]
                
                if age ==0:
                    frame = pd.DataFrame({'name': sort_name,col_name: sort_num})
                else:
                    tmp = pd.DataFrame({'name': sort_name, col_name: sort_num})
                    frame = pd.merge(frame, tmp, on='name', how='outer')
                
                frame = frame.fillna(0)
                
            
            # write into file
            frame.to_excel(writer, sheet_name=g, index=False, engine='openpyx1')
            print('State: %s    finish --> %s   %s' % (state, g, region))
        
        index+=1
        writer.save()    
    
    print("= = = done = = =")


def population_collection(state,gender):
    '''
    Given state name and gender, collect population data according to state and gender
    Save the dataframe into .csv file
    
    :param: state
    :type: str
    :param: gender
    :type: str
    
    '''
    writer = pd.ExcelWriter(f'data/population.xlsx')    
    g_index = 0
    for g in gender:
        
        data = defaultdict(list)
        index = 0
        for region, _ in state_list.items():
            
            # change url to the table we want to collect data now
            state='' if region=='United States' else str(index)
    
            url = 'https://www.worldlifeexpectancy.com/j/state-gbd-cause-age?sel=d_35_44&sex=female&state={}'.format(state)  
            response = requests.get(url)
            html_doc = response.content 
            json_parsed = json.loads(html_doc)
    
            
            # avoid missing number in url, check whether url exists
            while (json_parsed['chart']['pops']['popitem'][g_index]['p'])=='0':
                index+=1
                state='' if region=='United States' else str(index)
                url = 'https://www.worldlifeexpectancy.com/j/state-gbd-cause-age?sel=d_35_44&sex=female&state={}'.format(state)  
                response = requests.get(url)
                html_doc = response.content 
                json_parsed = json.loads(html_doc)
                    
            
            # put data into container
            tmp = json_parsed['chart']['pops']['popitem'][g_index]
            for i in tmp.keys():
                if i=='name':
                    continue
                data[region].append(int(tmp[i].replace(',','')))
            index+=1 
            
            print('Gender: %s    finish --> %s' % (g,region))       
        
    
        # change format to panda Dataframe    
        frame = pd.DataFrame(data)  
        frame = frame.T
        frame.columns=["p_all", "p_0_14", "p_15_24", "p_25_34","p_35_44","p_45_54","p_55_64","p_65_74","p_75+"]
        g_index+=1    
        
        # write into file
        frame.to_excel(writer, sheet_name=g, index=True,engine='openpyx1')
    
    writer.save()



if __name__ == '__main__':
    url = "https://www.worldlifeexpectancy.com/usa-cause-of-death-by-age-and-gender"
    state_list = state_list_fun(url)
    
    gender =['female','male','both']
    for i in gender:
        drate_collection(state_list,gender)
        population_collection(state_list,gender)