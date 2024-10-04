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