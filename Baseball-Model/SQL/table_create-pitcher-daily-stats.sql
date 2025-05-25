DROP TABLE IF EXISTS pitcher_daily_stats;
create table pitcher_daily_stats (
	
    game_date varchar(8),
    game_id varchar(8),
	player_id varchar(6),
	last_name varchar(100),
	first_name varchar(100),
    team varchar(6),
	starter_true integer,
	InningsPitched decimal(10,2),
	HitsAllowed decimal(10,2),
	EarnedRunsAllowed decimal(10,2),
	PitcherWalks decimal(10,2),
	PitcherSwings decimal(10,2),
	PitcherStrikes decimal(10,2),
	PitcherStrikeouts decimal(10,2)
    );
    
select * from pitcher_daily_stats where PitcherStrikeouts >= 10;
