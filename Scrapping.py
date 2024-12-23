from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

main_url = "https://villagesoulofindia.com/site/contactus"
menu_url = "https://villagesoulofindia.com/app/order/menu" 

#  Title
driver.get(main_url)
title = driver.title.split()[0]
print(title)

# Address
elements = driver.find_elements(By.CLASS_NAME, "info-box")
if len(elements) > 1:
    address_element = elements[1]  # Assuming the address is the second occurrence
    address = address_element.find_element(By.TAG_NAME, "p").text  # Extract the text from the <p> tag
    print("Address:", address)
else:
    print("Address not found.")

# Opening Hours
opening_time_element = driver.find_element(By.CLASS_NAME, "opening-time")
left_text = opening_time_element.find_element(By.CLASS_NAME, "left").text
right_text = opening_time_element.find_element(By.CLASS_NAME, "right").text
try:
    # Print full texts for clarity
    print("Left Text:", left_text)
    print("Right Text:", right_text)

    # Process `left_text` for Monday to Friday hours
    left_lines = left_text.split("\n")  # Split by newlines
    if len(left_lines) >= 2:
        monday_hours = left_lines[1] + " & " + left_lines[2]  # Combine timings
    else:
        monday_hours = "Unavailable"

    # Process `right_text` for Saturday/Sunday and holiday info
    right_lines = right_text.split("\n")
    if len(right_lines) >= 2:
        saturday_hours = right_lines[1]  # Saturday/Sunday timings
    else:
        saturday_hours = "Unavailable"

    holiday = "Tuesday" if "Closed" in right_text else "Open"
except Exception as e:
    print("Error while processing:", e)
    monday_hours, saturday_hours, holiday = "Unavailable", "Unavailable", "Unavailable"

# Combine opening times into a single string
opening_times = (
    f"Monday to Friday: {monday_hours},"
    f"Saturday & Sunday: {saturday_hours}"
     
)
print("Formatted Opening Times:", opening_times)


driver.get(menu_url)
# Find all menu item cards
menu_items = driver.find_elements(By.CLASS_NAME, "card-body")
# Extract names and prices
menu_data = []
for item in menu_items:
    name = item.find_element(By.TAG_NAME, "h5").text
    price = item.find_element(By.CLASS_NAME, "text-muted").text.strip('$')
    menu_data.append({"Restaurant": title, "Address": address, "Opening Hours": opening_times,"Holiday": holiday, "Name": name, "Price": price})

with open('menu_data.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=["Restaurant", "Address", "Opening Hours","Holiday", "Name", "Price"])
    writer.writeheader()
    writer.writerows(menu_data)

# Close the driver
driver.quit()

print("Data saved to CSV files.")