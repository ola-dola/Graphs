from room import Room
from player import Player
from world import World
from stack import Stack

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
# world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
traversal_graph = {}
stack = Stack()

while len(traversal_graph) < len(room_graph):
    room_id = player.current_room.id
    room_exits = player.current_room.get_exits()

    if room_id not in traversal_graph:
        # Build the graph, adding exits.
        traversal_graph[room_id] = {exit: "?" for exit in room_exits}

    if "n" in traversal_graph[room_id] and traversal_graph[room_id]["n"] == "?":
        # Get room up North.
        room_in_north = player.current_room.get_room_in_direction("n")
        room_in_north_id = room_in_north.id
        room_in_north_exits = room_in_north.get_exits()

        traversal_graph[room_id]["n"] = room_in_north_id

        # If room in north not in graph yet, add and build it's exits
        if room_in_north.id not in traversal_graph:

            traversal_graph[room_in_north_id] = {
                exit: "?" for exit in room_in_north_exits}

            traversal_graph[room_in_north_id]["s"] = room_id
        else:
            # If it already is, assign it's south to current room
            traversal_graph[room_in_north_id]["s"] = room_id
        # Make the trip, and append your path
        player.travel("n")
        traversal_path.append("n")
        # Add opposite dir to stack, so we can walk back from dead end.
        stack.push("s")
    elif "s" in traversal_graph[room_id] and traversal_graph[room_id]["s"] == "?":
        # Get room down south.
        room_in_south = player.current_room.get_room_in_direction("s")
        room_in_south_id = room_in_south.id
        room_in_south_exits = room_in_south.get_exits()

        traversal_graph[room_id]["s"] = room_in_south_id

        # If room in south not in graph yet, add and build it's exits
        if room_in_south.id not in traversal_graph:
            traversal_graph[room_in_south_id] = {
                exit: "?" for exit in room_in_south_exits}

            traversal_graph[room_in_south_id]["n"] = room_id
        else:
            # If it already is, assign it's north to current room
            traversal_graph[room_in_south_id]["n"] = room_id
        # Make the trip, and append your path
        player.travel("s")
        traversal_path.append("s")
        # Add opposite dir to stack, so we can walk back from dead end.
        stack.push("n")

    elif "e" in traversal_graph[room_id] and traversal_graph[room_id]["e"] == "?":
        # Get room in East.
        room_in_east = player.current_room.get_room_in_direction("e")
        room_in_east_id = room_in_east.id
        room_in_east_exits = room_in_east.get_exits()

        traversal_graph[room_id]["e"] = room_in_east_id

        # If room in east not in graph yet, add and build it's exits
        if room_in_east.id not in traversal_graph:
            traversal_graph[room_in_east_id] = {
                exit: "?" for exit in room_in_east_exits}
            traversal_graph[room_in_east_id]["w"] = room_id
        else:
            # If it already is, assign it's west to current room
            traversal_graph[room_in_east_id]["w"] = room_id
        # Make the trip, and append your path
        player.travel("e")
        traversal_path.append("e")
        # Add opposite dir to stack, so we can walk back from dead end.
        stack.push("w")

    elif "w" in traversal_graph[room_id] and traversal_graph[room_id]["w"] == "?":
        # Get room in west.
        room_in_west = player.current_room.get_room_in_direction("w")
        room_in_west_id = room_in_west.id
        room_in_west_exits = room_in_west.get_exits()

        traversal_graph[room_id]["w"] = room_in_west_id

        # If room in west not in graph yet, add and build it's exits
        if room_in_west.id not in traversal_graph:
            traversal_graph[room_in_west_id] = {
                exit: "?" for exit in room_in_west_exits}
            traversal_graph[room_in_west_id]["e"] = room_id
        else:
            # If it already is, assign it's east to current room
            traversal_graph[room_in_west_id]["e"] = room_id
        # Make the trip, and append your path
        player.travel("w")
        traversal_path.append("w")
        # Add opposite dir to stack, so we can walk back from dead end.
        stack.push("e")

    elif "e" in traversal_graph[room_id] and traversal_graph[room_id]["e"] == "?":
        # Get room in East.
        room_in_east = player.current_room.get_room_in_direction("e")
        room_in_east_id = room_in_east.id
        room_in_east_exits = room_in_east.get_exits()

        # If room in east not in graph yet, add and build it's exits
        if room_in_east.id not in traversal_graph:
            traversal_graph[room_in_east_id] = {
                exit: "?" for exit in room_in_east_exits}
        # else:
            # If it already is, assign it's west to current room
        traversal_graph[room_in_east_id]["w"] = room_id
        # Make the trip, and append your path
        player.travel("e")
        traversal_path.append("e")
        # Add opposite dir to stack, so we can walk back from dead end.
        stack.push("w")
    else:
        last_room_dir = stack.pop()
        if last_room_dir is None:
            break
        player.travel(last_room_dir)

        traversal_path.append(last_room_dir)

# print(traversal_graph)
# print(traversal_path)


# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
