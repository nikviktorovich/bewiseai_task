CREATE TABLE IF NOT EXISTS quizzes (
    id INT PRIMARY KEY,
    question VARCHAR NOT NULL,
    answer VARCHAR NOT NULL,
    created_at TIMESTAMP NOT NULL
);