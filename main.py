from pprint import pprint
from adpy_diplom.VKinter_queries import get_user_info, AddInfoToVKinterDB, VariableActionsWithDatingUsers
from adpy_diplom.VKinter_classes import token
from adpy_diplom.VKinter_database import Session, engine

print('Здравствуйте, Вас приветствует программа VKinter!')


class main:

    def choose_command(self):
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
                    self.DBInfo = AddInfoToVKinterDB(user_id, first_name, last_name, user_age, sex, city, token)
                    self.DBInfo.add_user_info()
                    result = self.DBInfo.add_dating_user_info()
                    if result:
                        continue
                    else:
                        break

            elif command == 2:
                self.actions = VariableActionsWithDatingUsers(Session, engine)
                pprint(self.actions.show_list_of_dating_users())
                print('*' * 100)

            elif command == 3:
                print('Для удобства сперва будет выведен список понравившихся людей пользователя')
                self.actions = VariableActionsWithDatingUsers(Session, engine)
                pprint(self.actions.show_list_of_dating_users())
                print('*' * 100)
                self.actions.deleting_dating_user()

            elif command == 4:
                self.actions = VariableActionsWithDatingUsers(Session, engine)
                self.actions.add_dating_user_to_blacklist()
                print('*' * 100)

            elif command == 5:
                self.actions = VariableActionsWithDatingUsers(Session, engine)
                pprint(self.actions.show_blacklist_of_dating_users())
                print('*' * 100)

            elif command == 0:
                exit()

            else:
                print('Неправильная комманда')

VKinter = main()
VKinter.choose_command()
