from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from appium_test_po.page.base_page import BasePage
from appium_test_po.page.search import Search
import logging


class Stocks(BasePage):
    _search_button = (By.ID, "action_search")
    _stock_name = (By.ID, "portfolio_stockName")
    _back = (By.ID, "action_back")

    logging.basicConfig(level=logging.INFO)

    def goto_search_page(self):
        WebDriverWait(self._driver, 10).until(expected_conditions.visibility_of_element_located(self._search_button))
        # 页面切换有延时，需要等待搜索按钮出现
        self.find(*self._search_button).click()
        # 点击搜索按钮
        return Search(self._driver)
        # 返回搜索页面

    def goto_search_page_by_yaml(self):
        WebDriverWait(self._driver, 10).until(expected_conditions.visibility_of_element_located(self._search_button))
        # 页面切换有延时，需要等待搜索按钮出现
        self.steps("../page/stock.yaml")
        # 点击搜索按钮
        return Search(self._driver)
        # 返回搜索页面

    def get_selected_stock(self):
        stock_name = []
        stock_list = self._driver.find_elements(By.ID, "portfolio_stockName")
        for stock in stock_list:
            stock_name.append(stock.get_attribute("text"))
        return stock_name
        # 获取自选页面股票的名称

    def clear_selected_stocks(self, key):
        stock = key
        pageSource1 = self._driver.page_source
        if "涨跌统计" in pageSource1:
            self.find_by_text("自选股").click()
        pageSource2 = self._driver.page_source
        if stock in pageSource2:
            # 打印自选页面的PageSource
            # 如果自选股票名字出现
            self.find_by_text(key).click()
            self.find_by_text("设自选").click()
            self.find_by_text("删除自选").click()
            self.find(*self._back).click()
            # 删除自选股票，使列表清空
            return self
        else:
            return self
            # 没有自选股票，啥都不做
