import bpy
from bpy.types import AddonPreferences


class RGPKf_Preferences(AddonPreferences):
    bl_idname = "RenderGPKeyframes"

    dopesheet : bpy.props.BoolProperty(name="Add to dopesheet", default=False)
    view_menu : bpy.props.BoolProperty(name="Add to View menu", default=False)


    def draw(self, context):
        layout = self.layout

        layout.label(text="Add to UI")
        layout.prop(self,"dopesheet")
        layout.prop(self,"view_menu")
    
    def update(self,context):
        print(self.dopesheet)