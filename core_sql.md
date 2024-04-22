# raw --> core
## core.name_basics
```sql
INSERT INTO core.name_basics (nconst, lastName, firstName, birthYear, deathYear)
SELECT nconst,
       TRIM(SUBSTRING_INDEX(primaryName, ' ', -1)) AS lastName,
       TRIM(SUBSTR(primaryName, 1, LENGTH(primaryName) - LENGTH(SUBSTRING_INDEX(primaryName, ' ', -1)))) AS firstName,
       birthYear,
       deathYear
FROM raw.name_basics;
```
## core.title_basics
```sql
INSERT INTO core.title_basics (tconst, titleType, primaryTitle, originalTitle, isAdult, startYear, endYear, runtimeMinutes)
SELECT tconst,
       titleType,
       primaryTitle,
       originalTitle,
       isAdult,
       CASE
           WHEN startYear = '\\N' THEN NULL
           ELSE CAST(startYear AS UNSIGNED)
       END AS startYear,
       CASE
           WHEN endYear = '\\N' THEN NULL
           ELSE CAST(endYear AS UNSIGNED)
       END AS endYear,
       CASE
           WHEN runtimeMinutes = '\\N' THEN NULL
           ELSE CAST(runtimeMinutes AS UNSIGNED)
       END AS runtimeMinutes
FROM raw.title_basics;
```
## core.title_episode
```sql
INSERT INTO core.title_episodes (tconst, parentTconst, seasonNumber, episodeNumber)
SELECT tconst,
       parentTconst,
       CAST(seasonNumber AS UNSIGNED),
       CAST(episodeNumber AS UNSIGNED)
FROM extract.title_episode;
```
## core.title_principals
```sql
INSERT INTO core.title_principals (tconst, ordering, nconst, category, job, characters)
SELECT tconst,
       ordering,
       nconst,
       category,
       job,
       characters
FROM raw.title_principals;
```
## core.title_ratings
```sql
INSERT INTO core.title_ratings (tconst, averageRating, numVotes)
SELECT tconst,
       averageRating,
       numVotes
FROM raw.title_ratings;
```
## core.title_writer
```sql
INSERT INTO core.title_writers (tconst, writer)
SELECT tconst,
       writers
FROM raw.title_crew;
```
## core.title_directors
```sql
-- Lösung ALT
-- SQL to split directors and insert into core.title_directors
INSERT INTO core.title_directors (director, tconst)
SELECT
    TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(tc.directors, ',', numbers.n), ',', -1)) AS director,
    tc.tconst
FROM
    raw.title_crew tc
JOIN
    (SELECT 1 n UNION ALL SELECT 2
     UNION ALL SELECT 3 UNION ALL SELECT 4
     UNION ALL SELECT 5) AS numbers
ON
    CHAR_LENGTH(tc.directors) - CHAR_LENGTH(REPLACE(tc.directors, ',', '')) >= numbers.n - 1;
```
```sql
-- Lösung NEU
-- Create a temporary table to store split directors
CREATE TEMPORARY TABLE temp_directors AS
WITH RECURSIVE DirectorSplit AS (
    SELECT
        tconst,
        TRIM(SUBSTRING_INDEX(directors, ',', 1)) AS director,
        SUBSTRING(directors, LENGTH(SUBSTRING_INDEX(directors, ',', 1)) + 2) AS remaining_directors
    FROM extract.title_crew

    UNION ALL

    SELECT
        tconst,
        TRIM(SUBSTRING_INDEX(remaining_directors, ',', 1)) AS director,
        SUBSTRING(remaining_directors, LENGTH(SUBSTRING_INDEX(remaining_directors, ',', 1)) + 2) AS remaining_directors
    FROM DirectorSplit
    WHERE remaining_directors != ''
)

SELECT director, tconst
FROM DirectorSplit
WHERE director IS NOT NULL;

-- Insert into core.title_directors from temporary table
INSERT INTO core.title_directors (director, tconst)
SELECT director, tconst
FROM temp_directors;

-- Drop the temporary table
DROP TEMPORARY TABLE temp_directors;
```
## core.title_akas
```sql
INSERT INTO core.title_akas(titleID, ordering, title, region, language, type, attribute, isOrginalTitle)
SELECT
    titleID,
    ordering,
    title,
    region,
    language,
    types,
    attributes,
    isOriginalTitle
FROM
    raw.title_akas;
```
## core.title_genres
```sql
-- Create a temporary table to store split directors
CREATE TEMPORARY TABLE temp_genre AS
WITH RECURSIVE GenreSplit AS (
    SELECT
        tconst,
        TRIM(SUBSTRING_INDEX(genres, ',', 1)) AS genres,
        SUBSTRING(genres, LENGTH(SUBSTRING_INDEX(genres, ',', 1)) + 2) AS remaining_genres
    FROM raw.title_basics

    UNION ALL

    SELECT
        tconst,
        TRIM(SUBSTRING_INDEX(remaining_genres, ',', 1)) AS director,
        SUBSTRING(remaining_genres, LENGTH(SUBSTRING_INDEX(remaining_genres, ',', 1)) + 2) AS remaining_genres
    FROM GenreSplit
    WHERE remaining_genres != ''
)

SELECT genres, tconst
FROM GenreSplit
WHERE genres IS NOT NULL;

-- Insert into core.title_directors from temporary table
INSERT INTO core.title_genres (genre, tconst)
SELECT genres, tconst
FROM temp_genre;

-- Drop the temporary table
DROP TEMPORARY TABLE temp_genre;
```
## core.knownfortitles
```sql
-- Create a temporary table to store split directors
CREATE TEMPORARY TABLE temp_kft AS
WITH RECURSIVE KFTSplit AS (
    SELECT
        nconst,
        TRIM(SUBSTRING_INDEX(knownForTitles, ',', 1)) AS tconst,
        SUBSTRING(knownForTitles, LENGTH(SUBSTRING_INDEX(knownForTitles, ',', 1)) + 2) AS remaining_kft
    FROM raw.name_basics

    UNION ALL

    SELECT
        nconst,
        TRIM(SUBSTRING_INDEX(remaining_kft, ',', 1)) AS director,
        SUBSTRING(remaining_kft, LENGTH(SUBSTRING_INDEX(remaining_kft, ',', 1)) + 2) AS remaining_kft
    FROM KFTSplit
    WHERE remaining_kft != ''
)

SELECT tconst, nconst
FROM KFTSplit
WHERE tconst IS NOT NULL;

-- Insert into core.title_directors from temporary table
INSERT INTO core.knownfortitles (tconst, nconst)
SELECT tconst, nconst
FROM temp_kft;

-- Drop the temporary table
DROP TEMPORARY TABLE temp_kft;
```
## core.primaryProfession
```sql
-- Create a temporary table to store split directors
CREATE TEMPORARY TABLE temp_primaryProfession AS
WITH RECURSIVE pPSplit AS (
    SELECT
        nconst,
        TRIM(SUBSTRING_INDEX(primaryProfession, ',', 1)) AS profession,
        SUBSTRING(primaryProfession, LENGTH(SUBSTRING_INDEX(primaryProfession, ',', 1)) + 2) AS remaining_pP
    FROM raw.name_basics

    UNION ALL

    SELECT
        nconst,
        TRIM(SUBSTRING_INDEX(remaining_pP, ',', 1)) AS profession,
        SUBSTRING(remaining_pP, LENGTH(SUBSTRING_INDEX(remaining_pP, ',', 1)) + 2) AS remaining_pP
    FROM pPSplit
    WHERE remaining_pP != ''
)

SELECT nconst, profession
FROM pPSplit
WHERE profession IS NOT NULL;

-- Insert into core.title_directors from temporary table
INSERT INTO core.primaryprofession (nconst, profession)
SELECT nconst, profession
FROM temp_primaryProfession;

-- Drop the temporary table
DROP TEMPORARY TABLE temp_primaryProfession;
```