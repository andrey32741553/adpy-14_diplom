from VKinter_functions_for_test import show_list_of_dating_users, show_blacklist_of_dating_users,\
    add_user_info
from VKinter_database import engine

connection = engine.connect()


class TestVKinter:

    def setup(self):
        print('method setup')

    def teardown(self):
        print('method teardown')

    def test_show_list_of_dating_users(self, monkeypatch):
        monkeypatch.setattr('builtins.input', lambda x: 12345678)
        assert show_list_of_dating_users() == connection.execute("""SELECT vk_id, dating_user_first_name,
        dating_user_last_name, age, user_id, city, photo_link FROM dating_user d
    JOIN photos p ON p.vk_id_dating_user = d.vk_id
    WHERE user_id = 12345678;
    """).fetchall()

    def test_show_blacklist_of_dating_users(self, monkeypatch):
        monkeypatch.setattr('builtins.input', lambda x: 12345678)
        assert show_blacklist_of_dating_users() == connection.execute(f"""SELECT vk_id, dating_user_first_name,
    dating_user_last_name, age, city
    FROM blacklist
    WHERE user_id = 12345678;
    """).fetchall()

    def test_add_user_info(self):
        assert add_user_info() == connection.execute("""SELECT vk_id, range_for_search_age FROM vk_user
    WHERE vk_id = 111222333;
    """).fetchall()
