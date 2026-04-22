# Project Copy

## GitHub Repository Description

Detect tracked ignored files, risky commits, and missing `.gitignore` rules in existing Git repositories.

## GitHub Topics

- git
- gitignore
- cli
- repository-hygiene
- developer-tooling
- python

## Short English Summary

Git Ignore Doctor is a small CLI for diagnosing Git repository hygiene problems that `.gitignore` alone does not solve. It detects tracked files that already match ignore rules, risky tracked and untracked files, suggests missing `.gitignore` entries, and prints safe `git rm --cached` commands for human review.

## Short Chinese Summary

Git Ignore Doctor 是一个轻量 CLI，用来诊断 `.gitignore` 解决不了的 Git 仓库卫生问题。它可以找出已经被追踪但当前应忽略的文件、常见高风险已追踪和未追踪文件、建议补充的 `.gitignore` 条目，以及可人工确认的 `git rm --cached` 修复命令。

## Resume / LinkedIn Version

Built and open-sourced Git Ignore Doctor, a lightweight CLI for diagnosing repository hygiene issues that `.gitignore` does not fix by itself. The tool detects tracked ignored files, risky committed artifacts such as `.env`, dependency directories, caches, and logs, then generates safe reviewable cleanup commands for local development and CI use.
