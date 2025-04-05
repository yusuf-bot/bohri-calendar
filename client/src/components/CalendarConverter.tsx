import React, { useState, useEffect } from 'react';
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
  const [loadingMessage, setLoadingMessage] = useState('');
  const [timeRemaining, setTimeRemaining] = useState(120); // Start with 2 minutes
  const { toast } = useToast();

  // Array of interesting loading messages
  const loadingMessages = [
    "Aligning celestial bodies...",
    "Converting lunar cycles...",
    "Calculating leap years...",
    "Synchronizing calendar systems...",
    "Mapping time across centuries...",
    "Consulting ancient astronomers...",
    "Adjusting for historical accuracy...",
    "Rendering calendar aesthetics...",
    "Finalizing month transitions...",
    "Preparing your time travel document..."
  ];

  // Effect to handle loading state messages and countdown
  useEffect(() => {
    if (!isLoading) return;
    
    // Set initial loading message
    setLoadingMessage(loadingMessages[0]);
    
    // Change message every 5 seconds
    const messageInterval = setInterval(() => {
      const randomIndex = Math.floor(Math.random() * loadingMessages.length);
      setLoadingMessage(loadingMessages[randomIndex]);
    }, 5000);
    
    // Define the specific time displays we want to show (in seconds)
    const timeDisplays = [120, 60, 30, 15, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1];
    setTimeRemaining(timeDisplays[0]); // Start with 2 minutes
    
    // Set up timers for each time display
    const timers = timeDisplays.map((time, index) => {
      if (index === 0) return null; // Skip the first one as we've already set it
      
      // Calculate how many milliseconds from start until we should show this time
      const delay = (timeDisplays[0] - time) * 1000;
      
      return setTimeout(() => {
        setTimeRemaining(time);
      }, delay);
    });
    
    return () => {
      clearInterval(messageInterval);
      // Clear all timers
      timers.forEach(timer => timer && clearTimeout(timer));
    };
  }, [isLoading]);

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
      // Generate and download the PDF
      const pdfBlob = await generatePDF(calendarType, Number(year));
      
      // Create a download link and trigger it
      const url = URL.createObjectURL(pdfBlob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `calendar_${calendarType}_${year}.pdf`;
      document.body.appendChild(a);
      a.click();
      
      // Clean up
      URL.revokeObjectURL(url);
      document.body.removeChild(a);
      
      toast({
        title: "Success!",
        description: "Your calendar PDF has been downloaded.",
      });
    } catch (error) {
      toast({
        title: "Error",
        description: error instanceof Error ? error.message : "Failed to generate PDF",
        variant: "destructive"
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center">
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle className="text-2xl">Calendar Converter</CardTitle>
          <CardDescription>
            Generate a calendar PDF for any year in Bohri Hijri or Georgian calendar
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="calendar-type">Calendar Type</Label>
              <RadioGroup
                defaultValue={calendarType}
                onValueChange={(value) => setCalendarType(value as 'islamic' | 'georgian')}
                className="flex space-x-4"
              >
                <div className="flex items-center space-x-2">
                  <RadioGroupItem value="islamic" id="islamic" />
                  <Label htmlFor="islamic">Bohri Hijri </Label>
                </div>
                <div className="flex items-center space-x-2">
                  <RadioGroupItem value="georgian" id="georgian" />
                  <Label htmlFor="georgian">Georgian</Label>
                </div>
              </RadioGroup>
            </div>
            
            <div className="space-y-2">
              <Label htmlFor="year">Year</Label>
              <Input
                id="year"
                placeholder={`Enter ${calendarType} year`}
                value={year}
                onChange={(e) => setYear(e.target.value)}
                type="number"
              />
            </div>
          </div>
        </CardContent>
        <CardFooter>
          <Button 
            className="w-full" 
            onClick={handleDownload}
            disabled={isLoading}
          >
            {isLoading ? (
              <span className="flex items-center">
                <Calendar className="mr-2 h-4 w-4 animate-spin" />
                {loadingMessage}
              </span>
            ) : (
              <span className="flex items-center">
                <FileDown className="mr-2 h-4 w-4" />
                Download Calendar PDF
              </span>
            )}
          </Button>
        </CardFooter>
      </Card>
      
      {isLoading && (
        <div className="mt-4 text-sm text-muted-foreground text-center">
          <p>Estimated time remaining: {timeRemaining >= 60 
            ? `${Math.floor(timeRemaining / 60)} minute${Math.floor(timeRemaining / 60) > 1 ? 's' : ''}` 
            : `${timeRemaining} second${timeRemaining !== 1 ? 's' : ''}`}
          </p>
          <div className="w-64 h-1 bg-gray-200 rounded-full mt-2">
            <div 
              className="h-full bg-primary rounded-full transition-all duration-1000"
              style={{ width: `${Math.max(0, (timeRemaining / 120) * 100)}%` }}
            ></div>
          </div>
        </div>
      )}
    </div>
  );
};

export default CalendarConverter;