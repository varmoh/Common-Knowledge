--liquibase formatted sql
--changeset varmoh:20250909-01
CREATE TABLE "user" (
    id BIGSERIAL PRIMARY KEY,
    login VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(60),
    first_name VARCHAR(50),
    last_name VARCHAR(50)
);

CREATE TABLE authority (
    name VARCHAR(50) PRIMARY KEY
);

CREATE TABLE user_authority (
    user_id BIGINT NOT NULL,
    authority_name VARCHAR(50) NOT NULL,
    PRIMARY KEY (user_id, authority_name),
    CONSTRAINT fk_authority_name FOREIGN KEY (authority_name)
        REFERENCES authority(name),
    CONSTRAINT fk_user_id FOREIGN KEY (user_id)
        REFERENCES "user"(id)
);
