CREATE TABLE OTPDB.tb_recievedOTP (
ID int AUTO_INCREMENT PRIMARY KEY,
PhoneNo char(10),
SrvRecvTime timestamp DEFAULT CURRENT_TIMESTAMP,
PhoneRcvUnixTime int,
OTPType varchar(32),
PassCode varchar(32)
)
