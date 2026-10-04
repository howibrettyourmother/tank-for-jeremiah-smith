# TANK FOR JEREMIAH SMITH

Live SHADYNASTY tank tracker: https://howibrettyourmother.github.io/tank-for-jeremiah-smith/

Non-playoff rookie picks go by **lowest max PF**. This page pulls the public Sleeper API in your browser (nothing stored, no keys), projects the playoff field from the current standings (6 teams: win %, then points for), and ranks everyone else by max PF. Use `?league=<sleeper league id>` to point it at another league.

Sections: tank leader hero, live pick order, **Tank Race odds for 1.01** (4,000-run Monte Carlo over the remaining regular-season schedule using each team's weekly max-PF average and swing), **Draft Pick Hoarders** (next 3 rookie drafts from traded picks), and **League Shame** (Bench Blunder of the Week with the worst start/sit call, plus the Waiver Regret Wall). League Shame needs Sleeper's big players file, so it only loads when you scroll to it. Finished weeks and player names are cached in sessionStorage for the tab.

Look: broadcast-style night-stadium theme. The two cheer squad photos (`img/cheer-laugh-*.webp`, `img/cheer-swoon-*.webp`, 600w/1024w, soft-faded edges) appear once each: laughing at the tank leader card and swooning over the Wilson Weasels card.

Game link: Morehouse More Problems opens this page in the same tab (`?from=game&back=<game url>`). The pinned BACK TO THE GAME button uses history.back() when it came from the game (so iOS home-screen mode never gets stranded) and falls back to a plain link. Opened directly, it reads PLAY MOREHOUSE MORE PROBLEMS.

Extras: refresh button (auto-refreshes when you come back after 10+ min), share button (`navigator.share`, falls back to copying the link), Sleeper/iMessage link preview (`og.jpg`, 1200x630), and weekly movers (▲/▼ vs last week's tank order; needs last week's best lineups, so it shows once League Shame has loaded on that device, then it's cached per scored week).
