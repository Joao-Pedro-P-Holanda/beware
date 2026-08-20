---
icon: lucide/pencil
---

# Declaring [`Unsafe`](../reference.md#beware.Unsafe) attributes

You can use the [`unsafe`](../reference.md#beware.unsafe) function to specify that a field should only be accessible  after some sanitization modifies it.

```python hl_lines="2 5"
from datetime import datetime
from beware import unsafe

class UserForm:
    name: str 
    email: str = unsafe()
    answer_time: datetime
```

Now everytime you try to instantiate an object of type `UserForm` and access the attribute `email` you will get an [`UnsafeReferenceException`](../reference.md#beware.exceptions.UnsafeReferenceException). 

In the [sanitization](../sanitization/index.md) section we are going to see how an [`Unsafe`](../reference.md#beware.Unsafe) can be validated by the library.

