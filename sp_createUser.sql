CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_createUser`(
    IN p_name VARCHAR(30),
    IN p_username VARCHAR(30),
    IN p_password VARCHAR(30)
)
BEGIN
    if ( select exists (select 1 from sign_up where user_username = p_username) ) THEN
     
        select 'Username Exists !!';
     
    ELSE
     
        insert into sign_up
        (
            user_name,
            user_username,
            user_password
        )
        values
        (
            p_name,
            p_username,
            p_password
        );
     
    END IF;
END