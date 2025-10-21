using System.Net.Http.Json;
using TradingExecutor.Domain.Interfaces;
using TradingExecutor.Domain.Models;

// Legacy interface for backward compatibility
public interface ILegacyOrderExecutor
{
    Task PlaceBuyAsync(string symbol, decimal qty);
    Task PlaceSellAsync(string symbol, decimal qty);
}

public sealed class LegacyMockOrderExecutor : ILegacyOrderExecutor
{
    public Task PlaceBuyAsync(string symbol, decimal qty)
    {
        Console.WriteLine($"[LEGACY MOCK BUY] {symbol} qty={qty}");
        return Task.CompletedTask;
    }

    public Task PlaceSellAsync(string symbol, decimal qty)
    {
        Console.WriteLine($"[LEGACY MOCK SELL] {symbol} qty={qty}");
        return Task.CompletedTask;
    }
}

// EXAMPLE for real implementation (Binance):
// - Use Binance.Net or your own signed REST call (HMAC SHA256) with API key/secret.
// - Implement PlaceBuyAsync/PlaceSellAsync creating LIMIT/MARKET orders as per your preference.
// - Respect exchange lot/tickSize limits.
// public sealed class BinanceSpotOrderExecutor : IOrderExecutor { ... }
