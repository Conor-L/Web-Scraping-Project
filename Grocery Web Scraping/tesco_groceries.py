from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

# Move the Chrome Driver executable to the folder containing the script and this PATH will work correctly
PATH="chromedriver.exe"

# General options in order to control the behaviour of the web driver
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images":2})

# Create the driver alongside the PATH and options provided
driver = webdriver.Chrome(options=chrome_options, executable_path=PATH) 

# URL locations of different categories
tesco_freshfoods = "/fresh-food/all"
tesco_bakery = "/bakery/all"
tesco_frozenfoods = "/frozen-food/all"
tesco_foodcupboard = "/food-cupboard/all"
tesco_drinks = "/drinks/all"

# Simple terminal input to find which page the user wants to use

print("""

        Choose from the following options numerically (i.e. 1):

        [1] Fresh Foods
        [2] Bakery Foods
        [3] Frozen Foods
        [4] Food Cupboard
        [5] Drinks


""")

successfulInput = False
while (successfulInput == False):
	try:
		choiceInput = int(input())
		if not choiceInput:
			raise ValueError('empty string')
		else:
			matchSingle = re.search("[12345]{1}", str(choiceInput))
			matchMultiple = re.search("[12345]{2,}", str(choiceInput))
			if (matchSingle is None or matchMultiple is not None):
				raise ValueError('out of range')
			else: successfulInput = True
	except ValueError as e:
		print("Please choose a valid option")

# Create a dictionary as replacement for a switch/case statement
def selectChoice(i):
    return {
        1: tesco_freshfoods,
        2: tesco_bakery,
        3: tesco_frozenfoods,
        4: tesco_foodcupboard,
        5: tesco_drinks
    }.get(i, tesco_freshfoods) # if an invalid input is entered then the default value will just be the first option

# Create filename based on website section
def filenameChoice(x):
    return {
        1: "Fresh_Foods",
        2: "Bakery_Foods",
        3: "Frozen_Foods",
        4: "Food_Cupboard",
        5: "Drinks"
    }.get(x, "Fresh_Foods")

# String variable for containing the location of the groceries
selectedChoice = selectChoice(choiceInput)

# Lists that will be used for the data
products=[]
prices=[]

driver.get("https://www.tesco.com/groceries/en-GB/shop" + selectedChoice) # Website location for webscraping

content = driver.page_source # The content of the web page
soup = BeautifulSoup(content, features="html.parser") # Constructor for Beautiful Soup

# Store the Currency unit
currency = soup.find('span', attrs={'class': 'currency'}).getText()

# Find out how many pages there are on this website URL
pgno_list=[]
for i in soup.find_all('a', attrs={'class': 'pagination--button'}):
    if i.find('span', attrs={'aria-hidden': 'true', 'class': None}) != None:
        pgno_list.append(int(i.getText()))

max_pgno = max(pgno_list)

for x in range(max_pgno + 1):

    driver.get("https://www.tesco.com/groceries/en-GB/shop" + selectedChoice + "?page=" + str(x)) # Website location for webscraping

    content = driver.page_source # The webpage
    soup = BeautifulSoup(content, features="html.parser") # Constructor for bs4

    for a in soup.find_all('div', attrs={'class': 'product-tile-wrapper'}):
        name=a.find('a', href=True, attrs={'class': 'sc-fznWqX dAkvW'}).getText()
        products.append(name)

        availability_tag = a.find('div', attrs={'class': 'price-details--wrapper'})

        if (availability_tag == None):
            price="Not Available"
            prices.append(price)
    
        else:
            price=a.find_next('span', attrs={'class': 'value'}).getText()
            prices.append(float(price))

# Zip products and prices lists together in order to sort the lists into a more sensible order
zipped = zip(products, prices)
sort_zipped = sorted(zipped)

# Run zip again with * to unzip the two lists back into their original variables
products, prices = zip(*sort_zipped)

df = pd.DataFrame({'Product Name':products, 'Price':prices})
df.to_csv(filenameChoice(choiceInput)+'.csv', index=False, encoding='utf-8')

driver.quit()

