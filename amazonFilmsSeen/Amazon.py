from HTMLParser import HTMLParser
import cookielib
import mechanize
import re

class LinkParser(HTMLParser):                  # parse movie names with HTMLParser

    breakfound = False # if True, means next tag contains movie name
    filmnamefound = False # tag contains movie name
    flag = False  # if True, list items (movie names) were found on the page

    def handle_starttag(self, tag, attrs):

        if tag == 'b':   # checks if next tag contains movie name
            for (key, value) in attrs:
                if "iyrListItemTitle" in value:
                    self.breakfound = True

        if tag == 'a':   # checks if this tag contains movie name
            if self.breakfound:
                self.filmnamefound = True
                self.breakfound = False

    def handle_data(self, data):
        if self.filmnamefound:
            print data  # fetches movie name
            self.filmnamefound = False
            self.flag = True

    def filmonpage(self):  # checks if there is anything on page
        if self.flag:
            return True

br = mechanize.Browser()                         # log into Amazon using mechanize

cookiejar = cookielib.LWPCookieJar()
br.set_cookiejar( cookiejar )

br.set_handle_equiv( True )
br.set_handle_gzip( True )
br.set_handle_redirect( True )
br.set_handle_referer( True )
br.set_handle_robots( False )

br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

br.addheaders = [('User-agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11'),
                 ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
                 ('Accept-Encoding', 'gzip,deflate,sdch'),
                 ('Accept-Language', 'en-US,en;q=0.8'),
                 ('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.3')]

country = raw_input("Please enter the end of the country-specific Amazon domain you use. (e.g. if you use 'amazon.de', enter 'de', if you use 'amazon.com', enter 'com' etc.):  ")
sign_in = br.open("https://www.amazon." + country + "/gp/sign-in.html")
br.select_form(name="signIn")
br["email"] = raw_input("Please enter the email you have registered with in Amazon (without the 'www.', of course):  ").encode("utf-8")
br["password"] = raw_input("Please enter your Amazon password:  ")
logged_in = br.submit()
                                               # log-in finished
min = 1        # Amazons pages always have 15 items in them
max = 15

while True:                                    # iterates through the pages
    web = br.open("https://www.amazon." + country + "/gp/yourstore/iyr/ref=pd_ys_iyr_prev?ie=UTF8&collection=watched&iyrGroup=&maxItem=" + str(max) + "&minItem=" + str(min))
    web = re.sub(r'<(script).*?</\1>(?s)', '', web.get_data(), flags=re.MULTILINE)
    web = re.sub(r'(<!.*>)', "", web, flags=re.MULTILINE)
    parse = LinkParser()
    parse.feed(web)
    if not parse.filmonpage(): # checks if last page
        break
    min += 15
    max += 15