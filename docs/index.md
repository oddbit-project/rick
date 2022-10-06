# Welcome to Rick

[![Tests](https://github.com/oddbit-project/rick/workflows/Tests/badge.svg?branch=master)](https://github.com/oddbit-project/rick/actions)
[![pypi](https://img.shields.io/pypi/v/rick.svg)](https://pypi.org/project/rick/)
[![license](https://img.shields.io/pypi/l/rick.svg)](https://github.com/oddbit-project/rick/blob/master/LICENSE)

Rick is a plumbing library for micro framework design. It provides base classes for miscellaneous purposes, ranging from
dependency injection to validation. However, it does not include any HTTP/{A,W}SGI functionality, nor any database-related 
functionality; you should instead using other existing projects for that functionality, such as [Flask](https://flask.palletsprojects.com) for
MVC and [RickDb](https://github.com/oddbit-project/rick_db) for database operations.

## Components
- Dependency Injection (DI) class;
- Container class;
- Generic resource map loader class;
- Registry class;
- Cache interface;
- REDIS cache client;
- AES256 crypto functions for cache mechanisms;
- Event manager;
- [Request validator](forms/requests.md);
- [Form management](forms/index.md)
- [Validation classes](validators/index.md);
- [Filters](filters/index.md)

