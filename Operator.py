
import bpy
import re

def render_GP_keyframes(selected_keyframes, selected_layers):
    frame_numbers = set()
    desired_render_formats = ['JPEG','PNG']

    # Init
    
    #context = bpy.context.area.type
    # for area in bpy.data.window_managers[0].windows[0].screen.areas:
    #     if area.type == "VIEW_3D":
    #         print(f'\x1b[38;2;254;211;48m This is the view 3d ')
    #bpy.data.window_managers['WinMan'].windows[0].screen.areas[4].spaces[0].region_3d.view_matrix
    # bpy.context.area.type = "VIEW_3D"

    init_render_format = bpy.context.scene.render.image_settings.file_format
    init_frame_number = bpy.context.scene.frame_current


    #   Grease Pencil Data
    pencils_data = {}
    selected_layers_list = []
    gp_layer_state = []

    for pencil in bpy.data.grease_pencils:
        pencils_data[pencil.name] = {
                                        "layer_name":[],
                                        "initial_layer_state":[],
                                        "modified_layer_state":[]
                                    }
    
        for layer in pencil.layers:
            # if render selected layers is True
            if selected_layers:
                pencils_data[pencil.name]["layer_name"].append(layer.info)

                if layer.select: 
                    pencils_data[pencil.name]["modified_layer_state"].append(False)
                    
                    if selected_keyframes:                                              # frame numbers only for selected layers and selected keyframes
                        for frame in layer.frames:
                            if frame.select:
                                frame_numbers.add(frame.frame_number)
                    else:
                        for frame in layer.frames:
                            frame_numbers.add(frame.frame_number)
                            
                else:                                                                   # if layer is not selected add it as 'hide' for modified layer state list
                    pencils_data[pencil.name]["modified_layer_state"].append(True)

                pencils_data[pencil.name]["initial_layer_state"].append(layer.hide)     # record initial state for recovery of visibility after rendering
            
            # if only render selected keyframes is True
            elif selected_keyframes:
                for frame in layer.frames:
                    if frame.select:
                        frame_numbers.add(frame.frame_number)

            else: # If no toggles selected
                for frame in layer.frames:
                    frame_numbers.add(frame.frame_number)

    frame_numbers = sorted(list(frame_numbers))


    # # Debug
    # print("\n")
    # print(f'\033[48;2;32;191;107m\033[38;2;0;0;0m{"START":-^40}\033[0m')
    
    # print(f"\033[48;2;165;94;234m\033[38;2;0;0;0m Layers: \033[m")
    # for pencil in pencils_data.items():
    #     print(f'{"":>2}{pencil[0]}')
    #     for items in pencil[1].items():
    #         print(f'{"":>6}{items[0]}: {items[1]}')

    # print(f"\033[48;2;247;183;49m\033[38;2;0;0;0m Frame Numbers: \033[m")
    # print(f'{"":>4}{frame_numbers}')

    


    #   Get File paths
    render_path = bpy.context.scene.render.filepath
    opened_file_path = bpy.data.filepath
    #   Populate Scene Name 
    scene_name = ""
    if render_path == "/tmp\\":
        #TODO: check if file has a name if it does give it to the scene_name, if it does not assign "untitled"
        scene_name = "untitled"

    # # Debug
    # print(f'\x1b[48;2;75;123;236m File Path : \x1b[0m')
    # print(render_path)
    # print(opened_file_path)


    #   Check for format
    render_format = init_render_format
    if render_format in desired_render_formats:
        pass
    else:
        bpy.context.scene.render.image_settings.file_format = 'PNG'
    # # Debug
    # print(f'\x1b[48;2;75;123;236m Format Is : \x1b[0m')
    # print(render_format)


    #   Main
    # if we have selected layers option on prepare layer visibility if we have selected layers option   #
    if selected_layers:                                                                                 # ˧
        for pencil in bpy.data.grease_pencils:                                                          # ˧
            if pencil.name in pencils_data.keys():                                                      # ˧
                for layer in pencil.layers:                                                             # ˧
                    if layer.info in pencils_data[pencil.name]["layer_name"]:                           # ˧
                        index = pencils_data[pencil.name]["layer_name"].index(layer.info)               # ˧
                        layer.hide = pencils_data[pencil.name]["modified_layer_state"][index] #<----------˩

    #   Start Rendering
    print(f'\x1b[48;2;32;191;107m\x1b[38;2;0;0;0;1m Rendering: \x1b[0m')
    
    #       adjust file name and path
    for i,frame in enumerate(frame_numbers):
        new_filepath = ""

        print(f'\x1b[48;2;32;191;107m\x1b[38;2;0;0;0;1m{"":^3}+ Rendering Frame: {frame:.>6} ')
        
        if render_path == "/tmp\\":
            new_filepath = render_path + scene_name + str(f'_{i:0>5}')
        else:
            new_filepath = render_path + str(f'_{i:0>5}')

        print(f'\x1b[0m\x1b[48;2;32;191;107m\x1b[38;2;0;0;0m{"":^5}- at : {new_filepath}')
        
        #   Move Frame
        bpy.context.scene.frame_set(frame)
        #   Assign new filepath
        bpy.context.scene.render.filepath = new_filepath
        #   Render
        bpy.ops.render.opengl(write_still=1, view_context=True)
        # bpy.ops.render.render(write_still = True, use_viewport = True)
        print(f'\x1b[0m')




    # #   Restore -Print color, context, render_path name, file format, layer visibility
    print(f'\x1b[48;2;32;191;107m\x1b[38;2;0;0;0;1m{"":^5} Render Complete \033[0m')
    bpy.context.scene.frame_set(init_frame_number)                              #  Restore initial timeline frame
    #bpy.context.area.type = context                                             #  Restore context
    bpy.context.scene.render.filepath = render_path                             #  Restore File Path       
    bpy.context.scene.render.image_settings.file_format = init_render_format    #  Restore image Format
    if selected_layers:                                                         # restore layer visibility if we have selected layers option
        for pencil in bpy.data.grease_pencils:                                                                                           # ˧     
            if pencil.name in pencils_data.keys():                                                                                       # ˧
                for layer in pencil.layers:                                                                                              # ˧   
                    if layer.info in pencils_data[pencil.name]["layer_name"]:                                                            # ˧
                        index = pencils_data[pencil.name]["layer_name"].index(layer.info)                                                # ˧
                        layer.hide = pencils_data[pencil.name]["initial_layer_state"][index]    #<-----------------------------------------˩


    # print(f'\033[48;2;32;191;107m\033[38;2;0;0;0m{"END":-^40}\033[0m')



class RenderGPKeyframes(bpy.types.Operator):
    bl_idname = "render.render_gp_keyframes"
    bl_label = "Render only Grease Pencil keyframes"



    def execute(self,context):
        sel_keyf = context.scene.selected_keyframes
        sel_layers = context.scene.selected_layers

        render_GP_keyframes(sel_keyf, sel_layers)
        return{'FINISHED'}

