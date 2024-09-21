CREATE DATABASE dental_management_db;

GRANT ALL ON SCHEMA public TO myuser; -- replace myuser to YOUR USER NAME
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO myuser;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO myuser;
GRANT USAGE, CREATE ON SCHEMA public TO myuser;

INSERT INTO public.doctors_specialty(id, name) VALUES 
    (1, 'Cleaning'),
	(2, 'Filling'),
	(3, 'Root Canal'),
	(4, 'Crown'),
	(5, 'Teeth Whitening')	;
