import os
import xml.etree.ElementTree as ET


class Messages:
    languages = {}
    files_path = "res/languages/"
    files_list = []
    lang = "en"

    def __init__(self):
        self.files_list = os.listdir(self.files_path)
        for file in self.files_list:
            lang_root = self.get_language_object(self.files_path + file)
            if lang_root is not None:
                lang_name = file.split(".")[0]
                self.languages[lang_name] = lang_root

    def get_string(self, path):
        class_name, var_name = path.split("/")
        string_object = self.languages[self.lang].find(
            "./" + class_name + "/string[@name='" + var_name + "']")
        if string_object is None:
            print("error: string - " + path + " not found")
            return None
        if string_object.text is None:
            string_object.text = ""
        string_text = string_object.text.replace("\\n", "\n")
        string_type = string_object.attrib.get("type")
        if string_type is not None:
            if string_type == "hex":
                string_text = bytearray.fromhex(string_text).decode()
        return string_text

    def set_language(self, lang):
        if lang in self.languages.keys():
            self.lang = lang
        else:
            print("error: no language - " + lang)

    @staticmethod
    def get_language_object(path):
        xml_root = None
        if path.split(".")[-1] == "xml":
            try:
                xml_tree = ET.parse(path, )
                xml_root = xml_tree.getroot()
            except Exception as e:
                print(e)
                pass
        if xml_root is None:
            print("Error loading file - " + path)
        return xml_root
