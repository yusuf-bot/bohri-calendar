import asyncio
import os
from playwright.async_api import async_playwright
async def convert_html_to_image(html_content, image_path, width=3840, height=2160):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(
            viewport={'width': width, 'height': height},
            device_scale_factor=2
        )
        
        page = await context.new_page()
        
        additional_style = """
        <style>
            body {
                padding: 40px 10px 0px 10px !important;
            }
            .calendar-container {
                max-width: 3700px !important;
                padding: 20px !important;
                margin: 0 auto !important;
            }
            .month-year { 
                font-size: 96px !important;
                margin: 0 !important;
            }
            .year, .islamic-month { 
                font-size: 72px !important;
                margin: 0 !important;
            }
            .calendar-header {
                margin-bottom: 30px !important;
            }
            .day-name { 
                font-size: 42px !important;
                padding: 20px !important;
            }
            .calendar-grid {
                gap: 8px !important;
            }
            .calendar-day {
                min-height: 320px !important;
                padding: 15px !important;
            }
            .gregorian { 
                font-size: 60px !important;
                font-weight: bold !important;
            }
            .hijri { 
                font-size: 50px !important;
                font-weight: bold !important;
                color: #666666 !important;
            }
            
            .product-feature, .special-offer {
                font-size: 32px !important;
                margin-top: 120px !important;
                padding: 12px 24px !important;
            }
        </style>
        """
        
        # Rest of the code remains the same...
        
        # Insert additional style into HTML content
        modified_html = html_content.replace('</head>', f'{additional_style}</head>')
        
        # Set content and wait for rendering
        await page.set_content(modified_html)
        await page.wait_for_load_state("networkidle")
        await page.wait_for_timeout(1000)  # Increased wait time for better rendering
        
        # Take screenshot in 4K
        await page.screenshot(path=image_path, full_page=True)
        
        # Cleanup
        await browser.close()
        
        print(f"4K image saved to {os.path.abspath(image_path)}")
# HTML content for January 2025 Calendar
html_content = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>January 2025 Calendar</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #F5F5F9;
            margin: 0;
            padding: 20px;
        }
        
        .calendar-container {
            max-width: 1000px;
            margin: 0 auto;
        }
        
        .calendar-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }
        
        .month-year {
            font-size: 32px;
            font-weight: bold;
            text-align: center;
            flex: 1;
        }
        
        .year, .islamic-month {
            font-size: 24px;
            font-weight: bold;
        }
        
        .days-header {
            display: grid;
            grid-template-columns: repeat(7, 1fr);
            gap: 10px;
            margin-bottom: 10px;
        }
        
        .day-name {
            background-color: #000;
            color: white;
            text-align: center;
            padding: 8px;
            border-radius: 20px;
            font-weight: bold;
        }
        
        .calendar-grid {
            display: grid;
            grid-template-columns: repeat(7, 1fr);
            gap: 10px;
        }
        
        .calendar-day {
            background-color: white;
            min-height: 100px;
            border-radius: 5px;
            padding: 10px;
            position: relative;
        }
        
        .date-number {
            display: flex;
            justify-content: space-between;
        }
        
        .gregorian {
            font-size: 30px;
            font-weight: bold;
        }
        .hijri {
            font-size: 16px;
            font-weight: bold;
        }

        .product-feature {
            background-color: #FFE4E1;
            color: #000;
            padding: 5px 10px;
            border-radius: 15px;
            text-align: center;
            font-size: 12px;
            margin-top: 45px;
        }
        
        .special-offer {
            background-color: #FFF8DC;
            color: #000;
            padding: 5px 10px;
            border-radius: 15px;
            text-align: center;
            font-size: 12px;
            margin-top: 45px;
        }
    </style>
</head>
<body>
    <div class="calendar-container">
        <div class="calendar-header">
            <div class="year">2025</div>
            <div class="month-year">January</div>
            <div class="islamic-month">Safar</div>
        </div>
        
        <div class="days-header">
            <div class="day-name">SUN</div>
            <div class="day-name">MON</div>
            <div class="day-name">TUE</div>
            <div class="day-name">WED</div>
            <div class="day-name">THU</div>
            <div class="day-name">FRI</div>
            <div class="day-name">SAT</div>
        </div>
        
        <div class="calendar-grid">
            <!-- Week 1 -->
            <div class="calendar-day">
                <div class="date-number">
                    <span class="gregorian">2</span>
                    <span class="hijri">2</span>
                </div>
            </div>
            <div class="calendar-day">
                <div class="date-number">
                    <span class="gregorian">2</span>
                    <span class="hijri">2</span>
                </div>
            </div>
            <div class="calendar-day">
                <div class="date-number">
                    <span class="gregorian">2</span>
                    <span class="hijri">2</span>
                </div>
            </div>
            <div class="calendar-day">
                <div class="date-number">
                    <span class="gregorian">2</span>
                    <span class="hijri">2</span>
                </div>
            </div>
            <div class="calendar-day">
                <div class="date-number">
                    <span class="gregorian">2</span>
                    <span class="hijri">2</span>
                </div>
            </div>
            <div class="calendar-day">
                <div class="date-number">
                    <span class="gregorian">2</span>
                    <span class="hijri">2</span>
                </div>
            </div>
            <div class="calendar-day">
                <div class="date-number">
                    <span class="gregorian">2</span>
                    <span class="hijri">2</span>
                </div>
            </div>
            
            <!-- Week 2 -->
            <div class="calendar-day">
                <div class="date-number">
                    <span class="gregorian">9</span>
                    <span class="hijri">9</span>
                </div>
                <div class="product-feature">Product Feature</div>
            </div>
            <div class="calendar-day">
                <div class="date-number">
                    <span class="gregorian">9</span>
                    <span class="hijri">9</span>
                </div>
                <div class="product-feature">Product Feature</div>
            </div>
            <div class="calendar-day">
                <div class="date-number">
                    <span class="gregorian">9</span>
                    <span class="hijri">9</span>
                </div>
                <div class="product-feature">Product Feature</div>
            </div>
            <div class="calendar-day">
                <div class="date-number">
                    <span class="gregorian">9</span>
                    <span class="hijri">9</span>
                </div>
                <div class="product-feature">Product Feature</div>
            </div>
            <div class="calendar-day">
                <div class="date-number">
                    <span class="gregorian">9</span>
                    <span class="hijri">9</span>
                </div>
                <div class="product-feature">Product Feature</div>
            </div>
            <div class="calendar-day">
                <div class="date-number">
                    <span class="gregorian">9</span>
                    <span class="hijri">9</span>
                </div>
                <div class="product-feature">Product Feature</div>
            </div>
            <div class="calendar-day">
                <div class="date-number">
                    <span class="gregorian">9</span>
                    <span class="hijri">9</span>
                </div>
                <div class="product-feature">Product Feature</div>
            </div>
            
            <!-- Week 3 -->
            <div class="calendar-day">
                <div class="date-number">
                    <span class="gregorian">16</span>
                    <span class="hijri">16</span>
                </div>
            </div>
            <div class="calendar-day">
                <div class="date-number">
                    <span class="gregorian">16</span>
                    <span class="hijri">16</span>
                </div>
            </div>
            <div class="calendar-day">
                <div class="date-number">
                    <span class="gregorian">16</span>
                    <span class="hijri">16</span>
                </div>
            </div>
            <div class="calendar-day">
                <div class="date-number">
                    <span class="gregorian">16</span>
                    <span class="hijri">16</span>
                </div>
            </div>
            <div class="calendar-day">
                <div class="date-number">
                    <span class="gregorian">16</span>
                    <span class="hijri">16</span>
                </div>
            </div>
            <div class="calendar-day">
                <div class="date-number">
                    <span class="gregorian">16</span>
                    <span class="hijri">16</span>
                </div>
            </div>
            <div class="calendar-day">
                <div class="date-number">
                    <span class="gregorian">16</span>
                    <span class="hijri">16</span>
                </div>
            </div>
            
            <!-- Week 4 -->
            <div class="calendar-day">
                <div class="date-number">
                    <span class="gregorian">23</span>
                    <span class="hijri">23</span>
                </div>
            </div>
            <div class="calendar-day">
                <div class="date-number">
                    <span class="gregorian">23</span>
                    <span class="hijri">23</span>
                </div>
            </div>
            <div class="calendar-day">
                <div class="date-number">
                    <span class="gregorian">23</span>
                    <span class="hijri">23</span>
                </div>
            </div>
            <div class="calendar-day">
                <div class="date-number">
                    <span class="gregorian">23</span>
                    <span class="hijri">23</span>
                </div>
            </div>
            <div class="calendar-day">
                <div class="date-number">
                    <span class="gregorian">23</span>
                    <span class="hijri">23</span>
                </div>
            </div>
            <div class="calendar-day">
                <div class="date-number">
                    <span class="gregorian">23</span>
                    <span class="hijri">23</span>
                </div>
            </div>
            <div class="calendar-day">
                <div class="date-number">
                    <span class="gregorian">23</span>
                    <span class="hijri">23</span>
                </div>
            </div>
            
            <!-- Week 5 -->
            <div class="calendar-day">
                <div class="date-number">
                    <span class="gregorian">30</span>
                    <span class="hijri">30</span>
                </div>
                <div class="special-offer">Special Offer</div>
            </div>
            <div class="calendar-day">
                <div class="date-number">
                    <span class="gregorian">30</span>
                    <span class="hijri">30</span>
                </div>
                <div class="special-offer">Special Offer</div>
            </div>
            <div class="calendar-day">
                <div class="date-number">
                    <span class="gregorian">30</span>
                    <span class="hijri">30</span>
                </div>
                <div class="special-offer">Special Offer</div>
            </div>
            <div class="calendar-day">
                <div class="date-number">
                    <span class="gregorian">30</span>
                    <span class="hijri">30</span>
                </div>
                <div class="special-offer">Special Offer</div>
            </div>
            <div class="calendar-day">
                <div class="date-number">
                    <span class="gregorian">30</span>
                    <span class="hijri">30</span>
                </div>
                <div class="special-offer">Special Offer</div>
            </div>
            <div class="calendar-day">
                <div class="date-number">
                    <span class="gregorian">30</span>
                    <span class="hijri">30</span>
                </div>
                <div class="special-offer">Special Offer</div>
            </div>
            <div class="calendar-day">
                <div class="date-number">
                    <span class="gregorian">30</span>
                    <span class="hijri">30</span>
                </div>
                <div class="special-offer">Special Offer</div>
            </div>
        </div>
    </div>
</body>
</html>
'''

if __name__ == "__main__":
    asyncio.run(convert_html_to_image(html_content, "calendar_2025_january_4k.png"))



