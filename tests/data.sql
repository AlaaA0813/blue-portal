-- Mock Data For Tests

INSERT INTO users (email, password, role, name)
VALUES ('teacher@stevenscollege.edu', 'pbkdf2:sha256:150000$nasr7fgN$56db30f9e2ef90e44569b5e5b4037cb2f5065a51f760a8cdc08b4c698e805486', 'teacher', 'bob'),
       ('student@stevenscollege.edu', 'pbkdf2:sha256:150000$dNYOatzF$3540f5ede0fea957e98badb530d7032b2ffd3fdcfa4ae79611a070fcf1b2074d', 'student', 'mary'),
       ('student2@stevenscollege.edu', 'pbkdf2:sha256:150000$dNYOatzF$3540f5ede0fea957e98cadb530d7032b2ffd3fdcfa4ae79611a070fcf1b2074d', 'student', 'gary'),
       ('student3@stevenscollege.edu', 'pbkdf2:sha256:150000$dNYOatzF$3540f5ede0fea957e98dadb530d7032b2ffd3fdcfa4ae79611a070fcf1b2074d', 'student', 'jary'),
       ('student4@stevenscollege.edu', 'pbkdf2:sha256:150000$dNYOatzF$3540f5ede0fea957e98eadb530d7032b2ffd3fdcfa4ae79611a070fcf1b2074d', 'student', 'kary');

INSERT INTO courses (course_number, course_title, instructor_id)
VALUES ('1', 'Math', 1),
       ('2', 'English', 1);

INSERT INTO sessions (letter, course_id, meets)
VALUES ('A', 1, 'MWF'),
       ('B', 1, 'TR'),
       ('A', 2, 'MTWRF');

INSERT INTO user_sessions (student_id, session_id, student_email)
VALUES (2, 1, 'student@stevenscollege.edu'),
       (3, 1, 'student2@stevenscollege.edu'),
       (4, 1, 'student3@stevenscollege.edu'),
       (2, 2, 'student@stevenscollege.edu'),
       (3, 2, 'student2@stevenscollege.edu'),
       (3, 3, 'student2@stevenscollege.edu'),
       (4, 3, 'student3@stevenscollege.edu');
