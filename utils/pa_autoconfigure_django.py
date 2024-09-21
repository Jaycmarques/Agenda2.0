# pa_autoconfigure_django.py
import sys
import subprocess


def main(repo_url, python_version, nuke, branch):
    # Exemplo básico do que o script pode fazer
    print(f"Clonando o repositório: {repo_url}")
    subprocess.run(["git", "clone", repo_url])
    # Adicione o restante da lógica do seu script aqui


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Uso: python3.10 pa_autoconfigure_django.py <repo_url> --python=<version> --nuke --branch=<branch>")
        sys.exit(1)

    repo_url = sys.argv[1]
    python_version = sys.argv[2]
    nuke = sys.argv[3]
    branch = sys.argv[4]

    main(repo_url, python_version, nuke, branch)
