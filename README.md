# CTFd Challenge Release Time
> Automate challenges according to the desired time on the CTFd platform.

## Before Install
- Rename/Copy `.env.example` to `.env`
- Rename/Copy `config.json.example` to `config.json`
- Set ACCESS_TOKEN and BASE_URL in `.env`
- Set your own configuration in `config.json`

## Installation
- `docker-compose build`
- `docker-compose --compatibility up -d`

## Notes
- `challenges` key in `config.json` contains challenges id.
- `minimum_score` key in `config.json` is the minimum score that must be achieved on the topmost scoreboard to unlock challenges.

## Credits
- cacadosman