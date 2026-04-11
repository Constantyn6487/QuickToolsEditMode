import bpy
from . import addon_updater_ops as f1

_orig_ui = None
_orig_ui_condensed = None

# Функция-посредник для динамического перевода
def _(text):
    # Проверяем: включен ли перевод интерфейса И выбран ли именно русский язык
    prefs = bpy.context.preferences.view
    if prefs.use_translate_interface and prefs.language == 'ru_RU':
        # Пытаемся достать перевод из твоего словаря
        return bpy.app.translations.pgettext(text, "*")
    
    # Если интерфейс английский - возвращаем оригинальный текст без изменений
    return text

def ru_update_settings_ui(self, context, element=None):
    if element is None: element = self.layout
    box = element.box()
    
    if f1.updater.invalid_updater:
        box.label(text=_("Updater Error"))
        return
        
    settings = f1.get_user_preferences(context)
    if not settings: return

    box.label(text=_("Updater Settings"))
    row = box.row()
    
    split = f1.layout_split(row, factor=0.4)
    sub_col = split.column()
    sub_col.prop(settings, "auto_check_update", text=_("Auto-check"))
    
    sub_col = split.column()
    if not settings.auto_check_update: sub_col.enabled = False
    sub_row = sub_col.row(); sub_row.label(text=_("Interval between checks"))
    sub_row = sub_col.row(align=True)
    sub_row.prop(settings, "updater_interval_months", text=_("Months"))
    sub_row.prop(settings, "updater_interval_days", text=_("Days"))

    row = box.row(); col = row.column()
    
    if f1.updater.update_ready is None and not f1.updater.async_checking:
        col.scale_y = 2
        col.operator(f1.AddonUpdaterCheckNow.bl_idname, text=_("Check now for update"))
    elif f1.updater.update_ready:
        col.scale_y = 2
        col.operator(f1.AddonUpdaterUpdateNow.bl_idname, text=_("Update now"))
    else:
        col.scale_y = 2
        col.label(text=_("Addon is up to date"), icon='CHECKMARK')

    col = row.column(align=True)
    col.operator(f1.AddonUpdaterUpdateTarget.bl_idname, text=_("(Re)install addon version"))
    col.operator(f1.AddonUpdaterRestoreBackup.bl_idname, text=_("Restore addon backup"))

    row = box.row(); row.scale_y = 0.7
    last_check = f1.updater.json.get("last_check", "Never")
    # Добавил перевод и для "Never" через _()
    row.label(text=_("Last update check: ") + _(last_check))

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
