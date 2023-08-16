### запуск контейнера с приложением
docker-compose up app

### запуск тестов в отдельном контейнере
docker-compose up pytest

### Upd: БД заполняется из Exel-файла, при обновлении данных в файле -> в БД так же происходит обновление этих записей без предварительного их удаления как было реализовано ранее, постороено на внедрении дополнительных индексов в БД. Запрос удаления записи из базы используется только в том случае, если эту запись действительно удалили в самом excel-файле. В случае некорректного ввода данных, запись не добавляется.
Так же изменены модели для генерации новых миграций. Новые миграции так же запушены в гит.
