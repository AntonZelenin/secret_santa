Contents:
- [/api/register/email](#apiregisteremail)
- [/api/register/email/resend-verification-code](#apiregisteremailresend-verification-code)
- [/api/register/email-verification-code](#apiregisteremail-verification-code)
- [/api/register/password](#apiregisterpassword)
- [/api/register/username](#apiregisterusername)

## /api/register/email

Supported methods: POST

Creates a new user with the given email address, sends an email with a verification code to the user.

Request:
```json
{
    "email": "string",
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
    "email": "string",
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
is correct. Returns a `create_password_token` that should be used to create a password for the user.

Request:
```json
{
    "email": "string",
    "verification_code": "string"
}
```

Response:

HTTP status code 200
```json
{
    "create_password_token": "string"
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

Creates a password for the user with the given `create_password_token`. Returns a `create_username_token` that should be used to create a username for the user.

Request:
```json
{
    "create_password_token": "string",
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