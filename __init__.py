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
    "location": "View3D > Sidebar > QuickTools",
    "category": "Mesh",
    "version": (2, 0, 0),
    "author": "Constantyn Wasilyev (Constantyn6487)",
    "description": "Fast Edge Crease, Bevel Weight (3 values) and Shading, Apply Transform access in Edit Mode",
}

import bpy
import bmesh
import mathutils
from bpy.types import (Panel, Operator, AddonPreferences, PropertyGroup, Menu)
from bpy.props import (StringProperty, FloatProperty, BoolProperty, IntProperty, PointerProperty)
from bpy.utils import (register_class, unregister_class)
from . import donates

# Попытка импорта внешних модулей
try:
    from . import translations
    from . import addon_updater_ops
except ImportError:
    translations = None
    addon_updater_ops = None

from . import descriptions_ru

#HELPER FUNCTION FOR TRANSLATION BASED ON TOOLTIPS SETTING
def get_ui_text(context, text):
    """
    Returns English text if 'use_translate_tooltips' is OFF.
    Returns Translated text (Russian) if 'use_translate_tooltips' is ON.
    """
    if not context.preferences.view.use_translate_interface:
        return text
    # Uses the registered translation dictionary (context "*")
    return bpy.app.translations.pgettext(text)

#UPDATE ADDON UI MENU
def update_panel(self, context):
    try:
        unregister_class(BAR_PT_Panelis)
        BAR_PT_Panelis.bl_category = self.category
        register_class(BAR_PT_Panelis)
    except Exception as e:
        print(f"Error updating panel category: {e}")

#ICON VERIFICATION FUNCTION
def get_icon(preferred, fallback):
    icons = bpy.types.UILayout.bl_rna.functions['prop'].parameters['icon'].enum_items
    return preferred if preferred in icons else fallback

#UPDATE ADDON PREFERENCES MENU
@addon_updater_ops.make_annotations if addon_updater_ops else lambda x: x
class QuickToolsEditModePreferences(AddonPreferences):
    bl_idname = __package__

    category: StringProperty(
        name="Tab Category",
        default="QuickToolsEditMode",
        update=update_panel
    ) # type: ignore vscode

    auto_check_update: BoolProperty(name="Auto-check", default=False, description= "Enable automatic update verification") # type: ignore vscode
    updater_interval_months: IntProperty(name="Months", default=0, description="Months") # type: ignore vscode
    updater_interval_days: IntProperty(name="Days", default=7, description="Days") # type: ignore vscode
    updater_interval_hours: IntProperty(name="Hours", default=0, description="Hours") # type: ignore vscode
    updater_interval_minutes: IntProperty(name="Minutes", default=0, description="Minutes") # type: ignore vscode

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "category")
        box = layout.box()
        row = box.row(align=True)
        row.label(text="Support the project", icon='FUND')
        #donates.py
        row.operator("wm.open_donate_link", icon='HEART', text=get_ui_text(context, "Support project on Boosty"))
        layout.separator()
        if addon_updater_ops:
            addon_updater_ops.update_settings_ui(self, context)

#SETTINGS STORAGE
class QuickToolsSettings(PropertyGroup):
    affect_edges: BoolProperty(name="Edges", default=True, description= "Enable data for selected edges") # type: ignore vscode
    affect_vertices: BoolProperty(name="Vertices", default=False, description= "Enable data for selected vertices") # type: ignore vscode

def apply_weight_smart(context, value, edge_attr, vert_attr):
    obj = context.edit_object
    me = obj.data
    bm = bmesh.from_edit_mesh(me)
    settings = context.scene.quick_tools_settings
    
    if settings.affect_edges:
        layer_e = bm.edges.layers.float.get(edge_attr) or bm.edges.layers.float.new(edge_attr)

    if settings.affect_vertices:
        layer_v = bm.verts.layers.float.get(vert_attr) or bm.verts.layers.float.new(vert_attr)

    if settings.affect_edges:
        for e in bm.edges:
            if e.select:
                e[layer_e] = value

    if settings.affect_vertices:
        for v in bm.verts:
            if v.select:
                v[layer_v] = value
    
    bmesh.update_edit_mesh(me)
    return {'FINISHED'}

# ------------------------------------------------------------
#  Compatibility layer – выбираем реализацию apply_weight_smart
# ------------------------------------------------------------
import bpy
# Если запущен Blender < 4.0, подменяем функцию реализацией
# из `bmesh_v3.py`, где использованы API‑слои, совместимые с 3.6.
if bpy.app.version < (4, 0, 0):
    # pylint: disable=unused-import
    from .bmesh_v3 import apply_weight_smart as apply_weight_smart  # type: ignore
# ------------------------------------------------------------

#OPERATORS
class BUTTON_OT_WeightSet(Operator):
    bl_idname = "button.weight_set"
    bl_label = "Set Weight"
    bl_options = {'REGISTER', 'UNDO'}
    value: FloatProperty() # type: ignore vscode
    mode: StringProperty() # type: ignore vscode

    @classmethod
    def description(cls, context, properties):
        msg = "Set weight value"
        if properties.mode == "CREASE":
            if properties.value == 1.0: msg = "Set edge crease to 1.00"
            elif properties.value == 0.5: msg = "Set edge crease to 0.50"
            elif properties.value == 0.0: msg = "Set edge crease to 0.00"
        elif properties.mode == "BEVEL":
            if properties.value == 1.0: msg = "Set edge bevel weight to 1.00"
            elif properties.value == 0.5: msg = "Set edge bevel weight to 0.50"
            elif properties.value == 0.0: msg = "Set edge bevel weight to 0.00"
        if not context.preferences.view.use_translate_tooltips:
            return msg
        return bpy.app.translations.pgettext(msg)

    def execute(self, context):
        if self.mode == "CREASE":
            return apply_weight_smart(context, self.value, "crease_edge", "crease_vert")
        else:
            return apply_weight_smart(context, self.value, "bevel_weight_edge", "bevel_weight_vert")

class BUTTON_OT_QuickAction(Operator):
    bl_idname = "button.quick_action"
    bl_label = "Quick Action"
    bl_options = {'REGISTER', 'UNDO'}
    action: StringProperty() # type: ignore vscode

    @classmethod
    def description(cls, context, properties):
        msg = "Perform quick action"
        if properties.action == 'SMOOTH':
            msg = "Apply smooth shading to selected faces"
        elif properties.action == 'FLAT':
            msg = "Apply flat shading to selected faces"
        elif properties.action == 'SCALE':
            msg = "Apply scale transformation"
        elif properties.action == 'ROTATION':
            msg = "Apply rotation transformation"
        if not context.preferences.view.use_translate_tooltips:
            return msg
        return bpy.app.translations.pgettext(msg)

    def execute(self, context):
        obj = context.edit_object
        me = obj.data
        if self.action in {'SMOOTH', 'FLAT'}:
            bm = bmesh.from_edit_mesh(me)
            for f in bm.faces: f.select = True
            bmesh.update_edit_mesh(me)
            bpy.ops.mesh.faces_shade_smooth() if self.action == 'SMOOTH' else bpy.ops.mesh.faces_shade_flat()
          
        elif self.action in {'SCALE', 'ROTATION'}:
            bm = bmesh.from_edit_mesh(me)
            if self.action == 'SCALE': 
                scale_matrix = mathutils.Matrix.Diagonal(obj.matrix_world.to_scale()).to_4x4()
                bm.transform(scale_matrix)
                obj.scale = (1.0, 1.0, 1.0)
            elif self.action == 'ROTATION':
                rotation_matrix = obj.matrix_world.to_quaternion().to_matrix().to_4x4()
                bm.transform(rotation_matrix)
                obj.rotation_euler = (0.0, 0.0, 0.0)
            bmesh.update_edit_mesh(me)
        return {'FINISHED'}

#UI ELEMENTS
#Context menu (r-click)
class VIEW3D_MT_edit_mesh_QuickPanelButtons(Menu):
    bl_label = "QuickToolsEditMode"
    def draw(self, context):
        layout = self.layout
        # Crease
        for v in [0.0, 0.5, 1.0]:
            # Using get_ui_text for button labels
            op = layout.operator("button.weight_set", text=get_ui_text(context, f"Edge Crease {v:.2f}"), icon=get_icon('EDGE_CREASE', 'MOD_SUBSURF'))
            op.value = v; op.mode = "CREASE"
        layout.separator()
        # Bevel
        for v in [0.0, 0.5, 1.0]:
            op = layout.operator("button.weight_set", text=get_ui_text(context, f"Edge Bevel {v:.2f}"), icon=get_icon('EDGE_BEVEL', 'MOD_BEVEL'))
            op.value = v; op.mode = "BEVEL"
        layout.separator()
        # Actions
        layout.operator("button.quick_action", text=get_ui_text(context, "Shadesmooth"), icon=get_icon('SHADING_SMOOTH', 'MESH_UVSPHERE')).action = 'SMOOTH'
        layout.operator("button.quick_action", text=get_ui_text(context, "Shadeflat"), icon=get_icon('SHADING_FLAT', 'MESH_ICOSPHERE')).action = 'FLAT'
        layout.separator()
        layout.operator("button.quick_action", text=get_ui_text(context, "ApplyScale"), icon=get_icon('TRANSFORM_SCALE', 'FULLSCREEN_ENTER')).action = 'SCALE'
        layout.operator("button.quick_action", text=get_ui_text(context, "ApplyRotation"), icon=get_icon('ORIENTATION_GLOBAL', 'ORIENTATION_GIMBAL')).action = 'ROTATION'

class BAR_PT_Panelis(Panel):
    bl_idname = 'VIEW3D_PT_example_panels'
    bl_label = 'Quick Tools Edit Modes'
    bl_category = 'QuickToolsEditMode'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options = {'DEFAULT_CLOSED'}

    def draw_header(self, context):
        self.layout.label(text=get_ui_text(context, "Quick Tools Edit Modes"))

    def draw(self, context):
        layout = self.layout
        obj = context.object
        settings = context.scene.quick_tools_settings

        #Check edit - outliner text
        if context.mode != 'EDIT_MESH':
            box = layout.box()
            box.alert = True
            box.label(text=get_ui_text(context, "Go to in Edit Mode!"), icon='ERROR')
            return
            
        if obj is not None:
            row = layout.row()
            row.label(text=get_ui_text(context, "Active object is: "), icon='OBJECT_DATA')
            box = layout.box()
            box.label(text=obj.name, icon='EDITMODE_HLT')

        main_box = layout.box()
        main_box.label(text=get_ui_text(context, "Selection Data:"), icon='OUTLINER_DATA_MESH')
        row = main_box.row(align=True)
        # Override property text to use our translation logic
        row.prop(settings, "affect_edges", toggle=True, text=get_ui_text(context, "Edges"))
        row.prop(settings, "affect_vertices", toggle=True, text=get_ui_text(context, "Vertices"))

        main_box.separator()

        #Crease
        main_box.label(text=get_ui_text(context, "Edge Crease:"), icon=get_icon('EDGE_CREASE', 'MOD_SUBSURF'))
        col = main_box.column(align=True)
        col.enabled = settings.affect_edges or settings.affect_vertices
        spl = col.split(align=True)
        op = spl.operator("button.weight_set", text="1.00"); op.value = 1.0; op.mode = "CREASE"
        op = spl.operator("button.weight_set", text="0.50"); op.value = 0.5; op.mode = "CREASE"
        op = spl.operator("button.weight_set", text="0.00"); op.value = 0.0; op.mode = "CREASE"

        main_box.separator()

        #Bevel
        main_box.label(text=get_ui_text(context, "Edge Bevel Weight:"), icon=get_icon('EDGE_BEVEL', 'MOD_BEVEL'))
        col = main_box.column(align=True)
        col.enabled = settings.affect_edges or settings.affect_vertices
        spl = col.split(align=True)
        op = spl.operator("button.weight_set", text="1.00"); op.value = 1.0; op.mode = "BEVEL"
        op = spl.operator("button.weight_set", text="0.50"); op.value = 0.5; op.mode = "BEVEL"
        op = spl.operator("button.weight_set", text="0.00"); op.value = 0.0; op.mode = "BEVEL"

        #Smooth
        layout.label(text=get_ui_text(context, "Smooth:"))
        col = layout.column()
        spl = col.split(align=True)
        spl.operator("button.quick_action", text=get_ui_text(context, "ShadeSmooth")).action = 'SMOOTH'
        spl.operator("button.quick_action", text=get_ui_text(context, "ShadeFlat")).action = 'FLAT'
        
        #Transform
        layout.label(text=get_ui_text(context, "Transform:"))
        col = layout.column()
        spl = col.split(align=True)
        spl.operator("button.quick_action", text=get_ui_text(context, "ApplyScale")).action = 'SCALE'
        spl.operator("button.quick_action", text=get_ui_text(context, "ApplyRotation")).action = 'ROTATION'

        if addon_updater_ops:
            addon_updater_ops.update_notice_box_ui(self, context)
        
        #Version
        layout.separator()
        row = layout.row()
        row.alignment = 'RIGHT'
        row.enabled = False
        version_str = ".".join(map(str, bl_info["version"]))
        row.label(text=f"v{version_str}")

def draw_menu_prepend(self, context):
    self.layout.separator()
    self.layout.menu("VIEW3D_MT_edit_mesh_QuickPanelButtons")
    self.layout.separator()

# --- 6. REGISTRATION ---

CLASSES = [
    QuickToolsEditModePreferences,
    QuickToolsSettings,
    BUTTON_OT_WeightSet,
    BUTTON_OT_QuickAction,
    BAR_PT_Panelis,
    VIEW3D_MT_edit_mesh_QuickPanelButtons,
]

def register():
    if translations: translations.register()
    if addon_updater_ops: addon_updater_ops.register(bl_info)
    descriptions_ru.register()
    donates.register()
    for cls in CLASSES:
        register_class(cls)
    bpy.types.Scene.quick_tools_settings = PointerProperty(type=QuickToolsSettings)
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.prepend(draw_menu_prepend)
    
    pref = bpy.context.preferences.addons[__package__].preferences
    BAR_PT_Panelis.bl_category = pref.category

def unregister():
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.remove(draw_menu_prepend)
    del bpy.types.Scene.quick_tools_settings
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)
    donates.unregister()
    descriptions_ru.unregister()
    if addon_updater_ops: addon_updater_ops.unregister()
    if translations: translations.unregister()

if __name__ == '__main__':
    register()
