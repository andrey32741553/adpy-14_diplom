from pprint import pprint
from VKinter_queries import get_user_info, AddInfoToVKinterDB, VariableActionsWithDatingUsers
from VKinter_classes import token
from VKinter_database import Session, engine

print('Здравствуйте, Вас приветствует программа VKinter!')


class Main:

    @staticmethod
    def choose_command():
        while True:
            print('Что вы хотите сделать?\n'
                  'Ввести данные пользователя и начать поиск по Вашим критериям - 1\n'
                  'Показать список понравившихся людей для конкретного пользователя - 2\n'
                  'Удалить понравившихся людей из списка пользователя - 3\n'
                  'Внести пользователя в чёрный список - 4\n'
                  'Показать чёрный список пользователя - 5\n'
                  'Выйти из программы - 0')
            command = int(input('Введите номер комманды: '))
            if command == 1:
                user_id, first_name, last_name, user_age, sex, city = get_user_info()
                while True:
                    DBInfo = AddInfoToVKinterDB(user_id, first_name, last_name, user_age, sex, city, token)
                    DBInfo.add_user_info()
                    result = DBInfo.add_dating_user_info()
                    if result:
                        continue
                    else:
                        break

            elif command == 2:
                actions = VariableActionsWithDatingUsers(Session, engine)
                pprint(actions.show_list_of_dating_users())
                print('*' * 100)

            elif command == 3:
                print('Для удобства сперва будет выведен список понравившихся людей пользователя')
                actions = VariableActionsWithDatingUsers(Session, engine)
                pprint(actions.show_list_of_dating_users())
                print('*' * 100)
                actions.deleting_dating_user()

            elif command == 4:
                actions = VariableActionsWithDatingUsers(Session, engine)
                actions.add_dating_user_to_blacklist()
                print('*' * 100)

            elif command == 5:
                actions = VariableActionsWithDatingUsers(Session, engine)
                pprint(actions.show_blacklist_of_dating_users())
                print('*' * 100)

            elif command == 0:
                exit()

            else:
                print('Неправильная комманда')

VKinter = Main()
VKinter.choose_command()
