name_basic_duplicate_profession
name_basics_duplicate_name_different_id

DELETE FROM name_basic 
WHERE EXISTS (
    SELECT 1 
    FROM name_basic AS nb2
    WHERE 
        name_basic.primaryName = nb2.primaryName 
        AND (
            name_basic.primaryProfession = nb2.primaryProfession 
            OR (name_basic.primaryProfession IS NULL AND nb2.primaryProfession IS NULL)
        )
        AND name_basic.nconst > nb2.nconst
)
OR EXISTS (
    SELECT 1 
    FROM (
        SELECT primaryName, COUNT(*) as cnt
        FROM name_basic
        GROUP BY primaryName
        HAVING cnt > 1
    ) AS dup_names
    WHERE name_basic.primaryName = dup_names.primaryName
);


title_basics_duplicate_originaltitle_different_id

DELETE FROM title_basics 
WHERE EXISTS (
    SELECT 1 
    FROM title_basics AS tb2
    WHERE 
        title_basics.originalTitle = tb2.originalTitle
        AND title_basics.tconst <> tb2.tconst
        AND title_basics.titleType = tb2.titleType
);


title_crew_duplicate_directors
-- Löschen von Duplikaten im Feld directors basierend auf tconst  //NOCH NICHT AUSGEFUEHRT
DELETE FROM cleaned.title_crew
WHERE EXISTS (
    SELECT 1
    FROM (
        SELECT tconst, director, COUNT(*) as cnt
        FROM (
            SELECT tconst, director
            FROM tcleaned.title_crew
            CROSS JOIN unnest(string_to_array(directors, ',')) AS director
        ) AS director_list
        GROUP BY tconst, director
        HAVING COUNT(*) > 1
    ) AS dupes
    WHERE cleaned.title_crew.tconst = dupes.tconst
    AND ',' || cleaned.title_crew.directors || ',' LIKE '%,' || dupes.director || ',%'
);



-- Löschen von Datensätzen basierend auf doppeltem tconst und ordering
DELETE FROM cleaned.title_principals
WHERE (tconst, ordering) IN (
    SELECT tconst, ordering
    FROM cleaned.title_principals
    GROUP BY tconst, ordering
    HAVING COUNT(*) > 1
);


