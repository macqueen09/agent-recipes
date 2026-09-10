# New recipe template

Copy this entire folder to `recipes/<category>/<id>/`. This template is intentionally excluded from the runnable catalog.

Write the task, expected input, output, prerequisites, exact command, and limitations here. Add a bilingual companion as README.zh-CN.md. Include fixtures and example output after implementing the recipe.

Example command after implementation:

```sh
python main.py --input path/to/input --output path/to/result
```

Document copied source and package reuse. See [contribution instructions](../../CONTRIBUTING.md).

