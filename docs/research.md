# Demand Research

Git Ignore Doctor is based on a recurring Git problem: developers add files to `.gitignore`, but Git keeps tracking files that were already committed.

## Repeated User Problem

The most common question is: "How do I make Git forget about a file that was tracked, but is now in `.gitignore`?"

Source:

- Stack Overflow: https://stackoverflow.com/questions/1274057/how-do-i-make-git-forget-about-a-file-that-was-tracked-but-is-now-in-gitignore

This is not a niche problem. The discussion has millions of views and many answers because the behavior is unintuitive for new and intermediate Git users.

The second recurring question is how to list ignored files that are already staged or committed.

Source:

- Stack Overflow: https://stackoverflow.com/questions/9320218/how-to-list-files-ignored-by-git-that-are-currently-staged-or-committed

Git itself can expose this information with commands such as:

```bash
git ls-files -ci --exclude-standard
```

But most developers do not remember that command, and it only solves one part of the problem.

## Official Behavior

GitHub documentation explains that `.gitignore` tells Git which files to ignore, but files already checked in must be untracked separately.

Source:

- GitHub Docs: https://docs.github.com/en/get-started/getting-started-with-git/ignoring-files

Git documentation also exposes the underlying primitive used by this tool.

Source:

- Git docs for `git ls-files`: https://git-scm.com/docs/git-ls-files

## Gap

Existing tools and services usually focus on generating `.gitignore` templates. That is useful for new projects, but it does not answer these operational questions:

- Which tracked files already match my ignore rules?
- Which risky files are still tracked even if they are not ignored yet?
- Which untracked files look risky and need a `.gitignore` rule?
- What exact safe commands should I review before removing files from the Git index?

Git Ignore Doctor focuses on diagnosing an existing repository, not generating a generic template.

## First-Version Product Decision

The first version intentionally does not auto-fix anything.

It only reports:

- tracked ignored files
- risky tracked files
- risky untracked files
- suggested `.gitignore` entries
- safe `git rm --cached` commands

This keeps the tool safe enough to run in local development and CI.

