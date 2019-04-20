/*
Navicat SQLite Data Transfer

Source Server         : asdas
Source Server Version : 30808
Source Host           : :0

Target Server Type    : SQLite
Target Server Version : 30808
File Encoding         : 65001

Date: 2019-04-20 20:22:31
*/

PRAGMA foreign_keys = OFF;

-- ----------------------------
-- Table structure for server
-- ----------------------------
DROP TABLE IF EXISTS "main"."server";
CREATE TABLE "server" (
"ID"  INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
"location"  TEXT,
"projects"  TEXT,
"ip"  TEXT,
"login_name"  TEXT,
"login_password"  TEXT,
"remark"  TEXT,
"software"  TEXT,
"os"  TEXT,
"model"  TEXT
);
