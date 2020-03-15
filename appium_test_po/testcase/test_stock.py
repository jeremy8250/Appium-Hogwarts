from appium_test_po.page.app import App


class TestStock:
    def setup(self):
        self.stocks = App().start().main().goto_stocks_page()
        # app初始化->启动->首页->行情

    def test_add_to_selected(self):
        self.stocks.clear_selected_stocks("京东")
        # 清空自选列表
        self.stocks.goto_search_page().search("京东").add_selected().cancel_search()
        # 搜索京东->点击添加自选->点击取消按钮
        assert "京东" in self.stocks.get_selected_stock()
        # 验证股票已添加到自选列表

    def test_add_to_selected_by_steps(self):
        self.stocks.clear_selected_stocks("京东")
        # 清空自选列表
        self.stocks.goto_search_page_by_yaml().search_by_yaml("京东").add_selected().cancel_search()
        # 搜索京东->点击添加自选->点击取消按钮
        assert "京东" in self.stocks.get_selected_stock()
        # 验证股票已添加到自选列表

