-- Procedure to compute and store the average score for a user
DELIMITER $$

CREATE PROCEDURE ComputeAverageScoreForUser(
    IN user_id INT
)
BEGIN
    DECLARE total_score FLOAT;
    DECLARE total_count INT;
    DECLARE avg_score FLOAT;

    -- Compute total score for the user
    SELECT SUM(score) INTO total_score FROM corrections WHERE user_id = user_id;

    -- Compute total count of corrections for the user
    SELECT COUNT(*) INTO total_count FROM corrections WHERE user_id = user_id;

    -- Calculate average score
    IF total_count > 0 THEN
        SET avg_score = total_score / total_count;
    ELSE
        SET avg_score = 0;
    END IF;

    -- Update average_score for the user
    UPDATE users SET average_score = avg_score WHERE id = user_id;
END $$

DELIMITER ;
