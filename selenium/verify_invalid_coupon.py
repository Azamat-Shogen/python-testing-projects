"""
Write a script to verify error message when invalid coupon is applied

"""

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException

from utils import get_base_url
from utils import init_driver

driver = init_driver()
base_url = get_base_url()
driver.get(base_url)
wait = WebDriverWait(driver, 10)

def add_item_to_cart():
    item_locator = '//*[@id="main"]/ul/li[1]/a[2]'
    add_cart_btn = driver.find_element(By.XPATH, item_locator)
    
    if not add_cart_btn.is_enabled():
        raise Exception("The button is not enabled")
    
    add_cart_btn.click()

    # Adjust locators based on actual element properties
    cart_item_locator = 'site-header-cart'
    cart_item = driver.find_element(By.CLASS_NAME, cart_item_locator)  # Assuming it's a class name
    

    try:
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, 'ul#site-header-cart span.count'), '1 item'))
        print("Item successfully added to cart.")
        cart_item.click()
    except TimeoutException as ex:
        print(f"Failed to locate element, error: {ex}")
    except StaleElementReferenceException as ex:
        print(f"Failed to locate element, error: {ex}")
    except Exception:
        print("Something went wrong while locating the cart element")


def verify_invalid_coupon_message():
    coupon_field = driver.find_element(By.ID, 'coupon_code')
    invalid_coupon_code = "ssqa101"
    coupon_field.send_keys(invalid_coupon_code)

    # Hit ENTER key to submit the coupon
    coupon_field.send_keys(Keys.ENTER)

    # Verify error message is displayed
    expected_error_message = f'Coupon "{invalid_coupon_code}" does not exist!'

    try:
        result_text = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'ul.woocommerce-error'))).text
        if result_text != expected_error_message:
            raise Exception(f"After applying an invalid coupon, the expected error message should be: {expected_error_message}")
        else:
            print("The actual result matches the expected result!")
       
    except TimeoutException as ex:
        print(f"Failed to locate element, error: {ex}")
    except StaleElementReferenceException as ex:
        print(f"Failed to locate element, error: {ex}")
    except Exception:
        print("Something went wrong while locating the error element")
    finally:
        driver.quit()


def main():
    add_item_to_cart()
    verify_invalid_coupon_message()

if __name__ == '__main__':
    main()
