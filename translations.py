# -*- coding: utf-8 -*-

translations_dict = {
    "ru_RU": {
        #("*", "Quick Tools Edit Modes"): "Быстрые инструменты",
        ("*", "Active object is: "): "Активный объект:",
        ("*", "Go to in Edit Mode!"): "Перейдите в режим редактирования!",
        ("*", "Speed Crease:"): "Быстрый Crease:",
        ("*", "Speed Edge Bevel Weight:"): "Быстрый вес грани:",
        ("*", "Smoothing mode:"): "Режим сглаживания:",
        ("*", "Apply Mesh Transform:"): "Применить трансформации:",
        # Названия кнопок
        ("*", "Edge Bevel Weight 0.00"): "Вес грани 0.00",
        ("*", "Edge Bevel Weight 0.50"): "Вес грани 0.50",
        ("*", "Edge Bevel Weight 1.00"): "Вес грани 1.00",
        ("*", "Edge Crease 0.00"): "Crease 0.00",
        ("*", "Edge Crease 0.50"): "Crease 0.50",
        ("*", "Edge Crease 1.00"): "Crease 1.00",
        ("*", "Shade Smooth"): "Сгладить",
        ("*", "Shade Flat"): "Плоский",
        ("*", "Apply Scale"): "Применить масштаб",
        ("*", "Apply Rotation"): "Применить вращение",
        ("*", "ShadeSmooth"): "Сгладить",
        ("*", "ShadeFlat"): "Плоский",
        ("*", "ApplyScale"): "Масштаб",
        ("*", "ApplyRotation"): "Вращение",
        # Подсказки (descriptions)
        ("*", "Sets the Crease 0.00"): "Установить Crease 0.00",
        ("*", "Sets the Crease 0.50"): "Установить Crease 0.50",
        ("*", "Sets the Crease 1.00"): "Установить Crease 1.00",
        ("*", "Clear the Bevel Weight 0.00"): "Сбросить вес грани 0.00",
        ("*", "Clear the Bevel Weight 0.50"): "Сбросить вес грани 0.50",
        ("*", "Sets the Bevel Weight 1.00"): "Установить вес грани 1.00",
        ("*", "Adds Shade Smooth"): "Применить сглаживание",
        ("*", "Adds Shade Flat"): "Отменить сглаживание",
        ("*", "Apply reset Scale"): "Применить и сбросить масштаб",
        ("*", "Apply reset Rotation"): "Применить и сбросить вращение",
        # Окно попап
        ("*", "Fast Edge Crease, Bevel Weight (3 values) and Shading, Apply Transform access in Edit Mode"): "Быстрый Edge Crease, Bevel Weight (3 значения) и Shading, Примените Transformation (Rotation and Scale) из режима редактирования.",
        ("*", "Choose a name for the category of the panel"): "Укажите название категории панели",
        ("*", "Tab Category"): "Вкладка",
        ("*", "Tab Category:"): "Название вкладки:",
    }
}

def register():
    from bpy.app import translations
    translations.register(__name__, translations_dict)

def unregister():
    from bpy.app import translations
    translations.unregister(__name__)
