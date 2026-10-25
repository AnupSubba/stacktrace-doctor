"""Stack trace parser: plain Python, no AI.

Finds the exception chain (top exception first, deepest "Caused by" last) and the frameworks
involved. The deepest cause is usually the real problem, so it drives retrieval and the prompt.
"""

import re

from .models import ExceptionInfo, ParsedTrace

# A fully qualified exception class: lowercase package segments, then a class name ending in
# Exception, Error or Throwable. Nested classes use $ (e.g. Outer$InnerException).
_EXC_CLASS = r"((?:[a-z_$][\w$]*\.)+[A-Z][\w$]*(?:Exception|Error|Throwable))"

# Lines that start an exception: plain, "Caused by:", or "Exception in thread ...".
_LINE = re.compile(rf'^\s*(?:Caused by:\s*|Exception in thread "[^"]*"\s+)?{_EXC_CLASS}(?::\s*(.*))?$')

# Spring MVC often logs handled exceptions as: "... Resolved [org.x.SomeException: message]"
_RESOLVED = re.compile(rf"Resolved \[{_EXC_CLASS}(?::\s*(.*?))?\]\s*$")

FRAMEWORKS = {
    "org.springframework.boot": "Spring Boot",
    "org.springframework.security": "Spring Security",
    "org.springframework.data": "Spring Data",
    "org.springframework": "Spring Framework",
    "org.hibernate": "Hibernate",
    "jakarta.persistence": "JPA",
    "javax.persistence": "JPA",
    "com.zaxxer.hikari": "HikariCP",
    "org.apache.catalina": "Tomcat",
    "com.fasterxml.jackson": "Jackson",
    "org.yaml.snakeyaml": "SnakeYAML",
}

MAX_MESSAGE_CHARS = 500


def parse(text: str) -> ParsedTrace | None:
    """Return the parsed exception chain, or None if the text contains no Java exception."""
    chain: list[ExceptionInfo] = []
    seen: set[tuple[str, str]] = set()

    for line in text.splitlines():
        match = _LINE.match(line) or _RESOLVED.search(line)
        if not match:
            continue
        info = ExceptionInfo(type=match.group(1), message=(match.group(2) or "").strip()[:MAX_MESSAGE_CHARS])
        key = (info.type, info.message)
        if key in seen:  # Spring sometimes prints the same cause twice ("with root cause")
            continue
        seen.add(key)
        chain.append(info)

    if not chain:
        return None

    frameworks: list[str] = []
    for prefix, name in FRAMEWORKS.items():
        if prefix in text and name not in frameworks:
            frameworks.append(name)

    return ParsedTrace(chain=chain, frameworks=frameworks)
