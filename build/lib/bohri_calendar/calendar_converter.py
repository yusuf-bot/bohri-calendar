import io
import calendar
import datetime

def print_custom_calendar(start_year, end_year, calendar_obj):
    """
    Generate custom calendars with precise formatting
    
    :param start_year: Starting Gregorian year
    :param end_year: Ending Gregorian year
    :param calendar_obj: CustomCalendar instance
    """
    # Use io.StringIO to capture output before writing to file
    output = io.StringIO()
    
    # Iterate through each year
    for year in range(start_year, end_year + 1):
        output.write(f"Calendar for {year}:\n")
        output.write(f"{year}\n\n")
        
        # Create a standard calendar for reference
        cal = calendar.Calendar()
        
        # Process months in groups of 3
        for row_start_month in range(1, 13, 3):
            # Prepare to store month outputs
            month_outputs = []
            
            # Process 3 months in each row
            for month_offset in range(3):
                month = row_start_month + month_offset
                if month > 12:
                    break
                
                # Get the month name
                month_name = calendar.month_name[month]
                
                # Get the custom calendar details for the first day of the month
                first_date = datetime.date(year, month, 1)
                try:
                    custom_year, custom_month, _ = calendar_obj.convert_to_custom_calendar(first_date)
                    custom_month_str = custom_month.upper()
                except Exception:
                    custom_year, custom_month_str = "N/A", "N/A"
                
                # Prepare month output
                month_output = [
                   f"{month_name} (Custom: {custom_month_str} Yr {custom_year})".center(49),
                    "  Mo     Tu     We     Th     Fr     Sa     Su   "
                ]
                
                # Create a matrix of weeks and days for this month
                month_calendar = cal.monthdayscalendar(year, month)
                
                # Process each week
                for week in month_calendar:
                    week_output = []
                    for day in week:
                        if day == 0:
                            week_output.append("       ")
                        else:
                            try:
                                # Convert each day to custom calendar
                                curr_date = datetime.date(year, month, day)
                                _, _, custom_day = calendar_obj.convert_to_custom_calendar(curr_date)
                                
                                # Format the output to show both Gregorian and custom day
                                week_output.append(f"{day:02d}({custom_day:02d})")
                            except Exception:
                                week_output.append(f"{day:2d}(--)")
                    
                    month_output.append(" ".join(week_output))
                
                month_outputs.append(month_output)
            
            # Determine max lines to print
            max_lines = max(len(m) for m in month_outputs)
            
            # Print months side by side
            for line_index in range(max_lines):
                line_parts = []
                for month_output in month_outputs:
                    # Get line or pad with spaces
                    line_part = month_output[line_index] if line_index < len(month_output) else " " * 20
                    line_parts.append(f"{line_part:<50}")
                
                output.write("".join(line_parts) + "\n")
            
            output.write("\n")
        
        output.write("\n\n")
    
    # Write to file
    with open('custom_calendar_1969_2018.txt', 'w') as f:
        f.write(output.getvalue())
    
    print("Calendar has been saved to custom_calendar_1969_2018.txt")



class CustomCalendar:
    def __init__(self):
        # Reference point: September 12, 2018 is the first day of year 1440 in custom calendar
        self.reference_date = datetime.date(2018, 9, 11)
        
        # Month names
        self.month_order = [
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
        
        # Precise month lengths
        self.month_days = {}
        days=30
        for i in self.month_order:
            self.month_days[i] = days
            if days==30:
                days=29
            else:
                days=30

    
    def is_leap_year(self, year):
        """
        Determine if it's a leap year based on the specified conditions
        Leap years occur when year mod 30 is in the list: 2, 5, 8, 13, 16, 19, 21, 24, 27, 29
        """
        leap_year_mods = [2, 5, 8, 10, 13, 16, 19, 21, 24, 27, 29]
        return year % 30 in leap_year_mods
    

    def get_month_calendar(self, year, month):
        """
        Generate a calendar matrix for a Hijri month
        Returns a list of weeks, where each week is a list of days (0 for padding)
        """
        # Get the month name from index
        month_name = self.month_order[month-1]
        
        # Get the first day of the month in Gregorian
        first_day_greg = self.convert_to_gregorian(year, month_name, 1)
        
        # Get the number of days in this month
        month_length = self.get_month_days(month_name, year)
      
        # Get the day of week for the first day (0 = Monday, 6 = Sunday)
        first_weekday = first_day_greg.weekday()
        
        # Create the calendar matrix
        calendar_matrix = []
        week = [0] * first_weekday
        
        for day in range(1, month_length + 1):
            week.append(day)
            
            # If we've filled a week or reached the end of the month
            if len(week) == 7:
                calendar_matrix.append(week)
                week = []
        
        # Pad the last week if necessary
        if week:
            week.extend([0] * (7 - len(week)))
            calendar_matrix.append(week)
        
        return calendar_matrix


    def get_month_days(self, month, year):
        """
        Get the number of days in a given month
        If it's the last month (l) and it's a leap year, add an extra day
        """
        days = self.month_days[month]
        
        # If it's the last month and a leap year, add an extra day
        if month == "Dhu al-Hijjah" and self.is_leap_year(year):
            days += 1
        
        return days
    def convert_to_custom_calendar(self, gregorian_date):
        """
        Convert a Gregorian date to the custom calendar with precise calculations
        
        :param gregorian_date: datetime.date object
        :return: tuple of (custom_year, custom_month, custom_day)
        """
        # Calculate days between the reference date and the input date
        days_difference = (gregorian_date - self.reference_date).days

        # Calculate the custom calendar year
        custom_year = 1440
        remaining_days = abs(days_difference)
        is_negative = days_difference < 0

        if is_negative:
            # Going backwards
            while remaining_days > 354 + (1 if self.is_leap_year(custom_year - 1) else 0):

                year_days = 354 + (1 if self.is_leap_year(custom_year - 1) else 0)
   
                remaining_days -= year_days
                custom_year -= 1
        else:
            # Going forwards
            while remaining_days >= 354 + (1 if self.is_leap_year(custom_year) else 0):
      
                year_days = 354 + (1 if self.is_leap_year(custom_year) else 0)
                remaining_days -= year_days
                custom_year += 1

        # Determine month and day
        if is_negative:
            # Adjust remaining days
   
            total_year_days = 354 + (1 if self.is_leap_year(custom_year-1) else 0)
            remaining_days = total_year_days - remaining_days
            custom_year-=1

            for month in (self.month_order):
           
                month_days = self.get_month_days(month, custom_year)
                if remaining_days < month_days:
                    return (custom_year, month,remaining_days+1)
                
                remaining_days -= month_days

        else:
            # Going forwards
            for month in self.month_order:
   
                month_days = self.get_month_days(month, custom_year)
                
                if remaining_days < month_days:
                    return (custom_year, month, remaining_days+1)
                
                remaining_days -= month_days
        
 
    def convert_to_gregorian(self, custom_year, custom_month, custom_day):
        """
        Convert a custom calendar date to Gregorian date with precise calculations
        
        :param custom_year: custom calendar year
        :param custom_month: custom calendar month (a-l)
        :param custom_day: day of the month
        :return: datetime.date object
        """
        # Validate input
        if custom_month not in self.month_order:
            raise ValueError(f"Invalid month. Must be one of {self.month_order}")
        
        # Validate day
        month_days = self.get_month_days(custom_month, custom_year)
        if custom_day < 1 or custom_day > month_days:
            raise ValueError(f"Invalid day for month {custom_month}. Must be between 1 and {month_days}")
        
        # Calculate total days from the reference point
        total_days = 0
        
        # Handling years going forward from reference point
        if custom_year >= 1440:
            # Calculate days for full years
            for year in range(1440, custom_year):
                total_days += 354 + (1 if self.is_leap_year(year) else 0)
            
            # Add days for months before the target month
            for month in self.month_order[:self.month_order.index(custom_month)]:
                total_days += self.get_month_days(month, custom_year)
            
            # Add the days in the target month
            total_days += custom_day - 1
        
        # Handling years going backward from reference point
        else:
            # Calculate days for full years
            for year in range(custom_year, 1440):
                
                total_days += 354 + (1 if self.is_leap_year(year) else 0)
   
            # Negate total days for backward calculation
            total_days = -total_days

            # Subtract days in months before the target month
            for month in self.month_order[:self.month_order.index(custom_month)]:
                total_days += self.get_month_days(month, custom_year)

            # Adjusted to match day counting logic
            total_days += (custom_day-1)

        # Calculate the Gregorian date
        gregorian_date = self.reference_date + datetime.timedelta(days=total_days)
        
        return gregorian_date

def main():
    calendar = CustomCalendar()
    
    print("Custom Calendar Converter")
    print("Reference: September 12, 2018 is the first day of year 1440")
    print("Conversion Options:")
    print("1. Gregorian to Custom Calendar")
    print("2. Custom Calendar to Gregorian")
    print("3. Exit")
    
    while True:
        try:
            choice = input("\nEnter your choice (1/2/3): ").strip()
            
            if choice == '3':
                print("Exiting...")
                break
            
            if choice == '1':
                # Gregorian to Custom Calendar
                date_str = input("Enter Gregorian date (YYYY-MM-DD): ").strip()
                gregorian_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
                
                custom_year, custom_month, custom_day = calendar.convert_to_custom_calendar(gregorian_date)
                print("\nConversion Result:")
                print(f"Gregorian Date: {gregorian_date}")
                print(f"Custom Calendar: Year {custom_year}, Month {custom_month}, Day {custom_day}")
            
            elif choice == '2':
                # Custom Calendar to Gregorian
                custom_year = int(input("Enter Custom Calendar Year: ").strip())
                custom_month = input("Enter Custom Calendar Month (a-l): ").strip().lower()
                custom_day = int(input("Enter Custom Calendar Day: ").strip())
                
                gregorian_date = calendar.convert_to_gregorian(custom_year, custom_month, custom_day)
                print("\nConversion Result:")
                print(f"Custom Calendar: Year {custom_year}, Month {custom_month}, Day {custom_day}")
                print(f"Gregorian Date: {gregorian_date}")
            
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
        
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    cal=CustomCalendar()
    print_custom_calendar(1969,2018,cal)
    main()
   