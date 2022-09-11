# Yinglong 

![](https://img.shields.io/badge/python-3.6+-orange)
![](https://img.shields.io/badge/Flask-0.12.2-blue)
![](https://img.shields.io/badge/documentation-yes-green)
![](https://img.shields.io/badge/maintained-yes-yellowgreen)
![](https://img.shields.io/badge/License-yes-yellow)

This is a project created and maintained by the Redflag organization. This project is an open source threat intelligence collection and publishing system that provides API usage. Please use this project reasonably and legally.

## Enviroment

- Python 3.6+
- Flask 0.12.2
- Flask-SQLAlchemy 2.5.1
- celery 5.1.2
- redis 4.3.4
- APScheduler 3.9.1

## APIs

| API | means |
| --- | --- |
| /api/phishing/ | Get the phishing website information of the day |
| /api/botnet/ | Get the botnet information of the day |

## Usage

Install dependencies

```shell
pip install -r requirements.txt
```
Run the program

```shell
python manage.py runserver
```
## Contributors

- [Quanfita](https://github.com/Quanfita)
- [RF&CTI](https://github.com/RFCTI)

## License

MIT License

Copyright (c) 2022 Redflag Organization.
