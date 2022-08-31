PyDui Documentation
===================

[![Docs](https://img.shields.io/badge/docs-latest-informational)](https://dzhsurf.github.io/pydui/)



![PyDui-GTK](https://github.com/dzhsurf/pydui/raw/main/docs/source/_static/apple-touch-icon-180x180.png)



## Introduction

**PyDui base on GTK-3, PyGObject**

PyDui is based on PyGObject/GTK-3, but totally runs on self-drawing canvas. Because GTK-3 widgets are not easy to understand how it works. We are tent to provide an easy API to help developers to build UI applications more quickly and efficiently, putting more focus on the product either than the details of the framework.



Why choose GTK, not QT or any other framework as the low-level module?
As GTK is a powerful cross-platform framework, it can run on Windows, MacOSX, and Linux well, and it's light enough, fewer dependencies mean it can be easy to pack and deploy.



And why use self-drawing instead of GTK's widget pattern?
Even though there is GTK/Glade can quickly build a powerful UI Application. But the Glade is not easy enough to learn. Especially the layout design pattern on GTK is terrible hell for developers and designers.



Sometimes, we need another solution for rapidly building a simple app. I think, on the windows platform, DuiLib is an option because it's easy to learn. That is the reason we use self-drawing to reimplement all the virtual widgets.




**Why not just wrap the DuiLib API ?** 

This is a good question because DuiLib only works on windows. And the author work on mac. So, this is not for cross-platform purposes, just personal reasons.



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





## Layout Rule

>  TODO: 
> ...





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