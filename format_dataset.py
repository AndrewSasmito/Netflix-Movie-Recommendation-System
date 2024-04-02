import csv
import random


def create_formatted_dataset(file_path: str) -> None:
    """This function takes in the file of a csv file and saves a formatted version of it to
    data/shuffled_user_ratings.csv. This includes deleting the header of the file and shuffling
    the rest of the lines.

    Preconditions:
        - file_path is the file path of a csv file
    """
    with open(file_path, 'r') as read_file, open('data/shuffled_user_ratings.csv', 'w', newline='') as write_file:
        next(read_file)
        shuffled_values = list(csv.reader(read_file))
        random.shuffle(shuffled_values)
        csv.writer(write_file).writerows(shuffled_values)


def create_large_formatted_dataset(file_path: str) -> None:
    """This function takes in the file of a very large csv file and saves a formatted version of it to
    data/shuffled_user_ratings.csv. This includes deleting the header of the file and shuffling
    the rest of the lines. This is only to be used on functions with over a hundred million lines.

    Preconditions:
        - file_path is the file path of a csv file
        - file_path is the file path of a file with over a hundred million lines
    """
    with open(file_path, 'r') as read_file, open('data/shuffled_user_ratings.csv', 'w', newline='') as write_file:
        next(read_file)
        reader, writer = csv.reader(read_file), csv.writer(write_file)
        for i in range(10):
            values = []
            index = 0
            while index < 10000000:
                values.append(next(reader))
                index += 1

            random.shuffle(values)
            writer.writerows(values)

        values = []
        for line in reader:
            values.append(line)
        random.shuffle(values)
        writer.writerows(values)


if __name__ == "__main__":
    create_large_formatted_dataset('data/user_ratings.csv')
