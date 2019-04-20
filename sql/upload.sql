/*
Navicat SQLite Data Transfer

Source Server         : qwe
Source Server Version : 30808
Source Host           : :0

Target Server Type    : SQLite
Target Server Version : 30808
File Encoding         : 65001

Date: 2019-04-20 20:20:03
*/

PRAGMA foreign_keys = OFF;

-- ----------------------------
-- Table structure for upload
-- ----------------------------
DROP TABLE IF EXISTS "main"."upload";
CREATE TABLE "upload" (
"ID"  INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
"src_name"  TEXT,
"sys_name"  TEXT,
"file_type"  TEXT,
"upload_time"  TEXT,
"creator"  TEXT
);
