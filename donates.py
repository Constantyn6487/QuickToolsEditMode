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

class WM_OT_OpenDonateLink(bpy.types.Operator):
    bl_idname = "wm.open_donate_link"
    bl_label = "Support the project"
    bl_description = "Opens the Boosty donation page in the browser."
    
    # Сюда вставьте вашу ссылку (Boosty/DonationAlerts)
    url: bpy.props.StringProperty(default="https://boosty.to/constantiniy6487/single-payment/donation/791948/target?share=target_link") # type: ignore vscode

    def execute(self, context):
        bpy.ops.wm.url_open(url=self.url)
        # Translation for report info is usually not critical, but can be added if needed
        self.report({'INFO'}, "Launching the Boosty donation page in browser.")
        return {'FINISHED'}
    
    @classmethod
    def description(cls, context, properties):
        msg = "Opens the Boosty donation page in the browser."
        # ПРОВЕРКА: Если галочка Tooltips выключена, возвращаем английский текст
        if not context.preferences.view.use_translate_tooltips:
            return msg
        
        return bpy.app.translations.pgettext(msg)

def register():
    bpy.utils.register_class(WM_OT_OpenDonateLink)

def unregister():
    bpy.utils.unregister_class(WM_OT_OpenDonateLink)
