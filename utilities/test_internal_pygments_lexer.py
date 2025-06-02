#  Copyright (c) 2024. Erbsland DEV. https://erbsland.dev
#  SPDX-License-Identifier: Apache-2.0

"""
This is the internal testing tool for the Pygments lexer that is used for the syntax highlighting of all code
examples in the documentation. It uses the test files from the `tests` directory, to make sure the lexer detects
any errors in a document correctly. The output files aren't used for these tests.
"""
import argparse
import re
from pathlib import Path
import traceback
import sys
from enum import StrEnum
from typing import List, Tuple, Optional

from pygments.token import Error


class TestOutcome(StrEnum):
    PASS = "PASS"
    FAIL = "FAIL"
    READ = "READ"


class WorkingSet:

    RE_CHARACTERS_TO_ESCAPE = re.compile(r"[\\\"\x00-\x1F\x7F-\x9F]")

    def __init__(self) -> None:
        self.re_name: re.Pattern = re.compile(
            rf"^(\d{{4}})-({'|'.join(outcome for outcome in TestOutcome)})-(.*).elcl$"
        )
        self.test_files: List[Path] = []
        self._initialize_paths()
        self._initialize_lexer()

    def _initialize_paths(self) -> None:
        self.doc_path: Path = Path(__file__).parent.parent / "doc" / "_ext"
        if not self.doc_path.is_dir():
            exit(f"Missing `doc` directory: {self.doc_path}")
        self.test_data: Path = Path(__file__).parent.parent / "tests" / "V1_0"
        if not self.test_data.is_dir():
            exit(f"Missing `tests` directory: {self.test_data}")
        sys.path.append(str(self.doc_path))

    def _initialize_lexer(self) -> None:
        from pygments_elcl import ErbslandConfigurationLanguage, InternalError, DocumentError

        self.ErbslandConfigurationLanguage = ErbslandConfigurationLanguage
        self.InternalError = InternalError
        self.DocumentError = DocumentError
        self.lexer: "ErbslandConfigurationLanguage" = self.ErbslandConfigurationLanguage(accept_all_signatures=False)

    def run(self) -> None:
        self.parse_command_line()
        failed_files: List[Path] = self.run_tests()
        if len(self.test_files) == 1:
            self.rerun_failed_tests(self.test_files)
        else:
            self.rerun_failed_tests(failed_files)

    def parse_command_line(self) -> None:
        parser = argparse.ArgumentParser(
            description="This command tests the internal pygments lexer, which is used for the syntax highlighting of "
            "the example files in the documentation."
        )
        parser.add_argument(
            "-t", "--test", required=False, type=Path, metavar="<file or path>", help="Test file or directory."
        )
        args = parser.parse_args()
        if args.test:
            path = args.test
            if path.is_dir():
                self.test_files = sorted(path.glob("*.elcl"))
            elif path.is_file():
                if path.suffix != ".elcl":
                    exit(f"Test file has unexpected suffix: {path.name}")
                self.test_files = [path]
            elif path.is_absolute():
                exit(f"Test file or directory does not exist: {path.as_posix()}")
            else:
                if (new_path := self.test_data / path).is_dir():
                    self.test_files = sorted(new_path.glob("*.elcl"))
                elif (new_path := self.test_data / path).is_file():
                    if new_path.suffix != ".elcl":
                        exit(f"Test file has unexpected suffix: {new_path.name}")
                    self.test_files = [new_path]
                else:
                    exit(f"Test file or directory does not exist: {path.as_posix()}")
        else:
            self.use_all_test_files()
        if not self.test_files:
            exit("No test files found.")

    def use_all_test_files(self) -> None:
        self.test_files = sorted(self.test_data.rglob("*.elcl"))

    def run_tests(self) -> list[Path]:
        failed_files: list[Path] = []

        print(f"Running tests for {len(self.test_files)} files...")
        for path in self.test_files:
            match: Optional[re.Match] = self.re_name.match(path.name)
            if not match:
                exit(f"Test file with unexpected filename: {path}")
            expected_outcome = TestOutcome(match.group(2))
            try:
                for token, text in self.lexer.get_tokens(path.read_text()):
                    if token is Error or token is None or not isinstance(text, str):
                        raise ValueError("Invalid syntax")
                outcome = TestOutcome.PASS
            except Exception:
                outcome = TestOutcome.FAIL
            failed = outcome != expected_outcome

            if failed:
                failed_files.append(path)
                print(f"Test {path.relative_to(self.test_data).as_posix()}")
                print(f"    ERROR: expected {expected_outcome} but got {outcome}.")

        self._print_summary(len(self.test_files), len(failed_files))
        return failed_files

    def _print_summary(self, total_tests: int, failed_tests: int) -> None:
        print(f"{'SUCCESS' if failed_tests == 0 else 'FAILED'} : processed {total_tests} tests, {failed_tests} failed.")

    @staticmethod
    def _escape_char(match: re.Match):
        c = match.group(0)
        if c == "\\":
            return "\\\\"
        if c == '"':
            return '\\"'
        if c == "\n":
            return "\\n"
        if c == "\r":
            return "\\r"
        if c == "\t":
            return "\\t"
        return f"\\u{{{ord(c):x}}}"

    def _escape_token_text(self, text: str) -> str:
        return self.RE_CHARACTERS_TO_ESCAPE.sub(self._escape_char, text)

    def _token_callback(self, pos, token, text, context) -> None:
        print(" ---- Stack: " + ", ".join(context.stack))
        line_start = "ERROR" if token is Error else "     "
        print(f'{line_start} token: {token} text="{self._escape_token_text(text)}"')

    def rerun_failed_tests(self, failed_files: List[Path]) -> None:
        self.lexer.error_tracing_enabled = True
        self.lexer.error_tracing_callback = self._token_callback
        for path in failed_files[:3]:
            match = self.re_name.match(path.name)
            expected_outcome = TestOutcome(match.group(2))
            print(f"Rerun {expected_outcome} test with tracing enabled: {path.relative_to(self.test_data).as_posix()}")
            text = path.read_text()
            try:
                # Read all tokens from the lexer
                tokens = list(self.lexer.get_tokens_unprocessed(text))
                # Find the first error token.
                error: Optional["DocumentError"] = None
                for pos, token, matched_text in tokens:
                    if token is None:
                        error = self.DocumentError(pos, matched_text, "First None token")
                        break
                    if token is Error:
                        error = self.DocumentError(pos, matched_text, "First Error token")
                        break
                # Compare expectations with the outcome.
                if not error and expected_outcome == TestOutcome.PASS:
                    print("    ERROR: unexpected success, parsing failed document a second time.")
                self.print_parsed_values()
                if error:
                    raise error
            except (self.InternalError, self.DocumentError) as e:
                self.print_document_error(e, text)

    def print_parsed_values(self) -> None:
        print("Parsed Values:")
        for value in self.lexer.last_root.all_values():
            path: str = ".".join(value.path)
            print(f"{path}: {value}")

    def print_document_error(self, e: "DocumentError", text: str) -> None:
        if e.message:
            print(f"Error message: {e.message}")
        print("Error location:")
        line_number: int = text.count("\n", 0, e.pos) + 1
        line_start: int = text.rfind("\n", 0, e.pos) + 1
        line_end: int = text.find("\n", e.pos)
        if line_end == -1:
            line_end = len(text)
        line_text: str = text[line_start:line_end]
        column_number: int = e.pos - line_start

        prev_line: Optional[str] = self.get_line(text, line_start, direction="previous")
        next_line: Optional[str] = self.get_line(text, line_end, direction="next")

        if prev_line:
            print(f"{line_number - 1:4}: {prev_line}")
        print(f"{line_number:4}: {line_text}")
        print(" " * (column_number + 6) + "^ here!")
        if next_line:
            print(f"{line_number + 1:4}: {next_line}")
        traceback.print_exc()

    def get_line(self, text: str, position: int, direction: str = "previous") -> Optional[str]:
        if direction == "previous":
            line_start: int = text.rfind("\n", 0, position - 1) + 1
            return text[line_start : position - 1] if position > 0 else None
        elif direction == "next":
            line_start: int = position + 1
            line_end: int = text.find("\n", line_start)
            return text[line_start:line_end] if line_end != -1 else None
        return None


def main() -> None:
    ws = WorkingSet()
    ws.run()


if __name__ == "__main__":
    main()
