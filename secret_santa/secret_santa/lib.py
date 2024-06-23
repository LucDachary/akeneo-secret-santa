"""Secret Santa processing library.
"""
from typing import List, Tuple, Dict, Set, Optional


class Participant:
    """A Secret Santa participant, represented by its name.

    Each participant has its set of valid recipient options.
    """
    __name: str
    __options: Set

    def __init__(self, name, options: Optional[Set] = None):
        assert isinstance(name, str) and name, "Please provide the name as a non-empty string."
        if options is not None:
            assert isinstance(options, set), "Please provide the options as a set of Participant."
            for option in options:
                assert isinstance(option, Participant), "All options must be of type Participant."

        self.__name = name
        self.__options = options or set()

    @property
    def name(self) -> str:
        return self.__name

    @property
    def options(self) -> Set:
        """Provide the valid recipient options as a set."""
        return self.__options

    @options.setter
    def options(self, new_options: Set):
        assert isinstance(new_options, set)
        for new_option in new_options:
            assert isinstance(new_option, Participant), "All options must be of type Participant."

        self.__options = new_options

    @property
    def options_str(self) -> str:
        """Return a string representation of the recipient options.

        Options are sorted alphabetically.
        """
        return ", ".join(sorted(map(str, self.__options)))

    def __str__(self):
        return self.__name

    def __repr__(self):
        return f"{self.__name} [options: {len(self.__options)}]"


def parse_data(names: Set[str], exclusions: List[Tuple[str, str]]) -> Dict[str, Participant]:
    """Parse and build the set of Participant.

    exclusions represent pairs of names that must not be recipient options for one another.
    Return a mapping of names and Participant.
    """
    # Each Participant is initialised with zero option.
    participants = dict([(name, Participant(name)) for name in names])

    # Add all options by default.
    all_participants = participants.values()
    for name, par in participants.items():
        par.options = set(all_participants) - set([par])

    # Remove options according to exclusions.
    for mate1, mate2 in exclusions:
        participants[mate1].options.remove(participants[mate2])
        participants[mate2].options.remove(participants[mate1])

    return participants


def secure_one_option_participants(participants: Dict[str, Participant]) -> Dict[str, Participant]:
    """Browse and modify the list of participants to secure the single options.

    If a participant only has one recipient option, this function will try to remove it from others'
    recipient options, to "secure" it. Return the refined mapping.
    Raise RuntimeError in case a participant's sole recipient cannot be secured.
    """
    to_secure = list(filter(lambda p: len(p.options) == 1, participants.values()))

    while to_secure:
        vip = to_secure.pop()

        for par in participants.values():
            if vip != par:
                # according to lehiester (https://stackoverflow.com/a/60233), the min() function
                # would be the most efficient way to get the value of a one-item set. Interesting!
                try:
                    par.options.remove(min(vip.options))

                    match len(par.options):
                        # We might have created another "single recipient" participant,
                        # so queue up!
                        case 1:
                            # Participant "par" is down to one option. To be secured…
                            to_secure.append(par)
                        case 0:
                            raise RuntimeError("Cannot secure this set of Participant.")
                except KeyError:
                    # this option was not available for par; nothing to do.
                    pass

    return participants


def work_a_distribution(participants: Dict[str, Participant], path: List[Participant]) -> bool:
    """Browse the list of participants to build a secret santa sorting.

    This function uses a backtrack algorithm. In case a valid distribution is found, path will
    represent the chain of sender-recipient. The last participant in the path will make a gift to
    the first participant in the path.
    Return false in case no valid distribution can be worked out.

    Warning: this is a recursive function.
    """
    if len(path) == len(participants) and path[0] in path[-1].options:
        # Found a path!
        return True

    for name, par in participants.items():
        if par not in path and (path == [] or par in path[-1].options):
            path.append(par)  # Trying…
            if work_a_distribution(participants, path):
                return True
            else:
                path.pop()  # … backtracking.

    # Failed to find path.
    return False
