-- Создание таблицы Жанров
CREATE TABLE Genres (
    GenreID SERIAL PRIMARY KEY,
    Name VARCHAR(255) NOT NULL UNIQUE
);

-- Создание таблицы Исполнителей
CREATE TABLE Singers (
    SingerID SERIAL PRIMARY KEY,
    Name VARCHAR(255) NOT NULL
);

-- Создание таблицы для связи Исполнителей и Жанров (многие ко многим)
CREATE TABLE SingersGenres (
    SingerID INT NOT NULL,
    GenreID INT NOT NULL,
    PRIMARY KEY (SingerID, GenreID),
    FOREIGN KEY (SingerID) REFERENCES Singers(SingerID) ON DELETE CASCADE,
    FOREIGN KEY (GenreID) REFERENCES Genres(GenreID) ON DELETE CASCADE
);

-- Создание таблицы Альбомов
CREATE TABLE Albums (
    AlbumID SERIAL PRIMARY KEY,
    Title VARCHAR(255) NOT NULL,
    ReleaseYear INT CHECK (ReleaseYear >= 1900 AND ReleaseYear <= EXTRACT(YEAR FROM CURRENT_DATE))
);

-- Создание таблицы для связи Исполнителей и Альбомов (многие ко многим)
CREATE TABLE SingersAlbums (
    SingerID INT NOT NULL,
    AlbumID INT NOT NULL,
    PRIMARY KEY (SingerID, AlbumID),
    FOREIGN KEY (SingerID) REFERENCES Singers(SingerID) ON DELETE CASCADE,
    FOREIGN KEY (AlbumID) REFERENCES Albums(AlbumID) ON DELETE CASCADE
);

-- Создание таблицы Треков
CREATE TABLE Tracks (
    TrackID SERIAL PRIMARY KEY,
    Title VARCHAR(255) NOT NULL,
    Duration INTERVAL NOT NULL,
    AlbumID INT NOT NULL,
    FOREIGN KEY (AlbumID) REFERENCES Albums(AlbumID) ON DELETE CASCADE
);

-- Создание таблицы Сборников
CREATE TABLE Collections (
    CollectionID SERIAL PRIMARY KEY,
    Name VARCHAR(255) NOT NULL UNIQUE,
    ReleaseYear INT CHECK (ReleaseYear >= 1900 AND ReleaseYear <= EXTRACT(YEAR FROM CURRENT_DATE))
);

-- Создание таблицы для связи Сборников и Треков (многие ко многим)
CREATE TABLE CollectionsTracks (
    CollectionID INT NOT NULL,
    TrackID INT NOT NULL,
    PRIMARY KEY (CollectionID, TrackID),
    FOREIGN KEY (CollectionID) REFERENCES Collections(CollectionID) ON DELETE CASCADE,
    FOREIGN KEY (TrackID) REFERENCES Tracks(TrackID) ON DELETE CASCADE
);