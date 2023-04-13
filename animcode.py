import os
import time
from typing import List, Dict

clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')

class _Element:
    def __init__(self, text="", length=0, defaults: List[int]=None):
        self.length = length
        if defaults is None:
            defaults = [2, 1, 3, 0, 0]
        self.text = text
        while len(defaults) < 5:
            defaults.append(0)
        self.defaults = [defaults[0], defaults[1], defaults[2], defaults[3], defaults[4]]


class Animator:
    def __init__(self):
        self._elements: List[_Element] = []

    def add(self, index: int, element: str, length: int = 0):
        if index != -1:
            self._elements.insert(index, _Element(element, length))
        else:
            self._elements.append(_Element(element, length))

    def set(self, element: List[_Element]):
        self._elements = element

    def rem(self, index: int):
        self._elements.pop(index)

    def replace(self, index: int, newel: str, length: int = 0):
        self._elements[index] = _Element(newel, length)

    def clear(self):
        self._elements = []

    async def animate(self, params: List[List[int]], speed=0.02, output=False, script=-1):
        # Variables
        result = """"""
        repl = {}
        group: Dict[int, List[_Element]] = {}
        clear()

        # Initialise
        for x in self._elements:

            # Will be run, if element have no group
            if len(params) < self._elements.index(x) + 1:
                params.append([0])
            # Script selecting
            if script != -1:
                params[self._elements.index(x)][0] = x.defaults[script]

            # Will be run if type is draw, or animations suspended
            if params[self._elements.index(x)][0] == 1:
                # Put element to text
                result += x.text
                if self._elements[-1] != x:
                    result += "\n"
            elif params[self._elements.index(x)][0] == 4:
                # Put element to text
                result += format_string(x.text, params[self._elements.index(x)][1])
                if self._elements[-1] != x:
                    result += "\n"


            # Will be run if type is animation
            elif params[self._elements.index(x)][0] == 2 or params[self._elements.index(x)][0] == 3 or params[self._elements.index(x)][0] == 5 or params[self._elements.index(x)][0] == 6:

                # Will be run if element have no run-group
                if len(params[self._elements.index(x)]) < 2:
                    params[self._elements.index(x)].append(0)

                # Add element to draw group
                if params[self._elements.index(x)][1] in group:
                    group[params[self._elements.index(x)][1]].append(x)
                else:
                    group[params[self._elements.index(x)][1]] = []
                    group[params[self._elements.index(x)][1]].append(x)

                # Create element default alias
                if params[self._elements.index(x)][0] == 2:
                    repl["(" + str(params[self._elements.index(x)][1]) + "&" + str(
                        group[params[self._elements.index(x)][1]].index(x)) + ")"] = " "
                elif params[self._elements.index(x)][0] == 3:
                    repl["(" + str(params[self._elements.index(x)][1]) + "&" + str(
                        group[params[self._elements.index(x)][1]].index(x)) + ")"] = x.text
                elif params[self._elements.index(x)][0] == 5:
                    repl["(" + str(params[self._elements.index(x)][1]) + "&" + str(
                        group[params[self._elements.index(x)][1]].index(x)) + ")"] = format_string(x.text, 0)
                elif params[self._elements.index(x)][0] == 6:
                    repl["(" + str(params[self._elements.index(x)][1]) + "&" + str(
                        group[params[self._elements.index(x)][1]].index(x)) + ")"] = format_string(x.text, 0)

                # Put element alias to text
                result += "(" + str(params[self._elements.index(x)][1]) + "&" + str(
                    group[params[self._elements.index(x)][1]].index(x)) + ")"
                if self._elements[-1] != x:
                    result += "\n"

        # Animate
        for x in group:

            # Used to find the longest element
            longest = 0
            for y in group[x]:
                if params[self._elements.index(y)][0] == 2 or params[self._elements.index(y)][0] == 3:
                    if len(y.text) > longest:
                        longest = len(y.text)
                elif params[self._elements.index(y)][0] == 5 or params[self._elements.index(y)][0] == 6:
                    if y.length > longest:
                        longest = y.length

            # Animation core
            for z in range(longest + 1):
                for y in group[x]:

                    # Element animation type
                    if params[self._elements.index(y)][0] == 2:
                        repl["(" + str(x) + "&" + str(group[x].index(y)) + ")"] = y.text[longest - z:]
                    elif params[self._elements.index(y)][0] == 3:
                        if len(y.text) + 1 < z:
                            repl["(" + str(x) + "&" + str(group[x].index(y)) + ")"] = ""
                        else:
                            repl["(" + str(x) + "&" + str(group[x].index(y)) + ")"] = y.text[z:]
                    elif params[self._elements.index(y)][0] == 5:
                        repl["(" + str(x) + "&" + str(group[x].index(y)) + ")"] = format_string(y.text, z)
                    elif params[self._elements.index(y)][0] == 6:
                        repl["(" + str(x) + "&" + str(group[x].index(y)) + ")"] = format_string(y.text, longest - z)
                clear()
                # print(result)
                # Result with replacing aliases
                print(replace_string(repl, result))
                time.sleep(speed)
        # If need output, query
        if output:
            clear()
            # Raw result
            # return input(result)
            # Result with replacing aliases
            return input(replace_string(repl, result))
        clear()
        # Raw result
        # print(result)
        # Result with replacing aliases
        print(replace_string(repl, result, True))


def create_array(elements: List[List[int]]) -> List[List[int]]:
    result: List[List[int]] = []
    for x in elements:
        for y in range(x[0]):
            result.append([x[1]])
    return result


def replace_string(templates, string, is_raw=False):
    res = string
    for x in templates:
        res = res.replace(x, templates[x])
    if not is_raw:
        for x in res:
            if x == "&":
                r = 0
                r2 = 0
                if res[res.index(x) - 2] == "(":
                    r = res.index(x) - 2
                elif res[res.index(x) - 3] == "(":
                    r = res.index(x) - 3
                if res[res.index(x) + 2] == ")":
                    r2 = res.index(x) + 2
                elif res[res.index(x) + 3] == ")":
                    r2 = res.index(x) + 3
                replacer = ""
                for y in range(r2 - r + 1):
                    replacer += " "
                ls = list(res)
                ls[r:r2 + 1] = replacer
                res = "".join(ls)
    return res

def format_string(text: str, var: int) -> str:
    loc = {}
    exec("a = " + text.format(var), globals(), loc)
    return loc["a"]

animator: Animator = Animator()
