Contents:
- [/api/register/email](#apiregisteremail)
- [/api/register/email/resend-verification-code](#apiregisteremailresend-verification-code)
- [/api/register/email-verification-code](#apiregisteremail-verification-code)
- [/api/register/password](#apiregisterpassword)
- [/api/register/username](#apiregisterusername)
- [/api/login](#apilogin)
- [/api/logout](#apilogout)
- [/api/password/request-reset](#apipasswordrequest-reset)
- [/api/password/reset](#apipasswordreset)

## /api/register/email

Supported methods: POST

Creates a new user with the given email address, sends an email with a verification code to the user.

Request:
```json
{
    "email": "string"
}
```

Response:

HTTP status code 200
```json
{}
```

HTTP status code 400
```json
{
    "error": "object"
}
```

## /api/register/email/resend-verification-code

Supported methods: POST

Resends the verification code to the user's email address if the resend cooldown has passed (1 minute).

Request:
```json
{
    "user_id": "string"
}
```

Response:

HTTP status code 200
```json
{}
```

HTTP status code 400
```json
{
    "error": "object"
}
```

## /api/register/email-verification-code

Supported methods: POST

Checks the verification code sent to the user's email address and marks the user as verified if the code
is correct. Returns a `set_password_token` that should be used to create a password for the user.

Request:
```json
{
    "user_id": "string",
    "verification_code": "string"
}
```

Response:

HTTP status code 200
```json
{
    "set_password_token": "string"
}
```

HTTP status code 400
```json
{
    "error": "object"
}
```

## /api/register/password

Supported methods: POST

Creates a password for the user with the given `set_password_token`. Returns a `create_username_token` that should be used to create a username for the user.

Request:
```json
{
    "user_id": "string",
    "set_password_token": "string",
    "password": "string"
}
```

Response:

HTTP status code 200
```json
{
    "create_username_token": "string"
}
```

HTTP status code 400
```json
{
    "error": "object"
}
```

## /api/register/username

Supported methods: POST

Creates a username for the user with the given `create_username_token`.

Request:
```json
{
    "create_username_token": "string",
    "username": "string"
}
```

Response:
HTTP status code 200
```json
{}
```

HTTP status code 400
```json
{
    "error": "object"
}
```

# /api/login

Supported methods: POST

Logs in the user with the given credentials. Returns a `key` that is used to authenticate the user

Request:
```json
{
    "email": "string",
    "password": "string"
}
```

Reesponse:

HTTP status code 200
```json
{
    "key": "string"
}
```

HTTP status code 400
```json
{
    "non_field_errors": "list[string]"
}
```

# /api/logout

Supported methods: POST

Request should contain no body and the `Authorization: Token <auth-token>` header should be provided.


Response:

HTTP status code 200
```json
{
    "detail": "string"
}
```

HTTP status code 401
```json
{
    "detail": "string"
}
```


## /api/password/request-reset

Supported methods: POST

Sends a password reset email to the user with the given email address. If the user is not found, the request is ignored and 200 OK response is still returned.

Request:
```json
{
    "email": "string"
}
```

Response:

HTTP status code 200
```json
{}
```

## /api/password/reset

Supported methods: POST

Resets the password for the user with the given email address and password reset code.

Request:
```json
{
    "email": "string",
    "set_password_token": "string",
    "password": "string"
}
```

Response:

HTTP status code 200
```json
{}
```

HTTP status code 400
```json
{
    "error": "object"
}
```
