# Open edX xAPI plugin

## Specification

This repository is a work in progress for the integration of xAPI in the Open
edx platform. For reference, please read: [Open edX Proposal -
0026](https://github.com/edx/open-edx-proposals/pull/73).

## Getting started

First things first, if you plan to work on the project itself, you will need to
clone this repository:

```
$ git clone git@github.com:openfun/openedx-xapi.git
```

Once the project has been cloned on your machine, you will need to build a
custom edx-platform docker image that includes the xapi Django application and
setup a development environment that includes all required services up and
running (more on this later):

```bash
$ cd openedx-xapi
$ make bootstrap
```

If everything went well, you should now be able to access to the following
services:

- Open edX LMS: http://localhost:8000
- Learning locker: https://localhost:8443
- MailCatcher: http://localhost:1080

with the following credentials:

```
email: admin@foex.edu
password: openedx-rox
```

## Developer guide

Once the project has been bootstrapped (see "Getting started" section), to start
working on the project, use:

```
$ make dev
```

You can stop running services _via_:

```
$ make stop
```

If for any reason, you need to drop databases and start with fresh ones, use the
`down` target:

```
$ make down
```

## License

The code in this repository is licensed under the AGPL-3.0 unless otherwise
noted (see [LICENSE](./LICENSE) for details).
