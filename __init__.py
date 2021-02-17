bl_info = {
    "name": "Viewport Render GP keyframes",
    "description": "Vieport rendering of all GP keyframes",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "support": "COMMUNITY",
    "category": "Animation"
}
import bpy

from .AddToViewDropdown import insert_in_view_dropdown,remove_from_view_dropdown
from .AddToDopeSheet import add_to_dopesheet,remove_from_dopesheet
from . import Operator,Preferences



def register():
    #Register classes and variables    
    context=bpy.context
    bpy.utils.register_class(Operator.RenderGPKeyframes)
    bpy.utils.register_class(Preferences.RGPKf_Preferences)
    bpy.types.Scene.selected_keyframes = bpy.props.BoolProperty(name="Render Selected Keyframes"   , default=False)
    bpy.types.Scene.selected_layers    = bpy.props.BoolProperty(name="Render Selected Layers"      , default=False)

    # Insert to dopesheet and view python files. Backups are in ./backup folder
    insert_in_view_dropdown()
    add_to_dopesheet()

    pass



def unregister():
    # If dopesheet or view_menu is ticked, do not remove. Otherwise remove
    if not bpy.context.preferences.addons['RenderGPKeyframes'].preferences.dopesheet:
        remove_from_dopesheet()
    if not bpy.context.preferences.addons['RenderGPKeyframes'].preferences.view_menu:
        remove_from_view_dropdown()

    # Unregister operator and addon preferences
    bpy.utils.unregister_class(Operator.RenderGPKeyframes)
    bpy.utils.unregister_class(Preferences.RGPKf_Preferences)
    print(f'{"":!<6}\033[1;40;92m"Operator Viewport Render GP Keyframes removed"\033[0m{"":!>6}')
    pass