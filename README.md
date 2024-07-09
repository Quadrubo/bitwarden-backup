# Bitwarden Backup

This project allows making periodic backups of your [Bitwarden](https://bitwarden.com/) vault.
Internally it is using the [Bitwarden CLI](https://bitwarden.com/help/cli/).

The Docker image is using [s6-overlay](https://github.com/just-containers/s6-overlay) to allow for the backups being executed on schedule by cron.

## Usage

Create a file named `docker-compose.yml` with the following content.
Make sure to use an up to date image tag.

Environment variables:

| Variable             | Example                                   | Description                                                                                                                                                                 |
| -------------------- | ----------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| BACKUP_PATH          | /backup                                   | The path to store backups in **inside** the container. Shouldn't change, instead change the volume mapping to access your backups.                                          |
| BW_BINARY            | /usr/local/bin/bw                         | The path to the Bitwarden CLI binary. Shouldn't need to change.                                                                                                             |
| BW_CLIENT_ID         | user.abcdefgh-1234-abcd-1234-abcdefghijkl | Your Bitwarden client id. Retrieve from [https://vault.bitwarden.com](https://vault.bitwarden.com).                                                                         |
| BW_CLIENT_SECRET     | abcdefghijklmnopqrstuvwxyzabcd            | Your Bitwarden client secret. Retrieve from [https://vault.bitwarden.com](https://vault.bitwarden.com).                                                                     |
| BW_MASTER_PASSWORD   | your-extremely-secure-master-password     | Your Bitwarden master password.                                                                                                                                             |
| BW_SERVER            | https://vault.bitwarden.com               | The bitwarden server to use. Replace with your selfhosted server or use the EU server [https://vault.bitwarden.eu](https://vault.bitwarden.eu).                             |
| BACKUP_FORMAT        | encrypted_json                            | The format of the backup. See the [Export command](https://bitwarden.com/help/cli/#export) for more details.                                                                |
| BACKUP_PASSWORD      | your-backup-encryption-password           | The password to encrypt the backup with. Only works if you use `encrypted_json` as your `BACKUP_FORMAT`. If no password is chosen your account encryption key will be used. |
| BACKUP_ORGANIZATIONS | organization_id_1,organization_id_2       | A comma delimted list of organization ids. These will also be backed up.                                                                                                    |
| CRON_SCHEDULE        | 0 1 \* \* \*                              | The cron schedule on which to run the backup. Use [https://crontab.guru/](https://crontab.guru/) for help generating one.                                                   |
| NTFY_SERVER          | https://ntfy.sh                           | The ntfy server to use.                                                                                                                                                     |
| NTFY_TOPIC           | your-ntfy-topic                           | The ntfy topic to use.                                                                                                                                                      |
| NTFY_USERNAME        | your-ntfy-username                        | The ntfy username used to authenticate. Can be left empty if your topic is unprotected.                                                                                     |
| NTFY_PASSWORD        | your-ntfy-password                        | The ntfy password used to authenticate. Can be left empty if your topic is unprotected.                                                                                     |
| TZ                   | Europe/Berlin                             | Your timezone. Needed for the cron job to work correctly. Here is a [List of valid timezones](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones).                |

```yml
services:
  bitwarden-backup:
    image: ghcr.io/quadrubo/bitwarden-backup:v0.1.0
    container_name: bitwarden-backup
    environment:
      # Paths
      - BACKUP_PATH=/backup
      - BW_BINARY=/usr/local/bin/bw
      # Authentication
      - BW_CLIENT_ID=your-client-id
      - BW_CLIENT_SECRET=your-client-secret
      - BW_MASTER_PASSWORD=your-master-password
      # Connection
      - BW_SERVER=https://vault.bitwarden.com
      # Backups
      - BACKUP_FORMAT=encrypted_json
      - BACKUP_PASSWORD=your-backup-encryption-password
      - BACKUP_ORGANIZATIONS=abcdefgh-1234-abcd-1234-abcdefghijkl,12345667-abcd-1234-abcd-123456789012
      # Cron
      - CRON_SCHEDULE=0 1 * * *
      # NTFY
      - NTFY_SERVER=https://ntfy.sh
      - NTFY_TOPIC=your-ntfy-topic
      - NTFY_USERNAME=your-ntfy-username
      - NTFY_PASSWORD=your-ntfy-password
      # Time
      - TZ=Europe/Berlin
    volumes:
      - ./backup:/backup
```

## Development

Get started by cloning the project.

```shell
git clone https://github.com/Quadrubo/bitwarden-backup
```

Navigate to the project folder and install install the dependencies.

```shell
pip install -r requirements.txt
```

There is also a `shell.nix` file available if you are on nixos.

Create the `.env` file.

```shell
cp .env.dev.example .env
```

Fill out the environment variables.
You can find the `BW_CLIENT_ID` and the `BW_CLIENT_SECRET` on [https://vault.bitwarden.com](https://vault.bitwarden.com).

```shell
BW_CLIENT_ID="user.abcdefgh-1234-abcd-1234-abcdefghijkl"
BW_CLIENT_SECRET="abcdefghijklmnopqrstuvwxyzabcd"
BW_MASTER_PASSWORD="your-extremely-secure-master-password"

BACKUP_PASSWORD=password
BACKUP_ORGANIZATIONS=abcdefgh-1234-abcd-1234-abcdefghijkl,12345667-abcd-1234-abcd-123456789012

NTFY_TOPIC=your-ntfy-topic
NTFY_USERNAME=your-ntfy-username
NTFY_PASSWORD=your-ntfy-password
```

Execute the program.

```shell
python src/main.py
```

## Development of Docker image

Follow these steps, if you want to test the docker image locally.

Create the `.env` file.

```shell
cp .env.docker.example .env
```

Fill out the environment variables.
You can find the `BW_CLIENT_ID` and the `BW_CLIENT_SECRET` on [https://vault.bitwarden.com](https://vault.bitwarden.com).

```shell
BW_CLIENT_ID="user.abcdefgh-1234-abcd-1234-abcdefghijkl"
BW_CLIENT_SECRET="abcdefghijklmnopqrstuvwxyzabcd"
BW_MASTER_PASSWORD="your-extremely-secure-master-password"

BACKUP_PASSWORD=password
BACKUP_ORGANIZATIONS=abcdefgh-1234-abcd-1234-abcdefghijkl,12345667-abcd-1234-abcd-123456789012

NTFY_TOPIC=your-ntfy-topic
NTFY_USERNAME=your-ntfy-username
NTFY_PASSWORD=your-ntfy-password
```

Start the container.

```shell
docker compose up
```
