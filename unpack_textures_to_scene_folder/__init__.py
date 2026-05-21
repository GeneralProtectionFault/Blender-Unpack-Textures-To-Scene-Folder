import bpy
import os
from pathlib import Path

bl_info = {
    "name": "Unpack Textures to Scene Folder",
    "blender": (4, 0, 0),
    "version": (1, 0, 0),
    "category": "Import-Export",
    "description": "Unpacks all textures to a folder named after the scene file",
    "author": "Your Name",
}


def show_warning_popup(title, message):
    """Display a warning popup dialog."""
    def draw(self, context):
        self.layout.label(text=message)
    
    bpy.context.window_manager.popup_menu(draw, title=title, icon='WARNING')


def unpack_textures_to_scene_folder():
    """
    Unpacks all textures to a folder named after the scene file (with _textures appended).
    Makes all texture paths relative.
    """
    # Check if file has been saved
    if not bpy.data.filepath:
        show_warning_popup(
            "File Not Saved",
            "Please save the blend file before unpacking textures."
        )
        return False
    
    # Get the blend file path and name
    blend_filepath = bpy.data.filepath
    blend_dir = os.path.dirname(blend_filepath)
    blend_name = os.path.splitext(os.path.basename(blend_filepath))[0]
    
    # Create textures folder name
    textures_folder_name = f"{blend_name}_textures"
    textures_folder_path = os.path.join(blend_dir, textures_folder_name)
    
    # Create the textures folder if it doesn't exist
    os.makedirs(textures_folder_path, exist_ok=True)
    
    # Unpack all image textures
    for image in bpy.data.images:
        if image.filepath:
            # Skip already packed images or special sources
            if image.source != 'FILE':
                continue
            
            # Get the image filename
            image_filename = os.path.basename(image.filepath)
            if not image_filename:
                image_filename = image.name
            
            # Set the new filepath to the textures folder
            new_filepath = os.path.join(textures_folder_path, image_filename)
            
            # Save the image if it's packed
            if image.packed_file:
                image.filepath = new_filepath
                image.save()
            else:
                # For already linked images, just copy them to the textures folder
                old_filepath = bpy.path.abspath(image.filepath)
                if os.path.exists(old_filepath):
                    import shutil
                    try:
                        shutil.copy2(old_filepath, new_filepath)
                        image.filepath = new_filepath
                    except Exception as e:
                        print(f"Warning: Could not copy {old_filepath}: {e}")
    
    # Make all image paths relative to the blend file
    for image in bpy.data.images:
        if image.filepath and image.source == 'FILE':
            abs_path = bpy.path.abspath(image.filepath)
            # Make relative path
            try:
                rel_path = os.path.relpath(abs_path, blend_dir)
                image.filepath = rel_path
            except ValueError:
                # Paths on different drives on Windows
                pass
    
    return True


class UNPACK_OT_textures_to_scene_folder(bpy.types.Operator):
    """Unpack all textures to a scene-named folder and make paths relative"""
    bl_idname = "unpack.textures_to_scene_folder"
    bl_label = "Unpack Textures to Scene Folder"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        try:
            success = unpack_textures_to_scene_folder()
            if success:
                self.report({'INFO'}, "Textures unpacked successfully")
                return {'FINISHED'}
            else:
                return {'CANCELLED'}
        except Exception as e:
            self.report({'ERROR'}, f"Error unpacking textures: {str(e)}")
            return {'CANCELLED'}


def menu_func(self, context):
    """Add the operator to the External Data submenu."""
    self.layout.operator(
        UNPACK_OT_textures_to_scene_folder.bl_idname,
        text="Unpack Textures to Scene Folder"
    )


def register():
    """Register the operator and menu."""
    bpy.utils.register_class(UNPACK_OT_textures_to_scene_folder)
    bpy.types.TOPBAR_MT_file_external_data.append(menu_func)


def unregister():
    """Unregister the operator and menu."""
    bpy.types.TOPBAR_MT_file_external_data.remove(menu_func)
    bpy.utils.unregister_class(UNPACK_OT_textures_to_scene_folder)


if __name__ == "__main__":
    register()
