from selenium import webdriver


def init_driver():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)
    
    return driver

def get_base_url(endpoint=None):
    if endpoint:
        if not isinstance(endpoint, str):
            raise Exception(f"Ivalid endpoint type, expected 'str' but got {type(endpoint)}")
        return f"http://bootcamp.store.supersqa.com/{endpoint}"
    return 'http://bootcamp.store.supersqa.com/'
    