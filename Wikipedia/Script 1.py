import pandas as pd
from requests_html import HTMLSession
s = HTMLSession()

###############################################
# Getting the specific table from the article #
###############################################

wiki_url= "https://en.wikipedia.org/wiki/Great_Britain_at_the_2020_Summer_Paralympics"

# Select the specific table of choice by using xpath
wiki_xpath= r'//*[@id="mw-content-text"]/div[1]/div[4]/table/tbody/tr/td[2]/table[1]'
r = s.get(wiki_url)

##########################################
# Getting the table and fixing structure #
##########################################

table_html = r.html.xpath(wiki_xpath)

# pd.read_html returns a list of df. Rather than one df
df = pd.read_html(table_html[0].html)[0]

# Renaming columns as the merge column as heading messed the structure
# use df.columns to get the columns
df = df.rename({
    "Medals by sport.1": "Gold",
    "Medals by sport.2": "Silver",
    "Medals by sport.3": "Bronze",
    "Medals by sport.4": "Total",
}, axis=1)

# More adjustments for the merged column by removing the the top row
df = df.drop(0, axis=0)


###################################
# Assigning appropriate data type #
###################################

for col in ['Gold', 'Silver', 'Bronze', 'Total']:
    df[col] = df[col].astype('int')

# FINAL RESULT
df