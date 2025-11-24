# **Azure Entra ID – Microsoft Graph Python CLI**

A clean, production-ready Python client and command-line tool for interacting with **Azure Entra ID (Azure AD)** using the **Microsoft Graph API**.

This project uses the **client credentials flow** via MSAL, with all configuration (tenant ID, client ID, client secret, tenant domain) stored in a safe, structured `config.json` file.

Perfect for:

* Automation scripts
* Admin tooling
* User provisioning pipelines
* Dev/Test labs
* Learning Microsoft Graph

---

## 🚀 Features

* Authenticate to Microsoft Graph using an Azure App Registration
* Read configuration from `config.json`
* List Azure AD users
* Search users by display name or email prefix
* Create new users (requires app perms)
* Delete users by ID or UPN
* Clean, extensible helper functions
* Simple CLI interface:

```bash
python graph.py --search bob
python graph.py --list-users 20
python graph.py --create-user --display-name "John" --username john --password "P@ssword!"
python graph.py --delete-user john@tenant.onmicrosoft.com
```

---

## 📂 Project Structure

```
azure-entra-graph-python-cli/
│
├── README.md
├── config.example.json
├── config.json (not committed)
├── requirements.txt
│
├── graph_client.py       # Graph helper library
├── graph.py              # CLI entry point
│
└── docs/
    └── user-crud.md      # CRUD documentation
```

---

## 🔐 Configuration (`config.json`)

Your credentials and settings live in a single JSON file.

### **`config.example.json`**

```json
{
  "tenant_id": "YOUR_TENANT_ID",
  "client_id": "YOUR_CLIENT_ID",
  "client_secret": "YOUR_CLIENT_SECRET",
  "graph_api_url": "https://graph.microsoft.com/v1.0",
  "tenant_domain": "yourtenant.onmicrosoft.com"
}
```

### Steps:

1. Copy the template

   ```bash
   cp config.example.json config.json
   ```
2. Fill in your details
3. **Do NOT commit** `config.json` to Github:

Add to `.gitignore`:

```
config.json
```

---

## 🛠️ Setup & Installation

### 1. Create a virtual environment (recommended)

```bash
python -m venv .venv
source .venv/bin/activate
# Windows: .venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Create your `config.json`

Populate with Azure App Registration credentials.

---

## 🔧 CLI Usage

### **List users**

```bash
python graph.py --list-users
python graph.py --list-users 25
```

### **Search users**

```bash
python graph.py --search bob
```

### **Create a user**

Requires **User.ReadWrite.All** (Application permissions).

```bash
python graph.py --create-user \
  --display-name "John Tester" \
  --username jtester \
  --password "P@ssw0rd123!"
```

UPN created as:

```
jtester@<tenant_domain>
```

Set `tenant_domain` in `config.json`.

### **Delete a user**

```bash
python graph.py --delete-user <object-id-or-upn>
```

---

## 🧠 How It Works

### **Authentication**

Uses MSAL:

```python
app = ConfidentialClientApplication(
    client_id=CLIENT_ID,
    client_credential=CLIENT_SECRET,
    authority="https://login.microsoftonline.com/<tenant>"
)
```

Requests a token:

```python
app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
```

This uses app-level permissions granted in Azure AD.

---

## 🧪 Permissions Required

To support full user CRUD:

| Operation    | Required App Permission |
| ------------ | ----------------------- |
| List users   | `User.Read.All`         |
| Search users | `User.Read.All`         |
| Create users | `User.ReadWrite.All`    |
| Delete users | `User.ReadWrite.All`    |

Make sure you **Grant Admin Consent** in Azure Portal.

---

## 🧩 Extending This Project

Ideas:

* Add groups CRUD
* Manage app roles
* Assign licenses
* Add batch operations
* Add logging and retry logic
* Convert into a Python package (`setup.cfg`)

---

## ❗ Troubleshooting

### **"insufficient privileges"**

You didn’t grant Admin Consent.

### **"Failed to acquire token"**

Check:

* Tenant ID
* Client ID
* Client secret
* App permissions

### **Graph API 401/403 errors**

Ensure:

```json
"graph_api_url": "https://graph.microsoft.com/v1.0"
```

And scope uses `.default`.

---

## 📜 License

MIT — free to use and adapt.
