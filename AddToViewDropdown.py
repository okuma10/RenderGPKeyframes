import bpy,pathlib,sys,os


def insert_in_view_dropdown():
    # os.system('cls')
    '''
    Writes the Operator to the VIEW3D View dropdown menu every time the 'addon' is activated(registered).
    Makes sure if the Operator is added to the file, it will not be added again.
    If the Operator is not in the file(the file is in it's original form) it will save the file to
    ./backup/ if something goes wrong and the file get's corrupted.
    '''
    #n Find the file path
    filename = 'space_view3d.py'
    a = sys.executable.split("\\")[:-3]
    b = bpy.app.version_string.split()[0][:-2]
    

    View3d_filepath = "\\".join(a) + '\\scripts\\startup\\bl_ui\\' + filename

    #n Prepare for file data and it's analysis
    data = []
    line_of_interest = 'Viewport Render Keyframes'
    new_line = '        layout.operator("render.render_gp_keyframes", text="Viewport Render GP Keyframes", icon="RENDER_ANIMATION")'
    with open(View3d_filepath,'r') as file:
        for line in file.readlines():
            data.append(line)

    new_line_in_file = False    #trigger to find if the operator is already added to the file
    #n Loop through the data to find the last line of the Snap Pie Menu, so we can add our operator after it
    data_index = 0
    for line in data:
        if new_line in line:
            new_line_in_file = True
        else:
            if line_of_interest in line:
                data_index = data.index(line)
    
    data_index+=4

    #n Once we found it we split the data in to two and insert our operator between the two parts
    new_data_partA = data[:data_index+1]
    insert = new_line
    new_data_partB = data[data_index+1:]

    #n We check if our Operator is added to the dropdown menu,if it is not -add it, if it is - do nothing
    if not new_line_in_file:
        a = str(pathlib.Path(__file__).parent)
        #n Our backup
        with open(f'{a}\\backup\\{filename}','w+') as file:
            for line in data:
                file.write(line)
        #n new file string
        modified_file_string = "".join(new_data_partA) + insert + "".join(new_data_partB)
        #n push new file string to View3d file(deleting the old and adding the new)
        with open(View3d_filepath,'w') as file:
            file.write(modified_file_string)
    else:
        pass



def remove_from_view_dropdown():
    '''
    Removes our Operator from the Snap Pie Menu once our 'addon' was removed
    '''
    filename = 'space_view3d.py'
    a = sys.executable.split("\\")[:-3]
    b = bpy.app.version_string.split()[0][:-2]
    View3d_filepath = "\\".join(a) + '\\scripts\\startup\\bl_ui\\' + filename

    data = []
    line_of_interest = 'layout.operator("render.render_gp_keyframes", text="Viewport Render GP Keyframes", icon="RENDER_ANIMATION")'
    with open(View3d_filepath, 'r') as file:
        for line in file.readlines():
            if line_of_interest in line:
                data.append("\n")
            else:
                data.append(line)

    with open(View3d_filepath,"w+") as file:
        file.write("".join(data))


