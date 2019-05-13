import urllib2
from bs4 import BeautifulSoup
from twilio.rest import Client

# Values needed for request.
requestUrl = 'https://www.cineplex.com/Movie/avengers-endgame'
userAgent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
requestHeader = {'User-Agent': userAgent}

# Twilio account vals
# These are empty strings on GitHub for security purposes.
accountSID = ''
authToken = ''
twilioPhoneNum = ''
recipientPhoneNum = ''

# html request to make soup, which returns the HTML webpage format
def getHTMLFromPage(url):
	try:
		req = urllib2.Request(url, headers=requestHeader)
		response = urllib2.urlopen(req)
	except urllib2.HTTPError, err:
		return -1
	else:
		html = response.read()
		soup = BeautifulSoup(html, 'html.parser')
        return soup

# Constructs Twilio account for sending the TICKETS ARE READY message
# SID and AuthToken from Twilio account
def sendMovieReadyMessage(message):
	client = Client(accountSID, authToken)
	client.messages.create(to=recipientPhoneNum, 
                            from_= twilioPhoneNum,
                    		body= message);

soup = getHTMLFromPage(requestUrl)

# Checking available tickets based on the no ticket window.
# That tag seems to be more reliable. I think because the tickets
# available widget class name is a prefix of the no tickets available
# class name. Still a bit shakey on reliability... There's probably a more
# elegant way to check this.
ticketPurchaseWindow = soup.find_all('div', attrs={"class":"md-qt-widget-container no-qt"})
if (len(ticketPurchaseWindow) == 0):
    message = '''
    DROP WHAT YOU'RE DOING!

    AVENGERS: ENDGAME TICKETS ARE AVAILABLE!!
    EXCELSIOR!
    '''
    sendMovieReadyMessage(message)
else:
    print("no tickets ready")
