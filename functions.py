import requests


def get_repos_stats(user_name: str) -> list[dict]:
    """Собирает статистику по репозиториям пользователя"""

    url = f'https://api.github.com/users/{user_name}/repos'
    # делаем get запрос к API
    response = requests.get(url)
    # проверяем статус код
    if response.status_code == 200:
        repos = response.json()
        # пустой список для результатов
        stats = []
        # итерируем, возвращаемые с запроса результаты
        for repo in repos:
            # достаем нужные данные по ключам
            repo_stats = {
                'name': repo['name'],
                'url': repo['html_url'],
                'stars': repo['stargazers_count'],
                'forks': repo['forks_count'],
                'watchers': repo['watchers_count']
            }
            # добавляем в итоговую таблицу
            stats.append(repo_stats)
        # возвращаем результат
        return stats
    # если запрос не прошел, возвращаем None
    return None