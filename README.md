# Apache Log Aggregator

## Описание
Приложение для парсинга, агрегации и визуализации логов доступа к веб-серверу Apache. Приложение предоставляет следующие возможности:

- Парсинг логов Apache из указанной директории.
- Сохранение данных логов в базу данных SQLite для удобного хранения и извлечения.
- Просмотр агрегированных логов с фильтрацией по дате, IP-адресу и статусу ответа.
- Автоматический парсинг логов в фоновом режиме с настраиваемым интервалом.
- Подсветка синтаксиса для удобства просмотра.

## Установка

1. **Установка Python:** Убедитесь, что на вашем компьютере установлен Python. Вы можете загрузить последнюю версию с официального сайта Python: [https://www.python.org/downloads/](https://www.python.org/downloads/).

2. **Установка зависимостей:** Установите необходимые зависимости, выполнив следующую команду:

   ```bash
   pip install -r requirements.txt
   ```

3. **Настройка путей:**
   -  **В файле `config.ini` измените переменную `files_dir` на путь к вашей директории с логами Apache.** 

## Использование

1. **Запуск приложения:**
   ```bash
   python main.py
   ```
2. **Настройка базы данных:**
    - Нажмите кнопку "**Setup Database**", чтобы создать базу данных и таблицы.
    - Нажмите кнопку "**Drop Database**", чтобы удалить базу данных и таблицы (будьте осторожны, это действие необратимо).

3. **Парсинг логов:**
   -  Нажмите кнопку "**Parse Logs**", чтобы начать парсинг логов Apache. Результаты будут отображены в текстовом поле.

4. **Просмотр логов:**
    - Введите диапазон дат (необязательно).
    - Выберите фильтр (IP, Status) и введите значение (необязательно).
    - Нажмите кнопку "**View Logs**", чтобы отобразить отфильтрованные логи. 

5. **Автоматический парсинг:**
   -  Приложение автоматически парсит новые логи в фоновом режиме.
   - Вы можете изменить интервал парсинга (в секундах) в поле "Parsing Interval" и нажать кнопку "**Update Interval**".

6. **Закрытие приложения:**
   -  Закрытие окна приложения не остановит фоновый парсинг.
   - Чтобы полностью закрыть приложение, нажмите "**OK**" в диалоговом окне подтверждения при закрытии окна.

7. **Настройка config.ini:**
    -  **В файле `config.ini` измените переменную `files_dir` на путь к вашей директории с логами Apache.**
    -  **В файле `config.ini` измените переменную `ext` на расширение логов Apache.**
    -  **В файле `config.ini` измените переменную `db` на путь к вашей базе данных.**
    -  **В файле `config.ini` измените переменную `format` на формат логов Apache.**

## Пример использования

1. Запустите приложение `python main.py`.
2. Настройте базу данных, нажав кнопку "Setup Database".
3. Укажите путь к вашим логам Apache в `parser.py`.
4. Нажмите кнопку "Parse Logs", чтобы начать парсинг.
5. Просмотрите агрегированные логи, используя фильтры по дате, IP и статусу.

## Примечания

- Приложение использует базу данных SQLite для хранения логов.
- Фоновый парсинг позволяет приложению обновлять данные без вмешательства пользователя.
- Подсветка синтаксиса улучшает читаемость логов.
