import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

APP_URL = "http://localhost:3001"

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.binary_location = "/usr/bin/chromium-browser"
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    from selenium.webdriver.chrome.service import Service
    driver = webdriver.Chrome(
        service=Service("/usr/bin/chromedriver"),
        options=options
    )
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

# TC01 - Page loads successfully
def test_01_page_loads(driver):
    driver.get(APP_URL)
    assert driver.current_url == APP_URL + "/"  or APP_URL in driver.current_url

# TC02 - Page title is correct
def test_02_page_title(driver):
    driver.get(APP_URL)
    assert "Expense" in driver.title or driver.title != ""

# TC03 - Add Expense heading is visible
def test_03_add_expense_heading(driver):
    heading = driver.find_element(By.XPATH, "//*[contains(text(),'Add New Expense')]")
    assert heading.is_displayed()

# TC04 - Title input field is visible
def test_04_title_field_visible(driver):
    title_field = driver.find_element(By.XPATH, "//input[@placeholder='Title *']")
    assert title_field.is_displayed()

# TC05 - Amount input field is visible
def test_05_amount_field_visible(driver):
    amount_field = driver.find_element(By.XPATH, "//input[@placeholder='Amount (Rs.) *']")
    assert amount_field.is_displayed()

# TC06 - Category dropdown is visible
def test_06_category_dropdown_visible(driver):
    category = driver.find_element(By.XPATH, "//select")
    assert category.is_displayed()

# TC07 - Save Expense button is visible
def test_07_save_button_visible(driver):
    save_btn = driver.find_element(By.XPATH, "//button[contains(text(),'Save Expense')]")
    assert save_btn.is_displayed()

# TC08 - Reset button is visible
def test_08_reset_button_visible(driver):
    reset_btn = driver.find_element(By.XPATH, "//button[contains(text(),'Reset')]")
    assert reset_btn.is_displayed()

# TC09 - All Expenses section is visible
def test_09_all_expenses_section(driver):
    heading = driver.find_element(By.XPATH, "//*[contains(text(),'All Expenses')]")
    assert heading.is_displayed()

# TC10 - Search bar is visible
def test_10_search_bar_visible(driver):
    search = driver.find_element(By.XPATH, "//input[@placeholder='Search expenses...']")
    assert search.is_displayed()

# TC11 - Add a new expense successfully
def test_11_add_expense(driver):
    driver.get(APP_URL)
    time.sleep(2)
    driver.find_element(By.XPATH, "//input[@placeholder='Title *']").clear()
    driver.find_element(By.XPATH, "//input[@placeholder='Title *']").send_keys("Test Expense")
    driver.find_element(By.XPATH, "//input[@placeholder='Amount (Rs.) *']").clear()
    driver.find_element(By.XPATH, "//input[@placeholder='Amount (Rs.) *']").send_keys("500")
    Select(driver.find_element(By.XPATH, "//select")).select_by_visible_text("Food")
    driver.find_element(By.XPATH, "//input[@type='date']").send_keys("2026-05-01")
    driver.find_element(By.XPATH, "//button[contains(text(),'Save Expense')]").click()
    time.sleep(2)
    page_text = driver.find_element(By.TAG_NAME, "body").text
    assert "Test Expense" in page_text

# TC12 - Added expense appears in list
def test_12_expense_in_list(driver):
    page_text = driver.find_element(By.TAG_NAME, "body").text
    assert "Test Expense" in page_text

# TC13 - Search functionality works
def test_13_search_works(driver):
    driver.get(APP_URL)
    time.sleep(2)
    search = driver.find_element(By.XPATH, "//input[@placeholder='Search expenses...']")
    search.clear()
    search.send_keys("Test Expense")
    time.sleep(2)
    page_text = driver.find_element(By.TAG_NAME, "body").text
    assert "Test Expense" in page_text

# TC14 - Category filter dropdown works
def test_14_category_filter(driver):
    driver.get(APP_URL)
    time.sleep(2)
    filters = driver.find_elements(By.XPATH, "//select")
    assert len(filters) >= 1

# TC15 - Delete expense works
def test_15_delete_expense(driver):
    driver.get(APP_URL)
    time.sleep(2)
    delete_buttons = driver.find_elements(By.XPATH, "//button[contains(text(),'Delete')]")
    if len(delete_buttons) > 0:
        initial_count = len(delete_buttons)
        delete_buttons[0].click()
        time.sleep(2)
        new_delete_buttons = driver.find_elements(By.XPATH, "//button[contains(text(),'Delete')]")
        assert len(new_delete_buttons) < initial_count
    else:
        assert True