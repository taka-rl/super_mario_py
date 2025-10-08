from pathlib import Path
import pygame


_CACHE: dict[str, pygame.Surface] = {}


def _key(path: str) -> str:
    # Normalize to avoid duplicate keys from different relative paths
    return str(Path(path).resolve())


def get_image(path: str) -> pygame.Surface:
    """
    Lazy-load and cache one image.
    """
    k = _key(path)
    surf = _CACHE.get(k)
    if surf is not None:
        return surf
    else:
        surf = pygame.image.load(path)
    _CACHE[k] = surf
    return surf


def get_images(paths: tuple[str, ...] | str) -> tuple[pygame.Surface, ...]:
    if isinstance(paths, str):
        # Prevent the "string is iterable of chars" bug
        raise TypeError("get_images() expects a tuple of paths. "
                        "Use get_image() for a single path, or pass ('foo.png',) with a trailing comma.")
    return tuple(get_image(p) for p in paths)


def clear_cache() -> None:
    _CACHE.clear()
