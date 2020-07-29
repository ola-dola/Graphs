from util import Queue


def earliest_ancestor(ancestors, starting_node):        # Solved using BFS
    # Counter keeps track of how many genrations from starting node
    counter = 0

    qq = Queue()
    # Enqueue tuple (x,y). x => generation, y => node/value
    qq.enqueue((counter, starting_node))
    # Track the ancestor level/generations using (x,y)
    # Ancestor at each level/generation could be more than one.
    # Arrays keep track of those, and return computation done later(get lowest).
    ancestor_tracker = [(0, starting_node)]

    while qq.size() > 0:
        curr_node = qq.dequeue()

        # if curr x is greater than old x, replace with new array.
        # New level now 😉
        if curr_node[0] > ancestor_tracker[0][0]:
            ancestor_tracker = [curr_node]

        # if curr_node val is still at same gen/level, and
        # the val is not what is already in the tracker. It happens sometimes
        # because the counter is yet to be incremented at this point
        # (Hnt:line14&17)
        if curr_node[0] == ancestor_tracker[0][0] and curr_node[1] != ancestor_tracker[-1][1]:
            ancestor_tracker.append(curr_node)

        # Increment before loop, so if found, the right count is used.
        counter += 1
        for ancestor in ancestors:
            # If cur_node[y], the val(read child) is found in descendants
            # location in ancestor (anc..[1]), add the position 0
            # (ancestor/parent) and generation(counter) to queue.
            if curr_node[1] == ancestor[1]:
                qq.enqueue((counter, ancestor[0]))

    if len(ancestor_tracker) == 1:
        if ancestor_tracker[0][1] == starting_node:  # Ancestor not found
            return -1

        return ancestor_tracker[0][1]   # Only ancestor at level/gen
    else:   # More than one at level, so find minimum
        min_val = ancestor_tracker[0][1]

        for value in ancestor_tracker:
            if value[1] < min_val:
                min_val = value[1]

        return min_val


# data = [(1, 3), (2, 3), (3, 6), (5, 6), (5, 7),
#         (4, 5), (4, 8), (8, 9), (11, 8), (10, 1)]

# print(earliest_ancestor(data, 6))
