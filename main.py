from selenium import webdriver
from instagramUserInfo import User
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep

class Instagram:
    def __init__(self,username,email,password):
        self.browser = webdriver.Firefox()
        self.base_url = "https://www.instagram.com/"
        self.login_page = "accounts/login/"
        self.user = User(username,email,password)

    def signIn(self):
        self.browser.get(self.base_url+self.login_page)
        self.browser.implicitly_wait(20)
        emailInput = self.browser.find_element(By.XPATH,"/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/section/main/div/div/div[1]/div[2]/form/div/div[1]/div/label/input")
        passwordInput = self.browser.find_element(By.XPATH,"/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/section/main/div/div/div[1]/div[2]/form/div/div[2]/div/label/input")

        emailInput.send_keys(self.user.username)
        passwordInput.send_keys(self.user.password)
        passwordInput.send_keys(Keys.ENTER)
        sleep(3)
    
    def getFollowers(self,username):
        self.browser.get(self.base_url+username+"/")
        sleep(2)
        followersButton = self.browser.find_element(By.XPATH,"/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[2]/a")
        followersButton.click()
        sleep(2)
        followersList = self.browser.find_element(By.XPATH,"/html/body/div[2]/div/div/div[3]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[1]/div")
        followersList = followersList.find_elements(By.CSS_SELECTOR,"._aano > div:nth-child(1) > div:nth-child(1) > *")
        
        for follower in followersList:
            link = follower.find_element(By.CSS_SELECTOR,"a").get_attribute("href")
            print(link)


instagram = Instagram("burcuy3403","burcuyilmazer34@yopmail.com","YG2%$',$5)PM2d~")
instagram.signIn()
instagram.getFollowers("burcuy3403")