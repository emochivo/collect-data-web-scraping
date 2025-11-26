# CREATE A DASHBOARD FROM DATA COLLECTED THROUGH WEB SCRAPING
### Written by: Chi Vo
### Date finished: Nov 25, 2025

### Summary
I collected data from the website Olympedia by web scraping, using the Python library Selenium, then wrote the data into a .csv file. I used PostGreSQL (the Python library psycopg2) to create a database and import the data from the .csv file into the database. After visualizing data with pandas, matplotlib, and seaborn, I created a simple dashboard using Streamlit.

### Steps
#### 1. Web scraping with Selenium to collect data from Olympedia
I went to a page that reports medals by country at the website Olympedia ("https://www.olympedia.org/statistics/medal/country") and used Selenium to scrape data about Olympic medals won by different countries throughout history. I collected data such as country name, year, medal type (gold, silver, bronze), and total medals won. The scraped data was then written into a .csv file for further processing.

#### 2. Create a PostgreSQL database and import data from the .csv file
I connected to a PostgreSQL database using the psycopg2 library in Python. I created a table to store the Olympic medals data and imported the data from the .csv file into the database table for efficient querying and analysis.

#### 3. Visualize data with pandas, matplotlib, and seaborn
To interpret the data, I used the Python library pandas to manipulate and analyze the data. I created various visualizations using matplotlib and seaborn to explore trends and patterns in Olympic medals won by different countries over the years. I made the following main visualizations:
- Two bar charts showing the top 10 countries with the most gold medals and total medals won.
- A linear regression plot showing the correlation between the number of gold medals and total medals won by countries.
- A box plot showing the distribution of total medals won by countries.
- A donut chart showing the proportion of total medals won by countries (<= 350 medals were grouped as "Others").

#### 4. Create a simple dashboard with Streamlit
I used Streamlit to create a simple dashboard that displays the visualizations created in the previous step. The dashboard is not very interactive because I focused more on the data collection and analysis part, but it provides a clear overview of the Olympic medals data.

---
#### How to run the code?
1. Make sure you have Python installed on your machine.

2. Install the required libraries using pip:

   ``` pip install selenium psycopg2 pandas matplotlib seaborn streamlit```

3. Run the main.py file using Streamlit:

   ```streamlit run path/to/your/main.py```


4. Open your web browser and go to the URL provided by Streamlit (usually http://localhost:8501) to view the dashboard.
