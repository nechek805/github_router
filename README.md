# GitHub router

## About the project

Small CLI helper for switching between several GitHub accounts on one machine. It updates the `IdentityFile` inside the `Host github.com` block of your OpenSSH config so the next `git` operations over `git@github.com` use the right key.

When you pick a profile whose email differs from the current `git config --global user.email`, it also sets:

- `git config --global user.name`
- `git config --global user.email`

using the `name` and `mail` fields from that profile in `data.json`. If the global email already matches the chosen profile, Git config is left unchanged.

## How to run

1. **Python** 3.10+ (uses `str | None` typing).

2. **Install dependencies** (from the project directory):

   ```bash
   pip install -r requirements.txt
   ```

3. **Environment** — copy or create `.env` next to `main.py`:

   | Variable       | Meaning |
   | -------------- | ------- |
   | `CONFIG_PATH`  | Absolute path to your SSH config file (e.g. `C:\Users\<you>\.ssh\config`). |
   | `DATA_PATH`    | Path to the accounts JSON (e.g. `./data.json` or an absolute path). |

4. **SSH config** must contain a `Host github.com` section with an `IdentityFile` line; the script only edits that line.

5. **Run**:

   ```bash
   python main.py
   ```

   Or use `github_router.bat` if your working directory is the project folder (it runs `python main.py`).

The script lists profiles, marks the one matching the current `IdentityFile`, asks for an `id`, then applies the change.

## Structure of `data.json`

`data.json` is a JSON **array** of account objects. Each object has:

| Field     | Type   | Description |
| --------- | ------ | ----------- |
| `id`      | number | Value you enter in the prompt; must be unique across entries. |
| `mail`    | string | Email used for `git config --global user.email` when this profile is selected and the global email changes. |
| `sshPath` | string | Absolute path to the **private** SSH key file used in `IdentityFile` for `Host github.com`. On Windows use escaped backslashes (`\\`) in JSON. |
| `name`    | string | GitHub username (or any display name) used for `git config --global user.name` together with `mail`. |

Example (replace paths and values with yours):

```json
[
  {
    "id": 1,
    "mail": "you@example.com",
    "sshPath": "C:\\Users\\you\\.ssh\\id_ed25519_work",
    "name": "work-account"
  }
]
```
