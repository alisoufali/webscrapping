# Amazon book searcher
## Library Importation
import requests
from bs4 import BeautifulSoup

## Parameter and Variable Definition
Url = "https://www.amazon.com/s"
print(" ")
Search_Text = input("Please enter the name of the book you want to search: ")
print("--------------------------------------------------------------------")
print(" ")
Payload = {"k":Search_Text, "i":"stripbooks-intl-ship"}
Headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36", "Accept-Language":"en-US,en;q=0.5"}
Price_Symbol = "$"

## Web-Scrapping, Data Gathering and Data Processing
Response = requests.get(Url, headers=Headers, params=Payload)
Soup = BeautifulSoup(Response.text, "lxml")
Books_Soup = Soup.select(".s-line-clamp-2")
Authors_Soup = Soup.select(".sg-col-12-of-28 .a-row.a-color-secondary")
Prices_Soup = Soup.select(".sg-col-20-of-28 .sg-col-4-of-32 .sg-col-inner")
Length = len(Books_Soup)
Books = []
Authors = []
Prices_Paperback = []
for Index in range(0, Length):
	Book = Books_Soup[Index].a.span.get_text()
	Books.append(Book)
	Author_Text = Authors_Soup[Index].get_text()
	Author_Text = Author_Text.replace("\n", "")
	while True:
		Author_Text_Temp = Author_Text.replace("  ", " ")
		if (Author_Text_Temp==Author_Text):
			break
		Author_Text = Author_Text_Temp
	if ("|" in Author_Text):
		Author_Text = Author_Text[3:(Author_Text.index("|")-1)]
	else:
		Author_Text = Author_Text[3:]
	Author = Author_Text
	Authors.append(Author)
	Price_Text = Prices_Soup[Index].get_text()
	Price_Text = Price_Text.replace("\n","")
	while True:
		Price_Text_Temp = Price_Text.replace("  ", " ")
		if (Price_Text_Temp==Price_Text):
			break
		Price_Text = Price_Text_Temp
	if ("other format" in Price_Text.lower()):
		Index_OtherFormat = Price_Text.lower().index("other format")
		Price_Text = Price_Text[:Index_OtherFormat]
	if ("paperback" in Price_Text.lower()):
		Index_Paperback = Price_Text.lower().index("paperback")
		Price_Text = Price_Text[Index_Paperback+10:]
		Price_Text_List = Price_Text[Price_Text.index("$")+1:].split(".")
		Price_Paperback = Price_Text_List[0]+"."+Price_Text_List[1][:2]
		try:
			Price_Paperback = float(Price_Paperback)
		except:
			print(Price_Text)
		Prices_Paperback.append(Price_Paperback)
	else:
		Prices_Paperback.append(None)
	print("Book Name: {}".format(Books[-1]))
	print("Author: {}".format(Authors[-1]))
	print("Paperback-Price: {}".format(Prices_Paperback[-1]))
	print(" ")
Price_Minimum = 100000.00
for Price in Prices_Paperback:
	if (Price!=None):
		if (Price < Price_Minimum):
			Price_Minimum = Price
Index_Price_Minimum = Prices_Paperback.index(Price_Minimum)
print("--------------------------------------------------------------------")

## Output Making
Output1 = {}
for Index in range(0, Length):
	Output1[Books[Index]] = Authors[Index]
Output2 = {Books[Index_Price_Minimum]:Prices_Paperback[Index_Price_Minimum]}
print("Output1:")
print(Output1)
print("")
print("Output2:")
print(Output2)