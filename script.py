from urllib.parse import quote_plus

import requests
from bs4 import BeautifulSoup


def scrape_fravega(code):

    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    fravega_url = f"https://www.fravega.com/p/--{code}"
    r = requests.get(fravega_url, headers=HEADERS)
    soup = BeautifulSoup(r.content, "lxml")

    product_name = soup.find("h1", {"data-test-id": "product-title"})
    product_name = product_name.text.strip() if product_name else "N/A"

    # Extract brand
    brand = soup.find("h2", class_="brand-title")
    brand = brand.text.strip() if brand else "N/A"

    # Extract both prices (original and discounted)
    price_wrapper = soup.find("div", {"data-test-id": "price-wrapper"})

    if price_wrapper:
        price_span = price_wrapper.find_all("span")
        prices = [
            span.text.strip()
            for span in price_span
            if span.text.strip() and "$" in span.text
        ]
    search_query = quote_plus(brand + " " + product_name)
    search_query_d = brand + " " + product_name

    ml_search_url = (
        f"https://listado.mercadolibre.com.ar/{search_query}#D[A:{search_query_d}]"
    )
    prices_int = [
        float(s.replace("$", "").replace(".", "").replace(",", ".")) for s in prices
    ]

    return {
        "Product Name": product_name,
        "Brand": brand,
        "Original Price": min(prices_int),
        "Mercadolibre_url": ml_search_url,
    }


if __name__ == "__main__":
    scrape_fravega("20027482")
    print(scrape_fravega("20027482"))
