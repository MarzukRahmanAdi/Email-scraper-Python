from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import re
from bs4 import BeautifulSoup
import ssl
import smtplib
import requests
from dotenv import load_dotenv
import os

load_dotenv()


sent_emails = []
invalidEmails = []
link_extensions = ['']

f = open("emails.txt", "w")

def check_email(emails):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    regex2 = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$' 
    for email in emails:
        if(re.search(regex,email) or re.search(regex2, email)):  
            print("Valid Email")
            print("\t" + email)
            if email not in sent_emails:
                f.write(email + '\n')

                sent_emails.append(email)
            print(sent_emails)
            return True
            break
        else:
            print("Invalid Email")
            if len(email) <= 195:
                if(email in invalidEmails):
                    pass
                else:
                    invalidEmails.append(email)
                    f.write(email + "---------- Not Sure if this is a valid email \n")
                    print("\t" + email)
            else:
                pass

def validurl(link):
    for extension in link_extensions:
                try:
                    source = requests.get(link + extension, timeout=10)
                    soup = BeautifulSoup(source.text, 'lxml')
                    print(link[-1])
                    if link[-1] != "/":
                        link = link + "/"
                    print("Looking for emails in " + link + extension)
                    # Look for emails on the website

                    find_emails = soup.body.findAll(text=re.compile('@')) #instead of re.findall
                    check_email(find_emails)

                    if check_email(find_emails):
                        f.write(link + '\n')
                        f.write("\n \n")

                        break
                except:
                    pass


# Path of the chrome driver
PATH = my_variable = os.getenv("chromedriver_path")

driver = webdriver.Chrome(PATH)

start_count = ['0', '10', '20', '30', '40', '50', '60', '70', '80', '90', '100', '110', '120', '130', '140']

for num in start_count:
    driver.get("https://www.google.com/search?q=%22London%22+AND+%22UK%22+AND+%22Canada%22+-intitle%3A%22profiles%22+-inurl%3A%22dir%2F+%22+site%3Auk.linkedin.com%2Fin%2F+OR+site%3Auk.linkedin.com%2Fpub%2F+%22%40gmail.com%22&sxsrf=ALiCzsb9gt1ccBnmVxLya940UzOOQi5HBQ%3A1669476223569&ei=fy-CY8avIqXw4-EPid-HwA8&ved=0ahUKEwiG65DKk8z7AhUl-DgGHYnvAfgQ4dUDCA8&uact=5&oq=%22London%22+AND+%22UK%22+AND+%22Canada%22+-intitle%3A%22profiles%22+-inurl%3A%22dir%2F+%22+site%3Auk.linkedin.com%2Fin%2F+OR+site%3Auk.linkedin.com%2Fpub%2F+%22%40gmail.com%22&start=" + num)
    driver.implicitly_wait(20)
    parentElement = driver.find_elements(By.CLASS_NAME , "yuRUbf")
    
    for element in parentElement:
        elementList = element.find_element(By.TAG_NAME,"a")
        link = elementList.get_attribute("href")
        print(link)
        validurl(link)
    

print(sent_emails)
print("Finished scraping for emails!")
driver.quit()
