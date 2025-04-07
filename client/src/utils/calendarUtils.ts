/**
 * Converts a year between Islamic and Georgian calendars
 * @param sourceCalendar The source calendar type ('islamic' or 'georgian')
 * @param year The year to convert
 * @returns The converted year
 */
export const generatePDF = async (
  calendarType: string, 
  year: number, 
  quality: 'low' | 'medium' | 'high' = 'medium'
) => {
  try {
    // First check if server is reachable
    const healthCheck = await checkServerHealth();
    if (!healthCheck) {
      throw new Error('Server is not running or not accessible');
    }

    console.log('Attempting to generate PDF with:', { calendarType, year, quality });
    
    const response = await fetch('http://localhost:5001/api/calendar', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/pdf',
      },
      mode: 'cors',
      credentials: 'include',
      body: JSON.stringify({
        year,
        calendar_type: calendarType,
        quality
      }),
    });
    
    console.log('Server response status:', response.status);
    console.log('Server response headers:', response.headers);
    
    if (!response.ok) {
      const errorText = await response.text();
      console.error('Server error response:', errorText);
      throw new Error(`Server error: ${errorText || response.statusText}`);
    }
    
    return await response.blob();
  } catch (error) {
    console.error('Detailed error:', error);
    throw error;
  }
};

export async function checkServerHealth(): Promise<boolean> {
  try {
    const response = await fetch('http://localhost:5001/api/health');
    if (!response.ok) {
      throw new Error(`Server health check failed: ${response.status}`);
    }
    return true;
  } catch (error) {
    console.error('Server health check failed:', error);
    return false;
  }
}

export const convertCalendar = async (
  fromType: 'islamic' | 'georgian',
  toType: 'islamic' | 'georgian',
  year: number
) => {
  try {
    const response = await fetch('http://localhost:5001/api/convert', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        from_type: fromType,
        to_type: toType,
        year,
      }),
    });
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ error: 'Unknown error' }));
      throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error converting calendar:', error);
    throw error;
  }
};

// Add this function for date conversion
export async function convertDate(
  day: number,
  month: number,
  year: number,
  conversionType: 'greg-to-hijri' | 'hijri-to-greg'
): Promise<any> {
  try {
    const response = await fetch('http://localhost:5001/api/convert-date', {
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