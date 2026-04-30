import typer
from pathlib import Path
from typing import Optional
from typing_extensions import Annotated
from bgremove.api.service import remove_background

app = typer.Typer(help="Production Background Remover CLI")

@app.command()
def main(
    input_path: Path = typer.Argument(..., help="Path to input image or folder"),
    out: Optional[Path] = typer.Option(None, "--out", help="Output file path"),
    quality: str = typer.Option("pro", "--quality", help="Processing level (fast/balanced/pro/max)"),
    background: str = typer.Option("transparent", "--background", help="Background replacement"),
    shadow: str = typer.Option("auto", "--shadow", help="Shadow behavior"),
    batch: bool = typer.Option(False, "--batch", help="Process folder"),
    preview: bool = typer.Option(False, "--preview", help="Save before/after preview"),
    debug: bool = typer.Option(False, "--debug", help="Save debug outputs"),
    report: bool = typer.Option(False, "--report", help="Save report JSON"),
    format: str = typer.Option("png", "--format", help="Output format"),
    device: str = typer.Option("auto", "--device", help="Device to use (auto/cpu/cuda)"),
    force_model: Optional[str] = typer.Option(None, "--force-model", hidden=True, help="Force specific model")
):
    """
    Remove background from an image.
    """
    if not input_path.exists():
        typer.secho(f"Error: Input path {input_path} does not exist.", fg=typer.colors.RED)
        raise typer.Exit(1)
        
    if input_path.is_dir() and not batch:
        typer.secho("Error: Input is a directory. Use --batch to process directories.", fg=typer.colors.RED)
        raise typer.Exit(1)

    if batch:
        typer.secho("Batch mode not fully implemented yet.", fg=typer.colors.YELLOW)
        raise typer.Exit(0)
    
    try:
        result = remove_background(
            image_path=input_path,
            output_path=out,
            quality=quality,
            background=background,
            shadow=shadow,
            preview=preview,
            debug=debug,
            report=report,
            device=device,
            format=format,
            force_model=force_model
        )
        typer.secho(f"Success: Saved to {result.output_path}", fg=typer.colors.GREEN)
    except Exception as e:
        typer.secho(f"Error: {e}", fg=typer.colors.RED)
        raise typer.Exit(1)

if __name__ == "__main__":
    app()
