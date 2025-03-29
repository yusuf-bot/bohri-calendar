
import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group';
import { FileDown, Calendar } from 'lucide-react';
import { useToast } from '@/components/ui/use-toast';
import { convertCalendar, generatePDF } from '@/utils/calendarUtils';

const CalendarConverter = () => {
  const [calendarType, setCalendarType] = useState<'islamic' | 'georgian'>('islamic');
  const [year, setYear] = useState<string>('');
  const [isLoading, setIsLoading] = useState(false);
  const { toast } = useToast();

  const handleDownload = async () => {
    if (!year || isNaN(Number(year))) {
      toast({
        title: "Invalid Year",
        description: "Please enter a valid year.",
        variant: "destructive"
      });
      return;
    }

    setIsLoading(true);
    try {
      // Convert the year using our utility function
      const convertedYear = await convertCalendar(calendarType, Number(year));
      
      // Generate and download the PDF with both years
      const pdfBlob = await generatePDF(calendarType, Number(year), convertedYear);
      
      // Create a download link and trigger it
      const url = URL.createObjectURL(pdfBlob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `calendar-conversion-${year}.pdf`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);

      toast({
        title: "PDF Downloaded",
        description: "Your PDF has been downloaded successfully.",
      });
    } catch (error) {
      toast({
        title: "Download Failed",
        description: "There was an error generating the PDF. Please try again.",
        variant: "destructive"
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Card className="w-full max-w-md mx-auto">
      <CardHeader className="text-center">
        <div className="flex justify-center mb-2">
          <Calendar className="h-8 w-8 text-primary" />
        </div>
        <CardTitle className="text-xl">Time Travel PDF</CardTitle>
        <CardDescription>
          Download calendar conversion between Islamic and Georgian years
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        <div className="space-y-2">
          <Label htmlFor="calendar-type">Calendar Type</Label>
          <RadioGroup 
            value={calendarType} 
            onValueChange={(value) => setCalendarType(value as 'islamic' | 'georgian')}
            className="flex space-x-4"
          >
            <div className="flex items-center space-x-2">
              <RadioGroupItem value="islamic" id="islamic" />
              <Label htmlFor="islamic">Islamic (Hijri)</Label>
            </div>
            <div className="flex items-center space-x-2">
              <RadioGroupItem value="georgian" id="georgian" />
              <Label htmlFor="georgian">Georgian</Label>
            </div>
          </RadioGroup>
        </div>
        
        <div className="space-y-2">
          <Label htmlFor="year">Enter Year</Label>
          <Input
            id="year"
            type="number"
            value={year}
            onChange={(e) => setYear(e.target.value)}
            placeholder={`Enter ${calendarType} year`}
          />
        </div>
      </CardContent>
      <CardFooter>
        <Button 
          onClick={handleDownload} 
          className="w-full" 
          disabled={isLoading}
        >
          {isLoading ? 'Processing...' : 'Download PDF'}
          <FileDown className="ml-2 h-4 w-4" />
        </Button>
      </CardFooter>
    </Card>
  );
};

export default CalendarConverter;
