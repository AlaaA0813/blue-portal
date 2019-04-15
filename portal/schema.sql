DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS courses;

CREATE TABLE users (
    user_id bigserial PRIMARY KEY,
    email text UNIQUE NOT NULL,
    password text NOT NULL,
    role varchar(7) NOT NULL CHECK (role IN ('teacher', 'student')),
    name varchar(200) NOT NULL
);

CREATE TABLE courses (
    course_number varchar(15) PRIMARY KEY,
    course_title varchar(100) NOT NULL,
    instructor integer REFERENCES users(user_id)
);
