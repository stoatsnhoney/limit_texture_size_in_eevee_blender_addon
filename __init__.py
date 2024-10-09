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

import bpy


class OBJECT_OT_limit_texture_size(bpy.types.Operator):
    """Limit the texture size in the viewport"""
    bl_idname = "object.limit_texture_size"
    bl_label = "Limit Texture Size"
    bl_options = {'REGISTER', 'UNDO'}

    sizes = [
        ('CLAMP_OFF', 'Off', 'No limit'),
        ('CLAMP_128', '128', '128 px'),
        ('CLAMP_256', '256', '256 px'),
        ('CLAMP_512', '512', '512 px'),
        ('CLAMP_1024', '1024', '1024 px'),
        ('CLAMP_2048', '2048', '2048 px'),
        ('CLAMP_4096', '4096', '4096 px'),
        ('CLAMP_8192', '8192', '8192 px')
    ]

    size: bpy.props.EnumProperty(
        name="Texture Limit",
        description="Limit the texture size in the viewport",
        items=sizes,
        default='CLAMP_OFF',
        update=lambda self, context: self.update_texture_limit(context)
    )

    def update_texture_limit(self, context):
        context.preferences.system.gl_texture_limit = self.size
        context.area.tag_redraw()
        self.report({'INFO'}, f"Texture size limited to {self.size.replace('CLAMP_', '')} px" if self.size != 'CLAMP_OFF' else "Texture size limit turned off")

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)


class RENDER_PT_limit_texture_size(bpy.types.Panel):
    """Creates a subpanel in the Simplify panel in Render Properties"""
    bl_label = "Texture Limit"
    bl_idname = "RENDER_PT_limit_texture_size"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"  # This is the Render Properties tab
    bl_parent_id = "RENDER_PT_simplify"  # Parent to Simplify panel

    def draw(self, context):
        layout = self.layout
        render_settings = context.scene.render

        # Check if Simplify is enabled
        if not render_settings.use_simplify:
            # Set texture limit to 'Off' if Simplify is disabled
            context.preferences.system.gl_texture_limit = 'CLAMP_OFF'
        
        # Add the texture limit dropdown
        row = layout.row()
        row.prop(context.preferences.system, "gl_texture_limit", text="Texture Limit")
        row.enabled = render_settings.use_simplify  # Enable only if Simplify is on


def register():
    bpy.utils.register_class(OBJECT_OT_limit_texture_size)
    bpy.utils.register_class(RENDER_PT_limit_texture_size)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_limit_texture_size)
    bpy.utils.unregister_class(RENDER_PT_limit_texture_size)


if __name__ == "__main__":
    register()
