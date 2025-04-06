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
CREATE TABLE IF NOT EXISTS logined_user_follow
(
    user_logined_id SERIAL NOT NULL,
    user_logined_ip inet NOT NULL,
    user_login varchar(50) NOT NULL,
	user_logined_utc_data VARCHAR(20) NOT NULL,
    PRIMARY KEY (user_logined_id)
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
