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

sudo cp dk.sh /usr/local/bin/dk
sudo chmod +x /usr/local/bin/dk

Do not try to install it with `pip install .` -- this creates a binary which is not in the right place relative to the directories of command code for things to work.


## Ideas for commands

### dk config

Set user-specific config details.

### dk edit {command}

One thing you can configure is your editor. This should store just a string of text - could be anything. For me it would be "code", but it could be "vim" or "rm" (ha!), or whatever.

Running `dk edit some-command` would cd to the `some-command` directory and run `code .`.

### module design

Basic commands like "list" and "new" are part of the dk repo. But other commands can get their own repos.

If you run `dk install gh:dkurth/something`, it will clone the "something" repo. That repo could be public or private, so this would let me have some personal commands that I don't have to make public. Commands can be updated without publishing a whole new version of dk. And other people could write their own commands.

Maybe `dk new dreamhostify` creates a local dk/dreamhostify directory, you write the code, and then you can run `dk publish dreamhostify` to create a repo. It could prompt you to make it public or private.

I think this will get easier if the built-in commands live in a `dk/core` directory. All commands the user installs (or creates) will go under `dk/commands`. This folder is not tracked in git, since the individual commands will have their own git repos.


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

`dk list --quiet` will print just a list of possible commands, one per line.

Add this to your ~/.zshrc to get tab autocompletion for the dk command:

```sh
# Add dynamic autocomplete to the dk command
_dk_completion() {
    compadd $(dk list --quiet)
}
compdef _dk_completion dk
```