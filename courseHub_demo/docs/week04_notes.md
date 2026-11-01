# CourseHub - Buoi 4

- Migration 001: enrollment_events.
- Demo class: RACE-01, capacity = 1.
- POST /enrollments: lock class_sections bang FOR UPDATE.
- Concurrency test: 1 request 201, 1 request 409.
- Performance data: 100000 rows, dataset=performance.
- Index: idx_enrollment_events_dataset_student_time.
- Ghi lai scan type va Execution Time truoc/sau o day.

Planning Time: 1.637 ms
Execution Time: 4.018 ms

Sau khi tạo composite index:

"Index Scan using idx_enrollment_events_dataset_student_time on enrollment_events  (cost=0.42..1117.97 rows=833 width=39) (actual time=0.048..0.084 rows=50.00 loops=1)"
"Buffers: shared hit=39 read=1"
"Planning Time: 1.145 ms"
"Execution Time: 0.098 ms"

Khong commit backend/.env.