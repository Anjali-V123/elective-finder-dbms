-- TRIGGERS
DELIMITER //
CREATE TRIGGER CGPA_check
BEFORE INSERT ON Student
FOR EACH ROW
BEGIN
  IF NEW.CGPA IS NOT NULL AND (NEW.CGPA > 10.00 OR NEW.CGPA < 0.00) THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Invalid CGPA';
  END IF;
END//
DELIMITER ;

DELIMITER //
CREATE TRIGGER DOB_check
BEFORE INSERT ON Student
FOR EACH ROW
BEGIN
  IF NEW.DOB IS NOT NULL AND YEAR(NEW.DOB) > YEAR(CURDATE()) - 15 THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Invalid DOB';
  END IF;
END//
DELIMITER ;

DELIMITER //
CREATE TRIGGER update_elective
AFTER INSERT ON Belongs_To
FOR EACH ROW
BEGIN
  DECLARE Average_Grade DECIMAL(5,2);
  DECLARE Difficulty_Level VARCHAR(20);

  SELECT AVG(b.grade) INTO Average_Grade
  FROM Belongs_To b
  JOIN Student s ON b.SRN=s.SRN
  WHERE b.Course_ID = NEW.Course_ID
    AND s.Graduated_year = YEAR(CURDATE()) - 1;

  IF Average_Grade IS NULL THEN
    SET Average_Grade = 0;
  END IF;

  IF Average_Grade >= 80 THEN
    SET Difficulty_Level = 'EASY';
  ELSEIF Average_Grade >= 60 THEN
    SET Difficulty_Level = 'MEDIUM';
  ELSEIF Average_Grade >= 40 THEN
    SET Difficulty_Level = 'HARD';
  ELSE
    SET Difficulty_Level = 'EXTREME';
  END IF;

  UPDATE Elective SET Avg_Grade = Average_Grade, Difficulty = Difficulty_Level
  WHERE Course_ID = NEW.Course_ID;
END//
DELIMITER ;

-- PROCEDURES (fulltext)
DELIMITER &&
CREATE PROCEDURE interest_matcher_project(IN interest VARCHAR(255))
BEGIN
  SELECT Project_name, Project_Year
  FROM Projects
  WHERE MATCH(Project_name) AGAINST (interest IN NATURAL LANGUAGE MODE)
  ORDER BY MATCH(Project_name) AGAINST (interest IN NATURAL LANGUAGE MODE) DESC
  LIMIT 5;
END &&
DELIMITER ;

DELIMITER &&
CREATE PROCEDURE interest_matcher_elective(IN interest VARCHAR(255))
BEGIN
  SELECT Course_Name
  FROM Elective
  WHERE MATCH(Syllabus) AGAINST (interest IN NATURAL LANGUAGE MODE)
  ORDER BY MATCH(Syllabus) AGAINST (interest IN NATURAL LANGUAGE MODE) DESC
  LIMIT 5;
END &&
DELIMITER ;

DELIMITER &&
CREATE PROCEDURE pastproject_matcher_project(IN pastproject VARCHAR(255))
BEGIN
  SELECT Project_name, Project_Year
  FROM Projects
  WHERE MATCH(Project_name) AGAINST (pastproject IN NATURAL LANGUAGE MODE)
  ORDER BY MATCH(Project_name) AGAINST (pastproject IN NATURAL LANGUAGE MODE) DESC
  LIMIT 5;
END &&
DELIMITER ;

DELIMITER &&
CREATE PROCEDURE pastproject_matcher_elective(IN pastproject VARCHAR(255))
BEGIN
  SELECT Course_Name
  FROM Elective
  WHERE MATCH(Syllabus) AGAINST (pastproject IN NATURAL LANGUAGE MODE)
  ORDER BY MATCH(Syllabus) AGAINST (pastproject IN NATURAL LANGUAGE MODE) DESC
  LIMIT 5;
END &&
DELIMITER ;