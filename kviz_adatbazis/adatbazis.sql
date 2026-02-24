DROP DATABASE IF EXISTS kviz;
CREATE DATABASE kviz DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_hungarian_ci;
USE kviz;

CREATE TABLE kerdes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tipus VARCHAR(20) NOT NULL,
    szoveg TEXT NOT NULL,
    aktiv INT NOT NULL DEFAULT 1,
    helyes_szam DOUBLE NULL,
    helyes_datum DATE NULL
);

CREATE TABLE valaszlehetoseg (
    id INT AUTO_INCREMENT PRIMARY KEY,
    kerdes_id INT NOT NULL,
    szoveg VARCHAR(255) NOT NULL,
    helyes INT NOT NULL DEFAULT 0,
    FOREIGN KEY (kerdes_id) REFERENCES kerdes(id)
        ON DELETE CASCADE
);

CREATE TABLE lista_helyes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    kerdes_id INT NOT NULL,
    elem VARCHAR(100) NOT NULL,
    FOREIGN KEY (kerdes_id) REFERENCES kerdes(id)
        ON DELETE CASCADE
);

CREATE TABLE futas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    jatekos_nev VARCHAR(80) NOT NULL,
    datum DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE naplo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    futas_id INT NOT NULL,
    kerdes_id INT NOT NULL,

    valasztott_valasz_id INT NULL,
    adott_szoveg TEXT NULL,
    adott_szam DOUBLE NULL,
    adott_datum DATE NULL,

    helyes INT NOT NULL,
    pont DOUBLE NOT NULL,
    elteres_szam DOUBLE NULL,
    elteres_nap INT NULL,

    FOREIGN KEY (futas_id) REFERENCES futas(id)
        ON DELETE CASCADE,

    FOREIGN KEY (kerdes_id) REFERENCES kerdes(id)
        ON DELETE CASCADE,

    FOREIGN KEY (valasztott_valasz_id) REFERENCES valaszlehetoseg(id)
        ON DELETE SET NULL
);