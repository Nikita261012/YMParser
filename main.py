import asyncio
import csv
import os
import typer
from dotenv import load_dotenv, set_key
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from yandex_music import ClientAsync

ENV_FILE = ".env"
load_dotenv(ENV_FILE)

app = typer.Typer(help="🎵 Export tracks from Yandex Music to a CSV file for importing to another streaming service..")
console = Console()


async def get_yandex_tracks(token: str):
    """Contacts Yandex and downloads liked tracks."""
    client = ClientAsync(token)
    await client.init()
    liked = await client.users_likes_tracks()
    return await liked.fetch_tracks_async()


@app.command(name="config")
def configure():
    """Saving the Yandex token."""
    console.print("[bold purple]🔧 Setting up Yandex Music configuration[/]\n")
    ym_token = typer.prompt("Enter your YANDEX_TOKEN (from the extension)", hide_input=True)

    if not os.path.exists(ENV_FILE):
        with open(ENV_FILE, "w") as f: f.write("")

    set_key(ENV_FILE, "YANDEX_TOKEN", ym_token)
    console.print("\n[bold green]✔ Token successfully saved to .env![/]")


@app.command(name="run")
def run(
        output: str = typer.Option("yandex_tracks.csv", "--output", "-o", help="Output CSV file name"),
        limit: int = typer.Option(0, "--limit", "-l", help="Track limit (0 - download all)")
):
    """Downloads media library and saves as CSV."""
    load_dotenv(ENV_FILE)
    ym_token = os.getenv("YANDEX_TOKEN")

    if not ym_token:
        console.print("[red]❌ Token not found! Please run first:[/] [bold]python main.py config[/]")
        raise typer.Exit(code=1)

    console.print("[bold green]🚀 Connecting to Yandex Music...[/]")
    try:
        tracks = asyncio.run(get_yandex_tracks(ym_token))
    except Exception as e:
        console.print(f"[red]❌ Authorization or connection error with Yandex:[/] {e}")
        raise typer.Exit(code=1)

    # Apply the limit if it is specified
    if limit > 0:
        tracks = tracks[:limit]

    total_tracks = len(tracks)
    console.print(f"[green]✔[/] Successfully received [bold]{total_tracks}[/] tracks. Starting export...\n")

    # Recording in CSV format, which is perfectly understood by all transfer services
    with open(output, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Track Name", "Artist", "Album"])  # Headlines

        with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(bar_width=40),
                TaskProgressColumn(),
                console=console
        ) as progress:
            task = progress.add_task("[cyan]Writing to a file...[/]", total=total_tracks)

            for track in tracks:
                title = track.title if track.title else "Unknown Title"
                artists = ", ".join([a.name for a in track.artists if a.name]) if track.artists else "Unknown Artist"
                album = track.albums[0].title if track.albums else ""

                writer.writerow([title, artists, album])
                progress.advance(task)

    console.print(f"\n[bold green]🎉🎉🎉 Done! The file [yellow]{output}[/Y] has been successfully created.![/]")
    console.print(f"[bold]Number of saved tracks:[/] {total_tracks}")


if __name__ == "__main__":
    app()