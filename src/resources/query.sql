WITH
non_zero_distance_trips AS (
    SELECT *,Cast(EXTRACT(EPOCH FROM TO_TIMESTAMP(tpep_dropoff_datetime, 'YYYY-MM-DD HH24:mi:ss'))
             - EXTRACT(EPOCH FROM TO_TIMESTAMP(tpep_pickup_datetime, 'YYYY-MM-DD HH24:mi:ss')) as int) as trip_time,
            CAST(EXTRACT(WEEK FROM TO_TIMESTAMP(tpep_dropoff_datetime, 'YYYY-MM-DD HH24:mi:ss')) as INT) as week_number,
            CAST(EXTRACT(MONTH FROM TO_TIMESTAMP(tpep_dropoff_datetime, 'YYYY-MM-DD HH24:mi:ss')) as INT) as drop_month,
            CAST(EXTRACT(MONTH FROM TO_TIMESTAMP(tpep_pickup_datetime, 'YYYY-MM-DD HH24:mi:ss')) as INT) as pickup_month
    FROM trip
    WHERE trip_distance<>0
),
non_zero_distance_time_trips AS (
    SELECT *
    FROM non_zero_distance_trips
    WHERE trip_time <> 0 AND drop_month=3 AND pickup_month=3
),
trip_avg_speed AS (
    SELECT sum(trip_distance/trip_time)/31 AS avg_speed
    FROM non_zero_distance_time_trips
),
trip_enriched AS (
    SELECT *, (trip_distance/trip_time) AS speed
    FROM non_zero_distance_time_trips,trip_avg_speed
),
trip_grouped AS (
    SELECT week_number, PULocationID, min(speed) as min_speed
    FROM
    trip_enriched
    WHERE avg_speed>speed
    GROUP BY week_number,PULocationID
),
trip_partitioned AS (
    SELECT *,
    ROW_NUMBER() OVER (PARTITION BY week_number ORDER BY min_speed) AS row_number
    FROM trip_grouped
)
SELECT week_number-10 as march_week ,PULocationID FROM trip_partitioned WHERE row_number<6 ORDER BY week_number;
