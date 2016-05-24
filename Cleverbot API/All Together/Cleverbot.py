
#
# Cleverbot Webscraping API for Python
#
# Made By: Ryan Beltran
#
# On: March 30th 2016
#
# Version history:
#    1.0  3/30/16
#
# Todo list:
#    * Disguise traffic as human
#    * Make ask() more resilient to changes in site structure
#    * Add reset operation by clearing CBSTATE cookie
#    * Save sessions by storing raw CBSTATE's (and perhaps SESSIONIDs; experimentation needed)
#    * Filter inappropriate responces
#    * Filter self advertisements from Cleverbot
#    * Further optimize the ask() function
#

#
# Disclaimer
#
# Please use webscrapers responcibly and practice fair and legal discression when deciding on how and if a scraper should be used.
# Under precedent from previous court cases including 'Ebay V. Bidders Edge', the use of a web scraper in ways that interfere with the host's intersts may (possibly) be considered illegal trespass.
# Cleverbot does not openly grant site access to robots, or humans attempting to access the site indirectly, and infact statedly denies it.
# Writing this code is not in violation of anyone's Terms of Use. RUNNING this code may be in violation of somebody's Terms of Use.
# If cleverbot blocks you IP address as a result of your use of any of the following code, consider it a personal problem.
# Per my undrstanding, the only authorized ways of using Cleverbot are:
#       * To have a human interface their web application directly at www.cleverbot.com
#       * To pay a heck of a lot of money to use their cleverscript API
# Oh also one quick note, software should be free.
#

try:    # ~~~~ Aquire Dependencies ~~~~
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    import time, urllib
except:
    print "::Error 011 - Failure to load dependency (Selenium)"


            
class Cleverbot:

    # An automated webscraper for the cleverbot chat AI

    # Required Dependencies:
        # Selenium
        # Phantom JS
        # Firefox (for debugging only, firebug plugin recommended to view cookies)
        
    # As well as:
        # Python 2.x
        # and a stable internet conection
        

    # |---------------------------------------------|
    # |---------------------------------------------|
    # |           - - Error Codes - -               |
    # |---------------------------------------------|
    # |---------------------------------------------|
    # |                                             |
    # | ::Error 011 : Failure to load dependency    |
    # | ::Error 110 : Timeout - retrying            |
    # | ::Error 111 : Timeout - not retrying        |
    # | ::Error 211 : Failure to load web resource  |
    # |                                             |
    # | ::Failure 111 : Failure to answer prompt    |
    # |---------------------------------------------|
    # |---------------------------------------------|

    # Disable headless only for debugging

    def __init__(self, headless = True):
        
        try:
            if headless:
                self.driver = webdriver.PhantomJS('./phantomjs') # Load the phantom JS headless browser
                self.driver.set_window_size(1200, 600) # Needs a size, this is kinda arbitrary
            else:
                self.driver = webdriver.Firefox() # Load the firefox browser
        except:
            if headless:
                print "::Error 011 - Failure to load dependency (PhantomJS)"
            else:
                print "::Error 011 - Failure to load dependency (Firefox)"
        self.load()

        
    def load(self):

        try:
            self.driver.get("http://cleverbot.com/") # Load the cleverbot page
        except:

            print "::Error 211 : Failure to load resource" 


    def ask(self, question, maxretries = 8):
                 
        # Send the question
        self.driver.find_element_by_class_name('stimulus').send_keys(question) # Input field is named 'stimulus'
        time.sleep(0.1) # Just for safety
        self.driver.execute_script("cleverbot.sendAI()") # This is the JS that is run by the form's 'onsubmit()'

        # Wait for a responce
        for iteration in range(maxretries): # Keep trying, it can take a while sometimes
            try:
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "snipTextIcon"))) # An icon with a pair of sizzors will pop up when it is ready
                break
            except:
                if iteration < maxretries:
                    print "     ::Error 110 : Timeout - retrying "
                else:
                    print "     ::Error 111 : Timeout - not retrying (recurrent timeout limit exceeded) "
                    print "     ::Failure 111 : Failure to answer prompt"
                    return ""
        time.sleep(0.1)

        # Aquire and return responce 
        cookies = self.driver.get_cookies()                                     # Get cookies
        cbstate = [x[u'value'] for x in cookies if x['name'] == u'CBSTATE'][0]  # Full conversation is stored in the CBSTATE cookie
        return str(urllib.unquote(cbstate.replace('%20',' ').split('&')[-1]))   # Extract and format conversation


    def getConversation():
        
        cookies = self.driver.get_cookies()                                     # Get cookies
        cbstate = [x[u'value'] for x in cookies if x['name'] == u'CBSTATE'][0]  # Full conversation is stored in the CBSTATE cookie
        return str(urllib.unquote(cbstate.replace('%20',' ').split('&')[6:]))   # Extract and format conversation


    def quit(self):

        self.driver.quit() # Shutdown driver


# A brief testing example
def run_example(headless = True):
    
    cb = Cleverbot(headless)
    query = raw_input("Ask cleverbot: ")
    while query != "end":
        print cb.ask(query)
        query = raw_input("\nAsk cleverbot: ")
    cb.quit()

run_example()
