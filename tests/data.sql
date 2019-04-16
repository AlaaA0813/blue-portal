-- Mock Data For Tests

INSERT INTO users (email, password, role)
VALUES ('teacher@stevenscollege.edu', 'pbkdf2:sha256:150000$nasr7fgN$56db30f9e2ef90e44569b5e5b4037cb2f5065a51f760a8cdc08b4c698e805486', 'teacher'),
       ('student@stevenscollege.edu', 'pbkdf2:sha256:150000$dNYOatzF$3540f5ede0fea957e98badb530d7032b2ffd3fdcfa4ae79611a070fcf1b2074d', 'student');
