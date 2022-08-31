PyDui Documentation
===================

[![Docs](https://img.shields.io/badge/docs-latest-informational)](https://dzhsurf.github.io/pydui/)



![PyDui-GTK](https://github.com/dzhsurf/pydui/raw/main/docs/source/_static/apple-touch-icon-180x180.png)



## Introduction

**PyDui base on GTK-3, PyGObject**

Even though there is GTK/Glade can quickly and efficiently build a powerful UI Application. But the Glade is not easy enough to learn. Sometimes, we need another solution for rapidly building a simple app. I think, on the windows platform, DuiLib is an option because it's easy to learn.


**Why not just wrap the DuiLib API ?** 

This is a good question because DuiLib only works on windows. And the author work on mac. So, this is not for cross-platform purposes, just personal reasons.


**The simple layout rule**

PyDui only has one layout rule, it's easy to understand how it works.



## Install

`PyDui require python >= 3.9`

Even though it's easy to downgrade the python version, personal reasons, the author DO NOT WANT TO KEEP ALL THE VERSION WORK!

```shell
pip install pydui-gtk
```



## Code Example

```python
import pydui
from pydui import *


class DemoWindowHandler(PyDuiWindowHandler):
    def __init__(self, window: PyDuiWindow):
        super().__init__(window=window)

    def on_window_show(self):
        print(f"on_window_show")
        window = self.window()
        widget = window.get_widget(widget_id="button")

        def handle_click(object):
            print("You clicked!", object)

        widget.connect("clicked", handle_click)

    def on_window_destroy(self):
        print(f"on_window_destroy")
        PyDuiApplication.main_quit()


def main():
    print(f"start pydui version: {pydui.__version__}")

    window = PyDuiBuilder.build_window(
        path="res/main.xml",
        handler=DemoWindowHandler,
    )
    window.show()

    PyDuiApplication.main_run()


if __name__ == "__main__":
    main()

```




## Build Environment Setup

```shell
# first, checkout the code
# second, use conda setup environment 
conda env create -f conda_env.yaml
conda activate pydui
# local install 
pip install -e .
```





## Development

In the early stage, performance optimization, resource leakage issue, text rendering quality, and correctness issue are not the primary tasks. The first task is to complete the essential module function.

* Core
  * Builder, Render, Event Dispatch

* Layout
  * HLayout, VLayout, FixedLayout, FitLayout 
* Widgets
  * Label, Button, Image, Edit, InfiniteList, Menu, Toast
* Deployment
  * Resource builder
  * Application builder
* Special Features
  * Drag&Drop
  * Model Window
  * Intl
  * RichText
  * Window Shadow



## Reference

https://lazka.github.io/pgi-docs/Gtk-3.0/index.html

https://valadoc.org/gtk+-3.0/index.htm

https://python-gtk-3-tutorial.readthedocs.io/en/latest/index.html