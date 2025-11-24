CREATE TABLE IF NOT EXISTS sessions (
    id UUID PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    telegram_user_id BIGINT,
    telegram_username TEXT,
    consent_given BOOLEAN DEFAULT false,
    consent_at TIMESTAMP WITH TIME ZONE,
    notes JSONB
);

CREATE TABLE IF NOT EXISTS visits (
    id BIGSERIAL PRIMARY KEY,
    session_id UUID REFERENCES sessions(id) ON DELETE CASCADE,
    ip TEXT,
    user_agent TEXT,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT now(),
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    city TEXT,
    region TEXT,
    country TEXT,
    provider TEXT,
    raw_geodata JSONB
);

CREATE INDEX IF NOT EXISTS visits_session_idx ON visits(session_id);
CREATE INDEX IF NOT EXISTS visits_ts_idx ON visits(timestamp);
