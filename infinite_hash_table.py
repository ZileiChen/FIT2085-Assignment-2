from __future__ import annotations
from typing import Generic, TypeVar

from data_structures.referential_array import ArrayR
from data_structures.linked_stack import* 
K = TypeVar("K")
V = TypeVar("V")

class InfiniteHashTable(Generic[K, V]):
    """
    Infinite Hash Table.

    Type Arguments:
        - K:    Key Type. In most cases should be string.
                Otherwise `hash` should be overwritten.
        - V:    Value Type.

    Unless stated otherwise, all methods have O(1) complexity.
    """

    TABLE_SIZE = 27

    def __init__(self) -> None:
        """
        Initiate a hash table and additional arguements.
        """
        # Create a parent hash table with size = TABLE_SIZE
        self.table = ArrayR(self.TABLE_SIZE)
        # Create a counter counting the total elements (key,value) added to hash table
        self.count = 0
        # Create a level indicating the level of current working hash table
        self.level = 0
        
    def hash(self, key: K) -> int:
        """
        Hash the key into the hash table

        Args: the key to be inserted for hashing
        Raises: None
        Returns: the position of the key in hash table
        Complexity: Best case = Worst case = O(1).
        """
        if self.level < len(key):
            return ord(key[self.level]) % (self.TABLE_SIZE-1)
        return self.TABLE_SIZE-1

    def __getitem__(self, key: K) -> V:
        """
        Get the value at a certain key

        Args: the key used for searching its value
        Raises: KeyError: when the key doesn't exist
        Returns: the value based on its key
        Complexity: 
          Best case: O(1): 
            key found at the parent table, at the first position in table
          Worst case: O(self.TABLE_SIZE*len(key)): 
            key found at the furthest sub-table, at the last position in table
        """
        value = 0
        # Create a Stack tracking all went-through hash table  
        tracking = LinkedStack()
        # Push parent table to tracking
        tracking.push(self.table)
        # Create a location list getting all went-through positions of the key
        location = self.get_location(key)

        for i in range(len(location)-1):
            # Get the current table for investigating
            cur = tracking.pop()
            for j in range(self.TABLE_SIZE):
                # If current position matches location list
                if j == location[i]:
                    # Push the current sub-table for tracking
                    tracking.push(cur[j][1])
                    break
        # Get the value at the final hash table where the key is located
        value = tracking.peek()[location[-1]][0][1]
        # If no value found: key doesnt exist
        if value == 0:
            raise KeyError('Key doesnt exist')
        
        return value

    def __setitem__(self, key: K, value: V) -> None:
        """
        Set an (key, value) pair in our hash table.

        Args: the key and value to be inserted to hash table
        Raises: None
        Returns: None
        Complexity: 
          Best case: O(1): 
            (key,value) can be added at the parent table, at the first position in table 
            (no collision)
          Worst case: O(self.TABLE_SIZE*len(key)): 
            (key,value) can be added at the furthest sub-table, at the last position in table
        """
        # Increment number of item added to hash table
        self.count += 1
        # Initialise the current level = 0, indicating the parent hash table
        self.level = 0
        # Create a storage of unallocated items
        # An item includes [key, its value, its position in hash table]
        item_store = LinkedStack()
        # Create a Stack tracking all went-through hash table
        tracking = LinkedStack()
        # Position of hashed key in parent table
        pos = self.hash(key)
        # Add item to item's storage
        item_store.push([key,value,pos])
        # Add parent table for tracking
        tracking.push(self.table)
        while (item_store.is_empty() == False):
            # Take out unallocated item from storage for hashing
            item = item_store.pop()
            # Take the current table from tracking & hash item to this table
            cur = tracking.peek()
            # Position of hashed key in current table
            item[2] = self.hash(item[0])
            # If there is no item in this position
            if cur[item[2]] == None:
                # Add item to this position
                cur[item[2]] = []
                cur[item[2]].append(item)
            else:
                # If this position was used before (no real item located currently)
                if len(cur[item[2]]) == 2:
                    # Take back the item to storage and move to next sub-table
                    tracking.push(cur[item[2]][1])
                    item_store.push(item)
                    # Increment the current level
                    self.level += 1

                # If there is already an item in this position
                else:
                    # Push both items to unallocated storage
                    item2 = cur[item[2]][0]
                    item_store.push(item)
                    item_store.push(item2)
                    # Add a marker to this collided position, indicating it was used
                    char_count = self.level + 1
                    dict_item = [item[0][0:char_count],0,item[2]]
                    cur[item[2]][0] = (dict_item)
                    # print("Same")
                    # print(item[0],item2[0])
                    # print(dict_item)
                    self.level += 1
                    # Create new sub hash table at current collided position
                    cur[item[2]].append(ArrayR(self.TABLE_SIZE))  
                    # Add this sub-table for tracking                  
                    tracking.push(cur[item[2]][1])
        return


    def __delitem__(self, key: K) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        Args: the key and value to be deleted from hash table
        Raises: KeyError: when the key doesn't exist
        Returns: None
        Complexity: 
          Best case: O(1): 
            (key, value) is deleted at the parent table, at the first position in table
          Worst case: O(self.TABLE_SIZE*len(key)): 
            (key, value) is deleted at the furthest sub-table, at the last position in table
        """
        # Decrement the number of item in hash table
        self.count -= 1
        # Get sequence of positions of key
        location = self.get_location(key)
        # Create a Stack tracking all went-through hash table of this key
        tracking = LinkedStack()
        tracking.push(self.table)
        # Push all tables' location to Stack, from parent table to table containing key
        for i in range(len(location)-1):
           # Get current table location
           cur = tracking.peek()
           tracking.push(cur[location[i]][1])

        # Delete item (key,value) from the current table
        tracking.peek()[location[-1]] = None
        # If deleted item is in parent table: Do nothing
        if len(location) == 1:
            return
        else:
            # Check if there is any item left in hash table other than deleted item
            for k in range(len(location)-1):
                cur = tracking.pop()
                # Initialize counter counting any item left
                element_count = 0   
                for j in range(self.TABLE_SIZE):
                    # If there is any item left: increment counter
                    if cur[j] is not None:
                        if (cur[j][0][1] != 0) and (cur[j][0][0] != key):
                            item = cur[j][0]
                            element_count += 1
                # If there is only 1 item found
                if element_count == 1:
                    # Previous table location
                    prev = tracking.peek()
                        #print(location[len(location) - k - 1])
                        #print(prev[location[len(location) - k - 1]])
                    # Add this item to higher-level table
                    prev[location[-1 -k - 1]][0] = item
                    # Collapse the current table
                    cur = None
                # If there are more than 1 item left, or we are at parent table
                else:
                    break

    def __len__(self):
        """
        Return the total number of (key,value) inserted in hash table
        """
        return self.count

    def __str__(self) -> str:
        """
        String representation.

        Not required but may be a good testing tool.
        """
        raise NotImplementedError()

    def get_location(self, key):
        """
        Get the sequence of positions required to access this key.

        Args: the key used to get all of its positions
        Raises: KeyError: when the key doesn't exist
        Returns: list of all went-through positions of the key
        Complexity:
          Best case: O(1): 
            key found at the parent table, at the first position in table
          Worst case: O(self.TABLE_SIZE*(len(key)+1)): 
            key found at the furthest sub-table, at the last position in table
        """
        # Initialize the list containing the sequence of positions
        location = []
        # Create a Stack tracking all went-through hash table
        tracking = LinkedStack()
        # Add the parent hash table for tracking
        tracking.push(self.table)
        # Initiate counter counting each character (left->right) in the key
        char_count = 1
        while (tracking.is_empty() == False):
            # Pop current hash table for investigating
            cur = tracking.pop()
            for i in range(self.TABLE_SIZE):
                # If the position in table is not empty
                if cur[i] is not None:
                    # If the key in this position totally matched with input key
                    if (key == cur[i][0][0]) & (cur[i][0][1] != 0):
                        # Add this location to list and return the list
                        location.append(i)
                        return location
                    # If the key in this position partially matched with input key
                    if key[0:char_count] == cur[i][0][0]:
                        # Add the sub-table in this position for tracking
                        tracking.push(cur[i][1])
                        # Increment key's character counter
                        char_count += 1
                        # Add this location to list
                        location.append(i)
                        break
        if len(location) == 0:
            # If there is no location found in hash table: Key doesnt exist
            raise KeyError('Key doesnt exist')
        return location

    def __contains__(self, key: K) -> bool:
        """
        Checks to see if the given key is in the Hash Table

        :complexity: See linear probe.
        """
        try:
            _ = self[key]
        except KeyError:
            return False
        else:
            return True
