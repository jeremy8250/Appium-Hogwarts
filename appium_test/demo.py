from time import sleep

import pytest
import yaml
from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class TestXueqiu:

    # data_value = yaml.safe_load(open('/Users/ouchou/Projects/Appium-Hogwarts/data.yaml', "r"))
    data_value = yaml.safe_load(open('/Projects/Appium-Hogwarts/data.yaml', "r"))
    # 读取外部数据

    def setup(self):
        caps = {}
        caps["platformName"] = "android"
        caps["deviceName"] = "5554"
        caps["appPackage"] = "com.xueqiu.android"
        caps["appActivity"] = ".view.WelcomeActivityAlias"
        caps["noReset"] = True
        # 启动时不重置数据
        caps["autoGrantPermissions"] = True
        # 自动确认权限
        caps["unicodeKeyBoard"] = True
        # # 使用非英文键盘输入
        # caps["resetKeyBoard"] = True
        # # 测试完后重置为英文键盘输入
        # caps["dontStopAppOnReset"] = True
        # app启动时不重启进程
        caps["disableAndroidWatchers"] = True
        # 关闭安卓监听机制，提速用
        caps["skipDeviceInitialization"] = True
        # 每次执行时，跳过appium对设备权限和配置的初始化，加快启动速度
        caps["skipServerInstallation"] = True
        # 每次执行时，跳过uiautomator2 server的安装，加快启动速度
        caps["chromedriverExecutable"] = "/Users/ouchou/chromedriver/chromedriver_2.20"
        # 切换到webview后，需要指定chromedriver的版本，否则切换失败
        caps["avd"] = "p_api_23"
        # 启动指定模拟器

        self.driver = webdriver.Remote("http://localhost:4723/wd/hub", caps)
        self.driver.implicitly_wait(10)


        self.driver.find_element(MobileBy.XPATH, '//*[@resource-id="com.xueqiu.android:id/tv_skip"]').click()
        # 启动页加载时的倒计时

    @pytest.mark.parametrize("gupiao", data_value)
    # 数据驱动
    def test_search(self, gupiao):
        self.driver.find_element(MobileBy.ID, "tv_search").click()
        # 使用MobileBy定位方法
        self.driver.find_element(MobileBy.ID, "search_input_text").send_keys(gupiao)
        # 读取data_value中的【gupiao】
        self.driver.hide_keyboard()
        # 隐藏键盘

    @pytest.mark.parametrize("gupiao", data_value)
    # 数据驱动
    def test_search_and_get_price(self, gupiao):
        self.driver.find_element(MobileBy.ID, "tv_search").click()
        self.driver.find_element(MobileBy.ID, "search_input_text").send_keys(gupiao)
        self.driver.find_element(MobileBy.ID, "name").click()
        # assert float(self.driver.find_element(MobileBy.ID, "current_price").text) > 200
        # print(self.driver.page_source)
        # 通过打印page_source可以使用xpath定位该元素是否存在
        assert float(self.driver.find_element(MobileBy.ID, "current_price").get_attribute("text")) > 200

    @pytest.mark.parametrize("gupiao", data_value)
    # 数据驱动
    def test_search_HK_and_getprice(self, gupiao):
        self.driver.find_element(MobileBy.ID, "tv_search").click()
        self.driver.find_element(MobileBy.ID, "search_input_text").send_keys(gupiao)
        self.driver.find_element(MobileBy.XPATH,
                                 '//*[@resource-id="com.xueqiu.android:id/code" and @text="09988"]').click()
        # xpath组合定位：阿里巴巴港股代码
        assert float(self.driver.find_element(MobileBy.ID, "current_price").text) > 100

    @pytest.mark.parametrize("gupiao", data_value)
    # 数据驱动
    def test_search_and_add_into_optional(self, gupiao):
        self.driver.find_element(MobileBy.ID, "tv_search").click()
        self.driver.find_element(MobileBy.ID, "search_input_text").send_keys(gupiao)
        self.driver.find_element(MobileBy.XPATH,
                                 '//*[@resource-id="com.xueqiu.android:id/code" and @text="09988"]').click()
        self.driver.find_element(MobileBy.ID, "follow_btn").click()
        assert self.driver.find_element(MobileBy.XPATH, '//*[@class="android.widget.Toast"]').text == "添加成功"
        # 获取toast内容，并断言
        next_time_button = (
        MobileBy.XPATH, '//*[@resource-id="com.xueqiu.android:id/md_buttonDefaultNegative" and @text="下次再说"]')
        try:
            self.driver.find_element(*next_time_button).click()
            self.driver.find_element(MobileBy.ID, "action_close").click()
        except NoSuchElementException:
            self.driver.find_element(MobileBy.ID, "action_close").click()
            # 处理弹窗逻辑
            # 下次再说只有第一次的时候才会出现
            # 因此需要做判断
        self.driver.find_element(MobileBy.ID, "tv_search").click()
        self.driver.find_element(MobileBy.ID, "search_input_text").send_keys(gupiao)
        self.driver.find_element(MobileBy.XPATH,
                                 '//*[@resource-id="com.xueqiu.android:id/code" and @text="09988"]').click()
        assert self.driver.find_element(MobileBy.ID, "followed_btn").get_attribute("text") == "已添加"

    def test_scroll(self):
        # print(self.driver.get_window_rect())
        # 打印当前屏幕的宽度、高度、初始坐标
        size = self.driver.get_window_size()
        x1 = size['width'] * 0.5
        # 初始x轴坐标：当前屏幕宽度*百分比系数
        y1 = size['height'] * 0.8
        # 初始y轴坐标：当前屏幕高度*百分比系数
        x2 = size['width'] * 0.5
        # 最终x轴坐标：当前屏幕宽度*百分比系数
        y2 = size['height'] * 0.2
        # 最终y轴坐标：当前屏幕高度*百分比系数
        for i in range(10):
            # 连续滑动10次
            TouchAction(self.driver).long_press(x=x1, y=y1).move_to(x=x2, y=y2).release().perform()

    def test_uiselector(self):
        scroll_to_element = (MobileBy.ANDROID_UIAUTOMATOR,
                             'new UiScrollable(new UiSelector().scrollable(true).instance(0)).scrollIntoView(new UiSelector().text("清扬君").instance(0))')
        self.driver.find_element(*scroll_to_element).click()

    def test_driver(self):
        self.driver.background_app(5)
        # 放到后台5秒后自动返回
        self.driver.lock(5)
        # 锁屏5秒
        self.driver.unlock()
        # 解锁

    def test_webview_context(self):
        self.driver.find_element(By.XPATH, '//*[@resource-id="com.xueqiu.android:id/tab_name" and @text="交易"]').click()
        # 点击【交易】
        WebDriverWait(self.driver, 20).until(lambda x: len(self.driver.contexts) > 1)
        # 等待webview出现
        webview = self.driver.contexts[-1]
        self.driver.switch_to.context(webview)
        # 获取webview的上下文，并切换到webview
        # print(self.driver.page_source)
        # # 打印page_source可以查看是否成功切换到webview
        self.driver.find_element(By.CSS_SELECTOR, '.trade_home_agu_3ki').click()
        # 点击【A股开户】
        # print(self.driver.window_handles)
        # 打印所有窗口句柄
        WebDriverWait(self.driver, 20).until(lambda x: len(self.driver.window_handles) > 4)
        # 等待所有窗口出现
        self.driver.switch_to.window(self.driver.window_handles[-1])
        # 切换到最新窗口
        # print(self.driver.current_window_handle)
        # 打印当前窗口句柄
        phone = (By.ID, 'phone-number')
        WebDriverWait(self.driver, 20).until(expected_conditions.visibility_of_element_located(phone))
        self.driver.find_element(*phone).send_keys("12345")

    def test_account_open(self):
        self.driver.find_element(By.XPATH, '//*[@resource-id="com.xueqiu.android:id/tab_name" and @text="交易"]').click()
        # 点击【交易】
        WebDriverWait(self.driver, 20).until(lambda x: len(self.driver.contexts) > 1)
        # 等待webview出现
        webview = self.driver.contexts[-1]
        self.driver.switch_to.context(webview)
        # 获取webview的上下文，并切换到webview
        self.driver.find_element(By.CSS_SELECTOR, '.trade_home_xueying_SJY').click()
        # 点击【港美股开户】
        # print(self.driver.window_handles)
        # 打印所有窗口句柄
        WebDriverWait(self.driver, 20).until(lambda x: len(self.driver.window_handles) > 3)
        # 等待所有窗口出现
        self.driver.switch_to.window(self.driver.window_handles[-1])
        # 切换到最新窗口
        # print(self.driver.current_window_handle)
        # 打印新窗口的句柄
        phone = (By.CSS_SELECTOR, 'input[placeholder="请输入手机号"]')
        WebDriverWait(self.driver, 20).until(expected_conditions.visibility_of_element_located(phone))
        # 等待页面出现手机号输入框
        self.driver.find_element(*phone).send_keys("12345")
        # 输入错误的手机号
        submit = (By.CSS_SELECTOR, '.open_form-submit_1Ms')
        self.driver.find_element(*submit).click()
        # 提交
        toast_msg = (By.CSS_SELECTOR, '.Toast_toast_22U')
        # 非android toast，webview中的toast提示
        assert self.driver.find_element(*toast_msg).text == "请输入正确的手机号！"
        # 验证toast提示是否正确
        native = self.driver.contexts[0]
        self.driver.switch_to.context(native)
        # 切换回【native】
        self.driver.find_element(MobileBy.XPATH, '//*[@resource-id="com.xueqiu.android:id/action_bar_back"]').click()
        # 返回前一页

    def test_avd(self):
        self.driver.find_element(MobileBy.XPATH, '//*[@text="行情"]')
        # 自动启动模拟器，并进行点击操作


    def teardown(self):
        sleep(3)
        self.driver.quit()
