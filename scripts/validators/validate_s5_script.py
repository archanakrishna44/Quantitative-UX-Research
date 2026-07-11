#!/usr/bin/env python3
"""
validate_s5_script.py — AST-walk a Python script for banned inferential patterns
that must not appear in S5 (exploratory) analysis scripts.

Usage:
    python3 validate_s5_script.py <path_to_python_script>

Exit codes:
    0 — No banned patterns found (PASS)
    1 — One or more banned patterns found (FAIL)
"""

import argparse
import ast
import os
import sys


# ---------------------------------------------------------------------------
# Banned function names that are hypothesis tests in scipy.stats
# ---------------------------------------------------------------------------
BANNED_SCIPY_STATS_FUNCS = {
    "ttest_1samp",
    "ttest_ind",
    "ttest_rel",
    "f_oneway",
    "kruskal",
    "mannwhitneyu",
    "wilcoxon",
    "chi2_contingency",
    "fisher_exact",
    "spearmanr",
    "pearsonr",
    "kendalltau",
    "ks_2samp",
    # shapiro, normaltest, anderson are distributional checks on residuals/covariates
    # needed to inform the S6 analysis plan — they are NOT banned at S5.
}

# ---------------------------------------------------------------------------
# Banned pingouin functions
# ---------------------------------------------------------------------------
BANNED_PINGOUIN_FUNCS = {
    "ttest",
    "anova",
    "ancova",
    "rm_anova",
    "mixed_anova",
    "manova",
    "pairwise_tests",
    "mediation_analysis",
    "logistic_regression",
}

# ---------------------------------------------------------------------------
# Banned top-level module imports
# ---------------------------------------------------------------------------
BANNED_TOP_LEVEL_IMPORTS = {"pymc", "bambi", "stan"}

# ---------------------------------------------------------------------------
# Banned module names for dynamic import checks (Gap 2)
# ---------------------------------------------------------------------------
BANNED_DYNAMIC_IMPORT_MODULES = {
    "scipy.stats",
    "statsmodels",
    "pingouin",
    "pymc",
    "bambi",
    "stan",
}

# ---------------------------------------------------------------------------
# Dynamic code execution functions (Gap 1)
# ---------------------------------------------------------------------------
BANNED_EXEC_FUNCS = {"exec", "eval", "compile"}

# ---------------------------------------------------------------------------
# Subprocess / shell execution functions (Gap 4)
# ---------------------------------------------------------------------------
BANNED_SUBPROCESS_FUNCS = {
    "subprocess.run",
    "subprocess.call",
    "subprocess.Popen",
    "subprocess.check_output",
    "subprocess.check_call",
    "os.system",
    "os.popen",
    "os.execv",
    "os.execve",
    "os.spawnl",
    "pty.spawn",
}


class S5Checker(ast.NodeVisitor):
    """
    Walk a Python AST and collect banned inferential patterns.

    Detection strategy
    ------------------
    1.  Track which names are bound to `scipy.stats` or `pingouin` through
        import statements so that aliased calls are caught.
    2.  Detect `scipy.stats.<func>` attribute accesses (both direct and via
        an alias).
    3.  Detect `.fit(` calls on names that were imported from statsmodels.
    4.  Detect `.pvalue` attribute accesses anywhere.
    5.  Detect banned top-level imports (pymc, bambi, stan).
    """

    def __init__(self, source_lines):
        self.source_lines = source_lines
        self.findings = []

        # Maps alias name → canonical module, e.g. {"ss": "scipy.stats"}
        self._scipy_stats_aliases = set()   # names bound to scipy.stats
        self._pingouin_aliases = set()       # names bound to pingouin module
        self._statsmodels_imported = False   # any statsmodels import present
        self._statsmodels_aliases = set()    # variable names bound to statsmodels objects
        # statsmodels.stats.power is ALLOWED — track it to avoid false positives
        self._statsmodels_power_aliases = set()
        # Maps local alias → canonical dotted name for `import mod as alias` (finding #8)
        self._import_alias_map = {}         # e.g. {"x": "os", "sp": "subprocess"}
        # Bare names imported from subprocess/os modules (finding #6)
        self._bare_subprocess_names = set() # e.g. {"system"} from `from os import system`

    # ------------------------------------------------------------------ helpers

    def _flag(self, node, category, detail):
        lineno = getattr(node, "lineno", "?")
        line_text = ""
        if isinstance(lineno, int) and lineno <= len(self.source_lines):
            line_text = self.source_lines[lineno - 1].rstrip()
        self.findings.append(
            {
                "lineno": lineno,
                "category": category,
                "detail": detail,
                "source": line_text,
            }
        )

    def _dotted_name(self, node):
        """Return dotted module name from an ast.Attribute chain, or None."""
        parts = []
        while isinstance(node, ast.Attribute):
            parts.append(node.attr)
            node = node.value
        if isinstance(node, ast.Name):
            parts.append(node.id)
        return ".".join(reversed(parts)) if parts else None

    # ------------------------------------------------------------------ imports

    def visit_Import(self, node):
        for alias in node.names:
            mod = alias.name
            local = alias.asname if alias.asname else mod.split(".")[0]
            # Track all module aliases for dotted-name resolution (finding #8)
            if alias.asname:
                self._import_alias_map[alias.asname] = mod
            if mod in BANNED_TOP_LEVEL_IMPORTS:
                self._flag(
                    node,
                    "banned_import",
                    f"Import of banned module '{mod}'",
                )
            if mod == "scipy.stats":
                self._scipy_stats_aliases.add(local)
            if mod == "pingouin":
                self._pingouin_aliases.add(local)
            if mod.startswith("statsmodels") and "power" not in mod:
                self._statsmodels_imported = True
                self._statsmodels_aliases.add(local)
            if mod.startswith("statsmodels") and "power" in mod:
                self._statsmodels_power_aliases.add(local)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        mod = node.module or ""
        if mod in BANNED_TOP_LEVEL_IMPORTS or mod.split(".")[0] in BANNED_TOP_LEVEL_IMPORTS:
            self._flag(
                node,
                "banned_import",
                f"Import from banned module '{mod}'",
            )

        # `from scipy import stats` or `from scipy.stats import ...`
        if mod == "scipy" or mod == "scipy.stats":
            for alias in node.names:
                # Wildcard import from banned module — reject outright (finding #5)
                if alias.name == "*":
                    self._flag(
                        node,
                        "banned_import",
                        f"Wildcard import 'from {mod} import *' is not permitted — "
                        f"banned inferential functions cannot be tracked through wildcard imports.",
                    )
                    continue
                local = alias.asname if alias.asname else alias.name
                if mod == "scipy" and alias.name == "stats":
                    self._scipy_stats_aliases.add(local)
                elif mod == "scipy.stats":
                    # `from scipy.stats import ttest_ind` — register as direct name
                    if alias.name in BANNED_SCIPY_STATS_FUNCS:
                        self._scipy_stats_aliases.add(f"__direct__{local}")
                    self._scipy_stats_aliases.add(f"__ss_member__{local}__{alias.name}")

        if mod == "pingouin":
            for alias in node.names:
                local = alias.asname if alias.asname else alias.name
                if alias.name in BANNED_PINGOUIN_FUNCS:
                    self._pingouin_aliases.add(f"__direct__{local}")

        if mod.startswith("statsmodels"):
            if "power" not in mod:
                self._statsmodels_imported = True
                for alias in node.names:
                    local = alias.asname if alias.asname else alias.name
                    self._statsmodels_aliases.add(local)
            else:
                for alias in node.names:
                    local = alias.asname if alias.asname else alias.name
                    self._statsmodels_power_aliases.add(local)

        # Track bare names imported from subprocess/os modules (finding #6)
        # e.g. `from os import system` → flag `system(...)` as a bare call
        _SUBPROCESS_SOURCE_MODULES = {"os", "subprocess", "pty"}
        if mod in _SUBPROCESS_SOURCE_MODULES or mod.split(".")[0] in _SUBPROCESS_SOURCE_MODULES:
            for alias in node.names:
                local = alias.asname if alias.asname else alias.name
                canonical = f"{mod}.{alias.name}"
                if canonical in BANNED_SUBPROCESS_FUNCS:
                    self._bare_subprocess_names.add(local)

        self.generic_visit(node)

    # ------------------------------------------------------------------ calls

    def visit_Call(self, node):
        func = node.func

        # ---- scipy.stats.<banned_func>(...)
        if isinstance(func, ast.Attribute):
            attr_name = func.attr
            value = func.value

            # Direct: scipy.stats.ttest_ind(...)
            if isinstance(value, ast.Attribute) and value.attr == "stats":
                parent = value.value
                if isinstance(parent, ast.Name) and parent.id == "scipy":
                    if attr_name in BANNED_SCIPY_STATS_FUNCS:
                        self._flag(
                            node,
                            "scipy_stats_hypothesis_test",
                            f"Call to scipy.stats.{attr_name}()",
                        )

            # Aliased: ss.ttest_ind(...) where ss = scipy.stats
            if isinstance(value, ast.Name) and value.id in self._scipy_stats_aliases:
                if attr_name in BANNED_SCIPY_STATS_FUNCS:
                    self._flag(
                        node,
                        "scipy_stats_hypothesis_test",
                        f"Call to {value.id}.{attr_name}() "
                        f"('{value.id}' is bound to scipy.stats)",
                    )

            # ---- pingouin aliased: pg.ttest(...)
            if isinstance(value, ast.Name) and value.id in self._pingouin_aliases:
                if attr_name in BANNED_PINGOUIN_FUNCS:
                    self._flag(
                        node,
                        "pingouin_hypothesis_test",
                        f"Call to {value.id}.{attr_name}() "
                        f"('{value.id}' is bound to pingouin)",
                    )

            # ---- statsmodels .fit() — only when receiver is a statsmodels object
            #      (finding #7: don't flag sklearn .fit() just because statsmodels
            #      is imported somewhere in the script)
            if attr_name == "fit":
                caller_name = value.id if isinstance(value, ast.Name) else None
                is_statsmodels_obj = caller_name in self._statsmodels_aliases
                is_power = caller_name in self._statsmodels_power_aliases
                if is_statsmodels_obj and not is_power:
                    self._flag(
                        node,
                        "statsmodels_fit",
                        f"Call to .fit() on statsmodels object '{caller_name}' — "
                        f"model fitting (inferential) is not allowed in S5.",
                    )

        # ---- plain name call: ttest_ind(...) from `from scipy.stats import ttest_ind`
        if isinstance(func, ast.Name):
            fname = func.id
            # Check direct scipy.stats imports
            if f"__direct__{fname}" in self._scipy_stats_aliases:
                self._flag(
                    node,
                    "scipy_stats_hypothesis_test",
                    f"Call to {fname}() (imported directly from scipy.stats)",
                )
            # Check direct pingouin imports
            if f"__direct__{fname}" in self._pingouin_aliases:
                self._flag(
                    node,
                    "pingouin_hypothesis_test",
                    f"Call to {fname}() (imported directly from pingouin)",
                )

        # ---- Gap 1: exec / eval / compile of string literals ----------------
        func_dotted = self._dotted_name(func) if isinstance(func, ast.Attribute) else None
        func_simple = func.id if isinstance(func, ast.Name) else None

        if func_simple in BANNED_EXEC_FUNCS or func_dotted in {
            "runpy.run_source",
            "runpy.run_path",
            "runpy.run_module",
        }:
            self._flag(
                node,
                "dynamic_code_execution",
                "Dynamic code execution via exec/eval/compile is not permitted in "
                "S5 scripts — banned inferential tests may be hidden inside string "
                "arguments.",
            )

        # ---- Gap 2: __import__() and importlib dynamic imports --------------
        if func_simple == "__import__" or func_dotted in {
            "importlib.import_module",
            "importlib.__import__",
        }:
            first_arg = node.args[0] if node.args else None
            if first_arg is not None and isinstance(first_arg, ast.Constant) and isinstance(first_arg.value, str):
                mod_name = first_arg.value
                # Match exact name or a prefix (e.g. "statsmodels.api" starts with "statsmodels")
                banned_hit = any(
                    mod_name == bm or mod_name.startswith(bm + ".")
                    for bm in BANNED_DYNAMIC_IMPORT_MODULES
                )
                if banned_hit:
                    self._flag(
                        node,
                        "dynamic_import_banned_module",
                        f"Dynamic import of banned module '{mod_name}' via "
                        f"{func_simple or func_dotted}().",
                    )
            else:
                # Non-literal argument — cannot verify; flag unconditionally
                self._flag(
                    node,
                    "dynamic_import_unverifiable",
                    "Dynamic import detected — cannot verify banned modules are not "
                    "loaded.",
                )

        # ---- Gap 3: getattr() reflection to access banned functions ---------
        if func_simple == "getattr":
            obj_arg = node.args[0] if len(node.args) >= 1 else None
            attr_arg = node.args[1] if len(node.args) >= 2 else None

            if attr_arg is not None and isinstance(attr_arg, ast.Constant) and isinstance(attr_arg.value, str):
                attr_name = attr_arg.value
                all_banned_funcs = (
                    BANNED_SCIPY_STATS_FUNCS
                    | BANNED_PINGOUIN_FUNCS
                    # statsmodels: any name that could be a model/test
                    # (we flag only when statsmodels is imported)
                )
                if attr_name in all_banned_funcs:
                    self._flag(
                        node,
                        "getattr_reflection_banned_func",
                        f"getattr() reflection used to access banned function "
                        f"'{attr_name}' — inferential test may be invoked via "
                        f"reflection.",
                    )
                elif self._statsmodels_imported:
                    # If statsmodels is in scope and first arg tracks to it, flag
                    obj_name = obj_arg.id if isinstance(obj_arg, ast.Name) else None
                    if obj_name is not None:
                        self._flag(
                            node,
                            "getattr_reflection_statsmodels",
                            f"getattr() reflection on '{obj_name}' with statsmodels "
                            f"imported — cannot verify no inferential method is "
                            f"accessed.",
                        )
            else:
                # Non-literal second argument — check if first arg is a tracked alias
                obj_name = obj_arg.id if isinstance(obj_arg, ast.Name) else None
                if obj_name is not None and (
                    obj_name in self._scipy_stats_aliases
                    or obj_name in self._pingouin_aliases
                    or self._statsmodels_imported
                ):
                    self._flag(
                        node,
                        "getattr_reflection_unverifiable",
                        f"getattr() reflection on tracked stats object '{obj_name}' "
                        f"with a dynamic attribute name — cannot verify no banned "
                        f"function is accessed.",
                    )

        # ---- Gap 4: subprocess / shell execution ----------------------------
        # Resolve the leading alias to its canonical module before checking
        # e.g. `import os as x; x.system(...)` → func_dotted = "x.system"
        # → resolved = "os.system" (finding #8)
        resolved_dotted = func_dotted
        if func_dotted:
            parts = func_dotted.split(".", 1)
            if len(parts) == 2 and parts[0] in self._import_alias_map:
                resolved_dotted = f"{self._import_alias_map[parts[0]]}.{parts[1]}"
        if resolved_dotted in BANNED_SUBPROCESS_FUNCS:
            self._flag(
                node,
                "subprocess_execution",
                "Subprocess/shell execution is not permitted in S5 scripts — "
                "banned inferential code may be executed in a child process.",
            )
        # Bare names imported from os/subprocess (finding #6)
        # e.g. `from os import system; system('cmd')`
        if func_simple in self._bare_subprocess_names:
            self._flag(
                node,
                "subprocess_execution",
                f"Call to bare '{func_simple}()' imported from a subprocess/os module — "
                "shell execution is not permitted in S5 scripts.",
            )

        self.generic_visit(node)

    # ------------------------------------------------------------------ attribute accesses

    def visit_Attribute(self, node):
        # .pvalue anywhere
        if node.attr == "pvalue":
            self._flag(
                node,
                "pvalue_access",
                f"Access to .pvalue attribute — "
                f"p-values must not be computed or referenced in S5.",
            )

        self.generic_visit(node)


def validate(script_path):
    if not os.path.isfile(script_path):
        print(f"ERROR: File not found: {script_path}")
        sys.exit(1)

    with open(script_path, "r", encoding="utf-8") as fh:
        source = fh.read()
        source_lines = source.splitlines()

    try:
        tree = ast.parse(source, filename=script_path)
    except SyntaxError as exc:
        print(f"ERROR: Syntax error in {script_path}:")
        print(f"  {exc}")
        sys.exit(1)

    checker = S5Checker(source_lines)
    checker.visit(tree)

    findings = checker.findings

    print(f"\nS5 script validation: {script_path}")
    print("=" * 60)

    if not findings:
        print("No banned inferential patterns found.")
        print("\nResult: PASS")
    else:
        # Group by category for readability
        print(f"Banned patterns found ({len(findings)} total):\n")
        for f in findings:
            print(f"  Line {f['lineno']:>4}  [{f['category']}]")
            print(f"           {f['detail']}")
            if f["source"]:
                print(f"           Source: {f['source']}")
            print()
        print(f"Result: FAIL — {len(findings)} banned pattern(s) found.")
        print(
            "\nS5 scripts must not contain hypothesis tests, model fitting,\n"
            ".pvalue accesses, or imports of banned inferential libraries.\n"
            "Move any confirmatory analysis to an S7 script."
        )

    print("=" * 60)
    return bool(findings)


def main():
    parser = argparse.ArgumentParser(
        description=(
            "AST-walk a Python script and reject any calls to banned "
            "inferential functions (S5 exploratory scripts only)."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "script_path",
        help="Path to the Python script to validate.",
    )
    args = parser.parse_args()

    failed = validate(args.script_path)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
