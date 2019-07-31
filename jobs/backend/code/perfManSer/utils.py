import time
from datetime import (date, datetime)

def string2days(s, format="%Y-%m-%d"):
    if s:
        return datetime.strptime(s, format).date()
    else:
        return -1

def walk_tree_bf(node, visit):
    """Breadth-first (level order)."""
    to_visit = [node]
    while to_visit:
        new_to_visit = []
        for node in to_visit:
            visit(node)
            new_to_visit.extend(node.children)
        to_visit = new_to_visit