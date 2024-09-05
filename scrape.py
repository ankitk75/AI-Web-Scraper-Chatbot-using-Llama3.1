import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import time

load_dotenv()

def scrape_website(website):
    # print("Launching chrome browser...")
    # chrome_driver_path = "./chromedriver"  # Ensure the path is correct
    # options = webdriver.ChromeOptions()
    # driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)

    print("Launching Safari browser...")
    options = webdriver.SafariOptions()
    driver = webdriver.Safari(options=options)

    try:
        driver.get(website)
        print("Page loaded...")
        html = driver.page_source

        return html

    finally:
        driver.quit()

def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""


def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")

    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    # Get text or further process the content
    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )

    return cleaned_content


def split_dom_content(dom_content, max_length=6000):
    return [
        dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length)
    ]


# For Commercial Use to bypass CAPTCHA and other bot detection mechanisms

# SBR_WEBDRIVER = os.getenv("SBR_WEBDRIVER")

# def scrape_website(website):
#     print("Connecting to Scraping Browser...")
#     sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, "goog", "chrome")
#     with Remote(sbr_connection, options=ChromeOptions()) as driver:
#         driver.get(website)
#         print("Waiting captcha to solve...")
#         solve_res = driver.execute(
#             "executeCdpCommand",
#             {
#                 "cmd": "Captcha.waitForSolve",
#                 "params": {"detectTimeout": 10000},
#             },
#         )
#         print("Captcha solve status:", solve_res["value"]["status"])
#         print("Navigated! Scraping page content...")
#         html = driver.page_source
#         return html