import click
import asyncio
from datetime import datetime
from .calendar_converter import CustomCalendar
from .pdf_generator import generate_calendar_images

@click.group()
def main():
    """Bohri Calendar CLI tool"""
    pass

@main.command()
@click.argument('date', type=str)
def convert_gregorian(date):
    """Convert Gregorian date to Bohri date (format: YYYY-MM-DD)"""
    try:
        date_obj = datetime.strptime(date, '%Y-%m-%d').date()
        calendar = CustomCalendar()
        year, month, day = calendar.convert_to_custom_calendar(date_obj)
        click.echo(f"Bohri date: {day} {month} {year}")
    except ValueError as e:
        click.echo(f"Error: {str(e)}", err=True)

@main.command()
@click.argument('year', type=int)
@click.option('--gregorian/--bohri', default=False, help='Calendar type')
def generate_calendar(year, gregorian):
    """Generate calendar PDF for specified year"""
    try:
        asyncio.run(generate_calendar_images(year, is_gregorian=gregorian))
        click.echo(f"Calendar generated successfully for year {year}")
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)

if __name__ == '__main__':
    main()