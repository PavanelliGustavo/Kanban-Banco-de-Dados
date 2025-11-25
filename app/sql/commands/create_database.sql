CREATE TABLE tb_corporate (
    id SERIAL PRIMARY KEY,
    cnpj VARCHAR(14) NOT NULL,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    password VARCHAR(128) NOT NULL
);

CREATE TABLE tb_government (
    id SERIAL PRIMARY KEY,
    user_name VARCHAR(100) NOT NULL,
    department_name VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    password VARCHAR(128) NOT NULL
);

CREATE TABLE tb_location (
    id SERIAL PRIMARY KEY,
    address VARCHAR(255) NOT NULL
);

CREATE TABLE tb_field_of_activity (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE tb_public_work (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    start_date DATE,
    location_id INTEGER NOT NULL,
    government_id INTEGER NOT NULL,
    corporate_id INTEGER NOT NULL,
    FOREIGN KEY (location_id) REFERENCES tb_location (id) ON DELETE CASCADE,
    FOREIGN KEY (government_id) REFERENCES tb_government (id) ON DELETE CASCADE,
    FOREIGN KEY (corporate_id) REFERENCES tb_corporate (id) ON DELETE CASCADE
);

CREATE TABLE tb_column (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    position INTEGER NOT NULL,
    public_work_id INTEGER,
    corporate_id INTEGER,
    FOREIGN KEY (public_work_id) REFERENCES tb_public_work (id) ON DELETE CASCADE,
    FOREIGN KEY (corporate_id) REFERENCES tb_corporate (id) ON DELETE CASCADE
);

CREATE TABLE tb_card (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    deadline DATE NOT NULL,
    column_id INTEGER NOT NULL,
    corporate_id INTEGER NOT NULL,
    FOREIGN KEY (column_id) REFERENCES tb_kanban_column (id) ON DELETE CASCADE,
    FOREIGN KEY (corporate_id) REFERENCES tb_corporate (id) ON DELETE CASCADE
);

CREATE TABLE tb_document (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    file_data BYTEA,
    upload_date DATE,
    public_work_id INTEGER NOT NULL,
    government_id INTEGER NOT NULL,
    corporate_id INTEGER NOT NULL,
    FOREIGN KEY (public_work_id) REFERENCES tb_public_work (id) ON DELETE CASCADE,
    FOREIGN KEY (government_id) REFERENCES tb_government (id) ON DELETE CASCADE,
    FOREIGN KEY (corporate_id) REFERENCES tb_corporate (id) ON DELETE CASCADE
);

CREATE TABLE tb_corporate_field_of_activity (
    corporate_id INT NOT NULL,
    field_of_activity_id INT NOT NULL,
    PRIMARY KEY (corporate_id, field_of_activity_id),
    FOREIGN KEY (corporate_id) REFERENCES tb_corporate (id) ON DELETE CASCADE,
    FOREIGN KEY (field_of_activity_id) REFERENCES tb_field_of_activity (id) ON DELETE CASCADE
);

CREATE TABLE tb_public_work_field_of_activity (
    public_work_id INT NOT NULL,
    field_of_activity_id INT NOT NULL,
    PRIMARY KEY (public_work_id, field_of_activity_id),
    FOREIGN KEY (public_work_id) REFERENCES tb_public_work (id) ON DELETE CASCADE,
    FOREIGN KEY (field_of_activity_id) REFERENCES tb_field_of_activity (id) ON DELETE CASCADE
);