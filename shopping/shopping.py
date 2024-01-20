import csv
import sys
import calendar

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """

    # Read data in from file
    with open(filename) as f:
        reader = csv.DictReader(f)

        evidence = []
        labels = []

        for row in reader:
            inner = []

            # Convert all values to numeric
            for key, value in list(row.items())[:17]:
                if key == "Administrative_Duration" or key == "Informational_Duration" or key == "ProductRelated_Duration" or key == "BounceRates" or key == "ExitRates" or key == "PageValues" or key == "SpecialDay":
                    inner.append(float(value))

                elif key == "VisitorType":
                    if value == "Returning_Visitor":
                        inner.append(1)
                    else:
                        inner.append(0)
                elif key == "Weekend":
                    if value == "FALSE":
                        inner.append(0)
                    else:
                        inner.append(1)
                elif key == "Month":
                    # conver the month name to the month number
                    if value == "June":
                        inner.append(5)
                    else:
                        inner.append(list(calendar.month_abbr).index(value)-1)
                else:
                    inner.append(int(value))

            evidence.append(inner)

            for key, value in list(row.items())[17:]:
                if key == "Revenue":
                    if value == "FALSE":
                        labels.append(0)
                    else:
                        labels.append(1)

        return (evidence, labels)


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    neigh = KNeighborsClassifier(n_neighbors=1)

    return neigh.fit(evidence, labels)


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """

    label_positive = 0
    label_negative = 0
    predict_positive = 0
    predict_negative = 0

    # Calculate true labels in in the testing set
    for i in range(len(labels)):
        if labels[i] == 1:
            label_positive += 1
            if predictions[i] == 1:
                predict_positive += 1
        else:
            label_negative += 1
            if predictions[i] == 0:
                predict_negative += 1

    sensitivity = float(predict_positive/label_positive)
    specificity = float(predict_negative/label_negative)

    return (sensitivity, specificity)


if __name__ == "__main__":
    main()
