-- Grade Update Statements - Batch 1 (50 students)
-- Class: EHSS-01 (pattern: %EHSS-1%)
-- Uses classid LIKE pattern (no leading zeros)
-- Counts total records across ALL time (no term filter)
-- Only updates students with 2-3 total records (normal enrollment)

-- Student: 09072, Grade: F
UPDATE AcademicCourseTakers
SET Grade = 'F'
WHERE ID = '09072'
  AND classid LIKE '%EHSS-1%'
  AND section NOT IN ('87', '147')
  AND Attendance = 'Normal'
  AND (
    SELECT COUNT(*)
    FROM AcademicCourseTakers AS t
    WHERE t.ID = '09072'
      AND t.classid LIKE '%EHSS-1%'
      AND t.section NOT IN ('87', '147')
      AND t.Attendance = 'Normal'
  ) BETWEEN 2 AND 3;

-- Student: 12389, Grade: F
UPDATE AcademicCourseTakers
SET Grade = 'F'
WHERE ID = '12389'
  AND classid LIKE '%EHSS-1%'
  AND section NOT IN ('87', '147')
  AND Attendance = 'Normal'
  AND (
    SELECT COUNT(*)
    FROM AcademicCourseTakers AS t
    WHERE t.ID = '12389'
      AND t.classid LIKE '%EHSS-1%'
      AND t.section NOT IN ('87', '147')
      AND t.Attendance = 'Normal'
  ) BETWEEN 2 AND 3;

-- Student: 14612, Grade: C
UPDATE AcademicCourseTakers
SET Grade = 'C'
WHERE ID = '14612'
  AND classid LIKE '%EHSS-1%'
  AND section NOT IN ('87', '147')
  AND Attendance = 'Normal'
  AND (
    SELECT COUNT(*)
    FROM AcademicCourseTakers AS t
    WHERE t.ID = '14612'
      AND t.classid LIKE '%EHSS-1%'
      AND t.section NOT IN ('87', '147')
      AND t.Attendance = 'Normal'
  ) BETWEEN 2 AND 3;

-- Student: 14617, Grade: C
UPDATE AcademicCourseTakers
SET Grade = 'C'
WHERE ID = '14617'
  AND classid LIKE '%EHSS-1%'
  AND section NOT IN ('87', '147')
  AND Attendance = 'Normal'
  AND (
    SELECT COUNT(*)
    FROM AcademicCourseTakers AS t
    WHERE t.ID = '14617'
      AND t.classid LIKE '%EHSS-1%'
      AND t.section NOT IN ('87', '147')
      AND t.Attendance = 'Normal'
  ) BETWEEN 2 AND 3;

-- Student: 14619, Grade: F
UPDATE AcademicCourseTakers
SET Grade = 'F'
WHERE ID = '14619'
  AND classid LIKE '%EHSS-1%'
  AND section NOT IN ('87', '147')
  AND Attendance = 'Normal'
  AND (
    SELECT COUNT(*)
    FROM AcademicCourseTakers AS t
    WHERE t.ID = '14619'
      AND t.classid LIKE '%EHSS-1%'
      AND t.section NOT IN ('87', '147')
      AND t.Attendance = 'Normal'
  ) BETWEEN 2 AND 3;

-- Student: 14621, Grade: A
UPDATE AcademicCourseTakers
SET Grade = 'A'
WHERE ID = '14621'
  AND classid LIKE '%EHSS-1%'
  AND section NOT IN ('87', '147')
  AND Attendance = 'Normal'
  AND (
    SELECT COUNT(*)
    FROM AcademicCourseTakers AS t
    WHERE t.ID = '14621'
      AND t.classid LIKE '%EHSS-1%'
      AND t.section NOT IN ('87', '147')
      AND t.Attendance = 'Normal'
  ) BETWEEN 2 AND 3;

-- Student: 14623, Grade: B
UPDATE AcademicCourseTakers
SET Grade = 'B'
WHERE ID = '14623'
  AND classid LIKE '%EHSS-1%'
  AND section NOT IN ('87', '147')
  AND Attendance = 'Normal'
  AND (
    SELECT COUNT(*)
    FROM AcademicCourseTakers AS t
    WHERE t.ID = '14623'
      AND t.classid LIKE '%EHSS-1%'
      AND t.section NOT IN ('87', '147')
      AND t.Attendance = 'Normal'
  ) BETWEEN 2 AND 3;

-- Student: 14624, Grade: C
UPDATE AcademicCourseTakers
SET Grade = 'C'
WHERE ID = '14624'
  AND classid LIKE '%EHSS-1%'
  AND section NOT IN ('87', '147')
  AND Attendance = 'Normal'
  AND (
    SELECT COUNT(*)
    FROM AcademicCourseTakers AS t
    WHERE t.ID = '14624'
      AND t.classid LIKE '%EHSS-1%'
      AND t.section NOT IN ('87', '147')
      AND t.Attendance = 'Normal'
  ) BETWEEN 2 AND 3;

-- Student: 14630, Grade: D
UPDATE AcademicCourseTakers
SET Grade = 'D'
WHERE ID = '14630'
  AND classid LIKE '%EHSS-1%'
  AND section NOT IN ('87', '147')
  AND Attendance = 'Normal'
  AND (
    SELECT COUNT(*)
    FROM AcademicCourseTakers AS t
    WHERE t.ID = '14630'
      AND t.classid LIKE '%EHSS-1%'
      AND t.section NOT IN ('87', '147')
      AND t.Attendance = 'Normal'
  ) BETWEEN 2 AND 3;

-- Student: 14634, Grade: C
UPDATE AcademicCourseTakers
SET Grade = 'C'
WHERE ID = '14634'
  AND classid LIKE '%EHSS-1%'
  AND section NOT IN ('87', '147')
  AND Attendance = 'Normal'
  AND (
    SELECT COUNT(*)
    FROM AcademicCourseTakers AS t
    WHERE t.ID = '14634'
      AND t.classid LIKE '%EHSS-1%'
      AND t.section NOT IN ('87', '147')
      AND t.Attendance = 'Normal'
  ) BETWEEN 2 AND 3;

-- Student: 14635, Grade: F
UPDATE AcademicCourseTakers
SET Grade = 'F'
WHERE ID = '14635'
  AND classid LIKE '%EHSS-1%'
  AND section NOT IN ('87', '147')
  AND Attendance = 'Normal'
  AND (
    SELECT COUNT(*)
    FROM AcademicCourseTakers AS t
    WHERE t.ID = '14635'
      AND t.classid LIKE '%EHSS-1%'
      AND t.section NOT IN ('87', '147')
      AND t.Attendance = 'Normal'
  ) BETWEEN 2 AND 3;

-- Student: 14642, Grade: F
UPDATE AcademicCourseTakers
SET Grade = 'F'
WHERE ID = '14642'
  AND classid LIKE '%EHSS-1%'
  AND section NOT IN ('87', '147')
  AND Attendance = 'Normal'
  AND (
    SELECT COUNT(*)
    FROM AcademicCourseTakers AS t
    WHERE t.ID = '14642'
      AND t.classid LIKE '%EHSS-1%'
      AND t.section NOT IN ('87', '147')
      AND t.Attendance = 'Normal'
  ) BETWEEN 2 AND 3;

-- Student: 14643, Grade: A
UPDATE AcademicCourseTakers
SET Grade = 'A'
WHERE ID = '14643'
  AND classid LIKE '%EHSS-1%'
  AND section NOT IN ('87', '147')
  AND Attendance = 'Normal'
  AND (
    SELECT COUNT(*)
    FROM AcademicCourseTakers AS t
    WHERE t.ID = '14643'
      AND t.classid LIKE '%EHSS-1%'
      AND t.section NOT IN ('87', '147')
      AND t.Attendance = 'Normal'
  ) BETWEEN 2 AND 3;

-- Student: 14648, Grade: A
UPDATE AcademicCourseTakers
SET Grade = 'A'
WHERE ID = '14648'
  AND classid LIKE '%EHSS-1%'
  AND section NOT IN ('87', '147')
  AND Attendance = 'Normal'
  AND (
    SELECT COUNT(*)
    FROM AcademicCourseTakers AS t
    WHERE t.ID = '14648'
      AND t.classid LIKE '%EHSS-1%'
      AND t.section NOT IN ('87', '147')
      AND t.Attendance = 'Normal'
  ) BETWEEN 2 AND 3;

-- Student: 14650, Grade: A
UPDATE AcademicCourseTakers
SET Grade = 'A'
WHERE ID = '14650'
  AND classid LIKE '%EHSS-1%'
  AND section NOT IN ('87', '147')
  AND Attendance = 'Normal'
  AND (
    SELECT COUNT(*)
    FROM AcademicCourseTakers AS t
    WHERE t.ID = '14650'
      AND t.classid LIKE '%EHSS-1%'
      AND t.section NOT IN ('87', '147')
      AND t.Attendance = 'Normal'
  ) BETWEEN 2 AND 3;

-- Student: 14651, Grade: C
UPDATE AcademicCourseTakers
SET Grade = 'C'
WHERE ID = '14651'
  AND classid LIKE '%EHSS-1%'
  AND section NOT IN ('87', '147')
  AND Attendance = 'Normal'
  AND (
    SELECT COUNT(*)
    FROM AcademicCourseTakers AS t
    WHERE t.ID = '14651'
      AND t.classid LIKE '%EHSS-1%'
      AND t.section NOT IN ('87', '147')
      AND t.Attendance = 'Normal'
  ) BETWEEN 2 AND 3;

-- Student: 14653, Grade: B
UPDATE AcademicCourseTakers
SET Grade = 'B'
WHERE ID = '14653'
  AND classid LIKE '%EHSS-1%'
  AND section NOT IN ('87', '147')
  AND Attendance = 'Normal'
  AND (
    SELECT COUNT(*)
    FROM AcademicCourseTakers AS t
    WHERE t.ID = '14653'
      AND t.classid LIKE '%EHSS-1%'
      AND t.section NOT IN ('87', '147')
      AND t.Attendance = 'Normal'
  ) BETWEEN 2 AND 3;

-- Student: 14771, Grade: D
UPDATE AcademicCourseTakers
SET Grade = 'D'
WHERE ID = '14771'
  AND classid LIKE '%EHSS-1%'
  AND section NOT IN ('87', '147')
  AND Attendance = 'Normal'
  AND (
    SELECT COUNT(*)
    FROM AcademicCourseTakers AS t
    WHERE t.ID = '14771'
      AND t.classid LIKE '%EHSS-1%'
      AND t.section NOT IN ('87', '147')
      AND t.Attendance = 'Normal'
  ) BETWEEN 2 AND 3;

-- Student: 14776, Grade: B
UPDATE AcademicCourseTakers
SET Grade = 'B'
WHERE ID = '14776'
  AND classid LIKE '%EHSS-1%'
  AND section NOT IN ('87', '147')
  AND Attendance = 'Normal'
  AND (
    SELECT COUNT(*)
    FROM AcademicCourseTakers AS t
    WHERE t.ID = '14776'
      AND t.classid LIKE '%EHSS-1%'
      AND t.section NOT IN ('87', '147')
      AND t.Attendance = 'Normal'
  ) BETWEEN 2 AND 3;

-- Student: 14778, Grade: A
UPDATE AcademicCourseTakers
SET Grade = 'A'
WHERE ID = '14778'
  AND classid LIKE '%EHSS-1%'
  AND section NOT IN ('87', '147')
  AND Attendance = 'Normal'
  AND (
    SELECT COUNT(*)
    FROM AcademicCourseTakers AS t
    WHERE t.ID = '14778'
      AND t.classid LIKE '%EHSS-1%'
      AND t.section NOT IN ('87', '147')
      AND t.Attendance = 'Normal'
  ) BETWEEN 2 AND 3;

-- Student: 14796, Grade: F
UPDATE AcademicCourseTakers
SET Grade = 'F'
WHERE ID = '14796'
  AND classid LIKE '%EHSS-1%'
  AND section NOT IN ('87', '147')
  AND Attendance = 'Normal'
  AND (
    SELECT COUNT(*)
    FROM AcademicCourseTakers AS t
    WHERE t.ID = '14796'
      AND t.classid LIKE '%EHSS-1%'
      AND t.section NOT IN ('87', '147')
      AND t.Attendance = 'Normal'
  ) BETWEEN 2 AND 3;

-- Student: 14800, Grade: B
UPDATE AcademicCourseTakers
SET Grade = 'B'
WHERE ID = '14800'
  AND classid LIKE '%EHSS-1%'
  AND section NOT IN ('87', '147')
  AND Attendance = 'Normal'
  AND (
    SELECT COUNT(*)
    FROM AcademicCourseTakers AS t
    WHERE t.ID = '14800'
      AND t.classid LIKE '%EHSS-1%'
      AND t.section NOT IN ('87', '147')
      AND t.Attendance = 'Normal'
  ) BETWEEN 2 AND 3;

-- Student: 14805, Grade: C
UPDATE AcademicCourseTakers
SET Grade = 'C'
WHERE ID = '14805'
  AND classid LIKE '%EHSS-1%'
  AND section NOT IN ('87', '147')
  AND Attendance = 'Normal'
  AND (
    SELECT COUNT(*)
    FROM AcademicCourseTakers AS t
    WHERE t.ID = '14805'
      AND t.classid LIKE '%EHSS-1%'
      AND t.section NOT IN ('87', '147')
      AND t.Attendance = 'Normal'
  ) BETWEEN 2 AND 3;

-- Student: 14806, Grade: D
UPDATE AcademicCourseTakers
SET Grade = 'D'
WHERE ID = '14806'
  AND classid LIKE '%EHSS-1%'
  AND section NOT IN ('87', '147')
  AND Attendance = 'Normal'
  AND (
    SELECT COUNT(*)
    FROM AcademicCourseTakers AS t
    WHERE t.ID = '14806'
      AND t.classid LIKE '%EHSS-1%'
      AND t.section NOT IN ('87', '147')
      AND t.Attendance = 'Normal'
  ) BETWEEN 2 AND 3;

-- Student: 14815, Grade: C
UPDATE AcademicCourseTakers
SET Grade = 'C'
WHERE ID = '14815'
  AND classid LIKE '%EHSS-1%'
  AND section NOT IN ('87', '147')
  AND Attendance = 'Normal'
  AND (
    SELECT COUNT(*)
    FROM AcademicCourseTakers AS t
    WHERE t.ID = '14815'
      AND t.classid LIKE '%EHSS-1%'
      AND t.section NOT IN ('87', '147')
      AND t.Attendance = 'Normal'
  ) BETWEEN 2 AND 3;

-- Student: 14821, Grade: D
UPDATE AcademicCourseTakers
SET Grade = 'D'
WHERE ID = '14821'
  AND classid LIKE '%EHSS-1%'
  AND section NOT IN ('87', '147')
  AND Attendance = 'Normal'
  AND (
    SELECT COUNT(*)
    FROM AcademicCourseTakers AS t
    WHERE t.ID = '14821'
      AND t.classid LIKE '%EHSS-1%'
      AND t.section NOT IN ('87', '147')
      AND t.Attendance = 'Normal'
  ) BETWEEN 2 AND 3;

-- Student: 14840, Grade: B
UPDATE AcademicCourseTakers
SET Grade = 'B'
WHERE ID = '14840'
  AND classid LIKE '%EHSS-1%'
  AND section NOT IN ('87', '147')
  AND Attendance = 'Normal'
  AND (
    SELECT COUNT(*)
    FROM AcademicCourseTakers AS t
    WHERE t.ID = '14840'
      AND t.classid LIKE '%EHSS-1%'
      AND t.section NOT IN ('87', '147')
      AND t.Attendance = 'Normal'
  ) BETWEEN 2 AND 3;

-- Student: 11285, Grade: B
UPDATE AcademicCourseTakers
SET Grade = 'B'
WHERE ID = '11285'
  AND classid LIKE '%EHSS-1%'
  AND section NOT IN ('87', '147')
  AND Attendance = 'Normal'
  AND (
    SELECT COUNT(*)
    FROM AcademicCourseTakers AS t
    WHERE t.ID = '11285'
      AND t.classid LIKE '%EHSS-1%'
      AND t.section NOT IN ('87', '147')
      AND t.Attendance = 'Normal'
  ) BETWEEN 2 AND 3;

-- Student: 12168, Grade: C
UPDATE AcademicCourseTakers
SET Grade = 'C'
WHERE ID = '12168'
  AND classid LIKE '%EHSS-1%'
  AND section NOT IN ('87', '147')
  AND Attendance = 'Normal'
  AND (
    SELECT COUNT(*)
    FROM AcademicCourseTakers AS t
    WHERE t.ID = '12168'
      AND t.classid LIKE '%EHSS-1%'
      AND t.section NOT IN ('87', '147')
      AND t.Attendance = 'Normal'
  ) BETWEEN 2 AND 3;

-- Student: 12437, Grade: A
UPDATE AcademicCourseTakers
SET Grade = 'A'
WHERE ID = '12437'
  AND classid LIKE '%EHSS-1%'
  AND section NOT IN ('87', '147')
  AND Attendance = 'Normal'
  AND (
    SELECT COUNT(*)
    FROM AcademicCourseTakers AS t
    WHERE t.ID = '12437'
      AND t.classid LIKE '%EHSS-1%'
      AND t.section NOT IN ('87', '147')
      AND t.Attendance = 'Normal'
  ) BETWEEN 2 AND 3;

-- Student: 13038, Grade: B
UPDATE AcademicCourseTakers
SET Grade = 'B'
WHERE ID = '13038'
  AND classid LIKE '%EHSS-1%'
  AND section NOT IN ('87', '147')
  AND Attendance = 'Normal'
  AND (
    SELECT COUNT(*)
    FROM AcademicCourseTakers AS t
    WHERE t.ID = '13038'
      AND t.classid LIKE '%EHSS-1%'
      AND t.section NOT IN ('87', '147')
      AND t.Attendance = 'Normal'
  ) BETWEEN 2 AND 3;

-- Student: 13238, Grade: B
UPDATE AcademicCourseTakers
SET Grade = 'B'
WHERE ID = '13238'
  AND classid LIKE '%EHSS-1%'
  AND section NOT IN ('87', '147')
  AND Attendance = 'Normal'
  AND (
    SELECT COUNT(*)
    FROM AcademicCourseTakers AS t
    WHERE t.ID = '13238'
      AND t.classid LIKE '%EHSS-1%'
      AND t.section NOT IN ('87', '147')
      AND t.Attendance = 'Normal'
  ) BETWEEN 2 AND 3;

-- Student: 13383, Grade: C
UPDATE AcademicCourseTakers
SET Grade = 'C'
WHERE ID = '13383'
  AND classid LIKE '%EHSS-1%'
  AND section NOT IN ('87', '147')
  AND Attendance = 'Normal'
  AND (
    SELECT COUNT(*)
    FROM AcademicCourseTakers AS t
    WHERE t.ID = '13383'
      AND t.classid LIKE '%EHSS-1%'
      AND t.section NOT IN ('87', '147')
      AND t.Attendance = 'Normal'
  ) BETWEEN 2 AND 3;

-- Student: 13665, Grade: D
UPDATE AcademicCourseTakers
SET Grade = 'D'
WHERE ID = '13665'
  AND classid LIKE '%EHSS-1%'
  AND section NOT IN ('87', '147')
  AND Attendance = 'Normal'
  AND (
    SELECT COUNT(*)
    FROM AcademicCourseTakers AS t
    WHERE t.ID = '13665'
      AND t.classid LIKE '%EHSS-1%'
      AND t.section NOT IN ('87', '147')
      AND t.Attendance = 'Normal'
  ) BETWEEN 2 AND 3;

-- Student: 13726, Grade: D
UPDATE AcademicCourseTakers
SET Grade = 'D'
WHERE ID = '13726'
  AND classid LIKE '%EHSS-1%'
  AND section NOT IN ('87', '147')
  AND Attendance = 'Normal'
  AND (
    SELECT COUNT(*)
    FROM AcademicCourseTakers AS t
    WHERE t.ID = '13726'
      AND t.classid LIKE '%EHSS-1%'
      AND t.section NOT IN ('87', '147')
      AND t.Attendance = 'Normal'
  ) BETWEEN 2 AND 3;

-- Student: 13833, Grade: C
UPDATE AcademicCourseTakers
SET Grade = 'C'
WHERE ID = '13833'
  AND classid LIKE '%EHSS-1%'
  AND section NOT IN ('87', '147')
  AND Attendance = 'Normal'
  AND (
    SELECT COUNT(*)
    FROM AcademicCourseTakers AS t
    WHERE t.ID = '13833'
      AND t.classid LIKE '%EHSS-1%'
      AND t.section NOT IN ('87', '147')
      AND t.Attendance = 'Normal'
  ) BETWEEN 2 AND 3;

-- Student: 14137, Grade: C
UPDATE AcademicCourseTakers
SET Grade = 'C'
WHERE ID = '14137'
  AND classid LIKE '%EHSS-1%'
  AND section NOT IN ('87', '147')
  AND Attendance = 'Normal'
  AND (
    SELECT COUNT(*)
    FROM AcademicCourseTakers AS t
    WHERE t.ID = '14137'
      AND t.classid LIKE '%EHSS-1%'
      AND t.section NOT IN ('87', '147')
      AND t.Attendance = 'Normal'
  ) BETWEEN 2 AND 3;

-- Student: 14236, Grade: F
UPDATE AcademicCourseTakers
SET Grade = 'F'
WHERE ID = '14236'
  AND classid LIKE '%EHSS-1%'
  AND section NOT IN ('87', '147')
  AND Attendance = 'Normal'
  AND (
    SELECT COUNT(*)
    FROM AcademicCourseTakers AS t
    WHERE t.ID = '14236'
      AND t.classid LIKE '%EHSS-1%'
      AND t.section NOT IN ('87', '147')
      AND t.Attendance = 'Normal'
  ) BETWEEN 2 AND 3;

-- Student: 14237, Grade: D
UPDATE AcademicCourseTakers
SET Grade = 'D'
WHERE ID = '14237'
  AND classid LIKE '%EHSS-1%'
  AND section NOT IN ('87', '147')
  AND Attendance = 'Normal'
  AND (
    SELECT COUNT(*)
    FROM AcademicCourseTakers AS t
    WHERE t.ID = '14237'
      AND t.classid LIKE '%EHSS-1%'
      AND t.section NOT IN ('87', '147')
      AND t.Attendance = 'Normal'
  ) BETWEEN 2 AND 3;

-- Student: 14291, Grade: C
UPDATE AcademicCourseTakers
SET Grade = 'C'
WHERE ID = '14291'
  AND classid LIKE '%EHSS-1%'
  AND section NOT IN ('87', '147')
  AND Attendance = 'Normal'
  AND (
    SELECT COUNT(*)
    FROM AcademicCourseTakers AS t
    WHERE t.ID = '14291'
      AND t.classid LIKE '%EHSS-1%'
      AND t.section NOT IN ('87', '147')
      AND t.Attendance = 'Normal'
  ) BETWEEN 2 AND 3;

-- Student: 14296, Grade: D
UPDATE AcademicCourseTakers
SET Grade = 'D'
WHERE ID = '14296'
  AND classid LIKE '%EHSS-1%'
  AND section NOT IN ('87', '147')
  AND Attendance = 'Normal'
  AND (
    SELECT COUNT(*)
    FROM AcademicCourseTakers AS t
    WHERE t.ID = '14296'
      AND t.classid LIKE '%EHSS-1%'
      AND t.section NOT IN ('87', '147')
      AND t.Attendance = 'Normal'
  ) BETWEEN 2 AND 3;

-- Student: 14299, Grade: D
UPDATE AcademicCourseTakers
SET Grade = 'D'
WHERE ID = '14299'
  AND classid LIKE '%EHSS-1%'
  AND section NOT IN ('87', '147')
  AND Attendance = 'Normal'
  AND (
    SELECT COUNT(*)
    FROM AcademicCourseTakers AS t
    WHERE t.ID = '14299'
      AND t.classid LIKE '%EHSS-1%'
      AND t.section NOT IN ('87', '147')
      AND t.Attendance = 'Normal'
  ) BETWEEN 2 AND 3;

-- Student: 14377, Grade: A
UPDATE AcademicCourseTakers
SET Grade = 'A'
WHERE ID = '14377'
  AND classid LIKE '%EHSS-1%'
  AND section NOT IN ('87', '147')
  AND Attendance = 'Normal'
  AND (
    SELECT COUNT(*)
    FROM AcademicCourseTakers AS t
    WHERE t.ID = '14377'
      AND t.classid LIKE '%EHSS-1%'
      AND t.section NOT IN ('87', '147')
      AND t.Attendance = 'Normal'
  ) BETWEEN 2 AND 3;

-- Student: 14419, Grade: C
UPDATE AcademicCourseTakers
SET Grade = 'C'
WHERE ID = '14419'
  AND classid LIKE '%EHSS-1%'
  AND section NOT IN ('87', '147')
  AND Attendance = 'Normal'
  AND (
    SELECT COUNT(*)
    FROM AcademicCourseTakers AS t
    WHERE t.ID = '14419'
      AND t.classid LIKE '%EHSS-1%'
      AND t.section NOT IN ('87', '147')
      AND t.Attendance = 'Normal'
  ) BETWEEN 2 AND 3;

-- Student: 14437, Grade: B
UPDATE AcademicCourseTakers
SET Grade = 'B'
WHERE ID = '14437'
  AND classid LIKE '%EHSS-1%'
  AND section NOT IN ('87', '147')
  AND Attendance = 'Normal'
  AND (
    SELECT COUNT(*)
    FROM AcademicCourseTakers AS t
    WHERE t.ID = '14437'
      AND t.classid LIKE '%EHSS-1%'
      AND t.section NOT IN ('87', '147')
      AND t.Attendance = 'Normal'
  ) BETWEEN 2 AND 3;

-- Student: 14438, Grade: B
UPDATE AcademicCourseTakers
SET Grade = 'B'
WHERE ID = '14438'
  AND classid LIKE '%EHSS-1%'
  AND section NOT IN ('87', '147')
  AND Attendance = 'Normal'
  AND (
    SELECT COUNT(*)
    FROM AcademicCourseTakers AS t
    WHERE t.ID = '14438'
      AND t.classid LIKE '%EHSS-1%'
      AND t.section NOT IN ('87', '147')
      AND t.Attendance = 'Normal'
  ) BETWEEN 2 AND 3;

-- Student: 14442, Grade: B
UPDATE AcademicCourseTakers
SET Grade = 'B'
WHERE ID = '14442'
  AND classid LIKE '%EHSS-1%'
  AND section NOT IN ('87', '147')
  AND Attendance = 'Normal'
  AND (
    SELECT COUNT(*)
    FROM AcademicCourseTakers AS t
    WHERE t.ID = '14442'
      AND t.classid LIKE '%EHSS-1%'
      AND t.section NOT IN ('87', '147')
      AND t.Attendance = 'Normal'
  ) BETWEEN 2 AND 3;

-- Student: 14444, Grade: C
UPDATE AcademicCourseTakers
SET Grade = 'C'
WHERE ID = '14444'
  AND classid LIKE '%EHSS-1%'
  AND section NOT IN ('87', '147')
  AND Attendance = 'Normal'
  AND (
    SELECT COUNT(*)
    FROM AcademicCourseTakers AS t
    WHERE t.ID = '14444'
      AND t.classid LIKE '%EHSS-1%'
      AND t.section NOT IN ('87', '147')
      AND t.Attendance = 'Normal'
  ) BETWEEN 2 AND 3;

-- Student: 14445, Grade: B
UPDATE AcademicCourseTakers
SET Grade = 'B'
WHERE ID = '14445'
  AND classid LIKE '%EHSS-1%'
  AND section NOT IN ('87', '147')
  AND Attendance = 'Normal'
  AND (
    SELECT COUNT(*)
    FROM AcademicCourseTakers AS t
    WHERE t.ID = '14445'
      AND t.classid LIKE '%EHSS-1%'
      AND t.section NOT IN ('87', '147')
      AND t.Attendance = 'Normal'
  ) BETWEEN 2 AND 3;

-- Student: 14446, Grade: C
UPDATE AcademicCourseTakers
SET Grade = 'C'
WHERE ID = '14446'
  AND classid LIKE '%EHSS-1%'
  AND section NOT IN ('87', '147')
  AND Attendance = 'Normal'
  AND (
    SELECT COUNT(*)
    FROM AcademicCourseTakers AS t
    WHERE t.ID = '14446'
      AND t.classid LIKE '%EHSS-1%'
      AND t.section NOT IN ('87', '147')
      AND t.Attendance = 'Normal'
  ) BETWEEN 2 AND 3;
