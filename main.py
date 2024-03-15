from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# Set Chrome options for headless mode
options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # Uncomment if you want to run Chrome in headless mode

# Initialize WebDriver
driver = webdriver.Chrome(service=Service(executable_path="chromedriver.exe"), options=options)

# Maximize window
driver.maximize_window()

# Navigate to the URL
driver.get("https://directory.ntschools.net/#/schools")

# Wait for the selector to be present
selector = '#search-panel-container .nav-link'
links = WebDriverWait(driver, 60).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
    ) 

# Store results
results = []

# Selector for school name
school_name_selector = ".school-title h1"

# Iterate over links
for i in range(len(links)):
    # Wait for the link to be clickable
    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
    )

    # Click the link using JavaScript executor to avoid "element click intercepted" issue
    driver.execute_script("arguments[0].click();", links[i])
    
    # Wait for the school name element to be present
    name_e = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, school_name_selector))
    )

    # Extract details
    details = {
        'name': name_e.text,
        'physical_address': driver.find_element(By.XPATH,'//div[text()="Physical Address"]/following-sibling::div').text,
        'postal_address': driver.find_element(By.XPATH,'//*[text()="Postal Address"]/following-sibling::*').text,
        'phone_number': driver.find_element(By.XPATH,'//*[text()="Phone"]/following-sibling::*/a').text,
    }
    results.append(details)
    
    # Navigate back to the previous page to process the next element
    driver.back()

    # Re-find the links after navigating back
    links = WebDriverWait(driver, 60).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
    )

# Quit the WebDriver
driver.quit()

# Write results to CSV file
with open('schools_data.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file,
                            fieldnames=['name', 'physical_address', 'postal_address', 'phone_number'])
    writer.writeheader()
    writer.writerows(results)
