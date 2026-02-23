# ########################################################################
# Quick Tools Edit Mode
# 
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
    "blender": (4, 5, 0),
    "location": "View3D > Sidebar > Item",
    "category": "Object",
    "version": (1, 7),
    "author": "Constantyn Wasilyev (Constantyn6487)",
    "description": "Fast Edge Crease, Bevel Weight (3 values) and Shading, Apply Transform access in Edit Mode",
}


import bpy
from bpy.types import (Panel, Operator, AddonPreferences, PropertyGroup, Mesh, Menu)
from bpy.props import (StringProperty, FloatProperty)
from bpy.utils import (register_class, unregister_class)

################################################
###########ICON VERIFICATION FUNCTION###########
def get_icon(preferred, fallback):
    """Checks for the icon in the system. If not, it returns an empty string."""
#We get a list of all available icon names in the current version of Blender
    icons = bpy.types.UILayout.bl_rna.functions['prop'].parameters['icon'].enum_items
    if preferred in icons: return preferred
    if fallback in icons: return fallback
    return 'NONE'
    
################################################
############# Weight ### OPERATORS #############
class BUTTON_OT_BevelWeight0(Operator):
    ### buttom left = weith 0 ###
    bl_idname = "button.bevel_weight_0"
    bl_label = "Edge Bevel Weight 0.00"
    bl_description = "Clear the Bevel Weight 0.00"
        
    @classmethod
    def poll(self, context):
        return context.object is not None and context.mode == 'EDIT_MESH'
    
    def execute(self, context):
        bpy.ops.transform.edge_bevelweight(value=-1)
        return {'FINISHED'}

class BUTTON_OT_BevelWeight05(Operator):
    ### buttom left = weith 05 ###
    bl_idname = "button.bevel_weight_05"
    bl_label = "Edge Bevel Weight 0.50"
    bl_description = "Clear the Bevel Weight 0.50"
    
    @classmethod
    def poll(self, context):
        return context.object is not None and context.mode == 'EDIT_MESH'
    
    def execute(self, context):
        bpy.ops.transform.edge_bevelweight(value=0.5)
        return {'FINISHED'}

class BUTTON_OT_BevelWeight1(Operator):
    ### buttom right = weith 1 ###
    bl_idname = "button.bevel_weight_1"
    bl_label = "Edge Bevel Weight 1.00"
    bl_description = "Sets the Bevel Weight 1.00"
    
    @classmethod
    def poll(self, context):
        return context.object is not None and context.mode == 'EDIT_MESH'
    
    def execute(self, context):
        bpy.ops.transform.edge_bevelweight(value=1)
        return {'FINISHED'}


################################################
############# Crease ### OPERATORS #############
class BUTTON_OT_Crease0(Operator):
    ### buttom left = Crease 0 ###
    bl_idname = "button.crease_0"
    bl_label = "Edge Crease 0.00"
    bl_description = "Sets the Crease 0.00"
    
    @classmethod
    def poll(self, context):
        return context.object is not None and context.mode == 'EDIT_MESH'
    
    def execute(self, context):
        bpy.ops.transform.edge_crease(value=-1)
        return {'FINISHED'}
        
class BUTTON_OT_Crease05(Operator):
    ### buttom left = Crease 0 ###
    bl_idname = "button.crease_05"
    bl_label = "Edge Crease 0.00"
    bl_description = "Sets the Crease 0.00"
    
    @classmethod
    def poll(self, context):
        return context.object is not None and context.mode == 'EDIT_MESH'
    
    def execute(self, context):
        bpy.ops.transform.edge_crease(value=0.5)
        return {'FINISHED'}
    
class BUTTON_OT_Crease1(Operator):
    ### buttom right = Crease 1 ###
    bl_idname = "button.crease_1"
    bl_label = "Edge Crease 1.00"
    bl_description = "Sets the Crease 1.00"
    
    @classmethod
    def poll(self, context):
        return context.object is not None and context.mode == 'EDIT_MESH'
    
    def execute(self, context):
        bpy.ops.transform.edge_crease(value=1)
        return {'FINISHED'}

    
###############################################################  
############# Shade Smooth EDIT_MESH ### OPERATOR #############
class BUTTON_OT_OperationShadeSmoothEdit(Operator):
    bl_idname = "button.operation_shadesmooth_editmode"
    bl_label = "Shade Smooth"
    bl_description = "Adds Shade Smooth"
    
    @classmethod
    def poll(self, context):
        return context.object is not None and context.mode == 'EDIT_MESH'
    
    def execute(self, context):
    ### The current mode is remembered: ###
        mode = bpy.context.mode
        bpy.ops.object.mode_set(mode='OBJECT')
        if mode == 'EDIT_MESH':
            bpy.ops.object.shade_smooth()
            bpy.ops.object.mode_set(mode='EDIT')
            return {'FINISHED'}

class BUTTON_OT_OperationShadeFlatEdit(Operator):
    bl_idname = "button.operation_shadeflat_editmode"
    bl_label = "Shade Flat"
    bl_description = "Adds Shade Flat"
    
    @classmethod
    def poll(self, context):
        return context.object is not None and context.mode == 'EDIT_MESH'
    
    def execute(self, context):
    ### The current mode is remembered: ###
        mode = bpy.context.mode
        bpy.ops.object.mode_set(mode='OBJECT')
        if mode == 'EDIT_MESH':
            bpy.ops.object.shade_flat()
            bpy.ops.object.mode_set(mode='EDIT')
            return {'FINISHED'}


#######################################################################
############# Apply Scale-Rotation EDIT_MESH ### OPERATOR #############
class BUTTON_OT_OperationApplyScaleEdit(Operator):
    bl_idname = "button.operation_applyscale_editmode"
    bl_label = "Apply Scale"
    bl_description = "Apply reset Scale"
    
    @classmethod
    def poll(self, context):
        return context.object is not None and context.mode == 'EDIT_MESH'
    
    def execute(self, context):
    ### The current mode is remembered: ###
        mode = bpy.context.mode
        bpy.ops.object.mode_set(mode='OBJECT')
        if mode == 'EDIT_MESH':
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
            bpy.ops.object.mode_set(mode='EDIT')
            return {'FINISHED'}
        
class BUTTON_OT_OperationApplyRotationEdit(Operator):
    bl_idname = "button.operation_applyrotation_editmode"
    bl_label = "Apply Rotation"
    bl_description = "Apply reset Rotation"
    
    @classmethod
    def poll(self, context):
        return context.object is not None and context.mode == 'EDIT_MESH'
    
    def execute(self, context):
    ### The current mode is remembered: ###
        mode = bpy.context.mode
        bpy.ops.object.mode_set(mode='OBJECT')
        if mode == 'EDIT_MESH':
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
            bpy.ops.object.mode_set(mode='EDIT')
            return {'FINISHED'}

#####################################################Panel
            # This menu right mouse click
class VIEW3D_MT_edit_mesh_QickPanelButtons(Menu):
    bl_label = "QuickToolsEditMode"

#Method draw
    def draw(self, context):
        layout = self.layout
        layout.operator("button.crease_0", text="Edge Crease 0.00", icon=get_icon('TOOL_CREASE', 'MOD_SUBSURF'))
        layout.operator("button.crease_05", text="Edge Crease 0.50", icon=get_icon('TOOL_CREASE', 'MOD_SUBSURF'))
        layout.operator("button.crease_1", text="Edge Crease 1.00", icon=get_icon('TOOL_CREASE', 'MOD_SUBSURF'))
        layout.separator() #Разделитель
        layout.operator("button.bevel_weight_0", text="EdgeBevelWeight 0.00", icon=get_icon('TOOL_BEVEL', 'MOD_BEVEL'))
        layout.operator("button.bevel_weight_05", text="EdgeBevelWeight 0.50", icon=get_icon('TOOL_BEVEL', 'MOD_BEVEL'))
        layout.operator("button.bevel_weight_1", text="EdgeBevelWeight 1.00", icon=get_icon('TOOL_BEVEL', 'MOD_BEVEL'))
        layout.separator() #Разделитель
        layout.operator("button.operation_shadesmooth_editmode", text="Shadesmooth", icon=get_icon('SHADING_SMOOTH', 'MESH_ICOSPHERE'))
        layout.operator("button.operation_shadeflat_editmode", text="Shadeflat", icon=get_icon('SHADING_FLAT', 'MESH_UVSPHERE'))
        layout.separator() #Разделитель
        layout.operator("button.operation_applyscale_editmode", text="ApplyScale", icon=get_icon('TRANSFORM_SCALE', 'FULLSCREEN_ENTER'))
        layout.operator("button.operation_applyrotation_editmode", text="ApplyRotation", icon=get_icon('ORIENTATION_GLOBAL', 'ORIENTATION_GIMBAL'))

#This function should be SEPARATE(раздел.черта).
def draw_menu_append(self, context):
    self.layout.separator()
    self.layout.menu("VIEW3D_MT_edit_mesh_QickPanelButtons")
    self.layout.separator()

#####################################################Panel
                # This menu N-panel
class BAR_PT_Panelis(Panel):
    bl_idname = 'VIEW3D_PT_example_panels'
    bl_label = 'Quick Tools Edit Modes'
    bl_category = 'QuickToolsEditMode'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        
     ### Window, actives object ### 
        obj = context.object
        
        if context.mode != 'EDIT_MESH': #Проверка в режиме редактирования меша, если нет то:
            box = layout.box()
            box.alert = True  #Красит блок красным цветом
            box.label(text="Go to in Edit Mode!", icon='ERROR') #Иконка и текст
            return  #если не Edit, то убирает все что должно быть в режиме редактировании из панели
            
        if obj is not None:
            row = layout.row()
            row.label(text="Active object is: ", icon='OBJECT_DATA')
            box = layout.box()
            box.label(text=obj.name, icon='EDITMODE_HLT') #Показывает выделенный меш
            
    ### Button visibility in edit mode ###
        if context.object is not None and context.mode == 'EDIT_MESH':
            layout.label(text="Speed Crease:")
            col = layout.column()
            spl = col.split(align = True)
            #buttom left
            op = spl.operator("button.crease_1", text="1.00")
            #buttom midle
            op = spl.operator("button.crease_05", text="0.50")
            #buttom right
            op = spl.operator("button.crease_0", text="0.00")
            layout.label(text="Speed Edge Bevel Weight:")
            col = layout.column()
            #box = layout.box()
            spl = col.split(align = True)
            #buttom left
            op = spl.operator("button.bevel_weight_1", text="1.00")
            #buttom midle
            op = spl.operator("button.bevel_weight_05", text="0.50")
            #buttom right
            op = spl.operator("button.bevel_weight_0", text="0.00")
            col = layout.column()

    ### Button visibility in edit mode ### Bevel Subdivision ###
        if context.object is not None and context.mode == 'EDIT_MESH':
            layout.label(text="Smoothing mode:")
            col = layout.column()
            spl = col.split(align = True)
            op = spl.operator("button.operation_shadesmooth_editmode", text="ShadeSmooth")
            op = spl.operator("button.operation_shadeflat_editmode", text="ShadeFlat")	
            layout.label(text="Apply Mesh Transform:")
            col = layout.column()
            spl = col.split(align = True)
            op = spl.operator("button.operation_applyscale_editmode", text="ApplyScale")
            op = spl.operator("button.operation_applyrotation_editmode", text="ApplyRotation")		

#####################################################################
########## Update Panel Category ### in install addon panel##########
panels = (BAR_PT_Panelis,)

def update_panel(self, context):
    message = "Align Tools: Updating Panel locations has failed"
    try:
        for panel in panels:
            if "bl_rna" in panel.__dict__:
                bpy.utils.unregister_class(panel)

        for panel in panels:
            panel.bl_category = context.preferences.addons[__name__].preferences.category
            bpy.utils.register_class(panel)

    except Exception as e:
        print("\n[{}]\n{}\n\nError:\n{}".format(__name__, message, e))
        pass


class EditCategoryAddonUI(AddonPreferences):
    bl_idname = __name__

    category: StringProperty(
            name="Tab Category",
            description="Choose a name for the category of the panel",
            default="Edit",
            update=update_panel
            )

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        col = row.column()
        col.label(text="Tab Category:")
        col.prop(self, "category", text="")
        
################ END ### Category ### Update ### Panel ################
#######################################################################

CLASSES = [
    BUTTON_OT_BevelWeight0,
    BUTTON_OT_BevelWeight05,
    BUTTON_OT_BevelWeight1,
    BUTTON_OT_Crease0,
    BUTTON_OT_Crease05,
    BUTTON_OT_Crease1,
    BUTTON_OT_OperationShadeSmoothEdit,
    BUTTON_OT_OperationShadeFlatEdit,
    BUTTON_OT_OperationApplyScaleEdit,
    BUTTON_OT_OperationApplyRotationEdit,
    BAR_PT_Panelis,
    VIEW3D_MT_edit_mesh_QickPanelButtons, 
#I know there's a mistake in the word, that's the way it's supposed to be :)
]
    
    ##############################################    
    ###### registering and menu integration ######
def register():
    for cls in CLASSES:
        register_class(cls)
    ### Adding our wrapper function to the context menu ###
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.prepend(draw_menu_append)

def unregister():
    ### Removing exactly the function that was added ###
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.remove(draw_menu_append)
    for cls in reversed(CLASSES):
        unregister_class(cls)
    ###### unregistering and removing menus ######
    ##############################################

if __name__ == '__main__':
    register()