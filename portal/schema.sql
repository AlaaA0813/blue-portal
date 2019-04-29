DROP TABLE IF EXISTS assignments;
DROP TABLE IF EXISTS user_sessions CASCADE;
DROP TABLE IF EXISTS sessions;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id bigserial PRIMARY KEY,
    email text UNIQUE NOT NULL,
    password text NOT NULL,
    role varchar(7) NOT NULL CHECK (role IN ('teacher', 'student')),
    name varchar(200) NOT NULL
);

CREATE TABLE courses (
    id bigserial PRIMARY KEY,
    course_number varchar(15) NOT NULL,
    course_title varchar(100) NOT NULL,
    instructor_id integer REFERENCES users(id)
);

CREATE TABLE sessions (
    id bigserial PRIMARY KEY,
    letter char(1) NOT NULL,
    course_id integer REFERENCES courses(id),
    meets text NOT NULL
);

CREATE TABLE user_sessions (
  student_id integer REFERENCES users(id),
  session_id integer REFERENCES sessions(id),
  student_email text REFERENCES users(email)
);

CREATE TABLE assignments (
    id bigserial PRIMARY KEY,
    assignment_name varchar(200) NOT NULL,
    assignment_description text NOT NULL,
    course_id integer REFERENCES courses(id)
    -- type varchar(7) NOT NULL CHECK (type IN ('default', 'file')),
);
