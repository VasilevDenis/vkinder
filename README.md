# Документация по использованию программы-бота VKinder 3.0.
Данная документация предоставляет подробную информацию о функциональности и использовании программы-бота VKinder 3.0.
![Logo_VKinder](https://github.com/VasilevDenis/vkinder/blob/document/Logo_VKinder.jpg)

## Введение.
VKinder 3.0 - это программа-бот, разработанный на языке Python, который позволяет пользователям находить потенциальных партнеров для знакомств на основе их предпочтений и данных из социальной сети ВКонтакте.

### Инструменты и зависимости.
Перед использованием программы-бота VKinder 3.0 убедитесь, что у вас установлены следующие инструменты и зависимости:

* Python 3.x: VKinder 3.0 разработан на языке Python, поэтому вам понадобится установленная версия Python 3.x на вашем компьютере. Вы можете загрузить Python с официального сайта [Python](https://www.python.org).

* IDE: Рекомендуется использовать IDE (интегрированную среду разработки) для Python, такую как PyCharm, для удобного разработки и запуска программы-бота.

* Git и GitHub: Git - это система контроля версий, а GitHub - хостинг репозиториев Git. Убедитесь, что у вас установлен Git и что у вас есть аккаунт на GitHub для управления и совместной разработки кода.

* PostgreSQL и PgAdmin: VKinder 3.0 использует базу данных PostgreSQL для хранения информации о пользователях. Убедитесь, что у вас установлен PostgreSQL и PgAdmin для настройки и управления базой данных. Вы можете загрузить [PostgreSQL](https://www.postgresql.org) и [PgAdmin](https://www.pgadmin.org) с официальных веб-сайтов.

* ВКонтакте: VKinder 3.0 взаимодействует с социальной сетью ВКонтакте для получения данных о пользователях. У вас должна быть создана группа в ВКонтакте, от имени которой будет общаться программный бот. Инструкцию по созданию группы можно найти на официальном сайте [ВКонтакте](https://vk.com).

### Установка и настройка.
Прежде чем начать использовать программу-бота VKinder 3.0, выполните следующие шаги:

**1. Склонируйте репозиторий:** Склонируйте репозиторий проекта с помощью Git на ваш компьютер. Выполните команду git clone <URL репозитория> в командной строке, указав URL репозитория VKinder 3.0.

**2. Установите зависимости:** Перейдите в директорию проекта VKinder 3.0 и установите необходимые зависимости, указанные в файле requirements.txt. Выполните команду pip install -r requirements.txt в командной строке.

**3. Настройте базу данных:** Создайте базу данных PostgreSQL и используйте PgAdmin для настройки подключения к базе данных. Убедитесь, что у вас есть информация о хосте, порту, имени базы данных, имени пользователя и пароле для подключения к базе данных.

**4. Получите токен ВКонтакте:** Следуйте инструкциям на официальном сайте ВКонтакте, чтобы получить токен для вашей группы ВКонтакте. Вам понадобится токен для взаимодействия с API ВКонтакте.

**5. Настройте конфигурацию:** В директории проекта VKinder 3.0 найдите файл constants.py. Откройте его и настройте следующие параметры:

* db_uri: Параметры подключения к Ваше Базе Данных.
* APP_TOKEN: Токен для взаимодействия приложения API ВКонтакте.
* TOKEN: Личный токен для парсинга пользователей API ВКонтакте.
* API_VERSION: Текущая версия API ВКонтакте.
После настройки вы можете приступить к использованию программы-бота VKinder 3.0.

### Запуск программы-бота.
Для запуска программы-бота VKinder 3.0 выполните следующие шаги:

**1.** Откройте терминал или командную строку и перейдите в директорию проекта VKinder 3.0.

**2.** Выполните запуск программы-бота через файл main.py.

**3.** Убедитесь, что бот успешно запущен и готов к работе.

### Использование программы-бота.
После успешного запуска программы-бота VKinder 3.0 вы можете использовать его для поиска людей для знакомств. Следуйте инструкциям бота и используйте команды для взаимодействия с ботом. Ниже приведены основные команды и функции программы-бота VKinder 3.0:

**1.** Поиск людей для знакомств:
* Отправьте сообщение боту "START", либо нажмите соответствующую кнопку.
* Бот произведет поиск пользователей ВКонтакте, подходящих Вам, а именно: выдаст пользователей противоположного пола, с тем же возрастом и из Вашего города. 
* Получите информацию о найденных пользователях, включая имя, фамилию, ссылку на профиль и три самые популярные фотографии.

**2.** Сохранение пользователя в список избранных:
* При получении информации о пользователе, вы можете сохранить его в список избранных с помощью команды "Like".
* Выбрав кнопку "Like", пользователь добавится в список избранных.

**3.** Взаимодействие с найденными пользователями:
* При получении информации о найденных пользователях, вы можете перейти к следующему пользователю нажав кнопку "Dislike".
* Выбрав "Dislike", пользователь больше не будет Вам выводиться.

**4.** Вывод списка избранных людей:
* Нажмите кнопку "Favorites" для вывода списка избранных людей.
* Бот выведет информацию о пользователях из списка избранных.

### Заключение.
Документация по использованию программы-бота VKinder 3.0 предоставляет вам все необходимые инструкции и указания для настройки и использования. Следуйте инструкциям, командам и рекомендациям, чтобы получить оптимальный опыт использования программы-бота. Удачи в поисках второй половинки! VKinder 3.0!

### Дополнительные материалы.
В данной секции приведены дополнительные материалы и инструменты, которые могут быть полезными при разработке и использовании программы-бота VKinder.

* [Python](https://www.python.org) - Официальный сайт Python.
* [PyCharm](https://www.jetbrains.com/pycharm/) - Интегрированная среда разработки для Python.
* [Git](https://git-scm.com) - Официальный сайт Git.
* [GitHub](https://github.com) - Хостинг репозиториев Git.
* [PostgreSQL](https://www.postgresql.org) - Официальный сайт PostgreSQL.
* [PgAdmin](https://www.pgadmin.org) - Официальный сайт PgAdmin.
* [API ВКонтакте](https://vk.com/dev/manuals) - Документация по API ВКонтакте.
