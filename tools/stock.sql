-- phpMyAdmin SQL Dump
-- version 4.1.9
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: 2015-09-22 16:31:29
-- 服务器版本： 5.6.25
-- PHP Version: 5.5.14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `stock`
--

-- --------------------------------------------------------

--
-- 表的结构 `deal_detail`
--

CREATE TABLE IF NOT EXISTS `deal_detail` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(10) NOT NULL COMMENT '股票代码',
  `time` datetime NOT NULL COMMENT '时间',
  `price` float NOT NULL COMMENT '成交价格',
  `price_change` float NOT NULL COMMENT '价格变动',
  `volume` int(11) NOT NULL COMMENT '成交手',
  `amount` float NOT NULL COMMENT '成交金额（元）',
  `type` tinyint(4) NOT NULL COMMENT '买卖类型 0中性盘 1买盘 2卖盘',
  PRIMARY KEY (`id`),
  KEY `code` (`code`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 COMMENT='分笔交易表' AUTO_INCREMENT=12652 ;

-- --------------------------------------------------------

--
-- 表的结构 `deal_record`
--

CREATE TABLE IF NOT EXISTS `deal_record` (
  `did` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '交易id',
  `code` varchar(10) NOT NULL COMMENT '股票代码',
  `deal_time` datetime NOT NULL COMMENT '交易日期',
  `open` float NOT NULL COMMENT '开盘价',
  `close` float NOT NULL COMMENT '收盘价',
  `high` float NOT NULL COMMENT '最高价',
  `low` float NOT NULL COMMENT '最低价',
  `volume` float NOT NULL COMMENT '成交量',
  `amount` float NOT NULL COMMENT '成交金额',
  `price_change` float NOT NULL COMMENT '价格变动',
  `price_change_rate` float NOT NULL COMMENT '价格变化率',
  `turnover` float NOT NULL COMMENT '换手率（指数无此项）',
  `zhuli_in` float NOT NULL COMMENT '主力买入',
  `zhuli_out` float NOT NULL COMMENT '主力卖出',
  `sanhu_in` float NOT NULL COMMENT '散户买入',
  ` sanhu_out` float NOT NULL COMMENT '散户卖出',
  PRIMARY KEY (`did`),
  KEY `code` (`code`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT=' 天级历史行情表' AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- 表的结构 `stocks`
--

CREATE TABLE IF NOT EXISTS `stocks` (
  `code` varchar(10) NOT NULL COMMENT '股票代码,唯一主键',
  `type` int(11) NOT NULL COMMENT '类型',
  `name` varchar(20) NOT NULL COMMENT '股票名称',
  `time_to_market` datetime NOT NULL COMMENT '上市时间',
  `classify` varchar(500) NOT NULL COMMENT '概念',
  `can_deal` tinyint(4) NOT NULL COMMENT '是否可交易，1yes，0no',
  PRIMARY KEY (`code`),
  UNIQUE KEY `name` (`name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='股票列表';

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
