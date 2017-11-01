CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_learnersLicense`(
    IN p_firstname varchar(10),
    IN p_lastname varchar(10),
    IN p_dob date,
    IN p_sex varchar(6),
    in p_aadharno decimal(12),
    in p_mobileno decimal(10),
    IN p_addressno int,
    IN p_addresslocality varchar(10),
    IN p_addressdistrict varchar(10),
	IN p_addresspincode decimal(6),
    IN p_licensetype varchar(6),
    in p_rtooffice varchar(4),
	in p_photo mediumblob,
    in p_addressproof mediumblob,
    in p_aadharcard mediumblob,
    in p_email varchar(30)
)
BEGIN
    if ( select exists (select 1 from license where aadharno = p_aadharno) ) THEN
     
        select 'Username Exists !!';
     
    ELSE
     
        insert into license
        (
            firstname,lastname,dob,sex,aadharno,mobileno,address_no,address_locality,address_district,
            address_pincode,licensetype,rtooffice,photo,address_proof,aadharcard,loginid
        )
        values
        (
            p_firstname,
   p_lastname,
    p_dob,
    p_sex,
   p_aadharno,
    p_mobileno,
    p_addressno ,
    p_addresslocality,
     p_addressdistrict,
	 p_addresspincode,
    p_licensetype,
    p_rtooffice,
    p_photo,
	p_addressproof,
    p_aadharcard,
    (select user_id from sign_up where user_username = p_email)
        );
     
    END IF;
END