from appium_test_po.page.base_page import BasePage
from appium_test_po.page.profile import Profile
from appium_test_po.page.search import Search
from appium_test_po.page.stocks import Stocks


class Main(BasePage):

    def goto_search_page_with_datadrive(self):
        # self.find(MobileBy.ID, "tv_search").click()
        # 点击搜索输入框
        self.steps("../page/steps.yaml")
        return Search(self._driver)
        # 返回搜索页面（需要给定一个driver）

    def goto_search_page(self):
        # self.find(MobileBy.ID, "tv_search").click()
        # 点击搜索输入框
        self.steps("../page/steps.yaml")
        return Search(self._driver)
        # 返回搜索页面（需要给定一个driver）

    def goto_stocks_page(self):
        self.find_by_text("行情").click()
        # 点击底部【行情】tab
        return Stocks(self._driver)
        # 跳转【行情】页面

    def goto_trade_page(self):
        pass

    def goto_profile_page(self):
        self.find_by_text("我的").click()
        # 点击底部【我的】tab
        return Profile(self._driver)
        # 跳转【我的】页面

    def goto_message_page(self):
        pass
