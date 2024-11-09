import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup

def scrape_website(url):
    print("Launching Chrome Browser...")
    chrome_driver_path = "./chromedriver.exe"
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)

    try:
        driver.get(url)
        print("page loaded")
        html = driver.page_source
        return html
    except Exception as e:
        print("An error occurred: ", e)
    finally:
        driver.quit()
        print("Browser closed")

def extract_title(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup.title.string

def extract_body_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    body_content = soup.body
    if body_content:
        return body_content.get_text(strip=True)
    else:
        return "No body content found"
    
def clean_body_content(text, url):
    soup = BeautifulSoup(text, 'html.parser')

    for script_or_style in soup(['script', 'style']):
        script_or_style.extract()

    cleaned_text = soup.get_text(separator="\n")
    if "hindustantimes.com" in url:
        title = soup.title.string
        cleaned_text = cleaned_text.split(title, 1)[-1].strip()
    if "thehindu.com" in url:
        read_comments_index = cleaned_text.find("Read Comments")
        if read_comments_index != -1:
            cleaned_text = cleaned_text[:read_comments_index]
    
    cleaned_content = "\n".join([line.strip() for line in cleaned_text.splitlines() if line.strip()])
    
    return cleaned_content

def split_into_sections(text, max_length=8000):
    return [text[i:i+max_length] for i in range(0, len(text), max_length)]
