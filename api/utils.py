from typing import List

from rest_framework import exceptions


def validate_multiple_choice(choices_list: List, user_choice: str) -> str:
    """ Checks if the user's choice is part of the list of choices.
        Else raises an error and displays the choices. """

    is_choice_valid = False
    choices_proposition = "Choices: "
    for choice in choices_list:
        choices_proposition += f"'{choice[0]}' "
        if user_choice == choice[0]:
            is_choice_valid = True
    if not is_choice_valid:
        print("Choice -> not valid!")
        message = f"{user_choice}: not a valid choice -> {choices_proposition}"
        raise exceptions.ValidationError(detail=message)
    else:
        print("Choice -> valid! :D")
        return user_choice
