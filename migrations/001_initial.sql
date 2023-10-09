CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE resourcetype (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    max_speed INTEGER NOT NULL
);

CREATE TABLE resource (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type_id UUID REFERENCES resourcetype(id),
    current_speed INTEGER NOT NULL
);
