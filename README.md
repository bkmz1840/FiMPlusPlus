# Интерпретатор эзотерического языка FiM++
Версия 1.1

Автор: Васильев Илья (bkmz1840@gmail.com)

Ревью выполнили: Быков Роман


## Описание
Данное приложение является реализацией интерпретатора эзотерического языка FiM++. Скрипт может исполнять как и готовую программу, так и работать в режиме пошагового интерпритатора.


## Требования
* Python версии не ниже 3.6


## Состав
* Консольная версия: `fimpp.py`
* Тесты: `tests/`
* Примеры кода на языке FiM++: `examples/`


## Консольная версия
Справка по запуску: `./fimpp.py --help`

Пример запуска: `./fimpp.py`, `fimpp.py my_program.fpp`


## Подробности реализации
Классы, отвечающие за работу интерпритатора находятся в той же дериктории, что и сам интерпритатор. В основе реализации лежат два класса `Program`, исполняющий код из файла, указанного при запуске, и `Interpreter`, реализующий работу интерпритатора в пошаговом режиме, который принимает на вход предложение (обязательно со знаком пунктуации) и исполняет его.

Индиксация массивов начинается с нуля. Не используете `add X and Y` или любую другую конструкцию, которая содержит в себе `and`, в логическом выражении или в вызове метода, так как однозачно определить к чему относится `and` не возможно. Не заканчивайте предложение троеточием.

Использованная документация для реализации интерпритатора: https://docs.google.com/document/d/1gU-ZROmZu0Xitw_pfC1ktCDvJH5rM85TxxQf5pg_xmg/edit#heading=h.cuyv3gdkf95d
