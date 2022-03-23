import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, SessionNotCreatedException
import pytz
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, date, timedelta
import yaml
import logging 
import logging.handlers
import pandas as pd
from apscheduler.schedulers.background import BackgroundScheduler
sched = BackgroundScheduler()

flag = 0
point = 0
movie_alert_list = []
movie_alert_dict = {}
daily_mail = []
daily_dict = {}
theatres_dict = {}
theatres_list = []
movie_counting_list = []
movie_release_date = {}
movie_ignore_list = []
cinema_dict = {}
exception_dict = {}

movie_released_list = []

def web_scrape():
    try:
        time_now = str(datetime.now()).split(":")[0]
        global exception_dict
        global cinema_dict
        pd.set_option('display.max_colwidth', None)
        logger.info("***************************************")
        logger.info("Initiating Web Driver to start scraping")
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--remote-debugging-port=9222')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("start-maximized")
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-software-rasterizer')
        chrome_options.binary_location="C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
        s = Service("G:\\Selenium Browser Drivers\\chromedriver.exe")
        browser = webdriver.Chrome(service=s,options=chrome_options)
        URL = "https://in.bookmyshow.com/explore/home/hyderabad"

        logger.info("Checking for backup config file")
        primary_path = "G:\\Python Programs\\GIT Projects\\BookMyShow_BOT\\resources\\config.yml"
        backup_path = "G:\\Python Programs\\GIT Projects\\BookMyShow_BOT\\resources\\config1.yml"
        try:
            if os.path.exists(backup_path):
                logger.info("Found backup file, replacing the configuration to match latest input")
                os.remove(primary_path)
                os.rename(backup_path,primary_path)
                logger.info("Updated the configuration with latest user inputs")
            else:
                logger.info("Didn't find backup config file, utilizing the primary configuration")
        except Exception as err:
            logger.error(err)
        file = open("../resources/config.yml", "r")
        CONFIG_FILE = yaml.load(file,Loader=yaml.FullLoader)
        logger.info("Loaded the latest configuration given by the user")
        email_list = [i for i in CONFIG_FILE['Emails']]
        email_one = CONFIG_FILE['Emails'][0]
        
        logger.info("Starting Web-Scrape")

    except SessionNotCreatedException as err:
        logger.error("Facing issues with Chrome Instance")
        primary_path = "G:\\Python Programs\\GIT Projects\\BookMyShow_BOT\\resources\\config.yml"
        backup_path = "G:\\Python Programs\\GIT Projects\\BookMyShow_BOT\\resources\\config1.yml"
        try:
            if os.path.exists(backup_path):
                logger.info("Found backup file, replacing the configuration to match latest input")
                os.remove(primary_path)
                os.rename(backup_path,primary_path)
                logger.info("Updated the configuration with latest user inputs")
            else:
                logger.info("Didn't find backup config file, utilizing the primary configuration")
        except Exception as err:
            logger.error(err)

        file = open("../resources/config.yml", "r")
        CONFIG_FILE = yaml.load(file,Loader=yaml.FullLoader)
        logger.info("Loaded the latest configuration given by the user")
        email_one = CONFIG_FILE['Emails'][0]

        if 'SessionNotCreatedException' in exception_dict.keys():
            if exception_dict['SessionNotCreatedException'] != time_now:
                logger.error("Alerting script master via e-mail about the exception")
                send_exception_mail(email_one,err,'SessionNotCreatedException',81)
                exception_dict['SessionNotCreatedException'] = time_now
            else:
                logger.error("Already sent the mail this hour, skipping now")
        else:
            logger.error("Alerting script master via e-mail about the exception")
            send_exception_mail(email_one,err,'SessionNotCreatedException',81)
            exception_dict['SessionNotCreatedException'] = time_now

    except Exception as err:
        logger.error("Facing issues with Chrome Instance")
        primary_path = "G:\\Python Programs\\GIT Projects\\BookMyShow_BOT\\resources\\config.yml"
        backup_path = "G:\\Python Programs\\GIT Projects\\BookMyShow_BOT\\resources\\config1.yml"
        try:
            if os.path.exists(backup_path):
                logger.info("Found backup file, replacing the configuration to match latest input")
                os.remove(primary_path)
                os.rename(backup_path,primary_path)
                logger.info("Updated the configuration with latest user inputs")
            else:
                logger.info("Didn't find backup config file, utilizing the primary configuration")
        except Exception as err:
            logger.error(err)

        file = open("../resources/config.yml", "r")
        CONFIG_FILE = yaml.load(file,Loader=yaml.FullLoader)
        logger.info("Loaded the latest configuration given by the user")
        email_one = CONFIG_FILE['Emails'][0]
       
        if type(err).__name__ in exception_dict.keys():
            if exception_dict[type(err).__name__] != time_now:
                logger.error("Alerting script master via e-mail about the exception")
                send_exception_mail(email_one,err,type(err).__name__,113)
                exception_dict[type(err).__name__] = time_now
            else:
                logger.error("Already sent the mail this hour, skipping now")
        else:
            logger.error("Alerting script master via e-mail about the exception")
            send_exception_mail(email_one,err,type(err).__name__,113)
            exception_dict[type(err).__name__] = time_now

    try:
        browser.get(URL)
    except Exception as err:
        logger.error("Unable to reach Bookmyshow")
    try:
        browser.implicitly_wait(10)
        logger.info("Successfully reached Bookmyshow")
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[1]/div[2]/header/div[2]/div/div/div/div[1]/div/a[1]")))
    except Exception as err:
        logger.error(err)
        if type(err).__name__ in exception_dict.keys():
            if exception_dict[type(err).__name__] != time_now:
                logger.error("Alerting script master via e-mail about the exception")
                send_exception_mail(email_one,err,type(err).__name__,153)
                exception_dict[type(err).__name__] = time_now
            else:
                logger.error("Already sent the mail this hour, skipping now")
        else:
            logger.error("Alerting script master via e-mail about the exception")
            send_exception_mail(email_one,err,type(err).__name__,153)
            exception_dict[type(err).__name__] = time_now
    
    df_all_showing_info = pd.DataFrame(columns = ['Movie Name','Status'])
    df_alert_info = pd.DataFrame(columns = ['Movie Name','Status','Requested By','Comment'])
    df_cinema_update_info = pd.DataFrame(columns = ['Movie','Theatre','Show Timings'])
    df_show_update_info = pd.DataFrame(columns = ['Movie','Theatre','New Show(s) Added','Show Timings'])

    if not CONFIG_FILE['Force']['Mode']:
        logger.info("Force Mode - OFF : Going Full-Mode")
        now_showing_top = []
        try:
            for i in range(5):
                current = f"/html/body/div[1]/div[1]/div[2]/div[2]/div[1]/div[2]/div/div/div/div[2]/div/div[1]/div[{i+1}]/a/div/div[2]/div/img"
                now_showing_top.append(browser.find_element(By.XPATH, current).get_attribute('alt'))
        except NoSuchElementException:
            logger.error("There are less than 5 movies currently running")
        except Exception as err:
            logger.error(err)
            if type(err).__name__ in exception_dict.keys():
                if exception_dict[type(err).__name__] != time_now:
                    logger.error("Alerting script master via e-mail about the exception")
                    send_exception_mail(email_one,err,type(err).__name__,181)
                    exception_dict[type(err).__name__] = time_now
                else:
                    logger.error("Already sent the mail this hour, skipping now")
            else:
                logger.error("Alerting script master via e-mail about the exception")
                send_exception_mail(email_one,err,type(err).__name__,181)
                exception_dict[type(err).__name__] = time_now

        logger.info(f"Got list of Top-5 Movies currently open for bookings : {', '.join(now_showing_top)}")

        logger.info("Getting the list of all movies with bookings open")

        browser.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[2]/header/div[2]/div/div/div/div[1]/div/a[1]").click()
        browser.implicitly_wait(10)

        all_showing = []
        all_showing_xpath = []
        count = 0
        try:
            for i in range(50):
                if i // 4 == 0:
                    count += 1
                    all = f"/html/body/div[1]/div[1]/div[2]/div[4]/div[2]/div[4]/div/div/div[2]/a[{count}]/div/div[2]/div/img"
                    all_showing_xpath.append(all)
                    all_showing.append(browser.find_element(By.XPATH, all).get_attribute('alt'))
                else:
                    count += 1
                    if count > 4:
                        count = 1
                    all = f"/html/body/div[1]/div[1]/div[2]/div[4]/div[2]/div[{4+(i//4)}]/div/div/div[2]/a[{count}]/div/div[2]/div/div/img"
                    all_showing_xpath.append(all)
                    all_showing.append(browser.find_element(By.XPATH, all).get_attribute('alt'))
        except NoSuchElementException:
            try:
                all = f"/html/body/div[1]/div[1]/div[2]/div[4]/div[2]/div[{4+(i//4)}]/div/div/div[2]/a/div/div[2]/div/div/img"
                all_showing_xpath.append(all)
                all_showing.append(browser.find_element(By.XPATH, all).get_attribute('alt'))
            except NoSuchElementException:
                logger.info(f"Found {i} movies with bookings open")
            except Exception as err:
                logger.error(err)
            
        except Exception as err:
            logger.error(err)
            if type(err).__name__ in exception_dict.keys():
                if exception_dict[type(err).__name__] != time_now:
                    logger.error("Alerting script master via e-mail about the exception")
                    send_exception_mail(email_one,err,type(err).__name__,229)
                    exception_dict[type(err).__name__] = time_now
                else:
                    logger.error("Already sent the mail this hour, skipping now")
            else:
                logger.error("Alerting script master via e-mail about the exception")
                send_exception_mail(email_one,err,type(err).__name__,229)
                exception_dict[type(err).__name__] = time_now

        logger.info(f"Got list of all movies open for bookings: {', '.join(all_showing)}")

        logger.info("Preparing Data Frames for sending any e-mail alerts if needed")

        global movie_ignore_list
        for keys,values in CONFIG_FILE['Movies'].items():
            for value in values:
                if value in movie_release_date:
                    today_month = int((str(datetime.now())).split(" ")[0].split("-")[2])
                    today_date = int((str(datetime.now())).split(" ")[0].split("-")[1])
                    if movie_release_date[value][0] < today_date and movie_release_date[value][1] <= today_month:
                        movie_ignore_list.append(value)
        try:
            global movie_released_list
            if all_showing:
                alert_list = []
                all_list = []
                for movies in all_showing:
                    all_showing_dict = {}
                    all_showing_dict['Movie Name'] = movies
                    all_showing_dict['Status'] = "Open"
                    all_list.append(all_showing_dict)

                logger.info(f"Checking whether the movie(s) you want have opened bookings or not")

                for keys,values in CONFIG_FILE['Movies'].items():
                    for value in values:
                        if value in all_showing and value not in movie_ignore_list:
                            global movie_alert_dict
                            global movie_alert_list

                            alert_dict = {}
                            alert_dict['Movie Name'] = value
                            alert_dict['Status'] = 'Bookings Opened'
                            alert_dict['Requested By'] = keys
                            alert_dict['Comment'] = 'Please take necessary action'
                            alert_list.append(alert_dict)
                            check_count = 0
                            if movie_alert_list:
                                for index in range(len(movie_alert_list)):
                                    if value in movie_alert_list[index]:
                                        movie_alert_list[index][value] += 1
                                    elif value not in movie_alert_list[index]:
                                        check_count += 1
                                if check_count == len(movie_alert_list):
                                    movie_alert_dict[value] = 1
                                    movie_alert_list.append(movie_alert_dict)
                                    movie_alert_dict = {}
                            else:
                                movie_alert_dict[value] = 1
                                movie_alert_list.append(movie_alert_dict)
                                movie_alert_dict = {}

                df_all_showing_data = pd.DataFrame(all_list,index = None)

                df_alert_data = pd.DataFrame(alert_list,index = None)

                try:
                    df_alert_info = pd.merge(df_alert_info,df_alert_data,how = 'outer')
                except pd.errors.MergeError:
                    logger.info("Movies in your wish-lists are not open for bookings yet")
                except Exception as err:
                    logger.error(err)
                    if type(err).__name__ in exception_dict.keys():
                        if exception_dict[type(err).__name__] != time_now:
                            logger.error("Alerting script master via e-mail about the exception")
                            send_exception_mail(email_one,err,type(err).__name__,304)
                            exception_dict[type(err).__name__] = time_now
                        else:
                            logger.error("Already sent the mail this hour, skipping now")
                    else:
                        logger.error("Alerting script master via e-mail about the exception")
                        send_exception_mail(email_one,err,type(err).__name__,304)
                        exception_dict[type(err).__name__] = time_now

                try:
                    df_all_showing_info = pd.merge(df_all_showing_info,df_all_showing_data,how = 'outer')
                except Exception as err:
                    logger.error(err)
                    if type(err).__name__ in exception_dict.keys():
                        if exception_dict[type(err).__name__] != time_now:
                            logger.error("Alerting script master via e-mail about the exception")
                            send_exception_mail(email_one,err,type(err).__name__,320)
                            exception_dict[type(err).__name__] = time_now
                        else:
                            logger.error("Already sent the mail this hour, skipping now")
                    else:
                        logger.error("Alerting script master via e-mail about the exception")
                        send_exception_mail(email_one,err,type(err).__name__,320)
                        exception_dict[type(err).__name__] = time_now

                if not df_alert_info.empty:
                    global flag
                    flag += 1
                    for index1 in range(len(alert_list)):
                        for index2 in range(len(movie_alert_list)):
                            if alert_list[index1]['Movie Name'] in movie_alert_list[index2]:
                                movie = alert_list[index1]['Movie Name']
                                if movie_alert_list[index2][movie] == 1:
                                    logger.info(f"{alert_list[index1]['Movie Name']} is now open for booking, alerting everyone via e-mail")
                                    send_alert_mail(email_list,df_alert_info,alert_list[index1]['Movie Name'])
                
                logger.info("Starting to check for theatre and show updates for movies in your wish-list")
                for keys,values in CONFIG_FILE['Movies'].items():
                    global movie_counting_list
                    for value in values:
                        if value not in movie_ignore_list:
                            movie_counter_machine = {}
                            if value in all_showing:
                                if movie_released_list:
                                    for index in range(len(movie_released_list)):
                                        if value in movie_released_list[index]:
                                            movie_counter_machine[value] = movie_released_list[index][value]
                                movie_released_dict = {}
                                i = all_showing.index(value)
                                WebDriverWait(browser, 60).until(EC.element_to_be_clickable((By.XPATH, all_showing_xpath[i])))
                                button = browser.find_element(By.XPATH,all_showing_xpath[i])
                                browser.execute_script("arguments[0].click();", button)
                                browser.implicitly_wait(10)
                                try:
                                    release = "/html/body/div[1]/div[1]/div[2]/section[1]/div/div/div[2]/section/div[2]/div[2]/div/span[1]"
                                    release_date = browser.find_element(By.XPATH,release).text
                                except NoSuchElementException as err:
                                    logger.info(f"{value} - already released")
                                    movie_ignore_list.append(value)
                                    continue
                                except Exception as err:
                                    logger.err(err)
                                    if type(err).__name__ in exception_dict.keys():
                                        if exception_dict[type(err).__name__] != time_now:
                                            logger.error("Alerting script master via e-mail about the exception")
                                            send_exception_mail(email_one,err,type(err).__name__,369)
                                            exception_dict[type(err).__name__] = time_now
                                        else:
                                            logger.error("Already sent the mail this hour, skipping now")
                                    else:
                                        logger.error("Alerting script master via e-mail about the exception")
                                        send_exception_mail(email_one,err,type(err).__name__,369)
                                        exception_dict[type(err).__name__] = time_now

                                if value not in movie_release_date:
                                    temp_list = []
                                    temp_list.append(int(release_date.split(" on ")[1].split(" ")[0]))
                                    months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
                                    temp_index = months.index(release_date.split(" "+str(temp_list[0])+" ")[1].split(",")[0])
                                    temp_list.append(int(temp_index+1))
                                    movie_release_date[value] = temp_list
                                release_date_num = release_date.split(" on ")[1].split(" ")[0]

                                windows = []
                                titles = []
                                temp_count = 0
                                logger.info(f"Opening {len(CONFIG_FILE['Theatres'])} tabs to search for theatres")
                                for theatres in CONFIG_FILE['Theatres']:
                                    temp_count += 1
                                    browser.execute_script(f"window.open('about:blank', 'tab{temp_count}');")
                                    windows.append(f"tab{temp_count}")
                                    browser.switch_to.window(windows[temp_count-1])
                                    browser.get(theatres)
                                    browser.implicitly_wait(10)
                                    titles.append(browser.title.split("|")[0])
                                    logger.info(f"Switched to {windows[temp_count-1]} : {titles[temp_count-1]}")
                                for i in range(len(windows)):
                                    browser.switch_to.window(windows[i])
                                    try:
                                        for j in range(30):
                                            movie_date = f"/html/body/div[5]/section[1]/div/div/div/div/div[1]/ul/div/div/li[{j+1}]/a/div[1]"
                                            a = browser.find_element(By.XPATH,movie_date).text 
                                            if a == release_date_num:
                                                browser.find_element(By.XPATH,movie_date).click()
                                                browser.implicitly_wait(10)
                                                for k in range(2,20):
                                                    movie_name = f"/html/body/div[5]/section[2]/div/div/ul/li[{k}]/div[1]/div[1]/span/a"
                                                    b = browser.find_element(By.XPATH,movie_name).text 
                                                    if b == value:
                                                        show_list = []
                                                        for l in range(1,50):
                                                            show_timings = f"/html/body/div[5]/section[2]/div/div/ul/li[2]/div[2]/div[{l}]/a/div/div"
                                                            try:
                                                                show_list.append(browser.find_element(By.XPATH,show_timings).text)
                                                            except NoSuchElementException:
                                                                logger.info(f"Found {l-1} shows for {value} in {titles[i]}")
                                                                break
                                                            except Exception as err:
                                                                logger.error(err)
                                                                if type(err).__name__ in exception_dict.keys():
                                                                    if exception_dict[type(err).__name__] != time_now:
                                                                        logger.error("Alerting script master via e-mail about the exception")
                                                                        send_exception_mail(email_one,err,type(err).__name__,426)
                                                                        exception_dict[type(err).__name__] = time_now
                                                                    else:
                                                                        logger.error("Already sent the mail this hour, skipping now")
                                                                else:
                                                                    logger.error("Alerting script master via e-mail about the exception")
                                                                    send_exception_mail(email_one,err,type(err).__name__,426)
                                                                    exception_dict[type(err).__name__] = time_now
                                                                break                                                       
                                                        cinema_dict[titles[i]] = show_list
                                                        cinema_update_list = []
                                                        show_update_list = []
                                                        if movie_counter_machine:
                                                            if titles[i] not in movie_counter_machine[value].keys():
                                                                logger.info(f"New theatre added - {titles[i]}")
                                                                cinema_update = {}
                                                                cinema_update['Movie'] = value
                                                                cinema_update['Theatre'] = titles[i]
                                                                cinema_update['Show Timings'] = ", ".join(show_list)
                                                                cinema_update_list.append(cinema_update)
                                                                movie_counter_machine[value] = cinema_dict.copy()
                                                            elif titles[i] in movie_counter_machine[value].keys():
                                                                if movie_counter_machine[value][titles[i]] != cinema_dict[titles[i]]:
                                                                    if len(list(set(show_list)-set(movie_counter_machine[value][titles[i]]))) == 1:
                                                                        logger.info(f"New show added in {titles[i]}")
                                                                    else:
                                                                        logger.info(f"{len(list(set(show_list)-set(movie_counter_machine[value][titles[i]])))} new shows added in {titles[i]}")
                                                                    show_update = {}
                                                                    show_update['Movie'] = value
                                                                    show_update['Theatre'] = titles[i]
                                                                    show_update['New Show(s) Added'] = ', '.join(list(set(show_list)-set(movie_counter_machine[value][titles[i]])))
                                                                    show_update['Show Timings'] = show_list
                                                                    show_update_list.append(show_update)
                                                                    movie_counter_machine[value] = cinema_dict.copy()
                                                        else:
                                                            logger.info("First theatre added - Alerting instantly")
                                                            cinema_update = {}
                                                            cinema_update['Movie'] = value
                                                            cinema_update['Theatre'] = titles[i]
                                                            cinema_update['Show Timings'] = ", ".join(show_list)
                                                            cinema_update_list.append(cinema_update)
                                                            movie_counter_machine[value] = cinema_dict.copy()
                                                            
                                                        df_cinema_update_data = pd.DataFrame(cinema_update_list,index = None)

                                                        df_show_update_data = pd.DataFrame(show_update_list,index = None)

                                                        try:
                                                            df_cinema_update_info = pd.merge(df_cinema_update_info,df_cinema_update_data,how = 'outer')
                                                        except pd.errors.MergeError:
                                                            pass
                                                        except Exception as err:
                                                            logger.error(err)
                                                            if type(err).__name__ in exception_dict.keys():
                                                                if exception_dict[type(err).__name__] != time_now:
                                                                    logger.error("Alerting script master via e-mail about the exception")
                                                                    send_exception_mail(email_one,err,type(err).__name__,479)
                                                                    exception_dict[type(err).__name__] = time_now
                                                                else:
                                                                    logger.error("Already sent the mail this hour, skipping now")
                                                            else:
                                                                logger.error("Alerting script master via e-mail about the exception")
                                                                send_exception_mail(email_one,err,type(err).__name__,479)
                                                                exception_dict[type(err).__name__] = time_now
                                
                                                        try:
                                                            df_show_update_info = pd.merge(df_show_update_info,df_show_update_data,how = 'outer')
                                                        except pd.errors.MergeError:
                                                            logger.info(f"No new shows added for {value} in {titles[i]}")
                                                        except Exception as err:
                                                            logger.error(err)
                                                            if type(err).__name__ in exception_dict.keys():
                                                                if exception_dict[type(err).__name__] != time_now:
                                                                    logger.error("Alerting script master via e-mail about the exception")
                                                                    send_exception_mail(email_one,err,type(err).__name__,497)
                                                                    exception_dict[type(err).__name__] = time_now
                                                                else:
                                                                    logger.error("Already sent the mail this hour, skipping now")
                                                            else:
                                                                logger.error("Alerting script master via e-mail about the exception")
                                                                send_exception_mail(email_one,err,type(err).__name__,497)
                                                                exception_dict[type(err).__name__] = time_now

                                                        if not df_cinema_update_info.empty:
                                                            logger.info(f"Sending an e-mail alert - {titles[i]} opened for {value}")
                                                            send_theatre_alert_mail(email_list,1,df_cinema_update_info)

                                                        if not df_show_update_info.empty:
                                                            logger.info(f"Sending an e-mail alert - {titles[i]} has new shows for {value}")
                                                            send_theatre_alert_mail(email_list,2,df_show_update_info)
                                                        break
                                                break
                                    except NoSuchElementException:
                                        logger.info(f"Either {value} is not running in {titles[i]} (or) {titles[i]} is unreachable right now")
                                    except Exception as err:
                                        logger.error(err)
                                        if type(err).__name__ in exception_dict.keys():
                                            if exception_dict[type(err).__name__] != time_now:
                                                logger.error("Alerting script master via e-mail about the exception")
                                                send_exception_mail(email_one,err,type(err).__name__,522)
                                                exception_dict[type(err).__name__] = time_now
                                            else:
                                                logger.error("Already sent the mail this hour, skipping now")
                                        else:
                                            logger.error("Alerting script master via e-mail about the exception")
                                            send_exception_mail(email_one,err,type(err).__name__,522)
                                            exception_dict[type(err).__name__] = time_now

                                flag_check = 0
                                logger.info("Updating the main global list with all the latest theatre and show updates, to match for any updates next time")
                                if movie_released_list:
                                    for index in range(len(movie_released_list)):
                                        if value in movie_released_list[index]:
                                            movie_released_list[index][value] = cinema_dict.copy()
                                            break
                                        else:
                                            flag_check += 1
                                    if flag_check == len(movie_released_list):
                                        movie_released_dict[value] = cinema_dict.copy()
                                        movie_released_list.append(movie_released_dict)
                                else:
                                    movie_released_dict[value] = cinema_dict.copy()
                                    movie_released_list.append(movie_released_dict)
                                logger.info("Updated the main global list with all the latest updates")

                                logger.info("Preparing data-frames for theatre or show alerts, if any")

                logger.info(f"Here's the master list: {movie_released_list}")
                browser.quit()
                    
            else:
                logger.info("No movies found which are open for bookings")
            
            if now_showing_top:
                    daily_top5_list = []
                    for movies in now_showing_top:
                        top5_showing_dict = {}
                        top5_showing_dict['Movie Name'] = movies
                        top5_showing_dict['Status'] = "Open for booking"
                        daily_top5_list.append(top5_showing_dict)
                    df_daily_top5_info = pd.DataFrame(columns = ['Movie Name','Status'])
                    df_daily_top5_data = pd.DataFrame(daily_top5_list,index = None)
                    try:
                        df_daily_top5_info = pd.merge(df_daily_top5_info,df_daily_top5_data,how='outer')
                    except pd.errors.MergeError:
                        logger.error("Unable to merge dataframes, please check")
                    except Exception as err:
                        logger.error(err)
                    
                    logger.info("Checking notification conditions, whether I can send summary report at this time or not")

            if not df_daily_top5_info.empty:
                global point
                global daily_mail
                global daily_dict
                point += 1
                if date.today() not in daily_dict.values():
                    point = 1
                    daily_dict['Date'] = date.today()
                    daily_dict['Count'] = point
                    daily_mail.append(daily_dict)
                mail_time = datetime.strftime((datetime.now(pytz.timezone('Asia/Calcutta')) - timedelta()),'%Y-%m-%d %H')
                if (int(mail_time.split(" ")[1]) >= 8 and int(mail_time.split(" ")[1]) < 9) and daily_dict['Count'] < 2:
                    daily_dict['Count'] += 1
                    logger.info("Sending today's BookMyShow summary report on e-mail to all subscribers")
                    send_daily_mail(CONFIG_FILE,df_daily_top5_info,df_all_showing_info)
                elif int(mail_time.split(" ")[1]) < 8 and daily_dict['Count'] < 2:
                    logger.info("Not the correct time to send BookMyShow summary report, will send after 8 AM IST")
                else:
                    logger.info("Already sent the report today, won't send more now")
        except Exception as err:
            logger.error(err)
            if type(err).__name__ in exception_dict.keys():
                if exception_dict[type(err).__name__] != time_now:
                    logger.error("Alerting script master via e-mail about the exception")
                    send_exception_mail(email_one,err,type(err).__name__,598)
                    exception_dict[type(err).__name__] = time_now
                else:
                    logger.error("Already sent the mail this hour, skipping now")
            else:
                logger.error("Alerting script master via e-mail about the exception")
                send_exception_mail(email_one,err,type(err).__name__,598)
                exception_dict[type(err).__name__] = time_now
    else:
        logger.info("Force Mode - ON : Going Quick-Mode")
        for key in CONFIG_FILE['Force'].keys():
            if key != 'Mode':
                value = key
        email_one = CONFIG_FILE['Emails'][0]
        release_date_num = str(CONFIG_FILE['Force'][value]['Release'])
        movie_counter_machine = {}
        if movie_released_list:
            for index in range(len(movie_released_list)):
                if value in movie_released_list[index]:
                    movie_counter_machine[value] = movie_released_list[index][value]
        movie_released_dict = {}
        windows = []
        titles = []
        temp_count = 0
        try:
            logger.info(f"Opening {len(CONFIG_FILE['Force'][value]['Theatres'])} tabs to search for theatres")
            for i in CONFIG_FILE['Force'][value]['Theatres']:
                theatre = CONFIG_FILE['Theatres'][i-1]
                temp_count += 1
                browser.execute_script(f"window.open('about:blank', 'tab{temp_count}');")
                windows.append(f"tab{temp_count}")
                browser.switch_to.window(windows[temp_count-1])
                time.sleep(1)
                browser.get(theatre)
                browser.implicitly_wait(10)
                titles.append(browser.title.split(" | ")[0])
                logger.info(f"Switched to {windows[temp_count-1]} : {titles[temp_count-1]}")
            for i in range(len(windows)):
                browser.switch_to.window(windows[i])
                time.sleep(1)
                try:
                    for j in range(30):
                        movie_date = f"/html/body/div[5]/section[1]/div/div/div/div/div[1]/ul/div/div/li[{j+1}]/a/div[1]"
                        a = browser.find_element(By.XPATH,movie_date).text
                        if a == release_date_num:
                            browser.find_element(By.XPATH,movie_date).click()
                            browser.implicitly_wait(10)
                            for k in range(2,20):
                                movie_name = f"/html/body/div[5]/section[2]/div/div/ul/li[{k}]/div[1]/div[1]/span/a"
                                b = browser.find_element(By.XPATH,movie_name).text 
                                if b == value:
                                    show_list = []
                                    for l in range(1,50):
                                        show_timings = f"/html/body/div[5]/section[2]/div/div/ul/li[2]/div[2]/div[{l}]/a/div/div"
                                        try:
                                            show_list.append(browser.find_element(By.XPATH,show_timings).text)
                                        except NoSuchElementException:
                                            logger.info(f"Found {l-1} shows for {value} in {titles[i]}")
                                            break
                                        except Exception as err:
                                            logger.error(err)
                                            if type(err).__name__ in exception_dict.keys():
                                                if exception_dict[type(err).__name__] != time_now:
                                                    logger.error("Alerting script master via e-mail about the exception")
                                                    send_exception_mail(email_one,err,type(err).__name__,662)
                                                    exception_dict[type(err).__name__] = time_now
                                                else:
                                                    logger.error("Already sent the mail this hour, skipping now")
                                            else:
                                                logger.error("Alerting script master via e-mail about the exception")
                                                send_exception_mail(email_one,err,type(err).__name__,662)
                                                exception_dict[type(err).__name__] = time_now
                                            break    
                                    cinema_update_list = []
                                    show_update_list = []
                                    cinema_dict[titles[i]] = show_list

                                    if movie_counter_machine:
                                        if titles[i] not in movie_counter_machine[value].keys():
                                            logger.info(f"New theatre added - {titles[i]}")
                                            cinema_update = {}
                                            cinema_update['Movie'] = value
                                            cinema_update['Theatre'] = titles[i]
                                            cinema_update['Show Timings'] = ", ".join(show_list)
                                            cinema_update_list.append(cinema_update)
                                            cinema_dict[titles[i]] = show_list
                                            movie_counter_machine[value] = cinema_dict.copy()
                                        elif titles[i] in movie_counter_machine[value].keys():
                                            if movie_counter_machine[value][titles[i]] != cinema_dict[titles[i]]:
                                                logger.info(f"New show added in {titles[i]}")
                                                show_update = {}
                                                show_update['Movie'] = value
                                                show_update['Theatre'] = titles[i]
                                                show_update['New Show(s) Added'] = ', '.join(list(set(show_list)-set(movie_counter_machine[value][titles[i]])))
                                                show_update['Show Timings'] = ', '.join(show_list)
                                                show_update_list.append(show_update)
                                                cinema_dict[titles[i]] = show_list
                                                movie_counter_machine[value] = cinema_dict.copy()
                                    else:
                                        logger.info("First theatre added - Alerting instantly")
                                        cinema_update = {}
                                        cinema_update['Movie'] = value
                                        cinema_update['Theatre'] = titles[i]
                                        cinema_update['Show Timings'] = ", ".join(show_list)
                                        cinema_update_list.append(cinema_update)
                                        cinema_dict[titles[i]] = show_list
                                        movie_counter_machine[value] = cinema_dict.copy()

                                    df_cinema_update_info = pd.DataFrame(columns = ['Movie','Theatre','Show Timings'])
                                    df_show_update_info = pd.DataFrame(columns = ['Movie','Theatre','New Show(s) Added','Show Timings'])

                                    df_cinema_update_data = pd.DataFrame(cinema_update_list,index = None)
                                    df_show_update_data = pd.DataFrame(show_update_list,index = None)

                                    try:
                                        df_cinema_update_info = pd.merge(df_cinema_update_info,df_cinema_update_data,how = 'outer')
                                    except pd.errors.MergeError:
                                        pass
                                    except Exception as err:
                                        logger.error(err)
                                        if type(err).__name__ in exception_dict.keys():
                                            if exception_dict[type(err).__name__] != time_now:
                                                logger.error("Alerting script master via e-mail about the exception")
                                                send_exception_mail(email_one,err,type(err).__name__,721)
                                                exception_dict[type(err).__name__] = time_now
                                            else:
                                                logger.error("Already sent the mail this hour, skipping now")
                                        else:
                                            logger.error("Alerting script master via e-mail about the exception")
                                            send_exception_mail(email_one,err,type(err).__name__,721)
                                            exception_dict[type(err).__name__] = time_now
            
                                    try:
                                        df_show_update_info = pd.merge(df_show_update_info,df_show_update_data,how = 'outer')
                                    except pd.errors.MergeError:
                                        logger.info(f"No new shows added for {value} in {titles[i]}")
                                    except Exception as err:
                                        logger.error(err)
                                        if type(err).__name__ in exception_dict.keys():
                                            if exception_dict[type(err).__name__] != time_now:
                                                logger.error("Alerting script master via e-mail about the exception")
                                                send_exception_mail(email_one,err,type(err).__name__,739)
                                                exception_dict[type(err).__name__] = time_now
                                            else:
                                                logger.error("Already sent the mail this hour, skipping now")
                                        else:
                                            logger.error("Alerting script master via e-mail about the exception")
                                            send_exception_mail(email_one,err,type(err).__name__,739)
                                            exception_dict[type(err).__name__] = time_now

                                    if not df_cinema_update_info.empty:
                                        logger.info(f"Sending an e-mail alert - {titles[i]} opened for {value}")
                                        send_theatre_alert_mail(email_list,1,df_cinema_update_info)

                                    if not df_show_update_info.empty:
                                        logger.info(f"Sending an e-mail alert - {titles[i]} has new shows for {value}")
                                        send_theatre_alert_mail(email_list,2,df_show_update_info)
                                    break
                            break
                except NoSuchElementException:
                    logger.info(f"Either {value} is not running in {titles[i]} (or) {titles[i]} is unreachable right now")
                except Exception as err:
                    logger.error(err)
                    if type(err).__name__ in exception_dict.keys():
                        if exception_dict[type(err).__name__] != time_now:
                            logger.error("Alerting script master via e-mail about the exception")
                            send_exception_mail(email_one,err,type(err).__name__,764)
                            exception_dict[type(err).__name__] = time_now
                        else:
                            logger.error("Already sent the mail this hour, skipping now")
                    else:
                        logger.error("Alerting script master via e-mail about the exception")
                        send_exception_mail(email_one,err,type(err).__name__,764)
                        exception_dict[type(err).__name__] = time_now

            flag_check = 0
            logger.info("Updating the main global list with all the latest theatre and show updates, to match for any updates next time")
            if movie_released_list:
                for index in range(len(movie_released_list)):
                    if value in movie_released_list[index]:
                        movie_released_list[index][value] = cinema_dict.copy()
                        break
                    else:
                        flag_check += 1
                if flag_check == len(movie_released_list):
                    movie_released_dict[value] = cinema_dict.copy()
                    movie_released_list.append(movie_released_dict)
            else:
                movie_released_dict[value] = cinema_dict.copy()
                movie_released_list.append(movie_released_dict)
            logger.info("Updated the main global list with all the latest updates")

            logger.info(f"Here's the master list: {movie_released_list}")
            browser.quit()

        except Exception as err:
            logger.error(err)
            if type(err).__name__ in exception_dict.keys():
                if exception_dict[type(err).__name__] != time_now:
                    logger.error("Alerting script master via e-mail about the exception")
                    send_exception_mail(email_one,err,type(err).__name__,798)
                    exception_dict[type(err).__name__] = time_now
                else:
                    logger.error("Already sent the mail this hour, skipping now")
            else:
                logger.error("Alerting script master via e-mail about the exception")
                send_exception_mail(email_one,err,type(err).__name__,798)
                exception_dict[type(err).__name__] = time_now

def send_theatre_alert_mail(emails,mode,dataframe):
    try:
        mail_id = os.environ.get('MAIL_ID')
        mail_password = os.environ.get('MAIL_PASSWORD')

        msg = MIMEMultipart('alternative')
        if mode == 1:
            msg['Subject'] = f"[BMS BOT]: New theatres added for movie(s) in your wish-list on BookMyShow"
        else:
            msg['Subject'] = f"[BMS BOT]: New shows added for movie(s) in your wish-list"
        msg['From'] = "BookMyShow BOT"
        msg['To'] = mail_id
        if mode == 1:
            body_html = "Hey,<br> \
            <p> New theatres have been added for one or more movies in your wish-lists: </p> \
            <p>Following is the list of latest theatre updates for movie(s) you might be interested in.</p> \
            {0}<br> \
            <p> Kindly take the necessary action </p> \
            <br> Thanks  \
            <hr>This is an Automated Email Notification from BookMyShow BOT.".format(dataframe.to_html(index=False))
        else:
            body_html = "Hey,<br> \
            <p> New shows have been added for one or more movies in your wish-lists: </p> \
            <p>Following is the list of newly added shows, on BookMyShow:.</p> \
            {0}<br> \
            <p> Kindly take the necessary action </p> \
            <br> Thanks  \
            <hr>This is an Automated Email Notification from BookMyShow BOT.".format(dataframe.to_html(index=False))
        msg_body = MIMEText(body_html, 'html')
        msg.attach(msg_body)
        mail_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        mail_server.login(mail_id,mail_password)
        mail_server.sendmail(mail_id, emails, msg.as_string())
        mail_server.close()
        if mode == 1:
            logger.info(f"Sent the latest theatre updates")
        else:
            logger.info(f"Sent the newly added show(s) report")
    except Exception as err:
        logger.error("Unable to send the theatre/show updates")
        logger.error(err)


def send_daily_mail(emails,info1,info2):
    try:
        mail_id = os.environ.get('MAIL_ID')
        mail_password = os.environ.get('MAIL_PASSWORD')

        msg = MIMEMultipart('alternative')
        msg['Subject'] = "[BMS BOT]: Movies currently open for bookings on BookMyShow"
        msg['From'] = "BookMyShow BOT"
        msg['To'] = mail_id
        body_html = "Hey,<br> \
        <p> Please find today's BookMyShow summary: </p> \
        <p>Following is the list of Top-5 Movies on BookMyShow:.</p> \
        {0}<br> \
        <p> Following is the list of all movies currently open for bookings: </p> \
        {1}<br> \
        <br> Thanks  \
        <hr>This is an Automated Email Notification from BookMyShow BOT.".format(info1.to_html(index=False),info2.to_html(index=False))
        msg_body = MIMEText(body_html, 'html')
        msg.attach(msg_body)
        mail_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        mail_server.login(mail_id,mail_password)
        mail_server.sendmail(mail_id, emails, msg.as_string())
        mail_server.close()
        logger.info("Sent daily report on e-mail successfully to all subscribers")
    except Exception as err:
        logger.error("Unable to send daily report")
        logger.error(err)


def send_alert_mail(emails,info1,info2):
    try:
        mail_id = os.environ.get('MAIL_ID')
        mail_password = os.environ.get('MAIL_PASSWORD')

        msg = MIMEMultipart('alternative')
        msg['From'] = "BookMyShow BOT"
        msg['To'] = mail_id
        msg['Subject'] = "[BMS BOT]: IMPORTANT - One or more movies in your wish-list open for bookings"
        body_html = "Hey,<br> \
        <p>One or more movies in your wish-lists now <b>OPEN</b> for bookings</p> \
        {0}<br> \
        <br> Thanks  \
        <hr>This is an Automated Email Notification from BookMyShow BOT.".format(info1.to_html(index=False))
        logger.info("Sending an alert mail first time")
        msg_body = MIMEText(body_html, 'html')
        msg.attach(msg_body)
        mail_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        mail_server.login(mail_id,mail_password)
        mail_server.sendmail(mail_id, emails, msg.as_string())
        mail_server.close()
        
        logger.info(f"Sent an alert mail to all subscribers, tickets for {info2} are now open")

    except Exception as err:
        logger.error("Unable to send alert on mail, please check the logging errors")
        logger.error(err)

def send_exception_mail(emails,info1,exception_name,line):
    try:
        mail_id = os.environ.get('MAIL_ID')
        mail_password = os.environ.get('MAIL_PASSWORD')

        msg = MIMEMultipart('alternative')
        msg['From'] = "BookMyShow BOT"
        msg['To'] = mail_id
        msg['Subject'] = "[BMS BOT]: CRITICAL: An exception was raised during the execution of the script"
        body_html = "Hey, <br> \
        <p>A <b>CRITICAL</b> error occurred during the execution of the script. </p> \
        <p> <b>Line - {0}</b> </p> \
        <p> Please find the details below: </p> \
        {1}<br> \
        <br> Thanks \
        <hr> This is an Automated Email Notification from BookMyShow BOT.".format(line,info1)
        logger.info("Sending the exception alert on mail")
        msg_body = MIMEText(body_html, 'html')
        msg.attach(msg_body)
        mail_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        mail_server.login(mail_id,mail_password)
        mail_server.sendmail(mail_id, emails, msg.as_string())
        mail_server.close()

        logger.info(f"Sent the exception mail alert: {exception_name}")

    except Exception as err:
        logger.error("Unable to send alert on mail, please check the logging errors")
        logger.error(err)
    
def main():
    
    logger.info("\n")
    logger.info("----------> SCRIPT STARTS HERE <----------")

    while True:
        web_scrape()


if __name__ == '__main__':
    LOG_FILENAME="G:\\Python Programs\\GIT Projects\\BookMyShow_BOT\\logs\\BMS_Bot.log"
    handler = logging.handlers.RotatingFileHandler(filename=LOG_FILENAME, mode='a', maxBytes =1*1024*1024, backupCount=4)
    logging.basicConfig(format='%(asctime)s - [%(levelname)s] - %(thread)d - %(filename)s.%(funcName)s(%(lineno)d) - %(message)s',
    level = logging.INFO, handlers = [handler])
    logger=logging.getLogger(__name__)

    main()





    

