#!/usr/bin/env python3

import csv
import sys
from pathlib import Path


def compute_average(csv_path: Path) -> float:
    grades = []

    with csv_path.open(newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        if not reader.fieldnames or "Grade" not in reader.fieldnames:
            raise ValueError("CSV must contain a 'Grade' column.")

        for row_number, row in enumerate(reader, start=2):
            grade_text = (row.get("Grade") or "").strip()
            if not grade_text:
                continue

            try:
                grades.append(float(grade_text))
            except ValueError as error:
                raise ValueError(
                    f"Invalid grade on row {row_number}: {grade_text!r}"
                ) from error

    if not grades:
        raise ValueError("No grades were found in the CSV.")

    return sum(grades) / len(grades)


def main() -> None:
    csv_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("grades.csv")

    try:
        average = compute_average(csv_path)
    except (FileNotFoundError, OSError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        raise SystemExit(1)

    print(f"Class average: {average:.2f}")


if __name__ == "__main__":
    main()
