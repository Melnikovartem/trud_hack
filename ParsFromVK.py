import requests

token = 'dda4eeaddda4eeaddda4eeadaaddd61e23ddda4dda4eead82a032200963ecfbb7fcf175'

# Парсинг общей информации
def _information_about_user(user_link):
    global token
    fields = 'city,about,bdate,books,education,interests'
    response = requests.get(f'https://api.vk.com/method/users.get?access_token={token}&user_ids={user_link}&v=5.120&fields={fields}')
    if response.json()['response'][0]['is_closed']:
        return None
    return response.json()['response'][0]

# Парсинг друзей
def _ids_of_users_friends(user_id):
    global token
    response = requests.get(f'https://api.vk.com/method/friends.get?access_token={token}&user_id={user_id}&v=5.120&return_system=0&order=name')
    return response.json()['response']['items']

# Парсинг групп
def _information_about_users_groups(user_id):
    global token
    response = requests.get(f'https://api.vk.com/method/users.getSubscriptions?access_token={token}&user_id={user_id}&v=5.120&extended=1')
    return response.json()['response']['items']

def pars_from_vk(user_id):
    information_about_user = {}

    # Тут мы получаем общую информацию и смотрим закрыт ли профиль
    information_about_user = _information_about_user(user_id)
    if information_about_user is None:
        return (-1, -1, -1)

    user_id = information_about_user['id']

    ids_of_users_friends = _ids_of_users_friends(user_id)
    information_about_users_groups = _information_about_users_groups(user_id)
    temp = []
    for element in information_about_users_groups:
        temp.append(element['name'])
    information_about_users_groups = temp
    return (information_about_user, ids_of_users_friends, information_about_users_groups)

if __name__ == '__main__':
    a, b, c = pars_from_vk('zacontent')
    print(a)
    print('--------------------------------------------------------------------------------------')
    print(b)
    print('--------------------------------------------------------------------------------------')
    print(c)
    print('--------------------------------------------------------------------------------------')
