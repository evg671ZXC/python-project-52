#!/usr/bin/env bash

show_message() {
    echo "$1"
}

install_poetry() {
    show_message "Установка Poetry..."
    
    # Устанавливаем Poetry
    curl -sSL https://install.python-poetry.org | python3 -
    
    show_message "Poetry успешно установлен!"

    export PATH="/root/.local/bin:$PATH"
}


install_poetry

exec ./build.sh