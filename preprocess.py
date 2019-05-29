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

def preprocess_with_nonce(path_with_nonce):
    """ Convert paths with loops to no-loop paths 
    Input: list of (mutable) tuples e.g. [[nonce, pc], [...]] 
    Output: list of list of tuples of type (nonce, pc)
    """
    new_paths = []

    visited = []
    visited_pcs = []

    for (nonce, pc) in path_with_nonce:
        if pc in visited_pcs: # Loop found
            # Terminate path and add to new_paths
            new_path = visited + [(nonce, pc)]
            new_paths.append(new_path)

            # Unwind visited pcs
            node_idx = visited_pcs.index(pc)
            visited_pcs = visited_pcs[:node_idx+1]

            # Unwind visited nodes
            visited = visited[:node_idx+1]

        else:
            visited_pcs.append(pc)
            visited.append((nonce, pc))

    # Add completed path to new_paths
    new_paths.append(visited)

    return new_paths


def main():

    #input_paths = [[1,2,3,4,2,3,4,5,7,8,5,6,8,9],[1,2,3,10,11,12,10,11,12,13]]

    path_with_nonce = [[1,0],[8,11],[19,31],[24,42],[29,53],[34,64],[39,75],[44,489],[76,530],[81,536],[85,1520],[95,1660],[104,1678],[108,1810],[119,1292],[156,1826],[174,1849],[178,1853],[182,1859],[243,684],[253,848],[311,919],[331,944]]

    print("Input paths are: ")
    #pprint(input_paths)
    pprint(path_with_nonce)

    #new_paths = preprocess(input_paths)
    new_paths = preprocess_with_nonce(path_with_nonce)

    print("Final output paths are: ")
    pprint(new_paths)

if __name__ == "__main__":
    main()