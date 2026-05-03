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

bl_info = {
    "name": "Quick Tools Edit Mode",
    "blender": (3, 6, 0),
    "location": "View3D > Sidebar > Item",
    "category": "Object",
    "version": (2, 1, 0),
    "author": "Constantyn Wasilyev (Constantyn6487)",
    "description": "Fast Edge Crease, Bevel Weight (3 values) and Shading, Apply Transform access in Edit Mode",
}

import bpy
from bpy.types import Panel, AddonPreferences, PropertyGroup, Menu
from bpy.props import StringProperty, BoolProperty, IntProperty, PointerProperty
from bpy.utils import register_class, unregister_class

from . import donates
from . import bmesh
from . import descriptions_ru

try:
    from . import translations
    from . import addon_updater_ops
except ImportError:
    translations = None
    addon_updater_ops = None


# ===========================================================================
# UI HELPERS
# ===========================================================================

def get_ui_text(context: bpy.types.Context, text: str) -> str:
    """Переводит текст интерфейса, если включен перевод."""
    if not context.preferences.view.use_translate_interface:
        return text
    return bpy.app.translations.pgettext(text)


def get_icon(preferred: str, fallback: str) -> str:
    """Проверяет наличие иконки, возвращает fallback если нет."""
    icons = bpy.types.UILayout.bl_rna.functions["prop"].parameters["icon"].enum_items
    return preferred if preferred in icons else fallback


def update_panel(self, context):
    """Обновляет категорию панели при изменении настроек."""
    try:
        unregister_class(BAR_PT_Panel)
        BAR_PT_Panel.bl_category = self.category
        register_class(BAR_PT_Panel)
    except Exception as e:
        print(f"Error updating panel category: {e}")


# ===========================================================================
# PREFERENCES
# ===========================================================================

@addon_updater_ops.make_annotations if addon_updater_ops else lambda x: x
class QuickToolsEditModePreferences(AddonPreferences):
    bl_idname = __package__

    category: StringProperty(
        name="Tab Category",
        default="QuickToolsEditMode",
        update=update_panel,
    )  # type: ignore

    auto_check_update: BoolProperty(
        name="Auto-check",
        description="Enable automatic update verification",
        default=False
    )  # type: ignore

    updater_interval_months: IntProperty(
        name="Months",
        description="Months between update checks",
        default=1,
        min=0
    )  # type: ignore

    updater_interval_days: IntProperty(
        name="Days",
        description="Days between update checks",
        default=3,
        min=0
    )  # type: ignore

    updater_interval_hours: IntProperty(
        name="Hours",
        description="Hours",
        default=0
    ) # type: ignore vscode

    updater_interval_minutes: IntProperty(
        name="Minutes",
        description="Minutes",
        default=0
    ) # type: ignore vscode

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "category")
        box = layout.box()
        row = box.row(align=True)
        row.label(text="Support the project", icon="FUND")
        row.operator(
            "wm.open_donate_link",
            icon="HEART",
            text=get_ui_text(context, "Support project on Boosty"),
        )

        layout.separator()

        if addon_updater_ops:
            addon_updater_ops.update_settings_ui(self, context)


# ===========================================================================
# PROPERTY GROUP
# ===========================================================================

class QuickToolsSettings(PropertyGroup):
    affect_edges: BoolProperty(
        name="Edges",
        default=True,
        description="Enable data for selected edges"
    )  # type: ignore

    affect_vertices: BoolProperty(
        name="Vertices",
        default=False,
        description="Enable data for selected vertices"
    )  # type: ignore


# ===========================================================================
# UI ELEMENTS
# ===========================================================================

class VIEW3D_MT_edit_mesh_QuickPanelButtons(Menu):
    bl_label = "QuickToolsEditMode"

    def draw(self, context):
        layout = self.layout
        settings = context.scene.quick_tools_settings
        is_enabled = settings.affect_edges or settings.affect_vertices

        if not is_enabled:
            error_col = layout.column(align=True)
            error_col.alert = True
            box = error_col.box()
            box.scale_y = 1.2
            box.operator(
                "button.open_n_panel",
                text=get_ui_text(context, "Select edge data, open N-Panel!"),
                icon='ERROR',
                emboss=False
            )
            layout.separator()

        col = layout.column()
        col.enabled = is_enabled

        # Edge Crease
        for v in [0.0, 0.5, 1.0]:
            text_key = f"Edge Crease {v:.2f}"
            op = layout.operator(
                "button.weight_set",
                text=get_ui_text(context, text_key),
                icon=get_icon('EDGE_CREASE', 'MOD_SUBSURF')
            )
            op.value = v
            op.mode = "CREASE"

        col.separator()

        # Edge Bevel
        for v in [0.0, 0.5, 1.0]:
            text_key = f"Edge Bevel {v:.2f}"
            op = layout.operator(
                "button.weight_set",
                text=get_ui_text(context, text_key),
                icon=get_icon('EDGE_BEVEL', 'MOD_BEVEL')
            )
            op.value = v
            op.mode = "BEVEL"

        layout.separator()

        # Auto Smooth
        if bpy.app.version < (4, 1, 0):
            obj = context.active_object
            if obj and obj.type == "MESH":
                layout.operator(
                    "button.enable_auto_smooth",
                    text=get_ui_text(context, "Shade Auto Smooth"),
                    icon=get_icon('SHADING_SMOOTH', 'MOD_SMOOTH')
                )
        else:
            op = layout.operator(
                "button.quick_action",
                text=get_ui_text(context, "Shade Auto Smooth"),
                icon=get_icon('SHADING_SMOOTH', 'MOD_SMOOTH')
            ).action = "AUTO_SMOOTH"

        layout.separator()

        # Shade Smooth / Flat
        layout.operator(
            "button.quick_action",
            text=get_ui_text(context, "ShadeSmooth"),
            icon=get_icon('SHADING_SMOOTH', 'MESH_UVSPHERE')
        ).action = 'SMOOTH'
        layout.operator(
            "button.quick_action",
            text=get_ui_text(context, "ShadeFlat"),
            icon=get_icon('SHADING_FLAT', 'MESH_ICOSPHERE')
        ).action = 'FLAT'

        layout.separator()

        # Transform
        layout.operator(
            "button.quick_action",
            text=get_ui_text(context, "ApplyScale"),
            icon=get_icon('TRANSFORM_SCALE', 'FULLSCREEN_ENTER')
        ).action = 'SCALE'
        layout.operator(
            "button.quick_action",
            text=get_ui_text(context, "ApplyRotation"),
            icon=get_icon('ORIENTATION_GLOBAL', 'ORIENTATION_GIMBAL')
        ).action = 'ROTATION'


class BAR_PT_Panel(Panel):
    bl_idname = "VIEW3D_PT_example_panels"
    bl_label = "Quick Tools Edit Modes"
    bl_category = "QuickToolsEditMode"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        obj = context.object
        settings = context.scene.quick_tools_settings

        if context.mode != "EDIT_MESH":
            box = layout.box()
            box.alert = True
            box.label(text=get_ui_text(context, "Go to in Edit Mode!"), icon="ERROR")
            return

        if obj:
            row = layout.row()
            row.label(text=get_ui_text(context, "Active object is: "), icon="OBJECT_DATA")
            box = layout.box()
            box.label(text=obj.name, icon="EDITMODE_HLT")

        # Selection toggles
        main_box = layout.box()
        main_box.label(text=get_ui_text(context, "Selection Data:"), icon="OUTLINER_DATA_MESH")
        row = main_box.row(align=True)
        row.prop(settings, "affect_edges", toggle=True, text=get_ui_text(context, "Edges"))
        row.prop(settings, "affect_vertices", toggle=True, text=get_ui_text(context, "Vertices"))

        main_box.separator()

        # Edge Crease
        main_box.label(
            text=get_ui_text(context, "Edge Crease:"),
            icon=get_icon("EDGE_CREASE", "MOD_SUBSURF")
        )
        col = main_box.column(align=True)
        col.enabled = settings.affect_edges or settings.affect_vertices
        spl = col.split(align=True)
        op = spl.operator("button.weight_set", text="1.00"); op.value = 1.0; op.mode = "CREASE"
        op = spl.operator("button.weight_set", text="0.50"); op.value = 0.5; op.mode = "CREASE"
        op = spl.operator("button.weight_set", text="0.00"); op.value = 0.0; op.mode = "CREASE"

        main_box.separator()

        # Edge Bevel
        main_box.label(
            text=get_ui_text(context, "Edge Bevel Weight:"),
            icon=get_icon("EDGE_BEVEL", "MOD_BEVEL")
        )
        col = main_box.column(align=True)
        col.enabled = settings.affect_edges or settings.affect_vertices
        spl = col.split(align=True)
        op = spl.operator("button.weight_set", text="1.00"); op.value = 1.0; op.mode = "BEVEL"
        op = spl.operator("button.weight_set", text="0.50"); op.value = 0.5; op.mode = "BEVEL"
        op = spl.operator("button.weight_set", text="0.00"); op.value = 0.0; op.mode = "BEVEL"

        # Smooth tools
        layout.label(text=get_ui_text(context, "Smooth:"))
        col = layout.column(align=True)

        if bpy.app.version < (4, 1, 0):
            mesh = obj.data
            col.prop(
                mesh,
                "use_auto_smooth" if hasattr(mesh, "use_auto_smooth") else "auto_smooth",
                text=get_ui_text(context, "Auto Smooth")
            )
            sub = col.column(align=True)
            sub.active = (
                getattr(mesh, "use_auto_smooth", getattr(mesh, "auto_smooth", False))
                and not mesh.has_custom_normals
            )
            if hasattr(mesh, "auto_smooth_angle"):
                sub.prop(mesh, "auto_smooth_angle", toggle=True, text=get_ui_text(context, "Angle"))
            else:
                sub.prop(mesh, "smooth_angle", toggle=True, text=get_ui_text(context, "Angle"))
        else:
            op = col.operator("button.quick_action", text=get_ui_text(context, "Shade Auto Smooth"))
            op.action = 'AUTO_SMOOTH'

        # Shade Smooth / Flat
        row = col.row(align=True)
        row.operator("button.quick_action", text=get_ui_text(context, "ShadeSmooth")).action = 'SMOOTH'
        row.operator("button.quick_action", text=get_ui_text(context, "ShadeFlat")).action = 'FLAT'

        # Transform
        layout.label(text=get_ui_text(context, "Transform:"))
        col = layout.column(align=True)
        spl = col.split(align=True)
        spl.operator("button.quick_action", text=get_ui_text(context, "ApplyScale")).action = 'SCALE'
        spl.operator("button.quick_action", text=get_ui_text(context, "ApplyRotation")).action = 'ROTATION'

        if addon_updater_ops:
            addon_updater_ops.update_notice_box_ui(self, context)

        layout.separator()
        row = layout.row()
        row.alignment = "RIGHT"
        row.enabled = False
        version_str = ".".join(map(str, bl_info["version"]))
        row.label(text=f"v{version_str}")


def draw_menu_prepend(self, context):
    self.layout.separator()
    self.layout.menu("VIEW3D_MT_edit_mesh_QuickPanelButtons")
    self.layout.separator()


# ===========================================================================
# REGISTRATION
# ===========================================================================

CLASSES = [
    QuickToolsEditModePreferences,
    QuickToolsSettings,
    BAR_PT_Panel,
    VIEW3D_MT_edit_mesh_QuickPanelButtons,
]


def register():
    if translations:
        translations.register()
    if addon_updater_ops:
        addon_updater_ops.register(bl_info)

    descriptions_ru.register()
    donates.register()
    bmesh.register()

    for cls in CLASSES:
        bpy.utils.register_class(cls)

    bpy.types.Scene.quick_tools_settings = PointerProperty(type=QuickToolsSettings)
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.prepend(draw_menu_prepend)


def unregister():
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.remove(draw_menu_prepend)
    del bpy.types.Scene.quick_tools_settings

    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)

    bmesh.unregister()
    donates.unregister()
    descriptions_ru.unregister()
    if addon_updater_ops:
        addon_updater_ops.unregister()
    if translations:
        translations.unregister()


if __name__ == "__main__":
    register()
