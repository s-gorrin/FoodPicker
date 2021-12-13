"""
Seth Gorrin
Class: CS 521 - Fall 2
Date: 12 December 2021
Term Project
A class to generate dinner suggestions based on some user input.
At each step of the selection process, if the previous step has not happened,
    use all available options from what has already been chosen.
"""
import random
from copy import copy
from sys import exit


class FoodPicker:
    """
    A class to generate a list of foods and make random suggestions from it.
    The functionality of the class is around generating and then using a set
        of foods, based on meals I commonly cook and restaurants in my area.
    """
    __COOK_FILE = "cook.txt"
    __RESTAURANT_FILE = "restaurant.txt"
    __RESPONSES = {"cook":
                   ["1", "cook", "c", "make", "make food", "in", "eat in"],
                   "out":
                   ["2", "restaurant", "out", "eat out", "r", "o", "buy",
                    "buy food"]}

    def __init__(self):
        # private attributes
        self.__dining_index = 2  # use either as default value
        self.__dining_type = ""
        self.__foods_set = set()  # set used to handle multiples in rare cases
        self.__rejected = set()

        # public attributes
        self.region = ""
        self.suggestion = ""
        self.foods_dict = {}
        self.accepted = False

    def __repr__(self):
        """
        Generate a string of all the class variables with values
        :return: a newline-separated string of class variables
        """
        pick_string = ["A class to select a food. Information so far:"]

        if self.__dining_type != "":
            pick_string.append("Dining type: {}".format(self.__dining_type))
        if self.region != "":
            pick_string.append("Region: {}".format(self.region))
        # print label for foods no matter what
        pick_string.append("Foods: {}".format(
                ", ".join(sorted(self.__foods_set))))
        if self.__rejected:
            pick_string.append("Rejected foods: {}".format(
                ", ".join(sorted(self.__rejected))))
        if self.suggestion != "":
            pick_string.append("Suggestion: {}".format(
                self.suggestion))
        return "\n".join(pick_string)  # join info with newlines to print

    def __len__(self):
        """
        :return: The number of foods in the current foods set
        """
        return len(self.__foods_set)

    def __copy__(self):
        """
        :return: A new FoodPicker with the same data as this one
        """
        other = FoodPicker()

        other.__dining_index = copy(self.__dining_index)
        other.__dining_type = copy(self.__dining_type)
        other.__foods_set = copy(self.__foods_set)
        other.__rejected = copy(self.__rejected)

        other.region = self.region
        other.suggestion = self.suggestion
        other.foods_dict = copy(self.foods_dict)
        other.accepted = self.accepted

        return other

    def __add__(self, other):
        """
        combine the foods lists of two instances with awareness of type etc
        :param other: another instance of the FoodPicker class
        :return: a new instance with both lists and data
        """
        combined = FoodPicker()
        # agree on food type
        if self.__dining_index == other.__dining_index:
            combined.__dining_index = self.__dining_index
        else:
            combined.__dining_index = 2
        if combined.__dining_index == 2:
            combined.__dining_type = "both"
        else:
            combined.__dining_type = self.__dining_type

        # agree on region or use a string combining both
        if self.region == "All Regions" or other.region == "All Regions":
            combined.region = "All Regions"
        else:
            combined.region = ", ".join({self.region, other.region})

        combined.foods_dict.update(self.foods_dict)
        combined.foods_dict.update(other.foods_dict)

        combined.__foods_set.update(self.__foods_set)
        combined.__foods_set.update(other.__foods_set)
        # just add everything to the foods set
        combined.__foods_set.update(self.__rejected)
        combined.__foods_set.update(other.__rejected)

        return combined

    def clear(self):
        """
        reset the class to blank state
        """
        self.__init__()

    def get_foods(self):
        """
        :return: The current foods set as a tuple so it can't be changed
        """
        return tuple(sorted(self.__foods_set))

    def get_full_random(self, source_file="both"):
        """
        Get a random food from one file or the other or both without changing
            any variables of self
        :param source_file: Selector for which file to use
        :return: A randomly selected food from any category
        """
        # Create an instance of the FoodPicker class to maintain current state
        #   of self, to avoid breaking features.
        other = FoodPicker()
        # if source is a clear choice, use that. Anything else use both
        if source_file.lower() in self.__COOK_FILE or \
                source_file.lower() not in self.__RESTAURANT_FILE:
            other.__read_file(self.__COOK_FILE)
        if source_file.lower() in self.__RESTAURANT_FILE \
                or source_file.lower() not in self.__COOK_FILE:
            other.__read_file(self.__RESTAURANT_FILE)

        other.__use_all_regions()
        return other.get_random_food()

    def set_file(self, file_name):
        """
        Manually set the file to use, or do nothing if file is invalid.
        This can be used to use non-hard coded (const) files with the class.
            Additional files must contain one ':' per line to be valid.
        :param file_name: The name of a file
        :return: True for success, False for failure
        """
        if file_name in self.__RESPONSES["cook"]:
            self.__read_file(self.__RESTAURANT_FILE)
            return True
        if file_name in self.__RESPONSES["out"]:
            self.__read_file(self.__COOK_FILE)
            return True

        try:
            fd = open(file_name, 'r')
            file = fd.readlines()
            fd.close()
        except IOError:
            # if file not found, return False and do nothing about it
            return False

        for line in file:
            # there must be exactly one ':' per line to create foods_dict
            if line.count(':') != 1:
                return False

        self.__read_file(file_name)
        return True

    def prompt_file(self):
        """
        Prompt user for input and call helper to read the selected file.
        """
        # get a starting option from the user, with several ways to respond
        while True:
            response = input("Please indicate if you would like to"
                             " cook (1), or eat out (2): ").lower()
            
            if response in self.__RESPONSES["cook"]:
                response = self.__COOK_FILE
                break
            if response in self.__RESPONSES["out"]:
                response = self.__RESTAURANT_FILE
                break

            print("I don't understand that response.")

        # store the user response
        self.__dining_type = response[:-4]
        self.__dining_index = 0 if response == self.__COOK_FILE else 1
        self.__read_file(response)

    def __read_file(self, file_name):
        """
        Take a file name, read the file, and generate a dict of foods
        :param file_name: Name of a food-file, from a const variable
        """

        try:
            foods_file = open(file_name, 'r')
            foods = foods_file.readlines()
            foods_file.close()
        except IOError:
            exit("Error: The file '{}' seems to be missing.".format(file_name))
        else:
            for line in foods:
                # generate dictionary entries with a region and list of foods
                category = line[:line.find(':')]
                line = line[line.find(':') + 1:].strip()
                if category in self.foods_dict.keys():
                    self.foods_dict[category].extend(line.split(", "))
                else:
                    self.foods_dict[category] = line.split(", ")

    def __use_all_regions(self):
        """
        Helper function to add every food in the file to foods_set
        :return: the All Regions identifier and a set of every food
        """
        for value in self.foods_dict.values():
            self.__foods_set.update(value)
        self.region = "All Regions"
        return self.region, self.__foods_set

    def __region_helper(self, response):
        """
        Hand some of the input processing for prompt_region()
        :param response: user response from the input call in prompt_region()
        :return: A region, or "all"
        """
        regions = list(self.foods_dict.keys())
        for e in regions:
            if response in e.lower():
                return e

        if response in ("rand", "random", "pick", "surprise", "any"):
            region = random.choice(list(regions))
            print("The region {} has been randomly selected.".format(
                region))
            return region

        if response in ("all", "each", "every"):
            return "all"

        try:
            region = regions[int(response) - 1]
            return region
        except IndexError:
            print("That index is not in the list.")
        except ValueError:
            print("Please enter a region from the list.")
        return None

    def prompt_region(self, all_regions=False):
        """
        Prompt the user to select a region to narrow down food options
        :param all_regions: bool to get suggestions from all regions
        :return: the selected region and corresponding list of foods
        """
        # if prompt_file() has not been called, use both
        if self.__dining_type == "":
            self.__read_file(self.__COOK_FILE)
            self.__read_file(self.__RESTAURANT_FILE)
            self.__dining_type = "either"
            self.__dining_index = 2

        if all_regions:
            return self.__use_all_regions()

        print("Available regions:", ", ".join(self.foods_dict.keys()))
        region = None
        while not region:
            response =\
                input("Which region's foods sound good?\n> ").lower()
            region = self.__region_helper(response)

        # store and return the results for flexibility.
        if region == "all":
            return self.__use_all_regions()
        self.region = region
        self.__foods_set.update(self.foods_dict[region])
        self.accepted = False
        return region, self.foods_dict[region]

    def set_region(self, region):
        """
        Set the region manually without going through the prompt.
        If region is not in the current foods_dict, this does nothing
        :param region: A region from the current list
        :return: The foods list for the successfully chosen region or None
        """
        if region.lower() in ("all", "all regions", "every"):
            self.__use_all_regions()
            return tuple(sorted(self.__foods_set))

        for r in self.foods_dict.keys():
            if region.lower() in r.lower():
                self.region = r
                self.__foods_set.update(self.foods_dict[r])
                self.accepted = False
                return tuple(sorted(self.__foods_set))

        return None

    def get_random_food(self):
        """
        Get a random food from the list, but don't change self.suggestion.
        This is part of the more manual functionality of the class
        :return: A randomly selected food item from the list
        """
        if not self.__foods_set:
            return None
        return random.choice(tuple(self.__foods_set))

    def __suggest_helper(self, dining):
        """
        A private helper function to handle the food suggestion loop
        :param dining: The key word for the user's choice of dining
        :return: The accepted suggestion
        """
        # possible user responses to accept or reject suggestions
        yes = ("y", "yes", "t", "true", "okay", "sure", "good", "yup", "yeah",
               "accept", "alright", "1")

        suggestion = None
        while self.__foods_set:
            # get a random element from the foods set because pop is not random
            suggestion = self.get_random_food()
            self.__foods_set.remove(suggestion)
            response = input("Would you like to {} {}?\n> ".format(
                dining, suggestion))

            # suggestion is accepted
            if response.lower() in yes:
                print("Great! Enjoy your meal.")
                self.accepted = True
                break
            else:
                self.__rejected.add(suggestion)
        else:
            # keep last suggested option if the category runs out
            print("I have no more options in that category to suggest.")
            print("You didn't want:", ", ".join(self.__rejected))

        self.suggestion = suggestion
        return suggestion

    def suggest_food(self):
        """
        Suggest foods to the user from their previous choices
        :return: The accepted food suggestion
        """
        # if this is called before select_region, use all regions
        if self.region == "":
            self.prompt_region(True)
        summaries = ("You have opted to cook from the region:",
                     "You have opted to go to a restaurant of the region:",
                     "You have opted to have food of the region:")
        prompt = ("cook", "go to", "have")

        print(summaries[self.__dining_index], self.region)

        return self.__suggest_helper(prompt[self.__dining_index])

    def none_accepted(self):
        """
        Return True if the foods_set is empty
        :return: True or False
        """
        return len(self.__foods_set) == 0

    def reset_foods(self, *args):
        """
        Reset the foods to suggest, optionally adding more foods are arguments
        :param args: A list of foods to add to the foods set
        :return: A tuple of the state of the foods set before this update
        """
        starting_state = {"foods": tuple(self.__foods_set),
                          "rejected": tuple(self.__rejected)}
        for e in self.__rejected:
            self.__foods_set.add(e)
        self.__rejected.clear()
        if self.suggestion != "":
            self.__foods_set.add(self.suggestion)
        for e in args:
            self.__foods_set.add(e)

        self.accepted = False
        return starting_state


if __name__ == '__main__':
    import FoodPickerTester
    FoodPickerTester.run_all_tests()
