CREATE TABLE IF NOT EXISTS Register_user_data
(
	user_id SERIAL NOT NULL,
	user_login VARCHAR(50) NOT NULL,
	user_password VARCHAR(50) NOT NULL,
	user_ip inet NOT NULL,
	utc_user_regdata VARCHAR(20) NOT NULL,
	PRIMARY KEY(user_id)
)
;
CREATE TABLE IF NOT EXISTS user_follow
(
    user_logined_id SERIAL NOT NULL,
    user_logined_ip inet NOT NULL,
    user_login varchar(50) NOT NULL,
	user_logined_utc_data VARCHAR(20) NOT NULL,
	user_done VARCHAR NOT NULL,
	topic_name VARCHAR NOT NULL,
	user_message VARCHAR NOT NULL,
	PRIMARY KEY (user_logined_id)
);


CREATE TABLE IF NOT EXISTS sport_topic_bd
(
	user_message_id SERIAL NOT NULL,
	user_message VARCHAR NOT NULL,
	user_message_utc_time VARCHAR(20) NOT NULL,
	user_login VARCHAR(50) NOT NULL,
	PRIMARY KEY(user_message_id)
);
CREATE TABLE IF NOT EXISTS FFIP_upgrades_topic_bd
(
	user_message_id SERIAL NOT NULL,
	user_message VARCHAR NOT NULL,
	user_message_utc_time VARCHAR(20) NOT NULL,
	user_login VARCHAR(50) NOT NULL,
	PRIMARY KEY(user_message_id)
);
CREATE TABLE IF NOT EXISTS games_topic_bd
(
	user_message_id SERIAL NOT NULL,
	user_message VARCHAR NOT NULL,
	user_message_utc_time VARCHAR(20) NOT NULL,
	user_login VARCHAR(50) NOT NULL,
	PRIMARY KEY(user_message_id)
);
/*
	Обєднання 2-х таблиць по ip користувача
SELECT register_user_data.user_id,
register_user_data.user_login,
register_user_data.user_ip,
logined_user_follow.user_logined_ip,
logined_user_follow.user_logined_utc_data
FROM register_user_data
INNER JOIN logined_user_follow ON register_user_data.user_ip = logined_user_follow.user_logined_ip
*/
