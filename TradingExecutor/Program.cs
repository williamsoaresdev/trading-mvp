using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using TradingExecutor.Application.Services;
using TradingExecutor.Domain.Interfaces;
using TradingExecutor.Infrastructure.Services;
using TradingExecutor.Infrastructure.WebSocket;

namespace TradingExecutor;

class Program
{
    static async Task Main(string[] args)
    {
        Console.WriteLine("🤖 Trading MVP - Real-Time Executor");
        Console.WriteLine("=====================================");
        Console.WriteLine();
        
        // Build dependency injection container
        var host = CreateHostBuilder(args).Build();
        
        // Get the main service
        var tradingService = host.Services.GetRequiredService<TradingExecutionService>();
        
        // Handle Ctrl+C gracefully
        var cancellationTokenSource = new CancellationTokenSource();
        Console.CancelKeyPress += (sender, e) =>
        {
            e.Cancel = true;
            Console.WriteLine("\n👋 Shutdown requested...");
            cancellationTokenSource.Cancel();
        };
        
        try
        {
            // Start the trading service
            await tradingService.StartAsync();
            
            // Wait for cancellation
            await Task.Delay(Timeout.Infinite, cancellationTokenSource.Token);
        }
        catch (OperationCanceledException)
        {
            // Expected when cancellation is requested
        }
        catch (Exception ex)
        {
            Console.WriteLine($"❌ Fatal error: {ex.Message}");
        }
        finally
        {
            // Stop the service gracefully
            await tradingService.StopAsync();
            tradingService.Dispose();
        }
        
        Console.WriteLine("🏁 Executor stopped");
    }
    
    /// <summary>
    /// Configure dependency injection container.
    /// This follows the Dependency Inversion Principle - high-level modules
    /// don't depend on low-level modules, both depend on abstractions.
    /// </summary>
    static IHostBuilder CreateHostBuilder(string[] args) =>
        Host.CreateDefaultBuilder(args)
            .ConfigureServices((context, services) =>
            {
                // Configuration
                services.AddSingleton<IConfigurationProvider, ConfigurationProvider>();
                
                // Logging
                services.AddSingleton<ITradingLogger, ConsoleTradingLogger>();
                
                // Core services
                services.AddSingleton<IRiskManager, RiskManager>();
                services.AddSingleton<IOrderExecutor, MockOrderExecutor>();
                services.AddSingleton<IWebSocketClient, TradingWebSocketClient>();
                
                // Application service
                services.AddSingleton<TradingExecutionService>();
            });
}
