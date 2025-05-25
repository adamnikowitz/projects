DROP TABLE IF EXISTS batter_daily_stats;
create table batter_daily_stats (
	
    game_date varchar(8),
	player_id varchar(6),
	last_name varchar(100),
	first_name varchar(100),
	starter_true integer,
	team varchar(6),
	atbats decimal(10,2),
	homeruns decimal(10,2),
	BatterWalks decimal(10,2),
	BatterSwings decimal(10,2),
	BatterStrikes decimal(10,2),
	BatterStrikesFoul decimal(10,2),
	BatterStrikesMiss decimal(10,2),
	BatterStrikesLooking decimal(10,2),
	BatterGroundBalls decimal(10,2),
	BatterFlyBalls decimal(10,2),
	BatterLineDrives decimal(10,2),
	BatterStrikeouts decimal(10,2),
	StolenBases decimal(10,2),
	CaughtBaseSteals decimal(10,2),
	ExtraBaseHits decimal(10,2),
	BatterDoublePlays decimal(10,2),
	PitchesFaced decimal(10,2),
	PlateAppearances decimal(10,2)
    );
    

