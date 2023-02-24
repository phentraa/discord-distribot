# discord-distribot
A Discord bot - written in Python 3 - who helps colleagues see through all the information they are involved in. 
With collecting relevant messages in one place, they can avoid to fiddle around with different channels.

---


### What does the bot do?
- Read all channels on the Discord server
- When a message tagged by the name of the bot:
  - Collect all other tags (groups, roles as well as persons)
  - Distributes the message via DM for the tagged persons (without duplications)
- As a result I will see all the relevant, up-to-date information for me in the direct message thread with the bot.


Available commands:
```commandline
!help            Shows all commands and their description
!help command    Shows detailed information about the given command

!users           Shows users on the server grouped by their roles
!users role      Shows users from a specific role

!roles           Shows the roles on the server 
```
---

### Requirements

- **.env file**  
  For storing environment variable key-value pairs. (In the same directory as the bot.py)  
  _(You can overwrite the .env-template file)_
  ```text
  # .env
  DISCORD_TOKEN={oauth2-token-of-the-bot}
  DISCORD_GUILD={name-of-the-discord-server}
  ```

- **discord.py**  
  Discord API wrapper
  ```commandline
  pip install -U discord.py
  ```
- **getenv**  
  For reading environment variables
  ```commandline
  pip install -U python-getenv
  ```
  
**For bulk installation you can use the _requirements.txt_ file:**

```commandline
pip install -r requirements.txt
```