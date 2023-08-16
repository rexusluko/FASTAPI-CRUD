1. Перейти в директорию проекта
2. в файле docker-compose в celery_worker заменить {your_path) на путь к директории
3. Для запуска приложения выполнить docker-compose up
4. Для проверки операций можно перейти по адресу http://localhost:8000/docs#/
5. Для проверки работы админки можно поменять содержимое admin/Menu.xlsx
6. Остановить контейнер приложения и удалить volume restaurant_postgres_data
7. Для запуска тестов выполнить docker-compose -f docker-compose-test.yaml up
8. Остановить контейнер приложения и удалить volume restaurant_postgres_data
9. Для проверки Postman тестов выполнить docker-compose -f docker-compose-postman.yaml up
