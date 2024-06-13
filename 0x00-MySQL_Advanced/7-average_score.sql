-- Calculate average score for a given user
DELIMITER $$
CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INT)
BEGIN
    DECLARE total_score FLOAT;
    DECLARE score_count INT;
    
    -- Calculate total score for the user
    SELECT SUM(score) INTO total_score FROM corrections WHERE user_id = user_id;
    
    -- Calculate number of corrections for the user
    SELECT COUNT(*) INTO score_count FROM corrections WHERE user_id = user_id;
    
    -- Calculate average score
    IF score_count > 0 THEN
        UPDATE users SET average_score = total_score / score_count WHERE id = user_id;
    ELSE
        -- If no corrections for the user, set average score to 0
        UPDATE users SET average_score = 0 WHERE id = user_id;
    END IF;
END$$
DELIMITER ;
