# Converts paths with loops to no-loop paths. 
# Path terminates upon reaching a visited node (loop) or the end of the entire original path.
from pprint import pprint

def preprocess(input_paths):

    new_paths = []

    for path in input_paths:

        visited = []

        for node in path:

            if node in visited:
                # Terminate path and add to new_paths
                new_path = visited + [node]
                new_paths.append(new_path)

                # Unwind visited nodes
                node_idx = visited.index(node)
                visited = visited[:node_idx+1]
            else:
                visited += [node]

        # Add completed path to new_paths
        new_paths.append(visited)

    return new_paths


def main(input_paths):
    print("Input paths are: ")
    pprint(input_paths)

    new_paths = preprocess(input_paths)

    print("Final output paths are: ")
    pprint(new_paths)

if __name__ == "__main__":
    test_inputs = [[1,2,3,4,2,3,4,5,7,8,5,6,8,9],
                    [1,2,3,10,11,12,10,11,12,13]]
    main(test_inputs)