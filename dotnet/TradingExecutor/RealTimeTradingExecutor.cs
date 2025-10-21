using System.Net.WebSockets;
using System.Text;
using System.Text.Json;

namespace TradingExecutor;

public class WebSocketMessage
{
    public string type { get; set; } = "";
    public JsonElement data { get; set; }
}

public class TradingDecision
{
    public string timestamp { get; set; } = "";
    public string symbol { get; set; } = "";
    public PredictionData prediction { get; set; } = new();
    public long decision_id { get; set; }
}

public class PredictionData
{
    public string action { get; set; } = "";
    public double proba_buy { get; set; }
    public double proba_sell { get; set; }
    public double current_price { get; set; }
    public double position_fraction { get; set; }
    public double atr_pct { get; set; }
}

public class RealTimeTradingExecutor
{
    private readonly ClientWebSocket webSocket = new();
    private readonly string webSocketUrl = "ws://localhost:8000/ws";
    private readonly CancellationTokenSource cancellationTokenSource = new();
    private bool isConnected = false;

    public async Task StartAsync()
    {
        Console.WriteLine("🚀 Real-Time Trading Executor starting...");
        
        try
        {
            await ConnectWebSocketAsync();
            await ListenForDecisionsAsync();
        }
        catch (Exception ex)
        {
            Console.WriteLine($"❌ Error in trading executor: {ex.Message}");
        }
        finally
        {
            await DisconnectAsync();
        }
    }

    private async Task ConnectWebSocketAsync()
    {
        Console.WriteLine("🔌 Connecting to WebSocket...");
        
        try
        {
            await webSocket.ConnectAsync(new Uri(webSocketUrl), cancellationTokenSource.Token);
            isConnected = true;
            Console.WriteLine("✅ WebSocket connected successfully!");
        }
        catch (Exception ex)
        {
            Console.WriteLine($"❌ Failed to connect to WebSocket: {ex.Message}");
            throw;
        }
    }

    private async Task ListenForDecisionsAsync()
    {
        var buffer = new byte[4096];
        
        Console.WriteLine("👂 Listening for trading decisions...");
        
        while (webSocket.State == WebSocketState.Open && !cancellationTokenSource.Token.IsCancellationRequested)
        {
            try
            {
                var result = await webSocket.ReceiveAsync(new ArraySegment<byte>(buffer), cancellationTokenSource.Token);
                
                if (result.MessageType == WebSocketMessageType.Text)
                {
                    var messageJson = Encoding.UTF8.GetString(buffer, 0, result.Count);
                    await ProcessWebSocketMessage(messageJson);
                }
                else if (result.MessageType == WebSocketMessageType.Close)
                {
                    Console.WriteLine("🔚 WebSocket connection closed by server");
                    break;
                }
            }
            catch (OperationCanceledException)
            {
                Console.WriteLine("🛑 WebSocket operation cancelled");
                break;
            }
            catch (Exception ex)
            {
                Console.WriteLine($"❌ Error receiving WebSocket message: {ex.Message}");
                await Task.Delay(1000); // Wait before retry
            }
        }
    }

    private async Task ProcessWebSocketMessage(string messageJson)
    {
        try
        {
            var message = JsonSerializer.Deserialize<WebSocketMessage>(messageJson);
            
            switch (message?.type)
            {
                case "trading_decision":
                    var decision = JsonSerializer.Deserialize<TradingDecision>(message.data.GetRawText());
                    if (decision != null)
                    {
                        await ProcessTradingDecision(decision);
                    }
                    break;
                    
                case "status":
                    Console.WriteLine($"📊 Status update received: {message.data}");
                    break;
                    
                default:
                    Console.WriteLine($"📨 Unknown message type: {message?.type}");
                    break;
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"❌ Error processing message: {ex.Message}");
        }
    }

    private async Task ProcessTradingDecision(TradingDecision decision)
    {
        Console.WriteLine($"📈 Trading Decision Received:");
        Console.WriteLine($"   Timestamp: {decision.timestamp}");
        Console.WriteLine($"   Symbol: {decision.symbol}");
        Console.WriteLine($"   Action: {decision.prediction.action}");
        Console.WriteLine($"   Price: ${decision.prediction.current_price:F2}");
        Console.WriteLine($"   Confidence: Buy={decision.prediction.proba_buy:P2}, Sell={decision.prediction.proba_sell:P2}");
        Console.WriteLine($"   Position Size: {decision.prediction.position_fraction:P2}");
        
        // Apply trading rules
        await ApplyTradingRules(decision);
        
        // Execute the order (mock implementation)
        await ExecuteOrder(decision);
        
        Console.WriteLine("─────────────────────────────────────────");
    }

    private async Task ApplyTradingRules(TradingDecision decision)
    {
        // Risk management rules
        double maxPositionSize = 0.02; // Maximum 2% of portfolio
        double minConfidence = 0.6; // Minimum 60% confidence
        
        var action = decision.prediction.action;
        var confidence = Math.Max(decision.prediction.proba_buy, decision.prediction.proba_sell);
        var adjustedSize = Math.Min(decision.prediction.position_fraction, maxPositionSize);
        
        Console.WriteLine($"🛡️  Risk Management:");
        Console.WriteLine($"   Original Size: {decision.prediction.position_fraction:P2}");
        Console.WriteLine($"   Adjusted Size: {adjustedSize:P2}");
        Console.WriteLine($"   Confidence: {confidence:P2} (min: {minConfidence:P2})");
        
        if (confidence < minConfidence)
        {
            Console.WriteLine($"⚠️  Low confidence - skipping trade");
            return;
        }
        
        if (action == "FLAT")
        {
            Console.WriteLine($"🔄 FLAT signal - no action required");
            return;
        }
        
        // Update decision with adjusted parameters
        decision.prediction.position_fraction = adjustedSize;
        
        await Task.Delay(100); // Simulate processing time
    }

    private async Task ExecuteOrder(TradingDecision decision)
    {
        var action = decision.prediction.action;
        
        if (action == "FLAT")
        {
            return; // No execution needed
        }
        
        Console.WriteLine($"⚡ Executing {action} Order:");
        Console.WriteLine($"   Symbol: {decision.symbol}");
        Console.WriteLine($"   Price: ${decision.prediction.current_price:F2}");
        Console.WriteLine($"   Size: {decision.prediction.position_fraction:P2}");
        
        // Simulate order execution
        await Task.Delay(200);
        
        // Mock execution result
        var orderId = Random.Shared.Next(100000, 999999);
        var executionPrice = decision.prediction.current_price + Random.Shared.NextDouble() * 0.1 - 0.05;
        
        Console.WriteLine($"✅ Order Executed:");
        Console.WriteLine($"   Order ID: {orderId}");
        Console.WriteLine($"   Execution Price: ${executionPrice:F2}");
        Console.WriteLine($"   Status: FILLED");
        
        // Log execution for monitoring
        await LogExecution(decision, orderId, executionPrice);
    }

    private async Task LogExecution(TradingDecision decision, int orderId, double executionPrice)
    {
        var logEntry = new
        {
            timestamp = DateTime.UtcNow.ToString("yyyy-MM-dd HH:mm:ss UTC"),
            order_id = orderId,
            symbol = decision.symbol,
            action = decision.prediction.action,
            execution_price = executionPrice,
            position_size = decision.prediction.position_fraction,
            decision_id = decision.decision_id
        };
        
        var logJson = JsonSerializer.Serialize(logEntry, new JsonSerializerOptions { WriteIndented = true });
        
        // In a real implementation, this would write to a database or log file
        Console.WriteLine($"📝 Execution Log: {logJson}");
        
        await Task.Delay(50); // Simulate logging time
    }

    private async Task DisconnectAsync()
    {
        Console.WriteLine("🔌 Disconnecting WebSocket...");
        
        try
        {
            if (webSocket.State == WebSocketState.Open)
            {
                await webSocket.CloseAsync(WebSocketCloseStatus.NormalClosure, "Executor shutting down", CancellationToken.None);
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"⚠️  Error during disconnect: {ex.Message}");
        }
        finally
        {
            webSocket.Dispose();
            cancellationTokenSource.Dispose();
            Console.WriteLine("✅ WebSocket disconnected");
        }
    }

    public void Stop()
    {
        Console.WriteLine("🛑 Stopping executor...");
        cancellationTokenSource.Cancel();
    }
}