from kirby.instruction.instruction_model import Instruction

TYPER_LOG_INSTRUCTION = Instruction(
    instructions=[
        # ───────────── mandatory rules ─────────────
        "✅ MANDATORY: Replace all ad-hoc `print()` calls with"
        "`typer.echo()` or `typer.secho()` calls so that logging"
        "honors Typer/Click flags.",
        "🔹 Use `typer.secho(..., fg=...)` to add color:"
        "green for success/info (ℹ️), yellow for warnings (⚠️),"
        "red for errors (❌), blue for debug (🐛).",
        "🔹 Prefix messages with a single emoji to indicate level,"
        "then a short descriptive text, e.g.:\n"
        "    • `typer.secho(f'ℹ️ Loading config: {config_path}', fg='green')`\n"
        "    • `typer.secho('⚠️  Missing optional field, "
        "using default', fg='yellow')`\n"
        "    • `typer.secho('❌  Failed to connect to DB',"
        "fg='red', err=True)`",
        "",
        # ───────────── where to log ─────────────
        "📍 At entry and exit of every public command function"
        "(before and after major steps).",
        "📍 Before and after any file I/O, network call, or subprocess invocation.",
        "📍 Inside `except` blocks to surface stack-level context with"
        "`err=True` for stderr.",
        "📍 Around key state changes: configuration load, cache clear,"
        "DB write, test generation, etc.",
        "",
        # ───────────── formatting & style ─────────────
        "🎨 Keep messages concise (one sentence plus context), no stack"
        "traces or raw objects—format data neatly.",
        "🚫 DO NOT leave bare `print()` or commented‐out debug lines"
        "in the final patch.",
        "🚫 DO NOT over-log: one log per logical operation is enough.",
        "",
        # ───────────── examples ─────────────
        "📄 Example – command start:\n"
        "```python\n"
        "@app.command()\n"
        "def build():\n"
        "    typer.secho('🐛 Starting build process…', fg='blue')\n"
        "    …\n"
        "    typer.secho('✅ Build succeeded!', fg='green')\n"
        "```",
        "",
        "📄 Example – warning on failure:\n"
        "```python\n"
        "    try:\n"
        "        do_something()\n"
        "    except Exception as e:\n"
        "        typer.secho(f'⚠️  Something went wrong: {e}', fg='yellow', err=True)\n"
        "        raise\n"
        "```",
    ],
)
