CREATE DATABASE dbTestCenter

CREATE TABLE [dbo].[tb_TestPlanStat] (
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[PlanRuntimeGUID] [char](36) NOT NULL,
	[RuntimeName] [varchar](64) NOT NULL,
	[Filename] [varchar](64) NOT NULL,
	[TaskAmount] [smallint] DEFAULT 0,
	[TriggerTime] [datetime] DEFAULT getdate(),
	[LastUpdTime] [datetime] NULL,
	[Status] [smallint] DEFAULT -1

PRIMARY KEY CLUSTERED
(
	[ID] ASC
)
)

CREATE TABLE [dbo].[tb_TaskStat] (
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[PlanRuntimeGUID] [char](36) NOT NULL,
	[TaskGUID] [char](32) NOT NULL,
	[TaskName] [varchar](128) NULL,
	[StartTime] [datetime] NULL,
	[LastUpdTime] [datetime] NULL,
	[Status] [varchar](16) NULL,
	[SumCaseAmount] [int] NULL,
	[PassAmt] [int] DEFAULT 0,
	[FailAmt] [int] DEFAULT 0
PRIMARY KEY CLUSTERED
(
	[ID] ASC
)
)



CREATE TABLE [dbo].[tb_CaseStat] (
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[TaskGUID] [char](32) NOT NULL,
	[CaseRuntimeGUID] [char](36) NOT NULL,
	[CaseID] [varchar](64) NOT NULL,
	[StartTime] [datetime] NULL,
	[ExecDuration] [decimal](8,3) NULL,
	[Status] [smallint] NULL,
	[ExecMsg] [nvarchar](2048)
PRIMARY KEY CLUSTERED
(
	[ID] ASC
)
)


CREATE TABLE [dbo].[tb_ScheduleTask] (
	[ID] INT IDENTITY(1,1) NOT NULL,
	[Name] VARCHAR(64) NOT NULL,
	[ProcName] VARCHAR(64) NOT NULL,
	[Type] SMALLINT NOT NULL, --1: Schedule, 2: Interval
	[Interval] SMALLINT NULL,
	[Hr] TINYINT NULL,
	[Mi] TINYINT NULL,
	[LastExecTime] DATETIME NULL,
	[Desc] NVARCHAR(256)
PRIMARY KEY CLUSTERED
(
	[ID] ASC
)
)



