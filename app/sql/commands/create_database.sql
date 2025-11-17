CREATE TABLE user_table (
	user_id SERIAL PRIMARY KEY,
	user_name VARCHAR(100) NOT NULL,
	email VARCHAR(120) NOT NULL,
	password_hash VARCHAR(128) NOT NULL,
	user_type VARCHAR(50) NOT NULL
);

CREATE TABLE government (
	user_id INTEGER PRIMARY KEY,
	department_name VARCHAR(100) NOT NULL,
	FOREIGN KEY  (user_id) REFERENCES user_table (user_id)
);


CREATE TABLE location_table (
	location_id SERIAL PRIMARY KEY,
	address VARCHAR(255) NOT NULL
);

CREATE TABLE field_of_activity (
	field_id SERIAL PRIMARY KEY,
	field_name VARCHAR(100)
);

CREATE TABLE corporate (
	user_id INTEGER PRIMARY KEY,
	cnpj VARCHAR(14) NOT NULL,
	company_name VARCHAR(100) NOT NULL,
	field_id INTEGER NOT NULL,
	FOREIGN KEY  (user_id) REFERENCES user_table (user_id),
	FOREIGN KEY (field_id) REFERENCES field_of_activity (field_id)
);

CREATE TABLE public_work (
	public_work_id SERIAL PRIMARY KEY,
	title VARCHAR(255) NOT NULL,
	description TEXT NOT NULL,
	start_date DATE,
	location_id INTEGER NOT NULL,
	registrant_gov_id INTEGER NOT NULL,
	managing_corp_id INTEGER NOT NULL,
	FOREIGN KEY (location_id) REFERENCES location_table (location_id),
	FOREIGN KEY (registrant_gov_id) REFERENCES government (user_id),
	FOREIGN KEY (managing_corp_id) REFERENCES corporate (user_id)
);

CREATE TABLE colum_table (
	colum_id SERIAL PRIMARY KEY,
	colum_name VARCHAR(100) NOT NULL,
	colum_position INTEGER NOT NULL,
	work_id INTEGER,
	updater_corp_id INTEGER,
	FOREIGN KEY (work_id) REFERENCES public_work (public_work_id),
	FOREIGN KEY (updater_corp_id) REFERENCES corporate (user_id)
);

CREATE TABLE card (
	card_id SERIAL PRIMARY KEY,
	title VARCHAR(255) NOT NULL,
	description TEXT NOT NULL,
	due_date DATE NOT NULL,
	colum_id INTEGER NOT NULL,
	updater_corp_id INTEGER NOT NULL,
	FOREIGN KEY (colum_id) REFERENCES colum_table (colum_id),
	FOREIGN KEY (updater_corp_id) REFERENCES corporate (user_id)
);

CREATE TABLE document_table (
	document_id SERIAL PRIMARY KEY,
	title VARCHAR(255) NOT NULL,
	file_data BYTEA,
	upload_date DATE,
	work_id INTEGER NOT NULL,
	signing_gov_id INTEGER NOT NULL,
	signing_corp_id INTEGER NOT NULL,
	FOREIGN KEY (work_id) REFERENCES public_work (public_work_id),
	FOREIGN KEY (signing_gov_id) REFERENCES government (user_id),
	FOREIGN KEY (signing_corp_id) REFERENCES corporate (user_id)
);
