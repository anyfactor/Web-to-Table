import pandas as pd
from requests_html import HTMLSession
s = HTMLSession()

# URL, Getting the table HTML from the Webpage and converting to a raw table in Pandas
url= 'https://www.uksport.gov.uk/our-work/investing-in-sport/current-funding-figures'
r = s.get(url)
table_elem= r.html.find("table")[1]
df = pd.read_html(table_elem.html)[0]

# Merged rows issue. But luckily the merged issues are separated by a space. Still needs a lot of work.
# Setting the appropriate column
df.columns = df.iloc[0]
# Using the columns that have data on them
df= df.iloc[:, [1,2,3]]

# You can't do this operation (easily) on the DataFrame you have to break it down to nested lists.
df_list= df.values.tolist()

temp_list = []
for row in df_list:
  # Splitting the merged rows then creating a separate lists with them
  for funding_type, funding_amount in list(zip(row[-2].split(), row[-1].split())):
    funding_amount = funding_amount.replace(",", "")[1:]
    temp_list.append([row[0], funding_type, funding_amount])

# The entire dataset
df_parsed = pd.DataFrame(temp_list)
df_parsed.columns = df.columns

# Only selecting the rows that have the word "total" and dropping the "funding_type" column
df_parsed_total = df_parsed[df_parsed['Funding type'] == "Total"]
df_parsed_total= df_parsed_total.iloc[:, [0,2]]

# you get two useful dataset from this.