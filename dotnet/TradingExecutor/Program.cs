using TradingExecutor;

class Program
{
    static async Task Main(string[] args)
    {
        Console.WriteLine("🤖 Trading MVP - Real-Time Executor");
        Console.WriteLine("=====================================");
        Console.WriteLine();
        
        var executor = new RealTimeTradingExecutor();
        
        // Handle Ctrl+C gracefully
        Console.CancelKeyPress += (sender, e) =>
        {
            e.Cancel = true;
            Console.WriteLine("\n👋 Shutdown requested...");
            executor.Stop();
        };
        
        try
        {
            await executor.StartAsync();
        }
        catch (Exception ex)
        {
            Console.WriteLine($"❌ Fatal error: {ex.Message}");
        }
        
        Console.WriteLine("🏁 Executor stopped");
    }
}
