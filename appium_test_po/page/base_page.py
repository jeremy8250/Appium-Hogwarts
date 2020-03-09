import yaml
from appium.webdriver.webdriver import WebDriver
from selenium.webdriver.common.by import By
import logging


class BasePage:
    logging.basicConfig(level=logging.INFO)
    # 初始化log级别

    _driver: WebDriver

    _black_list = [
        (By.XPATH, "//*[@text='确定']"),
        (By.ID, "image_cancel"),
        (By.XPATH, "//*[@text='下次再说']")
    ]
    # 黑名单里面存放着业务流中出现的各种异常弹窗的元素定位符
    # 这些弹窗是需要被处理掉的
    _error_max = 3
    # 抛异常次数的最大值
    _error_count = 0
    # 初始化抛异常的次数

    _params = {}
    # 声明变量的集合
    # 临时性的保存外部参数的地方，初始化为空字典
    # 数据驱动-测试步骤驱动用

    def __init__(self, driver: WebDriver = None):
        # WebDriver = None，默认为None
        # 这是因为App不需要继承driver
        # 它是创建driver的
        self._driver = driver
        # 构造函数，创建一个driver，供其他类使用

    # todo: 通用异常 通过装饰器让函数自动处理异常
    def find_and_get_text(self, locator, value: str = None):
        # logging.info(locator)
        # logging.info(value)
        try:
            if isinstance(locator, tuple):
                element = self._driver.find_element(*locator)
                # 如果findElement需要传一个元组类型的参数，使用(*locator)
            else:
                element = self._driver.find_element(locator, value)
                # 如果findElement需要传两个参数，使用(locator, value)
            self._error_count = 0
            # 如果找到元素了，计数器清零
            return element.text
        except Exception as e:
            # 如果元素没有找到，则捕获异常
            if self._error_count > self._error_max:
                raise e
            # 如果捕获异常的累加次数大于max阈值，则直接抛异常
            self._error_count += 1
            # 如果累加次数没有超过max阈值，则计数器+1
            for element in self._black_list:
                # logging.info(element)
                # 遍历黑名单里面的元素
                elements = self._driver.find_elements(*element)
                if len(elements) > 0:
                    elements[0].click()
                    # 如果在当前页面找到了黑名单里的元素，则点掉
                    return self.find_and_get_text(locator, value)
                    # 返回find方法继续查找正常元素(递归查找)

    def find(self, locator, value: str = None):
        # logging.info(locator)
        # logging.info(value)
        try:
            if isinstance(locator, tuple):
                element = self._driver.find_element(*locator)
                # 如果findElement需一个元组类型的参数，使用(*locator)
            else:
                element = self._driver.find_element(locator, value)
                # 如果findElement传两个参数，使用(locator, value)
            self._error_count = 0
            # 如果找到元素了，计数器清零
            return element
            # 返回找到的元素
        except Exception as e:
            # 如果元素没有找到，则捕获异常
            if self._error_count > self._error_max:
                raise e
            # 如果捕获异常的累加次数大于max阈值，则直接抛异常
            self._error_count += 1
            # 如果累加次数没有超过max阈值，则计数器+1
            for element in self._black_list:
                # logging.info(element)
                # 遍历黑名单里面的元素
                elements = self._driver.find_elements(*element)
                if len(elements) > 0:
                    elements[0].click()
                    # 如果在当前页面找到了黑名单里的元素，则点掉
                    return self.find(locator, value)
                    # 返回find方法继续查找正常元素(递归查找)

    def get_toast(self):
        return self.find(By.XPATH, "//*[@class='android.widget.Toast']").text
        # 封装Toast

    def text(self, key):
        return (By.XPATH, "//*[@text='%s']" % key)

    def find_by_text(self, key):
        return self.find(self.text(key))
        # 封装XPATH文本方式定位

    # 步骤驱动为测试平台准备
    # 不会写代码的人可以通过yaml配置直接实现自动化
    def steps(self, path):
        with open(path, encoding="utf-8") as f:
            # 加了encoding可以防止yaml中文乱码
            steps: list[dict] = yaml.safe_load(f)
            # 读取steps.yaml文件到steps
            # steps为列表中包着词典的类型
            element: WebElement = None
            # 找元素找元素，首页需要有元素
            for step in steps:
                # logging.info(step)
                if "by" in step.keys():
                    # 如果在step的key有by
                    element = self.find(step["by"], step["locator"])
                    # 找到by对应的定位方法，找到locator对用的定位符，传给element(这个element类型为WebElement)
                if "action" in step.keys():
                    # 如果在step的key有action
                    action = step["action"]
                    # 取action的值
                    if action == "click":
                        # 如果action为click方法
                        element.click()
                        # 点击元素
                    elif action == "text":
                        # 如果action为text方法
                        element.text
                        # 获取元素的文本
                    elif action == "attribute":
                        # 如果action为attribute方法
                        element.get_attribute(step["value"])
                        # 获取元素的value属性值
                    elif action == "send":
                        # 如果action为send方法
                        content: str = step["value"]
                        # content为send对应的value
                        # 指定content类型为str，才能调用replace()
                        for key in self._params.keys():
                            # 循环遍历所有外部传入的参数
                            content = content.replace("{%s}" % key, self._params[key])
                            # 将外部传入的参数批量替换{}里面的内容
                            # {}为send对应的value值(如value: "{key}")
                        element.send_keys(content)
                        # 发送替换的内容
