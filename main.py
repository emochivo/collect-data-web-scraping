# libraries for data visualization
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.patches import Patch
import seaborn as sns
import psycopg2
import streamlit as st
  

# and then do the data visualization with matplotlib, pandas, seaborn, etc.
conn = psycopg2.connect(database='postgres',
                        user='postgres',
                        password='12345678',
                        port=5432,
                        options='-c search_path=web_scraping_project')

query = 'select * from medals_by_country'


# put the whole table to the df variable
df = pd.read_sql(query, conn)


## Figure 1: Top 20 countries with the most medals in total (1.1) and Top 20 with most gold medals (1.2)
# sort both top-20 tables by the metric we care about and reset the index so positional access is stable
top20countries_total = df.sort_values(by='total_medals', ascending=False).head(20).reset_index(drop=True)
top20countries_gold = df.sort_values(by='gold_medals', ascending=False).head(20).reset_index(drop=True)

# build a list of country codes whose positions are the same between the two sorted top-20 lists
country_tmplist = []
for i in range(len(top20countries_gold)):
    if top20countries_gold.loc[i, 'country_code'] == top20countries_total.loc[i, 'country_code']:
        country_tmplist.append(top20countries_gold.loc[i, 'country_code'])


figure1 = plt.figure(figsize=(11,7))

sp1_f1 = plt.subplot(2,1,1)
t1 = sns.barplot(top20countries_total, x='country_code', y='total_medals',
            palette=['blue' if country in country_tmplist else 'orange' for country in top20countries_total['country_code']])
# add the value of each bar on top of the bar
for bar in t1.containers:
    plt.bar_label(bar, fontsize=8, padding=-0.5)
plt.ylabel("Total Medals")
plt.xlabel("Countries")


sp2_f1 = plt.subplot(2,1,2)
t2 = sns.barplot(top20countries_gold, x='country_code', y='gold_medals', 
            palette=['blue' if country in country_tmplist else 'orange' for country in top20countries_total['country_code']])
# add the value of each bar on top of the bar
for bar in t2.containers:
    plt.bar_label(bar, fontsize=8, padding=-0.5)
plt.ylabel("Gold Medals")
plt.xlabel("Countries")

plt.suptitle("Top 20 Countries with Most Total Medals vs. Most Gold Medals")
patch1 = Patch(color='orange', label='Countries with different ranks')
patch2 = Patch(color='blue', label='Countries with same ranks')
plt.figlegend(handles=[patch1, patch2], loc='upper right')


## Figure 2: The linear regression plot with trends displaying the relationship between total and gold medals in every country
figure2 = plt.figure(figsize=(11,7))
sns.regplot(x=df['gold_medals'], y=df['total_medals'], color='purple', line_kws=dict(color='red'))
plt.title("The correlation between Gold Medals vs. Total Medals quantity")


## Figure 3: The box plots displaying the distribution of gold medals (3.1), silver medals (3.2), and bronze medals (3.3)
figure3 = plt.figure(figsize=(11,7))
plt.boxplot([df['gold_medals'], df['silver_medals'], df['bronze_medals']], 
            tick_labels=["Gold Medals", "Silver Medals", "Bronze Medals"])
plt.title("Distribution of medals of all countries")


## Figure 4: A pie chart presenting the percentage of medals (total) that each country has achieved
figure4 = plt.figure(figsize=(11,7))
total_medals_pie = []
others = 0
for i in range(len(df)):
    if df.loc[i, 'total_medals'] > 350:
        total_medals_pie.append([df.loc[i, 'country'], int(df.loc[i, 'total_medals'])])
    else:
        others += int(df.loc[i, 'total_medals'])
total_medals_pie.append(['Others', others])

total_medals_pie_numbers = [item[1] for item in total_medals_pie]

cmap = cm.get_cmap('tab20')
plt.pie(x=total_medals_pie_numbers, autopct='%1.1f', pctdistance=0.91,
        wedgeprops={'width': 0.6, 'edgecolor': 'black', 'label': 'hi'}, textprops={'fontsize': 8}, radius=1.05)
plt.text(0,0, f"Total medals:\n{sum(total_medals_pie_numbers[1:-1])}",ha='center',va='center')

plt.legend([item[0] for item in total_medals_pie],bbox_to_anchor=(1.5,0.97), loc='upper right')
plt.title("Percentage of total medals in each country (unit: percent)" )

figure4.subplots_adjust(left=-0.13)


# show all figures
# plt.show()




### DASHBOARD???

st.title("Olympic Medals: A Simple Dashboard")
st.subheader("A simple analysis of Olympic medals won by different countries throughout history")  


col1, col2 = st.columns(2, gap="large")


with col1:
    st.pyplot(figure1)
    st.caption('''
    Until now, USA is the country with the most total and gold Olympic medals, with 3105 and 1229 medals, respectively.
               The former Soviet Union, even though no longer exist, is still having incredible numbers of gold medals (473 - rank #2)
               and total medals (1204 - rank #3). The USA's gold and total medals are approximately 2.6 times larger than 
               the second-ranks in each category.
               \n
    There are countries that remain the same ranks in both gold and total medals (e.g, USA, Britain, Italy, Russia, Sweden,
               Japan, the Netherlands, and Switzerland), but even though having rank changes, most of the countries in top 20 
               gold medals will still be in top 20 in total medals. Not mentioning the countries that do not exist anymore, 
               the countries with high medal counts are usually from Europe, North America, and East Asia.
    ''')
    st.caption('---')
    st.pyplot(figure2, )
    st.caption('''
    Using linear regression, the correlation between gold medal and total medal counts is strongly positive. The data points mostly are above 
               the regression line, indicating that countries usually have more total medals than what would be expected from their gold medal counts. 
               The majority of data points also locate at the origin, which implies that most countries obtain zero or just a few medals in general 
               (also lead to few gold medal counts).

    ''')

with col2:
    st.pyplot(figure3)
    st.caption('''
    The box plots are not the ideal visualizations for the medal distributions due to the high number of outliers (countries with very high medal counts).
               However, we can still observe that the median values of gold, silver, and bronze medals are all very low (close to 0). The interquartile ranges 
               (IQRs) are also small, indicating that most countries have low medal counts. The presence of numerous outliers shows that only a few countries 
               have exceptionally high medal counts, which skews the distribution.
               \n
    Looking at the box plots, the outliers for gold medals appear to have higher values compared to silver and bronze medals. This implies that countries with 
               high medal counts tend to focus on and win more gold medals relative to silver and bronze. This could be due to various factors, such as investment 
               in elite athletes, training programs, and sports infrastructure that prioritize winning gold medals.
    ''')
    st.caption('---')
    st.pyplot(figure4)
    st.caption('''
    The donut chart illustrates that only a small number of countries dominate the total medal counts in the Olympics. Countries like USA, Soviet Union, 
               Germany, Great Britain, and France have significantly larger shares of the total medals compared to other countries. This indicates a concentration 
               of athletic success in a few nations, especially developed countries with strong sports programs and resources.
               \n
    The "Others" category, which aggregates the medal counts of all remaining countries with fewer medals, still constitutes a substantial portion of the total medals.
                This highlights that while a few countries dominate, there is still a diverse range of nations contributing to the overall medal count in the Olympics.
    ''')

st.set_page_config(layout="wide", page_title="Olympic Medals Dashboard", page_icon=":bar_chart:")
