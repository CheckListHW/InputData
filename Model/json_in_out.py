from Tools.recursive_extraction_of_list import recursive_extraction


class JsonInOut:
    __slots__ = 'this_class'

    def __init__(self, class_name):
        self.this_class = class_name

    def get_as_dict(self) -> dict:
        my_dict = {}
        this_class = self.this_class
        for slot in this_class.__slots__:
            if hasattr(self, slot):
                my_dict[slot] = recursive_extraction(getattr(self, slot))
        return my_dict

    def load_from_dict(self, load_dict: dict):
        for name_property in load_dict:
            if hasattr(self, name_property):
                self.__setattr__(name_property, load_dict[name_property])
