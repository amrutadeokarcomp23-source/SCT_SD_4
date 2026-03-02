from flask import Flask, render_template, request
from scraper import scrape_amazon
import pandas as pd

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    products = []

    if request.method == "POST":
        search_query = request.form["search"]
        products = scrape_amazon(search_query)

        # Save CSV
        df = pd.DataFrame(products)
        df.to_csv("amazon_products.csv", index=False)

    return render_template("index.html", products=products)

if __name__ == "__main__":
    app.run(debug=True)
