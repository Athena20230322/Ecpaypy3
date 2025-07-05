ALTER PROCEDURE [dbo].[sp_ExpireRunningPlan]
AS
SET NOCOUNT ON
BEGIN TRANSACTION

DECLARE @FirstPlanGUID CHAR(36)
DECLARE @CurrDateTime DATETIME

SET @CurrDateTime = GETDATE()

--Create temp table for running test plans
	CREATE TABLE #tempPlan
	(
		[ID] INT,
		[RuntimeGUID] CHAR(36),
		[TriggerTime] DATETIME,
		[LastUpdTime] DATETIME,
		[Status] SMALLINT

	)
	CREATE INDEX [Idx_Src_ID] ON #tempPlan (ID)

	INSERT INTO #tempPlan
	SELECT
		ID,
		PlanRuntimeGUID,
		TriggerTime,
		LastUpdTime,
		NULL
	FROM tb_TestPlanStat WITH (NOLOCK)
	WHERE Status < 100

	UPDATE #tempPlan SET
		Status = 101
	WHERE
		DATEDIFF(HOUR, LastUpdTime, @CurrDateTime) >= 1
		OR DATEDIFF(HOUR, TriggerTime, @CurrDateTime) >= 24

	select * from #tempPlan

	DELETE FROM #tempPlan WHERE Status is NULL

	UPDATE tb_TestPlanStat SET
		Status = TMP.Status
	FROM tb_TestPlanStat AS P
	INNER JOIN #tempPlan AS TMP WITH (NOLOCK)
	ON P.ID = TMP.ID


	DROP TABLE #tempPlan



COMMIT TRANSACTION
SET NOCOUNT OFF