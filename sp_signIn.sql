CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_signIn`(
    IN p_username VARCHAR(30),
    IN p_password VARCHAR(30)
)
BEGIN
    if ( select exists (select 1 from sign_up where user_username = p_username and user_password = p_password) ) THEN
     
        select user_name from sign_up where user_username = p_username;
     
    END IF;
END