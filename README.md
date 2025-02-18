# dk

## How this works

Say I have a small program I expect to run more than once, but maybe not that often. For example, `dreamhostify`, a script that adds the `deploy-to-dreamhost` GitHub Actions workflow to a project, so the project automatically deploys to my Dreamhost server when I push to master.

Instead of this:

```
cd path/to/my-project
python3 ~/code/dreamhostify/dreamhostify.py .
```

I want to do this:

```
cd path/to/my-project
dk dreamhostify
```

I also should be able to run `dk list` to see all available commands, along with a short description.

And `dk list dreamhostify` should give a long description.

Each command goes in its own directory. In fact, `list` is just a directory. So is `dreamhostify`.

## Why do this? 

To have a single project that collects useful scripts that I might otherwise forget about.

## How to set up the "dk" command

```sh
sudo cp dk.sh /usr/local/bin/dk
sudo chmod +x /usr/local/bin/dk
```

## Modular Commands

Basic commands like "list" and "new" are part of the dk repo. But other commands can get their own repos.

If you run `dk install gh:dkurth/something`, it will clone the "something" repo into the `user/` directory, where user commands are kept. (You can also run it as `dk install gh:dkurth/something my_something` if you want to give the command a different name.)

That repo could be public or private, which allows personal commands that I don't have to make public. Keeping commands in their own repos means they can be updated without publishing a whole new version of dk. And other people could write their own commands.

Built-in commands live in the `dk/core` directory. All commands the user installs (or creates) go under `dk/user`. This folder is not tracked in git, since the individual commands have their own git repos. Running `dk new dreamhostify` creates a local `dk/user/dreamhostify` directory, which is .gitignored. You write the code, set up a repo for it, and push to GitHub.

## Ideas for improvement

- add a place to put shared code that any module can call
- a module should be able to ask dk (which called it) for things like the path to the user commands directory


## Ideas for commands

### dk print

echo "Hello, printer" | lp -d Brother_MFC_L2700DW_series

I wonder what characters you can print this way. Emoji? Borders? How can I spool a bunch of stuff to the printer? What if I pipe a text file to it? What if I pipe a pdf? And can I limit it to 1 page of output, to avoid accidentally printing 100 pages of binary data?

If I put an "!" in the message, bash tries to interpret it, and it doesn't work.

Maybe include this in dk, like:

dk print "some text here"

---

Idea: assemble a page (like a newspaper, or recent tweets, or whatever) into some text, then pipe that to the printer.

dk tweets --funny --count=10 | dk print

That should print 10 funny tweets. (How does it know which tweets are funny? Hmm, an exercise left to the reader...)

## How autocomplete works

`dk list --quiet` (or `-q`) will print just a list of possible commands, one per line.

Add this to your ~/.zshrc to get tab autocompletion for the dk command:

```sh
# Add dynamic autocomplete to the dk command
_dk_completion() {
    compadd $(dk list --quiet)
}
compdef _dk_completion dk
```