from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

driver = webdriver.Chrome("C:/Users/lambe/Desktop/chromedriver.exe")

products=[]
prices=[]
ratings=[]

driver.get("https://www.tesco.com/groceries/en-GB/shop/fresh-food/all")

content = driver.page_source
soup = BeautifulSoup(content, features="html.parser")
for a in soup.find_all('div', attrs={'class': 'product-tile-wrapper'}):
    name=a.find('a', href=True, attrs={'class': 'sc-fznWqX dAkvW'}).contents
    products.append(name)

    childTag = a.find('div', attrs={'class': 'price-details--wrapper'})

    if (childTag == None):
        price="[\'Not Available\']"
        prices.append(price)
    
    else:
        price=a.find_next('span', attrs={'class': 'value'}).contents
        prices.append(price)    


print(len(products))
print(len(prices))

#print(products[10])
#print(prices[10])


df = pd.DataFrame({'Product Name':products, 'Price':prices})
df.to_csv('products.csv', index=False, encoding='utf-8')

