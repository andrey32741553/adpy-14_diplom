from adpy_diplom.VKinter_functions_for_test import show_list_of_dating_users, show_blacklist_of_dating_users
from adpy_diplom.VKinter_database import engine

connection = engine.connect()


class Test_VKinter:

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
