from selenium.webdriver.common.by import By

from appium_test_po.page.base_page import BasePage


class Profile(BasePage):
    def login_by_password(self, mobile, password):
        self.find(By.XPATH, '//*[@text="帐号密码登录"]').click()
        self.find(By.ID, "login_account").send_keys(mobile)
        self.find(By.ID, 'login_password').send_keys(password)
        self.find(By.XPATH, '//*[@text="登录"]').click()
        message = self.find(By.ID, 'md_content').text
        self.find(By.XPATH, '//*[@text="确定"]').click()
        return message