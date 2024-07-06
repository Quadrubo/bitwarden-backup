# Bitwarden Backup

This project allows making periodic backups of your [Bitwarden](https://bitwarden.com/) vault.
Internally it is using the [Bitwarden CLI](https://bitwarden.com/help/cli/).

The Docker image is using [s6-overlay](https://github.com/just-containers/s6-overlay) to allow for the backups being executed on schedule by cron.

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
```

Start the container.

```shell
docker compose up
```
