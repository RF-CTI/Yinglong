# Yinglong 

![](https://img.shields.io/badge/python-3.6+-orange)
![](https://img.shields.io/badge/Flask-0.12.2-blue)
![](https://img.shields.io/badge/documentation-yes-green)
![](https://img.shields.io/badge/maintained-yes-yellowgreen)
![](https://img.shields.io/badge/License-yes-yellow)

This is a project created and maintained by the Redflag organization. This project is an open source threat intelligence collection and publishing system that provides API usage. Please use this project reasonably and legally.

## APIs

| API | means |
| --- | --- |
| /api/phishing/ | Get the phishing website information of the day |
| /api/botnet/ | Get the botnet information of the day |
| /api/c2/ | Get the C&C information of the day |

## Wiki

If you have any problem, you can look at [wiki](https://github.com/RF-CTI/Yinglong/wiki) that include all APIs usage.

Attention: If you have problems with authentication in API usage, please see [How to use authentication](https://github.com/RF-CTI/Yinglong/wiki/Must-see-before-use---instructions-on-authentication).

## Enviroment

- Python 3.6+
- Flask 0.12.2
- Flask-SQLAlchemy 2.5.1
- celery 5.1.2
- redis 4.3.4
- APScheduler 3.9.1

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
