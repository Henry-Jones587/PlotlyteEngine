import json
import os
import sys
import random
import time
from dotdot import *
DotDot.credits(" for Plotlyte")
print("\n"*2)
class Game:
    def __init__(self):
        self.flags = {}
        self.inventory = []
        self.load_game()
        self.run()

    def load_game(self):
        # Check if a filename argument was provided
        if len(sys.argv) > 1:
            game = sys.argv[1]
            if not game.endswith(".json"):
                game += ".json"
            path = game
            if os.path.exists(path):
                with open(path, "r") as f:
                    self.gamedata = json.load(f)
                DotDot.load()
                print(f"Loaded game '{self.gamedata.get('title', 'Untitled')}' (version {self.gamedata.get('version', 'unknown')})")
                return
            else:
                print(f"File '{path}' not found. Falling back to prompt.")
        # Prompt user for filename if not provided or not found
        while True:
            game = input("Enter the file name of the game (without .json): ").strip()
            if not game:
                print("You need to enter a file name.")
                continue
            path = f"{game}.json"
            if not os.path.exists(path):
                print(f"File '{path}' not found. Try again.")
                continue
            with open(path, "r") as f:
                self.gamedata = json.load(f)
            DotDot.load()
            print(f"Loaded game '{self.gamedata.get('title', 'Untitled')}' (version {self.gamedata.get('version', 'unknown')})")
            break

    def check_condition(self, condition):
        """Return True if condition is met (or if no condition)."""
        if not condition:
            return True
        # Condition can check for items or flags
        has_item = condition.get("has_item")
        flag_set = condition.get("flag_set")
        not_has_item = condition.get("not_has_item")
        if has_item and has_item not in self.inventory:
            return False
        if flag_set and not self.flags.get(flag_set, False):
            return False
        if not_has_item and not_has_item in self.inventory:
            return False
        return True

    def apply_effects(self, effects):
        """Apply effects from option selection."""
        if not effects:
            return
        for effect, value in effects.items():
            if effect == "add_item":
                if value not in self.inventory:
                    self.inventory.append(value)
                    DotDot.dprint(DotDot.colour("BLUE") + f"You picked up a {self.gamedata['items'][value]['name']}!" + DotDot.colour("END"))
            elif effect == "remove_item":
                if value in self.inventory:
                    self.inventory.remove(value)
                    DotDot.dprint(DotDot.colour("RED") + f"You lost: {value}!" + DotDot.colour("END"))
            elif effect == "set_flag":
                self.flags[value] = True
            elif effect == "clear_flag":
                self.flags[value] = False
            elif effect == "restore_hp":
                # Placeholder for future health system
                print(f"You restore {value} HP. (Health system not implemented yet.)")
            else:
                print(f"Unknown effect: {effect} = {value}")

    def run(self):
        current_stage = self.gamedata.get("start")
        if not current_stage:
            print("Error: No start stage defined in the game file.")
            return

        while True:
            stage = self.gamedata["stages"].get(current_stage)
            if not stage:
                print(f"Error: Stage '{current_stage}' not found.")
                return

            DotDot.dprint("\n" + DotDot.colour("YELLOW") + stage["description"], 0.01)
            # Filter options by condition
            available_options = [
                option for option in stage["options"]
                if self.check_condition(option.get("condition"))
            ]

            if not available_options:
                DotDot.dprint("Thanks for playing!")
                break

            DotDot.dprint("\nOptions:")
            for i, option in enumerate(available_options, 1):
                DotDot.dprint(f"{i}. {option['label']}")

            DotDot.dprint(DotDot.colour("GREEN") + "Type the number of your choice, or 'inventory' to see your items, or 'quit' to exit." + DotDot.colour("END"))

            choice = input("> ").strip().lower()
            if choice == "quit":
                DotDot.dprint("Thanks for playing!" + DotDot.colour("END"))
                break
            elif choice == "inventory":
                if self.inventory:
                    DotDot.dprint("You have:")
                    for item in self.inventory:
                        item_data = self.gamedata.get("items", {}).get(item)
                        name = item_data["name"] if item_data else item
                        DotDot.dprint(f"- {name}")
                else:
                    DotDot.dprint("Your inventory is empty.")
                continue

            if not choice.isdigit() or int(choice) < 1 or int(choice) > len(available_options):
                DotDot.dprint(DotDot.colour("RED") + "Invalid choice. Try again." + DotDot.colour("END"))
                continue

            selected_option = available_options[int(choice) - 1]
            self.apply_effects(selected_option.get("effects"))
            current_stage = selected_option["target"]
if __name__ == "__main__":
    Game()
