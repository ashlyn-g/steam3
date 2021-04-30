from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from decimal import *
import mysql.connector
#mydb = mysql.connector.connect(
 #   host='localhost',
 #   user='root',
#    passwd='M017360827648DB',
#    database='tf2itemsdb'
#)
#mycursor = mydb.cursor(buffered=True)

#mycursor.execute("SHOW TABLES")

#sqlFormula = "INSERT INTO iteminfo (name, id, game) VALUES (%s, %s, %s)"

#item1 = ["Mann Co. Supply Crate Key", 1, "TF2"]

#mycursor.execute(sqlFormula, item1)

#mydb.commit()

#getting rid of popups
#driver = webdriver.Chrome()
def OpenChrome():
    chrome_options = webdriver.ChromeOptions()

    prefs = {"profile.default_content_setting_values.notifications" : 2}

    chrome_options.add_experimental_option("prefs",prefs)

    driver = webdriver.Chrome(options=chrome_options)

    executor_url = driver.command_executor._url
    session_id = driver.session_id

    print(session_id)
    print(executor_url)
    return driver

#driver = OpenChrome()
#print("Opened Chrome")
def create_driver_session(session_id, executor_url):
    from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver

    # Save the original function, so we can revert our patch
    org_command_execute = RemoteWebDriver.execute

    def new_command_execute(self, command, params=None):
        if command == "newSession":
            # Mock the response
            return {'success': 0, 'value': None, 'sessionId': session_id}
        else:
            return org_command_execute(self, command, params)

    # Patch the function before creating the driver object
    RemoteWebDriver.execute = new_command_execute

    new_driver = webdriver.Remote(command_executor=executor_url, desired_capabilities={})
    new_driver.session_id = session_id

    # Replace the patched function with original function
    RemoteWebDriver.execute = org_command_execute

    return new_driver

executor_url = ''
session_id = ''

driver2 = create_driver_session(session_id, executor_url)
print(driver2.current_url)

#Messages
commandslist = ["!trade - Opens a trade session with the user and bot", "!gift - Allows the user to send the bot an item. Used primarily for debugging",
               "!inventory - Sends the user a list of items with prices, # of each item, and the corresponding ID.",
               "!help - Displays this message again."
               "!remove - Bot will immediately remove the user from its friends list"]
welcometext = ['Hi, I am a python trading bot. Here are some commands you can use to communicate with me:'] + commandslist

inventory = []



#links
steamchat = "https://steamcommunity.com/chat/"
steamauthgen = "https://scholtz.me/steam-auth-web-util/"
steaminvites = "https://steamcommunity.com/profiles/76561199059315772/friends/pending"
steamfriends = "https://steamcommunity.com/profiles/76561199059315772/friends"
steaminventory = 'https://steamcommunity.com/profiles/76561199059315772/inventory/'
steamgroupinvites = 'https://steamcommunity.com/profiles/76561199059315772/groups/pending'

# Log in to steam
def steamlogin(driver):
    driver.get(steamchat)
    steamAccountName = driver.find_element_by_id('steamAccountName')
    steamAccountName.send_keys("") # Put Steam Username here
    steamAccountName.send_keys(Keys.RETURN)

    steamPassword = driver.find_element_by_id('steamPassword')
    steamPassword.send_keys("") # Put Steam Password here
    steamPassword.send_keys(Keys.RETURN)

    #time.sleep(5)
    shared_secret = ''

    #Authenticator open and grab code
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get(steamauthgen)
    getcode = driver.find_element_by_name('shared-secret')
    getcode.send_keys(shared_secret)
    time.sleep(1)
    authcode = driver.find_element_by_xpath("//div[@class='output']/span[1]")
    SteamGuardCode = authcode.text
    driver.close()
    #Finish Login
    driver.switch_to.window(driver.window_handles[0])
    twofactorcode_entry = driver.find_element_by_id('twofactorcode_entry')
    twofactorcode_entry.send_keys(SteamGuardCode)
    twofactorcode_entry.send_keys(Keys.RETURN)
    time.sleep(7)
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get(steaminvites)
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[2])
    driver.get(steamfriends)
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[3])
    driver.get(steaminventory)

def addcurrency():
    ref = Decimal('1')
    key = Decimal('51.94')
    rec = Decimal('0.33')
    scrap = Decimal('0.11')
    weapons = Decimal('0.05')
    #we'll probably take a list as an input, use a database to find the values of the inserted items and to check their validity, and then add the value
    pass

class currency:
    ref = Decimal('1')
    key = Decimal('51.94')
    rec = Decimal('0.33')
    scrap = Decimal('0.11')
    weapons = Decimal('0.05')
    #(0.99 'ref') = 1
    #now we need to interpret these...

    def __init__(self, value, type):
        self.v = Decimal(value)
        self.t = type

#should add a function here to get all pure from inventory and then have each function check if it can use items from list

#need to add a function somewhere to give change as well

    def weaponfunc(self):
        if self.v >= self.weapons:
            # we need at least one weapon
            num_weapons_r = (self.v % self.weapons)
            num_weapons = ((self.v - num_weapons_r) / self.weapons)
            print(str(num_weapons) + " weapons")
            self.v -= (num_weapons * self.weapons)
           # weaponstart = currency(self.v)
           # weaponstart.weapon()
            print("Done")
        else:
            print("Done")
           # weaponstart = currency(self.v)
          #  weaponstart.weapon()

    def scrapfunc(self):
        if self.v >= self.scrap:
            # we know we need at least one scrap
            num_scrap_r = (self.v % self.scrap)
            num_scrap = ((self.v - num_scrap_r) / self.scrap)
            print(str(num_scrap) + " scrap")
            self.v -= (num_scrap * (self.scrap))
            weaponstart = currency(self.v, self.t)
            weaponstart.weaponfunc()
        else:
            weaponstart = currency(self.v, self.t)
            weaponstart.weaponfunc()
    def recfunc(self):
        if self.v >= self.rec:
            # we know we need at least one rec
            num_rec_r = (self.v % self.rec)
            num_rec = ((self.v - num_rec_r) / self.rec)
            print(str(num_rec) + " rec")
            self.v -= (num_rec * (self.rec))
            scrapstart = currency(self.v, self.t)
            scrapstart.scrapfunc()
        else:
            scrapstart = currency(self.v, self.t)
            scrapstart.scrapfunc()

    def reffunc(self):
        # determine number of refined metal for action
        if self.v >= self.ref:
            # we know we need at least one ref to express this value
            num_ref_r = (self.v % self.ref)
            num_ref = ((self.v - num_ref_r) / self.ref)
            print(str(num_ref) + " ref")
            self.v -= num_ref
            # we can move on to the next value
            recstart = currency(self.v, self.t)
            recstart.recfunc()
        else:
        # we can move on to the next value
            recstart = currency(self.v, self.t)
            recstart.recfunc()


    def convertkeystoref(self):
        #we need to convert the number of keys to ref for this
        #check to make sure that we have more key value that needs conversion
        if self.v >= 0.0001:
            #now we convert:
            v1 = (self.key * self.v)
            newv = round(v1, 2)
            print(newv)
            refstart = currency(newv, self.t)
            refstart.reffunc()
        else:
            print('Done')

    def keyfunc(self):
        #interpretting number of keys
        if self.v >= 1:
            # we know we need at least one key to express this value
            num_keys_r = (self.v % 1)
            num_keys = ((self.v - num_keys_r) / 1)
            print(str(num_keys) + " keys")
            self.v -= num_keys
            # we can move on to the next value
            convert = currency(self.v, self.t)
            convert.convertkeystoref()
        else:
        # we can move on to the next value
            convert = currency(self.v, self.t)
            convert.convertkeystoref()

    def interpretcurrency(self):
        #this is where we determine the type of currency and then redirect it so its cost can be appropriately determined
        if self.t == 'keys':
            print("Currency is keys")
            keystart = currency(self.v, self.t)
            keystart.keyfunc()
        elif self.t == 'ref':
            print("Currency is ref")
            print(self.v)
            refstart = currency(self.v, self.t)
            refstart.reffunc()

        else:
            print("Error: Currency type not recognized")

class itemchecker:
    def __init__(self, name, game, id, priceb, prices, idcustom, itemtype, pure, quality, craftable):
        #this is our master info about item

        #primary distinguishing features - check these first
        self.name = name
        self.game = game
        #TF2 = 440

        #ids on record V - may need a list
        self.id = id


        self.quality = quality
        #maybe this could be a simple true or false
        self.craftable = craftable

        #stuff i'll need to edit

        #these I likely won't get an input for; i'll need to add them myself. they still need a column though

        self.priceb = priceb
        #price to buy at
        self.prices = prices
        #price to sell at


        #bp.tf suggested and possibly an estimate for current pricing???
        #would probably be a separate bot that gives this input.

        self.itemtype = itemtype

        # maybe this could be a simple true or false
        self.pure = pure
        #need to generate a custom code for each new item type but doesn't have to be edited manually. this will not be an input
        self.idcustom = idcustom

    def checkiteminfodb(self):
        #we get the info for the item. if info not found, we add to db
        #we also check if item id is new. if it is new we add that to db even if main item is already in db
        pass

    def additemtodb(self):
        #we add info to db
        pass


class inventoryitems:
    def __init__(self, name, game, id):
        self.name = name
        self.game = game
        self.id = id
        self.number = 0

    def addtoinventorylist(self):
        #we're checking to make sure an identical item does not already exist in this list

        #we can add the item to our db here - check to make sure one is not already in db
        #need date/time for inv db
        #find a way to check for items that are no longer in inv - we could clear the db every time but that would mess up the timestamps I want for each item
        #clear these items from db

        for items in inventory:
            print(items)
            if items == self.name:
                print("Item is already in list!")
                #add the number - this will keep track of the number of items per type in our inv so we don't print dupes
                self.number += 1
        else:
            print("Item does not appear in list")
            #we're adding a 1 since self.number starts at zero. this number will be what we print as the quantity of items
            self.number += 1
            #adding item to our list to print
            additemstoinv = inventoryitems(self.name, self.game, self.id)
            additemstoinv.itemprint()
    def itemprint(self):
        itemstats = (str(self.game) + " " + str(self.name) + " - " + str(self.number))
        print(itemstats)
        inventory.append(itemstats)
        #we will use the above list for printing purposes only.


def getinventory(driver):
    inventory.clear()
    driver.switch_to.window(driver.window_handles[3])
    time.sleep(5)
    iteminfo = driver.find_elements_by_css_selector('.itemHolder > div')
    #finding all items in inventory
    itemcount = 0
    for item in iteminfo:
        itemid = item.get_attribute("id")
        try:
            int(itemid)
            itemcount += 1
            print(itemcount)
            while itemid.startswith('440'):
                #Item is from TF2
                itemclass = item.get_attribute('class')
                if 'activeInfo' in itemclass:
                    rightinfo = driver.find_element_by_id('iteminfo1_item_name')
                    itemname = rightinfo.text
                    mainiteminfo = ("Item #" + str(itemcount) + ": " + itemname)
                    print(mainiteminfo)
                    additemstoinv = inventoryitems(itemname, 'TF2', itemid)
                    additemstoinv.addtoinventorylist()
                    #we need to add this to our inventory database
                    #we also need to check if this item is in our big database and add it if it isn't
                    break
                else:
                    print('Item is inactive')
                    item.click()
                    item.click()
                    print("Clicked item")
            else:
                print("Game of item is not valid")
        except ValueError:
            print('Value Error Occurred')
            #some string types share this id. this exception prevents the program from breaking when a string has the same id while also filtering out anything that isn't an int
    pass


def removefriends(driver, number=None, name=None):
    driver.switch_to.window(driver.window_handles[2])
    managefriends = driver.find_element_by_id('manage_friends_control')
    managefriends.click()
    friendbox = driver.find_element_by_id("search_results")
    print("Tag1")
    if name == None:
        #this means we're removing excess friends without anyone specific in mind
        desired = 150
        #how many friends we will need to remove to get to desired amount
        removecount = number - desired

        pass
    else:
        print("tag2")
        friendtoremove = friendbox.find_element_by_css_selector('div[data-search="' + str(name) + ' ; "]')
        print(friendtoremove.text)
        time.sleep(5)
        removingfriend = friendtoremove.find_element_by_class_name('selectable_overlay')

        removingfriend.click()
        print("Tag3")
        clickremove = driver.find_element_by_css_selector("""span[onclick="ExecFriendAction('remove', 'friends/all')"]""")
        clickremove.click()
        print("Tag4")
        #we're removing one specific friend at their request

    pass

def checkfriendcount(driver):
    driver.switch_to.window(driver.window_handles[1])
    max = 250
    above = 200
    friendcount = driver.find_element_by_id('menu_friends_ct')
    print(friendcount.text)
    if friendcount.text >= above:
        removefriends(driver,friendcount)


def sendtradeoffer(driver, friendname):
    #sends a trade offer to a given user. this function will not work for a while until steam guard has been active for 15 days
    #driver.switch_to.window(driver.window_handles[0])
    pass

def readmsg(driver, friendname):
    driver.switch_to.window(driver.window_handles[0])
    chatwindows = driver.find_elements_by_css_selector('div.DropTarget.chatWindow.MultiUserChat')
    for chats in chatwindows:
        try:
            attributes = chats.get_attribute('data-activechat')
            if attributes == "true":
                print("Active Chat Found")
                chathistory = chats.find_element_by_css_selector('div.chatHistory')
                message_blocks = chathistory.find_elements_by_css_selector('div[class*="ChatMessageBlock"]')
                for newestblock in message_blocks:
                    if newestblock == message_blocks[-1]:
                        print("Newest message block/item is found")
                        messages = newestblock.find_elements_by_css_selector('span')
                        for messagetoread in messages:
                            if messagetoread == messages[-1]:
                                message = messagetoread.text
                                print("Newest message found")
                                if message == "!trade":
                                    print("Message is !trade")
                                    findchatfriend(driver, "0", friendname, 'tradeoffer')
                                elif message == "!gift":
                                    print("Message is !gift")
                                    findchatfriend(driver, "0", friendname, 'tradeoffer')
                                elif message == "!help":
                                    print("Message is !help")
                                    findchatfriend(driver, welcometext, friendname, 'sendmessage')
                                elif message == "!inventory":
                                    print("Message is !inventory")
                                    findchatfriend(driver, inventory, friendname, 'sendmessage')
                                elif message == "!remove":
                                    print("Message is !remove")
                                    removefriends(driver, friendname)
                                else:
                                    messagetoreply = ("You entered: " + '"' + str(message) + '"' + " This command is not recognized. Please try again or type !help if you need a list of commands.")
                                    print(messagetoreply)
                                    findchatfriend(driver, messagetoreply, friendname, 'sendmessage')
        except StaleElementReferenceException:
            print("No active chat")
            continue


def findunreadmsg(driver):
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(5)
    tabslist = driver.find_elements_by_class_name('chattabs_ChatTab_1WfqA.no-drag')
    try1 = 0
    while True:
        for tabs in tabslist:
            try:
                tabs.find_element_by_class_name('chattabs_UnreadGlow_30PFd')
                findname = tabs.find_element_by_class_name('personanameandstatus_playerName_1uxaf')
                name = findname.text
                tabs.click()
                #read and send a message
                readmsg(driver, name)
            except NoSuchElementException:
                print("There was an exception")
                continue
        else:
            findchatfriend(driver, "0", 'ash_minty', 'openchatbox')
            if try1 == 1:
                print("No unread message found")
                break
            try1 = 1


def opengroups(driver, message, friendname, function):
#if they are offline, we need to find them in the group
    findGroups = driver.find_elements_by_class_name("ExpandPlusMinus")
    for Closedgroups in findGroups:
        Closedgroups.click()
    print("Opened groups to look for friend")
    time.sleep(3)
    findchatfriend(driver, message, friendname, function)




    #finding a friend in the chat menu
def findchatfriend(driver, message, friendname, function):
    driver.switch_to.window(driver.window_handles[0])
    #Finding the friend and opening their chat/trade
    try:
        friendcontainer = driver.find_element_by_xpath("//*[@id='friendslist-container']/div/div[3]/div[1]/div/div[2]/div[3]/div")
        friendincontainer = friendcontainer.find_element_by_xpath(".//div[contains(text(),'" + str(friendname) + "')]//following-sibling::div[@class = 'ContextMenuButton']")
        friendincontainer.click()
        time.sleep(1)
        # dropdown to send message, opens chat
        if function == 'sendmessage':
            print("Tag6")
            send = driver.find_element_by_xpath('//*[text()="Send Message"]')
            send.click()
            sendamessage(driver, message, friendname)
        elif function == 'tradeoffer':
            trademenu = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[text()="Trading"]')))
            ActionChains(driver).move_to_element(trademenu).perform()
            sendtrade = driver.find_element_by_xpath('//*[text()="Send a Trade Offer"]')
            sendtrade.click()
            sendtradeoffer(driver, friendname)
        elif function == 'openchatbox':
            send = driver.find_element_by_xpath('//*[text()="Send Message"]')
            send.click()
    except NoSuchElementException:
        #send to a function to open all the groups
        print("Friend not found")
        opengroups(driver, message, friendname, function)




def sendamessage(driver, message, friendname):
    #finds the chatbox and sends the message
    typemessage = driver.find_element_by_xpath(
        '//*[@id="friendslist-container"]/div/div[3]/div[3]/div[2]/div/div[4]/div/div/div/div/div/div/div[2]/div[2]/form/textarea')
    typemessage.click()
    if isinstance(message, str):
        typemessage.send_keys(message)
        typemessage.send_keys(Keys.RETURN)
    else:
        if message == inventory:
            getinventory(driver)
            print("Got inventory")
        for lines in message:
            typemessage.send_keys(lines)
            typemessage.send_keys(Keys.CONTROL, Keys.RETURN)
        else:
            typemessage.send_keys(Keys.RETURN)




def acceptfriends(driver):
    driver.switch_to.window(driver.window_handles[1])
    print("hi")
    invitelist = driver.find_elements_by_xpath("//*[contains(@id, 'invite_')]")
    print(invitelist)
    for invites in invitelist:
        invites.find_element_by_xpath(".//span[contains(text(),'Accept')]").click()
        name = invites.get_attribute('data-persona')
        print(name)
        print("Friend Accepted")
        findchatfriend(driver, welcometext, name, 'sendmessage')
        #need to test with multiple invites
    else:
        if len(invitelist) == 0:
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[4])
            driver.get(steamgroupinvites)
            ignoregroups = driver.find_elements_by_css_selector('.invite_action_text:contains("Ignore")')
            for groups in ignoregroups:
                groups.click()
                print("Ignored a group")
            #check groups



def listen(driver):
    print("Tag1")
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(1)
    notificationpopup = driver.find_element_by_xpath('/html/body/div[1]/div[7]/div[1]/div/div[3]/div/div[2]/div[1]')
    print(notificationpopup.text)
    if int(notificationpopup.text) != 0:
        notificationpopup.click()
        #respond to notification
        #findnotification = driver.find_element_by_xpath('//*[@id="header_notification_dropdown"]/div/a[5]/span[3]/span')

        comments = driver.find_element_by_css_selector('.popup_menu_item.notification_ctn.header_notification_comments')
        value_comments1 = comments.find_element_by_css_selector('.notification_count')#.text
        value_comments = value_comments1.text

        items = driver.find_element_by_css_selector('.popup_menu_item.notification_ctn.header_notification_items')
        value_items1 = items.find_element_by_css_selector('.notification_count')#.text
        value_items = value_items1.text

        invites = driver.find_element_by_css_selector('.popup_menu_item.notification_ctn.header_notification_invites')
        value_invites1 = invites.find_element_by_css_selector('.notification_count')#.text
        value_invites = value_invites1.text

        gifts = driver.find_element_by_css_selector('.popup_menu_item.notification_ctn.header_notification_gifts')
        value_gifts1 = gifts.find_element_by_css_selector('.notification_count')#.text
        value_gifts = value_gifts1.text

        offlinemessages = driver.find_element_by_css_selector('.popup_menu_item.notification_ctn.header_notification_offlinemessages')
        value_offlinemessages1 = offlinemessages.find_element_by_css_selector('.notification_count')#.text
        value_offlinemessages = value_offlinemessages1.text

        print(comments)
        print(items)
        print(invites)
        print(gifts)
        print(offlinemessages.text)

        #value = findnotification.text
        if value_comments != "0":
            print("Notification is an unread comment")
            #send email or steam msg, clear notification

        elif value_items != "0":
            print("Notification is a new item")
            #clear notification

        elif value_invites != "0":
            print("Notification is an invite")
            acceptfriends(driver)

        elif value_gifts != "0":
            #probably have it send me an email or steam message?

            print("Notification is a gift")
        elif value_offlinemessages != "0":
            print("Notification is an unread chat message")
            findunreadmsg(driver)
            #sends to a function to find the unread message, read it, form a response, and send it
#testiditems(driver2)
#steamlogin(driver)
#findchatfriend(driver2, welcometext, 'ash_minty')
#acceptfriends(driver)
listen(driver2)
#readmsg(driver2)
#driver.switch_to.window(driver.window_handles[0])
#findunreadmsg(driver2)
#findchatfriend(driver2, welcometext, 'ash_minty', 'tradeoffer')
#checkfriendcount(driver2)
#sendamessage(driver, welcometest)
#removefriends(driver2, "ash_minty")
#testvalue = currency('3.6', 'keys')
#testvalue.interpretcurrency()
#secrets = {
   # 'key' : "1o5ihSVwz4kQqIoLZo4iWWwvjcY="
#}
#sa = SteamAuthenticator(secrets)
#sa.get_code()
#print(sa.get_code())

#SteamGuardCode = (c)
#print(str(cheese()) + "cheesey")
#twofactorcode_entry = driver.find_element_by_id('twofactorcode_entry')
#twofactorcode_entry.send_keys(SteamGuardCode)
#twofactorcode_entry.send_keys(Keys.RETURN)
