"""
app页面定义一些通用的方法
"""
import os

from appium import webdriver
from selenium.webdriver.common import utils
from selenium.webdriver.support.wait import WebDriverWait

from appium_test_po.page.base_page import BasePage
from appium_test_po.page.main import Main


class App(BasePage):
    _appPackage = "com.xueqiu.android"
    _appActivity = ".view.WelcomeActivityAlias"

    def start(self):
        if self._driver is None:
            # 启动app的时候，如果没有给driver，就创建一个
            # 如果已经有driver了，就杀掉进程，重启起一个
            # 这样可以避免再次安装appium控件
            caps = {}
            caps["platformName"] = "android"
            caps["deviceName"] = "emulator"
            caps["appPackage"] = self._appPackage
            caps["appActivity"] = self._appActivity
            caps["noReset"] = True
            # 启动时不重置数据
            udid = os.getenv("UDID", None)
            if udid != None:
                caps["udid"] = udid
            # caps["udid"] = "emulator-5554"
            # 从外部获取udid，使得selenium grid可以将job分发到不同设备运行
            caps["systemPort"] = utils.free_port()
            caps["chromedrivePort"] = utils.free_port()
            caps["autoGrantPermissions"] = True
            # 自动确认权限
            # caps["unicodeKeyBoard"] = True
            # # 使用非英文键盘输入
            # caps["resetKeyBoard"] = True
            # # 测试完后重置为英文键盘输入
            # caps["dontStopAppOnReset"] = True
            # app启动时不重启进程
            # caps["disableAndroidWatchers"] = True
            # 关闭安卓监听机制，提速用
            # caps["skipDeviceInitialization"] = True
            # 每次执行时，跳过appium对设备权限和配置的初始化，加快启动速度
            # caps["skipServerInstallation"] = True
            # 每次执行时，跳过uiautomator2 server的安装，加快启动速度
            caps["chromedriverExecutable"] = "/Users/ouchou/chromedriver/chromedriver_2.20"
            # 切换到webview后，需要指定chromedriver的版本，否则切换失败
            # caps["avd"] = "p_api_23"
            # 启动指定模拟器

            # self._driver = webdriver.Remote("http://localhost:4723/wd/hub", caps)
            self._driver = webdriver.Remote("http://192.168.1.9:4444/wd/hub", caps)
            # 通过selenium hub转发
            self._driver.implicitly_wait(6)

            # self.driver.find_element(MobileBy.XPATH, '//*[@resource-id="com.xueqiu.android:id/tv_skip"]').click()
            # 启动页加载时的倒计时
        else:
            self._driver.start_activity(self._appPackage, self._appActivity)
            # 如果没有初始化driver,直接启动app

        return self
        # 启动后返回自己，可链式调用下面的main方法

    def restart(self):
        pass

    def stop(self):
        pass

    def main(self) -> Main:
        # 【->】返回引导类型
        # 返回类型为Main
        # todo:wait main Page
        def wait_load(driver):
            source = self._driver.page_source
            if "我的" in source:
                return True
            # 如果【我的】在pageSource里面，表示加载完成了，返回True
            if "同意" in source:
                return True
            return False
            # 如果既没有【我的】，也没有【同意】，表示没有加载完成

        WebDriverWait(self._driver, 30).until(wait_load)
        # wait_load这里不用加()，只用名字表示方法
        # 加了()就会调用方法
        return Main(self._driver)
