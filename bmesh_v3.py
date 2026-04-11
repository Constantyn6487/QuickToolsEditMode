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
import bmesh

def apply_weight_smart(context, value, edge_attr, vert_attr):
    obj = context.edit_object
    me = obj.data
    bm = bmesh.from_edit_mesh(me)
    settings = context.scene.quick_tools_settings
    
    # Прямое обращение к системным слоям Blender 3.6
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
    me.update() # Обновление вьюпорта
    return {'FINISHED'}





