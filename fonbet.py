from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium_stealth import stealth
from time import sleep
from datetime import date, datetime, timedelta
import csv

# Задаём константы
profile = 'C:\\Users\\Алексей\\Desktop\\script\\User Data'
engine = r'C:\\Users\\Алексей\\Desktop\\script\\chromedriver.exe'
out_path = r'C:\\Users\\Алексей\\Desktop\\script\\odds_from_fonbet.csv'
url_addr = 'https://www.fon.bet/sports'

WINDOW_SIZE = "1920,1080"

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
driver.implicitly_wait(5)  # ожидание до выброса исключения (exception)
driver.get(url_addr)

# для последующего открытия вспомогательного окна
driver.execute_script("window.open('');")
driver.switch_to.window(driver.window_handles[0])

# ==============================

stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )

def month_to_num(month):
    dict = {
        'января': 1,
        'февраля': 2,
        'марта': 3,
        'апреля': 4,
        'мая': 5,
        'июня': 6,
        'июля': 7,
        'августа:': 8,
        'сентября': 9,
        'октября': 10,
        'ноября': 11,
        'декабря': 12
    }
    return dict[month]

# список коэффициентов и информация по матчу: odd_list = [sport_name, championship_name, match_name, date_and_time, W1, X, W2, 1X, 12, X2]
# задача: сформировать такие списки для каждого матча и занести в файл

with open(out_path, 'w', newline='') as file:
    writer = csv.writer(file)

    try: # (проход по видам спорта)
        # count_kind_of_sport: 1-футбол, 2-хоккей
        for count_kind_of_sport in range(1, 2):
            odd_list = []

            # переход на вкладку вида спорта
            link_sport = driver.find_element("xpath", f"//aside[@class='sport-filter-layout__filter--Zd0Qe _vertical--1dX3h']/div/div[2]/div[2]/div[1]/div/div/div[{count_kind_of_sport}]/a").get_attribute("href")
            driver.get(link_sport)

            # вписываем название вида спорта в массив
            sport_name = driver.find_element("xpath", f"//aside[@class='sport-filter-layout__filter--Zd0Qe _vertical--1dX3h']/div/div[2]/div[2]/div[1]/div/div/div[{count_kind_of_sport}]/a/span[3]").text
            odd_list.append(sport_name)

            # клик по стрелке -> раскрываем список чемпионатов под видом спорта
            elem = driver.find_element("xpath", f"//aside[@class='sport-filter-layout__filter--Zd0Qe _vertical--1dX3h']/div/div[2]/div[2]/div[1]/div/div/div[{count_kind_of_sport}]/a/span[1]/span")
            elem.click()

            # клик по кнопке "Показать все" -> раскрываем список чемпионатов полностью
            elem = driver.find_element("xpath", f"//aside[@class='sport-filter-layout__filter--Zd0Qe _vertical--1dX3h']/div/div[2]/div[2]/div[1]/div/div/div[{count_kind_of_sport}]/div[12]/span")
            elem.click()

            try: # (проход по чемпионатам)
                count_championship = 3
                while True:
                    odd_list = [sport_name]

                    # # клик по кнопке "Показать все" -> раскрываем список чемпионатов полностью
                    # # (версия, которая исправляла баг после прохождения чемпионата, который находился под кнопкой "Показать все" после раскрытия всех чемпионатов
                    # if count_championship > 11:
                    #     elem = driver.find_element("xpath", f"//aside[@class='sport-filter-layout__filter--Zd0Qe _vertical--1dX3h']/div/div[2]/div[2]/div[1]/div/div/div[{count_kind_of_sport}]/div[{count_championship}]/span")
                    #     elem.click()
                    # else:
                    #     elem = driver.find_element("xpath", f"//aside[@class='sport-filter-layout__filter--Zd0Qe _vertical--1dX3h']/div/div[2]/div[2]/div[1]/div/div/div[{count_kind_of_sport}]/div[12]/span")
                    #     elem.click()

                    # переход на вкладку чемпионата
                    # link_championship = driver.find_element("xpath", f"//aside[@class='sport-filter-layout__filter--Zd0Qe _vertical--1dX3h']/div/div[2]/div[2]/div[1]/div/div/div[{count_kind_of_sport}]/div[{count_championship}]/a").get_attribute("href")
                    # driver.get(link_championship)

                    # вписываем название чемпионата в массив
                    championship_name = driver.find_element("xpath", f"//aside[@class='sport-filter-layout__filter--Zd0Qe _vertical--1dX3h']/div/div[2]/div[2]/div[1]/div/div/div[{count_kind_of_sport}]/div[{count_championship}]/a/span[2]").text
                    odd_list.append(championship_name)

                    # клик по стрелке -> раскрываем список матчей в чемпионата
                    if 'disabled' in driver.find_element("xpath", f"//aside[@class='sport-filter-layout__filter--Zd0Qe _vertical--1dX3h']/div/div[2]/div[2]/div[1]/div/div/div[{count_kind_of_sport}]/div[{count_championship}]/a/span[1]").get_attribute("class"):
                        count_championship += 1
                        continue
                    elem = driver.find_element("xpath", f"//aside[@class='sport-filter-layout__filter--Zd0Qe _vertical--1dX3h']/div/div[2]/div[2]/div[1]/div/div/div[{count_kind_of_sport}]/div[{count_championship}]/a/span[1]/span")
                    elem.click()

                    try: # (проход по матчам в рамках чемпионата)
                        count_match = 2
                        while True:
                            odd_list = [sport_name, championship_name]

                            # вписываем название матча в массив
                            match_name = driver.find_element("xpath", f"//aside[@class='sport-filter-layout__filter--Zd0Qe _vertical--1dX3h']/div/div[2]/div[2]/div[1]/div/div/div[{count_kind_of_sport}]/div[{count_championship}]/a[{count_match}]/span").text
                            if ('голы' in match_name) or ('карты' in match_name) or ('офсайды' in match_name):
                                count_match += 1
                                continue
                            odd_list.append(match_name)

                            # переход на страницу матча (переход осуществляется в другой вкладке браузера, чтобы список чемпионатов не сворачивался при обновлении первой вкладки (~ кнопка "Показать все"))
                            link_match = driver.find_element("xpath", f"//aside[@class='sport-filter-layout__filter--Zd0Qe _vertical--1dX3h']/div/div[2]/div[2]/div[1]/div/div/div[{count_kind_of_sport}]/div[{count_championship}]/a[{count_match}]").get_attribute("href")
                            count_match += 1
                            # непосредственно переключение на вторую вкладку браузера
                            driver.switch_to.window(driver.window_handles[1])
                            driver.get(link_match)

                            try: # (достаём дату проведения матча)
                                day = date.today()  # -> '%Y-%m-%d'
                                elem = driver.find_element("xpath", "//div[@class='ev-sport-header--67vcd _sport_1--5lZ4W']/div[1]/div[2]/div[2]/span[1]").text
                                if elem == 'Сегодня':
                                    day = str(day)
                                elif elem == 'Завтра':
                                    day += timedelta(days=1)
                                    day = str(day)
                                else:
                                    elem = elem.split()  # elem = [день, месяц (словом)]
                                    # сравним дату матча с сегодняшним днём, чтобы правильно определить год проведения матча (этот или следующий)
                                    date1 = date(datetime.now().year, month_to_num(elem[1]), int(elem[0]))
                                    date2 = date.today()
                                    day = str(date1)
                                    if date1 < date2:
                                        # то есть матч будет в следующем году, поэтому ставим следующий год
                                        day = str(int(day[:4]) + 1) + day[4:]

                                # на данном этапе имеем дату в формате 'год-месяц-день'
                                # осталось добавить время

                                # время проведения матча
                                elem = driver.find_element("xpath", "//div[@class='ev-sport-header--67vcd _sport_1--5lZ4W']/div[1]/div[2]/div[2]/span[2]").text
                                date_and_time = day + ' ' + elem + ':00'

                                # добавляем в таблицу полную дату проведения матча в формате: 'Y-m-d h:m:s'
                                odd_list.append(date_and_time)

                            except Exception as e4:
                                print(e4)
                                # если матч уже начался, то указываем текущую дату и время 00:00:00
                                day = str(date.today()) + ' 00:00:00'
                                odd_list.append(day)

                            try: # (достаём коэффициенты)
                                for i in range(1,3):
                                    for j in range(1, 4):
                                        elem = driver.find_element("xpath", f"//div[@class='event-view-tables-wrap--7IFsJ']/div[{count_kind_of_sport}]/div[2]/div/div[2]/div/div/div[{i}]/div[{j}]/div/div/div[2]").text
                                        if elem == '–':
                                            elem = '1'
                                        odd_list.append(elem)

                                # записываем список (массив) с коэффициентами и информацией по матчу в файл
                                writer.writerow(odd_list)

                            except Exception as e5:
                                print('не удалось достать коэффициенты')
                                print(e5)

                            # возврат на первую вкладку браузера, где список чемпионатов остался несвернутым (не надо ещё раз нажимать на кнопку "Показать все")
                            driver.switch_to.window(driver.window_handles[0])

                    except Exception as e3:
                        print(e3)

                    # сворачиваем список матчей в чемпионате
                    elem = driver.find_element("xpath", f"//aside[@class='sport-filter-layout__filter--Zd0Qe _vertical--1dX3h']/div/div[2]/div[2]/div[1]/div/div/div[{count_kind_of_sport}]/div[{count_championship}]/a/span[1]/span")
                    elem.click()

                    count_championship += 1

            except Exception as e2:
                print(e2)

            # сворачиваем список чемпионатов для вида спорта
            driver.get(link_sport)
            elem = driver.find_element("xpath", f"//aside[@class='sport-filter-layout__filter--Zd0Qe _vertical--1dX3h']/div/div[2]/div[2]/div[1]/div/div/div[{count_kind_of_sport}]/a/span[1]/span")
            elem.click()

    except Exception as e1:
        print(e1)