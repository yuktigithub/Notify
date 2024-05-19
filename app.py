from flask import Flask, render_template, request
import smtplib
import requests
from bs4 import BeautifulSoup

NOTIFY_EMAIL = "pythonpractice094@gmail.com"
NOTIFY_PASSWORD = "pvpkjxjyoadyfpld"       # app password
IS_SUCCESSFUL = "False"

# HEADERS = {'User_Agent ': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"}
app = Flask(__name__)


def amazon_element(soup):
    element = soup.find(name="span", class_="a-price-whole").text.strip().replace(",", "").replace(".", "")

    return float(element)


def flipkart_element(soup):
    element = soup.find(name="div", class_="_30jeq3 _16Jk6d").text.strip().replace("₹", "").replace(",", "")
    return float(element)


def nykaa_element(soup):
    element = soup.find(name="span", class_="css-1jczs19")
    price = element.text.strip().replace("₹", "").replace(",", "")
    return float(price)


def amazon_title(soup):
    product_title = soup.find(name="span", id="productTitle").text.strip()
    return product_title


def flipkart_title(soup):
    product_title = soup.find(name="span", class_="B_NuCI").text.strip()
    return product_title


def nykaa_title(soup):
    product_title = soup.find(name="h1", class_="css-1gc4x7i").text.strip()
    return product_title


def success(m_url, m_email, m_price, site):

    response = requests.get(m_url)
    content = response.text
    m_price = float(m_price)
    soup = BeautifulSoup(content, 'html.parser')

    try:
        if site == "amazon":
            product_price = amazon_element(soup)
            product_title = amazon_title(soup)
        elif site == "flipkart":
            product_price = flipkart_element(soup)
            product_title = flipkart_title(soup)
        elif site == "nykaa":
            product_price = nykaa_element(soup)
            product_title = nykaa_title(soup)
        else:
            product_price = 0
            product_title = "SORRY! Not found."
        # element = soup.find(name="span", class_="a-price-whole").text.strip().replace(",", "").replace(".", "")
        # product_title = soup.find(name="span", id="productTitle").text.strip()
        difference = m_price - product_price
        if product_price <= m_price:
            print("Successful")
            # generated from app password fron the security of gmail
            with smtplib.SMTP("smtp.gmail.com") as connection:
                connection.starttls()
                connection.login(user=NOTIFY_EMAIL, password=NOTIFY_PASSWORD)
                connection.sendmail(
                    from_addr="pythonpractice094@gmail.com",
                    to_addrs=m_email,
                    msg='subject: Exciting News! Price Drop Alert on Your Desired Product 🚀\n\n'
                        f'Dear Valued Customer,\n'
                        f'We hope this email finds you well and excited for some '
                        f'fantastic news! We are thrilled to inform you that the '
                        f'price of your coveted product has dropped, making it the perfect time '
                        f'for you to make your purchase and fulfill your desires.\n\n'
                        f'Product: {product_title}\n'
                        f'Current Price: {product_price}\n'
                        f'Savings: {difference}\n\n'
                        'This remarkable price reduction comes as part of our commitment to offering you the best '
                        'deals and ensuring your satisfaction. We understand the importance of your preferences, '
                        'and that\'s why we\'ve taken this step to bring you closer to making this product yours.'
                        'Hesitate no more, as this offer is valid for a limited time only! '
                        'By clicking the link below, you\'ll be able to explore the product in more detail, '
                        'read customer reviews, and seize the opportunity to make your purchase at the newly discounted price.\n'
                        f'Click here to view the product and place your order\n{m_url} \n\n'
                        'Should you have any questions or require assistance, our dedicated customer support team is here to help. '
                        'Feel free to reach out to us via email at [pythonpractice094@gmail.com] or by phone at [ '
                        '6269498184].\n\n'
                        'Thank you for choosing us as your preferred shopping destination. '
                        'We look forward to serving you and making your shopping experience truly exceptional.\n'
                        'Happy shopping!\n'
                        'Best regards,\n'
                        'Team Notify! 🏹'
                )
                return "True"
        else:
            print("OOPS! Price not drop yet.")
            return "False"
    except:
        render_template("failed.html")


@app.route("/")
def home_page():
    return render_template("index.html")


@app.route("/amazon", methods =["GET", "POST"])
def amazon():
    A_VAR ="amazon"

    if request.method == "POST":

        PRODUCT_URL = request.form.get("url")
        EMAIL = request.form.get("mail")
        P_PRICE = request.form.get("price")
        success(PRODUCT_URL, EMAIL, P_PRICE, A_VAR)
        if success(PRODUCT_URL, EMAIL, P_PRICE, A_VAR) == "True":
               return render_template("success.html")
        else:
              return render_template("failed.html")
    return render_template("amazon.html")


@app.route("/flipkart", methods=["GET", "POST"])
def flipkart():
    F_VAR ="flipkart"
    if request.method == "POST":
        PRODUCT_URL = request.form.get("url")
        EMAIL = request.form.get("mail")
        P_PRICE = request.form.get("price")
        success(PRODUCT_URL, EMAIL, P_PRICE, F_VAR)
        if success(PRODUCT_URL, EMAIL, P_PRICE, F_VAR) == "True":
               return render_template("success.html")
        else:
              return render_template("failed.html")
    return render_template("flipkart.html")


@app.route("/nykaa", methods=["GET", "POST"])
def nykaa():
    N_VAR ="nykaa"
    if request.method == "POST":
        PRODUCT_URL = request.form.get("url")
        EMAIL = request.form.get("mail")
        P_PRICE = request.form.get("price")
        success(PRODUCT_URL, EMAIL, P_PRICE, N_VAR)
        if success(PRODUCT_URL, EMAIL, P_PRICE, N_VAR) == "True":
               return render_template("success.html")
        else:
              return render_template("failed.html")
    return render_template("nykaa.html")


@app.route("/result")
def final_page():
    IS_SUCCESSFUL = amazon()


if __name__ =="__main__":
    app.run(debug=True)