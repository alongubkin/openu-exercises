DROP TRIGGER IF EXISTS T1 on map;
DROP FUNCTION IF EXISTS trigf1;

CREATE FUNCTION trigf1() RETURNS trigger as $$
	BEGIN
		IF (SELECT COUNT(*) FROM keyword WHERE keyword.kword = NEW.kword) = 0 THEN
			RAISE EXCEPTION 'Your kword does not exist in the keyword table.';
		END IF;
		
		RETURN NEW;
	END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER T1 
	BEFORE INSERT ON map 
	FOR EACH ROW EXECUTE PROCEDURE trigf1();