PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS "answers";
DROP TABLE IF EXISTS "login";
DROP TABLE IF EXISTS "questions";


CREATE TABLE "login"
(
"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
"user"	TEXT NOT NULL UNIQUE ,
"password"	TEXT NOT NULL,
"admin" BOOLEAN NOT NULL DEFAULT 0
);

CREATE TABLE "questions"
(
"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
"id_user"	INTEGER NOT NULL,
"question"	TEXT NOT NULL,
"type" TEXT NOT NULL
);

CREATE TABLE "answers"
(
"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
"id_user"	INTEGER NOT NULL,
"id_question"	INTEGER NOT NULL,
"question"	TEXT NOT NULL,
"answer" TEXT NOT NULL,
"is_answer" BOOLEAN DEFAULT 1
);
