DROP TABLE IF EXISTS full_game_schedule;
create table stg_full_game_schedule (
	
    game_id varchar(8),
	season varchar(4),
	game_date varchar(8),
	game_time varchar(8),
	away_team varchar(8),
	home_team varchar(8),
	stadium varchar(100)
    );
    
select * from stg_full_game_schedule;