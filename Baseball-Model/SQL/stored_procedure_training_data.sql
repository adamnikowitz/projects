DELIMITER //

create procedure training_data(IN training_date varchar(8))

begin 

with game_dates as
(select 
	distinct game_date
from pitcher_daily_stats)

,player_dates as
(select
	distinct player_id
    ,a.game_date 
from pitcher_daily_stats
cross join game_dates a)

,pitcher_stats as
(select 
	game_date as pitcher_game_date
    ,player_id as pitcher_player_id
    ,last_name
    ,first_name
    ,concat(first_name,' ',last_name) as pitcher_name
    ,team
    ,InningsPitched
    ,PitcherStrikeouts
    ,round(sum(InningsPitched) over (partition by player_id order by game_date),2) as cum_innings
    ,sum(PitcherWalks) over (partition by player_id order by game_date) as cum_walks
    ,sum(PitcherStrikeouts) over (partition by player_id order by game_date) as cum_strikeouts
    ,row_number() over (partition by player_id order by game_date asc) as games_played
    ,row_number() over (partition by player_id order by game_date desc) as latest_game
from pitcher_daily_stats)

,running_totals as
(select *,
	round((cum_innings / games_played),2) as ip_per_game
    ,round((cum_walks / games_played),2) as bb_per_game
    ,round((cum_strikeouts / games_played),2) as so_per_game
    ,ifnull(round((cum_strikeouts / cum_innings),2),0) as so_per_inning
from pitcher_stats)

,schedule as
(select 
	game_id
    ,season
    ,game_date as schedule_game_date
    ,game_time
    ,away_team as schedule_team
    ,home_team as opponent_team
    ,stadium
    ,0 as home_team
from stg_full_game_schedule

union all

select 
	game_id
    ,season
    ,game_date
    ,game_time
    ,home_team as schedule_team
    ,away_team as opponent_team
    ,stadium
    ,1 as home_team
from stg_full_game_schedule)

,batter_stats as
(with tmp as
(select 
	game_date 
    ,team
	,sum(batterstrikeouts) as total_strikeouts
    ,sum(atbats) as total_atbats
    ,sum(PlateAppearances) as total_plate_appearances
    ,sum(BatterWalks) as total_batter_walks
from batter_daily_stats
group by game_date, team
order by game_date)

,tmp2 as
(select 
	team
    ,game_date as batter_game_date
    ,sum(total_strikeouts) over (partition by team order by game_date) as cum_strikeouts
    ,sum(total_atbats) over (partition by team order by game_date) as cum_atbats
    ,sum(total_plate_appearances) over (partition by team order by game_date) as cum_pa
    ,sum(total_batter_walks) over (partition by team order by game_date) as cum_batter_walks
    ,row_number() over (partition by team order by game_date) as games_played
    ,row_number() over (partition by team order by game_date desc) as latest_game
from tmp)

select *,
	round((cum_strikeouts / games_played),2) as batter_so_per_game
    ,round((cum_atbats / games_played),2) as ab_per_game
    ,round(((cum_strikeouts / games_played) / (cum_atbats / games_played)),2) as batter_so_rate
    ,round((cum_pa / games_played),2) as pa_per_game
    ,round((cum_batter_walks / games_played),2) as batter_walk_per_game
from tmp2) -- select * from batter_stats;

select 
	-- player info
    player_id
    ,pitcher_name
    ,rt.team
    ,opponent_team
    -- game info
    ,game_id
    ,game_date
    ,game_time
    ,season
    ,stadium
    ,home_team
    -- target
    ,pitcherstrikeouts
    -- pitcher stats
    ,rt.latest_game as game_number
    ,ip_per_game
    ,bb_per_game
    ,so_per_game
    ,so_per_inning
    -- batter stats
    ,batter_so_per_game
    ,ab_per_game
    ,batter_so_rate
    ,pa_per_game
    ,batter_walk_per_game
from player_dates pd
inner join running_totals rt
	on pd.game_date = rt.pitcher_game_date 
    and pd.player_id = rt.pitcher_player_id
inner join schedule s
	on pd.game_date = s.schedule_game_date
    and rt.team = s.schedule_team
inner join batter_stats bs
	on s.opponent_team = bs.team
    and pd.game_date = bs.batter_game_date
where InningsPitched > 0
	and game_date < training_date;
    
end//

DELIMITER ;