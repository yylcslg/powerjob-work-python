from time import sleep

from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

chromedriver = '/home/yinyunlong/person/program/chromedriver/chromedriver'


class SeleniumDirver:

    def __init__(self):
        options = webdriver.ChromeOptions()
        # options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-blink-features=AutomationControlled')

        options.add_experimental_option("excludeSwitches", ['enable-automation'])
        options.add_experimental_option('detach', True)  # 不自动关闭浏览
        options.add_argument("--disable-blink-features")
        options.add_argument("--proxy-server={0}".format('127.0.0.1:8889'))
        options.add_argument("--disable-blink-features=AutomationControlled")

        service = Service(executable_path=chromedriver)
        self.driver = webdriver.Chrome(options=options, service=service)  # Chrome浏览器
        self.driver.maximize_window()
        # driver.implicitly_wait(30)


        pass


    def x_login(self, user_name,account_name,pwd):
        url = 'https://twitter.com/login'
        self.driver.get(url)
        wait = WebDriverWait(self.driver, 20)
        email_input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[autocomplete=username]'))
        )
        email_input.send_keys(user_name)

        sleep(3)
        email_input.send_keys(Keys.ENTER)
        try:
            user_name_input = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[autocomplete=on]'))
            )
            user_name_input.send_keys(account_name)
            sleep(3)
            user_name_input.send_keys(Keys.ENTER)
        except Exception :
            print('user_name_input pass')


        password_input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name=password]'))
        )
        password_input.send_keys(pwd)

        sleep(3)
        password_input.send_keys(Keys.ENTER)

        sleep(3)

#
    def reply_msg(self, url, msg):

        for cookie in self.driver.get_cookies():
            self.driver.add_cookie(cookie)

        self.driver.get(url)

        wait = WebDriverWait(self.driver, 20)
        reply_xpath = '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/section/div/div/div[1]/div/div/div/div/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div/div/span'

        reply_span = wait.until(
            EC.presence_of_element_located((By.XPATH, reply_xpath))
        )

        reply_span.send_keys(msg)
        sleep(3)
        reply_span.send_keys(Keys.ENTER)


        sleep(3)

        reply_btn = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-testid=tweetButtonInline]'))
        )

        action = ActionChains(self.driver)
        action.move_to_element(reply_btn).click(reply_btn).perform()
        sleep(3)


    def close(self):
        self.driver.close()
        self.driver.quit()


if __name__ == '__main__':



    # s = SeleniumDirver()
    # s.x_login()
    # s.reply_msg('https://x.com/loadingman5862/status/1855524233650254217', 'hello 1111 @supermain059029')
    # s.close()
    print('finish............')
