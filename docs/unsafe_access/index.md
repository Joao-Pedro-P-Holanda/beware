---
icon: lucide/shield-alert
---

# Unsafe variable access

You can access a [`Unsafe`](../reference.md#beware.Unsafe) field without sanitizing it first using the [`unsafe_context`](../reference.md#beware.unsafe_context) (if you really have to).


```python

received = UserForm() 

with unsafe_context(UserForm.email):
    print(f"User raw email is {received.email}")

print(f"User email outside contenxt {received.email}") # raises UnsafeReferenceException
```


