CREATE DATABASE digit;
USE digit;

CREATE TABLE classification_data (
    id SERIAL PRIMARY KEY,
    image BYTEA
    prediction VARCHAR(1)
);
