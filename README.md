# Команда Папамс, **хакатон TrudHack**
- **Папка artem**.

Здесь содержится работа с датасетом, который вы выдали на хакатоне.
____
- Папка **vk_alg**.

Здесь содержится алгоритм для определния профессии **Вконтакте**. Файл Graph - строит граф из ключевых слов. Файл FirstChapter - содержит сам алгоритм определения профессии. Файл Aho-Coras содержит алгоритм Ахо-Корасика для быстрого нахождения ключевых слов в детерменированном автомате. Все остальные файлы вспомогательные, в которых хранится информация для обучения алгоритмов(например id конкретных профессий).
____
- Папка **linkedIn_alg**.

Здесь содержится алгоритм для определения профессии в **LinkedIn**. Так как на сайте уже и указаны и профессии и навыки, которыми владеет человек, то по сути мы используем там только парсер. В файле secondChapter содержится алгоритм(по сути просто вызывание парсера)
____
- **Остальные**.

Все остальные файлы, которые начинаются на **Pars** это парсеры, в некоторых из них идет взаимодествие с api например как вконтакте, однако в других идет работа с chrome driver и библиотекой selenium для получения данных с профиля.
