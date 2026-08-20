---
icon: lucide/flag
---

# Caveats

There are specific points of the library that can cause some confusion at first.
In the next sections we try to clear the most error-prone points of the library.

If you want a deeper explanation on how the Descriptor mechanism works, you can
check Python's [HOWTO Guide](https://docs.python.org/3/howto/descriptor.html).

## Attribute only

The internal implementation of `beware` uses Python Descriptors to track the 
sanitization state of instance attributes, thus the library can only keep track
of accessed with dot notation or the `__getattribute__` magic method.

This also means that accessing a descriptor field as a class attribute will return
the `Unsafe` descriptor instead. 


## Default value and `del`

Deleting an attribute with default values has a side effect that can be an unexpected behavior: 
the default field is returned when accessing a deleted field instead of raising an error. 
This is primarly to conform with the `default` parameter on dataclasses Field, that
does the same thing.


So after deletion this would happen:

```python 
>>> class MyClass:
...     attr = unsafe(default=1) 

>>> instance = MyClass()
>>> instance.attr
1
>>> del instance.attr
>>> instance.attr # Your code could expect an AttributeError here
1
```


## Subclassing and field override

Another relevant point is subclassing classes with `Unsafe` fields.

If you define a subclass containing a class attribute with the same name of the 
Descriptor field, the unsafe logic will be overwritten on the subclass.

```python hl_lines="2 5 8 9"
>>> class ParentClass:
...     attr: int = Unsafe()
...
>>> class ChildClass(ParentClass):
...     attr: int = 10
...
>>> child = ChildClass()
>>> child.attr == 10 # can be accessed normally
10
```

Conversively, instance attributes are shadowed by a Descriptor in a parent class.

```py hl_lines="2 6 9"
>>> class ParentClass:
...     attr: int = Unsafe()
...
>>> class ChildClass(ParentClass):
...     def __init__(self, attr:int):
...         self.attr = attr
...
>>> child = ChildClass(10)
>>> child.attr == 10 # raises beware.exceptions.UnsafeReferenceException
```

