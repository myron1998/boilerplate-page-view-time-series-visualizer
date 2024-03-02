import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv("fcc-forum-pageviews.csv", parse_dates=['date'], index_col='date')


# Clean data
df = df[(df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))]

months_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']


def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(14, 7))
    ax.plot(df.index, df['value'], color='red', label='Page Views')
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")
    ax.legend()

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar['month'] = df_bar.index.month_name()
    df_bar['year'] = df_bar.index.year

    df_pivot = pd.pivot_table(df_bar, values='value', index='year', columns='month', aggfunc='mean')

    # Draw bar plot
    fig, ax = plt.subplots(figsize=(12, 10))
    df_pivot = df_pivot.reindex(columns=months_order)
    df_pivot.plot(kind='bar', ax=ax)
    ax.set_xlabel("Years")
    ax.set_ylabel("Average Page Views")
    ax.legend(title="Months", labels=months_order, loc='upper left')

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(20, 8))

    # Draw box plots (using Seaborn)
    # Year-wise
    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0])
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Page Views")
    axes[0].set_title("Year-wise Box Plot (Trend)")

    # Month-wise
    sns.boxplot(x='month', y='value', data=df_box, ax=axes[1])
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Page Views")
    axes[1].set_title("Month-wise Box Plot (Seasonality)")
    axes[1].set_xticklabels(labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])


    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
