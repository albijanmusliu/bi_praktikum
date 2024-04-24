# Entfernen der Duplikate im Schema cleaned
## Lösung name_basics_duplicate_profession
```sql
DELETE FROM name_basics 
WHERE EXISTS (
    SELECT 1 
    FROM name_basics AS nb2
    WHERE 
        name_basics.primaryName = nb2.primaryName 
        AND (
            name_basics.primaryProfession = nb2.primaryProfession 
            OR (name_basics.primaryProfession IS NULL AND nb2.primaryProfession IS NULL)
        )
        AND name_basics.nconst > nb2.nconst
);
```

## Lösung name_basics_duplicate_name_different_id:
```sql
DELETE FROM name_basics
WHERE EXISTS (
    SELECT 1 
    FROM (
        SELECT primaryName, MIN(nconst) as min_nconst
        FROM name_basics
        GROUP BY primaryName
        HAVING COUNT(*) > 1
    ) AS dup_names
    WHERE name_basics.primaryName = dup_names.primaryName
    AND name_basics.nconst > dup_names.min_nconst
);
```

## Lösung title_basics_duplicate_originaltitle_different_id
```sql
DELETE FROM title_basics 
WHERE EXISTS (
    SELECT 1 
    FROM title_basics AS tb2
    WHERE 
        title_basics.originalTitle = tb2.originalTitle
        AND title_basics.tconst <> tb2.tconst
        AND title_basics.titleType = tb2.titleType
);
```

## Lösung title_crew_duplicate_directors
```sql
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
```
## Lösung title_principals_duplicate_row
```sql
DELETE FROM cleaned.title_principals
WHERE (tconst, ordering) IN (
    SELECT tconst, ordering
    FROM cleaned.title_principals
    GROUP BY tconst, ordering
    HAVING COUNT(*) > 1
);
```

# INSERT INTO unified FROM cleaned
```sql
INSERT INTO unified.name_basics(nconst, primaryName, birthYear, deathYear, primaryProfession, knownForTitles)
SELECT nconst, primaryName, birthYear, deathYear, primaryProfession, knownForTitles
FROM cleaned.name_basics
```
```sql
INSERT INTO unified.title_basics(tconst, titleType, primaryTitle, originalTitle, isAdult, startYear, endYear, runtimeMinutes, genres) 
SELECT tconst, titleType, primaryTitle, originalTitle, isAdult, startYear, endYear, runtimeMinutes, genres
FROM cleaned.title_basics
```
```sql
INSERT INTO unified.title_akas (titleId, ordering, title, region, language, types, attributes, isOriginalTitle) 
SELECT titleId, ordering, title, region, language, types, attributes, isOriginalTitle
FROM cleaned.title_akas
```
```sql
INSERT INTO unified.title_crew(tconst, directors, writers) 
SELECT tconst, directors, writers
FROM cleaned.title_crew
```
```sql
INSERT INTO unified.title_episode(tconst, parentTconst, seasonNumber, episodeNumber)
SELECT tconst, parentTconst, seasonNumber, episodeNumber
FROM cleaned.title_episode
```
```sql
INSERT INTO unified.title_principals(tconst, ordering, nconst, category, job, characters)
SELECT tconst, ordering, nconst, category, job, characters
FROM cleaned.title_principals
```
```sql
INSERT INTO unified.title_ratings(tconst, averageRating, numVotes)
SELECT tconst, averageRating, numVotes
FROM cleaned.title_ratings
```

