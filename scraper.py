from selenium import webdriver
from config import CHROMEDRIVER_PATH
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pandas as pd


# Chrome options (headless + hide logs)
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run without GUI
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

# Setup driver
service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open website
driver.get("https://www.adamchoi.co.uk/overs/detailed")

# Click on "All Matches" button
all_matches_button = driver.find_element(By.XPATH, '//*[@id="page-wrapper"]/div/home-away-selector/div/div/div/div/label[2]')
all_matches_button.click()

# Collect matches
matches = driver.find_elements(By.TAG_NAME, "tr")

date = []
home_team = []
result = []
away_team = []

# Extract table data
for match in matches:
    cells = match.find_elements(By.TAG_NAME, "td")
    if len(cells) >= 5:  # avoid header row
        date.append(cells[0].text)
        home_team.append(cells[2].text)
        result.append(cells[3].text)
        away_team.append(cells[4].text)

# Create DataFrame
df = pd.DataFrame({
    "date": date,
    "home_team": home_team,
    "score": result,
    "away_team": away_team
})

# Save to CSV (without index)
df.to_csv("football_data.csv", index=False)

# Close driver
driver.quit()

print("Scraping complete! Data saved to football_data.csv")

