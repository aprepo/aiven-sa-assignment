-- Enable TimescaleDB extension
CREATE EXTENSION IF NOT EXISTS timescaledb;

-- Create the clickstream events table
CREATE TABLE IF NOT EXISTS clickstream_events (
    timestamp TIMESTAMPTZ NOT NULL,
    event_id UUID DEFAULT gen_random_uuid(), -- Rather make this NOT NULL and don't set default
    user_id UUID NOT NULL,
    session_id UUID NOT NULL,
    event_type TEXT NOT NULL,
    page_url TEXT NOT NULL,
    referrer_url TEXT,
    user_agent TEXT,
    ip_address INET,
    device TEXT
);

-- Convert it into a TimescaleDB hypertable
SELECT create_hypertable('clickstream_events', 'timestamp');

-- Instead of a primary key, we create a unique index
CREATE UNIQUE INDEX clickstream_event_idx ON clickstream_events (event_id, timestamp);

-- Add indexes for performance
CREATE INDEX ON clickstream_events (timestamp DESC);

-- Create a table for session stats calculated by the kafka consumer script
CREATE TABLE IF NOT EXISTS clickstream_session_stats (
    session_id UUID PRIMARY KEY,
    page_views BIGINT NOT NULL,
    button_clicks BIGINT NOT NULL
);