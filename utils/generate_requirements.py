import json


def pipfile_lock_to_requirements():
    with open('Pipfile.lock') as f:
        data = json.load(f)

    # Obter dependências padrão
    packages = data.get('default', {})
    dev_packages = data.get('develop', {})

    with open('requirements.txt', 'w') as f:
        for pkg, details in packages.items():
            version = details.get('version', '')
            if version:
                f.write(f"{pkg}{version}\n")
            else:
                f.write(f"{pkg}\n")

        for pkg, details in dev_packages.items():
            version = details.get('version', '')
            if version:
                f.write(f"{pkg}{version}\n")
            else:
                f.write(f"{pkg}\n")


if __name__ == "__main__":
    pipfile_lock_to_requirements()
