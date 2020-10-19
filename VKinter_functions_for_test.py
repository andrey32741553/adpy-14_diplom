from adpy_diplom.VKinter_database import engine

connection = engine.connect()


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
