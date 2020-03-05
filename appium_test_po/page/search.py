from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.common.by import By
from appium_test_po.page.base_page import BasePage


class Search(BasePage):
    # todo: 写到这里的好处：多平台、多版本、多个可能定位符
    _name_locator = (MobileBy.ID, "name")
    _search_input = (MobileBy.ID, "search_input_text")

    def search_with_datadrive(self, key: str):
        # 【key:string】参数引导类型
        # 表示需要输入的参数类型是string
        # self.find(*self._search_input).send_keys(key)
        # self.find(self._name_locator).click()
        # self.steps("../page/search.yaml")
        # 通过steps里定义的by/location/action完成步骤的数据驱动
        self._params = {}
        # 先清空params内容
        self._params["key"] = key
        # 往parms里面追加外部传入的参数
        self.steps("../page/search.yaml")
        return self

    def search(self, key: str):
        # 【key:string】参数引导类型
        # 表示需要输入的参数类型是string
        self.find(*self._search_input).send_keys(key)
        self.find(self._name_locator).click()
        return self

    def get_price(self, key: str) -> float:
        # 输入类型为string，返回类型为float
        return float(self.find(MobileBy.ID, "current_price").text)

    def add_selected(self):
        element = self.find_by_text("加自选")
        element.click()
        return self
        # 点击添加自选

    def get_selected_message(self):
        return self.find_and_get_text(By.ID, "followed_btn")
        # 返回【已添加】按钮的文本

    def cancel_search(self):
        self.find(By.ID, "action_close").click()
        return self
        # 点击取消按钮
