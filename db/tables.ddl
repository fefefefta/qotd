CREATE TABLE "User" (
    id VARCHAR(64) PRIMARY KEY,
    username VARCHAR(255) NOT NULL
);

CREATE TABLE Question (
    id SERIAL PRIMARY KEY,
    pub_date DATE NOT NULL,
    title TEXT NOT NULL,
    text TEXT
);

CREATE TABLE Comment (
    id SERIAL PRIMARY KEY,
    text TEXT NOT NULL,
    upvotes INTEGER DEFAULT 0,
    question_id INT NOT NULL,
    parent_id INT,
    user_id VARCHAR(64) NOT NULL,
    pub_ts TIMESTAMP WITH TIME ZONE NOT NULL,

    CONSTRAINT fk_question
        FOREIGN KEY (question_id)
        REFERENCES Question (id)
        ON DELETE CASCADE,

    CONSTRAINT fk_parent
        FOREIGN KEY (parent_id)
        REFERENCES Comment (id)
        ON DELETE CASCADE,

    CONSTRAINT fk_user
        FOREIGN KEY (user_id)
        REFERENCES "User" (id)
        ON DELETE CASCADE
);

CREATE TABLE Vote (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(64) NOT NULL,
    comment_id INT NOT NULL,

    CONSTRAINT fk_user
        FOREIGN KEY (user_id)
        REFERENCES "User" (id)
        ON DELETE CASCADE,

    CONSTRAINT fk_comment
        FOREIGN KEY (comment_id)
        REFERENCES Comment (id)
        ON DELETE CASCADE
);

-- Inserting test data
-- Insert a user
INSERT INTO "User" (id, username) VALUES ('dklkdkdkdkkdkdkkdkd', 'testuser');

-- Insert a question
INSERT INTO Question (pub_date, title, text) VALUES ('2024-05-11', 'Test Question Title', 'This is a test question text.');

-- Insert comments
-- First comment (top-level comment)
INSERT INTO Comment (text, question_id, user_id, pub_ts) VALUES ('This is a top-level comment.', (SELECT id FROM Question WHERE title='Test Question Title'), (SELECT id FROM "User" WHERE username='testuser'), NOW());

-- Second comment (reply to the first comment)
INSERT INTO Comment (text, question_id, parent_id, user_id, pub_ts) VALUES ('This is a reply to the first comment.', (SELECT id FROM Question WHERE title='Test Question Title'), (SELECT id FROM Comment WHERE text='This is a top-level comment.'), (SELECT id FROM "User" WHERE username='testuser'), NOW());