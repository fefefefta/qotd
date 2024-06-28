GET_QUESTION_FOR_DATE = """
    SELECT
        id,
        title,
        text
    FROM
        Question
    WHERE
        pub_date = :date
"""


GET_COMMENTS_FOR_QUESTION = """
    WITH RECURSIVE CommentHierarchy AS (
    -- Получаем все комментарии верхнего уровня для заданного question_id
        SELECT
            c.id,
            c.text,
            c.question_id,
            c.parent_id,
            c.user_id,
            c.pub_ts,
            (SELECT username FROM "User" WHERE id = c.user_id) AS username,
            (SELECT COUNT(*) FROM Vote v WHERE v.comment_id = c.id) AS upvotes,
            EXISTS (SELECT 1 FROM Vote v WHERE v.comment_id = c.id AND v.user_id = :user_id) AS voted,
            1 AS depth
        FROM Comment c
        WHERE c.question_id = :question_id AND c.parent_id IS NULL

        UNION ALL

        -- Рекурсивно получаем все вложенные комментарии
        SELECT
            c.id,
            c.text,
            c.question_id,
            c.parent_id,
            c.user_id,
            c.pub_ts,
            (SELECT username FROM "User" WHERE id = c.user_id) AS username,
            (SELECT COUNT(*) FROM Vote v WHERE v.comment_id = c.id) AS upvotes,
            EXISTS (SELECT 1 FROM Vote v WHERE v.comment_id = c.id AND v.user_id = :user_id) AS voted,
            ch.depth + 1 AS depth
        FROM Comment c
        INNER JOIN CommentHierarchy ch ON c.parent_id = ch.id
    )
    SELECT * FROM CommentHierarchy ORDER BY depth, pub_ts
"""


CREATE_USER = '''
    INSERT INTO "User" (id, username) VALUES (:user_id, :username)
    RETURNING id, username
'''


GET_USER = '''
    SELECT id, username FROM "User" WHERE id = :user_id
'''


CHECK_USER_VOTED = """
    SELECT EXISTS(SELECT * FROM vote WHERE user_id = :user_id AND comment_id = :comment_id)
"""


VOTE_COMMENT = """
    INSERT INTO vote (user_id, comment_id) VALUES (:user_id, :comment_id)
    RETURNING id, user_id, comment_id, TRUE AS vote_type
"""


UNVOTE_COMMENT = """
    DELETE FROM vote WHERE user_id = :user_id AND comment_id = :comment_id
    RETURNING id, user_id, comment_id, FALSE AS vote_type
"""


CREATE_COMMENT = """
    INSERT INTO comment (user_id, question_id, parent_id, text, pub_ts)
    VALUES (:user_id, :question_id, :parent_id, :text, CURRENT_TIMESTAMP)
    RETURNING id, text, user_id, (SELECT username FROM "User" WHERE id = :user_id) as username, question_id, parent_id, pub_ts, (SELECT COUNT(*) FROM vote v WHERE v.comment_id = id) AS upvotes, FALSE AS voted
"""