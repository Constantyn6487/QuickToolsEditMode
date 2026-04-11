# Copyright (C) 2024 Constantyn Wasilyev (Constantyn6487)
# https://github.com/Constantyn6487/QuickToolsEditMode
# Originally an addon: 2023-Fast Panel Button, 2024-Quick Panel Button.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org>.
# ########################################################################

translations_dict = {
    "ru_RU": {
        # title panel
        ("*", "Active object is: "): "Активный объект:",
        ("*", "Go to in Edit Mode!"): "Перейдите в режим редактирования!",
        ("*", "Edge Crease:"): "Складка на ребре:",
        ("*", "Edge Bevel Weight:"): "Вес Фаски на ребре:",
        ("*", "Selection Data:"): "Данные выбора:",
        ("*", "Edges"): "Ребра",
        ("*", "Vertices"): "Вершины",
        ("*", "Smooth:"): "Сглаживание:",
        ("*", "Transform:"): "Трансформации:",
        # Name buttom
        ("*", "ShadeSmooth"): "Сгладить",
        ("*", "ShadeFlat"): "Плоский",
        ("*", "ApplyScale"): "Масштаб",
        ("*", "ApplyRotation"): "Вращение",
        # data Edges/Vertices
        ("*", "Enable data for selected edges"): "Включить данные выбранных рёбер",
        ("*", "Enable data for selected vertices"): "Включить данные выбранных вершин",
        # Crease/Weight
        ("*", "Set edge crease to 1.00"): "Установить складку ребра равной 1.00",
        ("*", "Set edge crease to 0.50"): "Установить складку ребра равной 0.50",
        ("*", "Set edge crease to 0.00"): "Установить складку ребра равной 0.00",
        ("*", "Set edge bevel weight to 1.00"): "Установить вес фаски ребра равным 1.00",
        ("*", "Set edge bevel weight to 0.50"): "Установить вес фаски ребра равным 0.50",
        ("*", "Set edge bevel weight to 0.00"): "Установить вес фаски ребра равным 0.00",
        # shade smooth/flat, apply scale/rotation
        ("*", "Apply smooth shading to selected faces"): "Применить мягкое затенение",
        ("*", "Apply flat shading to selected faces"): "Применить плоское затенение",
        ("*", "Apply scale transformation"): "Применить масштабирование",
        ("*", "Apply rotation transformation"): "Применить вращение",
        # Edit Category
        ("*", "Tab Category"): "Категория вкладок",
        # DonateLink
        ("*", "Support the project"): "Поддержать проект",
        ("*", "Support project on Boosty"): "Поддержите проект на Boosty",
        ("*", "Opens the Boosty donation page in the browser."): "Запуск страницы пожертвований Boosty в браузере",
        ("*", "Launching the browser..."): "Запуск браузера...",
        # Updater translations
        ("*", "Enable automatic update verification"): "Включить автоматическую проверку обновлений",
        ("*", "Months"): "Месяцы",
        ("*", "Days"): "Дни",
        ("*", "Hours"): "Часы",
        ("*", "Minutes"): "Минуты",
        # descriptions_ru.py
        ("*", "Updater Settings"): "Параметры обновления",
        ("*", "Auto-check"): "Авто-проверка",
        ("*", "Interval between checks"): "Интервал проверки",
        ("*", "Months"): "Месяцы",
        ("*", "Days"): "Дни",
        ("*", "Check now for update"): "Проверить обновление",
        ("*", "Update now"): "Обновить сейчас",
        ("*", "Addon is up to date"): "Аддон актуален",
        ("*", "(Re)install addon version"): "Выбор версии / Откат",
        ("*", "Restore addon backup"): "Восстановить бэкап",
        ("*", "Last update check: "): "Последняя проверка: ",
        ("*", "Last update check: "): "Последняя проверка: ",
        ("*", "Never"): "Никогда",
    }
}

def register():
    from bpy.app import translations
    translations.register(__name__, translations_dict)

def unregister():
    from bpy.app import translations
    translations.unregister(__name__)
