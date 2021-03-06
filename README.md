[![](https://img.shields.io/github/v/release/erickyeagle/notification-roles-bot)](https://github.com/erickyeagle/notification-roles-bot/releases)
[![](https://img.shields.io/github/v/tag/erickyeagle/notification-roles-bot)](https://github.com/erickyeagle/notification-roles-bot/tags)

# Notification Roles Bot
Notification Roles Bot is a Discord bot that simplifies the use of no permission, mentionable roles that a user wants to subscribe to.

## Installation
This is a self-hosted Discord bot. You will need to provide your own hosting. The host environment needs to have the following software packages:

* Latest Notification Roles Bot source code
	* [Download a release package](https://github.com/erickyeagle/notification-roles-bot/releases)
	* Clone the repository via Git

		```
		git clone https://github.com/erickyeagle/notification-roles-bot.git
		```
* [Python 3.5.3+](https://www.python.org/downloads)

## Usage
In order to run this Discord bot, you will need to create a bot application from the Discord developer's portal. The bot's token will be used below.

1. Copy `requirements.txt` and everything in `/src` to the host environment.
2. Export the `NOTIFICATION_ROLES_BOT_TOKEN` environment variable. The method of exporting of this environment variable may depend on the host environment. Refer to the documentation for your host environment for the correct approach to use. One option is to export the environment variable via the command line.

    ```
    export NOTIFICATION_ROLES_BOT_TOKEN=<token>
    ```
3. Install dependencies.

	```
	pip install -r requirements.txt
	```
4. Run Notification Roles Bot.

    ```
    python notification_roles_bot.py
    ```

**Note:** If you are running the bot on [Replit](https://replit.com) with a free account, you will need to keep the bot alive using something like [replit-keep-alive](https://github.com/erickyeagle/replit-keep-alive).

## Bot Commands
These commands must be issued from inside a guild context (ie. not in a private message).

`!nr add <role>`  
Adds a notification role to the guild.

`!nr list`  
Lists all notification roles for the current guild.

`!nr sub[scribe] <role>`  
Subscribes a user to a notification role.

`!nr unsub[scribe] <role>`  
Unsubscribes a user from a notification role.

## Contributing
If you would like to contribute to this project, you can [file an issue](https://github.com/erickyeagle/notification-roles-bot/issues/new) or [submit a pull request](https://github.com/erickyeagle/notification-roles-bot/compare) from a forked repository. If you would like to contribute, but don't have any coding experience, you can ask questions or propose changes over at our [discussions page](https://github.com/erickyeagle/notification-roles-bot/discussions).