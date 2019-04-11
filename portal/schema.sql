DROP TABLE IF EXISTS users;

CREATE TABLE users (
    user_id bigserial PRIMARY KEY,
    email text UNIQUE NOT NULL,
    password text NOT NULL,
    role varchar(7) NOT NULL CHECK (role IN ('teacher', 'student'))
);

CREATE TABLE courses (
    course_id bigserial PRIMARY KEY,
    course varchar(15) UNIQUE NOT NULL,
    title varchar(100) NOT NULL,
    meets varchar(50) NOT NULL,
    instructor varchar(100) REFERENCES users(user_id)
);
