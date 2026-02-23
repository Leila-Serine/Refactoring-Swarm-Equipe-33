from pathlib import Path


# Dossier autorisé
SANDBOX_DIR = Path("sandbox").resolve()


def _is_safe_path(target_path: Path) -> bool:
    """
    Vérifie que le chemin est STRICTEMENT dans le dossier sandbox.
    """
    try:
        target_path = target_path.resolve()
        return SANDBOX_DIR in target_path.parents or target_path == SANDBOX_DIR
    except Exception:
        return False


def read_file(file_path: str) -> str:
    """
    Lit le contenu d'un fichier texte en toute sécurité.
    """

    if not isinstance(file_path, str):
        raise ValueError("file_path must be a string")

    path = Path(file_path)

    if path.is_absolute():
        raise PermissionError("Chemins absolus interdits.")

    if ".." in path.parts:
        raise PermissionError("Remontée de dossier interdite ('..').")

    full_path = path.resolve()

    if not _is_safe_path(full_path):
        raise PermissionError("Lecture autorisée uniquement dans le dossier sandbox.")

    if not full_path.exists():
        raise FileNotFoundError(f"Fichier introuvable : {file_path}")

    if not full_path.is_file():
        raise ValueError("Le chemin fourni n'est pas un fichier.")

    return full_path.read_text(encoding="utf-8")


def write_file(file_path: str, content: str) -> None:
    """
    Écrit du contenu texte dans un fichier, UNIQUEMENT dans sandbox/.
    """

    if not isinstance(file_path, str):
        raise ValueError("file_path must be a string")

    if not isinstance(content, str):
        raise ValueError("content must be a string")

    path = Path(file_path)

    if path.is_absolute():
        raise PermissionError("Chemins absolus interdits.")

    if ".." in path.parts:
        raise PermissionError("Remontée de dossier interdite ('..').")

    full_path = path.resolve()

    if not _is_safe_path(full_path):
        raise PermissionError("Écriture autorisée uniquement dans le dossier sandbox.")

    full_path.parent.mkdir(parents=True, exist_ok=True)
    full_path.write_text(content, encoding="utf-8")


def write_files(files: dict[str, str]) -> None:
    """
    Écrit plusieurs fichiers dans sandbox/.
    """

    if not isinstance(files, dict):
        raise ValueError("files must be a dictionary")

    for path, content in files.items():
        write_file(path, content)
