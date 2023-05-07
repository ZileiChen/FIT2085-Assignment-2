from mountain import Mountain

class MountainManager:

    def __init__(self) -> None:
        """
        Initiate neccessary arguements
        """
        # Initiate storage (list) storing all mountains added
        self.storage:list = []
        # Initiate the maximum difficulty of all mountains added so far
        self.max_diff:int = 0

    def add_mountain(self, mountain: Mountain):
        """
        Add a mountain to manager

        Args: the mountain to be added
        Raises: None
        Returns: None
        Complexity: Best case = Worst case = O(1)
        """
        # Add a mountain to storage
        self.storage.append(mountain)
        # Find the maximum difficulty of all mountains added so far
        if (mountain.difficulty_level > self.max_diff):
            self.max_diff = mountain.difficulty_level

    def remove_mountain(self, mountain: Mountain):
        """
        Remove a mountain from manager

        Args: the mountain to be removed
        Raises: ValueError: mountain is not in list
        Returns: None
        Complexity: Best case = Worst case = O(len(self.storage))
        """
        # Remove a mountain from storage
        # Mountain is removed at position n, and shift all mountains from position n+1 to left
        self.storage.remove(mountain)
        return

    def edit_mountain(self, old: Mountain, new: Mountain):
        """
        Edit a mountain from manager

        Args: the old mountain to be removed, the new mountain to be added
        Raises: None
        Returns: None
        Complexity: 
          Best case = O(1): Mountain is replaced at first position in list
          Worst case = O(len(self.storage)): Mountain is replaced at last position in list,
            or no old mountain is found in storage
        """
        for i in range(len(self.storage)):
            if self.storage[i] == old:
                # Replace specified old mountain with new one
                self.storage[i] = new
                break
        return

    def mountains_with_difficulty(self, diff: int):
        """
        Return list of mountains with same specified difficulty

        Args: difficulty to filter mountains with
        Raises: None
        Returns: list of mountains with this difficulty
        Complexity: 
          Best case = Worst case = O(len(self.storage)): 
            Traverse through entire list to find mountains with matching difficulty
        """
        # Initiate a mountain list storing all mountains with this difficulty
        mountain_list = []
        for i in range(len(self.storage)):
            if (self.storage[i].difficulty_level == diff):
                # Add mountain with this difficulty to list
                mountain_list.append(self.storage[i])
        return mountain_list

    def group_by_difficulty(self):
        """
        Return list of lists of mountains, grouped by and sorted by ascending difficulty.

        Args: None
        Raises: None
        Returns: list of lists of mountains
        Complexity: 
          Best case = Worst case = O(len(self.storage) * self.max_diff): 
            Traverse through entire list to find mountains with matching difficulty,
            with difficulty ranging from 1 to maximum
        """        
        # Initiate a list storing all diffculty list of mountains
        group_diff_list = []
        for i in range(self.max_diff):
            # Get a list of mountain with specific difficulty
            diff_list = self.mountains_with_difficulty(i+1)
            if (len(diff_list) != 0):
                # Add the list to group
                group_diff_list.append(diff_list)
        return group_diff_list

