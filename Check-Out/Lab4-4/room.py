"""
Chatchana Chaenban
683040487-6
P1
"""

from abc import ABC, abstractmethod

class Room(ABC):
    def __init__(self, length, width):
        self.length = length
        self.width = width
    
    @abstractmethod
    def get_purpose(self):
        """Returns a string describing purposes of the room"""
        pass

    @abstractmethod
    def get_recommended_lighting(self):
        """Returns recommended lighting in lumens per square foot"""
        pass

    def calculate_area(self):
        return self.length * self.width
    
    def describe_room(self):
        area = self.calculate_area()
        return f"A {self.__class__.__name__} of {area} sq ft used for {self.get_purpose()}"
    
class Bedroom(Room):
    def __init__(self, length, width, bedsize):
        super().__init__(length, width)
        self.bed_size = bedsize
    
    def get_purpose(self):
        return f"Comfy sleepy bed's size is {self.bed_size} ft"
    
    def get_recommended_lighting(self):
        return 15

class Kitchen(Room):
    def __init__(self, length, width, has_island=True):
        super().__init__(length, width)
        self.has_island = has_island

    def get_purpose(self):
        if self.has_island:
            return "Island's Kitchen had already for opening and serving "
        return "Island's Kitchen is preparing for food"
    
    def get_recommended_lighting(self):
        return 35
    
    def calculate_counter_space(self):
        """
        Calculate Kitchen Area
        
        Parameters
        ------
        nothing
        
        Return
        ------
        tuple(float, float)
              island_counter_area is area of the island counter in feet
              wall_counter is area of wall counter in feet

        Raises
        ------
        nothing
        
        Example
        ------
        >>> obj.calculate_counter_space()
        (3.14, 2.25)

        """

        room_area = self.calculate_area()
        if self.has_island:
            island_counter_area = room_area * (1/5)
            wall_counter = room_area * (1/4)
        else:
            island_counter_area = 0
            wall_counter = room_area * (1/2)
        
        return island_counter_area, wall_counter

    

