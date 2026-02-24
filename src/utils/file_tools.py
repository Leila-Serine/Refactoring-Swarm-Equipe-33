from pathlib import Path


def _is_safe_path(base_dir: Path, target_path: Path) -> bool:
    """
    Vérifie que target_path est STRICTEMENT dans base_dir.
    """
    try:
        base_dir = base_dir.resolve()
        target_path = target_path.resolve()
        return base_dir in target_path.parents or target_path == base_dir
    except Exception:
        return False

def read_file(file_path: str) -> str:
    """
    Lecture robuste d’un fichier avec fallback d'encodage.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if not path.is_file():
        raise ValueError("Path is not a file")

    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        # Fallback Windows
        return path.read_text(encoding="utf-16", errors="ignore")


def write_file(file_path: str, content: str) -> None:
    """
    Écriture sécurisée d’un fichier.
    """

    if not isinstance(file_path, str):
        raise ValueError("file_path must be a string")

    if not isinstance(content, str):
        raise ValueError("content must be a string")

    path = Path(file_path)

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")