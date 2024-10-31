from flask import Flask, render_template
from bs4 import BeautifulSoup
import requests
import math

app = Flask(__name__)

@app.route("/")
def home():
    searchTerm = "4080"
    url = f"https://www.data-systems.fi/?s={searchTerm}&post_type=product"
    result = requests.get(url).text
    doc = BeautifulSoup(result, "html.parser")
    # Display the search result amount
    searchResultAmountText = doc.find('p', class_="woocommerce-result-count").text
    # Extract the number of search hits from the search result
    searchHits = float(str(searchResultAmountText).split("/")[-1])
    # Calculate the number of pages to scrape
    pages = math.ceil(searchHits / 20)

    
    productsFound = []

    # Browse through all the pages and extract the product information
    for page in range(1, pages+1):
        url = f"https://www.data-systems.fi/page/{page}/?s={searchTerm}&post_type=product"
        page = requests.get(url).text
        doc = BeautifulSoup(page, "html.parser")
        productList = doc.find('ul', class_="products columns-4")
        products = productList.findAll('a', class_="woocommerce-LoopProduct-link woocommerce-loop-product__link")
        
        for product in products:
            productImage = product.find('img', class_="attachment-woocommerce_thumbnail size-woocommerce_thumbnail")
            if productImage:
                productImage = productImage['src']
            else:
                productImage = "https://www.data-systems.fi/wp-content/uploads/2021/03/DS-Logo-1.png"
            productTitle = product.find('h2', class_="woocommerce-loop-product__title").text
            productLink = product['href']
            productPrice = product.find('span', class_="price").text
            productInfo = {"productTitle": productTitle, "productImage": productImage, "link": productLink, "price": productPrice}
            productsFound.append(productInfo)

    return render_template("index.html", productsFound=productsFound)

if __name__ == "__main__":
    app.run(debug=True)