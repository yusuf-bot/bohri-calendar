from flask import Flask, request, send_file, jsonify
import calendar
import datetime
import asyncio
import os
import logging
from flask_cors import CORS
from custom_calendar import CustomCalendar
from test2 import generate_calendar_images, CUSTOM_MONTHS, GREGORIAN_MONTHS, events

# Configure logging
logging.basicConfig(level=logging.DEBUG, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, origins="*", allow_headers=["Content-Type", "Authorization"], 
     methods=["GET", "POST", "OPTIONS"])

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # Disable caching
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload

@app.before_request
def log_request_info():
    logger.debug('Request Headers: %s', request.headers)
    logger.debug('Request Method: %s, Path: %s', request.method, request.path)


# Add this new endpoint
@app.route('/api/test', methods=['GET', 'POST'])
def test_endpoint():
    """Simple test endpoint to verify the server is working"""
    return jsonify({"status": "ok", "message": "Server is running correctly"}), 200

@app.route('/api/calendar', methods=['POST'])
def generate_calendar():
    """
    API endpoint to generate a calendar PDF
    """
    try:
        logger.info("Received calendar generation request")
        data = request.get_json()
        if not data:
            logger.error("No JSON data received")
            return jsonify({"error": "No data provided"}), 400
            
        year = data.get('year')
        calendar_type = data.get('calendar_type', 'gregorian')
        quality = data.get('quality', 'medium')
        
        logger.info(f"Processing request for year: {year}, calendar type: {calendar_type}, quality: {quality}")
        
        # Validate input
        if not isinstance(year, int):
            logger.error(f"Invalid year format: {year}")
            return jsonify({"error": "Year must be an integer"}), 400
            
        if calendar_type not in ['gregorian', 'hijri', 'islamic', 'georgian']:
            logger.error(f"Invalid calendar type: {calendar_type}")
            return jsonify({"error": "Calendar type must be 'gregorian', 'georgian', 'hijri', or 'islamic'"}), 400
            
        if quality not in ['low', 'medium', 'high']:
            logger.error(f"Invalid quality: {quality}")
            return jsonify({"error": "Quality must be 'low', 'medium', or 'high'"}), 400
        
        # Map calendar types to boolean flag
        is_gregorian = calendar_type in ['gregorian', 'georgian']
        
        # Generate the calendar images and PDF
        logger.info(f"Starting PDF generation for {year}, is_gregorian={is_gregorian}, quality={quality}")
        try:
            pdf_filename = asyncio.run(generate_calendar_images(year, is_gregorian, quality))
            logger.info(f"PDF generation completed: {pdf_filename}")
        except Exception as e:
            logger.error(f"Error in generate_calendar_images: {str(e)}")
            return jsonify({"error": f"Failed to generate calendar: {str(e)}"}), 500
        
        # Check if file exists
        if not os.path.exists(pdf_filename):
            logger.error(f"PDF file not found: {pdf_filename}")
            return jsonify({"error": "Failed to generate PDF file"}), 500
        
        # Return the PDF as a downloadable file
        try:
            logger.info(f"Sending file: {pdf_filename}")
            return send_file(
                pdf_filename,
                as_attachment=True,
                download_name=pdf_filename,
                mimetype='application/pdf'
            )
        except Exception as e:
            logger.error(f"Error sending file: {str(e)}")
            return jsonify({"error": f"Error sending file: {str(e)}"}), 500
            
    except Exception as e:
        logger.error(f"Error generating calendar: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Simple health check endpoint"""
    return jsonify({"status": "ok"}), 200

# Add a new endpoint for date conversion
@app.route('/api/convert-date', methods=['POST'])
def convert_date():
    """
    API endpoint to convert between Gregorian and Hijri dates
    """
    try:
        data = request.get_json()
        day = data.get('day')
        month = data.get('month')
        year = data.get('year')
        conversion_type = data.get('conversion_type')  # 'hijri-to-greg' or 'greg-to-hijri'
        
        # Validate input
        if not all(isinstance(x, int) for x in [day, month, year]):
            return jsonify({"error": "Day, month, and year must be integers"}), 400
            
        if conversion_type not in ['hijri-to-greg', 'greg-to-hijri']:
            return jsonify({"error": "Conversion type must be 'hijri-to-greg' or 'greg-to-hijri'"}), 400
        
        # Initialize custom calendar
        custom_cal = CustomCalendar()
        
        # Perform conversion
        if conversion_type == 'hijri-to-greg':
            # Convert Hijri to Gregorian
            if month < 1 or month > 12:
                return jsonify({"error": "Month must be between 1 and 12"}), 400
                
            month_name = CUSTOM_MONTHS[month-1]
            month_days = custom_cal.get_month_days(month_name, year)
            
            if day < 1 or day > month_days:
                return jsonify({"error": f"Day must be between 1 and {month_days} for {month_name}"}), 400
                
            gregorian_date = custom_cal.convert_to_gregorian(year, month_name, day)
            result = {
                "original": {
                    "day": day,
                    "month": month,
                    "month_name": month_name,
                    "year": year,
                    "calendar": "Hijri"
                },
                "converted": {
                    "day": gregorian_date.day,
                    "month": gregorian_date.month,
                    "month_name": GREGORIAN_MONTHS[gregorian_date.month-1],
                    "year": gregorian_date.year,
                    "calendar": "Gregorian"
                }
            }
            
            # Check for events
            hijri_key = f"{day}-{month}"
            greg_key = f"@{gregorian_date.day}-{gregorian_date.month}"
            
            events_list = []
            if hijri_key in events and not hijri_key.startswith('@'):
                events_list.extend(events[hijri_key])
            if greg_key in events:
                events_list.extend(events[greg_key])
                
            result["events"] = events_list
            
        else:
            # Convert Gregorian to Hijri
            if month < 1 or month > 12:
                return jsonify({"error": "Month must be between 1 and 12"}), 400
                
            days_in_month = calendar.monthrange(year, month)[1]
            if day < 1 or day > days_in_month:
                return jsonify({"error": f"Day must be between 1 and {days_in_month} for {GREGORIAN_MONTHS[month-1]}"}), 400
                
            gregorian_date = datetime.date(year, month, day)
            hijri_year, hijri_month, hijri_day = custom_cal.convert_to_custom_calendar(gregorian_date)
            
            if isinstance(hijri_month, str):
                hijri_month_name = hijri_month
                hijri_month_index = CUSTOM_MONTHS.index(hijri_month) + 1
            else:
                hijri_month_name = CUSTOM_MONTHS[hijri_month-1]
                hijri_month_index = hijri_month
                
            result = {
                "original": {
                    "day": day,
                    "month": month,
                    "month_name": GREGORIAN_MONTHS[month-1],
                    "year": year,
                    "calendar": "Gregorian"
                },
                "converted": {
                    "day": hijri_day,
                    "month": hijri_month_index,
                    "month_name": hijri_month_name,
                    "year": hijri_year,
                    "calendar": "Hijri"
                }
            }
            
            # Check for events
            greg_key = f"@{day}-{month}"
            hijri_key = f"{hijri_day}-{hijri_month_index}"
            
            events_list = []
            if greg_key in events:
                events_list.extend(events[greg_key])
            if hijri_key in events and not hijri_key.startswith('@'):
                events_list.extend(events[hijri_key])
                
            result["events"] = events_list
        
        return jsonify(result), 200
        
    except Exception as e:
        import traceback
        print(f"Error converting date: {str(e)}")
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':

    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port)