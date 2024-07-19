# BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# END GPL LICENSE BLOCK #####

bl_info = {
    "name": "Limit Texture Size Menu",
    "author": "Jay Friesen",
    "version": (1, 0),
    "blender": (4, 2, 0),
    "location": "View3D > Textures",
    "description": "Adds a menu in the 3D view header to limit the viewport texture size.",
    "category": "Render",
}

import bpy


class OBJECT_OT_limit_texture_size(bpy.types.Operator):
    """Limit the texture size in the viewport"""
    bl_idname = "object.limit_texture_size"
    bl_label = "Limit Texture Size"
    bl_options = {'REGISTER', 'UNDO'}

    sizes = [
        ('CLAMP_OFF', 'Off', 'No limit'),
        ('CLAMP_128', '128 px', '128 px'),
        ('CLAMP_256', '256 px', '256 px'),
        ('CLAMP_512', '512 px', '512 px'),
        ('CLAMP_1024', '1024 px', '1024 px'),
        ('CLAMP_2048', '2048 px', '2048 px'),
        ('CLAMP_4096', '4096 px', '4096 px'),
        ('CLAMP_8192', '8192 px', '8192 px')
    ]

    size: bpy.props.EnumProperty(
        name="Texture Size Limit",
        description="Limit the texture size in the viewport",
        items=sizes,
        default='CLAMP_OFF'
    )

    def execute(self, context):
        context.preferences.system.gl_texture_limit = self.size
        self.report({'INFO'}, f"Texture size limited to {self.size.replace('CLAMP_', '')} px" if self.size != 'CLAMP_OFF' else "Texture size limit turned off")
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)


class VIEW3D_MT_limit_menu(bpy.types.Menu):
    bl_label = "Textures"
    bl_idname = "VIEW3D_MT_limit_menu"

    def draw(self, context):
        layout = self.layout
        layout.operator(OBJECT_OT_limit_texture_size.bl_idname)


def draw_item(self, context):
    layout = self.layout
    layout.menu(VIEW3D_MT_limit_menu.bl_idname)


def register():
    bpy.utils.register_class(OBJECT_OT_limit_texture_size)
    bpy.utils.register_class(VIEW3D_MT_limit_menu)

    bpy.types.VIEW3D_MT_editor_menus.append(draw_item)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_limit_texture_size)
    bpy.utils.unregister_class(VIEW3D_MT_limit_menu)

    bpy.types.VIEW3D_MT_editor_menus.remove(draw_item)


if __name__ == "__main__":
    register()
