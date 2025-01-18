#!/bin/bash

if ! command -v python3 &> /dev/null
then
    echo "Python3 не установлен. Пожалуйста, установите его и повторите попытку."
    exit
fi

if [ ! -d ".venv" ]; then
    echo "Создание виртуального окружения..."
    python3 -m venv .venv
else
    echo "Виртуальное окружение уже существует."
fi

echo "Активируем виртуальное окружение..."
source .venv/bin/activate

if [ ! -f "requirements.txt" ]; then
    echo "Файл requirements.txt не найден. Убедитесь, что он существует."
    exit
fi

echo "Установка зависимостей..."
pip install -r requirements.txt

if [ ! -f "main.py" ]; then
    echo "Файл main.py не найден. Убедитесь, что он существует."
    deactivate
    exit
fi

echo "Запуск main.py..."
python main.py

echo "Завершение работы. Деактивируем виртуальное окружение."
deactivate