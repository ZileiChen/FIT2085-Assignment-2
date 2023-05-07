from __future__ import annotations

import copy
from dataclasses import dataclass

from data_structures.linked_stack import LinkedStack
from data_structures.stack_adt import Stack
from mountain import Mountain

from typing import TYPE_CHECKING, Union

# Avoid circular imports for typing.
if TYPE_CHECKING:
    from personality import WalkerPersonality

@dataclass
class TrailSplit:
    """
    A split in the trail.
       ___path_top____
      /               \
    -<                 >-path_follow-
      \__path_bottom__/
    """

    path_top: Trail
    path_bottom: Trail
    path_follow: Trail

    def remove_branch(self) -> TrailStore:
        """Removes the branch, should just leave the remaining following trail."""
        return self.path_follow.store

@dataclass
class TrailSeries:
    """
    A mountain, followed by the rest of the trail

    --mountain--following--

    """

    mountain: Mountain
    following: Trail

    def remove_mountain(self) -> TrailStore: # Similarly to remove its either the current implementation or simple return Trail
        """Removes the mountain at the beginning of this series."""
        return self.following.store

    def add_mountain_before(self, mountain: Mountain) -> TrailStore:
        """Adds a mountain in series before the current one."""
        self.following = self
        self.mountain = mountain
        return self

    def add_empty_branch_before(self) -> TrailStore:
        """Adds an empty branch, where the current trailstore is now the following path."""
        # Contruct a new splitted trail containing a new branch & the old trail
        new_trail = TrailSplit(Trail(None),Trail(None),Trail(self))
        return new_trail

    def add_mountain_after(self, mountain: Mountain) -> TrailStore:
        """Adds a mountain after the current mountain, but before the following trail."""
        # Current mountain remains the same
        # The new following trail contain a new mountain & the old following trail
        new_following = Trail(TrailSeries(mountain,self.following))
        # Contruct a complete trail
        new_trail = TrailSeries(self.mountain,new_following)
        return new_trail

    def add_empty_branch_after(self) -> TrailStore:
        """Adds an empty branch after the current mountain, but before the following trail."""
        # Current mountain remains the same
        # Create a new following trail containing new branch & the old following trail
        new_following = Trail(TrailSplit(Trail(None),Trail(None),self.following))
        # Contruct a complete trail
        new_trail = TrailSeries(self.mountain,new_following)
        return new_trail

TrailStore = Union[TrailSplit, TrailSeries, None]

@dataclass
class Trail:

    store: TrailStore = None

    def add_mountain_before(self, mountain: Mountain) -> Trail:
        """Adds a mountain before everything currently in the trail."""
        return Trail(TrailSeries(mountain, self))

    def add_empty_branch_before(self) -> Trail:
        """Adds an empty branch before everything currently in the trail."""
        return Trail(TrailSplit(Trail(None), Trail(None), self))

    def follow_path(self, personality: WalkerPersonality) -> None:
        """Follow a path and add mountains according to a personality."""


        current_trail = self.store
        trail_stack = LinkedStack()
        isCompleted = False;

        while not isCompleted:
            if isinstance(current_trail, TrailSplit):
                trail_stack.push(current_trail)
                if personality.select_branch(current_trail.path_top, current_trail.path_bottom):
                    current_trail = current_trail.path_top.store
                else:
                    current_trail = current_trail.path_bottom.store
            if isinstance(current_trail, TrailSeries) or current_trail is None:
                if current_trail is None:
                    current_trail = trail_stack.pop()
                    current_trail = current_trail.path_follow.store
                else:
                    personality.add_mountain(current_trail.mountain)
                    if current_trail.following.store is None:
                        if not trail_stack.is_empty():
                            current_trail = trail_stack.pop()
                            current_trail = current_trail.path_follow.store
                        else:
                            current_trail = current_trail.following.store
                    else:
                        current_trail = current_trail.following.store


            if current_trail is None and trail_stack.is_empty():
                isCompleted = True



    def collect_all_mountains(self) -> list[Mountain]:
        """Returns a list of all mountains on the trail."""
        raise NotImplementedError()

    def length_k_paths(self, k) -> list[list[Mountain]]: # Input to this should not exceed k > 50, at most 5 branches.
        """
        Returns a list of all paths of containing exactly k mountains.
        Paths are represented as lists of mountains.

        Paths are unique if they take a different branch, even if this results in the same set of mountains.
        """
        raise NotImplementedError()
