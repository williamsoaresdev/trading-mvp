using System.Net.Http.Json;
using System.Text.Json;
using System.Text.Json.Serialization;

var http = new HttpClient { BaseAddress = new Uri("http://localhost:8000") };
IOrderExecutor executor = new MockOrderExecutor();

// Parâmetros simples
string symbol = "BTC/USDT";
string timeframe = "1h";
decimal capital = 10_000m;   // capital em USD (ajuste conforme sua conta)

Console.WriteLine("TradingExecutor started. Press Ctrl+C to stop.");

while (true)
{
    try
    {
        var resp = await http.GetFromJsonAsync<PredictResponse>($"/predict?symbol={Uri.EscapeDataString(symbol)}&timeframe={timeframe}");
        if (resp is null)
        {
            Console.WriteLine("Predict returned null");
        }
        else
        {
            Console.WriteLine($"{DateTime.UtcNow:O} | {resp.symbol} {resp.timeframe} | {resp.decision} | pBuy={resp.proba_buy:F3} pSell={resp.proba_sell:F3} | price={resp.price:F2} | pos={resp.position_fraction:P1}");

            // rulebook simples: se BUY/SELL acima de limiar, posiciona fração do capital
            if (resp.decision == "BUY")
            {
                var qty = (capital * (decimal)resp.position_fraction) / (decimal)resp.price;
                await executor.PlaceBuyAsync(resp.symbol, qty);
            }
            else if (resp.decision == "SELL")
            {
                var qty = (capital * (decimal)resp.position_fraction) / (decimal)resp.price;
                await executor.PlaceSellAsync(resp.symbol, qty);
            }
        }
    }
    catch (Exception ex)
    {
        Console.WriteLine($"Error: {ex.Message}");
    }

    // aguarda 60s (para timeframe 1h, poderia aguardar até fechar candle, este é um MVP)
    await Task.Delay(TimeSpan.FromSeconds(60));
}

public sealed class PredictResponse
{
    public string symbol { get; set; } = "";
    public string timeframe { get; set; } = "";
    public string decision { get; set; } = "";
    public double proba_buy { get; set; }
    public double proba_sell { get; set; }
    public double position_fraction { get; set; }
    public double price { get; set; }
    public double atr_pct { get; set; }
    public string ts_utc { get; set; } = "";
}
