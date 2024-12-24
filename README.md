# Haunt

## Purpose

Haunt is a WIP Python framework envised at building web-based desktop apps. It uses pywebview under the hood and should be compatible with any Javascript-based framework such as React, Vue, and so on.

It's primary goals are:

- Better developer ergonomics while building upon the Pywebview library.
- Simplify packaging process for making executables.
- Lightweight and fast apps.

## How it works

Haunt facilitates interaction between the Python back-end and the Javascript front-end. You can directly call python functions from javascript and vice-versa.

## Feature Roadmap

- [x] Function binding with async support
- [ ] Two-way data stores with compatibility with known Javascript frameworks
- [ ] Event-based logic

## Examples

### Hello world!

```python
from haunt.client import HauntClient

client = HauntClient()


@client.bind
def hello():
    print("Hello World!")


client.mount(path="test.html", title="Haunt", debug=True, gui="qt")
```

```html
<!-- test.html -->
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title></title>
  </head>
  <body>
    <script>
      setTimeout(function () {
        window.haunt.hello();
      }, 10);
    </script>
  </body>
</html>
```
