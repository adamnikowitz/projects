DROP TABLE IF EXISTS odds_2024;
create table odds_2024 (
	
    game_date varchar(8),
	player varchar(100),
	team varchar(6),
	bet decimal(10,2),
	over_odds decimal(10,2),
	under_odds decimal(10,2),
	over_pct decimal(10,2),
	under_pct decimal(10,2)
    );