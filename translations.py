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
        # Title panel
        ("*", "Active object is: "): "Активный объект:",
        ("*", "Go to in Edit Mode!"): "Перейдите в режим редактирования!",
        ("*", "Edge Crease:"): "Складка на ребре:",
        ("*", "Edge Bevel Weight:"): "Вес Фаски на ребре:",
        ("*", "Selection Data:"): "Данные выбора:",
        ("*", "Edges"): "Ребра",
        ("*", "Vertices"): "Вершины",
        ("*", "Smooth:"): "Сглаживание",
        ("*", "Transform:"): "Трансформации:",
        ("*", "Open the sidebar and go to the add-ons tab to select the data"): "Откройте боковую панель и перейдите на вкладку дополнения, чтобы выбрать данные",
        # Name buttons (Standardized Case)
        ("*", "ShadeSmooth"): "Сгладить",
        ("*", "ShadeFlat"): "Плоский",
        ("*", "ApplyScale"): "Масштаб",
        ("*", "ApplyRotation"): "Вращение",
        ("*", "Shade Auto Smooth"): "Автосглаживание",
        ("*", "Auto Smooth"): "Автосглаживание",
        ("*", "Angle"): "Угол",
        ("*", "Shade Auto Smooth"): "Сглаживание с автосглаживанием",
        ("*", "Enable auto smooth shading"): "Включить автосглаживание затенения",
        ("*", "Render and display faces smooth using vertex normals"): "Рендерить и отображать грани гладко с использованием нормалей вершин",
        # data Edges/Vertices
        ("*", "Enable data for selected edges"): "Включить данные выбранных рёбер",
        ("*", "Enable data for selected vertices"): "Включить данные выбранных вершин",
        # Context Menu & Panel Buttons (Fixed Case & Dynamic Values)
        ("*", "Select edge data, open N-Panel!"): "Выберите данные ребер, откройте N-панель!",
        ("*", "Edge Crease 1.00"): "Складка 1.00",
        ("*", "Edge Crease 0.50"): "Складка 0.50",
        ("*", "Edge Crease 0.00"): "Складка 0.00",
        ("*", "Edge Bevel 1.00"): "Вес фаски 1.00",
        ("*", "Edge Bevel 0.50"): "Вес фаски 0.50",
        ("*", "Edge Bevel 0.00"): "Вес фаски 0.00",
        # Crease/Weight
        ("*", "Set edge crease to 1.00"): "Установить складку ребра равной 1.00",
        ("*", "Set edge crease to 0.50"): "Установить складку ребра равной 0.50",
        ("*", "Set edge crease to 0.00"): "Установить складку ребра равной 0.00",
        ("*", "Set edge bevel weight to 1.00"): "Установить вес фаски ребра равным 1.00",
        ("*", "Set edge bevel weight to 0.50"): "Установить вес фаски ребра равным 0.50",
        ("*", "Set edge bevel weight to 0.00"): "Установить вес фаски ребра равным 0.00",
        # shade smooth/flat, apply scale/rotation
        ("*", "Apply smooth shading to selected faces"): "Применить сглаживание к граням",
        ("*", "Apply flat shading to selected faces"): "Применить плоское затенение",
        ("*", "Apply scale transformation"): "Применить масштаб",
        ("*", "Apply rotation transformation"): "Применить вращение",
        ("*", "Apply auto smooth shading"): "Применить автосглаживание",
        # DonateLink
        ("*", "Support the project"): "Поддержать проект",
        ("*", "Support project on Boosty"): "Поддержать на Boosty",
        ("*", "Opens the Boosty donation page in the browser."): "Запуск страницы поддержки чайком разработчика на Boosty в браузере",
        ("*", "Launching the Boosty in browser"): "Запуск страницы Boosty в браузере",
        ("*", "Tab Category"): "Категория вкладки",
        # Updater Settings (UI) / descriptions_ru.py
        ("*", "Updater Settings"): "Параметры обновления",
        ("*", "Auto-check"): "Авто-проверка",
        ("*", "Interval between checks"): "Интервал проверки",
        ("*", "Months between update checks"): "Месяцев между проверками обновлений",
        ("*", "Days between update checks"): "Дней между проверками обновлений",
        ("*", "Check now for update"): "Проверить обновление сейчас",
        ("*", "Update now"): "Обновить сейчас",
        ("*", "Addon is up to date"): "Актуальная версия",
        ("*", "(Re)install addon version"): "Выбор версии / Откат",
        ("*", "Restore addon backup"): "Восстановить из бэкапа",
        ("*", "Last update check: "): "Последняя проверка: ",
        ("*", "Never"): "Никогда",
        ("*", "Search for a new version now"): "Искать новую версию сейчас",
        ("*", "Download and install the latest version"): "Скачать и установить последнюю версию",
        ("*", "Enable automatic update verification"): "Включить автоматическую проверку обновлений",
        ("*", "Install a specific version"): "Установить конкретную версию",
        ("*", "Restore from backup folder"): "Восстановить из папки бэкапов",
        ("*", "Updater Error"): "Ошибка обновления",
        # Updater translations
        ("*", "Months"): "Месяцы",
        ("*", "Days"): "Дни",
    }
}

def register():
    from bpy.app import translations
    translations.register(__name__, translations_dict)

def unregister():
    from bpy.app import translations
    translations.unregister(__name__)
