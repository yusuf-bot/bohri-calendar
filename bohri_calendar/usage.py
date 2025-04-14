import asyncio
import datetime
from calendar_converter import CustomCalendar
from pdf_generator import generate_calendar_images
async def main():
    # Date conversion
    calendar = CustomCalendar()
    gregorian_date = datetime.date(2023, 1, 1)
    bohri_year, bohri_month, bohri_day = calendar.convert_to_custom_calendar(gregorian_date)
    print(f"Converted date: Year {bohri_year}, {bohri_month} {bohri_day}")

    # Generate calendar PDF
    year = 1445  # Bohri year
    await generate_calendar_images(year, is_gregorian=False)  # Generates Bohri calendar

if __name__ == "__main__":
    asyncio.run(main())