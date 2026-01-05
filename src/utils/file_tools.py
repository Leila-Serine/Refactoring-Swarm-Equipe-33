from pathlib import Path


# Dossier autorisé pour l'écriture
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

    Règles :
    - Pas de chemin absolu
    - Pas de '..'
    - Lecture autorisée uniquement si le fichier existe
    """

    path = Path(file_path)

    if path.is_absolute():
        raise PermissionError("Chemins absolus interdits.")

    if ".." in path.parts:
        raise PermissionError("Remontée de dossier interdite ('..').")

    if not path.exists():
        raise FileNotFoundError(f"Fichier introuvable : {file_path}")

    if not path.is_file():
        raise ValueError("Le chemin fourni n'est pas un fichier.")

    return path.read_text(encoding="utf-8")


def write_file(file_path: str, content: str) -> None:
    """
    Écrit du contenu texte dans un fichier, UNIQUEMENT dans sandbox/.

    Règles ABSOLUES :
    - Écriture autorisée UNIQUEMENT dans sandbox/
    - Chemins absolus interdits
    - '..' interdit
    """

    path = Path(file_path)

    if path.is_absolute():
        raise PermissionError("Chemins absolus interdits.")

    if ".." in path.parts:
        raise PermissionError("Remontée de dossier interdite ('..').")

    full_path = path.resolve()

    if not _is_safe_path(full_path):
        raise PermissionError("Écriture autorisée uniquement dans le dossier sandbox.")

    # Créer les dossiers parents si nécessaires
    full_path.parent.mkdir(parents=True, exist_ok=True)

    full_path.write_text(content, encoding="utf-8")
