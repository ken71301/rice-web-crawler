import json

from selenium import webdriver
from bs4 import BeautifulSoup


def get_titles_subtitles_traits(driver):
    # Navigate to the main page
    driver.get("https://rice.sinica.edu.tw/TRIM2/showTraits.php")

    # Parse the HTML of the main page
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Create a dictionary to store the results
    results = {}

    # Find all the tr elements in the table
    rows = soup.find_all("tr")

    current_main_title = None
    current_subtitles = None
    for row in rows:
        main_title_td = row.find("td", {"bgcolor": "#ccffcc"})
        subtitle_td = row.find("td", {"bgcolor": "#99ff99"})

        # If the row contains a main title, update the current main title
        if main_title_td is not None:
            current_main_title = main_title_td.text
            results[current_main_title] = {}
            current_subtitles = results[current_main_title]

        # If the row contains a subtitle, add it to the list of subtitles for the current main title
        if subtitle_td is not None and current_main_title is not None:
            subtitle = subtitle_td.text
            current_subtitles[subtitle] = []

            # Navigate to the subpage
            driver.get("https://rice.sinica.edu.tw/TRIM2/" + subtitle_td.a["href"])
            
            # Parse the HTML of the subpage
            subpage_soup = BeautifulSoup(driver.page_source, "html.parser")
            
            # Find the table with border=1
            table = subpage_soup.find("table", {"border": "1"})

            # Find all the trait IDs in the table
            for trait in table.find_all("td"):
                current_subtitles[subtitle].append(trait.text)

    return results


# Initialize the Selenium webdriver
driver = webdriver.Chrome()

# Use the function
results = get_titles_subtitles_traits(driver)

print(results)

# for main_title, subtitles in results.items():
#     print(f"Main title: {main_title}")
#     for subtitle, traits in subtitles.items():
#         print(f"\tSubtitle: {subtitle}, Traits: {traits}")
with open('results.json', 'w') as f:
    json.dump(results, f)
    
# Close the Selenium webdriver
driver.quit()
