from liteflow.core import *

def get_logger(name: str):
    import logging
    
    logger = logging.getLogger("my")
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    ch = logging.StreamHandler()
    ch.setLevel(level=logging.DEBUG)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    
    return logger


logger = get_logger("my")

    
def get_exists_by_xpath(browser, xpath: str, timeout: int = 10):
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import NoSuchElementException   
    try:
        return WebDriverWait(browser, timeout).until(
            EC.presence_of_element_located((By.XPATH, xpath)))
    except NoSuchElementException:
        return
    
    
def click_image(file_name: str):
    import pyautogui
    image = pyautogui.locateCenterOnScreen(file_name)
    while image == None:
        image = pyautogui.locateCenterOnScreen(file_name)
    
    pyautogui.moveTo(image)
    pyautogui.leftClick()
    
    
class UpdateRoboData(StepBody):
    def __init__(self):
        self.value = None
        
    def run(self, context: StepExecutionContext) -> ExecutionResult:
        return ExecutionResult.next()
    
    
class CustomLogger(StepBody):
    """
    Логгинг Step для использования внутри Flow
    level (str): уровень лога
    text (str): текст лога, может в себе содержать %s
    args (tuple): аргументы для %s
    
    Dev: Turukbayev Zamanbek
    """
    def __init__(self):
        self.level = 'info'
        self.text = str()
        self.args = tuple()
    
    def run(self, context: StepExecutionContext) -> ExecutionResult:
        if len(self.args) == 1:
            self.args = (self.args[0], )
        getattr(logger, self.level)(self.text, *self.args, )
        
        return ExecutionResult.next()
    

class Sleep(StepBody):
    
    def __init__(self):
        self.seconds = 30
    
    def run(self, context: StepExecutionContext) -> ExecutionResult:
        import time
        logger.info('Сплю %s секундов', self.seconds)
        time.sleep(self.seconds)
        return ExecutionResult.next()
    
    
class RunChrome(StepBody):
    """Запуск Chrome драйвера"""
    def __init__(self):
        self.browser = None
        
    def run(self, context: StepExecutionContext) -> ExecutionResult:
        from selenium import webdriver
        self.browser = webdriver.Chrome('chromedriver')
        self.browser.maximize_window()
        return ExecutionResult.next()
    
    def on_error(self):
        self.browser.quit()
        

class MongoAction(StepBody):
    """Запись данных в БД
    db [MongoDB.connect()]
    document [Mongo doc]
    method [What to call]
    in_data [In data]
    """

    def __init__(self):
        self.db = None
        self.document = None
        self.method = None
        self.in_data = None
        self.parameter = {}
        self.result = None

    def run(self, context: StepExecutionContext) -> ExecutionResult:
        from pymongo.errors import DuplicateKeyError, BulkWriteError

        if self.in_data == [[]]:
            logger.info(f'Пришел пустой текст = {self.in_data}')
            return ExecutionResult.next()

        logger.info(f'Взаимодействие с БД. Документ: {self.document} Операция: {str(self.method)}')
        try:
            self.result = getattr(getattr(self.db, str(self.document)), str(self.method))(*self.in_data,
                                                                                          **self.parameter)
        except DuplicateKeyError:
            pass
        except BulkWriteError:
            pass

        return ExecutionResult.next()


class EgovLogin(StepBody):
    """Авторизация в EGOV"""
    def __init__(self):
        self.browser = None
        
    def run(self, context: StepExecutionContext) -> ExecutionResult:
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        login_link_xpath = '//*[@id="top-right"]/div[2]/div[2]/div/a[1]'
        ecp_link_xpath = '//*[@id="certificate-nav-tab"]'
        choose_cert_btn_xpath = '//*[@id="buttonSelectCert"]'
        
        browser = self.browser
        browser.get('https://egov.kz/cms/ru')

        login_link = WebDriverWait(browser, 30).until(
            EC.presence_of_element_located((By.XPATH, login_link_xpath)))
        login_link.click()
        logger.info("Нажал 'Войти' ")

        ecp_link = WebDriverWait(browser, 30).until(
            EC.presence_of_element_located((By.XPATH, ecp_link_xpath)))
        ecp_link.click()
        logger.info("Выбрал 'ЭЦП' ")

        choose_cert = WebDriverWait(browser, 30).until(
            EC.element_to_be_clickable((By.XPATH, choose_cert_btn_xpath)))
        choose_cert.click()
        logger.info("Нажал 'Выбрать сертификат' ")
        
        return ExecutionResult.next()
        
        
        
class NCALayerSign(StepBody):
    """Подписание в NCALayer"""
    def __init__(self):
        self.secret_key_path = str
        self.key_password = str
        
    def run(self, context: StepExecutionContext) -> ExecutionResult:
        from pywinauto import Desktop
        from pywinauto import Application
        
        app = Application(backend='win32')
        app.connect(path='javaw.exe', timeout=60)
        logger.info("Подключился к NCALayer")
        
        file_name_field = app.window(class_name='SunAwtDialog')
        click_image('file_name.png')
        file_name_field.type_keys(f'egov/{self.secret_key_path}')
        file_name_field.type_keys('{ENTER}')
        logger.info("Ввел путь ключа '%s' ", self.secret_key_path)
        
        password_field = app.window(class_name='SunAwtDialog')
        click_image('enter_password.png')
        password_field.type_keys(self.key_password)
        password_field.type_keys('{ENTER}')
        logger.info("Ввел пароль ключа")
        
        click_image('sign.png')
        logger.info("Нажал подписать")
        
        return ExecutionResult.next()

    
class OrderService(StepBody):
    """Заказ услуги"""
    
    def __init__(self):
        self.browser = None
        self.service_name = str
        
    def run(self, context: StepExecutionContext) -> ExecutionResult:
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        search_field_xpath = '//*[@id="edit-query"]'
        search_result_class_name = 'search-results'
        
        browser = self.browser

        search_field = WebDriverWait(browser, 30).until(
            EC.element_to_be_clickable((By.XPATH, search_field_xpath)))
        search_field.send_keys(self.service_name)
        search_field.submit()
        logger.info("Ввел в поле поиск '%s' и нажал поиск", self.service_name)

        search_results = WebDriverWait(browser, 30).until(
                    EC.presence_of_element_located((By.CLASS_NAME, search_result_class_name)))
        service = search_results.find_element_by_partial_link_text(self.service_name)
        service.click()
        logger.info('Нажал услугу "%s" ', self.service_name)

        order_service_div = WebDriverWait(browser, 30).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'sticky-wrapper')))
        order_service_div.find_element_by_tag_name('a').click()
        logger.info("Нажал 'Заказать услугу онлайн' ")
    
        return ExecutionResult.next()
    

class OrderServiceSteps(StepBody):
    """Заказ услуги Шаги"""
    
    def __init__(self):
        self.browser = None
        self.iin = str
        self.target_info = str
        self.target_sign_text = str
        
    def run(self, context: StepExecutionContext) -> ExecutionResult:
        import time
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        
        iin_input_xpath = '//*[@id="requests"]/div/div/div[1]/div/div[1]/div[1]/div[2]/div[1]/div/input'
        check_iin_btn_xpath = '//*[@id="requests"]/div/div/div[2]/button'
        info_list_xpath = '//*[@id="requests"]/div/div/div[3]'
        sign_btn_xpath = '//*[@id="requests"]/div/div/div[6]/button'
        sign_types_xpath = '//*[@id="sign"]/div/div/div/div[1]/div'
        flash_card_xpath = '//*[@id="sign"]/div/div/div/div[2]/eds/div/div/div[2]/figure'
        
        browser = self.browser
        browser.switch_to.window(browser.window_handles[1])
        
        iin_input = WebDriverWait(browser, 30).until(
            EC.element_to_be_clickable((By.XPATH, iin_input_xpath)))
        iin_input.send_keys(self.iin)
        logger.info("Ввел иин '%s' ", self.iin)

        check_iin_btn = WebDriverWait(browser, 30).until(
            EC.element_to_be_clickable((By.XPATH, check_iin_btn_xpath)))
        check_iin_btn.click()
        logger.info("Нажал 'Проверить' ")
        
        time.sleep(2)
        info_list = WebDriverWait(browser, 30).until(
            EC.element_to_be_clickable((By.XPATH, info_list_xpath)))
        for info in info_list.find_elements_by_class_name('custom-chk'):
            if self.target_info in info.text:
                info.find_element_by_tag_name('label').click()
                logger.info('Выбрал услугу "%s" ', self.target_info)
        
        sign_btn = WebDriverWait(browser, 30).until(
            EC.element_to_be_clickable((By.XPATH, sign_btn_xpath)))
        sign_btn.click()
        logger.info('Нажал "Подписать и Запросить" ')

        sign_types = WebDriverWait(browser, 30).until(
            EC.element_to_be_clickable((By.XPATH, sign_types_xpath)))
        for sign_btn in sign_types.find_elements_by_tag_name('button'):
            if self.target_sign_text in sign_btn.text:
                sign_btn.click()
                logger.info('Нажал тип подписание "%s" ', self.target_sign_text)

        flash_card = WebDriverWait(browser, 30).until(
            EC.element_to_be_clickable((By.XPATH, flash_card_xpath)))
        flash_card.click()
        logger.info('Нажал "Носитель информации" ')
        
        return ExecutionResult.next()