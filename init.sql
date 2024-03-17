create database music_metadata;

\c music_metadata

create table artist (
    id uuid primary key,
    name text
);

create table album (
    id uuid primary key,
    name text,
    artist uuid
);

create table recording (
    id UUID primary key,
    name text,
    album uuid,
    length int
);

create extension pg_trgm;
create index recording_trgm_idx on recording using gin(name gin_trgm_ops);