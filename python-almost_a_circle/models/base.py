#!/usr/bin/python3
"""Module containing the Base class"""

import json
import turtle
import csv


class Base:
    """A base class"""
    __nb_objects = 0

    def __init__(self, id=None):
        """Initialize a new Base instance
        Args:
            id (int): The identity of the new Base instance.
        """
        if id is not None:
            self.id = id
        else:
            Base.__nb_objects += 1
            self.id = Base.__nb_objects

    @staticmethod
    def to_json_string(list_dictionaries):
        """Convert a list of dictionaries to a JSON string
        Args:
            list_dictionaries (list): A list of dictionaries.
        Returns:
            str: The JSON string representation of list_dictionaries.
        """
        if list_dictionaries is None or len(list_dictionaries) == 0:
            return "[]"
        return json.dumps(list_dictionaries)

    @classmethod
    def save_to_file(cls, list_objs):
        """Save a list of objects to a file
        Args:
            list_objs (list): A list of inherited Base instances.
        """
        file_name = cls.__name__ + ".json"
        new_list = []
        if list_objs:
            for obj in list_objs:
                new_list.append(cls.to_dictionary(obj))
        with open(file_name, mode="w") as myFile:
            myFile.write(cls.to_json_string(new_list))

    @staticmethod
    def from_json_string(json_string):
        """Convert a JSON string to a list of dictionaries
        Args:
            json_string (str): A string representing a list of dictionaries.
        Returns:
            list: The list of dictionaries represented by json_string.
        """
        if json_string is None or len(json_string) == 0:
            return []
        return json.loads(json_string)

    @classmethod
    def create(cls, **dictionary):
        """Create a new object
        Args:
            **dictionary (dict): Key/value pairs of attributes.
        Returns:
            object: An instance of cls.
        """
        if cls.__name__ == "Rectangle":
            dummy = cls(3, 2)
        elif cls.__name__ == "Square":
            dummy = cls(3)
        dummy.update(**dictionary)
        return dummy

    @classmethod
    def load_from_file(cls):
        """Load a list of objects from a file
        Returns:
            list: A list of instantiated objects.
        """
        try:
            with open(cls.__name__ + ".json", "r") as file:
                content = file.read()
        except FileNotFoundError:
            return []
        ex_content = cls.from_json_string(content)
        return [cls.create(**instance_dict) for instance_dict in ex_content]

    @classmethod
    def save_to_file_csv(cls, list_objs):
        """Save to a CSV file
        Args:
            list_objs (list): A list of inherited Base instances.
        """
        fn = cls.__name__ + ".csv"
        fields = ["id", "width", "height", "x", "y"] if fn == "Rectangle.csv" \
            else ["id", "size", "x", "y"]
        with open(fn, mode="w", newline="") as myFile:
            writer = csv.DictWriter(myFile, fieldnames=fields)
            if list_objs is None:
                writer.writerow([[]])
            else:
                writer.writeheader()
                for obj in list_objs:
                    writer.writerow(obj.to_dictionary())

    @classmethod
    def load_from_file_csv(cls):
        """Load from a CSV file
        Returns:
            list: A list of instantiated objects.
        """
        try:
            with open(cls.__name__ + ".csv", newline="") as myFile:
                reader = csv.DictReader(myFile)
                lst = []
                for row in reader:
                    for key, value in row.items():
                        row[key] = int(value)
                    lst.append(row)
                return [cls.create(**obj) for obj in lst]
        except FileNotFoundError:
            return []

    @staticmethod
    def draw(list_rectangles, list_squares):
        """Draw the rectangles and squares
        Args:
            list_rectangles (list): A list of Rectangle objects.
            list_squares (list): A list of Square objects.
        """
        shapes = []
        if list_rectangles:
            shapes.extend(list_rectangles)
        if list_squares:
            shapes.extend(list_squares)
        pen = turtle.Turtle()
        pen.pen(pencolor='black', pendown=False, pensize=2, shown=False)
        for shape in shapes:
            pen.penup()
            pen.setpos(shape.x, shape.y)
            pen.pendown()
            pen.forward(shape.width)
            pen.right(90)
            pen.forward(shape.height)
            pen.right(90)
            pen.forward(shape.width)
            pen.right(90)
            pen.forward(shape.height)
            pen.right(90)
