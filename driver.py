import os
import time

import logging
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from constants import Elements


LOCAL_HOST = "http://127.0.0.1"

class Driver:
    SECONDS_WAIT = 10
    HOST = os.environ.get('REACT_APP_STORE_URL', LOCAL_HOST)

    def __init__(self) -> None:
        self.chrome_options = Driver.set_chrome_options()
        self.driver = webdriver.Chrome(chrome_options=self.chrome_options, service=Service(ChromeDriverManager().install()))
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    @property
    def replace_value(self):
        return Keys.COMMAND + 'v'

    def set_chrome_options():
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920x1080")
        return chrome_options

    def get_card(self, wait, card):
        intents = 10
        while intents:
            try:
                wait.until(EC.presence_of_element_located((By.ID, Elements.DROPDOWN))).click()
                wait.until(EC.presence_of_element_located((By.ID, card))).click()
                intents = 0
            except:
                intents -= 1

    def enter_transaction(self, wait, driver, payment_method_button):
        wait.until(EC.presence_of_element_located((By.ID, payment_method_button))).click()
        time.sleep(5)

        driver.refresh()
        return driver

    def fill_braintree_transaction_form(self, wait, driver):
        for elem in [
            (Elements.NUMBER_BUTTON, Elements.BRAINTREE_NUMBER_FRAME, Elements.BRAINTREE_NUMBER_FIELD,),
            (Elements.EXP_DATE_BUTTON, Elements.BRAINTREE_EXP_DATE_FRAME, Elements.BRAINTREE_EXP_DATE_FIELD,)            
        ]:
            button, frame, field = elem
            driver.find_element(By.ID, button).click()

            time.sleep(5)
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, Elements.BRAINTREE_TRANSACTION_FORM)))
            wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, frame))) 
            wait.until(EC.element_to_be_clickable((By.ID, field))).send_keys(self.replace_value)
            driver.switch_to.default_content()
        return driver
    
    def fill_stripe_transaction_form(self, driver):
        for elem in [
            (Elements.NUMBER_BUTTON, Elements.STRIPE_NUMBER_FIELD,),
            (Elements.EXP_DATE_BUTTON, Elements.STRIPE_EXP_DATE_FIELD,),
            (Elements.CVC_BUTTON, Elements.STRIPE_CVC_FIELD,)
        ]:
            button, field = elem
            driver.find_element(By.ID, button).click()

            time.sleep(5)
            driver.switch_to.frame(driver.find_element(By.TAG_NAME, "iframe"))
            driver.find_element(By.ID, field).send_keys(Keys.COMMAND + 'v')
            driver.switch_to.default_content()
        return driver

    def purchase(self, payment_method, scenarios):
        is_stripe = 'stripe' in payment_method
        driver = self.driver
        driver.get(self.HOST)

        results = []
        try:
            for elem in scenarios:
                wait = WebDriverWait(driver, self.SECONDS_WAIT)

                logging.info('select product')
                driver.implicitly_wait(self.SECONDS_WAIT)
                driver = self.enter_transaction(
                    wait, driver, payment_method
                )
                driver.implicitly_wait(self.SECONDS_WAIT)

                self.get_card(wait, elem)
                logging.info(f'fill out transaction form')
                driver = self.fill_stripe_transaction_form(driver) if is_stripe else self.fill_braintree_transaction_form(wait, driver)

                logging.info('pay and get result')
                driver.find_element(By.ID, Elements.PAY_BUTTON).click()
                time.sleep(5)
                result = wait.until(EC.presence_of_element_located((By.ID, Elements.STATUS_RESPONSE)))
                time.sleep(5)

                results.append(result.text)

                logging.info('go back to catalogue')
                wait.until(EC.presence_of_element_located((By.ID, Elements.BACK_TO_CATALOGUE_BUTTON))).click()
        except:
            logging.error('Error')
            return ''
        finally:
            logging.info(f'Quit driver with results={results}')
            driver.quit()
            return results
