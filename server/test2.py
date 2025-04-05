import asyncio
import os
from playwright.async_api import async_playwright
import calendar
import datetime
from custom_calendar import CustomCalendar
from PIL import Image
import io
import time
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape


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


events={
    '1-1':['New Year'],
    '2-1':['Udaipur - Urs Syedi Khanji Fir Saheb (AQ)'],
    '7-1':['Jamnagar - 38th Dai Urs Syedna Ismali Badruddin Ibn Syedi Shk. Adam Saifuddin (RA)'],
    '10-1':['Youme Ashura','Yemen - 1st Dai Urs Syedna Zoeb (RA)'],
    '12-1':['Seyoum - Imam Hussain (SA)'],
    '16-1':['Yemen - 3rd Dai Urs Syedna Hatim Bin Syedna Ibrahim (RA)'],
    '17-1':['Ujjain - 39th Dai Urs Syedna Ibrahim (RA'],
    '23-1':['Denmal - Urs Syedi Hasanfeer Shaheed (AQ)'],
    '27-1':['Taherabad - Urs Syedi Fakhruddin Shaheed (AQ)'],
    '28-1':['Baroda - Urs Syedi Moosanji Taj Saheb (AQ)'],
    
    '1-2':['Yemen - 10th Dai Urs Syedna Ali Bin Hussain (RA)'],
    '3-2':['Yemen - 18th Dai Urs Syedna Ali Shamsuddin Bin (RA)'],
    '4-2':['Burhanpur - 41st Dai Urs Syedna Abdul Taiyeb Zakiuddin (RA)'],
    '14-2':['Khambat - Urs Kaka Akela Kaki Akela'],
    '@20-8':['Birthday - 53rd Dai Syedna Aali Qadr Mufaddal Saifuddin (TUS)'],
    '20-2':['Chelum - Imam Hussain (SA)'],
    '22-2':['Yemen - 8th Dai Urs Syedna Hussain Bin Syedna Ali (RA)'],
    '27-2':['Yemen - 23rd Dai Urs Syedna Mohammed Izzuddin (RA)'],
    '28-2':['Shahadat Imam Hasan (SA)'],

    '2-3':['Ahmedabad - 29th Dai Urs Syedna Abdul Taiyeb Zakiuddin (RA)'],
    '7-3':['Udaipur - Urs Syedi Dawoodi BS','Surat - Urs Syedi Abdeali BS'],
    '10-3':['Surat - 50th Dai Urs Syedna Abdullah Badruddin (RA)'],
    '12-3':['Eid - Milaad Un Nabi (SA)','Yemen - 6th Dai Urs Syedna Ali Bin Hanzala (RA)'],
    '16-3':['Mumbai - 52nd Dai Urs Syedna Mohammed Burhanuddin (RA)'],
    '23-3':['Morbi - Urs Molaya Raj (AQ)','Halwad - Urs Syedi Qazikhan(AQ)'],
    '25-3':['Yemen - 30th Dai Urs Syedna Ali Shamsuddin (RA)'],

    '4-4':['Milad Mubarak Imam Uz Zaman (SA)'],
    '10-4':['Banswara - Urs Syedi Abdul Rasool Shaheed (AQ)'],
    '14-4':['Godhra - Urs Syedi Ismailji Shaheed (AQ)'],
    '16-4':['Ahmedabad - 25th Dai Urs Syedna Jalal Shamsuddin (RA)'],
    '20-4':['Milaad Mubarak - 52nd Dai Syedna Mohammed Burhanuddin (RA)'],
    '22-4':['Jamnagar - 36th Dai Urs Syedna Moosa Kalimuddin (RA)','Bharuch - Urs Syedi Habibullah (AQ)'],
    '27-4':['Ahmedabad - 26th Dai Urs Syedna Dawood Bin Ajab Shah (RA)'],
    '28-4':['Pratapgarh - Urs Syedi Kakaji Saheb (AQ)'],

    '3-5':['Sidhpur - Urs Syedi Qazi Khan (AQ)'],
    '10-5':['Shahadat - Moulatana Fatema Tuz Zahra (SA)'],

    '15-6':['Ahmedabad - 27th Dai Urs Syedna Dawood Bin Qutub Shah (RA)'],
    '18-6':['Surat - 42nd Dai Urs Syedna Yusuf Najmuddin (RA)'],
    '23-6':['Jamnagar - 34th Dai Urs Syedna Ismail Badruddin Ibn Moula Raj (RA)'],
    '27-6':['Ahmedabad - 32nd Dai Urs Syedna Qutub Shah Qutbuddin (RA)'],
    '28-6':['Yemen - 7th Dai Urs Syedna Ahmed Bin Mubarak (RA)'],
    '29-6':['Washeq','Surat - 46th Dai Urs Syedna Mohammed Badruddin (RA) Urs Syedna Qazi Noman (RA)'],

    '4-7':['Mandvi - 37th Dai Urs Syedna Noor Mohammed Nooruddin (RA)','Ujjain - Urs Syedi Hasanji Badshah (AQ)'],
    '7-7':['Ahmedabad - 28th Dai Urs Syedna Shk. Adam Safiyuddin (RA)'],
    '13-7':['Milaad Mubaraak - Moulana Ali (SA)','Ayyam Ul Beez'],
    '14-7':['Yemen -  14th Dai Syedna Abdul Mutalib Najmuddin (RA)','Ayyum Ul Beez'],
    '15-7':['Ayyum Ul Beez'],
    '17-7':['Ayyam Barakaat  Khuldiyah'],
    '18-7':['Ayyam Barakaat  Khuldiyah','Yemen - 13th Dai Urs Syedna Ali Shamsuddin (RA)'],
    '19-7':['Mumbai - 51st Dai Urs Syedna Taher Saifuddin (RA)'],
    '26-7':['Washeq - Lailutul Meraaj','Ujjain - 47th Dai Urs Syedna Abdul Qadir Najmuddin (RA)'],
    '27-7':["Yomoul Al Mab'as"],
    '29-7':['Udaipur - Urs Syedi Luqmanji Mulla Dawood (AQ)'],

    '1-8':['Ujjain - 40th Dai Urs Syedna Hebatullah Moyad Fiddin (RA)'],
    '14-8':['Washeq - Shab E Barat'],
    '15-8':['Yemen - 20th Dai Urs Syedna Hasan Badruddin (RA)'],
    '16-8':['Yemen - 2nd Dai Urs Syedna Ibrahim Bin Hussain Hamadi (RA)'],
    '22-8':['Yemen - Urs Moulatuna Hurratul Malika (RA)'],
    '27-8':['Yemen - 5th Dai Urs Syedna Ali Bin Mohammed (RA)'],

    '@6-3':['Birthday - 52nd Dai Syedna Mohammed Burhanuddin (RA)'],
    '9-9':['Yemen - 16th Dai Urs Syedna Abdullah Fakhruddin (RA)'],
    '18-9':['Washeq'],
    '19-9':['Shahadat Moulana Ali (SA)','Surat - 44th Dai Urs Syedna Mohammed Izzudin (RA)'],
    '20-9':['Washeq'],
    '22-9':['Lailat Ul Qadr'],
    '23-9':['Milaad Mubarak - 53rd Dai Syedna Aali Qadr Muffadal Saifuddin (TUS)'],
    '29-9':['Washeq'],
    '30-9':['Washeq','Takbira'],

    '1-10':['Takbira','Eid Ul Fitr'],
    '5-10':['Burhanpur - Urs Syedi Abdul Qadir Hakimuddin (AQ)'],
    '6-10':['Yemem - 17th Dai Urs Syedna Hasan Badruddin (RA)'],
    '8-10':['Yemen - 15th Dai Urs Syedna abaas Bin Syedna Mohammed (RA)'],
    '9-10':['Ahmedabad - 31st Dai Urs Syedna Qasim Khan Zainuddin (RA)'],
    '10-10':['Yemen - 11th Dai Urs Syedna Ibrahim (RA)','Yemen - 21st Dai Urs Syedna Hussain Husamuddin (RA)'],
    '27-10':['Burhanpur - Urs Syedi Abdul Qadir Hakimuddin (AQ)'],
    '29-10':['Rampura - Urs Syedi Bawa Mulla Khan (AQ)'],

    '9-11':['Ahmedabad - 33rd Dai Urs Syedna Fir Khan Shajauddin (RA)'],
    '12-11':['Jamnagar - 35th Dai Urs Syedna Abdul Taiyeb Zakiuddin (RA)','Surat - 43rd Dai Urs Syedna Abdeali Saifuddin (RA)'],
    '13-11':['Yemen - 9th Dai Urs Syedna Ali Bin Syedna Hussain (RA)'],
    '15-11':['Surat - 45th Dai Urs Syedna Taiyeb Zainuddin (RA)'],
    '19-11':['Yemen - 19th Dai Urs Syedna Idris Imaduddin (RA)'],
    '21-11':['Yemen - 22th Dai Urs Syedna Ali Shamsuddin (RA)'],
    '25-11':['Yemen - 4th Dai Urs Syedna Ali Bin Syedna Hatim (RA)'],
    '27-11':['Milaad Mubarak - 51st Dai Syedna Taher Saifuddin (RA)'],
    '29-11':['Youm Nuzul Qaba'],

    '1-12':['Yemen - 12th Dai Urs Syedna Mohammed Bin Syedna Hatim (RA)'],
    '6-12':['Kapadwanj - Urs Syedi Khoj Bin Malik Shah (AQ)'],
    '9-12':['Washeq - Youm Ul Arafa','Takbira'],
    '10-12':['Eid Ul Adha','Takbira'],
    '11-12':['Takbira'],
    '12-12':['Takbira'],
    '13-12':['Takbira'],
    '16-12':['Yemen - 24th Dai Urs Syedna Yusuf Najmuddin (RA)'],
    '18-12':['Eid E Ghadir E Khum'],
    '27-12':['Surat - 48th Dai Urs Syedna Abdul Hussain Husamuddin (RA)','Surat - 49th Dai Urs Syedna Mohammed Burhanuddin (RA)'],

}

def get_event_color(event_text):
    if "(RA)" in event_text:
        return "#ffefd1"  # Yellow
    elif "(TUS)" in event_text:
        return "#def5e3"  # Green
    elif "(SA)" in event_text:
        return "#ffe4de"  # Red
    else:
        return "#dcebff"



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
        print(month_name)
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
                padding: 20px;
                width: 100%;
                height: 100%;
                overflow: hidden;
            }}
            
            .calendar-container {{
                max-width: 100%;
                margin: 0 auto;
                padding: 20px;
                aspect-ratio: 16/9; /* Fixed aspect ratio */
                width: calc(100% - 40px);
                height: auto;
                box-sizing: border-box;
            }}
            
            .calendar-header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 30px;
                width: 100%;
            }}
            
            .month-year {{
                font-size: 96px;
                font-weight: bold;
                text-align: center;
                flex: 1;
                margin: 0;
            }}
            
            .year, .islamic-month {{
                font-size: 72px;
                font-weight: bold;
                margin: 0;
            }}
            
            .days-header {{
                display: grid;
                grid-template-columns: repeat(7, 1fr);
                gap: 8px;
                margin-bottom: 8px;
            }}
            
            .day-name {{
                background-color: #000;
                color: white;
                text-align: center;
                padding: 20px;
                border-radius: 20px;
                font-weight: bold;
                font-size: 42px;
            }}
            
            .calendar-grid {{
                display: grid;
                grid-template-columns: repeat(7, 1fr);
                gap: 8px;
            }}
            
            .calendar-day {{
                background-color: white;
                min-height: 320px;
                border-radius: 5px;
                padding: 15px;
                position: relative;
            }}
            
            .date-number {{
                display: flex;
                justify-content: space-between;
            }}
            
            .gregorian {{
                font-size: 60px;
                font-weight: bold;
            }}
            
            .hijri {{
                font-size: 50px;
                font-weight: bold;
                color: #666666;
            }}
            
            .event {{
                background-color: #FFE4E1;
                color: #000;
                padding: 12px 24px;
                border-radius: 15px;
                text-align: center;
                font-size: 32px;
                margin-top: 10px;
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
                    if islamic_day>=23 and islamic_day<30 and islamic_month=="Ramadan":
                        if Thursday:
                            day_events.extend(["Nabi Na Naam"])
                        elif current_date.weekday()==3:
                            Thursday = True
                            day_events.extend(["Nabi Na Naam"])
                            
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
                        print(gregorian_events[greg_key])
                        day_events.extend(gregorian_events[greg_key])
                    if current_date.day == 1:
                        day_events.extend([f"New {GREGORIAN_MONTHS[current_date.month-1]} month"])

                events_html = ""
                for event in day_events:
                    if event:
                        event_color=get_event_color(event)  # Only add non-empty events
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
async def generate_calendar_images(year, is_gregorian=True, quality="high"):
    """Generate calendar images for all months and combine into PDF
    
    Args:
        year: The year to generate the calendar for
        is_gregorian: Whether to generate a Gregorian (True) or Hijri (False) calendar
        quality: The quality of the output - always set to "high" (4K) by default
    """
    custom_cal = CustomCalendar()
    image_paths = []
    start = time.time()
    
    # Always use 4K resolution
    viewport_width = 3840
    viewport_height = 2160
    scale_factor = 3
    
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
                # Launch browser with minimal arguments for stability
                browser = await p.chromium.launch(
                    headless=True,
                    timeout=300000,  # 5 minute timeout
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
                            
                            # Generate HTML content
                            html_content = await generate_calendar_html(year, month, events, custom_cal, is_gregorian)
                            
                            # Save HTML to a temporary file for debugging
                            temp_html_path = os.path.join(downloads_dir, f"temp_{month}.html")
                            with open(temp_html_path, "w", encoding="utf-8") as f:
                                f.write(html_content)
                            
                            # Create a new page
                            page = await context.new_page()
                            
                            # Set viewport explicitly
                            await page.set_viewport_size({"width": viewport_width, "height": viewport_height})
                            
                            # Navigate to the file instead of using setContent
                            file_url = f"file://{temp_html_path.replace(os.sep, '/')}"
                            await page.goto(file_url, timeout=60000, wait_until="networkidle")
                            await page.wait_for_timeout(2000)
                            
                            # Take screenshot
                            calendar_type = 'gregorian' if is_gregorian else 'hijri'
                            filename = f"calendar_{calendar_type}_{year}_{month:02d}.png"
                            filepath = os.path.join(os.getcwd(), filename)
                            
                            await page.screenshot(path=filepath, full_page=False)
                            image_paths.append(filename)
                            print(f"Generated image for {month_name} {year}")
                            
                            # Close page and clean up
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
    
    # Add top margin (150 pixels)
    top_margin = 150
    
    # Create a PDF with custom page size matching the image aspect ratio plus top margin
    # For 4K images (3840x2160), maintain the 16:9 aspect ratio
    page_width = max_width
    page_height = max_height + top_margin
    
    # Create PDF with custom page size
    c = canvas.Canvas(pdf_filename, pagesize=(page_width, page_height))
    
    # Use the specified background color #F5F5F9
    bg_color_rgb = [245/255, 245/255, 249/255]  # Convert hex #F5F5F9 to RGB ratio
    
    for img_path in image_paths:
        img = opened_images[img_path]
        width, height = img.size
        
        # Fill the page with the background color
        c.setFillColorRGB(bg_color_rgb[0], bg_color_rgb[1], bg_color_rgb[2])
        c.rect(0, 0, page_width, page_height, fill=True, stroke=False)
        
        # Center the image horizontally
        x_position = (page_width - width) / 2
        
        # Position image with top margin (ReportLab coordinates start from bottom-left)
        y_position = page_height - top_margin - height
        
        # Add image to PDF with proper positioning
        c.drawImage(img_path, x_position, y_position, width=width, height=height)
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