CREATE TABLE RequestCollectorDB.tb_OrderInfo (
ID int AUTO_INCREMENT PRIMARY KEY,
IdentifierCol varchar(64),
IdentValue varchar(128),
RecievedTime timestamp DEFAULT CURRENT_TIMESTAMP,
RecvUnixTime int,
ReqBodyFormat varchar(16),
RequestType varchar(64),
RequestCategory varchar(64), 
RequestHeader varchar(2048),
RequestBody varchar(4096),
RequestArguments varchar(1024)
)
