/**
 * Converts a year between Islamic and Georgian calendars
 * @param sourceCalendar The source calendar type ('islamic' or 'georgian')
 * @param year The year to convert
 * @returns The converted year
 */
export const convertCalendar = async (sourceCalendar: 'islamic' | 'georgian', year: number): Promise<string> => {
  // Simulate API call with a timeout
  return new Promise((resolve) => {
    setTimeout(() => {
      if (sourceCalendar === 'islamic') {
        // Convert Islamic to Georgian
        // Approximate conversion: Georgian year ≈ Islamic year + 622 - (Islamic year / 33)
        const georgianYear = Math.round(year + 622 - (year / 33));
        resolve(georgianYear.toString());
      } else {
        // Convert Georgian to Islamic
        // Approximate conversion: Islamic year ≈ (Georgian year - 622) + ((Georgian year - 622) / 32)
        const islamicYear = Math.round((year - 622) + ((year - 622) / 32));
        resolve(islamicYear.toString());
      }
    }, 800); // Simulate network delay
  });
};

/**
 * Generates a PDF for the calendar
 */
// Add this function to check server health before attempting PDF generation
export async function checkServerHealth(): Promise<boolean> {
  try {
    const response = await fetch('http://localhost:5000/api/health');
    if (!response.ok) {
      throw new Error(`Server health check failed: ${response.status}`);
    }
    return true;
  } catch (error) {
    console.error('Server health check failed:', error);
    return false;
  }
}

export async function generatePDF(
  calendarType: 'islamic' | 'georgian', 
  year: number, 
  quality: 'low' | 'medium' | 'high' = 'medium'
): Promise<Blob> {
  try {
    // Check server health first
    const isServerHealthy = await checkServerHealth();
    if (!isServerHealthy) {
      throw new Error('Server is not responding. Please check if the server is running.');
    }
    
    // Map calendar types to what the server expects
    const serverCalendarType = calendarType === 'islamic' ? 'hijri' : 'gregorian';
    
    const response = await fetch('http://localhost:5000/api/calendar', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        year,
        calendar_type: serverCalendarType,
        quality,
      }),
      // Add these options to improve fetch behavior
      mode: 'cors',
      credentials: 'same-origin',
      cache: 'no-cache',
      redirect: 'follow',
    });

    if (!response.ok) {
      // Try to get error details from response
      let errorMessage = `Server returned ${response.status}: ${response.statusText}`;
      try {
        const errorData = await response.json();
        if (errorData && errorData.error) {
          errorMessage = errorData.error;
        }
      } catch (e) {
        // If we can't parse the error JSON, just use the status
      }
      throw new Error(errorMessage);
    }

    return await response.blob();
  } catch (error) {
    console.error('Error generating PDF:', error);
    throw error;
  }
}

// Add this function for date conversion
export async function convertDate(
  day: number,
  month: number,
  year: number,
  conversionType: 'greg-to-hijri' | 'hijri-to-greg'
): Promise<any> {
  try {
    const response = await fetch('http://localhost:5000/api/convert-date', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        day,
        month,
        year,
        conversion_type: conversionType,
      }),
      mode: 'cors',
      cache: 'no-cache',
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || `Server returned ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error converting date:', error);
    throw error;
  }
}