CREATE TABLE cities (
	id SERIAL PRIMARY KEY,
	city VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE employers (
	id SERIAL PRIMARY KEY,
	city_id INTEGER NULL,
	employer VARCHAR(100) UNIQUE NOT NULL,

	CONSTRAINT fk_city
        	FOREIGN KEY(city_id) 
	  		REFERENCES cities(id)
			ON DELETE SET NULL
);

CREATE TABLE addresses (
	id SERIAL PRIMARY KEY,
	city_id INTEGER NULL,
	employer_id INTEGER NULL,
	address VARCHAR(255) UNIQUE NOT NULL,

	CONSTRAINT fk_city
        	FOREIGN KEY(city_id) 
	  		REFERENCES cities(id)
			ON DELETE SET NULL,
	CONSTRAINT fk_employer
        	FOREIGN KEY(employer_id) 
	  		REFERENCES employers(id)
			ON DELETE SET NULL
);

CREATE TABLE salary_modes (
	id SERIAL PRIMARY KEY,
	salary_mode VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE experiences (
	id SERIAL PRIMARY KEY NOT NULL,
	experience VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE jobs (
	id SERIAL PRIMARY KEY,
	url VARCHAR(255) UNIQUE NOT NULL,
	title VARCHAR(255) NOT NULL,
	salary_from INTEGER NULL,
	salary_to INTEGER NULL,
	salary_mode_id INTEGER NULL,
	address_id INTEGER NULL,
	experience_id INTEGER NULL,
	date DATE NULL,
	description TEXT NULL,
	employer_id INTEGER NULL,

	CONSTRAINT fk_salary_mode
        	FOREIGN KEY(salary_mode_id) 
	  		REFERENCES salary_modes(id)
			ON DELETE SET NULL,
	CONSTRAINT fk_address
        	FOREIGN KEY(address_id) 
	  		REFERENCES addresses(id)
			ON DELETE SET NULL,
	CONSTRAINT fk_experience
        	FOREIGN KEY(experience_id) 
	  		REFERENCES experiences(id)
			ON DELETE SET NULL,
	CONSTRAINT fk_employer
        	FOREIGN KEY(employer_id) 
	  		REFERENCES employers(id)
			ON DELETE SET NULL
);

CREATE TABLE employment_modes (
	id SERIAL PRIMARY KEY,
	employment_mode VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE job_employment_modes (
	job_id INTEGER NOT NULL,
	employment_mode_id INTEGER NOT NULL,
	PRIMARY KEY (job_id, employment_mode_id),

	CONSTRAINT fk_job
        	FOREIGN KEY(job_id) 
	  		REFERENCES jobs(id)
			ON DELETE SET NULL,
	CONSTRAINT fk_employment_mode
        	FOREIGN KEY(employment_mode_id) 
	  		REFERENCES employment_modes(id)
			ON DELETE SET NULL
);

CREATE TABLE skills (
	id SERIAL PRIMARY KEY,
	skill VARCHAR(300) UNIQUE NOT NULL
);

CREATE TABLE job_skills (
	job_id INTEGER NOT NULL,
	skill_id INTEGER NOT NULL,
	PRIMARY KEY (job_id, skill_id),

	CONSTRAINT fk_job
        	FOREIGN KEY(job_id) 
	  		REFERENCES jobs(id)
			ON DELETE SET NULL,
	CONSTRAINT fk_skill
        	FOREIGN KEY(skill_id) 
	  		REFERENCES skills(id)
			ON DELETE SET NULL
);