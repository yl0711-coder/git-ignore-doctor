# Git Ignore Doctor

[English](README.md) | [简体中文](README.zh-CN.md)

一个检查 Git 仓库卫生的小工具：哪些文件应该忽略、哪些已经被误提交、应该如何安全移出 Git 索引。

## 为什么做这个

很多人把文件加到 `.gitignore` 后，以为 Git 会自动停止追踪它。实际上不是这样：`.gitignore` 只影响未被追踪的文件。已经提交过的文件，需要明确从 Git 索引里移除。

Git Ignore Doctor 把这个常见问题变成一份清晰的仓库诊断报告。

## 状态

当前版本：`v0.1.0`

第一版有意保持小而稳：

- 不访问网络
- 不需要后台服务
- 不自动清理文件
- 不修改仓库
- 不依赖第三方运行时库

它已经适合做本地仓库检查和 CI 报告，但如果要在大型仓库里作为强制阻断项，建议先观察一段时间，确认没有误报。

## 检查内容

- 已经被 Git 追踪，但当前匹配 ignore 规则的文件
- 高风险已追踪文件，例如 `.env`、私钥、依赖目录、缓存、构建产物、日志
- 高风险未追踪文件，提示是否需要补 `.gitignore`
- 建议补充的 `.gitignore` 条目
- 可人工确认的安全修复命令

工具默认不会修改你的仓库。

## 运行要求

- Python 3.9 或更高版本
- `PATH` 中可以访问 Git
- 当前路径位于一个 Git 工作区内

CLI 使用 Git 自身能力检测 ignored files，不重新实现完整 `.gitignore` 语义。

## 使用

在任意 Git 仓库目录下运行：

```bash
bin/git-ignore-doctor
```

检查其他仓库：

```bash
bin/git-ignore-doctor /path/to/repo
```

JSON 输出：

```bash
bin/git-ignore-doctor --json
```

CI 严格模式：

```bash
bin/git-ignore-doctor --strict
```

如果你的 Python 环境有可用的打包工具，也可以本地安装：

```bash
python -m pip install -e .
git-ignore-doctor --strict
```

GitHub Actions 示例：

```yaml
- name: Check repository hygiene
  run: bin/git-ignore-doctor --strict
```

如果你要自己生成报告，可以使用 JSON 输出：

```bash
bin/git-ignore-doctor --json > git-ignore-report.json
```

退出码：

- `0`：命令执行成功
- `1`：`--strict` 模式下发现问题
- `2`：路径或 Git 错误

## 输出示例

```text
Git Ignore Doctor

Repository: /work/my-app

Tracked files that match ignore rules:
- .DS_Store

Risky tracked files:
- .env [secret] Environment files often contain credentials.
- vendor/autoload.php [dependency] PHP Composer dependencies are usually installed, not committed.

Risky untracked files:
- debug.log [log] Log files should not be committed.

Suggested .gitignore entries:
- .env
- *.log
- /vendor/

Suggested safe commands:
- git rm --cached -- .DS_Store
- git rm --cached -- .env
- git rm --cached -- vendor/autoload.php

Result: failed
```

## 设计说明

Git Ignore Doctor 第一版只输出修复计划，不自动执行修改。`git rm --cached` 这类命令经过确认后是安全的，但它仍然会修改 Git 索引，所以工具默认让使用者自己决定是否执行。

需求调研见 [docs/research.md](docs/research.md)。

## 检测范围

Git Ignore Doctor 当前检查常见仓库卫生风险：

- 环境文件：`.env`、`.env.*`
- 私钥文件：`*.pem`、`*.key`、`id_rsa`、`id_ed25519`
- 系统元数据：`.DS_Store`、`Thumbs.db`
- 依赖目录：`vendor/`、`node_modules/`、`.venv/`、`venv/`
- 缓存目录：`__pycache__/`、`.pytest_cache/`、`.phpunit.cache/`
- 构建产物：`coverage/`、`build/`、`dist/`、`.next/`
- 日志文件：`*.log`

`.env.example` 这类示例文件不会被视为风险文件。

## 非目标

Git Ignore Doctor 不打算做这些事情：

- `.gitignore` 模板生成器
- secret scanner
- 完整安全审计工具
- 自动清理工具
- 替代移除 Git 文件前的人工 code review

## 文档维护约定

以后更新英文 README 时，同一个提交或 PR 里要同步更新 `README.zh-CN.md`。两个 README 应该描述同一组功能、用法和限制。

## 开发

```bash
PYTHONPATH=src python -m unittest discover -s tests
bin/git-ignore-doctor --strict
```

## License

MIT
