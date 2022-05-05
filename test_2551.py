from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_my_pets(web_browser):
    # Open PetFriends base page:
    web_browser.get("https://petfriends1.herokuapp.com/")

    # click on the new user button
    element = WebDriverWait(web_browser, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[@onclick=\"document.location='/new_user';\"]")))
    btn_newuser = element
    btn_newuser.click()

    # click existing user button
    element = WebDriverWait(web_browser, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, u"У меня уже есть аккаунт")))
    btn_exist_acc = element
    btn_exist_acc.click()

    # add email
    element = WebDriverWait(web_browser, 10).until(
        EC.presence_of_element_located((By.ID, "email")))
    field_email = element
    field_email.clear()
    field_email.send_keys("test11@test.com")

    # add password
    element = WebDriverWait(web_browser, 10).until(
        EC.presence_of_element_located((By.ID, "pass")))
    field_pass = element
    field_pass.clear()
    field_pass.send_keys("password")

    # click submit button
    element = WebDriverWait(web_browser, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[@type='submit']")))
    btn_submit = element
    btn_submit.click()

    # переход в мои питомцы
    element = WebDriverWait(web_browser, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, u"Мои питомцы")))
    btn_exist_acc = element
    btn_exist_acc.click()

    # в переменную count сохраняем количество питомцев из статистики пользователя
    count = web_browser.find_element_by_css_selector(".\\.col-sm-4.left")
    count = count.text.split('\n')[1]
    count = int(count.split(' ')[1])

    # получаем количество строк в таблице (оно же и количество питомцев)
    count_strings = web_browser.find_elements_by_xpath('//tbody/tr')
    count_photo = 0  # количество питомцев с фото
    # получаем список ячеек в которых должны быть фотографии
    photo = web_browser.find_elements_by_xpath('//tbody/tr/th/img')
    # если в ячейке есть фото, то увеличиваем счетчик на 1
    for i in range(len(photo)):
        if str(photo[i].get_attribute('src')) != '':
            count_photo += 1

    # в переменную db сохраняем список питомцев
    # (каждый питомец - это список: имя, вид животного, возраст)
    db = []
    # получаем список всех строк
    strings = web_browser.find_elements_by_xpath('//tbody/tr')
    for i in range(len(strings)):
        # получаем список ячеек i-ой строки
        xpath = '//tbody/tr[' + str(i + 1) + ']/td'
        cells = web_browser.find_elements_by_xpath(xpath)
        pet = [cells[0].text, cells[1].text, cells[2].text]
        db.append(pet)

    # в список names сохраним имена всех питомцев
    names = []
    for i in range(len(db)):
        string = db[i]
        names.append(string[0])

    # проверяем, что находимся на нужной странице
    assert web_browser.current_url == 'https://petfriends1.herokuapp.com/my_pets', "login error"

    # сравниваем количество питомцев в статистике и количество строк в таблице
    assert len(count_strings) == count

    # проверяем что хотя бы у половины питомцев есть фото
    assert count_photo >= (count / 2), 'Фото есть меньше чем у половины питомцев'

    # проверяем, что у всех питомцев есть имя, тип животного и возраст
    for i in range(len(db)):
        string = db[i]
        for j in range(3):
            assert string[j] != '', 'У питомца заполнены не все данные'

    # проверяем, что нет дублирующихся питомцев
    for i in db:
        count_double_pet = db.count(i)
        assert count_double_pet == 1, 'Некоторые питомцы указаны дважды'

    # проверяем, что у всех питомцев разные имена
    for i in names:
        count_name = names.count(i)
        assert count_name == 1, 'Имена некторых питомцев совпадают'


def test_all_pets(web_browser):
    # driver.implicitly_wait(10)
    # Open PetFriends base page:
    web_browser.get("https://petfriends1.herokuapp.com/")

    # click on the new user button
    btn_newuser = web_browser.find_element_by_xpath("//button[@onclick=\"document.location='/new_user';\"]")
    btn_newuser.click()

    # click existing user button
    btn_exist_acc = web_browser.find_element_by_link_text(u"У меня уже есть аккаунт")
    btn_exist_acc.click()

    # add email
    field_email = web_browser.find_element_by_id("email")
    field_email.clear()
    field_email.send_keys("test11@test.com")

    # add password
    field_pass = web_browser.find_element_by_id("pass")
    field_pass.clear()
    field_pass.send_keys("password")

    # click submit button
    btn_submit = web_browser.find_element_by_xpath("//button[@type='submit']")
    btn_submit.click()

    # выбираем все фотографии
    images = web_browser.find_elements_by_css_selector('.card-deck .card-img-top')
    # выбираем все имена
    names = web_browser.find_elements_by_css_selector('.card-deck .card-title')
    # выбираем все типы животных и возрасты
    descriptions = web_browser.find_elements_by_css_selector('.card-deck .card-text')

    for i in range(len(names)):
        # проверяем, что изображение есть
        assert images[i].get_attribute('src') != '', 'У питомца отсутствует изображение'

        # проверяем, что имя есть
        assert names[i].text != '', 'У питомца отсутствует имя'

        # проверяем, что есть тип животного и возраст
        assert descriptions[i].text != '', 'У питомца отсутствует описание'

        # проверяем, что в описании есть запятая
        assert ', ' in str(descriptions[i])
        # делим строку на две части, разделитель - запятая с пробелом
        # и проверяем, что обе части не пустые
        parts = descriptions[i].text.split(", ")
        assert len(parts[0]) > 0
        assert len(parts[1]) > 0

    assert web_browser.current_url == 'https://petfriends1.herokuapp.com/all_pets', "login error"
