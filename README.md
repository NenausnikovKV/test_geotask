# Тестовое задание по геоданным

## Что делает

Программа позволяет создать полигоны посредством формы и drf поля, а также просмотреть список полигонов.
Использует Postgis для хранения данных в БД. 

Поддерживает пять адресов 

* http://127.0.0.1:8000/polygon/ - список адресов 
* http://127.0.0.1:8000/polygon/polygons/ - список имеющихся полигонов
* http://127.0.0.1:8000/polygon/form/ - форма для создания полигона
* http://127.0.0.1:8000/polygon/polygon-list/ - сгенерированная drf страница списка полигонов и создания нового
* http://127.0.0.1:8000/polygon/polygon/{n}/ - сгенерированная drf страница описание полигона с индексом n. Корректировка и удаление. 


## Установка 

### Необходимое ПО
* python 3.9.
* Установить необходимые пакеты для geodjango (https://docs.djangoproject.com/en/4.2/ref/contrib/gis/install/).
* Установить postgresql - для нее добавить расширение Postgis (https://docs.djangoproject.com/en/4.2/ref/contrib/gis/install/postgis/).

### Зависимости проекта
Установить зависимости
```
pip install -r path_to_requirements/requirements
```

## Запуск и тестирование

### Запуск проекта 
Запустить проект
```
python manage.py runserver
```
Перейти на локальный сервер \
http://127.0.0.1:8000/polygon/

### Тестирование
```
python manage.py test
```
