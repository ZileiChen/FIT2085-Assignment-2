from __future__ import annotations

from typing import Generic, TypeVar, Iterator
from data_structures.hash_table import LinearProbeTable, FullError
from data_structures.referential_array import ArrayR

K1 = TypeVar('K1')
K2 = TypeVar('K2')
V = TypeVar('V')

class DoubleKeyTable(Generic[K1, K2, V]):
    """
    Double Hash Table.

    Type Arguments:
        - K1:   1st Key Type. In most cases should be string.
                Otherwise `hash1` should be overwritten.
        - K2:   2nd Key Type. In most cases should be string.
                Otherwise `hash2` should be overwritten.
        - V:    Value Type.

    Unless stated otherwise, all methods have O(1) complexity.
    """

    # No test case should exceed 1 million entries.
    TABLE_SIZES = [5, 13, 29, 53, 97, 193, 389, 769, 1543, 3079, 6151, 12289, 24593, 49157, 98317, 196613, 393241, 786433, 1572869]

    HASH_BASE = 31

    def __init__(self, sizes:list|None=None, internal_sizes:list|None=None) -> None:
        # Creates a double has table with dimensions sizes*internal_sizes
        """
        check if sizes and internal sizes are none
        if they are none, then use the default list for both internal and outer

        """

        """
        self.INTERNAL_TABLE_SIZES = self.TABLE_SIZES
        if sizes is not None:
            self.TABLE_SIZES = sizes
        if internal_sizes is not None:
            self.INTERNAL_TABLE_SIZES = internal_sizes
        self.size_index = 0
        self.internal_size_index = 0

        self.array = ArrayR(self.TABLE_SIZES[self.size_index])
        for i in range(self.TABLE_SIZES[self.size_index]):
            self.array[i] = ArrayR(self.INTERNAL_TABLE_SIZES[self.internal_size_index])
        """

        # not sure which implementation is better, but i think it should be the one below
        # im not too sure
        self.array = LinearProbeTable(sizes)
        for i in range(len(self.array)):
            self.array[i][1] = LinearProbeTable(internal_sizes) # index: [position][key/value], where value is another hashmap

    def hash1(self, key: K1) -> int:
        """
        Hash the 1st key for insert/retrieve/update into the hashtable.

        :complexity: O(len(key))
        """

        value = 0
        a = 31415
        for char in key:
            value = (ord(char) + a * value) % self.table_size
            a = a * self.HASH_BASE % (self.table_size - 1)
        return value

    def hash2(self, key: K2, sub_table: LinearProbeTable[K2, V]) -> int:
        """
        Hash the 2nd key for insert/retrieve/update into the hashtable.

        :complexity: O(len(key))
        """

        value = 0
        a = 31415
        for char in key:
            value = (ord(char) + a * value) % sub_table.table_size
            a = a * self.HASH_BASE % (sub_table.table_size - 1)
        return value

    def _linear_probe(self, key1: K1, key2: K2, is_insert: bool) -> tuple[int, int]:
        """
        Find the correct position for this key in the hash table using linear probing.

        :raises KeyError: When the key pair is not in the table, but is_insert is False.
        :raises FullError: When a table is full and cannot be inserted.
        """
        outer_pos = self.hash1(key1)
        sub_table = self.array[outer_pos]
        inner_pos = self.hash2(key2, sub_table)

        for _ in range(self.table_size):
            if self.array[outer_pos][1][inner_pos] is None:
                if is_insert:
                    return inner_pos
                else:
                    raise KeyError(key1, key2)
            elif self.array[outer_pos][1][inner_pos][0] == key2:
                return inner_pos
            else:
                # Taken by something else. Time to linear probe.
                inner_pos = (inner_pos + 1) % self.array[outer_pos][1].table_size

        if is_insert:
            raise FullError("Table is full!")
        else:
            raise KeyError(key1, key2)

    def iter_keys(self, key:K1|None=None) -> Iterator[K1|K2]:
        """
        key = None:
            Returns an iterator of all top-level keys in hash table
        key = k:
            Returns an iterator of all keys in the bottom-hash-table for k.
        """
        raise NotImplementedError()

    def keys(self, key:K1|None=None) -> list[K1]:
        """
        key = None: returns all top-level keys in the table.
        key = x: returns all bottom-level keys for top-level key x.
        """
        # not sure if list is allowed here
        result = list
        if key is None:
            for i in range(len(self.array)):
                if self.array[i][0] is not None:
                    result.append(self.array[i][0])
            return result
        position = self.hash1(key)
        for i in range(len(self.array[position][0])):
            if self.array[position][1][i][0] is not None:
                result.append(self.array[position][1][i][0])
        return result



    def iter_values(self, key:K1|None=None) -> Iterator[V]:
        """
        key = None:
            Returns an iterator of all values in hash table
        key = k:
            Returns an iterator of all values in the bottom-hash-table for k.
        """
        raise NotImplementedError()

    def values(self, key:K1|None=None) -> list[V]:
        """
        key = None: returns all values in the table.
        key = x: returns all values for top-level key x.
        """
        # not sure if list is allowed here
        result = list
        if key is None:
            for i in range(len(self.array)):
                if self.array[i][0] is not None:
                    result.append(self.array[i][1])
            return result
        position = self.hash1(key)
        for i in range(len(self.array[position][0])):
            if self.array[position][1][i][0] is not None:
                result.append(self.array[position][1][i][1])
        return result

    def __contains__(self, key: tuple[K1, K2]) -> bool:
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

    def __getitem__(self, key: tuple[K1, K2]) -> V:
        """
        Get the value at a certain key

        :raises KeyError: when the key doesn't exist.
        """
        raise NotImplementedError()

    def __setitem__(self, key: tuple[K1, K2], data: V) -> None:
        """
        Set an (key, value) pair in our hash table.
        """

        raise NotImplementedError()

    def __delitem__(self, key: tuple[K1, K2]) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.
        """
        raise NotImplementedError()

    def _rehash(self) -> None:
        """
        Need to resize table and reinsert all values

        :complexity best: O(N*hash(K)) No probing.
        :complexity worst: O(N*hash(K) + N^2*comp(K)) Lots of probing.
        Where N is len(self)
        """
        raise NotImplementedError()

    def table_size(self) -> int:
        """
        Return the current size of the table (different from the length)
        """
        raise NotImplementedError()

    def __len__(self) -> int:
        """
        Returns number of elements in the hash table
        """
        raise NotImplementedError()

    def __str__(self) -> str:
        """
        String representation.

        Not required but may be a good testing tool.
        """
        raise NotImplementedError()
