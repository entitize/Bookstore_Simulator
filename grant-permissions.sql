CREATE USER 'appadmin'@'localhost' IDENTIFIED BY 'admin';
CREATE USER 'appclient'@'localhost' IDENTIFIED BY 'client';
GRANT ALL PRIVILEGES ON cs121_final_project.* TO 'appadmin'@'localhost';
GRANT SELECT ON cs121_final_project.* TO 'appclient'@'localhost';
GRANT INSERT ON cs121_final_project.* TO 'appclient'@'localhost';
FLUSH PRIVILEGES;