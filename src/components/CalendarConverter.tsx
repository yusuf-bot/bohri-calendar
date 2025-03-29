
import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group';
import { ArrowRight, FileDown, Calendar } from 'lucide-react';
import { useToast } from '@/components/ui/use-toast';
import { convertCalendar } from '@/utils/calendarUtils';

const CalendarConverter = () => {
  const [calendarType, setCalendarType] = useState<'islamic' | 'georgian'>('islamic');
  const [year, setYear] = useState<string>('');
  const [convertedYear, setConvertedYear] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const { toast } = useToast();

  const handleConvert = async () => {
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
      const result = await convertCalendar(calendarType, Number(year));
      setConvertedYear(result);
      toast({
        title: "Conversion Complete",
        description: `Year converted successfully.`,
      });
    } catch (error) {
      toast({
        title: "Conversion Failed",
        description: "There was an error converting the year. Please try again.",
        variant: "destructive"
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleDownloadPDF = async () => {
    if (!convertedYear) return;

    try {
      // Generate and download the PDF using our utility
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
        description: "There was an error downloading the PDF. Please try again.",
        variant: "destructive"
      });
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
          Convert between Islamic and Georgian calendars
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
        
        {convertedYear && (
          <div className="p-4 bg-secondary/30 rounded-md">
            <p className="text-sm">
              <span className="font-semibold">{calendarType === 'islamic' ? 'Georgian' : 'Islamic'} Year:</span> 
              <span className="ml-2">{convertedYear}</span>
            </p>
          </div>
        )}
      </CardContent>
      <CardFooter className="flex flex-col space-y-4">
        <Button 
          onClick={handleConvert} 
          className="w-full" 
          disabled={isLoading}
        >
          {isLoading ? 'Converting...' : 'Convert'}
          <ArrowRight className="ml-2 h-4 w-4" />
        </Button>
        
        {convertedYear && (
          <Button 
            onClick={handleDownloadPDF}
            variant="outline" 
            className="w-full"
          >
            Download PDF
            <FileDown className="ml-2 h-4 w-4" />
          </Button>
        )}
      </CardFooter>
    </Card>
  );
};

export default CalendarConverter;
