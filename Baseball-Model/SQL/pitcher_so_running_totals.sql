with tmp as
(select 
	game_date
    ,left(game_date,4) as season
    ,player_id
    ,last_name
    ,first_name
    ,concat(first_name,' ',last_name) as pitcher_name
    ,team
    ,InningsPitched
    ,round(sum(InningsPitched) over (partition by player_id, left(game_date,4) order by game_date),2) as cum_innings
    ,sum(PitcherWalks) over (partition by player_id, left(game_date,4) order by game_date) as cum_walks
    ,sum(PitcherStrikeouts) over (partition by player_id, left(game_date,4) order by game_date) as cum_strikeouts
    ,row_number() over (partition by player_id, left(game_date,4) order by game_date asc) as games_played
    ,row_number() over (partition by player_id, left(game_date,4) order by game_date desc) as latest_game
from pitcher_daily_stats)

select *,
	round((cum_innings / games_played),2) as ip_per_game
    ,round((cum_walks / games_played),2) as bb_per_game
    ,round((cum_strikeouts / games_played),2) as so_per_game
    ,round((cum_strikeouts / cum_innings),2) as so_per_inning
from tmp;
-- where latest_game = 1;