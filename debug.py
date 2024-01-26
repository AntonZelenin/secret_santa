def outer_function():
    outer_var = 10

    def inner_function():
        nonlocal outer_var
        outer_var += 1

    inner_function()
    print(outer_var)  # Output: 11

outer_function()