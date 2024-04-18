# SQL Fehlerbehebung und Bereinigung

## name_basic_inconsistent_birth_gt_death

### Fehlerbeschreibung
Einträge, bei denen das Geburtsjahr größer als das Sterbejahr ist werden entfernt.

## name_basic_incorrect_death_gt_current_year

### Fehlerbeschreibung
Einträge, bei denen das Sterbejahr in der Zukunft liegt werden entfernt.

## name_basic_incorrect_birth_lt_zero

### Fehlerbeschreibung
Einträge, bei denen das Geburtsjahr kleiner als Null ist werden entfernt.

# Lösung
```sql
INSERT INTO cleaned.name_basics (nconst, primaryName, birthYear, deathYear, primaryProfession, knownForTitles)
SELECT nconst, primaryName, birthYear, deathYear, primaryProfession, knownForTitles
FROM extract.name_basics
WHERE (birthYear <= deathYear OR deathYear IS NULL)
   AND (deathYear <= YEAR(CURRENT_DATE()))
   AND (birthYear >= 0 OR birthYear IS NULL)
   AND (primaryName LIKE '% %');

--Lösung_neu:
INSERT INTO cleaned.name_basics (nconst, primaryName, birthYear, deathYear, primaryProfession, knownForTitles)
SELECT nconst, primaryName, birthYear, deathYear, primaryProfession, knownForTitles
FROM extract.name_basics
WHERE ((birthYear <= deathYear OR birthYear IS NULL OR deathYear IS NULL)
   AND (deathYear <= YEAR(CURRENT_DATE()) OR deathYear IS NULL)
   AND (birthYear >= 0 OR birthYear IS NULL)
   AND (primaryName LIKE '% %'));

```

## title_akas_inconsistent_region

### Fehlerbeschreibung
Einträge mit einer ungültigen Region (mehr oder weniger als zwei Zeichen) werden entfernt.

## title_akas_inconsistent_language

### Fehlerbeschreibung
Einträge mit einer ungültigen Sprache (mehr oder weniger als zwei Zeichen) werden entfernt.

### Lösung
```sql
INSERT INTO cleaned.title_akas (titleId, ordering, title, region, language, types, attributes, isOriginalTitle)
SELECT titleId, ordering, title, region, language, types, attributes, isOriginalTitle
FROM extract.title_akas
WHERE
    (region IS NULL OR LENGTH(region) = 2)
    AND (language IS NULL OR LENGTH(language) = 2);
```

## title_basics_incorrect_runtime

### Fehlerbeschreibung
Einträge mit einer negativen Laufzeit werden entfernt.

## title_basics_incorrect_adult

### Fehlerbeschreibung
Einträge mit einem ungültigen Wert für isAdult werden entfernt.

## title_basics_incorrect_start

### Fehlerbeschreibung
Einträge mit einem Startjahr größer als das aktuelle Jahr werden entfernt.

### Lösung
```sql
INSERT INTO cleaned.title_basics (tconst, titleType, primaryTitle, originalTitle, isAdult, startYear, endYear, runtimeMinutes, genres)
SELECT tconst, titleType, primaryTitle, originalTitle, isAdult, startYear, endYear, runtimeMinutes, genres
FROM extract.title_basics
WHERE 
    (runtimeMinutes >= 0 OR runtimeMinutes IS NULL)
    AND (isAdult = 0 OR isAdult = 1)
    AND ((startYear >= 0 OR startYear IS NULL) AND (startYear < 2024));
```

## title_ratings_rating_incorrect_gt_ten

### Fehlerbeschreibung
Einträge mit einer Bewertung größer als 10 werden entfernt.

## title_ratings_rating_incorrect_lt_zero

### Fehlerbeschreibung
Einträge mit einer negativen Bewertung werden entfernt.

## title_ratings_rating_inconsistent_percentage

### Fehlerbeschreibung
Einträge mit einer Bewertung, die nicht zwischen 0 und 10 liegt werden entfernt.

## title_ratings_votes_incorrect_lt_zero

### Fehlerbeschreibung
Einträge mit einer negativen Anzahl von Stimmen werden entfernt.

## title_ratings_votes_incorrect_eq_zero

### Fehlerbeschreibung
Einträge mit einer Anzahl von Stimmen gleich Null werden entfernt.

### Lösung
```sql
INSERT INTO cleaned.title_ratings (tconst, averageRating, numVotes)
SELECT tconst, averageRating, numVotes
FROM extract.title_ratings
WHERE
    (averageRating < 10 OR averageRating > 0 OR averageRating IS NULL)
    AND (numVotes > 0 OR numVotes IS NULL);
```
# Unveränderte Tabellen
* title_crew
```sql
INSERT INTO cleaned.title_crew (tconst, directors, writers)
SELECT tconst, directors, writers
FROM extract.title_crew
```
* title_episode
```sql
INSERT INTO cleaned.title_episode (tconst, parentTconst, seasonNumber, episodeNumber)
SELECT tconst, parentTconst, seasonNumber, episodeNumber
FROM extract.title_episode
```
* title_principals
```sql
INSERT INTO cleaned.title_principals (tconst, ordering, nconst,category, job, characters)
SELECT tconst, ordering, nconst,category, job, characters
FROM extract.title_principals
```
  

