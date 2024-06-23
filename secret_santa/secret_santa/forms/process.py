from django import forms

from secret_santa import lib

# List of values to speed up the test
DEV_INITIAL_NAMES = """Albert
Bertrand
Caroline
David
"""

DEV_INITIAL_BLACKLIST = """Albert, David
Caroline, Bertrand
"""


class ProcessForm(forms.Form):
    participants = forms.CharField(widget=forms.Textarea, label="Participant Names",
                                   initial=DEV_INITIAL_NAMES)
    blacklist = forms.CharField(widget=forms.Textarea, label="Forbidden Pairs",
                                initial=DEV_INITIAL_BLACKLIST, required=False, )

    def is_valid(self):
        names = set()
        exclusions = []

        # Parse names
        for line in self.data["participants"].split("\n"):
            # TODO further clear undesired characters here.
            if line := line.strip():
                names.add(line)

        # Parse exclusions
        for line in self.data["blacklist"].split("\n"):
            if line := line.strip():
                left, right = line.split(",")

                if (left := left.strip()) and (right := right.strip()):
                    exclusions.append((left, right))
                # TODO handle malformed input

        # 1/3 prepping datasets…
        participants = lib.parse_data(names, exclusions)

        # 2/3 Securing participants with limited options…
        participants = lib.secure_one_option_participants(participants)

        # 3/3 Working Santa's magic…
        path = []
        if lib.work_a_distribution(participants, path):
            # Hurray! Santa sorted things out!
            path.append(path[0])

            for i in range(len(path) - 1):
                # {path[i].name} makes a gift to {path[i+1].name}
                # TODO path the list "path" to ProcessView so it can save the data into the
                # database.
                pass

        else:
            self.add_error("participants", "Hu-oh… I failed to find a satisfying solution for you "
                           "dataset and contraints.")

        participants = lib.parse_data(names, exclusions)
        return super().is_valid()
