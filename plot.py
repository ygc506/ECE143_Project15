import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.offline as py
import seaborn as sns

global_color = "OrangeRed"
line_color = "#3368FF"


def sorted_bar_plot_with_mean(df, x, y, title="Title", xlabel="xlabel", ylabel="ylabel"):
    """
    Plot a sorted bar plot with maximum, minimum and mean.
    :param pandas.DataFrame df: DataFrame of data to plot
    :param str x: Column name of x axis in data
    :param str y: Column name of y axis in data
    :param str title: Title of the plot
    :param str xlabel: Label of x axis in the plot
    :param str ylabel: Label of y axis in the plot
    :return: None
    """
    df = df.sort_values(by=x)  # sort value
    mean = df[x].mean()  # calculate mean

    f, ax = plt.subplots(figsize=(10, 15))
    splot = sns.barplot(x=x, y=y, data=df, color=global_color)
    p = splot.patches[0]
    plt.text(p.get_x() + p.get_width(), p.get_y() + p.get_height(), int(p.get_width()), fontdict={'size': 16})
    p = splot.patches[-1]
    plt.text(p.get_x() + p.get_width(), p.get_y() + p.get_height(), int(p.get_width()), fontdict={'size': 16})
    ax.set_title(title, fontsize=20)
    ax.set_ylabel(ylabel, fontsize=16)
    ax.set_xlabel(xlabel, fontsize=16)
    ax.yaxis.set_tick_params(labelsize=16)
    ax.xaxis.set_tick_params(labelsize=16)
    # line of mean
    ax.axvline(x=mean, lw=5, color=line_color)
    plt.text(mean + 10, p.get_y() / 2, "Mean:\n " + str(int(mean)), fontdict={'size': 16})
    plt.show()


def state_heat_map(df, z, zlabel, title, text):
    """
    Plot Choropleth map of the United States.
    :param pandas.DataFrame df: DataFrame indexed by states
    :param str z: Name of the column containing data to be shown
    :param zlabel: Label of the data
    :param title: Title of the plot
    :param text: Name of the column containing text to be shown when mouseover
    :return: None
    """
    py.init_notebook_mode()

    # extract the state code and add to the df
    statecode = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2011_us_ag_exports.csv')
    statecode = statecode[['code', 'state']]
    df = df.join(statecode.set_index('state'))

    df = df.reset_index()

    for col in df.columns:
        df[col] = df[col].astype(str)

    data = [go.Choropleth(
        colorscale="Reds",
        autocolorscale=False,
        locations=df['code'],
        z=df[z],
        locationmode='USA-states',
        text=df[text],
        marker=go.choropleth.Marker(
            line=go.choropleth.marker.Line(
                color='rgb(255,255,255)',
                width=2
            )),
        colorbar=go.choropleth.ColorBar(
            title=zlabel)
    )]

    layout = go.Layout(
        title=go.layout.Title(
            text=title
        ),
        geo=go.layout.Geo(
            scope='usa',
            projection=go.layout.geo.Projection(type='albers usa'),
            showlakes=True,
            lakecolor='rgb(255, 255, 255)'),
    )

    fig = go.Figure(data=data, layout=layout)
    py.iplot(fig, filename='d3-cloropleth-map')


def scatter_with_best_fit(df, x, y, title="Title", xlabel="xlabel", ylabel="ylabel", datalabel=None):
    """
    Draw scatter plot of x and y, and the best fit line.
    :param pandas.DataFrame df: DataFrame of data to plot
    :param str x: Column name of x axis in data
    :param str y: Column name of y axis in data
    :param str title: Title of the plot
    :param str xlabel: Label of x axis in the plot
    :param str ylabel: Label of y axis in the plot
    :param str datalabel: Description of points themselves
    :return: None
    """
    f, ax = plt.subplots(figsize=(10, 8))
    if datalabel is None:
        sns.scatterplot(x=x, y=y, data=df, color=global_color, s=100)
    else:
        sns.scatterplot(x=x, y=y, data=df, color=global_color, legend="full", s=100,
                        label=datalabel)
        ax.legend(prop={'size': 16})
    ax.set_title(title, fontsize=20)
    ax.set_ylabel(ylabel, fontsize=16)
    ax.set_xlabel(xlabel, fontsize=16)
    ax.yaxis.set_tick_params(labelsize=16)
    ax.xaxis.set_tick_params(labelsize=16)
    # draw best fit line
    lx = list(df[x])
    ly = list(df[y])
    plt.plot(np.unique(lx), np.poly1d(np.polyfit(lx, ly, 1))(np.unique(lx)), color=line_color, lw=5)
    plt.show()
