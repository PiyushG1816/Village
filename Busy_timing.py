from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

# Setup ChromeDriver
service = Service()  # Update with your ChromeDriver path
driver = webdriver.Chrome()

# Open the Google Maps URL
url = "https://www.google.com/maps/place/Village+-+The+Soul+of+India/@40.7665603,-73.5261129,17z/data=!3m1!4b1!4m6!3m5!1s0x89c281752d83843d:0x1f2a365d2207b71c!8m2!3d40.7665603!4d-73.523538!16s%2Fg%2F11thj448_5?entry=ttu&g_ep=EgoyMDI0MTIxMC4wIKXMDSoJLDEwMjExMjM0SAFQAw%3D%3D"
driver.get(url)

# Wait for the page to load
driver.implicitly_wait(10)

wait = WebDriverWait(driver, 10)
popular_times_sections = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'g2BVhd')))

popular_times_data = {}


# Locate Popular Times elements
popular_times = driver.find_elements(By.CLASS_NAME, 'g2BVhd')

days_of_week = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
for day_idx, section in enumerate(popular_times_sections):
    # Extract hourly data for the current day
    hourly_data = section.find_elements(By.CLASS_NAME, 'dpoVLd')
    times = []
    for hour in hourly_data:
        aria_label = hour.get_attribute('aria-label')
        if aria_label:
            time_value = int(aria_label.split('%')[0])  # Extract busy percentage
            times.append(time_value)
        else:
            times.append(0)  # If no data, assume 0% busy
    popular_times_data[days_of_week[day_idx]] = times

# Close the browser
driver.quit()

# Print the extracted data
time_slots = [f"{hour}:00" for hour in range(6, 24)] 
csv_data = [["Day"] + time_slots]
for day in days_of_week:
    # Each row is a day with corresponding time slots
    row = [day] + popular_times_data.get(day, [])
    csv_data.append(row)

# Write to a CSV file
csv_file = "popular_times.csv"
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(csv_data)

print(f"Popular times data saved to {csv_file}")