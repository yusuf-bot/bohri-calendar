
// Simple utility for converting between Islamic (Hijri) and Georgian (Gregorian) calendars
// This is a simplified implementation for demonstration purposes

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
 * Generates a PDF for the calendar conversion
 */
export const generatePDF = async (
  sourceCalendar: 'islamic' | 'georgian', 
  originalYear: number, 
  convertedYear: string
): Promise<Blob> => {
  // Import the PDF library dynamically to reduce initial load time
  const { jsPDF } = await import('jspdf');
  
  // Create a new PDF document
  const doc = new jsPDF({
    orientation: 'portrait',
    unit: 'mm',
    format: 'a4'
  });
  
  // Set up document content
  doc.setFontSize(22);
  doc.text('Calendar Conversion', 105, 20, { align: 'center' });
  
  doc.setFontSize(12);
  doc.text('Time Travel PDF Generator', 105, 30, { align: 'center' });
  
  doc.setFontSize(14);
  doc.text('Conversion Details:', 20, 50);
  
  doc.setFontSize(12);
  const sourceLabel = sourceCalendar === 'islamic' ? 'Islamic (Hijri) Year' : 'Georgian Year';
  const targetLabel = sourceCalendar === 'islamic' ? 'Georgian Year' : 'Islamic (Hijri) Year';
  
  doc.text(`${sourceLabel}: ${originalYear}`, 30, 60);
  doc.text(`${targetLabel}: ${convertedYear}`, 30, 70);
  
  doc.setFontSize(10);
  const date = new Date();
  doc.text(`Generated on: ${date.toLocaleDateString()} at ${date.toLocaleTimeString()}`, 105, 280, { align: 'center' });
  
  // Return the document as a blob
  return doc.output('blob');
};
