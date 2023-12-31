USE [master]
GO
	/****** Object:  Database [project_csharp]    Script Date: 2023/06/23 11:21:28 ******/
	CREATE DATABASE [project_csharp] CONTAINMENT = NONE ON PRIMARY (
		NAME = N'project_csharp',
		FILENAME = N'C:\Program Files\Microsoft SQL Server\MSSQL16.MSSQLSERVER\MSSQL\DATA\project_csharp.mdf',
		SIZE = 8192KB,
		MAXSIZE = UNLIMITED,
		FILEGROWTH = 65536KB
	) LOG ON (
		NAME = N'project_csharp_log',
		FILENAME = N'C:\Program Files\Microsoft SQL Server\MSSQL16.MSSQLSERVER\MSSQL\DATA\project_csharp_log.ldf',
		SIZE = 8192KB,
		MAXSIZE = 2048GB,
		FILEGROWTH = 65536KB
	) WITH CATALOG_COLLATION = DATABASE_DEFAULT,
	LEDGER = OFF
GO ALTER DATABASE [project_csharp]
SET COMPATIBILITY_LEVEL = 160
GO IF (
		1 = FULLTEXTSERVICEPROPERTY('IsFullTextInstalled')
	) begin EXEC [project_csharp].[dbo].[sp_fulltext_database] @action = 'enable'
end
GO ALTER DATABASE [project_csharp]
SET ANSI_NULL_DEFAULT OFF
GO ALTER DATABASE [project_csharp]
SET ANSI_NULLS OFF
GO ALTER DATABASE [project_csharp]
SET ANSI_PADDING OFF
GO ALTER DATABASE [project_csharp]
SET ANSI_WARNINGS OFF
GO ALTER DATABASE [project_csharp]
SET ARITHABORT OFF
GO ALTER DATABASE [project_csharp]
SET AUTO_CLOSE OFF
GO ALTER DATABASE [project_csharp]
SET AUTO_SHRINK OFF
GO ALTER DATABASE [project_csharp]
SET AUTO_UPDATE_STATISTICS ON
GO ALTER DATABASE [project_csharp]
SET CURSOR_CLOSE_ON_COMMIT OFF
GO ALTER DATABASE [project_csharp]
SET CURSOR_DEFAULT GLOBAL
GO ALTER DATABASE [project_csharp]
SET CONCAT_NULL_YIELDS_NULL OFF
GO ALTER DATABASE [project_csharp]
SET NUMERIC_ROUNDABORT OFF
GO ALTER DATABASE [project_csharp]
SET QUOTED_IDENTIFIER OFF
GO ALTER DATABASE [project_csharp]
SET RECURSIVE_TRIGGERS OFF
GO ALTER DATABASE [project_csharp]
SET ENABLE_BROKER
GO ALTER DATABASE [project_csharp]
SET AUTO_UPDATE_STATISTICS_ASYNC OFF
GO ALTER DATABASE [project_csharp]
SET DATE_CORRELATION_OPTIMIZATION OFF
GO ALTER DATABASE [project_csharp]
SET TRUSTWORTHY OFF
GO ALTER DATABASE [project_csharp]
SET ALLOW_SNAPSHOT_ISOLATION OFF
GO ALTER DATABASE [project_csharp]
SET PARAMETERIZATION SIMPLE
GO ALTER DATABASE [project_csharp]
SET READ_COMMITTED_SNAPSHOT OFF
GO ALTER DATABASE [project_csharp]
SET HONOR_BROKER_PRIORITY OFF
GO ALTER DATABASE [project_csharp]
SET RECOVERY FULL
GO ALTER DATABASE [project_csharp]
SET MULTI_USER
GO ALTER DATABASE [project_csharp]
SET PAGE_VERIFY CHECKSUM
GO ALTER DATABASE [project_csharp]
SET DB_CHAINING OFF
GO ALTER DATABASE [project_csharp]
SET FILESTREAM(NON_TRANSACTED_ACCESS = OFF)
GO ALTER DATABASE [project_csharp]
SET TARGET_RECOVERY_TIME = 60 SECONDS
GO ALTER DATABASE [project_csharp]
SET DELAYED_DURABILITY = DISABLED
GO ALTER DATABASE [project_csharp]
SET ACCELERATED_DATABASE_RECOVERY = OFF
GO EXEC sys.sp_db_vardecimal_storage_format N'project_csharp',
	N 'ON'
GO ALTER DATABASE [project_csharp]
SET QUERY_STORE = ON
GO ALTER DATABASE [project_csharp]
SET QUERY_STORE (
		OPERATION_MODE = READ_WRITE,
		CLEANUP_POLICY = (STALE_QUERY_THRESHOLD_DAYS = 30),
		DATA_FLUSH_INTERVAL_SECONDS = 900,
		INTERVAL_LENGTH_MINUTES = 60,
		MAX_STORAGE_SIZE_MB = 1000,
		QUERY_CAPTURE_MODE = AUTO,
		SIZE_BASED_CLEANUP_MODE = AUTO,
		MAX_PLANS_PER_QUERY = 200,
		WAIT_STATS_CAPTURE_MODE = ON
	)
GO USE [project_csharp]
GO
	/****** Object:  User [odbc_user]    Script Date: 2023/06/23 11:21:28 ******/
	CREATE USER [odbc_user] FOR LOGIN [odbc_user] WITH DEFAULT_SCHEMA = [dbo]
GO ALTER ROLE [db_owner]
ADD MEMBER [odbc_user]
GO
	/****** Object:  Table [dbo].[Address]    Script Date: 2023/06/23 11:21:28 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO CREATE TABLE [dbo].[Address](
		[street] [nvarchar](150) NOT NULL,
		[suite] [nvarchar](50) NULL,
		[city] [nvarchar](70) NOT NULL,
		[zipcode] [varchar](20) NOT NULL,
		[address_id] [int] IDENTITY(1, 1) NOT NULL,
		[geo_id] [int] NOT NULL,
		PRIMARY KEY CLUSTERED ([address_id] ASC) WITH (
			PAD_INDEX = OFF,
			STATISTICS_NORECOMPUTE = OFF,
			IGNORE_DUP_KEY = OFF,
			ALLOW_ROW_LOCKS = ON,
			ALLOW_PAGE_LOCKS = ON,
			OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF
		) ON [PRIMARY]
	) ON [PRIMARY]
GO
	/****** Object:  Table [dbo].[Company]    Script Date: 2023/06/23 11:21:28 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO CREATE TABLE [dbo].[Company](
		[name] [nvarchar](50) NOT NULL,
		[catchphrase] [nvarchar](80) NULL,
		[bs] [nvarchar](100) NULL,
		[company_id] [int] IDENTITY(1, 1) NOT NULL,
		PRIMARY KEY CLUSTERED ([company_id] ASC) WITH (
			PAD_INDEX = OFF,
			STATISTICS_NORECOMPUTE = OFF,
			IGNORE_DUP_KEY = OFF,
			ALLOW_ROW_LOCKS = ON,
			ALLOW_PAGE_LOCKS = ON,
			OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF
		) ON [PRIMARY]
	) ON [PRIMARY]
GO
	/****** Object:  Table [dbo].[Geo]    Script Date: 2023/06/23 11:21:28 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO CREATE TABLE [dbo].[Geo](
		[lat] [nvarchar](50) NOT NULL,
		[lng] [nvarchar](50) NOT NULL,
		[geo_id] [int] IDENTITY(1, 1) NOT NULL,
		PRIMARY KEY CLUSTERED ([geo_id] ASC) WITH (
			PAD_INDEX = OFF,
			STATISTICS_NORECOMPUTE = OFF,
			IGNORE_DUP_KEY = OFF,
			ALLOW_ROW_LOCKS = ON,
			ALLOW_PAGE_LOCKS = ON,
			OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF
		) ON [PRIMARY]
	) ON [PRIMARY]
GO
	/****** Object:  Table [dbo].[User]    Script Date: 2023/06/23 11:21:28 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO CREATE TABLE [dbo].[User](
		[name] [nvarchar](120) NOT NULL,
		[username] [nvarchar](50) NOT NULL,
		[email] [nvarchar](50) NOT NULL,
		[phone] [nvarchar](20) NULL,
		[website] [nvarchar](50) NULL,
		[user_id] [int] IDENTITY(1, 1) NOT NULL,
		[company_id] [int] NOT NULL,
		[address_id] [int] NOT NULL,
		PRIMARY KEY CLUSTERED ([user_id] ASC) WITH (
			PAD_INDEX = OFF,
			STATISTICS_NORECOMPUTE = OFF,
			IGNORE_DUP_KEY = OFF,
			ALLOW_ROW_LOCKS = ON,
			ALLOW_PAGE_LOCKS = ON,
			OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF
		) ON [PRIMARY]
	) ON [PRIMARY]
GO
ALTER TABLE [dbo].[Address] WITH CHECK
ADD CONSTRAINT [FK_Address_ToGeo] FOREIGN KEY([geo_id]) REFERENCES [dbo].[Geo] ([geo_id])
GO
ALTER TABLE [dbo].[Address] CHECK CONSTRAINT [FK_Address_ToGeo]
GO
ALTER TABLE [dbo].[User] WITH CHECK
ADD CONSTRAINT [FK_User_ToAddress] FOREIGN KEY([address_id]) REFERENCES [dbo].[Address] ([address_id])
GO
ALTER TABLE [dbo].[User] CHECK CONSTRAINT [FK_User_ToAddress]
GO
ALTER TABLE [dbo].[User] WITH CHECK
ADD CONSTRAINT [FK_User_ToCompany] FOREIGN KEY([company_id]) REFERENCES [dbo].[Company] ([company_id])
GO
ALTER TABLE [dbo].[User] CHECK CONSTRAINT [FK_User_ToCompany]
GO USE [master]
GO ALTER DATABASE [project_csharp]
SET READ_WRITE
GO