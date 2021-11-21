import os
import shutil

voice_folder = "C:\Waterloo\\1A\SEnsory\SEnsory\oop\inner\\"


def del_file(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(voice_folder, filename)
        print(file_path)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except:
            print("Failed to delete audio files")
