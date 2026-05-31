
## Default value and `del`

The behavior of deleting a field , this is primarly to conform with the `default`
parameter on dataclasses Field


So this would happen:

```
>>> class MyClass:
...     attr = unsafe(default=1) 

>>> instance = MyClass()
>>> instance.attr
1
>>> del instance.attr
>>> instance.attr
1
```


## Field override

