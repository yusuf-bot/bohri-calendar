import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group';
import { Calendar, ArrowRight } from 'lucide-react';
import { useToast } from '@/components/ui/use-toast';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { Badge } from '@/components/ui/badge';

interface ConversionResult {
  original: {
    day: number;
    month: number;
    month_name: string;
    year: number;
    calendar: string;
  };
  converted: {
    day: number;
    month: number;
    month_name: string;
    year: number;
    calendar: string;
  };
  events: string[];
}

const DateConverter = () => {
  const [conversionType, setConversionType] = useState<'greg-to-hijri' | 'hijri-to-greg'>('greg-to-hijri');
  const [day, setDay] = useState<string>('');
  const [month, setMonth] = useState<string>('');
  const [year, setYear] = useState<string>('');
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<ConversionResult | null>(null);
  const { toast } = useToast();

  const gregorianMonths = [
    'January', 'February', 'March', 'April', 'May', 'June', 
    'July', 'August', 'September', 'October', 'November', 'December'
  ];
  
  const hijriMonths = [
    "Muharram", "Safar", "Rabi al-Awwal", "Rabi al-Thani",
    "Jumada al-Awwal", "Jumada al-Thani", "Rajab", "Sha'ban",
    "Ramadan", "Shawwal", "Dhu al-Qadah", "Dhu al-Hijjah"
  ];

  const handleConvert = async () => {
    if (!day || !month || !year) {
      toast({
        title: "Missing Information",
        description: "Please enter day, month, and year.",
        variant: "destructive"
      });
      return;
    }

    if (isNaN(Number(day)) || isNaN(Number(month)) || isNaN(Number(year))) {
      toast({
        title: "Invalid Input",
        description: "Day, month, and year must be numbers.",
        variant: "destructive"
      });
      return;
    }

    setIsLoading(true);
    
    try {
      const response = await fetch('http://localhost:5000/api/convert-date', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          day: parseInt(day),
          month: parseInt(month),
          year: parseInt(year),
          conversion_type: conversionType,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to convert date');
      }

      const data = await response.json();
      setResult(data);
      
      toast({
        title: "Success!",
        description: "Date conversion completed.",
      });
    } catch (error) {
      toast({
        title: "Error",
        description: error instanceof Error ? error.message : "Failed to convert date",
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
          <CardTitle className="text-2xl">Date Converter</CardTitle>
          <CardDescription>
            Convert between Islamic Hijri and Gregorian dates
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="conversion-type">Conversion Type</Label>
              <RadioGroup
                defaultValue={conversionType}
                onValueChange={(value) => setConversionType(value as 'greg-to-hijri' | 'hijri-to-greg')}
                className="flex space-x-4"
              >
                <div className="flex items-center space-x-2">
                  <RadioGroupItem value="greg-to-hijri" id="greg-to-hijri" />
                  <Label htmlFor="greg-to-hijri">Gregorian to Hijri</Label>
                </div>
                <div className="flex items-center space-x-2">
                  <RadioGroupItem value="hijri-to-greg" id="hijri-to-greg" />
                  <Label htmlFor="hijri-to-greg">Hijri to Gregorian</Label>
                </div>
              </RadioGroup>
            </div>
            
            <div className="grid grid-cols-3 gap-4">
              <div className="space-y-2">
                <Label htmlFor="day">Day</Label>
                <Input
                  id="day"
                  placeholder="Day"
                  value={day}
                  onChange={(e) => setDay(e.target.value)}
                  type="number"
                  min="1"
                  max="31"
                />
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="month">Month</Label>
                <Select value={month} onValueChange={setMonth}>
                  <SelectTrigger>
                    <SelectValue placeholder="Month" />
                  </SelectTrigger>
                  <SelectContent>
                    {Array.from({ length: 12 }, (_, i) => i + 1).map((m) => (
                      <SelectItem key={m} value={m.toString()}>
                        {m} - {conversionType === 'greg-to-hijri' ? gregorianMonths[m-1] : hijriMonths[m-1]}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="year">Year</Label>
                <Input
                  id="year"
                  placeholder="Year"
                  value={year}
                  onChange={(e) => setYear(e.target.value)}
                  type="number"
                />
              </div>
            </div>
          </div>
        </CardContent>
        <CardFooter>
          <Button 
            className="w-full" 
            onClick={handleConvert}
            disabled={isLoading}
          >
            {isLoading ? (
              <span className="flex items-center">
                <Calendar className="mr-2 h-4 w-4 animate-spin" />
                Converting...
              </span>
            ) : (
              <span className="flex items-center">
                <ArrowRight className="mr-2 h-4 w-4" />
                Convert Date
              </span>
            )}
          </Button>
        </CardFooter>
      </Card>
      
      {result && (
        <Card className="w-full max-w-md mt-6">
          <CardHeader>
            <CardTitle className="text-xl">Conversion Result</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <div className="text-center">
                  <p className="text-sm text-muted-foreground">{result.original.calendar}</p>
                  <p className="text-xl font-bold">
                    {result.original.day} {result.original.month_name} {result.original.year}
                  </p>
                </div>
                
                <ArrowRight className="h-5 w-5 text-muted-foreground" />
                
                <div className="text-center">
                  <p className="text-sm text-muted-foreground">{result.converted.calendar}</p>
                  <p className="text-xl font-bold">
                    {result.converted.day} {result.converted.month_name} {result.converted.year}
                  </p>
                </div>
              </div>
              
              {result.events && result.events.length > 0 && (
                <div className="mt-4">
                  <h3 className="text-lg font-semibold mb-2">Events on this day:</h3>
                  <div className="space-y-2">
                    {result.events.map((event, index) => (
                      <Badge key={index} variant="secondary" className="mr-2 text-sm py-1 px-2">
                        {event}
                      </Badge>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default DateConverter;