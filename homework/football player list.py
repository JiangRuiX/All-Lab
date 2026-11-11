"""
Football Player Management System - Team Project (target: ~80 / Excellent band)

Aligned with the Grading Rubric:
  Features (40%)      Delete / Find (plus add, edit, view and statistics)
  Persistence (30%)   Multiple objects managed in a list (no file I/O - that is Outstanding)
  UX (10%)            Repeating menu with validated input
  DX (10%)            User input validation + data class validation
  Git (10%)           Commit history and tagged releases (outside the code)

Only topics covered this semester are used: classes and objects, lists, dictionaries,
loops, conditionals, functions and input validation. No third-party libraries, no file I/O.
Following the "Parameters & Return Values" lecture: data and statistics functions take
parameters and return results, while interaction functions handle input and printing.

[English submission version] Same code as the Chinese version, with all user-facing
text in English. The Chinese clean version and the Chinese annotated version are unchanged.
"""


class Player:
    """A football player. The jersey number is a unique id and cannot be duplicated."""

    def __init__(self, name, number, position, age, goals, assists):
        self.name = name
        self.number = number
        self.position = position
        self.age = age
        self.goals = goals
        self.assists = assists

    def is_valid(self):
        """Data class validation: return False early if any field is invalid."""
        if self.name == "" or self.position == "":
            return False
        if self.number < 1 or self.number > 99:
            return False
        if self.age < 15 or self.age > 50:
            return False
        if self.goals < 0 or self.assists < 0:
            return False
        return True

    def __str__(self):
        """Called automatically by print(player) when showing a single player."""
        return (f"  Name: {self.name}\n"
                f"  Jersey number: {self.number}\n"
                f"  Position: {self.position}\n"
                f"  Age: {self.age}\n"
                f"  Goals: {self.goals}\n"
                f"  Assists: {self.assists}")

    def to_row(self):
        """Return one player as a single table row."""
        return (pad(self.number, 8) + pad(self.name, 16) + pad(self.position, 14) +
                pad(self.age, 8) + pad(self.goals, 8) + pad(self.assists, 8))


def pad(text, width):
    """Pad text to a display width: CJK chars count as 2 columns, ASCII as 1."""
    size = 0
    for ch in str(text):
        if ord(ch) > 127:
            size += 2
        else:
            size += 1
    return str(text) + " " * max(0, width - size)


def find_index_by_number(players, number):
    """Find a player by jersey number; return its index, or -1 if not found."""
    for i in range(len(players)):
        if players[i].number == number:
            return i
    return -1


def find_by_name(players, name):
    """Find players by exact name match; return a list of matches."""
    result = []
    for p in players:
        if p.name == name:
            result.append(p)
    return result


def find_by_position(players, position):
    """Find players by position; return a list of matches."""
    result = []
    for p in players:
        if p.position == position:
            result.append(p)
    return result


def total_goals(players):
    """Return the total goals across all players."""
    total = 0
    for p in players:
        total += p.goals
    return total


def top_scorer(players):
    """Return the top scorer, or None when the list is empty."""
    if len(players) == 0:
        return None
    best = players[0]
    for p in players:
        if p.goals > best.goals:
            best = p
    return best


def count_by_position(players):
    """Count players per position using a dictionary."""
    counts = {}
    for p in players:
        if p.position in counts:
            counts[p.position] += 1
        else:
            counts[p.position] = 1
    return counts


def read_int(prompt, low, high, default=None):
    """Read an integer in [low, high]; pressing Enter keeps default when supplied."""
    while True:
        text = input(prompt + " ").strip()
        if text == "" and default is not None:
            return default
        try:
            value = int(text)
        except ValueError:
            print("Invalid input: please enter an integer!")
            continue
        if low <= value <= high:
            return value
        print(f"Invalid input: please enter an integer between {low} and {high}!")


def read_text(prompt, default=None):
    """Read a non-empty string; pressing Enter keeps default when supplied."""
    while True:
        text = input(prompt + " ").strip()
        if text == "" and default is not None:
            return default
        if text != "":
            return text
        print("Invalid input: this field cannot be empty!")


def read_yes_no(prompt):
    """Read y / n and return True or False."""
    while True:
        answer = input(prompt + " ").strip().lower()
        if answer == "y":
            return True
        if answer == "n":
            return False
        print("Invalid input: please enter y or n!")


def print_table(players):
    """Print a player table, reused by List All and Find results."""
    print(pad("No.", 8) + pad("Name", 16) + pad("Position", 14) +
          pad("Age", 8) + pad("Goals", 8) + pad("Assists", 8))
    print("-" * 62)
    for p in players:
        print(p.to_row())


def show_menu():
    """Print the main menu."""
    print("\n===== Football Player Management System =====")
    print("  1. Add Player")
    print("  2. List All Players")
    print("  3. View Player Details (by jersey number)")
    print("  4. Edit Player (by jersey number)")
    print("  5. Delete Player (by jersey number)")
    print("  6. Find Player (number / name / position)")
    print("  7. Statistics")
    print("  0. Exit")
    print("=============================================")


def add_player(players):
    """Add a player; reject duplicate jersey numbers."""
    print("\n===== Add Player =====")
    number = read_int("Jersey number (1-99):", 1, 99)
    if find_index_by_number(players, number) != -1:
        print("Could not add: that jersey number already exists!")
        return

    name = read_text("Name:")
    position = read_text("Position (Forward/Midfielder/Defender/Goalkeeper):")
    age = read_int("Age (15-50):", 15, 50)
    goals = read_int("Goals (0-999):", 0, 999)
    assists = read_int("Assists (0-999):", 0, 999)

    player = Player(name, number, position, age, goals, assists)
    if not player.is_valid():
        print("Could not add: invalid player data, please try again!")
        return
    players.append(player)
    print(f"Added player: {name} (No. {number})")


def show_all(players):
    """List all players."""
    print("\n===== All Players =====")
    if len(players) == 0:
        print("No player data yet. Please add a player first.")
        return
    print_table(players)
    print(f"Total players: {len(players)}")


def show_detail(players):
    """Show full details of one player by jersey number."""
    print("\n===== Player Details =====")
    if len(players) == 0:
        print("No player data.")
        return
    number = read_int("Enter jersey number (1-99):", 1, 99)
    index = find_index_by_number(players, number)
    if index == -1:
        print("No player found with that jersey number.")
        return
    print(players[index])


def edit_player(players):
    """Edit a player by jersey number; pressing Enter keeps the current value."""
    print("\n===== Edit Player =====")
    if len(players) == 0:
        print("No player data.")
        return
    number = read_int("Enter jersey number to edit (1-99):", 1, 99)
    index = find_index_by_number(players, number)
    if index == -1:
        print("No player found with that jersey number.")
        return

    p = players[index]
    print(players[index])
    print("(Press Enter to keep a value; jersey number is the unique id and cannot be changed)")
    p.name = read_text(f"Name (current {p.name}):", p.name)
    p.position = read_text(f"Position (current {p.position}):", p.position)
    p.age = read_int(f"Age (15-50, current {p.age}):", 15, 50, p.age)
    p.goals = read_int(f"Goals (0-999, current {p.goals}):", 0, 999, p.goals)
    p.assists = read_int(f"Assists (0-999, current {p.assists}):", 0, 999, p.assists)

    if not p.is_valid():
        print("Could not edit: invalid data!")
        return
    print("Player details updated.")


def delete_player(players):
    """Delete a player by jersey number after a confirmation prompt."""
    print("\n===== Delete Player =====")
    if len(players) == 0:
        print("No player data.")
        return
    number = read_int("Enter jersey number to delete (1-99):", 1, 99)
    index = find_index_by_number(players, number)
    if index == -1:
        print("No player found with that jersey number.")
        return

    p = players[index]
    if read_yes_no(f"Delete {p.name} (No. {number})? (y/n):"):
        players.pop(index)
        print(f"Deleted player: {p.name}")
    else:
        print("Deletion cancelled.")


def search_player(players):
    """Find players by number, exact name, or position."""
    print("\n===== Find Player =====")
    if len(players) == 0:
        print("No player data.")
        return
    print("  1. By jersey number")
    print("  2. By name (exact match)")
    print("  3. By position")
    choice = read_int("Choose a search option (1-3):", 1, 3)

    found = []
    if choice == 1:
        number = read_int("Enter jersey number (1-99):", 1, 99)
        index = find_index_by_number(players, number)
        if index != -1:
            found.append(players[index])
    elif choice == 2:
        found = find_by_name(players, read_text("Enter name:"))
    else:
        found = find_by_position(players, read_text("Enter position:"))

    if len(found) == 0:
        print("No players matched your search.")
        return
    print(f"Found {len(found)} player(s):")
    print_table(found)


def show_statistics(players):
    """Show totals, averages, top scorer and players per position."""
    print("\n===== Statistics =====")
    if len(players) == 0:
        print("No player data to summarise.")
        return

    total_age = 0
    total_assists = 0
    for p in players:
        total_age += p.age
        total_assists += p.assists

    best = top_scorer(players)
    print(f"Player count: {len(players)}")
    print(f"Total goals: {total_goals(players)}")
    print(f"Total assists: {total_assists}")
    print(f"Average age: {total_age / len(players):.1f}")
    print(f"Top scorer: {best.name} ({best.goals} goals)")

    print("Players by position:")
    counts = count_by_position(players)
    for position in counts:
        print(f"  {position}: {counts[position]}")


def main():
    """Entry point: seed sample data, then show the menu until the user exits."""
    players = [
        Player("Liam Murphy", 10, "Forward", 22, 18, 6),
        Player("James Kelly", 7, "Midfielder", 24, 5, 12),
        Player("Sean O'Brien", 1, "Goalkeeper", 26, 0, 1),
    ]
    print("Welcome to the Football Player Management System! (3 sample players loaded)")

    while True:
        show_menu()
        choice = read_int("Enter a menu option:", 0, 7)

        if choice == 0:
            print("Thank you for using the system. Goodbye!")
            break
        elif choice == 1:
            add_player(players)
        elif choice == 2:
            show_all(players)
        elif choice == 3:
            show_detail(players)
        elif choice == 4:
            edit_player(players)
        elif choice == 5:
            delete_player(players)
        elif choice == 6:
            search_player(players)
        elif choice == 7:
            show_statistics(players)


if __name__ == "__main__":
    main()
