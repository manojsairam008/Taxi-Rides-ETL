SELECT *,
Cast(EXTRACT(EPOCH FROM TO_TIMESTAMP(tpep_dropoff_datetime, 'YYYY-MM-DD HH24:mi:ss'))
 - EXTRACT(EPOCH FROM TO_TIMESTAMP(tpep_pickup_datetime, 'YYYY-MM-DD HH24:mi:ss')) as int) as diff
 FROM trip;
