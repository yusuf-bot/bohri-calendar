
import CalendarConverter from "@/components/CalendarConverter";

const Index = () => {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-b from-slate-50 to-slate-100 p-4">
      <h1 className="text-3xl font-bold mb-8 text-center">Islamic-Georgian Calendar Converter</h1>
      <CalendarConverter />
      <footer className="mt-12 text-center text-sm text-muted-foreground">
        <p>Enter a year and download a PDF showing both Islamic (Hijri) and Georgian calendar years</p>
      </footer>
    </div>
  );
};

export default Index;
