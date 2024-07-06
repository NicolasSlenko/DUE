**Discord User Enhancement Bot (DUE) 
**
The Discord User Enhancement (DUE) bot is a sophisticated tool designed to enhance user experience and server management in Discord. This bot provides a variety of moderation and utility features, including banned word filtering, strike management, and customizable message-type restrictions per channel. DUE is ideal for maintaining a safe and organized community by automating moderation tasks.

**Features**
Automated Moderation: Automatically deletes messages containing banned words and manages user strikes.
Customizable Warnings: Admins can set the number of strikes required before a user receives a warning.
Channel Restrictions: Restrict certain types of messages (e.g., images, videos, links) on a per-channel basis.
User Commands: Provides helpful commands for users to interact with the bot, including help commands and greeting responses.
Admin Commands: Extensive admin commands for managing banned words, strikes, and channel message types.


**Tech Stack**
Programming Language: Python

**Libraries:**
discord.py: For creating the Discord bot and handling events and commands.
csv: For reading and writing data to CSV files, which store banned words, strikes, and channel settings.
os: For interacting with the operating system, including environment variables.
random: For generating random values where necessary.
re: For regular expression operations.

**Hosting:** The bot is hosted on a cloud platform with the keep_alive module ensuring continuous operation.
**Environment Variables:** Utilizes environment variables to securely store and access the bot token.

**Getting Started**
To set up the DUE bot on your Discord server, follow these steps:

**Clone the Repository:**

bash
Copy code
git clone https://github.com/yourusername/DUE-Discord-Bot.git
cd DUE-Discord-Bot
Install Dependencies:

bash
Copy code
pip install -r requirements.txt
Set Up Environment Variables:
Create a .env file in the project root and add your Discord bot token:

makefile
Copy code
DUE_TOKEN=your_discord_bot_token
Run the Bot:

bash
Copy code
python main.py
Usage
User Commands
!duehelp: Display a list of available commands.
!hello: The bot greets the user.
!bye: The bot bids farewell to the user.
!strikes <username>: Check the number of strikes for a specified user.


**Admin Commands**
!bwa <word>: Add a word to the banned words list.
!bwr <word>: Remove a word from the banned words list.
!bwc: Clear all banned words.
!bwv: View the banned words list.
!clearallstrikes: Clear all strikes for all users.
!clearstrikes <username>: Clear strikes for a specified user.
!setstrike <number>: Set the number of strikes required before issuing a warning.
!channeladd <message_type>: Allow a specific message type in a channel.
!channelremove <message_type>: Disallow a specific message type in a channel.
!channeldisplay: Display the allowed message types in a channel.


**Contributing**
We welcome contributions to enhance the functionality and performance of the DUE bot. To contribute, follow these steps:

Fork the repository.
Create a new branch for your feature or bug fix.
Commit your changes with descriptive messages.
Push your branch to your forked repository.
Create a pull request to the main repository.
