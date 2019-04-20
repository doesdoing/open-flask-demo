/*
Navicat SQLite Data Transfer

Source Server         : asdas
Source Server Version : 30808
Source Host           : :0

Target Server Type    : SQLite
Target Server Version : 30808
File Encoding         : 65001

Date: 2019-04-20 20:21:32
*/

PRAGMA foreign_keys = OFF;

-- ----------------------------
-- Table structure for system
-- ----------------------------
DROP TABLE IF EXISTS "main"."system";
CREATE TABLE "system" (
"ID"  INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
"projects"  TEXT,
"ip"  TEXT,
"login_name"  TEXT,
"login_password"  TEXT,
"remark"  TEXT
);
