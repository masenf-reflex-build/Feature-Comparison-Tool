
CREATE TABLE feature_analysis (
	`Feature` STRING, 
	`Current_Value` DOUBLE, 
	`Optimal_Value` DOUBLE, 
	`Percentage_Difference` DOUBLE, 
	`Optimal_Status` STRING, 
	`ZN_Importance` DOUBLE, 
	`ZN_Rank` DOUBLE, 
	`CO3_Importance` DOUBLE, 
	`CO3_Rank` DOUBLE, 
	`Difference_Value` DOUBLE, 
	`Absolute_Difference_Value` DOUBLE, 
	`Model_Selection` STRING, 
	`Bounded_Min` DOUBLE, 
	`Bounded_Max` DOUBLE, 
	`Min_Data` DOUBLE, 
	`Max_Data` DOUBLE
) USING DELTA
TBLPROPERTIES('delta.feature.allowColumnDefaults' = 'enabled')


