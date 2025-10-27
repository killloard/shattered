# Shattered Pixel Extraction — Auto Build Repo (Template)

This repository **automatically builds** your game on GitHub Actions:

- Clones **Shattered Pixel Dungeon (SPD)**
- Applies the **Extraction patch** (difficulty, stash, portals, hardcore death, rarity scaffolding)
- Attempts minimal **code hook insertions**
- Builds a **desktop** distribution with Gradle
- Uploads a downloadable artifact (JAR/zip) to each workflow run
 
## Quick Start

1. Create a **throwaway GitHub account** (for setup) and make a **new repo**.
2. Upload the contents of this zip to that new repo (or "Import repository" / "Upload files").
3. Go to the **Actions** tab — enable workflows if prompted.
4. Push a commit (even editing README is fine). The workflow will run and produce a **downloadable build**.

You can later **transfer** the repo to your main account or organization.

---

## What it does (high level)

- Checks out this repo
- Downloads SPD source (shallow clone)
- Unzips `ShatteredPixelExtraction_patch_v0.1.zip`
- Copies patch files into the SPD **core** module
- Runs `ci/apply_patch.py` to add the required hook calls (best-effort; editable)
- Builds `desktop:dist`
- Uploads the build as an artifact ("SPEX-Desktop-Build")

If SPD’s upstream changes break an insertion, edit `ci/apply_patch.py` where marked.

---

## Legal

This is a **GPL-3.0** derivative of Shattered Pixel Dungeon (Evan Debenham), itself a derivative of Pixel Dungeon (Watabou).  
Keep credits intact. Include license files on any public releases.
