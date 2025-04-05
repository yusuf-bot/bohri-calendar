import React, { useState } from 'react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import CalendarConverter from '@/components/CalendarConverter';
import DateConverter from '@/components/DateConverter';
import { Toaster } from '@/components/ui/toaster';

function App() {
  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md mx-auto">
        <h1 className="text-3xl font-bold text-center mb-8">Calendar Tools</h1>
        
        <Tabs defaultValue="calendar" className="w-full">
          <TabsList className="grid w-full grid-cols-2 mb-8">
            <TabsTrigger value="calendar">Calendar PDF</TabsTrigger>
            <TabsTrigger value="date">Date Converter</TabsTrigger>
          </TabsList>
          
          <TabsContent value="calendar">
            <CalendarConverter />
          </TabsContent>
          
          <TabsContent value="date">
            <DateConverter />
          </TabsContent>
        </Tabs>
      </div>
      
      <footer className="mt-12 text-center text-sm text-gray-500">
        <p>© {new Date().getFullYear()} Calendar Converter. All rights reserved.</p>
      </footer>
      
      <Toaster />
    </div>
  );
}

export default App;