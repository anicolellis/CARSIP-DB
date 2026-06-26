<h1 align="center">
  &nbsp;CARSIP-DB
</h1>

![License](https://img.shields.io/badge/License-MIT-teal.svg) ![Python](https://img.shields.io/badge/Python-3.14-22558a.svg?logo=python&color=22558a)


## Table of Contents
- [Development](#development)
- [Contribution](#contributing)
- [License](#license)

## Development

CARSIP-DB is designed to be forked and extended. Contributors fork the repository, add features on a branch, and open a pull/merge request back to upstream.

### Prerequisites

- [Python 3.14](https://www.python.org/downloads/)
- [uv](https://docs.astral.sh/uv/) for dependency and environment management
- [git](https://git-scm.com/downloads)

### Setup

1. Fork the repository on [GitHub](https://github.com/CARS-IT/CARSIP-DB/fork) or [GitLab](https://gitlab.com/cars-it/carsip-db/-/forks/new), then clone your fork:

   ```bash
   git clone https://github.com/<your-username>/CARSIP-DB.git
   cd CARSIP-DB
   ```

2. Add the upstream remote so you can pull in changes from the main project:

   ```bash
   git remote add upstream https://github.com/CARS-IT/CARSIP-DB.git
   ```

3. Install the project with development dependencies:

   ```bash
   uv sync
   ```

   This creates a virtual environment in `.venv/` and installs all runtime and dev dependencies (`pytest`, `ruff`, `ty`).

### Development Workflow

1. Sync your fork with upstream before starting new work:

   ```bash
   git checkout main
   git pull upstream main
   git push origin main
   ```

2. Create a feature branch:

   ```bash
   git checkout -b feature/short-description
   ```

3. Make your changes, then run the checks below before pushing.

4. Push your branch to your fork and open a pull/merge request against upstream `main`:

   ```bash
   git push origin feature/short-description
   ```

### Running the Application

```bash
uv run carsip-db
```

### Checks

Run these before opening a pull/merge request:

```bash
uv run pytest
uv run ruff check .
uv run ruff format .
uv run ty check
```

## Contributing
All contributions to the CARSIP-DB project are welcome! Here are some ways you can help:
- Report a bug by opening a [GitHub](https://github.com/CARS-IT/CARSIP-DB/issues) or a [GitLab](https://gitlab.com/cars-it/carsip-db/-/boards) issue.
- Add new features, fix bugs or improve documentation by submitting a [GitHub](https://github.com/CARS-IT/CARSIP-DB/pulls) or a [GitLab](https://gitlab.com/cars-it/carsip-db/-/merge_requests) pull request.

Please adhere to the [GitHub flow](https://docs.github.com/en/get-started/quickstart/github-flow) model when making your contributions! This means creating a new branch for each feature of bug fix, and submitting your changes as a pull request against the main branch. If you're not sure how to contribute, please open an issue and we'll be happy to help you out.

By contributing to the CARSIP-DB project, you agree that your contributions will be licensed under the MIT License.

## License
CARSIP-DB is distributed under the MIT License. You should have received a [copy](LICENSE) of the MIT License along with this program. If not, see https://mit-license.org/ for additional details.