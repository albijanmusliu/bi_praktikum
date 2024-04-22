# Entfernen der Duplikate
## Lösung name_basic_duplicate_profession
```sql
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
);
```

## Lösung name_basics_duplicate_name_different_id:
```sql
DELETE FROM name_basic
WHERE EXISTS (
    SELECT 1 
    FROM (
        SELECT primaryName, MIN(nconst) as min_nconst
        FROM name_basic
        GROUP BY primaryName
        HAVING COUNT(*) > 1
    ) AS dup_names
    WHERE name_basic.primaryName = dup_names.primaryName
    AND name_basic.nconst > dup_names.min_nconst
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


TODO: HIER DIE INSERTS IN unified 
