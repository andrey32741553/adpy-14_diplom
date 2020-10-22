from adpy_diplom.VKinter_database import Session, engine, VKUser

connection = engine.connect()
session = Session()


def show_list_of_dating_users():
    id_user = input('Введите ID пользователя для вывода списка: ')
    select_query = connection.execute(f"""SELECT vk_id, dating_user_first_name, dating_user_last_name, age, 
    user_id, city, photo_link FROM dating_user d
    JOIN photos p ON p.vk_id_dating_user = d.vk_id
    WHERE user_id = {id_user};
    """).fetchall()
    print(f'Список понравившихся людей пользователя ID = {id_user}')
    return select_query


def show_blacklist_of_dating_users():
    id_user = input('Введите ID пользователя для вывода чёрного списка: ')
    select_query = connection.execute(f"""SELECT vk_id, dating_user_first_name, dating_user_last_name, age, city
    FROM blacklist
    WHERE user_id = {id_user};
    """).fetchall()
    print(f'Чёрный список пользователя ID = {id_user}:')
    return select_query


def add_user_info():
    """ Проверка наличия пользователя в БД, если такой есть - обновляются данные о дапазоне поиска. Если нет, то
    вносится информация о новом пользователе (else после цикла) """
    select_query = connection.execute("""SELECT vk_id FROM vk_user;
            """).fetchall()
    print(select_query)
    for user_id in select_query:
        if int(str(user_id).strip(',()')) == 111222333:
            session.query(VKUser).filter(VKUser.vk_id == 111222333).update(
                {"range_for_search_age": '20 - 80'}
            )
            session.commit()
            break
        else:
            continue
    else:
        session.add_all([VKUser(vk_id=111222333, first_name='Вася',
                                last_name='Пупкин', user_age=90,
                                range_for_search_age='18 - 90',
                                sex='мужской', city='Васюки')])
        session.commit()
    select_query_for_test = connection.execute("""SELECT vk_id, range_for_search_age FROM vk_user
    WHERE vk_id = 111222333;
    """).fetchall()
    return select_query_for_test
