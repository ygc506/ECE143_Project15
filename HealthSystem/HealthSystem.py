import sqlite3

import numpy as np
import pandas as pd
from flask import Flask, render_template, request
from pandas.io import sql

app = Flask(__name__)

# read merged data from csv
all_data = pd.read_csv("../data/state_population_ages_all_wo_us.csv")


def getdata4user(data, gender, state, age):
    """
    Get data for specific gender state and age
    :param data: all data
    :type data: pandas.DataFrame
    :param gender: gender male or female
    :type gender: str
    :param state: state
    :type state: str
    :param age: age integer 0 to 250
    :type age: int
    :return: dataframe for specific gender state and age
    :rtype: pandas.DataFrame
    """
    # load data into db
    conn = sqlite3.connect(':memory:')
    data.to_sql('Table1', conn)
    maxage = 150
    assert age < maxage
    age_range = "NULL"
    ranges = np.array([0] + [(5 + 10 * x) for x in range(1, 8)])  # [ 0, 15, 25, 35, 45, 55, 65, 75]
    ranges = np.hstack((ranges[:, None], (ranges + 10 * np.ones(len(ranges)))[:, None]))
    ranges[0, 1] = ranges[1, 0]
    ranges[-1, -1] = -1
    for rg in ranges:
        s, e = [int(i) for i in rg.tolist()]
        if e < 0:
            e = maxage
        if age in range(s, e):
            if e < maxage:
                age_range = f"{s}_{e - 1}"
            else:
                age_range = f"{s}+"
    query = f"select name as cause_of_death, drate as death_rate, d as death_number from Table1 " \
        f"where state=\'{state}\' and gender=\'{gender}\' and age=\'{age_range}\' order by drate desc"
    return sql.read_sql_query(query, conn)


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Render web page based on request.
    :return: Rendered web page
    """
    if request.method == 'POST':
        age = int(request.form["Age"])
        gender = str(request.form["Gender"]).lower()
        state = str(request.form["State"])
        data = getdata4user(all_data, gender, state, age).head()
        table = data.to_html(classes='data')
        # add google search hyperlink to table
        for cause in list(data.cause_of_death):
            q = cause.replace(" ", "+")
            table = table.replace(cause,
                                  f"<a href=\"https://www.google.com/search?q={q}\" target=\"view_window\">{cause}</a>")
        return render_template('result.html', tables=[table], titles=data.columns.values,
                               gender=gender, state=state, age=age)

    return render_template('index.html')


if __name__ == '__main__':
    app.run()
