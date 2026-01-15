"""
Chatchana Chaenban
683040487-6
P1
"""

from room import Bedroom, Kitchen

def main():
    print("----BEDROOM----")
    bedroom = Bedroom(12, 10, 5)
    print(bedroom.describe_room())
    print(bedroom.get_purpose())
    print("Bedroom lighting:", bedroom.get_recommended_lighting(), "lumen/sq ft")
    print()

    print("----KITCHEN----")
    kitchen1 = Kitchen(15, 12, has_island=True)
    print(kitchen1.describe_room())
    print(kitchen1.get_purpose())
    print("Kitchen lighting:", kitchen1.get_recommended_lighting(), "lumen/sq ft")

    island , wall = kitchen1.calculate_counter_space()
    print("Island counter area:", island, "sq ft")
    print("Wall counter area:", wall, "sq ft")
    print()

    kitchen2 = Kitchen(15, 12, has_island=False)
    print(kitchen2.describe_room())
    print(kitchen2.get_purpose())

    island, wall = kitchen2.calculate_counter_space()
    print("Island counter area:", island, "sq ft")
    print("Wall counter area:", wall, "sq ft")

if __name__=="__main__":
    main()