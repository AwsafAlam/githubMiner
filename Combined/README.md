## Desc

Files to run: downloadRunner.py, finderRunner.py (no command line parameters needed)


### Set Parameters

All necessary parameters should be given in config.py. 

### Issues

if db schema in DB.txt gives errors, use the following

```
CREATE TABLE `repos` (
  `id` int(20) NOT NULL,
  `url` varchar(200) NOT NULL,
  `language` varchar(20) DEFAULT NULL,
  `downloaded` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `repos_id_uindex` (`id`),
  UNIQUE KEY `repos_url_uindex` (`url`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8

```
