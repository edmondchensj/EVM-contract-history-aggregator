# Converts paths with loops to no-loop paths. 
# Path terminates upon reaching a visited node (loop) or the end of the entire original path.
from pprint import pprint
import json

def preprocess(input_paths):
    """ Convert paths with loop to no-loop paths.

    Input: list of ints
    Output: list of list of ints
    """
    new_paths = []

    for path in input_paths:
        visited = []

        for node in path:

            if node in visited: # Loop found
                # Terminate path and add to new_paths
                new_path = visited + [node]
                new_paths.append(new_path)

                # Unwind visited nodes
                node_idx = visited.index(node)
                visited = visited[:node_idx+1]
            else:
                visited.append(node)

        # Add completed path to new_paths
        new_paths.append(visited)

    return new_paths


def main():

    input_paths = [[1,2,3,4,2,3,4,5,7,8,5,6,8,9],[1,2,3,10,11,12,10,11,12,13]]

    print("Input paths are: ")
    pprint(input_paths)

    new_paths = preprocess(input_paths)
    
    print("Final output paths are: ")
    pprint(new_paths)

if __name__ == "__main__":
    main()