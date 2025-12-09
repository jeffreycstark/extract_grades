#!/usr/bin/env python3
"""
Update grades in MSSQL database from extracted CSV files.

Reads CSV files from extracted/ directory and updates the AcademicCourseTakers table
with the grade information. Failed files are moved to failed/ directory.
"""

import os
import csv
import re
import argparse
import shutil
from pathlib import Path
from datetime import datetime
from database.connection import get_db_connection
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def parse_filename_column(filename_value):
    """
    Parse the filename column from CSV to extract class and termid.

    Example: "EHSS-03 final 28-06-21_2021T2T2E"
    Returns: ("EHSS-03", "2021T2T2E")
    """
    # Split by underscore to get the termid (last part)
    parts = filename_value.split('_')
    termid = parts[-1] if parts else None

    # Get the first part (before first space) for class code
    first_part = filename_value.split()[0] if ' ' in filename_value else filename_value.split('_')[0]
    class_code = first_part

    return class_code, termid


def get_class_pattern(class_code):
    """
    Get simple LIKE pattern for class code matching.

    Removes leading zeros and uses wildcards.
    Examples:
    - "EHSS-03" → "%EHSS-3%"
    - "EHSS-7A" → "%EHSS-7%"
    - "GESL-01" → "%GESL-1%"
    """
    # Remove leading zero after hyphen (e.g., EHSS-03 → EHSS-3)
    match_with_zero = re.match(r'([A-Z]{4})-0(\d+)', class_code)
    if match_with_zero:
        prefix, digit = match_with_zero.groups()
        return f"%{prefix}-{digit}%"

    # For codes without leading zero, just use first part before any letters
    # E.g., EHSS-7A → EHSS-7
    match = re.match(r'([A-Z]{4}-\d+)', class_code)
    if match:
        return f"%{match.group(1)}%"

    # Fallback: use the code as-is
    return f"%{class_code}%"


def find_best_class_match(cursor, class_pattern, student_ids_str):
    """
    Find students who have 2-3 total records for this class (normal enrollment).
    Skips students with 4+ records (likely failed and retook multiple times).

    Returns: (matched_count, skipped_repeat_students)
    """
    matched_students = 0
    skipped_students = 0

    student_list = student_ids_str.split("', '")

    for student_id in student_list:
        # Count total records for this student-class combination across ALL time
        count_query = f"""
            SELECT COUNT(*)
            FROM AcademicCourseTakers
            WHERE classid LIKE '{class_pattern}'
              AND ID = '{student_id}'
              AND section NOT IN ('87', '147')
              AND Attendance = 'Normal'
        """
        cursor.execute(count_query)
        record_count = cursor.fetchone()[0]

        # Only include students with 2-3 records (normal enrollment, one class instance)
        if record_count >= 2 and record_count <= 3:
            matched_students += 1
        elif record_count >= 4:
            skipped_students += 1

    return matched_students, skipped_students


def process_csv_file(csv_path, dry_run=True, min_match_percent=80):
    """
    Process a single CSV file and update/query the database.

    Args:
        csv_path: Path to the CSV file
        dry_run: If True, only SELECT to verify. If False, perform UPDATE.
        min_match_percent: Minimum match percentage to consider success (default 80%)

    Returns:
        dict with processing results
    """
    logger.info(f"Processing: {csv_path.name}")

    results = {
        'file': csv_path.name,
        'total_students': 0,
        'matched_students': 0,
        'updated_records': 0,
        'unmatched_students': 0,
        'match_percent': 0.0,
        'class_code': None,
        'termid': None,
        'success': False,
        'errors': []
    }

    try:
        with open(csv_path, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            results['total_students'] = len(rows)

            if len(rows) == 0:
                logger.warning(f"  No data rows in {csv_path.name}")
                results['errors'].append("Empty CSV file")
                return results

            # Parse first row to get class and termid
            first_row = rows[0]
            filename_value = first_row['filename']
            class_code, termid = parse_filename_column(filename_value)

            results['class_code'] = class_code
            results['termid'] = termid

            logger.info(f"  Class: {class_code}, Term: {termid}")

            # Get class pattern
            class_pattern = get_class_pattern(class_code)
            logger.info(f"  Using pattern: {class_pattern}")

            # Collect all student IDs and grades
            student_data = []
            for row in rows:
                student_id = row['student_id'].zfill(5)
                grade = row['grade'].strip().upper()
                student_data.append({'id': student_id, 'grade': grade})

            # Get list of unique student IDs
            unique_student_ids = list(set(s['id'] for s in student_data))
            student_ids_str = "', '".join(unique_student_ids)

            # Connect to database
            conn = get_db_connection()
            cursor = conn.cursor()

            # Find matching students (2-3 records = normal enrollment)
            matched_count, skipped_repeats = find_best_class_match(
                cursor, class_pattern, student_ids_str
            )

            results['matched_students'] = matched_count
            results['unmatched_students'] = len(unique_student_ids) - matched_count
            results['match_percent'] = (matched_count / len(unique_student_ids) * 100) if len(unique_student_ids) > 0 else 0

            if matched_count == 0:
                logger.warning(f"  ✗ No matching records found in database")
                results['errors'].append("No matching records in database")
                conn.close()
                return results

            logger.info(f"  Matched: {matched_count}/{len(unique_student_ids)} students ({results['match_percent']:.1f}%)")
            if skipped_repeats > 0:
                logger.info(f"  Skipped {skipped_repeats} students with 4+ records (took class multiple times)")

            # Check if match percentage is acceptable
            if results['match_percent'] < min_match_percent:
                logger.warning(f"  ⚠ Match rate {results['match_percent']:.1f}% below threshold {min_match_percent}%")
                results['errors'].append(f"Low match rate: {results['match_percent']:.1f}% < {min_match_percent}%")
                conn.close()
                return results

            if dry_run:
                logger.info(f"  DRY RUN - Would update grades for {matched_count} students")

                # Show sample of what would be updated
                sample_query = f"""
                    SELECT TOP 5 ID, classid, Grade, section
                    FROM AcademicCourseTakers
                    WHERE classid LIKE '{class_pattern}'
                      AND ID IN ('{student_ids_str}')
                      AND section NOT IN ('87', '147')
                      AND Attendance = 'Normal'
                    ORDER BY ID
                """
                cursor.execute(sample_query)
                samples = cursor.fetchall()

                logger.info(f"  Sample records to update:")
                for record in samples:
                    student_id = record[0]
                    current_grade = record[2].strip() if record[2] else 'NULL'
                    new_grade = next((s['grade'] for s in student_data if s['id'] == student_id), '?')
                    logger.info(f"    {student_id} | {record[1]} | Section {record[3]} | {current_grade} → {new_grade}")

                results['success'] = True
            else:
                logger.info(f"  REAL UPDATE - Updating grades...")

                # Update each student's grade (only if they have 2-3 total records)
                updated_count = 0
                for student in student_data:
                    # Update uses subquery to validate 2-3 records
                    update_query = f"""
                        UPDATE AcademicCourseTakers
                        SET Grade = '{student['grade']}'
                        WHERE ID = '{student['id']}'
                          AND classid LIKE '{class_pattern}'
                          AND section NOT IN ('87', '147')
                          AND Attendance = 'Normal'
                          AND (
                            SELECT COUNT(*)
                            FROM AcademicCourseTakers AS t
                            WHERE t.ID = '{student['id']}'
                              AND t.classid LIKE '{class_pattern}'
                              AND t.section NOT IN ('87', '147')
                              AND t.Attendance = 'Normal'
                          ) BETWEEN 2 AND 3
                    """

                    cursor.execute(update_query)
                    rows_affected = cursor.rowcount

                    if rows_affected > 0:
                        updated_count += 1
                        results['updated_records'] += rows_affected

                conn.commit()

                logger.info(f"  ✓ Updated {updated_count} students ({results['updated_records']} total records)")

                if updated_count == matched_count:
                    results['success'] = True
                else:
                    logger.warning(f"  ⚠ Expected to update {matched_count} students but only updated {updated_count}")
                    results['errors'].append(f"Update mismatch: {updated_count}/{matched_count}")

            conn.close()

    except Exception as e:
        logger.error(f"  ✗ Error processing {csv_path.name}: {e}")
        results['errors'].append(str(e))

    return results


def move_to_failed(csv_path, failed_dir):
    """Move a failed CSV file to the failed directory."""
    try:
        failed_dir.mkdir(exist_ok=True)
        dest_path = failed_dir / csv_path.name
        shutil.move(str(csv_path), str(dest_path))
        logger.info(f"  → Moved to failed/")
        return True
    except Exception as e:
        logger.error(f"  ✗ Failed to move file: {e}")
        return False


def generate_audit_report(all_results, dry_run, output_file=None):
    """Generate detailed audit report."""

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    mode = "DRY RUN" if dry_run else "REAL UPDATE"

    # Calculate statistics
    total_files = len(all_results)
    successful_files = sum(1 for r in all_results if r['success'])
    failed_files = total_files - successful_files

    total_students = sum(r['total_students'] for r in all_results)
    matched_students = sum(r['matched_students'] for r in all_results)
    updated_records = sum(r['updated_records'] for r in all_results)

    # Build report
    report_lines = [
        "=" * 80,
        f"GRADE UPDATE AUDIT REPORT - {mode}",
        f"Generated: {timestamp}",
        "=" * 80,
        "",
        "SUMMARY:",
        f"  Total Files Processed: {total_files}",
        f"  Successful Files: {successful_files}",
        f"  Failed Files: {failed_files}",
        "",
        f"  Total Students in CSVs: {total_students}",
        f"  Students Matched in DB: {matched_students}",
        f"  Students Updated: {matched_students if not dry_run else 0}",
        f"  Database Records Updated: {updated_records if not dry_run else 0}",
        "",
        f"  Overall Match Rate: {(matched_students/total_students*100) if total_students > 0 else 0:.1f}%",
        "",
        "=" * 80,
        "SUCCESSFUL FILES:",
        "=" * 80,
    ]

    # List successful files
    for r in all_results:
        if r['success']:
            report_lines.append(
                f"  ✓ {r['file']:<50} | {r['class_code']:<12} | {r['termid']:<15} | "
                f"{r['matched_students']:>3}/{r['total_students']:>3} students ({r['match_percent']:>5.1f}%)"
            )

    if not any(r['success'] for r in all_results):
        report_lines.append("  (none)")

    report_lines.extend([
        "",
        "=" * 80,
        "FAILED FILES:",
        "=" * 80,
    ])

    # List failed files
    for r in all_results:
        if not r['success']:
            errors = '; '.join(r['errors']) if r['errors'] else 'Unknown error'
            report_lines.append(
                f"  ✗ {r['file']:<50} | {r['class_code']:<12} | {r['termid']:<15}"
            )
            report_lines.append(f"     Reason: {errors}")
            report_lines.append(f"     Match: {r['matched_students']}/{r['total_students']} students ({r['match_percent']:.1f}%)")

    if not any(not r['success'] for r in all_results):
        report_lines.append("  (none)")

    report_lines.extend([
        "",
        "=" * 80,
    ])

    report = '\n'.join(report_lines)

    # Print to console
    print("\n" + report)

    # Optionally save to file
    if output_file:
        with open(output_file, 'w') as f:
            f.write(report)
        logger.info(f"\nAudit report saved to: {output_file}")

    return report


def main():
    parser = argparse.ArgumentParser(
        description='Update MSSQL database with grades from extracted CSV files'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Perform dry run (SELECT only, no UPDATE)'
    )
    parser.add_argument(
        '--limit',
        type=int,
        help='Limit number of files to process'
    )
    parser.add_argument(
        '--file',
        type=str,
        help='Process a specific CSV file'
    )
    parser.add_argument(
        '--min-match',
        type=int,
        default=80,
        help='Minimum match percentage to consider success (default: 80)'
    )
    parser.add_argument(
        '--audit-report',
        type=str,
        help='Save audit report to specified file'
    )

    args = parser.parse_args()

    mode = "DRY RUN" if args.dry_run else "REAL UPDATE"
    logger.info(f"{'='*60}")
    logger.info(f"Grade Update Tool - {mode}")
    logger.info(f"{'='*60}")

    # Setup directories
    extracted_dir = Path('extracted')
    failed_dir = Path('failed')
    failed_dir.mkdir(exist_ok=True)

    # Get CSV files
    if args.file:
        csv_files = [Path(args.file)]
    else:
        csv_files = sorted(extracted_dir.glob('grades_extract_*.csv'))

        if args.limit:
            csv_files = csv_files[:args.limit]

    if not csv_files:
        logger.error("No CSV files found to process")
        return 1

    logger.info(f"Found {len(csv_files)} file(s) to process\n")

    # Process each file
    all_results = []
    for csv_file in csv_files:
        results = process_csv_file(csv_file, dry_run=args.dry_run, min_match_percent=args.min_match)
        all_results.append(results)

        # Move failed files to failed/ directory (only in real mode)
        if not args.dry_run and not results['success']:
            move_to_failed(csv_file, failed_dir)

        logger.info("")

    # Generate audit report
    audit_file = args.audit_report if args.audit_report else None
    generate_audit_report(all_results, args.dry_run, output_file=audit_file)

    # Return exit code based on success
    failed_count = sum(1 for r in all_results if not r['success'])
    return 0 if failed_count == 0 else 1


if __name__ == '__main__':
    exit(main())