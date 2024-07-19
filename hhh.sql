CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create tables
CREATE TABLE Users (
    UID UUID PRIMARY KEY,
    Username VARCHAR(50) NOT NULL,
    Email VARCHAR(100) NOT NULL,
    HashPW VARCHAR(255) NOT NULL
);

CREATE TABLE Admins (
    UID UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    FOREIGN KEY (UID) REFERENCES Users(UID) ON DELETE CASCADE
);

CREATE TABLE Players (
    UID UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    FOREIGN KEY (UID) REFERENCES Users(UID) ON DELETE CASCADE
);

CREATE TABLE Quests (
    QID UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    QuestName VARCHAR(100) NOT NULL,
    UID UUID NOT NULL,
    FOREIGN KEY (UID) REFERENCES Admins(UID),
    UNIQUE (QID, UID)
);

CREATE TABLE Topics (
    Type VARCHAR(50) PRIMARY KEY
);

CREATE TABLE Problems (
    PID UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    ProblemLink VARCHAR(255) NOT NULL,
    Difficulty VARCHAR(20) NOT NULL
);

CREATE TABLE ProblemTopics (
    PID UUID,
    Type VARCHAR(50),
    PRIMARY KEY (PID, Type),
    FOREIGN KEY (PID) REFERENCES Problems(PID),
    FOREIGN KEY (Type) REFERENCES Topics(Type)
);

CREATE TABLE QuestProblems (
    QID UUID,
    PID UUID,
    PRIMARY KEY (QID, PID),
    FOREIGN KEY (QID) REFERENCES Quests(QID),
    FOREIGN KEY (PID) REFERENCES Problems(PID)
);

CREATE TABLE CompletedProblems (
    UID UUID,
    PID UUID,
    CompletionDate TIMESTAMP NOT NULL,
    PRIMARY KEY (UID, PID),
    FOREIGN KEY (UID) REFERENCES Players(UID) ON DELETE CASCADE,
    FOREIGN KEY (PID) REFERENCES Problems(PID)
);

CREATE TABLE PlayerQuests (
    UID UUID,
    QID UUID,
    IsCompleted BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (UID, QID),
    FOREIGN KEY (UID) REFERENCES Players(UID) ON DELETE CASCADE,
    FOREIGN KEY (QID) REFERENCES Quests(QID)
);

-- Create views
CREATE MATERIALIZED VIEW UsersView AS
SELECT UID, Username, Email
FROM Users;

CREATE VIEW HardestPlayers AS
SELECT u.UID, u.Username, u.Email, COUNT(*) as HardProblemCount
FROM Users u
JOIN CompletedProblems cp ON u.UID = cp.UID
JOIN Problems p ON cp.PID = p.PID
WHERE LOWER(p.Difficulty) = 'hard'
GROUP BY u.UID, u.Username, u.Email
ORDER BY HardProblemCount DESC;

-- Create functions


-- Create triggers

-- Enforces distinct Subclasses --
-- Used to prevent Admins from being Players
CREATE OR REPLACE FUNCTION check_admin_player_conflict()
RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM Players WHERE UID = NEW.UID) THEN
        RAISE EXCEPTION 'User is already a Player';
    END IF;
    -- ensures new row is passed if no exception
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER admin_player_conflict_check
BEFORE INSERT ON Admins
FOR EACH ROW
EXECUTE FUNCTION check_admin_player_conflict();

-- Used to prevent Players from being Admins
CREATE OR REPLACE FUNCTION check_player_admin_conflict()
RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM Admins WHERE UID = NEW.UID) THEN
        RAISE EXCEPTION 'User is already an Admin';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER player_admin_conflict_check
BEFORE INSERT ON Players
FOR EACH ROW
EXECUTE FUNCTION check_player_admin_conflict();
-----------------------------------

-- prevents non-admins from creating quests
CREATE OR REPLACE FUNCTION check_quest_creator()
RETURNS TRIGGER AS $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM Admins WHERE UID = NEW.UID) THEN
        RAISE EXCEPTION 'Only Admins can create Quests';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER quest_creator_check
BEFORE INSERT ON Quests
FOR EACH ROW
EXECUTE FUNCTION check_quest_creator();

-- prevent problem or topic from being added to ProblemTopics if they do not exist
CREATE OR REPLACE FUNCTION check_problem_topic()
RETURNS TRIGGER AS $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM Problems WHERE PID = NEW.PID) THEN
        RAISE EXCEPTION 'Problem does not exist';
    END IF;
    IF NOT EXISTS (SELECT 1 FROM Topics WHERE Type = NEW.Type) THEN
        RAISE EXCEPTION 'Topic does not exist';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER problem_topic_check
BEFORE INSERT ON ProblemTopics
FOR EACH ROW
EXECUTE FUNCTION check_problem_topic();

-- prevent quest or problem from being added to QuestProblems if they do not exist
CREATE OR REPLACE FUNCTION check_quest_problem()
RETURNS TRIGGER AS $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM Quests WHERE QID = NEW.QID) THEN
        RAISE EXCEPTION 'Quest does not exist';
    END IF;
    IF NOT EXISTS (SELECT 1 FROM Problems WHERE PID = NEW.PID) THEN
        RAISE EXCEPTION 'Problem does not exist';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER quest_problem_check
BEFORE INSERT ON QuestProblems
FOR EACH ROW
EXECUTE FUNCTION check_quest_problem();

-- prevent user or problem from being added to CompletedProblems if they do not exist
CREATE OR REPLACE FUNCTION check_completed_problem()
RETURNS TRIGGER AS $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM Users WHERE UID = NEW.UID) THEN
        RAISE EXCEPTION 'User does not exist';
    END IF;
    IF NOT EXISTS (SELECT 1 FROM Problems WHERE PID = NEW.PID) THEN
        RAISE EXCEPTION 'Problem does not exist';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER completed_problem_check
BEFORE INSERT ON CompletedProblems
FOR EACH ROW
EXECUTE FUNCTION check_completed_problem();

-- prevent user or quest from being added to PlayerQuests if they do not exist
CREATE OR REPLACE FUNCTION check_player_quest()
RETURNS TRIGGER AS $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM Users WHERE UID = NEW.UID) THEN
        RAISE EXCEPTION 'User does not exist';
    END IF;
    IF NOT EXISTS (SELECT 1 FROM Quests WHERE QID = NEW.QID) THEN
        RAISE EXCEPTION 'Quest does not exist';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER player_quest_check
BEFORE INSERT ON PlayerQuests
FOR EACH ROW
EXECUTE FUNCTION check_player_quest();

-- replaces the UID of a deleted admin with the default admin UID in Quests
CREATE OR REPLACE FUNCTION update_quest_admin()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE Quests
    SET UID = '00000000-0000-0000-0000-000000000000'::UUID
    WHERE UID = OLD.UID;
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

-- in the case that an admin is deleted, we do not want Quests to have NULL as the UID
CREATE TRIGGER update_quest_admin_trigger
BEFORE DELETE ON Admins
FOR EACH ROW
EXECUTE FUNCTION update_quest_admin();

-- updates the IsCompleted field in PlayerQuests when all problems in a quest are completed
CREATE OR REPLACE FUNCTION update_player_quest_completion()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE PlayerQuests pq
    -- subquery returns true or false based on if the count of completed problems for a quest is equal to the count of problems in the quest
    SET IsCompleted = (
        SELECT CASE
            WHEN COUNT(*) = (SELECT COUNT(*) FROM QuestProblems WHERE QID = pq.QID)
            THEN TRUE
            ELSE FALSE
        END
        FROM QuestProblems qp
        JOIN CompletedProblems cp ON qp.PID = cp.PID
        WHERE qp.QID = pq.QID AND cp.UID = pq.UID
    )
    -- allows the function to work for both INSERT and DELETE operations
    WHERE pq.UID = NEW.UID OR pq.UID = OLD.UID;
    -- does not need to return a value if just modifying the table
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_player_quest_completion_trigger
AFTER INSERT OR DELETE ON CompletedProblems
FOR EACH ROW
EXECUTE FUNCTION update_player_quest_completion();

-- Insert default admin user
INSERT INTO Users (UID, Username, Email, HashPW)
VALUES ('00000000-0000-0000-0000-000000000000', 'DefaultAdmin', 'admin@example.com', 'default_hash_password');

INSERT INTO Admins (UID)
VALUES ('00000000-0000-0000-0000-000000000000');

-- Create database users and assign privileges
-- CREATE USER admin_user WITH PASSWORD 'admin_password';
GRANT SELECT ON UsersView TO admin_user;
GRANT INSERT ON Users TO admin_user;
GRANT SELECT ON Players TO admin_user;
GRANT ALL PRIVILEGES ON Admins TO admin_user;

CREATE USER scout_user WITH PASSWORD 'scout_password';
GRANT SELECT ON HardestPlayers TO scout_user;

-- Create roles
CREATE ROLE adminmanager;
GRANT SELECT ON UsersView TO adminmanager;
GRANT SELECT ON Users TO adminmanager;
GRANT SELECT ON Players TO adminmanager;
GRANT SELECT, INSERT, UPDATE, DELETE ON Admins TO adminmanager;

CREATE ROLE scout;
GRANT SELECT ON HardestPlayers TO scout;

-- Grant roles to users
GRANT adminmanager TO admin_user;
GRANT scout TO scout_user;