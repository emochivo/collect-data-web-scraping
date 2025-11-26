# required libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import csv # need this to create CSV file for data

# use Chrome for the webdriver
driver = webdriver.Chrome()

# read the website called Olympedia, which shows Olympic medals by country
driver.get("https://www.olympedia.org/statistics/medal/country")

# find the medal data by using the ID="medals"
medals = driver.find_elements(By.ID, "medals")

# obtain the lists of medals
medals_list = medals[0].text.split("\n")
medals_list.pop(0) # erase the header


for m in range(len(medals_list)):
    og_string = medals_list[m] # assign each element in the list to a temporary var 
    new_string = "" # create a new var to store the country name
    num = ""
    medals_num = [] # create a list to store the number of medals
                    # medals_num includes 4 numbers in order: gold, silver, bronze, total

    for n in og_string:
        if n.isdigit():
            num += n
        elif n.isalpha() or n.isspace() or n == "'":
            new_string += n

        if (num != "" and n.isspace()): 
            medals_num.append(int(num))
            num = ""
    
    # the total medals number still in variable num, so i'll put it into the list
    medals_num.append(int(num))

    country_name, country_code = new_string[:-8], new_string[-7:-4]
    medals_list[m] = [m+1, country_name, country_code] + [medals_num[i] for i in range(len(medals_num))]

driver.close()
 
# make the csv file to store the data
data = [["Number Order", "Country", "Country Code", "Gold Medal", "Silver Medal", "Bronze Medal", "Total"]] + \
        [medals_list[m] for m in range(len(medals_list))]

with open('olympic_medal_by_country.csv', 'w', newline='', encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(data)