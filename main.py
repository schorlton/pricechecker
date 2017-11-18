from google.appengine.api import mail
from bs4 import BeautifulSoup
import requests
import webapp2

from formdata import FORM_DATA
from contact import EMAIL_SENDER, EMAIL_RECIPIENT

def send_price_alert(price):
    # mail.send_mail(
    #     to=EMAIL_RECIPIENT,
    #     subject='HeliJet Price Alert',
    #     sender=EMAIL_SENDER,
    #     body='There are flights available for ${}'.format(price)
    # )
    print('would have sent price alert for {}'.format(price))

class PriceCheck(webapp2.RequestHandler):
    def get(self):
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'text/html',
            'Cookie': 'ASP.NET_SessionId=umrvj4t0np4c01rt14lcpxz0; CookieValidation=yes'
        }
        r = requests.post('https://bookings.blueskybooking.com/Booking.aspx?Company_ID=54', headers=headers, data=FORM_DATA)
        soup = BeautifulSoup(r.text.encode('utf-8'), 'html.parser')
        price_as = soup.find_all('a', {'class': 'ui-link-global-schedules-dialog-fare'})
        prices = []
        for price_a in price_as:
            prices.append(float(price_a.find('span').text[1:]))
        min_price = min(prices)
        if min_price < 400:
            send_price_alert(min_price)

app = webapp2.WSGIApplication([
    ('/pricecheck', PriceCheck),
])
