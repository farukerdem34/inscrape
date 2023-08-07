from selenium import webdriver
from instagramUserInfo import User
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep


class Instagram:
    def __init__(self, username, email, password):
        self.browser = webdriver.Firefox()
        self.base_url = "https://www.instagram.com/"
        self.login_page = "accounts/login/"
        self.user = User(username, email, password)

    def signIn(self):
        self.browser.get(self.base_url+self.login_page)
        self.browser.implicitly_wait(20)
        emailInput = self.browser.find_element(
            By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/section/main/div/div/div[1]/div[2]/form/div/div[1]/div/label/input")
        passwordInput = self.browser.find_element(
            By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/section/main/div/div/div[1]/div[2]/form/div/div[2]/div/label/input")

        emailInput.send_keys(self.user.username)
        passwordInput.send_keys(self.user.password)
        passwordInput.send_keys(Keys.ENTER)
        sleep(3)

    def getFollowers(self, username):
        self.browser.get(self.base_url+username+"/")
        sleep(2)
        followersButton = self.browser.find_element(
            By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[2]/a")
        followersButton.click()
        sleep(2)
        dialog = self.browser.find_element(
            By.XPATH, "/html/body/div[2]/div/div/div[3]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[1]/div")
        followersList = self.browser.find_elements(
            By.CSS_SELECTOR, "._aano > div:nth-child(1) > div:nth-child(1) > *")

        action = webdriver.ActionChains(self.browser)
        follower_count = len(followersList)
        print(follower_count)
        fbody = self.browser.find_element(By.XPATH, "//html/body/div[2]/div/div/div[3]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]")
        fbody.click()
        while True:
            self.browser.execute_script("arguments[0].scroll(0, arguments[0].scrollHeight);", fbody)

            sleep(5)
            followersList = self.browser.find_elements(
                By.CSS_SELECTOR, "._aano > div:nth-child(1) > div:nth-child(1) > *")
            sleep(2)
            if not (follower_count == len(followersList)):
                follower_count = len(followersList)
            else:
                break

        followers = []
        for follower in followersList:
            link = follower.find_element(
                By.CSS_SELECTOR, "a").get_attribute("href")
            data = {
                "username": link[26:-1],
                "profile_link": link
            }
            followers.append(data)
            print(data)
        return followers


instagram = Instagram(
    "burcuy3403", "burcuyilmazer34@yopmail.com", "YG2%$',$5)PM2d~")
instagram.signIn()
followers = instagram.getFollowers("burcuy3403")
print(followers)
