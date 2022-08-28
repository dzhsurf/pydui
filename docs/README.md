PyDui Documents
===============

## How to generate docs?

```shell
make gettext
make intl
make intl-build
```


## How to add more languages?

```shell
# Edit Makefile 
# sphinx-intl update -p en/latest/gettext -l zh_CN 
# append language follow rules: -l ja -l zh_CN ... 
# then regenerate the docs
```


