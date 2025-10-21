using TradingExecutor.Domain.Interfaces;
using TradingExecutor.Domain.Models;

namespace TradingExecutor.Infrastructure.Services;

/// <summary>
/// Mock implementation of order executor for safe testing.
/// Follows Single Responsibility Principle - only handles order execution simulation.
/// </summary>
public class MockOrderExecutor : IOrderExecutor
{
    private readonly ITradingLogger _logger;
    private readonly Random _random = new();
    
    public MockOrderExecutor(ITradingLogger logger)
    {
        _logger = logger ?? throw new ArgumentNullException(nameof(logger));
    }

    /// <summary>
    /// Execute a mock trading order.
    /// </summary>
    public async Task<OrderExecutionResult> ExecuteOrderAsync(TradingDecision decision, CancellationToken cancellationToken = default)
    {
        try
        {
            await _logger.LogSystemEventAsync("INFO", $"⚡ Executing {decision.Prediction.Action} Order");
            await _logger.LogSystemEventAsync("INFO", $"   Symbol: {decision.Symbol}");
            await _logger.LogSystemEventAsync("INFO", $"   Price: ${decision.Prediction.CurrentPrice:F2}");
            await _logger.LogSystemEventAsync("INFO", $"   Size: {decision.Prediction.PositionFraction:P2}");
            
            // Simulate order processing time
            await Task.Delay(200, cancellationToken);
            
            // Generate mock execution results
            var orderId = _random.Next(100000, 999999).ToString();
            var priceVariation = (double)(decision.Prediction.CurrentPrice * 0.001m); // 0.1% price variation
            var executionPrice = decision.Prediction.CurrentPrice + (decimal)(_random.NextDouble() * priceVariation * 2 - priceVariation);
            
            var result = new OrderExecutionResult
            {
                OrderId = orderId,
                Symbol = decision.Symbol,
                Action = decision.Prediction.Action,
                ExecutionPrice = executionPrice,
                PositionSize = decision.Prediction.PositionFraction,
                ExecutionTime = DateTime.UtcNow,
                Status = "FILLED"
            };
            
            await _logger.LogSystemEventAsync("INFO", "✅ Order Executed:");
            await _logger.LogSystemEventAsync("INFO", $"   Order ID: {result.OrderId}");
            await _logger.LogSystemEventAsync("INFO", $"   Execution Price: ${result.ExecutionPrice:F2}");
            await _logger.LogSystemEventAsync("INFO", $"   Status: {result.Status}");
            
            return result;
        }
        catch (Exception ex)
        {
            await _logger.LogSystemEventAsync("ERROR", "Order execution failed", ex);
            
            return new OrderExecutionResult
            {
                OrderId = "ERROR",
                Symbol = decision.Symbol,
                Action = decision.Prediction.Action,
                ExecutionPrice = decision.Prediction.CurrentPrice,
                PositionSize = decision.Prediction.PositionFraction,
                ExecutionTime = DateTime.UtcNow,
                Status = "FAILED",
                ErrorMessage = ex.Message
            };
        }
    }
}

/// <summary>
/// Risk management implementation.
/// Follows Single Responsibility Principle - only handles risk calculations and validations.
/// </summary>
public class RiskManager : IRiskManager
{
    private readonly ITradingLogger _logger;
    private readonly RiskManagementConfig _config;
    
    public RiskManager(ITradingLogger logger, IConfigurationProvider configProvider)
    {
        _logger = logger ?? throw new ArgumentNullException(nameof(logger));
        _config = configProvider?.GetRiskManagementConfig() ?? throw new ArgumentNullException(nameof(configProvider));
    }

    /// <summary>
    /// Apply risk management rules to a trading decision.
    /// </summary>
    public async Task<TradingDecision> ApplyRiskManagementAsync(TradingDecision decision)
    {
        if (!_config.EnableRiskManagement)
        {
            await _logger.LogSystemEventAsync("INFO", "Risk management disabled - using original decision");
            return decision;
        }

        var adjustedPositionSize = CalculateAdjustedPositionSize(
            decision.Prediction.PositionFraction,
            decision.Prediction.MaxProbability
        );
        
        var adjustedDecision = decision with
        {
            Prediction = decision.Prediction with
            {
                PositionFraction = adjustedPositionSize
            }
        };
        
        await _logger.LogSystemEventAsync("INFO", "🛡️  Risk Management:");
        await _logger.LogSystemEventAsync("INFO", $"   Original Size: {decision.Prediction.PositionFraction:P2}");
        await _logger.LogSystemEventAsync("INFO", $"   Adjusted Size: {adjustedPositionSize:P2}");
        await _logger.LogSystemEventAsync("INFO", $"   Confidence: {decision.Prediction.MaxProbability:P2} (min: {_config.MinConfidenceThreshold:P2})");
        
        await _logger.LogRiskManagementAsync("POSITION_SIZE_ADJUSTED", decision, adjustedDecision);
        
        return adjustedDecision;
    }

    /// <summary>
    /// Validate if a decision meets risk criteria.
    /// </summary>
    public bool IsDecisionValid(TradingDecision decision)
    {
        if (!_config.EnableRiskManagement)
        {
            return true;
        }

        // Check confidence threshold
        if (!decision.Prediction.MeetsConfidenceThreshold(_config.MinConfidenceThreshold))
        {
            return false;
        }
        
        // Check position size limits
        if (decision.Prediction.PositionFraction > _config.MaxPositionSize)
        {
            return false;
        }
        
        return true;
    }

    /// <summary>
    /// Calculate adjusted position size based on risk parameters.
    /// </summary>
    public double CalculateAdjustedPositionSize(double originalSize, double riskScore)
    {
        if (!_config.EnableRiskManagement)
        {
            return originalSize;
        }

        // Apply maximum position size limit
        var adjustedSize = Math.Min(originalSize, _config.MaxPositionSize);
        
        // Further adjust based on confidence (risk score)
        var confidenceMultiplier = Math.Min(riskScore / _config.MinConfidenceThreshold, 1.0);
        adjustedSize *= confidenceMultiplier;
        
        return Math.Max(adjustedSize, 0.001); // Minimum position size
    }
}

/// <summary>
/// Console-based trading logger implementation.
/// Follows Single Responsibility Principle - only handles logging concerns.
/// </summary>
public class ConsoleTradingLogger : ITradingLogger
{
    /// <summary>
    /// Log a trading decision received.
    /// </summary>
    public Task LogDecisionReceivedAsync(TradingDecision decision)
    {
        Console.WriteLine($"📈 Trading Decision Received:");
        Console.WriteLine($"   Timestamp: {decision.Timestamp}");
        Console.WriteLine($"   Symbol: {decision.Symbol}");
        Console.WriteLine($"   Action: {decision.Prediction.Action}");
        Console.WriteLine($"   Price: ${decision.Prediction.CurrentPrice:F2}");
        Console.WriteLine($"   Confidence: Buy={decision.Prediction.ProbabilityBuy:P2}, Sell={decision.Prediction.ProbabilitySell:P2}");
        Console.WriteLine($"   Position Size: {decision.Prediction.PositionFraction:P2}");
        
        return Task.CompletedTask;
    }

    /// <summary>
    /// Log order execution result.
    /// </summary>
    public Task LogOrderExecutionAsync(OrderExecutionResult result)
    {
        var logEntry = new
        {
            timestamp = result.ExecutionTime.ToString("yyyy-MM-dd HH:mm:ss UTC"),
            order_id = result.OrderId,
            symbol = result.Symbol,
            action = result.Action,
            execution_price = result.ExecutionPrice,
            position_size = result.PositionSize,
            status = result.Status,
            error_message = result.ErrorMessage
        };
        
        var logJson = System.Text.Json.JsonSerializer.Serialize(logEntry, new System.Text.Json.JsonSerializerOptions { WriteIndented = true });
        Console.WriteLine($"📝 Execution Log: {logJson}");
        
        return Task.CompletedTask;
    }

    /// <summary>
    /// Log system events.
    /// </summary>
    public Task LogSystemEventAsync(string level, string message, Exception? exception = null)
    {
        var timestamp = DateTime.Now.ToString("HH:mm:ss");
        var logMessage = $"[{timestamp}] [{level}] {message}";
        
        if (exception != null)
        {
            logMessage += $" - Exception: {exception.Message}";
        }
        
        Console.WriteLine(logMessage);
        
        return Task.CompletedTask;
    }

    /// <summary>
    /// Log risk management actions.
    /// </summary>
    public Task LogRiskManagementAsync(string action, TradingDecision originalDecision, TradingDecision adjustedDecision)
    {
        // In a real implementation, this would log detailed risk management actions
        return Task.CompletedTask;
    }
}

/// <summary>
/// Configuration provider implementation.
/// Follows Single Responsibility Principle - only provides configuration values.
/// </summary>
public class ConfigurationProvider : IConfigurationProvider
{
    private readonly RiskManagementConfig _riskConfig;
    private readonly TradingExecutionConfig _tradingConfig;
    
    public ConfigurationProvider()
    {
        _riskConfig = new RiskManagementConfig
        {
            MaxPositionSize = 0.02, // 2%
            MinConfidenceThreshold = 0.6, // 60%
            MaxDailyLoss = 0.04, // 4%
            EnableRiskManagement = true
        };
        
        _tradingConfig = new TradingExecutionConfig
        {
            EnableRealTrading = false, // Mock trading by default
            OrderTimeout = TimeSpan.FromSeconds(30),
            MaxRetryAttempts = 3
        };
    }
    
    public string GetWebSocketUri() => "ws://localhost:8000/ws";
    
    public RiskManagementConfig GetRiskManagementConfig() => _riskConfig;
    
    public TradingExecutionConfig GetTradingExecutionConfig() => _tradingConfig;
}