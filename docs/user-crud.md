# **User CRUD with Microsoft Graph (Python)**

This document explains how the sample project performs **Create, Read, Update, and Delete (CRUD)** operations for **Azure Entra ID (Azure Active Directory)** users using the **Microsoft Graph API** and **client credentials authentication**.

The implementation is built in `graph_client.py` and exposed through a CLI tool in `graph.py`.

---

# 🔐 Authentication Overview

This project uses the **Client Credentials Flow** with MSAL.

1. The application loads credentials from `config.json`:

   * `tenant_id`
   * `client_id`
   * `client_secret`
   * `tenant_domain`
2. A confidential client is created:

   ```python
   ConfidentialClientApplication(
       client_id=CLIENT_ID,
       client_credential=CLIENT_SECRET,
       authority=f"https://login.microsoftonline.com/{TENANT_ID}"
   )
   ```
3. The script requests a token using the application permissions granted in Azure:

   ```python
   app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
   ```
4. All Graph API calls include:

   ```
   Authorization: Bearer <access_token>
   ```

> ✔ Application permissions must be granted **admin consent** in your tenant.

---

# 📘 CRUD Operations Overview

Supported out of the box:

✔ **List users**
✔ **Search users**
✔ **Create users**
✔ **Delete users**
✖ Update users (easy to add—shown below)

---

# 📥 Reading Users

## 🔹 List Users

`list_users(top=10)` retrieves the first N users.

**Code:**

```python
users = list_users(top=5)
for u in users:
    print(u["displayName"], u["userPrincipalName"])
```

**Graph API endpoint:**

```
GET /users?$top=5
```

**CLI equivalent:**

```bash
python graph.py --list-users 5
```

---

## 🔹 Search Users

`search_users(query)` finds users with displayName or mail beginning with the given query.

**Code:**

```python
results = search_users("bob")
```

**Graph API endpoint:**

```
GET /users?$filter=startswith(displayName,'bob') or startswith(mail,'bob')
```

**CLI equivalent:**

```bash
python graph.py --search bob
```

---

# ➕ Creating Users

### Requirements:

* App permissions:

  * `User.ReadWrite.All`
* Admin consent granted
* `tenant_domain` defined in `config.json`
  (e.g., `contoso.onmicrosoft.com`)

---

## 🔹 Create User Function

```python
user = create_user(
    display_name="John Tester",
    username="jtester",
    password="P@ssw0rd123!"
)
```

### Graph API Request Body:

```json
{
  "accountEnabled": true,
  "displayName": "John Tester",
  "mailNickname": "jtester",
  "userPrincipalName": "jtester@contoso.onmicrosoft.com",
  "passwordProfile": {
    "forceChangePasswordNextSignIn": true,
    "password": "P@ssw0rd123!"
  }
}
```

### CLI Equivalent:

```bash
python graph.py --create-user \
  --display-name "John Tester" \
  --username jtester \
  --password "P@ssw0rd123!"
```

---

# ❌ Deleting Users

Users may be deleted by **object ID** or **UPN**.

**Code:**

```python
delete_user("00000000-0000-0000-0000-000000000000")
# or
delete_user("jtester@contoso.onmicrosoft.com")
```

**Graph API Endpoint:**

```
DELETE /users/{id-or-upn}
```

**CLI Equivalent:**

```bash
python graph.py --delete-user jtester@contoso.onmicrosoft.com
```

---

# 🛠️ Updating Users (Optional)

This project does not include update operations by default, but they are easy to add.

Example: Update a user’s display name.

### Add to `graph_client.py`:

```python
def graph_patch(endpoint: str, json_body: Dict[str, Any]) -> None:
    url = f"{GRAPH_API_URL}{endpoint}"
    headers = _get_headers()
    response = requests.patch(url, headers=headers, json=json_body)
    response.raise_for_status()
```

### Then add:

```python
def update_user_display_name(user_identifier: str, new_name: str) -> None:
    graph_patch(f"/users/{user_identifier}", {"displayName": new_name})
```

### Graph API:

```
PATCH /users/{id-or-upn}
```

---

# 🧪 Common Errors & Fixes

### ❌ `insufficient privileges to complete the operation`

You forgot to grant **Admin Consent** after adding app permissions.

### ❌ `invalid_client`

* Tenant, Client ID, or Secret incorrect
* Secret expired

### ❌ 401/403 on Graph calls

Check:

* `graph_api_url` is correct (`https://graph.microsoft.com/v1.0`)
* Scope uses `.default`
* App has required application permissions

---

# 📌 Summary

This project provides a clean Python codebase and CLI that demonstrates:

* How to authenticate to Microsoft Graph using client credentials
* How to perform common Azure AD user operations
* How to structure reusable Graph helper functions
* How to implement a flexible CLI for automation

It serves as a strong foundation for:

* Admin automation
* DevOps scripts
* Identity management prototypes
* User provisioning workflows
