#introduction.
"""
This bot is created by Fierylion on 8/7/2022.
It is intended to have automatic control over instagram account.
It can be used to automatically send messages to various people on instagram.
Follow me on instagram @fierylion1.
"""
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import sys,os,logging, pyinputplus as pyip, pyperclip, shelve, time

#TODO
#Assign a specific file in a specific folder for usernames and message to text with. This will be done by setup function
logging.basicConfig(level="DEBUG", format=r"%(asctime)s--%(levelname)s--%(message)s")
logging.disable(logging.DEBUG)  #To see the log message comment this...line
class instagram_bot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.progRun()
    def initial_setup(self):
        #This is an initial setup for long term use.
        username_message_path = pyip.inputFilepath(prompt="Please enter folder_path containing username file and message file: ", blockRegexes=[(r"\.\w+$", "Please enter file path in a format: .../dir and not../file: ")])
        try:
            os.makedirs("file_path")
        except FileExistsError:
            logging.info("created the shelve file")
        except PermissionError:
            print("Please create a folder and name it: file_path, Place it where this py file is placed.")
        except Exception as exc:
            print("There is a problem:  ")
            logging.error("shelve folder not created due to the following error: %s" %exc)
        shelve_obj = shelve.open("file_path")
        shelve_obj["path"] = username_message_path
        shelve_obj.close()
    def username_message(self):
        shelve_obj = shelve.open("file_path")
        path = Path(shelve_obj["path"])
        #check files in path are correct.
        files = os.listdir(path)
        if len(files) != 2:
            print("You should create only two files in %s" %path)
            sys.exit()
        try:
            assert ("username.txt" in files) and ("message.txt" in files)
        except:
            print("Please ensure that one of the file is username.txt and the other is message.txt in %s. " %path)
            sys.exit()
        logging.info("file names verified.")
        #file path is correct.
        with open(path/"username.txt", "r+") as username_file:
            usernames = username_file.read()
            username_file.write("")
        user_names = usernames.split()
        with open(path/"message.txt", "r+") as message_file:
            message = message_file.read()
            message_file.write("")
        if len(sys.argv) >1:
            user_names = [sys.argv[1]]
        if len(user_names) == 0:
            print("No user_name was provided: Provide username through username file in path %s" %path)
            sys.exit()
        if len(message) == 0:
            message = pyperclip.paste()
            if len(message) == 0:
                print("No message to send. Please provide message in the message file...")
                logging.info("No message provided")
                sys.exit()
        logging.info("Successfull provided details.")
        return {"username": user_names, "message": message}

    """
    Below method can be used to obtain random love messages from a the site provided: 
    You can uncomment  and modify the progRun method to use it
    """

    # def random_message_generator(self):
    #     random_website = r"https://www.romanticlovemessages.com/random/"
    #     driver  = webdriver.Chrome()
    #     driver.get(random_website)
    #     category = driver.find_element(By.CSS_SELECTOR, "#smaller > a")
    #     while category.text.lower() not in ["romantic messages", "romantic love poems", "love messages for her"]:
    #         driver.refresh()
    #         category = driver.find_element(By.CSS_SELECTOR, "#smaller > a")
    #     message = driver.find_element(By.CSS_SELECTOR, "#random").text
    #     driver.close()
    #     return message
    def message_sender(self, user, mes):
        website = "https://www.instagram.com/"
        driver = webdriver.Chrome()
        driver.get(website)
        #sign in
        driver.implicitly_wait(30)
        username = driver.find_element(By.CSS_SELECTOR, "#loginForm > div > div:nth-child(1) > div > label > input")
        username.send_keys(self.username)
        password = driver.find_element(By.CSS_SELECTOR, "#loginForm > div > div:nth-child(2) > div > label > input")
        password.send_keys(self.password)
        password.send_keys(Keys.ENTER)
        dm = driver.find_element(By.CSS_SELECTOR, "#react-root > section > nav > div._8MQSO.Cx7Bp > div > div > div.ctQZg.KtFt3 > div > div:nth-child(2) > a")
        try:
            dm.click()
        except:
            print("Provided details arent correct: ")
            sys.exit()
        notification = driver.find_element(By.CSS_SELECTOR, "._a9--._a9_1")  # Turn on notification instagram alert
        WebDriverWait(driver, 10).until(expected_conditions.element_to_be_clickable(notification))
        notification.click()  #click message icon..

        search = driver.find_element(By.CSS_SELECTOR, "._aauy")  #search box

        for i in user:               #users provided in the list
            search.send_keys(i)
            name = driver.find_element(By.CSS_SELECTOR, "._aacl._aaco._aacw._adda._aacx._aad6")
            name.click()
            time.sleep(2)
            driver.find_element(By.CSS_SELECTOR, "._aacl._aaco._aacw._adda._aacx._aada._aade").click()
            text = driver.find_element(By.CSS_SELECTOR,"textarea")
            text.send_keys(mes)   #type message
            text.send_keys(Keys.ENTER)
            time.sleep(1)
            send = driver.find_element(By.CSS_SELECTOR, "._acan._acao._acas")
            send.click()         #send message
            time.sleep(2)

        print("done")
    def progRun(self):
        shelve_obj = shelve.open("file_path")
        try:
            shelve_obj["path"]
        except:
            self.initial_setup()
        else:
            data = self.username_message()
            user = data["username"]
            mess = data["message"]
            self.message_sender(user, mess)
username = pyip.inputStr("Please input your instagram username:  ")
password = pyip.inputStr("Please input your instagram password: ")
instagram_bot(username, password)

















