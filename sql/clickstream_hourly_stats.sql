SELECT
    time_bucket('1 hour', timestamp) AS hour,
    session_id,
    COUNT(*) AS event_count,
    COUNT(DISTINCT user_id) AS unique_users,
    COUNT(DISTINCT page_url) AS unique_pages
FROM
    clickstream_events
GROUP BY
    hour, session_id
ORDER BY
    hour DESC, event_count DESC, session_id;