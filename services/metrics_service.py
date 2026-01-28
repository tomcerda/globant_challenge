from sqlalchemy import text
from app.database import engine

def hires_by_quarter():
    query = text("""
        SELECT
            d.department,
            j.job,
            SUM(CASE WHEN EXTRACT(QUARTER FROM e.datetime)=1 THEN 1 ELSE 0 END) AS q1,
            SUM(CASE WHEN EXTRACT(QUARTER FROM e.datetime)=2 THEN 1 ELSE 0 END) AS q2,
            SUM(CASE WHEN EXTRACT(QUARTER FROM e.datetime)=3 THEN 1 ELSE 0 END) AS q3,
            SUM(CASE WHEN EXTRACT(QUARTER FROM e.datetime)=4 THEN 1 ELSE 0 END) AS q4
        FROM employees e
        JOIN departments d ON e.department_id=d.id
        JOIN jobs j ON e.job_id=j.id
        GROUP BY d.department, j.job
        ORDER BY d.department, j.job
    """)
    with engine.connect() as conn:
        return [dict(row) for row in conn.execute(query).mappings().all()]

def departments_above_mean():
    query = text("""
        WITH hires_per_dept AS (
            SELECT
                d.id,
                d.department,
                COUNT(e.id) AS hired
            FROM employees e
            JOIN departments d ON e.department_id = d.id
            GROUP BY d.id, d.department
        ),
        mean_hires AS (
            SELECT AVG(hired) AS mean_value FROM hires_per_dept
        )
        SELECT
            h.id,
            h.department,
            h.hired
        FROM hires_per_dept h, mean_hires m
        WHERE h.hired > m.mean_value
        ORDER BY h.hired DESC
    """)
    with engine.connect() as conn:
        return [dict(row) for row in conn.execute(query).mappings().all()]
