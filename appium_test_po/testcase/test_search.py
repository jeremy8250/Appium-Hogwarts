import pytest
import yaml

from appium_test_po.page.app import App


class TestSearch:
    def setup(self):
        self.main = App().start().main()
        # app初始化->启动->回到首屏

    def test_search(self):
        assert self.main.goto_search_page().search("alibaba").get_price("BABA") > 200
        # 点击首屏->进入搜索页面->搜索"alibaba"->获取"BABA"股价->断言股价大于200

    def test_search_with_yaml(self):
        App().start().main().goto_search_page_with_datadrive().search_with_datadrive("jd")



    # @pytest.mark.parametrize("key, stock_type, price", [
    #     ("alibaba", "BABA", 200),
    #     ("JD", "JD", 20)
    # ])
    # # 参数化

    @pytest.mark.parametrize("key, stock_type, price", yaml.safe_load(open("data.yaml")))
    # 测试数据-数据驱动
    def test_search_data(self, key, stock_type, price):
        assert self.main.goto_search_page().search(key).get_price(stock_type) > price
        # 点击首屏->进入搜索页面->搜索"alibaba"->获取"BABA"股价->断言股价大于200

    def test_add_select(self):
        assert "已添加" in self.main.goto_search_page().search("京东").add_selected().get_selected_message()
        # 点击首屏->进入搜索页面->搜索"京东"->点击【加自选】->验证【已添加】
