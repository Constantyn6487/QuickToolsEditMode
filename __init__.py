# Copyright (C) 2024 Constantyn Wasilyev (Constantyn6487)
# <Constantyn6487@gmail.com>
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
    "blender": (4, 2, 0),
    "location": "View3D > Sidebar > Item",
    "category": "Object",
    "version": (1, 8, 4),
    "author": "Constantyn Wasilyev (Constantyn6487)",
    "description": "Fast Edge Crease, Bevel Weight (3 values) and Shading, Apply Transform access in Edit Mode",
}

import bpy
import bmesh
import mathutils
from bpy.types import (Panel, Operator, AddonPreferences, PropertyGroup, Menu)
from bpy.props import (StringProperty, FloatProperty, BoolProperty, PointerProperty)
from bpy.utils import (register_class, unregister_class)

#ICON VERIFICATION FUNCTION 
def get_icon(preferred, fallback):
    icons = bpy.types.UILayout.bl_rna.functions['prop'].parameters['icon'].enum_items
    if preferred in icons: return preferred
    if fallback in icons: return fallback
    return 'NONE'

#SETTINGS STORAGE 
class QuickToolsSettings(PropertyGroup):
    affect_edges: BoolProperty(
        name="Edges",
        description="Apply weight to edges",
        default=True
    ) # type: ignore
    affect_vertices: BoolProperty(
        name="Vertices",
        description="Apply weight to vertices",
        default=False
    ) # type: ignore

#Logic of Work Weight Bevel/Crease
def apply_weight_smart(context, value, edge_attr, vert_attr):
    obj = context.edit_object
    me = obj.data
    bm = bmesh.from_edit_mesh(me)
    settings = context.scene.quick_tools_settings
    if not settings.affect_edges and not settings.affect_vertices:
        return {'CANCELLED'}
    if not any(e.select for e in bm.edges) and not any(v.select for v in bm.verts):
        return {'CANCELLED'}
    if settings.affect_edges:
        layer_e = bm.edges.layers.float.get(edge_attr) or bm.edges.layers.float.new(edge_attr)
        for e in bm.edges:
            if e.select: e[layer_e] = value           
    if settings.affect_vertices:
        layer_v = bm.verts.layers.float.get(vert_attr) or bm.verts.layers.float.new(vert_attr)
        for v in bm.verts:
            if v.select: v[layer_v] = value      
    bmesh.update_edit_mesh(me)

#OPERATORS
class BUTTON_OT_WeightSet(Operator): #Crease/Bevel
    bl_idname = "button.weight_set"
    bl_label = "Set Weight"
    bl_options = {'REGISTER', 'UNDO'}
    value: FloatProperty() # type: ignore
    mode: StringProperty() # type: ignore
    
    @classmethod
    def poll(cls, context):
        return context.object is not None and context.mode == 'EDIT_MESH'
    def execute(self, context):
        if self.mode == "CREASE":
            apply_weight_smart(context, self.value, "crease_edge", "crease_vert")
        else:
            apply_weight_smart(context, self.value, "bevel_weight_edge", "bevel_weight_vert")
        return {'FINISHED'}

class BUTTON_OT_QuickAction(Operator): #Smooth/Transform
    bl_idname = "button.quick_action"
    bl_label = "Quick Smooth Transform"
    bl_options = {'REGISTER', 'UNDO'}
    action: StringProperty() # type: ignore

    @classmethod
    def poll(cls, context):
        return context.object is not None and context.mode == 'EDIT_MESH'
    def execute(self, context):
        obj = context.edit_object
        me = obj.data

        #Auto Smooth (4.2 -> 5.0+)
        if self.action == 'AUTO_SMOOTH':
            try:
                # Пробуем быстрый метод для 4.2/4.3
                bpy.ops.mesh.shade_auto_smooth()
            except (AttributeError, RuntimeError):
                # Если оператор удален (Blender 5.0+) или выдал ошибку
                bpy.ops.object.mode_set(mode='OBJECT')
                bpy.ops.object.shade_auto_smooth()
                bpy.ops.object.mode_set(mode='EDIT')
            return {'FINISHED'}

        #Smooth/Flat/Transform
        bm = bmesh.from_edit_mesh(me)

        for f in bm.faces:
            f.select = True
        bmesh.update_edit_mesh(me)
        if self.action == 'SMOOTH':
            bpy.ops.mesh.faces_shade_smooth()
        elif self.action == 'FLAT':
            bpy.ops.mesh.faces_shade_flat()  
        elif self.action in {'SCALE', 'ROTATION'}:
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
class VIEW3D_MT_edit_mesh_QuickPanelButtons(Menu): #Context Menu
    bl_label = "QuickToolsEditMode"
    def draw(self, context):
        layout = self.layout
        
        #Crease
        op = layout.operator("button.weight_set", text="Edge Crease 0.00", icon=get_icon('EDGE_CREASE', 'MOD_SUBSURF'))
        op.value = 0.0; op.mode = "CREASE"
        op = layout.operator("button.weight_set", text="Edge Crease 0.50", icon=get_icon('EDGE_CREASE', 'MOD_SUBSURF'))
        op.value = 0.5; op.mode = "CREASE"
        op = layout.operator("button.weight_set", text="Edge Crease 1.00", icon=get_icon('EDGE_CREASE', 'MOD_SUBSURF'))
        op.value = 1.0; op.mode = "CREASE"
        
        layout.separator()
        
        #Bevel
        op = layout.operator("button.weight_set", text="Edge Bevel 0.00", icon=get_icon('EDGE_BEVEL', 'MOD_BEVEL'))
        op.value = 0.0; op.mode = "BEVEL"
        op = layout.operator("button.weight_set", text="Edge Bevel 0.50", icon=get_icon('EDGE_BEVEL', 'MOD_BEVEL'))
        op.value = 0.5; op.mode = "BEVEL"
        op = layout.operator("button.weight_set", text="Edge Bevel 1.00", icon=get_icon('EDGE_BEVEL', 'MOD_BEVEL'))
        op.value = 1.0; op.mode = "BEVEL"
        
        layout.separator()
        
        #Shade Auto Smooth
        op = layout.operator("button.quick_action", text="Shade Auto Smooth", icon='MOD_SMOOTH')
        op.action = 'AUTO_SMOOTH'
        
        layout.separator()
        
        #Shade Smooth/Flat
        op = layout.operator("button.quick_action", text="Shade Smooth", icon=get_icon('SHADING_SMOOTH', 'MESH_UVSPHERE'))
        op.action = 'SMOOTH'
        op = layout.operator("button.quick_action", text="Shade Flat", icon=get_icon('SHADING_FLAT', 'MESH_ICOSPHERE'))
        op.action = 'FLAT'

        layout.separator()
        
        #Transform
        op = layout.operator("button.quick_action", text="ApplyScale", icon=get_icon('TRANSFORM_SCALE', 'FULLSCREEN_ENTER'))
        op.action = 'SCALE'
        op = layout.operator("button.quick_action", text="ApplyRotation", icon=get_icon('ORIENTATION_GLOBAL', 'ORIENTATION_GIMBAL'))
        op.action = 'ROTATION'

def draw_menu_prepend(self, context):
    self.layout.separator()
    self.layout.menu("VIEW3D_MT_edit_mesh_QuickPanelButtons")
    self.layout.separator()

class BAR_PT_Panelis(Panel): #n-panel
    bl_idname = 'VIEW3D_PT_example_panels'
    bl_label = 'Quick Tools Edit Modes'
    bl_category = 'QuickToolsEditMode'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options = {'DEFAULT_CLOSED'}
    def draw(self, context):
        layout = self.layout
        obj = context.object
        settings = context.scene.quick_tools_settings

        if context.mode != 'EDIT_MESH':
            box = layout.box()
            box.alert = True
            box.label(text="Go to in Edit Mode!", icon='ERROR')
            return
            
        if obj is not None:
            row = layout.row()
            row.label(text="Active object is: ", icon='OBJECT_DATA')
            box = layout.box()
            box.label(text=obj.name, icon='EDITMODE_HLT')

        main_box = layout.box()
        main_box.label(text="Selection Data:", icon='OUTLINER_DATA_MESH')
        row = main_box.row(align=True)
        row.prop(settings, "affect_edges", toggle=True)
        row.prop(settings, "affect_vertices", toggle=True)

        main_box.separator()

        #Crease
        main_box.label(text="Edge Crease:", icon=get_icon('EDGE_CREASE', 'MOD_SUBSURF'))
        col = main_box.column(align=True)
        col.enabled = settings.affect_edges or settings.affect_vertices
        spl = col.split(align=True)
        op = spl.operator("button.weight_set", text="0.00"); op.value = 0.0; op.mode = "CREASE"
        op = spl.operator("button.weight_set", text="0.50"); op.value = 0.5; op.mode = "CREASE"
        op = spl.operator("button.weight_set", text="1.00"); op.value = 1.0; op.mode = "CREASE"

        main_box.separator()

        #Bevel
        main_box.label(text="Edge Bevel Weight:", icon=get_icon('EDGE_BEVEL', 'MOD_BEVEL'))
        col = main_box.column(align=True)
        col.enabled = settings.affect_edges or settings.affect_vertices
        spl = col.split(align=True)
        op = spl.operator("button.weight_set", text="0.00"); op.value = 0.0; op.mode = "BEVEL"
        op = spl.operator("button.weight_set", text="0.50"); op.value = 0.5; op.mode = "BEVEL"
        op = spl.operator("button.weight_set", text="1.00"); op.value = 1.0; op.mode = "BEVEL"

        #Smooth
        layout.label(text="Smooth Tools:", icon='MOD_SMOOTH')
        col = layout.column(align=True)
        
        # Кнопка Auto Smooth
        op = col.operator("button.quick_action", text="Shade Auto Smooth")
        op.action = 'AUTO_SMOOTH'
        
        # Ряд кнопок под ней
        row = col.row(align=True)
        op = row.operator("button.quick_action", text="Smooth"); op.action = 'SMOOTH'
        op = row.operator("button.quick_action", text="Flat"); op.action = 'FLAT'

        # Transform раздел
        layout.label(text="Transform:")
        col = layout.column(align=True)
        spl = col.split(align=True)
        op = spl.operator("button.quick_action", text="ApplyScale"); op.action = 'SCALE'
        op = spl.operator("button.quick_action", text="ApplyRotation"); op.action = 'ROTATION'

#Update Panel Category 
def update_panel(self, context):
    try:
        bpy.utils.unregister_class(BAR_PT_Panelis)
        BAR_PT_Panelis.bl_category = context.preferences.addons[__name__].preferences.category
        bpy.utils.register_class(BAR_PT_Panelis)
    except Exception as e:
        print(f"Error updating panel category: {e}")

class EditCategoryAddonUI(AddonPreferences):
    bl_idname = __name__
    category: StringProperty(
            name="Tab Category",
            default="QuickToolsEditMode",
            update=update_panel
            ) # type: ignore

    def draw(self, context):
        self.layout.prop(self, "category")

#Registration
CLASSES = [
    QuickToolsSettings, BUTTON_OT_WeightSet, BUTTON_OT_QuickAction,
    BAR_PT_Panelis, VIEW3D_MT_edit_mesh_QuickPanelButtons, EditCategoryAddonUI
]

def register():
    for cls in CLASSES: bpy.utils.register_class(cls)
    bpy.types.Scene.quick_tools_settings = PointerProperty(type=QuickToolsSettings)
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.prepend(draw_menu_prepend)

def unregister():
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.remove(draw_menu_prepend)
    for cls in reversed(CLASSES): bpy.utils.unregister_class(cls)
    del bpy.types.Scene.quick_tools_settings

if __name__ == '__main__':
    register()
