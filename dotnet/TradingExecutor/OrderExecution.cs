using System.Net.Http.Json;

public interface IOrderExecutor
{
    Task PlaceBuyAsync(string symbol, decimal qty);
    Task PlaceSellAsync(string symbol, decimal qty);
}

public sealed class MockOrderExecutor : IOrderExecutor
{
    public Task PlaceBuyAsync(string symbol, decimal qty)
    {
        Console.WriteLine($"[MOCK BUY] {symbol} qty={qty}");
        return Task.CompletedTask;
    }

    public Task PlaceSellAsync(string symbol, decimal qty)
    {
        Console.WriteLine($"[MOCK SELL] {symbol} qty={qty}");
        return Task.CompletedTask;
    }
}

// EXEMPLO para implementação real (Binance):
// - Usar Binance.Net ou sua própria chamada REST assinada (HMAC SHA256) com API key/secret.
// - Implementar PlaceBuyAsync/PlaceSellAsync criando ordens LIMIT/MARKET conforme sua preferência.
// - Respeitar limites de lote/tickSize da exchange.
// public sealed class BinanceSpotOrderExecutor : IOrderExecutor { ... }
