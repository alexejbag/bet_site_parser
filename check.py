import csv
import difflib
from typing import List


def which_ishod(a: float, lst: List[float]):
    if a == lst[0]:
        return 'П1: '
    if a == lst[1]:
        return 'X: '
    if a == lst[2]:
        return 'П2: '
    if a == lst[3]:
        return '1X: '
    if a == lst[4]:
        return '12: '
    if a == lst[5]:
        return 'X2: '


def two_events(s: str, a: float, b: float, bk_1: List[float], bk_2: List[float]):
    '''
    функция проверяет, есть ли вилка на события (W1 и X2) или (W2 и 1X) или (X и 12) в двух Букмекерских Конторах, вероятности которых задаются коэффицентами a и b
    :param s: название матча
    :param a: коэффициент в первой БК
    :param b: коэффициент во второй БК
    :param bk_1: список коэффициентов из первой БК
    :param bk_2: список коэффициентов из второй БК
    :return: ничего не возвращает; в случае наличия вилки печатает на экран: * название матча
                                                                             * коэффициенты, на которые надо ставить (и в какой БК)
                                                                             * маржу букмекера
    '''
    margin = (1 / a + 1 / b) - 1
    if margin < 0:
        result = '>>> [' + s + ']  '
        if a in bk_1:
            result += 'фонбет '
            result += which_ishod(a, bk_1)
        elif a in bk_2:
            result += 'марафон '
            result += which_ishod(a, bk_2)
        else:
            return 0
        result += str(a)
        result += '  '

        if b in bk_1:
            result += 'фонбет '
            result += which_ishod(b, bk_1)
        elif b in bk_2:
            result += 'марафон '
            result += which_ishod(b, bk_2)
        else:
            return 0
        result += str(b)
        result += '  '

        result += 'маржа: '
        result += str(margin * 100)
        print(result)


def three_events(s: str, a: float, b: float, c: float, bk_1: List[float], bk_2: List[float]):
    '''
    функция проверяет, есть ли вилка на события (W1, X, W2) в двух Букмекерских Конторах, вероятности которых задаются коэффицентами a, b, c
    :param s: название матча
    :param a: коэффициент в одной из двух БК
    :param b: коэффициент в одной из двух БК
    :param c: коэффициент в одной из двух БК
    :param bk_1: список коэффициентов из первой БК
    :param bk_2: список коэффициентов из второй БК
    :return: ничего не возвращает; в случае наличия вилки печатает на экран: * название матча
                                                                             * коэффициенты, на которые надо ставить (и в какой БК)
                                                                             * маржу букмекера
    '''
    margin = (1 / a + 1 / b + 1 / c) - 1
    if margin < 0:
        result = '>>> [' + s + ']  '
        if a in bk_1:
            result += 'фонбет П1: '
        elif a in bk_2:
            result += 'марафон П1: '
        else:
            return 0
        result += str(a)
        result += '  '

        if b in bk_1:
            result += 'фонбет X: '
        elif b in bk_2:
            result += 'марафон X: '
        else:
            return 0
        result += str(b)
        result += '  '

        if c in bk_1:
            result += 'фонбет П2: '
        elif c in bk_2:
            result += 'марафон П2: '
        else:
            return 0
        result += str(c)
        result += '  '

        result += 'маржа: '
        result += str(margin * 100)
        print(result)


def check(s: str, a: List[float], b: List[float]):
    '''
    функция проверяет наличие вилки на события (W1, X, W2, 1X, 12, X2) в двух Букмекерских Конторах, вероятности которых задаются коэффицентами, содержащимися в списках a и b
    :param s: название матча
    :param a: список коэффициентов в первой БК [W1, X, W2, 1X, 12, X2]
    :param b: список коэффициентов во второй БК [W1, X, W2, 1X, 12, X2]
    :return: ничего не возвращает, но вызывает функции two_events и three_events
    '''

    # в качестве параметров a и b подаются списки коэффициентов, но в текстовом формате
    # чтобы производить расчёты, коэффициенты должны иметь числовой вид, поэтому приводим каждый коэффициент в формату float
    for i in range(len(a)):
        a[i] = float(a[i])
        b[i] = float(b[i])

    t = [max(a[i], b[i]) for i in range(6)]
    two_events(s, t[0], t[5], a, b)
    two_events(s, t[1], t[4], a, b)
    two_events(s, t[2], t[3], a, b)
    three_events(s, t[0], t[1], t[2], a, b)

    # two_events(s, a[0], b[5]) # W1 в БК_1, X2 в БК_2
    # two_events(s, a[2], b[3]) # W2 в БК_1, 1X в БК_2
    # two_events(s, a[1], b[4]) # X в БК_1, 12 в БК_2
    # two_events(s, a[5], b[0]) # X2 в БК_1, W1 в БК_2
    # two_events(s, a[3], b[2]) # 1X в БК_1, W2 в БК_2
    # two_events(s, a[4], b[1]) # 12 в БК_1, X в БК_2
    #
    # three_events(s, a[0], a[1], b[2])
    # three_events(s, a[0], b[1], a[2])
    # three_events(s, a[0], b[1], b[2])
    # three_events(s, b[0], a[1], a[2])
    # three_events(s, b[0], a[1], b[2])
    # three_events(s, b[0], b[1], a[2])


def edit_string(s: str):
    # Базовое
    s = s.replace('-', '').replace(' ', '')
    s = s.replace('b', 'команда2')
    # Англия
    s = s.replace('хотспур', '')
    s = s.replace('рексем', 'рексхэм')
    s = s.replace('суонсисити', 'суонси')
    s = s.replace('норвичсити', 'норвичс')
    s = s.replace('борэмвуд', 'борхэмвуд')
    s = s.replace('ньюкаслюнайтед', 'ньюкасл')
    s = s.replace('вестхэмюнайтед', 'вестхэм')
    s = s.replace('ротеремюнайтед', 'ротерхем')
    s = s.replace('челтнэмтаун', 'челтенхемтаун')
    s = s.replace('хаддерсфилдтаун', 'хаддерсфилд')
    s = s.replace('хаддерсфилдтаун', 'хаддерсфилд')
    s = s.replace('брайтонэндхоувальбион', 'брайтон')
    s = s.replace('вестбромвичальбион', 'вестбромвич')
    s = s.replace('вулверхэмптонуондерерс', 'вулверхэмптон')
    # Германия
    s = s.replace('майнц05', 'майнц')
    s = s.replace('леверкузен', '04')  # ??? replace('леверкузен', '04') and replace('байер04', 'байер') ???
    s = s.replace('рблейпциг', 'лейпциг')
    s = s.replace('вердербремен', 'вердер')
    s = s.replace('боруссиядортмунд', 'боруссияд')
    s = s.replace('айнтрахтфранкфурт', 'айнтрахтф')
    # Испания
    s = s.replace('ивиса', 'ибицауд')
    # Италия
    s = s.replace('интермилан', 'интер')
    # Португалия
    s = s.replace('спортингбрага', 'брага')
    s = s.replace('пасушдиферрейра', 'пасуш феррейра')
    # Росиия
    s = s.replace('фкростов', 'ростов')
    s = s.replace('ахматгрозный', 'ахмат')
    s = s.replace('уралекатеринбург', 'урал')
    s = s.replace('фккраснодар', 'краснодар')
    # Прочее
    s = s.replace('скднепр', 'днепр')
    s = s.replace('фксидней', 'сидней')
    s = s.replace('псвэйндховен', 'псв')
    s = s.replace('фккарабах', 'карабах')
    s = s.replace('азалкмаар', 'азалкмар')
    s = s.replace('торреэнше', 'торренше')
    s = s.replace('ркквалвейк', 'валвейк')
    s = s.replace('шерифтирасполь', 'шериф')
    s = s.replace('мидтъюлланн', 'мидтьюлланн')
    s = s.replace('кардиффсити', 'кардиффс')
    s = s.replace('республикакорея', 'южнаякорея')
    s = s.replace('редбуллзальцбург', 'зальцбург')

    return s

def compare_strings(game1: List[str], game2: List[str]):
    '''
    функция сравнивает строки, содержащие название команд, которые будут играть (в разных БК названия иностранных команд может быть написано по-разному)
    функция позволяет считать строки одинакомыми, если они отличаются не более, чем в два символа
    :param game1: вид спорта и название матча из первой БК (список из двух элементов)
    :param game2: вид спорта и название матча из второй БК (список из двух элементов)
    :return: 1 в случае полного или частичного совпадения строк (2 символа могут отличаться), иначе 0
    '''
    if game1[0] != game2[0]:
        # не совпадют виды спорта => сразу отметаем
        return False

    if game1[1] == game2[1]:
        # точное совпадение названий команд
        return True

    if difflib.SequenceMatcher(None, edit_string(game1[1]), edit_string(game2[1])).ratio() > 0.85:
        # print(game1[1], game2[1])  # чтобы посмотреть, в чём именно отличается названия команд
        return True

    return False


reader_fonbet = []
reader_marathon = []

with open('odds_from_fonbet.csv') as file:
    csv_fonbet = csv.reader(file)
    for row in csv_fonbet:
        reader_fonbet.append(row)

with open('odds_from_marathonbet.csv') as file:
    csv_marathonbet = csv.reader(file)
    for row in csv_marathonbet:
        reader_marathon.append(row)

N = 0

for row in reader_fonbet:
    teams1 = [row[0], row[2].replace(' — ', '-').lower()] # вид спорта и название матча

    count = 0
    tmp_row = ''

    for row2 in reader_marathon:
        teams2 = [row2[0], row2[2].replace(' - ', '-').lower()] # вид спорта название матча

        if compare_strings(teams1, teams2):
            N += 1
            count += 1
            tmp_row = row2

    if count > 0:
        check(teams1[1], row[4:], tmp_row[3:]) # передаём в функцию check название матча и коэффициенты из двух БК

print(N)