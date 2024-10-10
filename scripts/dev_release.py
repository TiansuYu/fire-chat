import toml
import random
import string


def add_random_dev_suffix(version: str) -> str:
    version = version.split(".dev")[0]
    suffix = "".join(random.choices(string.digits, k=6))
    return f"{version}.dev{suffix}"


def update_version_in_pyproject(file_path: str) -> str:
    with open(file_path, "r") as file:
        data = toml.load(file)

    version = data["project"]["version"]
    new_version = add_random_dev_suffix(version)
    data["project"]["version"] = new_version

    with open(file_path, "w") as file:
        toml.dump(data, file)

    return new_version


if __name__ == "__main__":
    pyproject_path = "pyproject.toml"
    new_version = update_version_in_pyproject(pyproject_path)
    print(f"Updated version in {pyproject_path} to '{new_version}'.")
