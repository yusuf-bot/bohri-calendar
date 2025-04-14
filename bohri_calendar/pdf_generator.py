import asyncio
import os
from playwright.async_api import async_playwright
import calendar
import datetime
from calendar_converter import CustomCalendar
from PIL import Image
import io
import time
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape

event={}
GREGORIAN_MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 
                   'July', 'August', 'September', 'October', 'November', 'December']
CUSTOM_MONTHS = [
    "Muharram",
    "Safar",
    "Rabi al-Awwal",
    "Rabi al-Thani",
    "Jumada al-Awwal",
    "Jumada al-Thani",
    "Rajab",
    "Sha'ban",
    "Ramadan",
    "Shawwal",
    "Dhu al-Qadah",
    "Dhu al-Hijjah"
]




async def generate_calendar_html(year, month, gregorian_events, custom_cal, is_gregorian=True):
    """Generate HTML for a specific month"""
    if is_gregorian:
        cal = calendar.monthcalendar(year, month)
        first_day = datetime.date(year, month, 1)
        main_month_name = GREGORIAN_MONTHS[month-1]
        islamic_year, islamic_month, _ = custom_cal.convert_to_custom_calendar(first_day)
        secondary_month_name = islamic_month if isinstance(islamic_month, str) else CUSTOM_MONTHS[islamic_month-1]
        display_year = year
    else:
        # For Hijri calendar
        month_name = CUSTOM_MONTHS[month-1]
    
        # Get month days before generating calendar
        month_days = custom_cal.get_month_days(month_name, year)
        cal = custom_cal.get_month_calendar(year, month)  # Fix: month-1 as index
        first_day = custom_cal.convert_to_gregorian(year, month_name, 1)
        main_month_name = month_name
        secondary_month_name = GREGORIAN_MONTHS[first_day.month-1]
        display_year = year

    complete_html = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{main_month_name} {display_year} Calendar</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #F5F5F9;
                margin: 0;
                padding: 0;
                width: 100vw;
                height: 100vh;
                overflow: hidden;
            }}
            
            .calendar-container {{
                width: 100%;
                height: 100%;
                margin: 0 auto;
                padding: 1.04vw; /* 40px / 38.4 = 1.04vw */
                box-sizing: border-box;
                background-color: #F5F5F9;
            }}
            
            .calendar-header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 0.78vw; /* 30px / 38.4 = 0.78vw */
                width: 100%;
            }}
            
            .month-year {{
                font-size: 2.5vw; /* 96px / 38.4 = 2.5vw */
                font-weight: bold;
                text-align: center;
                flex: 1;
                margin: 0;
            }}
            
            .year, .islamic-month {{
                font-size: 1.88vw; /* 72px / 38.4 = 1.88vw */
                font-weight: bold;
                margin: 0;
            }}
            
            .days-header {{
                display: grid;
                grid-template-columns: repeat(7, 1fr);
                gap: 0.21vw; /* 8px / 38.4 = 0.21vw */
                margin-bottom: 0.21vw; /* 8px / 38.4 = 0.21vw */
            }}
            
            .day-name {{
                background-color: #000;
                color: white;
                text-align: center;
                padding: 0.52vw; /* 20px / 38.4 = 0.52vw */
                border-radius: 0.52vw; /* 20px / 38.4 = 0.52vw */
                font-weight: bold;
                font-size: 1.09vw; /* 42px / 38.4 = 1.09vw */
            }}
            
            .calendar-grid {{
                display: grid;
                grid-template-columns: repeat(7, 1fr);
                gap: 0.21vw; /* 8px / 38.4 = 0.21vw */
                height: 80vh; /* Added fixed height to ensure consistent layout */
            }}
            
            .calendar-day {{
                background-color: white;
                min-height: 8.33vh; /* 320px / 38.4 = 8.33vw, but using vh for height */
                border-radius: 0.13vw; /* 5px / 38.4 = 0.13vw */
                padding: 0.39vw; /* 15px / 38.4 = 0.39vw */
                position: relative;
                display: flex;
                flex-direction: column;
            }}
            
            .date-number {{
                display: flex;
                justify-content: space-between;
            }}
            
            .gregorian {{
                font-size: 1.56vw; /* 60px / 38.4 = 1.56vw */
                font-weight: bold;
            }}
            
            .hijri {{
                font-size: 1.3vw; /* 50px / 38.4 = 1.3vw */
                font-weight: bold;
                color: #666666;
            }}
            
            .event {{
                background-color: #FFE4E1;
                color: #000;
                padding: 0.31vw 0.63vw; /* 12px / 38.4 = 0.31vw, 24px / 38.4 = 0.63vw */
                border-radius: 0.39vw; /* 15px / 38.4 = 0.39vw */
                text-align: center;
                font-size: 0.83vw; /* 32px / 38.4 = 0.83vw */
                margin-top: 0.26vw; /* 10px / 38.4 = 0.26vw */
            }}
        </style>
    </head>
    <body>
        <div class="calendar-container">
            <div class="calendar-header">
                <div class="year">{display_year}</div>
                <div class="month-year">{main_month_name}</div>
                <div class="islamic-month">{secondary_month_name}</div>
            </div>
            
            <div class="days-header">
                <div class="day-name">MON</div>
                <div class="day-name">TUE</div>
                <div class="day-name">WED</div>
                <div class="day-name">THU</div>
                <div class="day-name">FRI</div>
                <div class="day-name">SAT</div>
                <div class="day-name">SUN</div>
            </div>
            
            <div class="calendar-grid">
    '''
    Thursday = False
    # Generate calendar days
    for week in cal:
        for day in week:
            if day != 0:
                if is_gregorian:
                    current_date = datetime.date(year, month, day)
                    islamic_year, islamic_month, islamic_day = custom_cal.convert_to_custom_calendar(current_date)
                    main_day = day
                    secondary_day = islamic_day
                else:
                    # For Hijri calendar - validate day is within month's range
                    month_name = CUSTOM_MONTHS[month-1]
                    month_days = custom_cal.get_month_days(month_name, year)
                    
                    # Skip days that exceed the month's length
                    if day > month_days:
                        continue
                        
                    current_date = custom_cal.convert_to_gregorian(year, month_name, day)
                    main_day = day
                    secondary_day = current_date.day
                
                # Get events based on the date system
                day_events = []
                
                if is_gregorian:
                    # Check for Gregorian events (with @ prefix)
                    greg_key = f"@{day}-{month}"
                    if greg_key in gregorian_events:
                        day_events.extend(gregorian_events[greg_key])
                    
                    # Check for Islamic events using converted date
                    islamic_key = f"{islamic_day}-{CUSTOM_MONTHS.index(islamic_month)+1}"
                    if islamic_key in gregorian_events and not islamic_key.startswith('@'):
                        day_events.extend(gregorian_events[islamic_key])
                    if islamic_day == 1:
                        day_events.extend([f"New {islamic_month} month"])
                            
                else:
                    # For Hijri calendar
                    hijri_key = f"{day}-{month}"
                    if hijri_key in gregorian_events and not hijri_key.startswith('@'):
                        day_events.extend(gregorian_events[hijri_key])
                    if day>=23 and day<30 and month==9:
                        if Thursday:
                            day_events.extend(["Nabi Na Naam"])
                        elif current_date.weekday()==3:
                            Thursday = True
                            day_events.extend(["Nabi Na Naam"])
                            
                    # Check for Gregorian events on this date
                    greg_key = f"@{current_date.day}-{current_date.month}"
                    if greg_key in gregorian_events:
                        day_events.extend(gregorian_events[greg_key])
                    if current_date.day == 1:
                        day_events.extend([f"New {GREGORIAN_MONTHS[current_date.month-1]} month"])

                events_html = ""
                for event in day_events:
                    if event:
                        event_color="#dcebff"
                        events_html += f'<div class="event" style="background-color:{event_color}">{event}</div>'

                complete_html += f'''
                <div class="calendar-day">
                    <div class="date-number">
                        <span class="gregorian">{main_day}</span>
                        <span class="hijri">{secondary_day}</span>
                    </div>
                    {events_html}
                </div>
                '''
            else:
                complete_html += '''
                <div class="calendar-day">
                    <div class="date-number">
                        <span class="gregorian"></span>
                        <span class="hijri"></span>
                    </div>
                </div>
                '''

    complete_html += '''
            </div>
        </div>
    </body>
    </html>
    '''

    return complete_html
async def generate_calendar_images(year, is_gregorian=True, quality="medium"):
    """Generate calendar images for all months and combine into PDF
    
    Args:
        year: The year to generate the calendar for
        is_gregorian: Whether to generate a Gregorian (True) or Hijri (False) calendar
        quality: The quality of the output - low, medium, or high
    """
    custom_cal = CustomCalendar()
    image_paths = []
    start = time.time()
    
    # Set resolution based on quality
    if quality == "low":
        viewport_width = 1920
        viewport_height = 1080
        scale_factor = 1
    elif quality == "medium":
        viewport_width = 2560
        viewport_height = 1440
        scale_factor = 1
    else:  # high quality (4K)
        viewport_width = 3840
        viewport_height = 2160
        scale_factor = 1
    
    # Create a downloads directory if it doesn't exist
    downloads_dir = os.path.join(os.getcwd(), "downloads")
    os.makedirs(downloads_dir, exist_ok=True)
    
    # Add retry mechanism
    max_retries = 3
    retry_count = 0
    
    # ... rest of the function remains the same ...
    
    while retry_count < max_retries:
        try:
            # Launch browser with more resilient settings
            async with async_playwright() as p:
                browser = await p.chromium.launch()
                context = await browser.new_context(
                    viewport={'width': viewport_width, 'height': viewport_height},
                    device_scale_factor=scale_factor
                )
                
                # Create a persistent context
                context = await browser.new_context(
                    viewport={'width': viewport_width, 'height': viewport_height},
                    device_scale_factor=scale_factor
                )
                
                # Process each month
                for month in range(1, 13):
                    month_retry = 0
                    while month_retry < 3:  # Retry each month up to 3 times
                        try:
                            month_name = GREGORIAN_MONTHS[month-1] if is_gregorian else CUSTOM_MONTHS[month-1]
                            print(f"Processing {month_name}")
                            events={}
                            # Generate HTML content
                            html_content = await generate_calendar_html(year, month, events, custom_cal, is_gregorian)
                            
                            # Save HTML to a temporary file for debugging
                            temp_html_path = os.path.join(downloads_dir, f"temp_{month}.html")
                            with open(temp_html_path, "w", encoding="utf-8") as f:
                                f.write(html_content)
                            
                            # Create a new page
                            page = await context.new_page()
                            
                            # Set viewport explicitly to be larger to ensure all content is visible
                            await page.set_viewport_size({"width": viewport_width, "height": viewport_height})
                            
                            # Navigate to the file instead of using setContent
                            file_url = f"file://{temp_html_path.replace(os.sep, '/')}"
                            await page.goto(file_url, wait_until="networkidle")
                            
                            # Wait longer to ensure everything is rendered
                            await page.wait_for_timeout(2000)
                            
                            # Take screenshot of the entire content, not just the viewport
                            calendar_type = 'hijri' if not is_gregorian else 'gregorian'
                            filename = f"calendar_{calendar_type}_{year}_{month:02d}.png"
                            filepath = os.path.join(os.getcwd(), filename)
                            
                            # Take a full page screenshot to ensure we capture everything
                            await page.screenshot(path=filepath, full_page=True)
                            
                            image_paths.append(filepath)
                            print(f"Generated image for {month_name}")
                            
                            # Close the page to free up resources
                            await page.close()
                            try:
                                os.remove(temp_html_path)
                            except:
                                pass
                                
                            break  # Success, exit retry loop
                            
                        except Exception as e:
                            print(f"Error processing month {month}: {str(e)}, attempt {month_retry+1}/3")
                            month_retry += 1
                            await asyncio.sleep(2)  # Wait before retry
                            
                            if month_retry >= 3:
                                print(f"Failed to process month {month} after 3 attempts")
                
                # Close the browser after all months are processed
                await browser.close()
                
                # If we got here without exceptions, break out of the retry loop
                break
                
        except Exception as e:
            print(f"Browser error (attempt {retry_count+1}/{max_retries}): {str(e)}")
            retry_count += 1
            await asyncio.sleep(5)  # Wait 5 seconds before retrying
            
            if retry_count >= max_retries:
                print("Maximum retries reached, giving up")
                raise Exception(f"Failed to generate calendar images after {max_retries} attempts: {str(e)}")
    
    print(f"Image generation time: {time.time()-start:.2f} seconds")
    
    if not image_paths:
        raise Exception("Failed to generate any calendar images")
    
    # Create PDF from images
    pdf_start = time.time()
    create_pdf_from_images(image_paths, year, is_gregorian)
    print(f"PDF creation time: {time.time()-pdf_start:.2f} seconds")
    print(f"Total time: {time.time()-start:.2f} seconds")
    
    calendar_type = 'gregorian' if is_gregorian else 'hijri'
    return f"calendar_{calendar_type}_{year}.pdf"

def create_pdf_from_images(image_paths, year, is_gregorian):
    """Create a PDF from a list of image paths with consistent sizing and proper scaling"""
    calendar_type = 'gregorian' if is_gregorian else 'hijri'
    pdf_filename = f"calendar_{calendar_type}_{year}.pdf"
    
    # First, determine the maximum dimensions needed for all images
    max_width = 0
    max_height = 0
    opened_images = {}
    
    for img_path in image_paths:
        img = Image.open(img_path)
        opened_images[img_path] = img
        width, height = img.size
        max_width = max(max_width, width)
        max_height = max(max_height, height)
    
    # Add margins
    top_margin = 200
    side_margin = 100
    bottom_margin = 100
    
    # Create a PDF with custom page size matching the image dimensions plus margins
    page_width = max_width + (side_margin * 2)
    page_height = max_height + top_margin + bottom_margin
    
    # Create PDF with custom page size
    c = canvas.Canvas(pdf_filename, pagesize=(page_width, page_height))
    
    # Use the specified background color #F5F5F9
    bg_color_rgb = [245/255, 245/255, 249/255]  # Convert hex #F5F5F9 to RGB ratio
    
    for img_path in image_paths:
        img = opened_images[img_path]
        width, height = img.size
        
        # Calculate scaling factor to fit the image properly
        # We want to maintain aspect ratio while ensuring the image fits within the content area
        content_width = page_width - (side_margin * 2)
        content_height = page_height - top_margin - bottom_margin
        
        scale_factor = min(content_width / width, content_height / height)
        
        # Calculate the scaled dimensions
        scaled_width = width * scale_factor
        scaled_height = height * scale_factor
        
        # Fill the page with the background color
        c.setFillColorRGB(bg_color_rgb[0], bg_color_rgb[1], bg_color_rgb[2])
        c.rect(0, 0, page_width, page_height, fill=True, stroke=False)
        
        # Center the image horizontally
        x_position = (page_width - scaled_width) / 2
        
        # Position image with top margin (ReportLab coordinates start from bottom-left)
        y_position = page_height - top_margin - scaled_height
        
        # Add image to PDF with proper scaling and positioning
        c.drawImage(img_path, x_position, y_position, width=scaled_width, height=scaled_height)
        c.showPage()
    
    c.save()
    print(f"Created PDF: {pdf_filename}")
    
    # Close all opened images
    for img in opened_images.values():
        img.close()
    
    # Add a small delay to ensure files are released
    import time
    time.sleep(1)
    
    # Clean up individual image files
    for img_path in image_paths:
        try:
            os.remove(img_path)
        except Exception as e:
            print(f"Warning: Could not remove {img_path}: {e}")
    
    print("Removed individual image files")

if __name__ == "__main__":
    year = 1446 
    # Generate both calendar types
    #asyncio.run(generate_calendar_images(year, True))  # Gregorian calendar
    asyncio.run(generate_calendar_images(year, False))