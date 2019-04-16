DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS courses;

CREATE TABLE users (
    user_id bigserial PRIMARY KEY,
    email text UNIQUE NOT NULL,
    password text NOT NULL,
    role varchar(7) NOT NULL CHECK (role IN ('teacher', 'student')),
    user_name varchar(200) NOT NULL
);

CREATE TABLE courses (
    course_id bigserial PRIMARY KEY,
    course_number varchar(15) NOT NULL,
    course_title varchar(100) NOT NULL,
    instructor_id integer REFERENCES users(user_id)
);
