#!/usr/bin/python3

"""In this module defines FileStorage class"""

import json


class FileStorage:
    """
    Impliment and manipulate storage of objects (users' data) in a file

    Attributes
    ----------
    __file_path : str (private class attribute)
        JSON file where objects (users' data) is stored
    __objects : dict (initialized empty)
        store all objects by <class name>.id (ex: to store a BaseModel
        object with id=12121212, the key will be BaseModel.12121212)

    Methods
    -------
    __classes()
        Import classes from modules in models package and return a
        dictionary of classes
    all()
        Return the dictionary '__objects'
    new(obj)
        Set in '__objects' the 'obj' with key <obj class name>.id
    save()
        Serialize '__objects' to the JSON file (path: __file_path)
    delete(obj_id)
        Delete object with id equals 'obj_id' and update
        the file __file_path.
    reload()
        Deserialize the JSON file to '__objects'
        (only if __file_path exists)
    """
    __file_path = "file.json"
    __objects = {}

    def __classes(self):
        """Import classes from modules in models package and
        return a dictionary of classes

        Returns
        -------
        dict
            A dictionary of classes (as keys) defined in each modules
            in models package
        """
        # Importing in this method is done to avoid
        # circular imports error
        from models.base_model import BaseModel
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review
        classes = {"BaseModel": BaseModel,
                   "User": User,
                   "State": State,
                   "City": City,
                   "Amenity": Amenity,
                   "Place": Place,
                   "Review": Review}
        return classes

    def all(self):
        """Return the dictionary '__objects' """
        return self.__objects

    def new(self, obj):
        """Set in '__objects' the 'obj' with key <obj class name>.id

            Paramters
            ---------
            obj : any object in models.base_model module (e.g BaseModel)
        """
        if obj is not None:
            key = f"{obj.__class__.__name__}.{obj.id}"
            self.__objects[key] = obj

    def save(self):
        """Serialize '__objects' to the JSON file (path: __file_path)"""
        # Holds new objects (data) to be serialised
        new_objs = {}
        for key, obj_name in self.__objects.items():
            new_objs[key] = obj_name.to_dict()
        try:
            #  If file exist, load its content to a variable
            with open(self.__file_path, 'r') as jf:
                json_to_py = json.load(jf)
            if type(json_to_py) is dict:
                #  Modify the loaded file content with new objects
                for key, obj_dict in new_objs.items():
                    if key not in json_to_py:
                        json_to_py[key] = obj_dict
            new_objs = json_to_py
        except Exception as e:
            pass
        finally:
            #  Modify the file with new objects (data)
            with open(self.__file_path, 'w') as jf:
                json.dump(new_objs, jf)

    def delete(self, obj_id):
        """Delete object with id equals 'obj_id' and update
        the file __file_path.

        Parameters
        ----------
        obj_id : str
            id of an object to be deleted. This id is the
            concantenation of class name, '.' and object id.
        """
        if obj_id in self.__objects:
            del self.__objects[obj_id]
        new_objs = {}
        for id_, obj in self.__objects.items():
            new_objs[id_] = obj.to_dict()
        py_to_json = json.dumps(new_objs)
        with open(self.__file_path, 'w') as f:
            f.write(py_to_json)

    def reload(self):
        """Deserialize the JSON file to '__objects'
        (only if __file_path exists)"""
        try:
            with open(self.__file_path, 'r') as f:
                deserialized_objs = json.load(f)
            for id_, obj_dict in deserialized_objs.items():
                obj_name = obj_dict["__class__"]
                self.__objects[id_] = self.__classes()[obj_name](**obj_dict)
        except Exception as e:
            pass
