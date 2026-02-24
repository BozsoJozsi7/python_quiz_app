

INSERT INTO kerdes (tipus, szoveg, helyes_szam) VALUES
('szam', 'Hány foga van egy felnőtt embernek?', 32),
('szam', 'Hány deciliter egy liter?', 10),
('szam', 'Mikor volt a Mohácsi vész?', 1526),
('szam', 'Hány hét van egy évben?', 52),
('szam', 'Hány évente rendeznek nyári olimpiai játékokat?', 4),
('szam', 'Mennyi a 9 négyzete?', 81),
('szam', 'Mennyi a 3/4 értéke két tizedesjegyre kerekítve?', 0.75);

INSERT INTO kerdes (tipus, szoveg, helyes_datum) VALUES
('datum', 'Mikor volt az első ember Holdra szállása? (éééé-hh-nn)', '1969-07-20');

INSERT INTO kerdes (tipus, szoveg) VALUES
('lista', 'Sorold fel az 5 legnagyobb bolygót a Naprendszerben!');

SELECT id INTO @lista_kerdes_id
FROM kerdes
WHERE tipus = 'lista' AND szoveg = 'Sorold fel az 5 legnagyobb bolygót a Naprendszerben!'
ORDER BY id DESC
LIMIT 1;

INSERT INTO lista_helyes (kerdes_id, elem) VALUES
(@lista_kerdes_id, 'Jupiter'),
(@lista_kerdes_id, 'Szaturnusz'),
(@lista_kerdes_id, 'Uránusz'),
(@lista_kerdes_id, 'Neptunusz'),
(@lista_kerdes_id, 'Föld');


INSERT INTO kerdes (tipus, szoveg) VALUES
('feleletvalasztos', 'Mi a legnagyobb emlős a Földön?');

SELECT id INTO @mcq1
FROM kerdes
WHERE tipus='feleletvalasztos' AND szoveg='Mi a legnagyobb emlős a Földön?'
ORDER BY id DESC LIMIT 1;

INSERT INTO valaszlehetoseg (kerdes_id, szoveg, helyes) VALUES
(@mcq1, 'jegesmedve', 0),
(@mcq1, 'afrikai elefánt', 0),
(@mcq1, 'kodiak-medve', 0),
(@mcq1, 'kék bálna', 1);

INSERT INTO kerdes (tipus, szoveg) VALUES
('feleletvalasztos', 'Ki alakította Tony Starkot a Marvel filmekben?');

SELECT id INTO @mcq2
FROM kerdes
WHERE tipus='feleletvalasztos' AND szoveg='Ki alakította Tony Starkot a Marvel filmekben?'
ORDER BY id DESC LIMIT 1;

INSERT INTO valaszlehetoseg (kerdes_id, szoveg, helyes) VALUES
(@mcq2, 'Chris Hemsworth', 0),
(@mcq2, 'Chris Evans', 0),
(@mcq2, 'Robert Downey Jr.', 1),
(@mcq2, 'Mark Ruffalo', 0);

INSERT INTO kerdes (tipus, szoveg) VALUES
('feleletvalasztos', 'Ki a Ragyogás rendezője?');

SELECT id INTO @mcq3
FROM kerdes
WHERE tipus='feleletvalasztos' AND szoveg='Ki a Ragyogás rendezője?'
ORDER BY id DESC LIMIT 1;

INSERT INTO valaszlehetoseg (kerdes_id, szoveg, helyes) VALUES
(@mcq3, 'Stanley Kubrick', 1),
(@mcq3, 'Ridley Scott', 0),
(@mcq3, 'David Fincher', 0),
(@mcq3, 'Quentin Tarantino', 0);
