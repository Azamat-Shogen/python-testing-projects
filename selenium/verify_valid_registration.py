"""
Write a selenium script to verify valid registration

"""

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException

from utils import get_base_url
from utils import init_driver

driver = init_driver()
base_url = get_base_url('my-account')
driver.get(base_url)
wait = WebDriverWait(driver, 10)



def fill_out_registration_form():
    username_field = driver.find_element(By.ID, 'username')
    username_field.send_keys("user110")

    email_field = driver.find_element(By.ID, 'reg_email')
    email_field.send_keys('user112@gmail.com')

    password_field = driver.find_element(By.ID, 'password')
    password_field.send_keys('Password_12345')

    password_confirm_field = driver.find_element(By.ID, 'reg_password')
    password_confirm_field.send_keys('Password_12345')

    register_button = driver.find_element(By.NAME, 'register')
    register_button.click()
    
    print('Clicked register button')


def verify_successfull_registration():
    try:
        selector_text = '//*[@id="post-9"]/div/div/nav/ul/li[6]'
        logout_element = wait.until(EC.visibility_of_element_located((By.XPATH, selector_text)))
        if not logout_element.is_displayed():
            raise Exception("Logout element is not visible")
        print("User registration has been successful")
    except TimeoutException as ex:
        print(f"Failed to locate element, error: {ex}")
    except StaleElementReferenceException as ex:
        print(f"Failed to locate element, error: {ex}")
    except Exception:
        print("Something went wrong while locating the 'Logout' link")
    finally:
        driver.quit()




if __name__ == "__main__":
    fill_out_registration_form()
    verify_successfull_registration()