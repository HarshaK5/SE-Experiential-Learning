# Reflection

## 1. What is the purpose of static code analysis?

Static analysis examines source code without running it. It gives fast,
repeatable feedback about defects, insecure APIs, maintainability problems,
and style violations. This makes it useful both during development and in
continuous integration, before a defect reaches a user.

## 2. Which tool was most useful and why?

Bandit was the most immediately valuable for this program because it exposed
security risks that would not be obvious from the calculator output alone:
unsafe XML parsing, ECB mode, a weak RSA key, and the CGI handler. Pylint and
Flake8 were also useful because they made the code easier to review and
removed noise from unused names and inconsistent formatting.

## 3. What issue was most important to fix?

The XML parser and encryption implementation were the most important issues.
The calculator handles financial and identity data, so unsafe XML parsing could
enable denial-of-service or entity attacks, while ECB encryption and a
hard-coded key did not provide dependable confidentiality. The rebate and age
boundary bugs were also important because they directly changed tax results.

## 4. What are the limitations of static analysis?

Static tools cannot prove that tax rules are correct or that all business
requirements are satisfied. They also report patterns that require context,
such as whether a CGI handler is reachable. Runtime tests, security review,
dependency checks, and domain validation are still required. In this exercise,
the incorrect rebate and age behavior was found by reading and running the
program rather than relying on a tool warning.

