from pprint import pprint
from adpy_diplom.VKinter_database import VKUser, DatingUser, Photos, BlackList, Session, engine
from adpy_diplom.VKinter_classes import GetPartnerInfo
import datetime
from adpy_diplom.VKinter_classes import token


def get_user_info():
    """ Функция для сбора информации о пользователе """
    user_id = int(input('Введите Ваш VK ID: '))
    first_name = input('Введите Ваше имя: ')
    last_name = input('Введите Вашу фамилию: ')
    user_age = int(input('Введите Ваш возраст: '))
    sex = input('Ваш пол: ')
    city = input('Ваш город: ')
    return user_id, first_name, last_name, user_age, sex, city


class VariableActionsWithDatingUsers:
    """ Класс для работы со списком понравившихся людей """

    def __init__(self, Session, engine):
        self.session = Session()
        self.connection = engine.connect()

    def show_list_of_dating_users(self):
        """ Функция для вывода списка понравившихся людей для определённого пользователя """
        id_user = input('Введите ID пользователя для вывода списка: ')
        select_query = self.connection.execute(f"""SELECT vk_id, dating_user_first_name, dating_user_last_name, age, 
        user_id, city, photo_link FROM dating_user d
        JOIN photos p ON p.vk_id_dating_user = d.vk_id
        WHERE user_id = {id_user};
        """).fetchall()
        print(f'Список понравившихся людей пользователя ID = {id_user}')
        return select_query

    def deleting_dating_user(self):
        """ Функция для удаления людей из списка понравившихся для определённого пользователя """
        del_vk_id = int(input('(Чтобы выйти из режима удаления нажмите "0")\n'
                              'Введите ID пользователя для удаления из списка понравившихся людей\n'
                              '(скопируйте из списка выше): '))
        if del_vk_id == 0:
            print('*' * 100)
            pass
        else:
            self.connection.execute(f"""DELETE FROM photos USING dating_user
            WHERE vk_id_dating_user = dating_user.vk_id AND dating_user.vk_id = {del_vk_id};""")
            self.session.query(DatingUser).filter(DatingUser.vk_id == del_vk_id).delete()
            self.session.commit()
            print(f'Пользователь с ID = {del_vk_id} удалён')
            print('*' * 100)

    def add_dating_user_to_blacklist(self):
        """ Функция для перемещения в чёрный список из списка понравившихся людей для определённого пользователя.
        Сперва будет показан список понравившихся людей для удобства (чтоб можно было просто скопировать ID нужного
        человека)"""
        dating_user_list = self.show_list_of_dating_users()
        pprint(dating_user_list)
        print('Чтобы выйти из режима перемещения пользователя нажмите "0"')
        user_to_blist = int(input('Введите ID пользователя, которого хотите переместить в чёрный список: '))
        if user_to_blist == 0:
            print('*' * 100)
            pass
        else:
            for item in dating_user_list:
                if item[0] == user_to_blist:
                    dating_user_id = item[0]
                    dating_user_first_name = item[1]
                    dating_user_last_name = item[2]
                    age = item[3]
                    user_id = item[4]
                    city = [5]
                    self.session.add_all([BlackList(vk_id=dating_user_id,
                                                    dating_user_first_name=dating_user_first_name,
                                                    dating_user_last_name=dating_user_last_name,
                                                    age=age, user_id=user_id, city=city)])
            self.connection.execute(f"""DELETE FROM photos USING dating_user
                WHERE vk_id_dating_user = dating_user.vk_id AND dating_user.vk_id = {user_to_blist};""")
            self.session.query(DatingUser).filter(DatingUser.vk_id == user_to_blist).delete()
            self.session.commit()
            print(f'Пользователь с ID = {user_to_blist} перемещён в чёрный список')

    def show_blacklist_of_dating_users(self):
        """ Функция показывает чёрный список для определённого пользователя"""
        id_user = input('Введите ID пользователя для вывода чёрного списка: ')
        select_query = self.connection.execute(f"""SELECT vk_id, dating_user_first_name, dating_user_last_name, age
        FROM blacklist
        WHERE user_id = {id_user};
        """).fetchall()
        print(f'Чёрный список пользователя ID = {id_user}:')
        return select_query


class AddInfoToVKinterDB:
    """ Класс для работы с запросами в БД """

    def __init__(self, user_id, first_name, last_name, user_age, sex, city, token):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.user_age = user_age
        self.sex = sex
        self.city = city
        now = str(datetime.date.today()).split('-')
        self.token = token
        info = GetPartnerInfo(token, now)
        self.user_data, self.link_list, self.age, self.min_desired_range, self.max_desired_range = info.get_preferences_info()
        for item in self.user_data:
            self.dating_user_id = item['id']
            self.dating_user_first_name = item['first_name']
            self.dating_user_last_name = item['last_name']
            self.dating_user_city = item['city']['title']
        self.age_range = f'{self.min_desired_range} - {self.max_desired_range}'
        self.session = Session()
        self.connection = engine.connect()

    def add_user_info(self):
        """ Проверка наличия пользователя в БД, если такой есть - обновляются данные о дапазоне поиска. Если нет, то
        вносится информация о новом пользователе (else после цикла) """
        select_query = self.connection.execute("""SELECT vk_id FROM vk_user;
            """).fetchall()
        for vk_id in select_query:
            if self.user_id == int(str(vk_id).strip('(),')):
                self.session.query(VKUser).filter(VKUser.vk_id == self.user_id).update(
                    {"range_for_search_age": self.age_range}
                )
                self.session.commit()
                break
            else:
                continue
        else:
            self.session.add_all([VKUser(vk_id=self.user_id, first_name=self.first_name,
                                         last_name=self.last_name, user_age=self.user_age,
                                         range_for_search_age=self.age_range,
                                         sex=self.sex, city=self.city)])
            self.session.commit()

    def add_dating_user_info(self):
        """ Проверка на наличие найденного пользователя в базе данных, если есть, то пропускает и ищет снова """
        existance = self.checking_for_existance_in_DB()
        if existance:
            return True
        """ Вывод результата поиска """
        print(f'id - {self.dating_user_id}')
        print(f'Имя - {self.dating_user_first_name}')
        print(f'Фамилия - {self.dating_user_last_name}')
        print(f'Возраст - {self.age}')
        print(f'Город - {self.dating_user_city}')
        for link in self.link_list[:3]:
            print(f'Фото: - {link[0]}')

        """ Далее сообщение о том, что найден пользователь. Предложение сохранить данные. Независимо от того, что
        выберет пользователь, будет предложено продолжить поиск или остановить"""

        prefer_user = input('Подходящий по критериям пользователь найден. Сохранить данные? Y/N ')
        while True:
            if prefer_user == 'N' or prefer_user == 'n' or prefer_user == 'т' or prefer_user == 'Т':
                search = self.continuing_search()
                if search:
                    return True
                else:
                    return False
            elif prefer_user == 'Y' or prefer_user == 'y' or prefer_user == 'Н' or prefer_user == 'н':
                self.session.add_all([DatingUser(vk_id=self.dating_user_id,
                                                 dating_user_first_name=self.dating_user_first_name,
                                                 dating_user_last_name=self.dating_user_last_name,
                                                 age=self.age, user_id=self.user_id, city=self.dating_user_city)])
                self.session.commit()
                for link in self.link_list[:3]:
                    photo_link = link[0]
                    like_count = link[1]
                    self.session.add_all([Photos(photo_link=photo_link, likes=like_count,
                                                 vk_id_dating_user=self.dating_user_id)])
                self.session.commit()
                print('Данные сохранены')
                search = self.continuing_search()
                if search:
                    return True
                else:
                    return False
            else:
                print('Вы ввели неправильную комманду. Попробуйте заново')

    def continuing_search(self):
        """Функция предлагающая продолжить поиск """
        search_again = input('Продолжить поиск? Y/N ')
        while True:
            if search_again == 'N' or search_again == 'n' or search_again == 'т' or search_again == 'Т':
                print('*' * 100)
                return False
            elif search_again == 'Y' or search_again == 'y' or search_again == 'н' or search_again == 'Н':
                print('*' * 100)
                return True
            else:
                print('Вы ввели неправильную комманду')

    def checking_for_existance_in_DB(self):
        """Функция проверяющая наличие искомого пользователя в списке понравившихся людей или в чёрном списке"""
        select_query = self.connection.execute("""SELECT vk_id FROM dating_user;
                                """).fetchall()
        for vk_id in select_query:
            if int(str(vk_id).strip('(),')) == self.dating_user_id:
                return True
        select_query = self.connection.execute("""SELECT vk_id FROM blacklist;
                                """).fetchall()
        for vk_id in select_query:
            if int(str(vk_id).strip('(),')) == self.dating_user_id:
                return True


if __name__ == '__main__':
    user_id, first_name, last_name, user_age, sex, city = get_user_info()
    while True:
        DBInfo = AddInfoToVKinterDB(user_id, first_name, last_name, user_age, sex, city, token)
        DBInfo.add_user_info()
        result = DBInfo.add_dating_user_info()
        if result:
            continue
        else:
            break
