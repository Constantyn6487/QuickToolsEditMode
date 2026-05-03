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
import bmesh
import mathutils
from bpy.types import Operator
from bpy.props import FloatProperty, StringProperty


# ===========================================================================
# BMESH HELPERS (версионная совместимость 3.6 – 4.2+)
# ===========================================================================

def apply_weight_smart(
    context: bpy.types.Context, value: float, edge_attr: str, vert_attr: str
) -> set[str]:
    """Умное применение веса (crease/bevel) через bmesh."""
    obj = context.edit_object
    me = obj.data
    bm = bmesh.from_edit_mesh(me)
    settings = context.scene.quick_tools_settings

    # BLENDER < 4.0 — прямое обращение к системным слоям
    if bpy.app.version < (4, 0, 0):
        if settings.affect_edges:
            if "crease" in edge_attr:
                layer_e = bm.edges.layers.crease.verify()
            else:
                layer_e = bm.edges.layers.bevel_weight.verify()

            for e in bm.edges:
                if e.select:
                    e[layer_e] = value

        if settings.affect_vertices:
            if "crease" in vert_attr:
                layer_v = bm.verts.layers.crease.verify()
            else:
                layer_v = bm.verts.layers.bevel_weight.verify()

            for v in bm.verts:
                if v.select:
                    v[layer_v] = value

        bmesh.update_edit_mesh(me)
        me.update()  # Обновление вьюпорта

    # BLENDER ≥ 4.0 — новый API слоёв
    else:
        if settings.affect_edges:
            layer_e = (
                bm.edges.layers.float.get(edge_attr)
                or bm.edges.layers.float.new(edge_attr)
            )
        if settings.affect_vertices:
            layer_v = (
                bm.verts.layers.float.get(vert_attr)
                or bm.verts.layers.float.new(vert_attr)
            )

        if settings.affect_edges:
            for e in bm.edges:
                if e.select:
                    e[layer_e] = value
        if settings.affect_vertices:
            for v in bm.verts:
                if v.select:
                    v[layer_v] = value

        bmesh.update_edit_mesh(me, loop_triangles=False, destructive=False)

    return {"FINISHED"}


def _set_auto_smooth(mesh: bpy.types.Mesh) -> None:
    """Включает Auto Smooth (совместимо с 3.6–4.2)."""
    if hasattr(mesh, "auto_smooth"):
        mesh.auto_smooth = True
    elif hasattr(mesh, "use_auto_smooth"):
        mesh.use_auto_smooth = True
    else:
        print("[QuickTools] Warning: Mesh has no auto‑smooth flag.")


def _add_builtin_shade_smooth_by_angle(obj: bpy.types.Object) -> None:
    """Добавляет модификатор 'Smooth by Angle' (Blender 4.1+)."""
    cur_mode = obj.mode
    if cur_mode != "OBJECT":
        bpy.ops.object.mode_set(mode="OBJECT")

    ver = bpy.app.version
    if ver >= (4, 2, 0):
        bpy.ops.object.shade_auto_smooth()
    elif (4, 1, 0) <= ver < (4, 2, 0):
        bpy.ops.object.shade_smooth()
        exists = any(
            m.type == 'NODES' and
            ("Smooth by Angle" in m.name or "Сглаживание" in m.name)
            for m in obj.modifiers
        )
        if not exists:
            try:
                bpy.ops.object.modifier_add_node_group(
                    asset_library_type='ESSENTIALS',
                    asset_library_identifier="",
                    relative_asset_identifier="geometry_nodes\\smooth_by_angle.blend\\NodeTree\\Smooth by Angle"
                )
            except Exception as e:
                print(f"[QuickTools] Asset path failed, using fallback: {e}")
                bpy.ops.object.shade_smooth_by_angle(angle=0.523599)

    if cur_mode != "OBJECT":
        bpy.ops.object.mode_set(mode=cur_mode)


# ===========================================================================
# OPERATORS
# ===========================================================================

class BUTTON_OT_WeightSet(Operator):
    """Установка веса (crease/bevel) для рёбер/вершин."""
    bl_idname = "button.weight_set"
    bl_label = "Set Weight"
    bl_options = {"REGISTER", "UNDO"}

    value: FloatProperty()  # type: ignore
    mode: StringProperty()  # type: ignore

    @classmethod
    def description(cls, context, properties):
        msg = "Set weight value"
        if properties.mode == "CREASE":
            if properties.value == 1.0:
                msg = "Set edge crease to 1.00"
            elif properties.value == 0.5:
                msg = "Set edge crease to 0.50"
            elif properties.value == 0.0:
                msg = "Set edge crease to 0.00"
        elif properties.mode == "BEVEL":
            if properties.value == 1.0:
                msg = "Set edge bevel weight to 1.00"
            elif properties.value == 0.5:
                msg = "Set edge bevel weight to 0.50"
            elif properties.value == 0.0:
                msg = "Set edge bevel weight to 0.00"
        return get_tooltip_text(context, msg)

    def execute(self, context):
        if self.mode == "CREASE":
            return apply_weight_smart(context, self.value, "crease_edge", "crease_vert")
        else:
            return apply_weight_smart(context, self.value, "bevel_weight_edge", "bevel_weight_vert")


class BUTTON_OT_QuickAction(Operator):
    """Быстрые действия: сглаживание, трансформации."""
    bl_idname = "button.quick_action"
    bl_label = "Quick Smooth Transform"
    bl_options = {"REGISTER", "UNDO"}

    action: StringProperty()  # type: ignore

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
        elif properties.action == 'AUTO_SMOOTH':
            msg = "Apply auto smooth shading"
        return get_tooltip_text(context, msg)

    @classmethod
    def poll(cls, context):
        return context.object is not None and context.mode == "EDIT_MESH"

    def execute(self, context: bpy.types.Context) -> set[str]:
        obj = context.edit_object
        if not obj or obj.type != "MESH":
            self.report({"WARNING"}, "Active object is not a mesh")
            return {"CANCELLED"}

        mesh = obj.data

        # AUTO_SMOOTH
        if self.action == 'AUTO_SMOOTH':
            if bpy.app.version >= (4, 1, 0):
                _add_builtin_shade_smooth_by_angle(obj)
                self.report({'INFO'}, "Smooth by Angle modifier added")
            else:
                self.report({'WARNING'}, "Auto Smooth modifier requires Blender 4.1+")
                if hasattr(mesh, "use_auto_smooth"):
                    mesh.use_auto_smooth = True
                elif hasattr(mesh, "auto_smooth"):
                    mesh.auto_smooth = True
            return {"FINISHED"}

        # SMOOTH / FLAT
        if self.action in {"SMOOTH", "FLAT"}:
            bm = bmesh.from_edit_mesh(mesh)
            for f in bm.faces:
                f.select = True
            bmesh.update_edit_mesh(mesh, loop_triangles=False, destructive=False)

            if self.action == "SMOOTH":
                bpy.ops.mesh.faces_shade_smooth()
            else:
                bpy.ops.mesh.faces_shade_flat()
            return {"FINISHED"}

        # SCALE / ROTATION
        if self.action in {"SCALE", "ROTATION"}:
            bm = bmesh.from_edit_mesh(mesh)

            if self.action == "SCALE":
                scale_mat = mathutils.Matrix.Diagonal(obj.matrix_world.to_scale()).to_4x4()
                bm.transform(scale_mat)
                obj.scale = (1.0, 1.0, 1.0)
            else:  # ROTATION
                rot_mat = obj.matrix_world.to_quaternion().to_matrix().to_4x4()
                bm.transform(rot_mat)
                obj.rotation_euler = (0.0, 0.0, 0.0)

            bmesh.update_edit_mesh(mesh, loop_triangles=False, destructive=False)
            return {"FINISHED"}

        return {"CANCELLED"}


class BUTTON_OT_EnableAutoSmooth(Operator):
    """Аналог Object > Shade Auto Smooth (через bmesh, мульти-объект)."""
    bl_idname = "button.enable_auto_smooth"
    bl_label = "Shade Auto Smooth"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def description(cls, context, properties):
        msg = "Render and display faces smooth using vertex normals"
        return get_tooltip_text(context, msg)

    def execute(self, context):
        objects = [obj for obj in context.selected_objects if obj.type == "MESH"]
        if not objects and context.active_object and context.active_object.type == "MESH":
            objects = [context.active_object]

        if not objects:
            self.report({'WARNING'}, "No mesh objects selected")
            return {"CANCELLED"}

        count = 0
        for obj in objects:
            mesh = obj.data
            changed = False

            if hasattr(mesh, "use_auto_smooth"):
                if not mesh.use_auto_smooth:
                    mesh.use_auto_smooth = True
                    changed = True
            elif hasattr(mesh, "auto_smooth"):
                if not mesh.auto_smooth:
                    mesh.auto_smooth = True
                    changed = True

            if obj.mode == "EDIT":
                bm = bmesh.from_edit_mesh(mesh)
                for f in bm.faces:
                    if not f.smooth:
                        f.smooth = True
                        changed = True
                bmesh.update_edit_mesh(mesh)
            else:
                bm = bmesh.new()
                bm.from_mesh(mesh)
                for f in bm.faces:
                    if not f.smooth:
                        f.smooth = True
                        changed = True
                bm.to_mesh(mesh)
                bm.free()

            if changed:
                count += 1
                mesh.update_tag()

        if count > 0:
            self.report({'INFO'}, f"Shade Auto Smooth applied to {count} object(s)")
        else:
            self.report({'INFO'}, "Auto Smooth already enabled")

        return {"FINISHED"}


class BUTTON_OT_OpenNPanel(Operator):
    """Открывает N-панель и переключает вкладку аддона."""
    bl_idname = "button.open_n_panel"
    bl_label = "Open N-Panel Settings"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def description(cls, context, properties):
        msg = "Open the sidebar and go to the add-ons tab to select the data"
        return get_tooltip_text(context, msg)

    def execute(self, context):
        context.area.spaces.active.show_region_ui = True
        prefs = context.preferences.addons[__package__].preferences
        target_tab = prefs.category

        for region in context.area.regions:
            if region.type == 'UI':
                try:
                    region.active_panel_category = target_tab
                except Exception:
                    try:
                        context.space_data.tabs_category = target_tab
                    except:
                        pass
                region.tag_redraw()
                break

        return {'FINISHED'}


# ===========================================================================
# TRANSLATION HELPER
# ===========================================================================

def get_tooltip_text(context: bpy.types.Context, text: str) -> str:
    """Переводит текст подсказки, если включен перевод тултипов."""
    if not context.preferences.view.use_translate_tooltips:
        return text
    return bpy.app.translations.pgettext(text)


# ===========================================================================
# REGISTRATION LIST
# ===========================================================================

CLASSES = [
    BUTTON_OT_WeightSet,
    BUTTON_OT_QuickAction,
    BUTTON_OT_EnableAutoSmooth,
    BUTTON_OT_OpenNPanel,
]


def register():
    for cls in CLASSES:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)
