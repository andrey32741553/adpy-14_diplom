import requests
from random import randint
import datetime

now = str(datetime.date.today()).split('-')
token = 'Ваш VK токен'


class GetPartnerInfo:
    """Класс для ввода параметров и поиска в сети ВК"""

    def __init__(self, token, now):
        self.token = token
        self.now = now
        self.app_id = 0
        self.desired_city = input('Введите город для поиска: ')
        self.min_desired_age = int(input('Введите минимальный возраст для поиска: '))
        self.max_desired_age = int(input('Введите максимальный возраст для поиска: '))
        self.desired_sex = int(input('1 - женский;\n2 - мужской;\nВведите пол: '))
        self.desired_relation = int(input('1 — не женат/не замужем;\n2 — есть друг/есть подруга;\n'
                                          '3 — помолвлен/помолвлена;\n4 — женат/замужем;\n5 — всё сложно;\n'
                                          '6 — в активном поиске;\n7 — влюблён/влюблена;\n8 — в гражданском браке;\n'
                                          '0 — не указано.\n'
                                          'Какое семейное положение: '))

    def get_preferences_info(self):
        """ Функция поиска пользователя по указанным параметрам. Цикл работает пока не найдёт. Сперва делает запрос"""
        print('Идёт поиск...')
        while True:
            self.app_id = randint(1, 618607937)
            info_resp = self.making_info_response()
            user_data = info_resp.json()['response']
            try:
                for item in user_data:

                    """ Здесь вычисляется возраст пользователя. Метод прост - просто отнимает от нынешнего года год 
                    рождения пользователя. Решил числа и месяцы не использовать - погрешность небольшая """

                    birth_date = item['bdate'].split('.')
                    age = int(now[0]) - int(birth_date[2])

                    """ Далее условия для поиска """
                    if item['sex'] == self.desired_sex and item['relation'] == self.desired_relation\
                            and len(birth_date) == 3 and self.min_desired_age < age < self.max_desired_age\
                            and item['city']['title'].capitalize() == self.desired_city.capitalize():
                        link_list = self.making_link_list_from_photo_resp()

                        """Далее проверка количества фотографий пользователя. Если меньше трёх, то ищет далее. Если
                        условие выполняется, то создаёт сортированный список по лайкам"""

                        if len(link_list) < 3:
                            continue
                        else:
                            link_list.sort(key=lambda x: (x[1], x[0]), reverse=True)
                            return user_data, link_list, age, self.min_desired_age, self.max_desired_age
            except:
                """Здесь ловит исключение. Почему оно иногда вылезает - я не понял, поэтому решил его игнорировать"""
                KeyError: 'relation'

    def making_info_response(self):
        """ Функция для получения информации искомого пользователя """
        info_resp = requests.get(
            'https://api.vk.com/method/users.get',
            params={
                'user_ids': self.app_id,
                'access_token': token,
                'v': 5.21,
                'fields': 'bdate, city, sex, relation'
            }
        )
        return info_resp

    def making_photo_response(self):
        """ Функция получения фото искомого пользователя """
        photo_resp = requests.get(
            'https://api.vk.com/method/photos.get',
            params={
                'owner_id': self.app_id,
                'access_token': token,
                'v': 5.21,
                'album_id': 'profile',
                'photo_sizes': 1,
                'extended': 1
            }
        )
        return photo_resp

    def making_link_list_from_photo_resp(self):
        """ Создание списка фотографий искомого пользователя """
        photo_resp = self.making_photo_response()
        link_list = []
        photo_list = photo_resp.json()['response']['items']
        for item in photo_list:
            like = item['likes']['user_likes'] + item['likes']['count']
            for dictionary in item['sizes']:
                if dictionary['type'] == 'w':
                    break
            link_list.append((dictionary['src'], like))
        return link_list


if __name__ == '__main__':
    info = GetPartnerInfo(token, now)
    info.get_preferences_info()
