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
    TABLE_SIZES = [5, 13, 29, 53, 97, 193, 389, 769, 1543, 3079, 6151, 12289, 24593, 49157, 98317, 196613, 393241,
                   786433, 1572869]

    HASH_BASE = 31

    def __init__(self, sizes: list | None = None, internal_sizes: list | None = None) -> None:
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

        self.table = ArrayR(self.TABLE_SIZES[self.size_index])
        for i in range(self.TABLE_SIZES[self.size_index]):
            self.table[i] = ArrayR(self.INTERNAL_TABLE_SIZES[self.internal_size_index])
        """
        self.table = None
        # self.table = LinearProbeTable(sizes)
        # self.table.hash = lambda k: self.hash1(k)
        self.internal_sizes = internal_sizes
        self.sizes = sizes


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
        if self.table is None:
            self.table = LinearProbeTable(self.sizes)
            self.table.hash = lambda k: self.hash1(k)


        outer_pos = self.table._linear_probe(key1, is_insert)
        sub_data = self.table.array[outer_pos]

        if sub_data is None:
            if is_insert:
                self.table.array[outer_pos] = [key1, LinearProbeTable(self.internal_sizes)]
                sub_table = self.table.array[outer_pos][1]
                sub_table.hash = lambda k: self.hash2(k, sub_table)
                inner_pos = sub_table._linear_probe(key2, is_insert)
            else:
                raise KeyError(key1)
        else:
            sub_table = self.table.array[outer_pos][1]
            inner_pos = sub_table._linear_probe(key2, is_insert)
        return (outer_pos, inner_pos)

        # # Initial position outer table
        # position_outer = self.hash1(key1)
        # check_outer = True
        # for _ in range(self.table.table_size):
        #     if self.table.table[position_outer][0] is None:
        #         # Empty spot. Am I upserting or retrieving?
        #         if is_insert:
        #             check_outer = False
        #         else:
        #             raise KeyError(key1)
        #     elif self.table.table[position_outer][0] == key1:
        #         check_outer = False
        #     else:
        #         # Taken by something else. Time to linear probe.
        #         position_outer = (position_outer + 1) % self.table.table_size
        #
        # if check_outer:
        #     if is_insert:
        #         raise FullError("Table is full!")
        #     else:
        #         raise KeyError(key1)
        #
        #
        # # Initial position inner table
        # hashtable_inner = self.table.table[position_outer][1]
        # position_inner = self.hash2(key2, hashtable_inner)
        # check_inner = True
        # for _ in range(hashtable_inner.table_size):
        #     if hashtable_inner.table[position_inner] is None:
        #         # Empty spot. Am I upserting or retrieving?
        #         if is_insert:
        #             check_inner = False
        #         else:
        #             raise KeyError(key2)
        #     elif hashtable_inner.table[position_inner][0] == key2:
        #         check_inner = False
        #     else:
        #         # Taken by something else. Time to linear probe.
        #         position_inner = (position_inner + 1) % hashtable_inner.table_size
        #
        # if check_inner:
        #     if is_insert:
        #         raise FullError("Table is full!")
        #     else:
        #         raise KeyError(key2)
        #
        # return (position_outer, position_inner)
        #

    def iter_keys(self, key: K1 | None = None) -> Iterator[K1 | K2]:
        """
        key = None:
            Returns an iterator of all top-level keys in hash table
        key = k:
            Returns an iterator of all keys in the bottom-hash-table for k.
        """
        return DoubleKeyTableIterKeys(self, key)

    def keys(self, key: K1 | None = None) -> list[K1]:
        """
        key = None: returns all top-level keys in the table.
        key = x: returns all bottom-level keys for top-level key x.
        """
        result = []
        if key is None:
            for i in range(self.table.table_size):
                if self.table.array[i] is not None:
                    if self.table.array[i][0] is not None:
                        result.append(self.table.array[i][0])
            return result
        position = self.table._linear_probe(key, False)
        sub_table = self.table.array[position][1]
        for i in range(sub_table.table_size):
            if sub_table.array[i] is not None:
                if sub_table.array[i][0] is not None:
                    result.append(sub_table.array[i][0])
        return result

    def iter_values(self, key: K1 | None = None) -> Iterator[V]:
        """
        key = None:
            Returns an iterator of all values in hash table
        key = k:
            Returns an iterator of all values in the bottom-hash-table for k.
        """
        return DoubleKeyTableIterValues(self, key)

    def values(self, key: K1 | None = None) -> list[V]:
        """
        key = None: returns all values in the table.
        key = x: returns all values for top-level key x.
        """
        result = []
        if key is None:
            for i in range(self.table.table_size):
                if self.table.array[i] is not None:
                    if self.table.array[i][1] is not None:
                        sub_table = self.table.array[i][1]
                        for j in range(sub_table.table_size):
                            if sub_table.array[j] is not None:
                                result.append(sub_table.array[j][1])
            return result
        position = self.table._linear_probe(key, False)
        sub_table = self.table.array[position][1]
        for i in range(sub_table.table_size):
            if sub_table.array[i] is not None:
                if sub_table.array[i][0] is not None:
                    result.append(sub_table.array[i][1])
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
        positions = self._linear_probe(key[0], key[1], False)
        pos1 = positions[0]
        pos2 = positions[1]
        return self.table.array[pos1][1].array[pos2][1]

    def __setitem__(self, key: tuple[K1, K2], data: V) -> None:
        """
        Set an (key, value) pair in our hash table.
        """
        positions = self._linear_probe(key[0], key[1], True)
        pos1 = positions[0]
        pos2 = positions[1]

        if self.table.array[pos1][1].is_empty():
            self.table.array[pos1][0] = key[0]
            self.table.count += 1

        if self.table.array[pos1][1].array[pos2] is None:
            self.table.array[pos1][1].array[pos2] = (key[1], data)
            self.table.array[pos1][1].count += 1

        sub_table = self.table.array[pos1][1]
        if len(sub_table) > sub_table.table_size/ 2:
            sub_table._rehash()

        if len(self.table) > self.table_size / 2:
            self.table._rehash()

    def __delitem__(self, key: tuple[K1, K2]) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.
        """
        # First delete the item in the inner hash table and shuffle cluster back
        positions = self._linear_probe(key[0], key[1], False)
        pos1 = positions[0]
        pos2 = positions[1]
        sub_table = self.table.array[pos1][1]
        del sub_table[key[1]]

        # If inner hash table is empty, delete outer key
        if sub_table.is_empty():
            del self.table[key[0]]


        # # First delete the item in the inner hash table
        # positions = self._linear_probe(key[0], key[1], False)
        # pos1 = positions[0]
        # pos2 = positions[1]
        # self.table.array[pos1][1].array[pos2] = None
        #
        # # Shuffle the cluster back
        # sub_table = self.table.array[pos1][1]
        # pos2 = (pos2 + 1) % sub_table.table_size
        # while sub_table.array[pos2] is not None:
        #     key2, value = sub_table.array[pos2]
        #     sub_table.array[pos2] = None
        #     # Reinsert.
        #     sub_table.hash = lambda k: self.hash2(k, sub_table)
        #     newpos = sub_table._linear_probe(key2, True)
        #     sub_table.array[newpos] = (key2, value)
        #     pos2 = (pos2 + 1) % sub_table.table_size
        #
        # # If no elements left in the inner hash table, delete the inner hash table
        # if sub_table.is_empty():
        #     self.table.array[pos1] = None
        #
        # # Shuffle the outer cluster


    def _rehash(self) -> None:
        """
        Need to resize table and reinsert all values

        :complexity best: O(N*hash(K)) No probing.
        :complexity worst: O(N*hash(K) + N^2*comp(K)) Lots of probing.
        Where N is len(self)
        """
        raise NotImplementedError()

    @property
    def table_size(self) -> int:
        """
        Return the current size of the table (different from the length)
        """
        return len(self.table.array)

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


"""
i think an iterator class is required to complete iterators
"""


class DoubleKeyTableIterKeys:

    def __init__(self, double_key_table: DoubleKeyTable, key: K1 | None = None):
        self.count = 0
        self.all_keys = double_key_table.keys(key)
        self.max_count = len(self.all_keys)

    def __iter__(self):
        return self

    def __next__(self):
        found = False
        while not found:
            if self.count < self.max_count:
                self.count += 1
                return self.all_keys[self.count]
                found = True
            else:
                found = True
        raise StopIteration


class DoubleKeyTableIterValues:

    def __init__(self, double_key_table: DoubleKeyTable, key: K1 | None = None):
        self.count = 0
        self.all_values = double_key_table.values(key)
        self.max_count = len(self.all_values)


    def __iter__(self):
        return self

    def __next__(self):
        found = False
        while not found:
            if self.count < self.max_count:
                self.count += 1
                return self.all_values[self.count]
                found = True
            else:
                found = True
        raise StopIteration
