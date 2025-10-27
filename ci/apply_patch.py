
import os, re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1] / "spd"

def patch_file(path, find_pattern, insert_text, after=True):
    p = ROOT / path
    if not p.exists():
        print(f"[WARN] Missing target file: {p}", flush=True)
        return False
    s = p.read_text(encoding="utf-8", errors="ignore")
    if insert_text in s:
        print(f"[OK] Already patched: {path}", flush=True)
        return True
    m = re.search(find_pattern, s, re.MULTILINE|re.DOTALL)
    if not m:
        print(f"[WARN] Pattern not found in {path}", flush=True)
        return False
    idx = m.end() if after else m.start()
    s2 = s[:idx] + insert_text + s[idx:]
    p.write_text(s2, encoding="utf-8")
    print(f"[PATCHED] {path}", flush=True)
    return True

# 1) Initialize extraction config near game start
patch_file(
    "core/src/main/java/com/shatteredpixel/shatteredpixeldungeon/ShatteredPixelDungeon.java",
    r"public class ShatteredPixelDungeon.*?\{",
    '\n    // SPEX: initialize extraction config\n    spextraction.ExtractionConfig.init();\n',
    after=True
)

# 2) Show difficulty select before entering dungeon
# Attempt insert in InterlevelScene (or scene that transitions into a new run)
patch_file(
    "core/src/main/java/com/shatteredpixel/shatteredpixeldungeon/scenes/InterlevelScene.java",
    r"create\(\)\s*\{",
    '\n        // SPEX: show difficulty selection before dungeon load\n        spextraction.ui.DifficultySelectScreen.push(() -> { /* continue load after selection */ });\n',
    after=True
)

# 3) Spawn portals after level generation (Level class or builder)
patch_file(
    "core/src/main/java/com/shatteredpixel/shatteredpixeldungeon/levels/Level.java",
    r"build\(\)\s*\{",
    '\n        // SPEX: maybe spawn an Escape Portal on this level\n        spextraction.ExtractionSystem.maybeSpawnPortal(this);\n',
    after=True
)

# 4) Boss extract enable after boss chest creation
patch_file(
    "core/src/main/java/com/shatteredpixel/shatteredpixeldungeon/actors/mobs/Boss.java",
    r"die\([^\)]*\)\s*\{",
    '\n        // SPEX: enable boss extraction on boss floor\n        spextraction.ExtractionSystem.enableBossExtract(this.level);\n',
    after=True
)

# 5) Hardcore death handling (wipe inventory/equipment)
patch_file(
    "core/src/main/java/com/shatteredpixel/shatteredpixeldungeon/actors/hero/Hero.java",
    r"die\([^\)]*\)\s*\{",
    '\n        // SPEX: hardcore death → wipe inventory\n        spextraction.ExtractionSystem.onHardcoreDeath();\n',
    after=True
)

print("[INFO] Patch script finished.")
