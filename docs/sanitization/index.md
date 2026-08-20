---
icon: lucide/brush-cleaning
---

# Sanitizing attributes



There's two different ways of sanitizing [`Unsafe`](../reference.md#beware.Unsafe) fields: with a **decorated function** or inside of a **context manager**. Let's see how the `email` field from the previous example can be handled using these two strategies.

!!! note
    Default values can be accessed without sanitization, see [Caveats](../caveats.md#default-value-and-del) for more details.

=== "Decorator"

    ```python
    @sanitizes(UserForm.email)
    def clean_user_email(param: A):
        ...

    received = UserForm()

    clean_user_email(received)

    print(received.email)
    ```

=== "Context Manager"

    ```python
    received = UserForm()
    with sanitize_context(UserForm.email):
        ... 
        
    print(received.email)
    ```

Keep in mind that only **modified** fields are marked as sanitized in the end. So, if your function or context sanitizes a given attribute, only the instances that assigned a new value to the same attribute are going to be sanitized at the end.

=== "Decorator"

    ```python
    @sanitizes(A.a)
    def my_cleaning_function(param: A):
        ...
    ```

=== "Context Manager"

    ```python
    with sanitize_context(A.a):
        ...
    ```


