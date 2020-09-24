from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd

chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images":2})
driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="C:/Users/lambe/Desktop/chromedriver.exe") # ChromeDriver.exe location on device

# Locations of different categories
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

choiceInput = int(input())

# Create a dictionary as replacement for a switch/case statement
def selectChoice(i):
    return {
        1: tesco_freshfoods,
        2: tesco_bakery,
        3: tesco_frozenfoods,
        4: tesco_foodcupboard,
        5: tesco_drinks
    }.get(i, tesco_freshfoods)

selectedChoice = selectChoice(choiceInput)

# Lists that will be used for the data
products=[]
prices=[]
#ratings=[]

driver.get("https://www.tesco.com/groceries/en-GB/shop" + selectedChoice) # Website location for webscraping

content = driver.page_source # The webpage
soup = BeautifulSoup(content, features="html.parser") # Constructor for bs4

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


#print(len(products))
#print(len(prices))

#print(products[10])
#print(prices[10])


df = pd.DataFrame({'Product Name':products, 'Price':prices})
df.to_csv('products.csv', index=False, encoding='utf-8')

driver.quit()

