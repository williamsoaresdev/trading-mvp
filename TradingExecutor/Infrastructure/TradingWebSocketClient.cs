using System.Net.WebSockets;
using System.Text;
using System.Text.Json;
using TradingExecutor.Domain.Interfaces;
using TradingExecutor.Domain.Models;

namespace TradingExecutor.Infrastructure.WebSocket;

/// <summary>
/// Implementation of WebSocket client for trading communication.
/// Follows Single Responsibility Principle - only handles WebSocket communication.
/// </summary>
public class TradingWebSocketClient : IWebSocketClient
{
    private readonly ClientWebSocket _webSocket;
    private readonly ITradingLogger _logger;
    
    private bool _disposed = false;
    
    public event EventHandler<TradingDecision>? TradingDecisionReceived;
    public event EventHandler<bool>? ConnectionStatusChanged;
    
    public bool IsConnected => _webSocket.State == WebSocketState.Open;

    public TradingWebSocketClient(ITradingLogger logger)
    {
        _webSocket = new ClientWebSocket();
        _logger = logger ?? throw new ArgumentNullException(nameof(logger));
    }

    /// <summary>
    /// Connect to WebSocket endpoint.
    /// </summary>
    public async Task ConnectAsync(string uri, CancellationToken cancellationToken = default)
    {
        try
        {
            await _logger.LogSystemEventAsync("INFO", $"🔌 Connecting to WebSocket: {uri}");
            
            await _webSocket.ConnectAsync(new Uri(uri), cancellationToken);
            
            await _logger.LogSystemEventAsync("INFO", "✅ WebSocket connected successfully");
            ConnectionStatusChanged?.Invoke(this, true);
        }
        catch (Exception ex)
        {
            await _logger.LogSystemEventAsync("ERROR", "Failed to connect to WebSocket", ex);
            ConnectionStatusChanged?.Invoke(this, false);
            throw;
        }
    }

    /// <summary>
    /// Start listening for WebSocket messages.
    /// </summary>
    public async Task StartListeningAsync(CancellationToken cancellationToken = default)
    {
        var buffer = new byte[4096];
        
        await _logger.LogSystemEventAsync("INFO", "👂 Listening for trading decisions");
        
        try
        {
            while (_webSocket.State == WebSocketState.Open && !cancellationToken.IsCancellationRequested)
            {
                var result = await _webSocket.ReceiveAsync(new ArraySegment<byte>(buffer), cancellationToken);
                
                if (result.MessageType == WebSocketMessageType.Text)
                {
                    var messageJson = Encoding.UTF8.GetString(buffer, 0, result.Count);
                    await ProcessWebSocketMessage(messageJson);
                }
                else if (result.MessageType == WebSocketMessageType.Close)
                {
                    await _logger.LogSystemEventAsync("INFO", "🔚 WebSocket connection closed by server");
                    ConnectionStatusChanged?.Invoke(this, false);
                    break;
                }
            }
        }
        catch (OperationCanceledException)
        {
            await _logger.LogSystemEventAsync("INFO", "🛑 WebSocket operation cancelled");
        }
        catch (Exception ex)
        {
            await _logger.LogSystemEventAsync("ERROR", "Error in WebSocket listening loop", ex);
            ConnectionStatusChanged?.Invoke(this, false);
        }
    }

    /// <summary>
    /// Send message through WebSocket.
    /// </summary>
    public async Task SendMessageAsync(string message, CancellationToken cancellationToken = default)
    {
        if (_webSocket.State != WebSocketState.Open)
        {
            throw new InvalidOperationException("WebSocket is not connected");
        }

        var bytes = Encoding.UTF8.GetBytes(message);
        await _webSocket.SendAsync(new ArraySegment<byte>(bytes), WebSocketMessageType.Text, true, cancellationToken);
    }

    /// <summary>
    /// Disconnect from WebSocket.
    /// </summary>
    public async Task DisconnectAsync()
    {
        try
        {
            await _logger.LogSystemEventAsync("INFO", "🔌 Disconnecting WebSocket");
            
            if (_webSocket.State == WebSocketState.Open)
            {
                await _webSocket.CloseAsync(WebSocketCloseStatus.NormalClosure, "Client shutting down", CancellationToken.None);
            }
            
            ConnectionStatusChanged?.Invoke(this, false);
            await _logger.LogSystemEventAsync("INFO", "✅ WebSocket disconnected");
        }
        catch (Exception ex)
        {
            await _logger.LogSystemEventAsync("WARNING", "Error during WebSocket disconnect", ex);
        }
    }

    /// <summary>
    /// Process incoming WebSocket messages.
    /// </summary>
    private async Task ProcessWebSocketMessage(string messageJson)
    {
        try
        {
            var message = JsonSerializer.Deserialize<WebSocketMessage>(messageJson);
            
            if (message == null)
            {
                await _logger.LogSystemEventAsync("WARNING", "Received null WebSocket message");
                return;
            }

            switch (message.Type.ToLowerInvariant())
            {
                case "trading_decision":
                    await ProcessTradingDecisionMessage(message.Data);
                    break;
                    
                case "status":
                    await _logger.LogSystemEventAsync("INFO", $"📊 Status update: {message.Data}");
                    break;
                    
                default:
                    await _logger.LogSystemEventAsync("INFO", $"📨 Unknown message type: {message.Type}");
                    break;
            }
        }
        catch (JsonException ex)
        {
            await _logger.LogSystemEventAsync("ERROR", "Failed to parse WebSocket message JSON", ex);
        }
        catch (Exception ex)
        {
            await _logger.LogSystemEventAsync("ERROR", "Error processing WebSocket message", ex);
        }
    }

    /// <summary>
    /// Process trading decision messages.
    /// </summary>
    private async Task ProcessTradingDecisionMessage(JsonElement data)
    {
        try
        {
            var decision = JsonSerializer.Deserialize<TradingDecisionDto>(data.GetRawText());
            
            if (decision?.Prediction == null)
            {
                await _logger.LogSystemEventAsync("WARNING", "Received invalid trading decision data");
                return;
            }

            var tradingDecision = new TradingDecision
            {
                DecisionId = decision.Decision_Id?.ToString() ?? Guid.NewGuid().ToString(),
                Timestamp = decision.Timestamp ?? DateTime.Now.ToString("O"),
                Symbol = decision.Symbol ?? "UNKNOWN",
                Prediction = new TradingPrediction
                {
                    Action = decision.Prediction.Action ?? "FLAT",
                    ProbabilityBuy = decision.Prediction.Proba_Buy,
                    ProbabilitySell = decision.Prediction.Proba_Sell,
                    CurrentPrice = (decimal)decision.Prediction.Current_Price,
                    PositionFraction = decision.Prediction.Position_Fraction,
                    AtrPercentage = decision.Prediction.Atr_Pct
                }
            };

            TradingDecisionReceived?.Invoke(this, tradingDecision);
        }
        catch (JsonException ex)
        {
            await _logger.LogSystemEventAsync("ERROR", "Failed to deserialize trading decision", ex);
        }
        catch (Exception ex)
        {
            await _logger.LogSystemEventAsync("ERROR", "Error processing trading decision message", ex);
        }
    }

    /// <summary>
    /// Dispose resources.
    /// </summary>
    public void Dispose()
    {
        if (!_disposed)
        {
            _webSocket?.Dispose();
            _disposed = true;
        }
    }
}

/// <summary>
/// DTO classes for JSON deserialization (internal implementation detail).
/// </summary>
internal class TradingDecisionDto
{
    public string? Timestamp { get; set; }
    public string? Symbol { get; set; }
    public PredictionDto? Prediction { get; set; }
    public long? Decision_Id { get; set; }
}

internal class PredictionDto
{
    public string? Action { get; set; }
    public double Proba_Buy { get; set; }
    public double Proba_Sell { get; set; }
    public double Current_Price { get; set; }
    public double Position_Fraction { get; set; }
    public double Atr_Pct { get; set; }
}