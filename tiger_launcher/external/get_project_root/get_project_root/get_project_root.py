import sys
import os
from typing import Set
import inspect


class NoPossibleRootsFound(Exception):
    def __init__(self):
        self.message = "Found no possible ancestor roots in sys.path!"
        super().__init__(self.message)


def does_file_path_contain_path_component(cur_file_dir: str):
    cur_file_components = os.path.normpath(cur_file_dir).split(os.sep)
    possible_roots = set()
    for path in sys.path:
        possible_root_dir = True
        for cur_file_comp, comp in zip(cur_file_components, os.path.normpath(path).split(os.sep)):
            if cur_file_comp != comp:
                possible_root_dir = False
        if possible_root_dir:
            possible_roots.add(path)
    if len(possible_roots) <= 0:
        raise NoPossibleRootsFound()
    return possible_roots


def shortest_possible_root(possible_roots: Set[str]):
    shortest_root_len = None
    shortest_root = None
    for root in possible_roots:
        comps = os.path.normpath(root).split(os.sep)
        comp_len = len(comps)
        if shortest_root_len is None or comp_len < shortest_root_len:
            shortest_root_len = comp_len
            shortest_root = root
    if shortest_root is None:
        raise NoPossibleRootsFound()
    return shortest_root


def root_path(ignore_cwd=False):
    """
    :param ignore_cwd: ignore the current working directory for deriving the root path
    :return returns project root path:
    :rtype: str
    """
    filename = os.path.abspath(inspect.stack()[1][0].f_code.co_filename)
    cur_file_dir = os.path.dirname(filename)
    if not ignore_cwd and cur_file_dir == os.path.abspath(os.getcwd()):
        return cur_file_dir
    possible_roots = does_file_path_contain_path_component(cur_file_dir)
    return shortest_possible_root(possible_roots)


if __name__ == '__main__':
    res = root_path()
    print(res)

