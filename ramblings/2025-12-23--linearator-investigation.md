# Linearator Investigation: Repository Confusion & Clarification

**Research Date:** 2025-12-23

## Executive Summary

**CRITICAL FINDING:** The YAML file `projects/linearator--linearator.yaml` contains an INCORRECT repository URL.

* **Incorrect URL in YAML:** `https://github.com/linearator/linearator` (404 - does not exist)
* **Correct Repository:** `https://github.com/AdiKsOnDev/linear-cli`
* **PyPI Package Name:** `linearator` (v1.4.0, last updated 2025-10-03)
* **Project Names:** The same project has TWO names:
  * PyPI: `linearator`
  * GitHub repo: `linear-cli`
  * CLI command: `linear`

## Key Findings

### 1. Repository Identity Confusion

**AdiKsOnDev/linear-cli** and the PyPI package **linearator** are the SAME PROJECT:

* GitHub: `https://github.com/AdiKsOnDev/linear-cli`
* PyPI: `https://pypi.org/project/linearator/`
* AUR source confirms identity: downloads from `https://files.pythonhosted.org/packages/source/l/linearator/linearator-1.4.0.tar.gz`

### 2. Current Statistics (as of 2025-12-23)

**GitHub Repository:** `AdiKsOnDev/linear-cli`

* Stars: 5
* Forks: 0
* Language: Python
* License: MIT
* Open Issues: 2
* Last Commit: Recent (exact date not captured, but repository active)
* Contributors: Primarily AdiKsOnDev (Adil Alizada)

**PyPI Package:** `linearator`

* Current Version: 1.4.0
* Last Release: 2025-10-03 14:44 UTC
* Installation: `pip install linearator`

**AUR Package:** `linear-cli`

* Version: 1.4.0-1
* Maintainer: AdiKsOnDev
* Source: PyPI linearator package

### 3. Alternative "linearcli" Package

There's a DIFFERENT, OLDER package on PyPI:

* **Package:** `linearcli` (NOT linearator)
* **Repository:** `https://github.com/frenchie4111/linearcli`
* **Version:** 1.0.1
* **Last Release:** 2022-01-07 (UNMAINTAINED - 3+ years old)
* **Status:** Abandoned/stale

## Feature Comparison with Other Linear CLI Tools

### Top Linear CLI Tools (2025)

1. **schpet/linear-cli** (TypeScript/Deno)
   * Git-aware workflow integration
   * GitHub PR automation
   * Branch management
   * Strong developer community presence
   * Platform: macOS, Linux

2. **czottmann/linearis** (Swift)
   * macOS-native implementation
   * AppleScript automation support
   * Recent release: 2025.12.11 (v2025.12.03)
   * Platform: macOS only
   * Excellent documentation

3. **AdiKsOnDev/linear-cli** aka **linearator** (Python)
   * Comprehensive CRUD operations
   * Bulk operations support
   * OAuth + API key authentication
   * Cross-platform (Linux, macOS, Windows)
   * AUR support for Arch Linux users

## Recommendation

### For Different Use Cases:

**Best for Python Users & AUR/Arch Users:**

* **Package:** linearator
* **Install:** `pip install linearator` or `paru -S linear-cli`
* **Repo:** `https://github.com/AdiKsOnDev/linear-cli`
* **Pros:** Cross-platform, bulk operations, comprehensive features
* **Cons:** Lower community adoption (5 stars), limited contributors

**Best for Git Workflow Integration:**

* **Package:** schpet/linear-cli
* **Install:** `brew install schpet/tap/linear` or `deno install jsr:@schpet/linear-cli`
* **Pros:** Git-aware, GitHub PR creation, branch automation
* **Cons:** No Windows support

**Best for macOS Native Experience:**

* **Package:** linearis
* **Install:** `brew install czottmann/tap/linearis`
* **Pros:** Swift native, AppleScript support, actively maintained
* **Cons:** macOS only

### Overall Recommendation

**For general CLI use:** If you're on macOS and want native performance → **linearis**

**For git-integrated workflows:** If you need GitHub PR automation → **schpet/linear-cli**

**For Python/cross-platform needs:** If you need Windows support or prefer Python → **linearator**

## Action Items

1. **Update YAML file:** Correct the repository URL in `projects/linearator--linearator.yaml`
2. **Clarify naming:** Document that "linearator" (PyPI) = "linear-cli" (GitHub repo)
3. **Consider adding:** Track the abandoned `linearcli` package separately for historical reference

## Sources

* [GitHub - AdiKsOnDev/linear-cli](https://github.com/AdiKsOnDev/linear-cli)
* [PyPI - linearator](https://pypi.org/project/linearator/)
* [AUR - linear-cli](https://aur.archlinux.org/packages/linear-cli)
* [Libraries.io - linearcli](https://libraries.io/pypi/linearcli)
* [GitHub - schpet/linear-cli](https://github.com/schpet/linear-cli)
* [GitHub - czottmann/linearis](https://github.com/czottmann/linearis)
