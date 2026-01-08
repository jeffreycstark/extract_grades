#!/usr/bin/env python3
"""
Process failed grade CSV files from failed/ folder.

Updates grades in MSSQL database using the specific logic:
UPDATE academiccoursetakers set grade = '<grade>' 
where classid like '<termid>%' and grade = 'IP' and ID = '<student_id>'

Moves successfully processed files to success/ folder and generates audit report.
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


def extract_termid_from_filename(filename):
    """
    Extract TERMID from filename.
    
    Example: 'grades_extract_2021T2T2E_EHSS-02.csv' → '2021T2T2E'
    """
    # Pattern: grades_extract_<TERMID>_<COURSEID>.csv
    match = re.match(r'grades_extract_([^_]+)_.*\.csv', filename)
    if match:
        return match.group(1)
    return None


def process_csv_file(csv_path, real_mode=False, diagnostic=False):
    """
    Process a single CSV file from failed/ folder.
    
    For each record, execute:
    UPDATE academiccoursetakers set grade = '<grade>' 
    where classid like '<termid>%' and grade = 'IP' and ID = '<student_id>'
    
    Args:
        csv_path: Path to the CSV file
        real_mode: If True, execute UPDATE. If False, dry run only.
        diagnostic: If True, provide detailed breakdown of why records don't match
    
    Returns:
        dict with processing results
    """
    logger.info(f"Processing: {csv_path.name}")
    
    results = {
        'file': csv_path.name,
        'termid': None,
        'total_records': 0,
        'updated_records': 0,
        'not_found_records': [],
        'errors': [],
        'success': False,
    }
    
    try:
        # Extract TERMID from filename
        termid = extract_termid_from_filename(csv_path.name)
        if not termid:
            results['errors'].append("Could not extract TERMID from filename")
            logger.error(f"  ✗ Could not extract TERMID from filename")
            return results
        
        results['termid'] = termid
        logger.info(f"  Term ID: {termid}")
        
        # Read CSV file
        with open(csv_path, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            results['total_records'] = len(rows)
        
        if len(rows) == 0:
            logger.warning(f"  ✗ No data rows in {csv_path.name}")
            results['errors'].append("Empty CSV file")
            return results
        
        # Connect to database
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Process each record
        updated_count = 0
        not_found_count = 0
        
        for row in rows:
            try:
                # Parse CSV columns - based on the sample: "EHSS-02 final 28-06-21_2021T2T2E,11993,A"
                # Columns are: filename, student_id, grade
                filename_val = row.get('filename', '').strip()
                student_id = row.get('student_id', '').strip().zfill(5)
                grade = row.get('grade', '').strip().upper()
                
                if not student_id or not grade:
                    results['errors'].append(f"Missing student_id or grade in row: {row}")
                    logger.warning(f"  ⚠ Skipping row with missing data: {row}")
                    continue
                
                # Build the exact UPDATE statement as specified
                update_query = f"""
                    UPDATE academiccoursetakers 
                    SET grade = '{grade}'
                    WHERE classid LIKE '{termid}%' 
                      AND grade = 'IP' 
                      AND ID = '{student_id}'
                """
                
                if not real_mode:
                    # Dry run: check if records would be found
                    
                    if diagnostic:
                        # Detailed diagnostic: check each condition separately
                        student_exists_query = f"SELECT COUNT(*) FROM academiccoursetakers WHERE ID = '{student_id}'"
                        cursor.execute(student_exists_query)
                        student_exists = cursor.fetchone()[0]
                        
                        term_match_query = f"SELECT COUNT(*) FROM academiccoursetakers WHERE ID = '{student_id}' AND classid LIKE '{termid}%'"
                        cursor.execute(term_match_query)
                        term_match = cursor.fetchone()[0]
                        
                        ip_status_query = f"SELECT COUNT(*) FROM academiccoursetakers WHERE ID = '{student_id}' AND classid LIKE '{termid}%' AND grade = 'IP'"
                        cursor.execute(ip_status_query)
                        ip_status = cursor.fetchone()[0]
                        
                        if student_exists == 0:
                            reason = "Student ID not in database"
                        elif term_match == 0:
                            reason = "No records for this term"
                        elif ip_status == 0:
                            reason = "No IP grade (already updated or different status)"
                        else:
                            reason = "Unknown"
                        
                        not_found_count += 1
                        results['not_found_records'].append({
                            'student_id': student_id,
                            'grade': grade,
                            'termid': termid,
                            'reason': reason,
                            'student_exists': student_exists > 0,
                            'has_term_records': term_match > 0,
                            'has_ip_grade': ip_status > 0
                        })
                        logger.warning(f"    ⚠ NOT FOUND: {student_id} | exists: {student_exists > 0} | term: {term_match > 0} | IP: {ip_status > 0} ({reason})")
                    else:
                        # Simple check: all conditions together
                        check_query = f"""
                            SELECT COUNT(*) as cnt
                            FROM academiccoursetakers
                            WHERE classid LIKE '{termid}%'
                              AND grade = 'IP'
                              AND ID = '{student_id}'
                        """
                        cursor.execute(check_query)
                        result = cursor.fetchone()
                        record_count = result[0] if result else 0
                        
                        if record_count == 0:
                            not_found_count += 1
                            results['not_found_records'].append({
                                'student_id': student_id,
                                'grade': grade,
                                'termid': termid,
                                'reason': 'No records matching criteria'
                            })
                            logger.warning(f"    ⚠ NOT FOUND: student {student_id} for term {termid}")
                        else:
                            logger.info(f"    ✓ Would update: student {student_id} → {grade} ({record_count} records)")
                            updated_count += 1
                else:
                    # Real mode: execute UPDATE
                    cursor.execute(update_query)
                    rows_affected = cursor.rowcount
                    
                    if rows_affected == 0:
                        not_found_count += 1
                        results['not_found_records'].append({
                            'student_id': student_id,
                            'grade': grade,
                            'termid': termid,
                            'reason': 'No records matching criteria'
                        })
                        logger.warning(f"    ⚠ NOT FOUND: student {student_id} for term {termid}")
                    else:
                        updated_count += 1
                        results['updated_records'] += rows_affected
                        logger.info(f"    ✓ Updated: student {student_id} → {grade} ({rows_affected} records)")
            
            except Exception as e:
                results['errors'].append(f"Error processing row {row}: {e}")
                logger.error(f"    ✗ Error: {e}")
        
        if real_mode:
            conn.commit()
        
        conn.close()
        
        # Determine success based on results
        if len(results['not_found_records']) == 0 and len(results['errors']) == 0:
            results['success'] = True
            logger.info(f"  ✓ Success: {updated_count}/{results['total_records']} records updated")
        else:
            logger.warning(f"  ⚠ Partial success: {updated_count}/{results['total_records']} records, "
                          f"{len(results['not_found_records'])} not found")
    
    except Exception as e:
        logger.error(f"  ✗ Error processing {csv_path.name}: {e}")
        results['errors'].append(str(e))
    
    return results


def move_to_success(csv_path, success_dir):
    """Move a successfully processed CSV file to the success directory."""
    try:
        success_dir.mkdir(exist_ok=True)
        dest_path = success_dir / csv_path.name
        shutil.move(str(csv_path), str(dest_path))
        logger.info(f"  → Moved to success/")
        return True
    except Exception as e:
        logger.error(f"  ✗ Failed to move file to success: {e}")
        return False


def generate_audit_report(all_results, real_mode, output_file=None):
    """Generate detailed audit report with failed records."""
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    mode = "REAL UPDATE" if real_mode else "DRY RUN"
    
    # Calculate statistics
    total_files = len(all_results)
    successful_files = sum(1 for r in all_results if r['success'])
    failed_files = total_files - successful_files
    
    total_records = sum(r['total_records'] for r in all_results)
    updated_records = sum(r['updated_records'] for r in all_results)
    not_found_count = sum(len(r['not_found_records']) for r in all_results)
    
    # Build report
    report_lines = [
        "=" * 100,
        f"FAILED GRADES UPDATE AUDIT REPORT - {mode}",
        f"Generated: {timestamp}",
        "=" * 100,
        "",
        "SUMMARY:",
        f"  Total Files Processed:        {total_files}",
        f"  Successfully Processed:       {successful_files}",
        f"  Failed Processing:            {failed_files}",
        "",
        f"  Total Records in CSVs:        {total_records}",
        f"  Records Updated:              {updated_records}",
        f"  Records NOT FOUND in DB:      {not_found_count}",
        "",
        "=" * 100,
        "SUCCESSFULLY PROCESSED FILES:",
        "=" * 100,
    ]
    
    # List successful files
    successful = [r for r in all_results if r['success']]
    if successful:
        for r in successful:
            report_lines.append(
                f"  ✓ {r['file']:<60} | Term: {r['termid']:<12} | "
                f"{r['updated_records']}/{r['total_records']} updated"
            )
    else:
        report_lines.append("  (none)")
    
    report_lines.extend([
        "",
        "=" * 100,
        "FAILED RECORDS (NOT FOUND IN DATABASE):",
        "=" * 100,
    ])
    
    # Collect all not found records
    all_not_found = []
    for r in all_results:
        for record in r['not_found_records']:
            all_not_found.append((r['file'], record))
    
    if all_not_found:
        for filename, record in all_not_found:
            report_lines.append(
                f"  File: {filename}"
            )
            # Check if this has diagnostic info
            if 'student_exists' in record:
                report_lines.append(
                    f"    Student ID: {record['student_id']:<10} | "
                    f"Grade: {record['grade']:<5} | "
                    f"Term: {record['termid']:<15}"
                )
                report_lines.append(
                    f"      Reason: {record['reason']}"
                )
                report_lines.append(
                    f"      Student exists: {record['student_exists']} | "
                    f"Has term records: {record['has_term_records']} | "
                    f"Has IP grade: {record['has_ip_grade']}"
                )
            else:
                report_lines.append(
                    f"    Student ID: {record['student_id']:<10} | "
                    f"Grade: {record['grade']:<5} | "
                    f"Term: {record['termid']:<15} | "
                    f"Reason: {record['reason']}"
                )
    else:
        report_lines.append("  (none)")
    
    report_lines.extend([
        "",
        "=" * 100,
        "FILES WITH PROCESSING ERRORS:",
        "=" * 100,
    ])
    
    # List files with errors
    error_files = [r for r in all_results if r['errors']]
    if error_files:
        for r in error_files:
            report_lines.append(f"  ✗ {r['file']}")
            for error in r['errors']:
                report_lines.append(f"     - {error}")
    else:
        report_lines.append("  (none)")
    
    report_lines.extend([
        "",
        "=" * 100,
    ])
    
    report = '\n'.join(report_lines)
    
    # Print to console
    print("\n" + report)
    
    # Save to file
    if output_file:
        with open(output_file, 'w') as f:
            f.write(report)
        logger.info(f"\nAudit report saved to: {output_file}")
    
    return report


def main():
    parser = argparse.ArgumentParser(
        description='Process failed grade CSV files and update database'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        default=True,
        help='Perform dry run (check only, no UPDATE) - default is dry run'
    )
    parser.add_argument(
        '--real',
        action='store_true',
        help='Execute real UPDATE statements'
    )
    parser.add_argument(
        '--limit',
        type=int,
        help='Limit number of files to process'
    )
    parser.add_argument(
        '--file',
        type=str,
        help='Process a specific CSV file from failed/ folder'
    )
    parser.add_argument(
        '--audit-report',
        type=str,
        help='Save audit report to specified file'
    )
    parser.add_argument(
        '--diagnostic',
        action='store_true',
        help='Show detailed diagnostic info for why records do not match (slower)'
    )
    
    args = parser.parse_args()
    
    # Determine mode
    real_mode = args.real
    mode = "REAL UPDATE" if real_mode else "DRY RUN"
    
    logger.info(f"{'='*70}")
    logger.info(f"Failed Grades Update Tool - {mode}")
    logger.info(f"{'='*70}")
    
    # Setup directories
    failed_dir = Path('failed')
    success_dir = Path('success')
    
    if not failed_dir.exists():
        logger.error(f"Failed directory not found: {failed_dir}")
        return 1
    
    # Get CSV files
    if args.file:
        csv_files = [failed_dir / args.file]
    else:
        csv_files = sorted(failed_dir.glob('grades_extract_*.csv'))
        
        if args.limit:
            csv_files = csv_files[:args.limit]
    
    if not csv_files:
        logger.error("No CSV files found in failed/ folder")
        return 1
    
    logger.info(f"Found {len(csv_files)} file(s) to process\n")
    
    # Process each file
    all_results = []
    for csv_file in csv_files:
        results = process_csv_file(csv_file, real_mode=real_mode, diagnostic=args.diagnostic)
        all_results.append(results)
        
        # Move successful files to success/ (only in real mode)
        if real_mode and results['success']:
            move_to_success(csv_file, success_dir)
        
        logger.info("")
    
    # Generate audit report
    audit_file = args.audit_report if args.audit_report else None
    generate_audit_report(all_results, real_mode, output_file=audit_file)
    
    # Summary
    successful_count = sum(1 for r in all_results if r['success'])
    failed_count = len(all_results) - successful_count
    not_found_total = sum(len(r['not_found_records']) for r in all_results)
    
    logger.info(f"\nProcessing complete: {successful_count} successful, {failed_count} failed, "
               f"{not_found_total} records not found in database")
    
    return 0 if failed_count == 0 and not_found_total == 0 else 1


if __name__ == '__main__':
    exit(main())
