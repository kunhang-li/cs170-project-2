import math
import time

def load_data(filename):
    """
    read data from the file
    each row uses following format:
    class_label feature1 feature2 ... featureN
    """
    data = []
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                row = [float(x) for x in line.split()]
                " split the sting by empty and transform the string to the float "
                data.append(row)
    return data

def leave_one_out_accuracy(data, feature_set):
    """
    compute the accuracy by using the 1-Nearest with leave-one-out validation. feature_set uses feature numbers starting from 1.
    column 0 is the class label
    """

    if len(feature_set) == 0:
        return 0.0
    correctly = 0
    total_data = len(data)

    for i in range (total_data):
        object_to_classify = data[i]
        label = object_to_classify[0]

        nearest_neighbor_label = None
        nearest_neighbor_distance = float('inf')
        for k in range(total_data):
            if k != i:
                distance = 0.0

                for feature in feature_set:
                    diff = object_to_classify[feature] - data[k][feature]
                    distance += diff ** 2
                    "(x - y) ^ 2"

                distance = math.sqrt(distance)

                if distance < nearest_neighbor_distance:
                    nearest_neighbor_label = data[k][0]
                    nearest_neighbor_distance = distance

        if label == nearest_neighbor_label:
            correctly = correctly + 1

    accuracy = correctly / total_data
    return accuracy

def format_feature_set(feature):
    """
     Format feature set like {1, 3, 5}

    """
    if not feature:
        return "{}"
    return "{" + ", ".join(str(f) for f in sorted(feature)) + "}"

def forward_selection(data, num_features):
    print("Beginning search with Forward Selection")

    current = []
    best_set =[]
    "The best feature during the search"
    best_accuracy = 0.0
    "The best accuracy during the search"

    for level in range (1, num_features + 1):
        "add feature when find"
        current_feature = None
        "The best feature to be add"
        current_best_accuracy = 0.0
        "The best accuracy now it have"

        for feature in range (1, num_features + 1):
            if feature not in current:
                candidate = current + [feature]
                candidate.sort()

                accuracy = leave_one_out_accuracy(data, candidate)

                print(f"\t Using feature(s) {format_feature_set(candidate)}"f"accuracy is {accuracy * 100:.2f}%")

                if accuracy > current_best_accuracy:
                    current_best_accuracy = accuracy
                    current_feature = feature

        if current_feature is not None:
            current.append(current_feature)
            current.sort()

            print()
            print(f"Feature set {format_feature_set(current)} was best, "f"accuracy is {current_best_accuracy * 100:.2f}%\n")

            if current_best_accuracy > best_accuracy:
                "If the new result is better than history, renew it"

                best_accuracy = current_best_accuracy
                best_set = current[:]

            else:
                print("(Warning, Accuracy has decreased! Continuing search in case of local maxima)\n")
    print(f"Finished search!! The best feature subset is {format_feature_set(best_set)}, "f"which has an accuracy of { best_accuracy * 100:.2f}%\n")

def backward_elimination(data, num_features):
    print("Beginning search using Backward Elimination.\n")

    current = list(range(1, num_features + 1))
    best_set = current[:]
    best_accuracy = leave_one_out_accuracy(data, current)
    "calculate the accuracy that with all features"

    while len(current) > 1:
        current_feature_moved = None
        current_accuracy = 0.0
        best_candidate = current[:]
        "record data after deletion"

        for feature in current:
            candidate = current[:]
            candidate.remove(feature)

            accuracy = leave_one_out_accuracy(data, candidate)
            "calculate the accuracy after delete candidate feature"

            print(f"\tUsing feature(s) {format_feature_set(candidate)} "
                  f"accuracy is {accuracy * 100:.2f}%")

            if accuracy > current_accuracy:
                current_accuracy = accuracy
                current_feature_moved = feature
                best_candidate = candidate[:]

        if current_feature_moved is not None:
            current = best_candidate[:]

            print()
            print(f"Feature set {format_feature_set(current)} was best, "
                  f"accuracy is {current_accuracy * 100:.2f}%\n")

            if current_accuracy > best_accuracy:
                best_accuracy = current_accuracy
                best_set = current[:]
            else:
                print("(Warning, Accuracy has decreased! Continuing search in case of local maxima)\n")
        else:
            break

    print(f"Finished search!! The best feature subset is {format_feature_set(best_set)}, "
          f"which has an accuracy of {best_accuracy * 100:.2f}%\n")

def main():
    print("Welcome to Kunhang Li's Feature Selection Algorithm.\n")

    filename = input("Type in the test file name: ").strip()
    data = load_data(filename)

    total_data = len(data)
    features = len(data[0]) - 1

    print(f"\nThis dataset has {features} features (not including the class attribute), "
          f"with {total_data} instances.\n")

    all_features = list(range(1, features + 1))
    all_accuracy = leave_one_out_accuracy(data, all_features)

    print(f'Running nearest neighbor with all {features} features, using '
          f'"leave-one-out" evaluation, I get an accuracy of {all_accuracy * 100:.2f}%\n')

    print("Type the number of the algorithm you want to run.")
    print("1) Forward Selection")
    print("2) Backward Elimination")
    choice = input("Enter your choice: ").strip()

    print()

    start_time = time.time()

    if choice == '1':
        forward_selection(data, features)
    elif choice == '2':
        backward_elimination(data, features)
    else:
        print("Invalid choice. Please run the program again and enter 1 or 2.")
        return

    end_time = time.time()
    print(f"Total runtime: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    main()