from __future__ import annotations

from mountain import Mountain

class MountainOrganiser:

    def __init__(self) -> None:
        self.mountain_list = []

    def cur_position(self, mountain: Mountain) -> int:
        for i in range(len(self.mountain_list)):
            if self.mountain_list[i] == mountain:
                return i

        raise KeyError(mountain)

    def add_mountains(self, mountains: list[Mountain]) -> None:
        mountains_sorted = []
        for mountain in mountains:
            # Using binary search to find the index to insert in
            lower = 0
            upper = len(mountains_sorted) - 1
            while lower <= upper:
                middle = (lower + upper) // 2
                comp1 = str(mountains_sorted[middle].length) + mountains_sorted[middle].name
                comp2 = str(mountain.length) + mountain.name
                if comp1 < comp2:
                    lower = middle + 1
                else:
                    upper = middle - 1

            # Insert at the found index
            mountains_sorted.insert(lower, mountain)

        # Combining 2 sorted lists
        i = 0
        j = 0
        result = []
        while i < len(self.mountain_list) and j < len(mountains_sorted):
            comp1 = str(self.mountain_list[i].length) + self.mountain_list[i].name
            comp2 = str(mountains_sorted[j].length) + mountains_sorted[j].name
            if comp1 < comp2:
                result.append(self.mountain_list[i])
                i += 1
            else:
                result.append(mountains_sorted[j])
                j += 1

        result = result + self.mountain_list[i:] + mountains_sorted[j:]
        self.mountain_list = result
