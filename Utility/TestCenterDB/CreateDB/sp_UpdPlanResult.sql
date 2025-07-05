ALTER PROCEDURE [dbo].[sp_UpdPlanResult]
AS
SET NOCOUNT ON
BEGIN TRANSACTION

DECLARE @FirstPlanGUID CHAR(36)
DECLARE @FirstTaskID int
DECLARE @FirstTaskID2 int

--Create temp table for running test plans
	CREATE TABLE #tempPlan
	(
		[ID] INT,
		[RuntimeGUID] CHAR(36),
		[LastUpdTime] DATETIME,
		[Status] SMALLINT

	)
	CREATE INDEX [Idx_Src_ID] ON #tempPlan (ID)

--Create temp table for related test task
	CREATE TABLE #tempTask
	(
		[ID] INT,
		[PlanRuntimeGUID] CHAR(36),
		[TaskGUID] CHAR(32),
		[LastUpdTime] DATETIME,
		[Status] VARCHAR(16),
		[SumCaseAmount] INT
	)
	CREATE INDEX [Idx_Src_ID] ON #tempTask (ID)

	--Insert test plans still running or not updated yet(Status < 100)
	INSERT INTO #tempPlan
	SELECT
		ID,
		PlanRuntimeGUID,
		NULL,
		NULL
	FROM tb_TestPlanStat WITH (NOLOCK)
	WHERE Status < 100

	SET @FirstPlanGUID = (SELECT TOP 1 RuntimeGUID FROM #tempPlan)
	SET @FirstTaskID = (SELECT TOP 1 ID FROM tb_TaskStat WHERE PlanRuntimeGUID = @FirstPlanGUID)


	IF  @FirstTaskID IS NULL
	BEGIN
		SET  @FirstTaskID = (SELECT MIN(ID) FROM tb_TaskStat)
	END


	INSERT INTO #tempTask
	SELECT
		ID,
		PlanRuntimeGUID,
		TaskGUID,
		LastUpdTime,
		Status,
		SumCaseAmount
	FROM tb_TaskStat WITH (NOLOCK)
	WHERE ID >= @FirstTaskID



	--SELECT * FROM #tempPlan
	--SELECT * FROM #tempTask

	--select * from #tempPlan inner join #tempTask on #tempPlan.RuntimeGUID = #tempTask.PlanRuntimeGUID

	UPDATE #tempPlan SET
		LastUpdTime = (SELECT MAX(LastUpdTime) FROM #tempTask WHERE PlanRuntimeGUID = P.RuntimeGUID),
		Status = CASE WHEN
			(SELECT COUNT(ID)
			 FROM #tempTask 
			 WHERE Status = 'Complete' AND
			  PlanRuntimeGUID = P.RuntimeGUID)
			   = 
			(SELECT COUNT(ID)
			 FROM #tempTask 
			 WHERE  PlanRuntimeGUID = P.RuntimeGUID) THEN 100
			 ELSE 3
			 END
	FROM #tempPlan AS P
	INNER JOIN #tempTask AS T 
	ON P.RuntimeGUID = T.PlanRuntimeGUID

	DELETE FROM #tempPlan WHERE LastUpdTime is NULL

	select * from #tempPlan

	UPDATE tb_TestPlanStat SET
		LastUpdTime = TMP.LastUpdTime,
		Status = TMP.Status
	FROM tb_TestPlanStat AS P
	INNER JOIN #tempPlan AS TMP WITH (NOLOCK)
	ON P.ID = TMP.ID

	select * from tb_TestPlanStat

	DROP TABLE  #tempPlan
	DROP TABLE #tempTask 

COMMIT TRANSACTION
SET NOCOUNT OFF