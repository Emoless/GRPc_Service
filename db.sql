CREATE TABLE Clubs (
    ClubID VARCHAR(20) PRIMARY KEY,
    ClubName VARCHAR(50) NOT NULL,
    FoundedYear SMALLINT,
    City VARCHAR(20),
    Country VARCHAR(20)
);

CREATE TABLE Roster (
    playerid VARCHAR(20),
    jersey SMALLINT,
    fname VARCHAR(20),
    sname VARCHAR(20),
    position VARCHAR(10),
    birthday TIMESTAMP,
    weight SMALLINT,
    height SMALLINT,
    birthcity VARCHAR(20),
    birthstate VARCHAR(20),
    ClubID VARCHAR(20),
    FOREIGN KEY (ClubID) REFERENCES Clubs(ClubID)
);

-- Вставка данных в таблицу roster
INSERT INTO Roster (playerid, jersey, fname, sname, position, birthday, weight, height, birthcity, birthstate, ClubID) VALUES
('adamlem', 12, 'Mike', 'Adamle', 'RW', '2001-09-21 00:00:00', 73, 197, 'Stamford', 'CT', 1),
('adamles', 17, 'Scott', 'Adamle', 'D', '1999-03-01 00:00:00', 70, 184, 'Columbus', 'OH', 1),
('armanova', 31, 'Arkady', 'Armanov', 'LW', '1998-10-25 00:00:00', 71, 197, 'Minsk', 'RU', 2),
('boolea', 8, 'Alexi', 'Boole', 'RW', '1997-09-14 00:00:00', 72, 194, 'Kiev', 'UK', 3),
('choakd', 11, 'Dominick', 'Choak', 'RW', '1997-02-22 00:00:00', 72, 196, 'Prague', 'CZ', 2),
('clobberk', 24, 'Kilroy', 'Clobber', 'D', '2002-06-21 00:00:00', 73, 200, 'Bangor', 'ME', 3),
('clubbes', 7, 'Sam', 'Clubbe', 'LW', '1999-07-26 00:00:00', 75, 190, 'Paramus', 'NJ', 2),
('finleyp', 14, 'Peter', 'Finley', 'D', '1987-06-08 00:00:00', 76, 194, 'Denver', 'CO', 2),
('fiskj', 25, 'Jerke', 'Fisk', 'D', '2001-11-25 00:00:00', 71, 193, 'Helsinki', 'FI', 1),
('gruberh', 29, 'Hans', 'Gruber', 'D', '1991-02-11 00:00:00', 70, 175, 'Munich', 'DE', 1),
('grunwala', 6, 'Allan', 'Grunwald', 'C', '1990-10-17 00:00:00', 74, 189, 'Buffalo', 'NY', 3),
('ivanovv', 4, 'Valerei', 'Ivanovich', 'C', '2004-09-20 00:00:00', 72, 175, 'Moscow', 'RU', 3),
('jeffriea', 30, 'Angus', 'Jeffries', 'G', '1995-11-08 00:00:00', 70, 185, 'Springfield', 'MA', 3),
('jonesr', 35, 'Robert', 'Jones', 'C', '1997-05-22 00:00:00', 73, 189, 'Hartford', 'CT', 2),
('lexourb', 9, 'Bruce', 'Lexour', 'D', '2001-09-05 00:00:00', 75, 198, 'Quincy', 'IL', 1),
('lunds', 93, 'Steven', 'Lund', 'D', '1997-05-22 00:00:00', 71, 193, 'St. Paul', 'MN', 3),
('maguirea', 34, 'Andre', 'Maguire', 'LW', '1999-12-08 00:00:00', 75, 191, 'Detroit', 'MI', 3),
('meyersd', 28, 'Doug', 'Meyers', 'G', '1998-02-11 00:00:00', 70, 195, 'Chicago', 'IL', 1),
('olsens', 37, 'Sandish', 'Olsen', 'D', '1999-08-16 00:00:00', 72, 192, 'Stockholm', 'SW', 1),
('quivep', 20, 'Pierre', 'Quive', 'LW', '1991-07-19 00:00:00', 71, 197, 'Quebec', 'QU', 2),
('springej', 38, 'Junior', 'Springer', 'C', '1995-10-14 00:00:00', 71, 184, 'Toronto', 'ON', 2),
('sullivar', 39, 'Russel', 'Sullivan', 'G', '2000-03-08 00:00:00', 70, 186, 'Vancouver', 'BC', 2),
('travisj', 19, 'John', 'Travis', 'C', '2003-06-23 00:00:00', 74, 200, 'Boston', 'MA', 2),
('zauberz', 22, 'Zeke', 'Zauber', 'RW', '1988-08-31 00:00:00', 74, 203, 'Moosehead', 'MA', 1);

-- Пример добавления данных в таблицу Clubs
INSERT INTO Clubs (ClubID, ClubName, FoundedYear, City, Country) VALUES
('1', 'Ice Warriors', 1990, 'New York', 'USA'),
('2', 'Polar Bears', 1985, 'Toronto', 'Canada'),
('3', 'Arctic Storm', 2000, 'Stockholm', 'Sweden');