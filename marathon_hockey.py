from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium_stealth import stealth
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import warnings
import csv

# Задаём константы
profile = 'C:\\Users\\Алексей\\Desktop\\script\\User Data'
engine = r'C:\\Users\\Алексей\\Desktop\\script\\chromedriver.exe'
out_path = r'C:\\Users\\Алексей\\Desktop\\script\\odds_from_marathonbet.csv'
url_addr = 'https://www.marathonbet.ru/su/popular/Ice+Hockey+-+537'

WINDOW_SIZE = "1920,1080"


def main_fun():
    options = webdriver.ChromeOptions()
    options.add_argument('user-data-dir=' + profile)
    options.add_argument('pageLoadStrategy=eager')
    # options.add_argument("--headless")
    options.add_argument("--window-size=%s" % WINDOW_SIZE)

    # ============================

    options.add_argument("--disable-blink-features")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("start-maximized")

    # ============================

    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "eager"

    # Читаем входной файл
    driver = webdriver.Chrome(desired_capabilities=caps, executable_path=engine, chrome_options=options)
    driver.implicitly_wait(10)  # ожидание до выброса исключения (exception)
    driver.get(url_addr)

    # ==============================

    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )

    with open(out_path, "a", newline='') as file:
        writer = csv.writer(file)
        try:
            iter = 1
            sum_iter = 0
            while True:
                odd_list = ['Хоккей']
                base_path = f"//div[@id = 'events_content']/div[1]/div[1]/div/div/div[{iter}]"

                event_size = len(driver.find_elements("xpath", f"{base_path}/div/div/div/table/tbody/tr/th"))

                if event_size <= 8:
                    return 0

                if event_size > 8:
                    event_1 = driver.find_element("xpath", f"{base_path}/div/div/div/table/tbody/tr/th[3]/span/b").text == '1'
                    event_x = driver.find_element("xpath", f"{base_path}/div/div/div/table/tbody/tr/th[4]/span/b").text == 'X'
                    event_2 = driver.find_element("xpath", f"{base_path}/div/div/div/table/tbody/tr/th[5]/span/b").text == '2'
                    event_1x = driver.find_element("xpath", f"{base_path}/div/div/div/table/tbody/tr/th[6]/span/b").text == '1X'
                    event_12 = driver.find_element("xpath", f"{base_path}/div/div/div/table/tbody/tr/th[7]/span/b").text == '12'
                    event_x2 = driver.find_element("xpath", f"{base_path}/div/div/div/table/tbody/tr/th[8]/span/b").text == 'X2'

                    if all([event_1, event_x, event_2, event_1x, event_12, event_x2]):
                        championship_name = ""
                        for tab_champ in driver.find_elements("xpath", f"{base_path}/table/tbody/tr/td[2]/div/a/h2/span"):
                            championship_name = championship_name + tab_champ.text + " "
                        print(championship_name)
                        odd_list.append(championship_name)

                        cnt = len(driver.find_elements("xpath", f"{base_path}/div/div/div/div"))  # количество матчей, по которым нужно пройти
                        for i in range(2, cnt + 1):
                            tab_row_path = f"{base_path}/div/div/div/div[{i}]"
                            tab_row = driver.find_element("xpath", tab_row_path)
                            match_name = tab_row.get_attribute("data-event-name")
                            if match_name.find(",") >= 0:
                                break
                            print(match_name)
                            odd_list.append(match_name)

                            for j in range(3, 9):
                                tab_row = driver.find_element("xpath", f"{tab_row_path}/table/tbody/tr/td[{j}]/span")
                                tab_text = tab_row.text
                                if tab_text == '—':
                                    tab_text = 1
                                odd_list.append(tab_text)

                            writer.writerow(odd_list)
                            del odd_list[2:]
                            sum_iter += 1

                        if sum_iter > 20:
                            # print("click")
                            # body = driver.find_element("xpath", "/html/body")
                            body = driver.find_element("xpath", "//div[@id='betslip-pc-place']")
                            body.click()
                            ActionChains(driver).send_keys(Keys.END).perform()
                            sum_iter -= 20
                iter += 1
                odd_list.clear()

        except Exception as e:
            print(e)
            print(0)

