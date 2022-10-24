from operator import contains
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.common import exceptions  
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from time import sleep
from io import BytesIO
import requests
import os

from pathlib import Path
from os import listdir

scriptDirectory = Path().absolute()
try:
    os.makedirs('Images')
except FileExistsError:
    pass
images_dir = f'{scriptDirectory}\\Images'
chrome_options = Options()
chrome_options.add_argument(f"user-data-dir={scriptDirectory}\\userdata")
driver = webdriver.Chrome('D:\\Selenium_drivers\\chromedriver.exe',options=chrome_options)
driver.maximize_window()
driver.get('https://www.grailed.com/users/sign_up')  # Already authenticated
sleep(3)
sell_xpath = '//*[@id="globalHeaderWrapper"]/div/div[2]/a[2]'
driver.find_element(by=By.XPATH, value = sell_xpath).click()


def category():
    try:
        driver.find_element(by=By.XPATH, value="//input[@placeholder='Category']").click()
        driver.find_element(By.CSS_SELECTOR, ".tops").click()
        driver.find_element(By.CSS_SELECTOR, ".tops\\.long_sleeve_shirts").click()
    except Exception as e:
        print ('CATEGORY is not found...pls check xpath!' + e)

def title():
    try:
        title = driver.find_element(by=By.NAME, value='title')
        title.click()
        title.clear()
        title.send_keys("black tshirt")
    except Exception as e:
        print ('TITLE is not found...pls check xpath!' + e)

def designer():
    try:
        sent_key = 'Nike'
        print (f'{sent_key = }')
        designer = driver.find_element(By.ID, "designer-autocomplete") # print (designer.rect)
        designer.click()
        sleep(1)
        designer.send_keys(sent_key)
        sleep(3)
        elems = driver.find_elements(By.XPATH, '//*[@id="SellForm"]/div/div[2]/form/div[1]/div/div[1]/div[2]/div/ul/li')
        # [el.click() for el in elems if el.text == sent_key]
        error=0
        for el in elems:
            if el.text in sent_key:
                print('designer exists')
                el.click()
                error=0
                break
            else:
                error=1
        if error==1:
            elem = driver.find_element(By.XPATH, '//*[@id="SellForm"]/div/div[2]/form/div[1]/div/div[1]/div[2]/div/ul/li[1]')
            elem.click()
    except StaleElementReferenceException as e:
        print(e)
    except Exception as e:
        print ('DESIGNER is not found...pls check xpath!' + e)

def size():
    try:
        select = Select(driver.find_element(by=By.NAME, value='size'))
        select.select_by_visible_text('US S / EU 44-46 / 1')
    except ElementClickInterceptedException:
        print ('Element qe sklikohet')
    except Exception as e:
        print ('SIZE is not found...pls check xpath!' + e)

def color():
    try:
        sent_key = 'Blu'
        print (f'{sent_key = }')
        color = driver.find_element(By.XPATH, value='//*[@id="color-autocomplete"]')
        axisY = color.rect['y']
        cursorr = f"window.scrollTo(0, {axisY - 300}, 'smooth');"
        driver.execute_script(cursorr)
        sleep(2)
        color.click()
        sleep(1)
        color.send_keys(sent_key)
        sleep(3)
        elems = driver.find_elements(By.XPATH, '//*[@id="SellForm"]/div/div[2]/form/div[2]/ul/li')
        # [el.click() for el in elems if el.text == sent_key]
        error=0
        for el in elems:
            if el.text in sent_key:
                print('color exists')
                el.click()
                error=0
                break
            else:
                error=1
        if error==1:
            elem = driver.find_element(By.XPATH, '//*[@id="SellForm"]/div/div[2]/form/div[2]/ul/li[1]')
            elem.click()
    except StaleElementReferenceException as e:
        print(e)
    except Exception as e:
        print ('DESIGNER is not found...pls check xpath!' + e)

def condition():
    try:
        select = Select(driver.find_element(by=By.NAME, value='condition'))
        select.select_by_visible_text('Gently Used')
    except ElementClickInterceptedException:
        print ('Element qe sklikohet')
    except Exception as e:
        print ('CONDITION is not found...pls check xpath!' + e)

def description():
    try:
        desc = driver.find_element(By.XPATH, value="//textarea[@name='description']")
        axisY = desc.rect['y']
        cursorr = f"window.scrollTo(0, {axisY - 300}, 'smooth');"
        driver.execute_script(cursorr)
        sleep(1)
        desc.click()
        desc.send_keys("cool and handy tshirt")
    except Exception as e:
        print ('DESCRIPTION is not found...pls check xpath!' + e)

def measurements():
    try:
        driver.find_element_by_xpath("//div[@id='SellForm']/div/div[2]/form/div[5]/div[3]/div/div[2]/input").click()
        driver.find_element_by_xpath("//input[@value='44']").clear()
        driver.find_element_by_xpath("//input[@value='44']").send_keys("44")
        sleep(0.5)
        driver.find_element_by_xpath("//div[@id='SellForm']/div/div[2]/form/div[5]/div[3]/div[2]/div[2]/input").click()
        driver.find_element_by_xpath("//input[@value='55']").clear()
        driver.find_element_by_xpath("//input[@value='55']").send_keys("55")
        sleep(0.5)
        driver.find_element_by_xpath("//div[@id='SellForm']/div/div[2]/form/div[5]/div[3]/div[3]/div[2]/input").click()
        driver.find_element_by_xpath("//input[@value='66']").clear()
        driver.find_element_by_xpath("//input[@value='66']").send_keys("66")
        sleep(0.5)
        driver.find_element_by_xpath("//div[@id='SellForm']/div/div[2]/form/div[5]/div[3]/div[4]/div[2]/input").click()
        driver.find_element_by_xpath("//input[@value='77']").clear()
        driver.find_element_by_xpath("//input[@value='77']").send_keys("77")
        sleep(0.5)
        driver.find_element_by_xpath("//div[@id='SellForm']/div/div[2]/form/div[5]/div[3]/div[5]/div[2]/input").click()
        driver.find_element_by_xpath("//input[@value='88']").clear()
        driver.find_element_by_xpath("//input[@value='88']").send_keys("88")
    except NoSuchElementException:
        print ('Element is not found...pls check xpath!')

def tags():
    try:
        driver.find_element_by_xpath("//div[@id='SellForm']/div/div[2]/form/div[6]/div[2]/ul/li/input").click()
        driver.find_element_by_xpath("//input[@value='loveit']").clear()
        driver.find_element_by_xpath("//input[@value='loveit']").send_keys("loveit")
    except NoSuchElementException:
        print ('Element is not found...pls check xpath!')

def price():
    try:
        price = driver.find_element(by=By.NAME, value="price")
        axisY = price.rect['y']
        cursorr = f"window.scrollTo(0, {axisY - 300}, 'smooth');"
        driver.execute_script(cursorr)
        sleep(1)
        price.click()
        price.send_keys("80")
    except Exception as e:
        print ('PRICE is not found...pls check xpath!' + e)

def cancel_smart_pricing():
    try:
        sprice = driver.find_element(By.XPATH, value='//*[@id="SellForm"]/div/div[2]/form/div[7]/div[2]/div[1]/div[2]/label/span[2]')
        sprice.click()
    except Exception as e:
        print ('SMART is not found...pls check xpath!' + e)

def download_images(row):
    [f.unlink() for f in Path(images_dir).glob("*") if f.is_file()]
    img_len = len(row['images'])
    for i in range(0, img_len):
        print(f"iteration: {i}")
        img_url = row['images'][i]
        print(f'img url: {img_url}')  ### 'https://s3.eu-west-1.amazonaws.com/twig.sales/053cc1a7bf9445e7971a3f35fed74b6d'
        img_name = img_url.split("/")[-1]  ###  053cc1a7bf9445e7971a3f35fed74b6d
        picture_req = requests.get(img_url)
        if picture_req.status_code == 200:
            with open(f"Images/{img_name}.jpg", 'wb') as f:
                f.write(picture_req.content)
        else:
            print (f'Image {i}: {img_url} is not downloaded!')

def photos():
    try:
        photos = driver.find_element(By.XPATH, value='//*[@id="photos"]/div[1]/h3')
        axisYp = photos.rect['y']
        print (f'{axisYp = }')
        cursorrp = f"window.scrollTo(0, {axisYp - 10}, 'smooth');"
        print (f'{cursorrp = }')
        driver.execute_script(cursorrp)
        sleep(1)
        for iteer, images in enumerate(os.listdir(images_dir)):
            if (images.endswith(".jpg")):
                print (f"Imagepath {iteer}: {images_dir}\\{images}")
                driver.find_element(by=By.XPATH, value=f"//input[@id='photo_input_{iteer}']").send_keys(f"{images_dir}\\{images}")
                sleep(7)
        sleep(5)
    except NoSuchElementException:
        print ('PHOTO is not found...pls check xpath!')

def save_as_draft():
    try:
        driver.find_element(By.XPATH, value='//*[@id="SellForm"]/div/div[2]/form/div[10]/div/button[1]').click()
    except NoSuchElementException:
        print ('DRAFT is not found...pls check xpath!')

def publish():
    try:
        driver.find_element(By.XPATH, value='//*[@id="SellForm"]/div/div[2]/form/div[10]/div/button[2]').click()
    except NoSuchElementException:
        print ('PUBLISH is not found...pls check xpath!')

def payload():
    '''
        Call other functions that are required for payload in order to publish items.
    '''
    driver.implicitly_wait(10)
    print ('Jemi mrenaaaa!!!')
    sleep(3)

    ## CATEGORY
    print ("*** Hyjme te CATEGORY ***")
    category()
    sleep(1)

    ## ITEM NAME/TITLE
    print ("*** Hyjme te TITLE ***")
    title()
    sleep(1)

    # DESIGNER
    print ("*** Hyjme te DESIGNER ***")
    designer()
    sleep(2)

    ## SIZE
    print ("*** Hyjme te SIZE ***")
    size()
    sleep(2)

    ## COLOR
    print ("*** Hyjme te COLOR ***")
    color()
    sleep(1)

    ## CONDITION
    print ("*** Hyjme te CONDITION ***")
    condition()
    sleep(2)

    # ## DESCRIPTION
    print ("*** Hyjme te DESCRIPTION ***")
    description()
    sleep(2)

    ## MEASUREMENTS
    # measurements()
    # sleep(0.5)

    ## TAGS
    # tags()
    # sleep(0.5)

    ## PRICE
    print ("*** Hyjme te PRICE ***")
    price()
    sleep(2)

    print ("*** Cancel SMART PRICING ***")
    cancel_smart_pricing()
    sleep(3)

    ### UPLOAD IMAGES
    print ("*** Hyjme te DOWNLADIMI I IMAZHEVE ***")
    download_images(row)

    # PHOTOS - Po funksionon.
    print ("*** Hyjme te UPLODIMI I IMAZHEVE ***")
    photos()

    with open('content.html', 'w', encoding='utf8') as aa:
        aa.write(driver.page_source)

    #SAVE AS DRAFT
    save_as_draft()

    #PUBLISH
    # publish()

    sleep(5)
    # driver.delete_all_cookies()
    # driver.close()
    driver.quit()
    print ('FINISHED!!!')

if __name__ == "__main__":
    row = {'images': [
        'https://s3.eu-west-1.amazonaws.com/twig.sales/6d591a8463a1456a8f0b0b1e47ae0e1b', 
        'https://s3.eu-west-1.amazonaws.com/twig.sales/6dc1442cecbf48e4b8951a1059d77f50', 
        'https://s3.eu-west-1.amazonaws.com/twig.sales/73b7044fe96549299295a93a9fa2812d'
    ]}
    payload()