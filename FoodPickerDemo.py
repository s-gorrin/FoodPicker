"""
Seth Gorrin
Class: CS 521 - Fall 2
Date: 12 December 2021
Term Project
A file to demonstrate some of the functionality of the FoodPicker class
"""

from FoodPicker import FoodPicker


def full_random_demo(source):
    """
    Let the FoodPicker class choose a random food from the indicated file
    :param source: The file to get the random food from
    :return: the suggestion
    """
    picker = FoodPicker()
    return picker.get_full_random(source)


def prompt_sequence_demo():
    """
    A demo of the full user-input sequence of the FoodPicker class
    :return: the suggestion
    """
    picker = FoodPicker()

    picker.prompt_file()
    picker.prompt_region()

    food = ""
    while not picker.accepted:
        if picker.none_accepted():
            picker.prompt_region()
        food = picker.suggest_food()

    print("\n{}\n".format(picker))
    return food


if __name__ == '__main__':
    print("FoodPicker class demonstration:\n")
    rand = full_random_demo("cook")
    prompt = prompt_sequence_demo()

    print("Random suggestion: {}".format(rand))
    print("Prompted suggestion: {}".format(prompt))
