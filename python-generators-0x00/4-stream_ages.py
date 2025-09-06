#!/usr/bin/env python3
"""
4-stream_ages.py

Objective:
- Use a generator to stream user ages row by row.
- Compute average age memory-efficiently without SQL AVG.
- Use no more than 2 loops total.
"""

import seed


def stream_user_ages():
    """
    Generator: yields ages from user_data one by one.
    Loop #1
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT age FROM user_data;")

    for row in cursor:  # Loop #1
        yield int(row["age"])

    cursor.close()
    connection.close()


def compute_average_age():
    """
    Consumes the generator and computes average age.
    Loop #2
    """
    total = 0
    count = 0

    for age in stream_user_ages():  # Loop #2
        total += age
        count += 1

    avg = total / count if count else 0
    print(f"Average age of users: {avg:.2f}")


if __name__ == "__main__":
    compute_average_age()
