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

import bpy
from . import addon_updater_ops as f1

_orig_ui = None
_orig_ui_condensed = None

# Функция-посредник для динамического перевода
def _(context: bpy.types.Context, text: str) -> str:
    # Проверяем: включен ли перевод интерфейса И выбран ли именно русский язык
    prefs = context.preferences.view
    if prefs.use_translate_interface and prefs.language == 'ru_RU':
        # Пытаемся достать перевод из твоего словаря
        return bpy.app.translations.pgettext(text, "*")
    
    # Если интерфейс английский - возвращаем оригинальный текст без изменений
    return text

def ru_update_settings_ui(self, context, element=None):
    if element is None: element = self.layout
    box = element.box()
    
    if f1.updater.invalid_updater:
        box.label(text=_(context, "Updater Error"))
        return
        
    settings = f1.get_user_preferences(context)
    if not settings: return

    box.label(text=_(context, "Updater Settings"))
    row = box.row()
    
    split = f1.layout_split(row, factor=0.4)
    sub_col = split.column()
    sub_col.prop(settings, "auto_check_update", text=_(context, "Auto-check"))
    
    sub_col = split.column()
    if not settings.auto_check_update: sub_col.enabled = False
    sub_row = sub_col.row(); sub_row.label(text=_(context, "Interval between checks"))
    sub_row = sub_col.row(align=True)
    sub_row.prop(settings, "updater_interval_months", text=_(context, "Months"))
    sub_row.prop(settings, "updater_interval_days", text=_(context, "Days"))

    row = box.row(); col = row.column()
    
    if f1.updater.update_ready is None and not f1.updater.async_checking:
        col.scale_y = 2
        col.operator(f1.AddonUpdaterCheckNow.bl_idname, text=_(context, "Check now for update"))
    elif f1.updater.update_ready:
        col.scale_y = 2
        col.operator(f1.AddonUpdaterUpdateNow.bl_idname, text=_(context, "Update now"))
    else:
        col.scale_y = 2
        col.label(text=_(context, "Addon is up to date"), icon='CHECKMARK')

    col = row.column(align=True)
    col.operator(f1.AddonUpdaterUpdateTarget.bl_idname, text=_(context, "(Re)install addon version"))
    col.operator(f1.AddonUpdaterRestoreBackup.bl_idname, text=_(context, "Restore addon backup"))

    row = box.row(); row.scale_y = 0.7
    last_check = f1.updater.json.get("last_check", "Never")
    # Добавил перевод и для "Never" через _()
    row.label(text=_(context, "Last update check: ") + _(context, last_check))

def register():
    global _orig_ui, _orig_ui_condensed
    
    # 1. Сохраняем оригиналы
    _orig_ui = f1.update_settings_ui
    _orig_ui_condensed = f1.update_settings_ui_condensed
    
    # 2. Подменяем функции отрисовки
    f1.update_settings_ui = ru_update_settings_ui
    f1.update_settings_ui_condensed = ru_update_settings_ui

    # 3. Устанавливаем ключи для перевода подсказок (tooltips)
    fixes = [
        (f1.AddonUpdaterCheckNow, "Check now for update", "Search for a new version now"),
        (f1.AddonUpdaterUpdateNow, "Update now", "Download and install the latest version"),
        (f1.AddonUpdaterUpdateTarget, "(Re)install addon version", "Install a specific version"),
        (f1.AddonUpdaterRestoreBackup, "Restore addon backup", "Restore from backup folder")
    ]
    for cls, label, desc in fixes:
        cls.bl_label = label
        cls.bl_description = desc

def unregister():
    global _orig_ui, _orig_ui_condensed
    # Возвращаем всё как было при выключении
    if _orig_ui is not None:
        f1.update_settings_ui = _orig_ui
    if _orig_ui_condensed is not None:
        f1.update_settings_ui_condensed = _orig_ui_condensed
