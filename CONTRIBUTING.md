# Contributing to pycomment

We welcome contributions to pycomment! Here's how you can get started.

## Development Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/podhmo/pycomment.git
    cd pycomment
    ```

2.  **Activate the development environment:**
    This project uses [Hatch](https://hatch.pypa.io/) for environment and project management. The dependencies are defined in `pyproject.toml`.

    To activate the virtual environment with all dependencies installed, run:
    ```bash
    hatch shell
    ```
    If you use `uv`, you can speed up environment creation with:
    ```bash
    uvx hatch shell
    ```

## Running Commands

Once you are inside the `hatch shell`, you can use the following commands defined in `pyproject.toml`:

*   **Run tests:**
    ```bash
    hatch test
    ```
    If you want to test with all python versions:
    ```bash
    hatch test --all
    ```


*   **Format the code:**
    We use `black` for code formatting. To apply formatting, run:
    ```bash
    hatch run format
    ```

*   **Lint the code:**
    We use `flake8` for linting.
    ```bash
    hatch run lint
    ```

*   **Run all CI checks:**
    This command runs tests, formatting checks, and linting, simulating what happens in our CI pipeline.
    ```bash
    hatch run ci
    make ci  # re-generate ./examples 's output
    ```

Thank you for your contributions!
