from Tools.recursive_extraction_of_list import recursive_extraction


class JsonInOut:
    def get_as_dict(self) -> dict:
        my_dict = {}
        this_class = self.__class__
        for slot in this_class.__slots__:
            if hasattr(self, slot):
                my_dict[slot] = recursive_extraction(getattr(self, slot))
        return my_dict

    def load_from_dict(self, load_dict: dict):
        for name_property in load_dict:
            if hasattr(self, name_property):
                if hasattr(getattr(self, name_property), 'load_from_dict'):
                    getattr(self, name_property).load_from_dict(load_dict[name_property])
                else:
                    self.__setattr__(name_property, load_dict[name_property])
