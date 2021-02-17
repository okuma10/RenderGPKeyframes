import bpy,pathlib,sys,os


def add_to_dopesheet():
    # Find File
    filename = "space_dopesheet.py"
    a = sys.executable.split("\\")[:-3]
    filepath = "\\".join(a) + '\\scripts\\startup\\bl_ui\\' + filename

    # Prepare seartch,indices,tab distance,
    search_line = 'row.operator("gpencil.layer_isolate", icon=\'LOCKED\', text="").affect_visibility = False'
    data = None
    insert_line_idx=None
    tab_distance = 0
    already_in_file_search = "# Render GP Keyframes Sart section"
    already_in_file = False

    with open(filepath,"r") as file:
        data = file.readlines()

        for line in data:
            if already_in_file_search in line:                  # Check if my additon is already in the file
                already_in_file = True
                print(f'\x1b[38;2;235;59;90m * Render GP keyframes already added to Dopesheet\n\t-Pass ')
            if search_line in line and not already_in_file:     #only procede if my addition is not in the file
                line_idx = data.index(line)
                insert_line_idx = line_idx + 1

                for char in line:
                    if char == " ":
                        tab_distance += 1
                    else: break

    if not already_in_file:                                     # Continue only if there is no addition from me
        empty_line = ["\n"]
        before_part = data[:insert_line_idx] + empty_line       # Modify before and after with new lines
        after_part  = empty_line + data[insert_line_idx:]       #   .

        a = str(pathlib.Path(__file__).parent)                 # Create backup of the original file
        #n Our backup
        with open(f'{a}\\backup\\{filename}', 'w+') as file:
            for line in data:
                file.write(line)

        # Lines to be insterted in to the file
        new_part = [f'{"":>{tab_distance-4}}# Render GP Keyframes Sart section\n',
                    f'{"":>{tab_distance-4}}layout.separator_spacer()\n\n',
                    f'{"":>{tab_distance-4}}if st.mode == \'GPENCIL\':\n',
                    f'{"":>{tab_distance}}row = layout.row(align=True)\n',
                    f'{"":>{tab_distance}}row.enabled = enable_but\n',
                    f'{"":>{tab_distance}}row.prop(context.scene, "selected_layers", icon=\'RENDERLAYERS\', text="", toggle=1)\n',
                    f'{"":>{tab_distance}}row.prop(context.scene, "selected_keyframes", icon=\'DECORATE_KEYFRAME\', text="", toggle=1)\n',
                    f'{"":>{tab_distance}}row.operator("render.render_gp_keyframes", icon=\'RENDER_ANIMATION\', text="Render")\n',
                    f'{"":>{tab_distance-4}}# Render GP Keyframes End Section'
                    ]

        # Inserting the new lines
        new_data = before_part + new_part + after_part

        # Writing the new data to the file
        with open(filepath,"w") as file:
            for line in new_data:
                file.write(line)

        print(f'\x1b[48;2;32;191;107m\x1b[38;2;0;0;0m * Render GP keyframes added to UI file. * \x1b[0m')



def remove_from_dopesheet():
    # Find File
    filename = "space_dopesheet.py"
    a = sys.executable.split("\\")[:-3]
    filepath = "\\".join(a) + '\\scripts\\startup\\bl_ui\\' + filename
    # Prepare Data
    data = None

    # Get date from file
    with open(filepath,'r')as file:
        data = file.readlines()

    # Prepare search and inicies
    start_line = "# Render GP Keyframes Sart section"
    end_line = "# Render GP Keyframes End Section"
    start_index = None
    end_index = None

    is_in_file = False

    # Check if my addition is in the file
    for line in data:
        if start_line in line:
            is_in_file = True
            start_index =data.index(line)
        if end_line in line:
            end_index = data.index(line)

    # If my addition is in the file, procede with removal , else pass
    if is_in_file:
        before_element = data[:start_index]
        after_element  = data[end_index+1:]

        del after_element[:1]   # Remove the new line I added for code clarity

        # Combine edited file
        new_data = before_element + after_element

        # Write the file
        with open(filepath,'w')as file:
            for line in new_data:
                file.write(line)
        # Notify about end of procedure
        print(f'\x1b[48;2;32;191;107m\x1b[38;2;0;0;0m * Render GP keyframes removed from UI file. * \x1b[0m')
    else:
        print(f'\x1b[38;2;235;59;90m Render GP keyframes not in file\n\t - Pass')

# add_to_dopesheet()
# remove_from_dopesheet()


# filename = "space_dopesheet.py"
# a = sys.executable.split("\\")[:-3]
# filepath = "\\".join(a) + '\\scripts\\startup\\bl_ui\\' + filename

# print(View3d_filepath)

# with open(View3d_filepath,'r')as file:
#     data = file.readlines()

#     for line in data:
#         if search_line in line:
#             print('found line and file')
#             print(line)















