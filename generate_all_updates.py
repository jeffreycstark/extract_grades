#!/usr/bin/env python3
"""
Generate all UPDATE statements from CSV files for manual execution.
"""
import csv
import re
from pathlib import Path

def parse_filename_column(filename_value):
    """Parse filename to extract class and termid."""
    parts = filename_value.split('_')
    termid = parts[-1] if parts else None
    first_part = filename_value.split()[0] if ' ' in filename_value else filename_value.split('_')[0]
    class_code = first_part
    return class_code, termid

def get_class_pattern(class_code):
    """Get simple LIKE pattern for class code matching."""
    # Remove leading zero after hyphen (e.g., EHSS-03 → EHSS-3)
    match_with_zero = re.match(r'([A-Z]{4})-0(\d+)', class_code)
    if match_with_zero:
        prefix, digit = match_with_zero.groups()
        return f"%{prefix}-{digit}%"

    # For codes without leading zero, just use first part before any letters
    match = re.match(r'([A-Z]{4}-\d+)', class_code)
    if match:
        return f"%{match.group(1)}%"

    # Fallback: use the code as-is
    return f"%{class_code}%"

def main():
    extracted_dir = Path('extracted')
    csv_files = sorted(extracted_dir.glob('grades_extract_*.csv'))

    output_file = 'update_statements_all_files.sql'

    print(f"Processing {len(csv_files)} CSV files...")

    with open(output_file, 'w') as out:
        out.write("-- UPDATE Statements for All Grade Files\n")
        out.write("-- Generated with corrected logic: classid LIKE pattern, no term filtering\n")
        out.write("-- Subquery validates 2-3 total records across ALL time\n")
        out.write(f"-- Total files: {len(csv_files)}\n")
        out.write("-- \n\n")

        total_statements = 0

        for csv_file in csv_files:
            try:
                with open(csv_file, 'r') as f:
                    reader = csv.DictReader(f)
                    rows = list(reader)

                    if len(rows) == 0:
                        continue

                    # Parse first row to get class and termid
                    first_row = rows[0]
                    filename_value = first_row['filename']
                    class_code, termid = parse_filename_column(filename_value)

                    # Get class pattern
                    class_pattern = get_class_pattern(class_code)

                    # Write header for this file
                    out.write(f"-- ========================================\n")
                    out.write(f"-- File: {csv_file.name}\n")
                    out.write(f"-- Class: {class_code}, Term: {termid}\n")
                    out.write(f"-- Pattern: {class_pattern}\n")
                    out.write(f"-- Students: {len(rows)}\n")
                    out.write(f"-- ========================================\n\n")

                    # Process each student
                    for row in rows:
                        student_id = row['student_id'].zfill(5)
                        grade = row['grade'].strip().upper()

                        # Generate UPDATE statement with subquery validation
                        update_sql = f"""-- Student: {student_id}, Grade: {grade}
UPDATE AcademicCourseTakers
SET Grade = '{grade}'
WHERE ID = '{student_id}'
  AND classid LIKE '{class_pattern}'
  AND section NOT IN ('87', '147')
  AND Attendance = 'Normal'
  AND (
    SELECT COUNT(*)
    FROM AcademicCourseTakers AS t
    WHERE t.ID = '{student_id}'
      AND t.classid LIKE '{class_pattern}'
      AND t.section NOT IN ('87', '147')
      AND t.Attendance = 'Normal'
  ) BETWEEN 2 AND 3;

"""
                        out.write(update_sql)
                        total_statements += 1

                    out.write("\n")

            except Exception as e:
                print(f"Error processing {csv_file.name}: {e}")
                continue

        out.write(f"-- Total UPDATE statements: {total_statements}\n")

    print(f"Generated {total_statements} UPDATE statements in {output_file}")

if __name__ == '__main__':
    main()