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

        self.array:ArrayR[tuple[K, V]] = ArrayR(self.TABLE_SIZE)
        self.count = 0
        self.level = 0
        self.table = ArrayR(self.TABLE_SIZE)

    def hash(self, key: K) -> int:
        if self.level < len(key):
            return ord(key[self.level]) % (self.TABLE_SIZE-1)
        return self.TABLE_SIZE-1

    def __getitem__(self, key: K) -> V:
        """
        Get the value at a certain key

        :raises KeyError: when the key doesn't exist.
        """
        tracking = LinkedStack()
        tracking.push(self.table)
        location = self.get_location(key)
        print(location)
        for i in range(len(location)-1):
            cur = tracking.pop()
            for j in range(self.TABLE_SIZE):
                if j == location[i]:
                    tracking.push(cur[j][1])
                    break
        value = tracking.peek()[location[-1]][0][1]
        return value

    def __setitem__(self, key: K, value: V) -> None:
        """
        Set an (key, value) pair in our hash table.
        """
        self.count += 1
        self.level = 0
        # Create a storage of unallocated item
        item_store = LinkedStack()
        # Create a tracking of all went-through location 
        tracking = LinkedStack()
        #char_count = 1
        pos = self.hash(key)
        item_store.push([key,value,pos])
        tracking.push(self.table)
        while (item_store.is_empty() == False):
            item = item_store.pop()
            cur = tracking.peek()
            item[2] = self.hash(item[0])
            if cur[item[2]] == None:

                cur[item[2]] = []
                cur[item[2]].append(item)
            else:
                if len(cur[item[2]]) == 2:

                    tracking.push(cur[item[2]][1])
                    item_store.push(item)
                    self.level += 1
                else:

                    item2 = cur[item[2]][0]
                    item_store.push(item)
                    item_store.push(item2)
                    char_count = self.level + 1
                    dict_item = [item[0][0:char_count],0,item[2]]
                    # print("Same")
                    # print(item[0],item2[0])
                    # print(dict_item)
                    self.level += 1
                    # Create new hash table at current collided cell
                    cur[item[2]].append(ArrayR(self.TABLE_SIZE))
                    cur[item[2]][0] = (dict_item)
                    tracking.push(cur[item[2]][1])
        return


    def __delitem__(self, key: K) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.
        """
        self.count -= 1
        location = self.get_location(key)
        tracking = LinkedStack()
        tracking.push(self.table)
        # Push all tables' location to Stack, from parent table to table containing key
        for i in range(len(location)-1):
           # Get current table location
           cur = tracking.peek()
           tracking.push(cur[location[i]][1])

        # Delete item at its location
        tracking.peek()[location[-1]] = None
        # If deleted item is in parent table: Do nothing
        if len(location) == 1:
            return
        
        else:
            # Check if there is any item left in hash table
            for k in range(len(location)-1):
                cur = tracking.pop()
                element_count = 0   
                for j in range(self.TABLE_SIZE):
                    if cur[j] is not None:
                        if (cur[j][0][1] != 0) and (cur[j][0][0] != key):
                            item = cur[j][0]
                            element_count += 1
                if element_count == 1:
                    # Previous table location
                    prev = tracking.peek()
                    #print(location[len(location) - k - 1])
                    #print(prev[location[len(location) - k - 1]])
                    prev[location[-1 -k - 1]][0] = item
                    
                    cur = None
    
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

        :raises KeyError: when the key doesn't exist.
        """
        
        location = []
        tracking = LinkedStack()
        tracking.push(self.table)
        found = False
        char_count = 1
        while (tracking.is_empty() == False):
            cur = tracking.pop()
            for i in range(self.TABLE_SIZE):
                if cur[i] is not None:
                    if (key == cur[i][0][0]) & (cur[i][0][1] != 0):
                        found = True
                        location.append(i)
                        return location
                    if key[0:char_count] == cur[i][0][0]:
                        tracking.push(cur[i][1])
                        char_count += 1
                        location.append(i)
        if len(location) == 0:
            # If there is no key in hash table
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
