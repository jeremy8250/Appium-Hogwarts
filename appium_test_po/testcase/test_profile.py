from appium_test_po.page.app import App


class TestProfile:
    def setup(self):
        self.profile = App().start().main().goto_profile_page()
        # app初始化->启动->首屏->我的

    def test_login_by_password(self):
        assert "错误" in self.profile.login_by_password("13817980369", "123456")
        # 输入错误的用户名密码后，获取报错信息，断言报错是否正确
