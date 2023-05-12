from __future__ import annotations

from mountain import Mountain

class MountainOrganiser:
    """
    Organises a list of mountains by their length, then by their name.
    """
    def __init__(self) -> None:
        """
        Initialises the class with a mountain list.
        :complexity: O(1)
        """
        self.mountain_list = []

    def cur_position(self, mountain: Mountain) -> int:
        """
        Returns the rank (index) of the mountain given.
        :raises KeyError: when the mountain is not in the list
        :complexity: worst case O(n) where n is the length of the mountain_list and the mountain is at the end or
        doesn't exist in the list.
        best cast O(1) where the mountain is at the start of the list
        """
        for i in range(len(self.mountain_list)):
            if self.mountain_list[i] == mountain:
                return i

        raise KeyError(mountain)

    def add_mountains(self, mountains: list[Mountain]) -> None:
        """
        Adds the given mountain(s) to the list of mountains. This is done by first sorting the provided list by
        inserting into a new list using binary search O(m*log(n)) where m is the length of the list of the provided
        mountains, and n is the list of the sorted mountains.
        Then we have 2 lists; the sorted list from the provided mountains, and the existing sorted list from previous
        additions. We use a simple sorting algorithm (same as the combining step of the merge sort algorithm) to sort
        the 2 lists together which yields a time complexity of O(m+n)
        :complexity: Hence, the combination of those 2 steps yields a time complexity of O(m*log(m)+n)
        """
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
