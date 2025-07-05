ALTER PROCEDURE [dbo].[sp_ExecScheduleTask]
AS
SET NOCOUNT ON
BEGIN TRANSACTION 

	DECLARE @Currtime DATETIME
	DECLARE @CurrHr TINYINT
	DECLARE @CurrMin TINYINT
	DECLARE @ProcedureName VARCHAR(64)
	
	


	CREATE TABLE #tmpScheduleTimeTask (
	ID INT,
	ProcName VARCHAR(64),
	Hr TINYINT NULL,
	Mi TINYINT NULL,
	LastExecTime DATETIME NULL
	)
	CREATE INDEX [Idx_Src_ID] ON #tmpScheduleTimeTask (ID)



	CREATE TABLE #tmpIntervalTask (
	ID INT,
	ProcName VARCHAR(64),
	Interval SMALLINT,
	LastExecTime DATETIME NULL,
	)
	CREATE INDEX [Idx_Src_ID] ON #tmpIntervalTask (ID)


	CREATE TABLE #tmpExecTask (
	ID INT,
	ProcName VARCHAR(64),
	ExecTime DATETIME NULL
	)
	CREATE INDEX [Idx_task_ID] ON #tmpExecTask (ID)


	SET @Currtime = GETDATE()
	SET @CurrHr = DATEPART( HOUR ,@Currtime)
	SET @CurrMin = DATEPART( MINUTE ,@Currtime)



	INSERT INTO #tmpScheduleTimeTask
	SELECT
		ID,
		ProcName,
		Hr,
		Mi,
		LastExecTime
	FROM tb_ScheduleTask WITH (NOLOCK)
	WHERE Type = 1

	INSERT INTO #tmpIntervalTask
	SELECT 
		ID,
		ProcName,
		Interval,
		LastExecTime
	FROM tb_ScheduleTask WITH (NOLOCK)
	WHERE Type = 2


	INSERT INTO #tmpExecTask
	SELECT
		ID,
		ProcName,
		NULL
	FROM #tmpScheduleTimeTask
	WHERE 
		Hr = @CurrHr AND
		Mi <= @CurrMin AND
		DATEDIFF(HOUR, LastExecTime, @Currtime) > 24



	INSERT INTO #tmpExecTask
	SELECT
		ID,
		ProcName,
		NULL
	FROM #tmpIntervalTask
	WHERE
		DATEDIFF(SECOND, LastExecTime, @Currtime) > Interval

	SELECT * from #tmpExecTask

	---------------------------
	--Exec SP through Cursor, Need to be refine if schedule job amount is more than 10
	---------------------------

	DECLARE cur CURSOR LOCAL FOR 
		SELECT ProcName 
		FROM #tmpExecTask

	OPEN cur

	FETCH NEXT FROM cur INTO @ProcedureName
	
	WHILE @@FETCH_STATUS = 0
	BEGIN
		EXEC @ProcedureName
		UPDATE #tmpExecTask SET ExecTime = @Currtime
		FETCH NEXT FROM cur INTO @ProcedureName
	END

	CLOSE cur
	DEALLOCATE cur

	SELECT * from #tmpExecTask

	UPDATE tb_ScheduleTask SET
		LastExecTime = TMP.ExecTime
	FROM #tmpExecTask AS TMP
	INNER JOIN tb_ScheduleTask AS TASK 
	ON TASK.ID = TMP.ID



	DROP TABLE #tmpScheduleTimeTask
	DROP TABLE #tmpIntervalTask
	DROP TABLE #tmpExecTask


COMMIT TRANSACTION
SET NOCOUNT OFF