import pandas as pd
from requests_html import HTMLSession
s = HTMLSession()

# URL, Getting the table HTML from the Webpage and converting to a raw table in Pandas
url= 'https://www.uksport.gov.uk/our-work/investing-in-sport/current-funding-figures'
r = s.get(url)
table_elem= r.html.find("table")[0]
df = pd.read_html(table_elem.html)[0]

# Assigning first row as column
df.columns = df.iloc[0]

# Removing error rows
df = df[1:-1]

# Removing empty columns
df= df.iloc[:, [1,3]]

# Converting currency amount to integer
def convert_currency(amount):
    return int(amount.replace(",", "")[1:]) # the first character is the pound sign

df['Funding Amount (Pound)'] = df['Funding amount'].apply(convert_currency)

# Removing the currency column entirely
df = df.drop('Funding amount', 1)

# Final output
df