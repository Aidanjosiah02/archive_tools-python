#NOTE: Script to create symlinks within folders whose name is specified in a list in text file.

from pathlib import Path
import re


SELECTED_LINE = 21  # line in text file(s) that contains a list of folders to create.
ENCLOSER_LENGTH = 2 # length of the open and close characters, seperately, for the list specified above. ex: [' for open and '] for close = 2
DELIMITER = '\', \''
DIRECTORY = Path(".")
TEXT_EXTENSION = ".txt"
IMAGE_EXTENTIONS = {".png", ".jpg"}
regex_pattern = r'([^/\\]+)'
invalid_chars = r'[~"#%&*:<>?/\\{|}]+'


def names_from_txt(text_file):
    with open(text_file, 'r', encoding='utf-8-sig') as file_read:
        for index, line in enumerate(file_read):
            split_items = []
            if index == SELECTED_LINE:
                strip_line = line.strip()
                remove_enclosure = strip_line[ENCLOSER_LENGTH: len(strip_line) - ENCLOSER_LENGTH]
                replace_delimiter = remove_enclosure.replace('\"', '\'')
                split_items = re.split(DELIMITER, replace_delimiter)
                return split_items
            elif index > SELECTED_LINE:
                break

def remove_extensions(file_string):
    file_noext = None
    ext_index = file_string.find(".")
    file_noext = file_string[:ext_index]
    return file_noext

file_list = {file for file in DIRECTORY.iterdir() if file.is_file()} # [file.txt, file.json, file.png, image.txt, image.json, image.png]
for file1 in file_list:
    file1_string = str(file1)
    match1 = re.match((regex_pattern + TEXT_EXTENSION + r'$'), file1_string)
    if match1:
        try:
            file1_noext = remove_extensions(file1_string)
            name_list = names_from_txt(file1)
            for file2 in file_list:
                file2_string = str(file2)
                file2_noext = remove_extensions(file2_string)
                if file2_noext == file1_noext:
                    for item in name_list:
                        item_replaced = re.sub(invalid_chars, "-", item)
                        target_path = ("./" + item_replaced + "/")
                        target = Path("../" + file2_string)          # target of symlink
                        symlink = Path(target_path + file2_string)   # location of symlink itself
                        print(target)
                        Path(target_path).mkdir(parents=True, exist_ok=True)
                        symlink.symlink_to(target)
                else:
                    continue
        except:
            print("Error on: " + file1_string)
            with open('symlink_failures.txt', 'a') as file_write:
                file_write.write(file1_string + "\n")
    else:
        continue