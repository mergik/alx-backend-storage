-- creates a stored procedure that computes and store the average weighted score for all students
DELIMITER $$

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
	UPDATE users
	JOIN corrections
	ON corrections.user_id = users.id
	SET average_score = (
		SELECT SUM(score * weight) / SUM(weight * 100) * 100
		FROM corrections
		JOIN projects
		ON corrections.project_id = projects.id
		WHERE users.id = corrections.user_id);
END $$
