/*
Navicat SQLite Data Transfer

Source Server         : 111
Source Server Version : 30808
Source Host           : :0

Target Server Type    : SQLite
Target Server Version : 30808
File Encoding         : 65001

Date: 2019-04-20 20:22:58
*/

PRAGMA foreign_keys = OFF;

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS "main"."user";
CREATE TABLE "user" (
"ID"  INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
"username"  TEXT(10) NOT NULL,
"password"  TEXT(16) NOT NULL,
"name"  TEXT(10) NOT NULL,
"level"  TEXT(5) NOT NULL,
"ip"  TEXT(15),
"cookies"  TEXT(150),
"personal_img"  TEXT
);
