"""
Seth Gorrin
Class: CS 521 - Fall 2
Date: 12 December 2021
Term Project
A suite of unit tests for the FoodPicker class.
"""

from FoodPicker import FoodPicker
from copy import copy
import random


def magic_tester(first, second):
    """
    test the magic methods of the FoodPicker class, including:
        __add__(), __len__(), __copy__(), clear(), get_foods()
    :param first: A FoodPicker
    :param second: A FoodPicker
    :return: A food suggestion
    """
    first.prompt_region(True)  # use all regions
    assert first.region == "All Regions", "prompt region all regions broke"
    assert len(first.get_foods()) == len(first), "__len__ or get_foods() broke"

    print("Please answer the following prompts:")
    second.prompt_file()
    second.prompt_region()

    combined = first + second
    assert set(combined.get_foods()) ==\
           set(first.get_foods() + second.get_foods()), "__add__ did not work"
    first.clear()
    assert first.suggestion == "", "clear did not work"
    first = copy(second)
    assert first.__repr__() == second.__repr__(), "copy did not work"

    print("Please accept any food you like, or none:")
    return second.suggest_food()


def randoms_and_suggestions_tester(picker):
    """
    Test get_full_random(), get_random_food(), reset_foods(), suggest_food()
        prompt_file(), prompt_region()
    :param picker: A FoodPicker
    :return: A suggestion
    """
    print("Please select a file choice:")
    picker.prompt_file()
    assert len(picker.foods_dict.keys()) != 0, "no file was set"

    picker.clear()  # make sure the picker is blank
    food = picker.get_random_food()
    assert not food, "clear didn't clear"

    picker.get_full_random()
    assert picker.suggestion == "", "full random edited the class"
    picker.reset_foods("soylent")  # add a food that's not in a file
    soy = picker.get_random_food()
    assert soy == "soylent", "get_random_food didn't return the only option"

    food = picker.suggest_food()  # should pick "all regions"
    assert picker.region == "All Regions", "suggest_food didn't get all"

    picker.clear()
    print("Please don't respond 'all' to this one:")
    picker.prompt_region()
    assert picker.region in picker.foods_dict.keys(), "prompt_region didn't"

    return food


def set_tester(picker):
    """
    Test setters of the FoodPicker class: set_file(), set_region()
    :param picker: A FoodPicker
    :return: A suggestion
    """
    picker.clear()  # make sure the picker is blank

    assert not picker.set_file("FoodPicker.py"), "set an invalid, existent file"
    assert picker.set_file("restaurant"), "failed to set a valid file"

    # set a random region
    picker.set_region(random.choice(tuple(picker.foods_dict.keys())))
    reg = picker.region
    picker.set_region("the earth's core")
    assert reg == picker.region, "set_region set a non-existent region"

    picker.set_region("Asia")
    assert picker.region == "Asia", "set_region did not set the region"

    return picker.get_random_food()


def run_all_tests():
    """
    Run the full sequence to test every public function in FoodPicker
    """
    print("++ FoodPicker unit tests. Please answer as directed. ++\n")
    # get one suggestion from each test function
    test_suggestions = []
    picker1 = FoodPicker()
    picker2 = FoodPicker()
    test_suggestions.append(magic_tester(picker1, picker2))
    test_suggestions.append(randoms_and_suggestions_tester(picker1))
    test_suggestions.append(set_tester(picker1))

    # for full repr output, reject a few options, then accept
    test_suggestions.append(picker1.suggest_food())
    print("\n"+"="*10, "FoodPicker sample repr output", "="*10)
    print(picker1)

    assert len(test_suggestions) == 4, "a test function didn't run correctly"
    print("\nSuggestions generated from these tests:", test_suggestions)
    print("\n++ All unit tests for FoodPicker passed successfully. ++")


if __name__ == '__main__':
    run_all_tests()
