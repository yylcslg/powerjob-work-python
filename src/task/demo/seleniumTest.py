from time import sleep

from selenium import webdriver


def testChrome():
    options = webdriver.ChromeOptions()
    options.add_experimental_option('detach', True)  # 不自动关闭浏览
    driver = webdriver.Chrome(options=options)  # Chrome浏览器
    driver.get('https://apetimism.com/launchpad/lineaape')

    # 休眠5秒
    sleep(5)

    js = "return frontEndSignature('')"
    msg = driver.execute_script(js)
    print(msg)
    # 休眠5秒
    sleep(5)
    # 关闭浏览器驱动对象
    driver.quit()





if __name__ == '__main__':
    testChrome()