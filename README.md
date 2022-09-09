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

![Demo](https://github.com/dzhsurf/pydui/raw/main/images/demo.png)

```python
import pydui
from pydui import *
from pydui.core.resource_loader import create_default_resource_loader

# config builder here
def get_builder() -> PyDuiBuilder:
    builder = PyDuiBuilder()
    builder.register_resource_loader(create_default_resource_loader())
    return builder

# custom window handler
class DemoHandler(PyDuiWindowHandler):
    def on_window_init(self, window: PyDuiWindow):
        print(f"on_window_init")
        
        def handle_click(object):
            print("You clicked!", object)
            
        # bind widget event here
        widget = window.get_widget(widget_id="button")
        widget.connect("clicked", handle_click)

    def on_window_destroy(self):
        print(f"on_window_destroy")
        PyDuiApplication.main_quit()


def main():
    print(f"start pydui version: {pydui.__version__}")

    window = get_builder().build_window(path="res/main.xml", handler=DemoHandler)
    window.show()

    PyDuiApplication.main_run()

if __name__ == "__main__":
    main()
```

XML File

```xml
<?xml version="1.0" encoding="utf-8"?>
<Window size="800,600" title='Quickstart Demo' min_size="400,300">
    <HLayout bkcolor="#FFE8E8E8">
        <VLayout bkcolor="#FFA8A8A8" width="200">
            <Label text="测试中文字体渲染,自动换行自动换行自动换行自动换行" font="Helvetica" fontsize="13" fontcolor="#FFFF0000"
                margin="20,20,20,20" />
        </VLayout>
        <VLayout halign="CENTER">
            <Button id="button" text="Click Me" margin="8,8,8,8"
                corner="12,12,12,12" width="200" height="48"
                bkimage="res/images/common_button_normal.png"
                bkimage_hover="res/images/common_button_hover.png"
                bkimage_press="res/images/common_button_press.png"
                bkimage_disable="res/images/common_button_disable.png"
            />
            <Label text="Test single line text end ellipsis, here is the long text document.Test single line text end ellipsis, here is the long text document."
                font="Helvetica Light"
                fontsize="16"
                fontcolor="#FF1A1A1A"
                bkcolor="#FFC8C8C8"
                wrap="NONE"
                margin="20,0,20,0"
            />
            <Label text="Test single line text middle ellipsis, here is the long text document.Test single line text middle ellipsis, here is the long text document."
                font="Helvetica"
                fontsize="16"
                fontcolor="#FF1A1A1A"
                wrap="NONE"
                ellipsis="MIDDLE"
                margin="20,20,20,20"
            />
            <Label text="Test Multi line text wrap text. Hello World!!! ctx.set_font_options() is part of the cairo toy font API and ignored by...
                font="SourceCodePro"
                fontsize="16"
                fontcolor="#FF1A1A1A"
                margin="20,20,20,20"
            />
        </VLayout>
    </HLayout>
</Window>
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
  * Label, Button, Picture, Edit, InfiniteList, Menu, Toast
* Deployment
  * Resource builder
  * Application builder
* Special Features
  * Text selection
  * Drag&Drop
  * Model Window
  * Intl
  * RichText
  * Window Shadow



## Development progress

Builder:

* Window - finish

* Label - finish
* Button - finish
* HLayout - finish
* VLayout - finish 

ResourceLoader:

* DefaultResourceLoader - finish

Render:

* DrawRetangle - finish
* DrawImage - finish
* DrawText - finish
* Hi-DPI suppose - almost done
* Draw area boundary protection - 0%, processing

Layout:

* HLayout - finish
* VLayout - finish
* FixedLayout - 0%
* FitLayout - 0%

Widget:

* Widget base - finish
* Label - finish
* Button - finish
* Edit - 0%, processing
  * Focus event suppose
* Picture - 0%, processing
* InfiniteList - 0%, not started
* Menu - 0%, not started



## Reference

Python Gtk-3 Tutorial: https://python-gtk-3-tutorial.readthedocs.io/en/latest/index.html

Python Gtk-3: https://lazka.github.io/pgi-docs/Gtk-3.0/index.html

Python Gdk-3: https://lazka.github.io/pgi-docs/Gdk-3.0/index.html

Python GdkPixbuf: https://lazka.github.io/pgi-docs/GdkPixbuf-2.0/index.html

Python Pango: https://lazka.github.io/pgi-docs/Pango-1.0/index.html

Pycairo: https://pycairo.readthedocs.io/en/latest/index.html

PyGObject: https://pygobject.readthedocs.io/en/latest/index.html

Python PangoCairo: https://lazka.github.io/pgi-docs/PangoCairo-1.0/index.html

---

Gtk-3: https://docs.gtk.org/gtk3/index.html

Pango: https://docs.gtk.org/Pango/index.html

GdkPixbuf: https://docs.gtk.org/gdk-pixbuf/index.html

PangoCairo: https://docs.gtk.org/PangoCairo/

---

Gtk pgi Symbol Mapping: https://lazka.github.io/pgi-docs/Gtk-3.0/mapping.html